"""
内容策展博客 - 基于飞书多维表格的个人博客
"""

import json
import html
import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from flask import Flask, render_template, abort, Response, request, send_file, redirect, url_for

import re as _re
from urllib.parse import quote as _urlquote

try:
    import markdown as _md_lib
    def _render_markdown(text):
        # Fix AI-generated double heading markers e.g. "### ### 子标题"
        text = _re.sub(r'^(#{1,6}) +#{1,6} +', r'\1 ', text or '', flags=_re.MULTILINE)
        return _md_lib.markdown(text, extensions=['extra'])
except ImportError:
    def _render_markdown(text):
        return html.escape(text or '').replace('\n', '<br>')

def _strip_markdown(text):
    """剥除 Markdown 符号，返回纯文本（用于摘要预览）"""
    if not text:
        return ''
    t = text
    t = _re.sub(r'#{1,6}\s+', '', t)           # 标题
    t = _re.sub(r'\*\*(.+?)\*\*', r'\1', t)    # 粗体
    t = _re.sub(r'\*(.+?)\*', r'\1', t)        # 斜体
    t = _re.sub(r'`{3}[\s\S]*?`{3}', '', t)    # 代码块
    t = _re.sub(r'`(.+?)`', r'\1', t)          # 行内代码
    t = _re.sub(r'^\s*[-*+]\s+', '', t, flags=_re.MULTILINE)  # 无序列表
    t = _re.sub(r'^\s*\d+\.\s+', '', t, flags=_re.MULTILINE)  # 有序列表
    t = _re.sub(r'\[(.+?)\]\(.+?\)', r'\1', t) # 链接
    t = _re.sub(r'^>\s*', '', t, flags=_re.MULTILINE)  # 引用
    t = _re.sub(r'\n{2,}', ' ', t)             # 多行变空格
    t = _re.sub(r'\n', ' ', t)
    return t.strip()

# 优先加载项目根目录的 config/.env（开发环境无需手动设置系统变量）
_env_path = Path(__file__).parent.parent / "config" / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass  # dotenv 未安装时跳过，依赖系统环境变量

from config import Config
from product_schema import TOPICS
import admin_auth
from daily_issues import (
    DAILY_TEXT_LIMITS,
    DailyIssueCorrupt,
    DailyIssueConflict,
    DailyIssueStore,
    DailyIssueValidationError,
    format_share_text,
    validate_issue_date,
)
import daily_editor

app = Flask(__name__)
app.config.from_object(Config)
if app.config["BLOG_ADMIN_PASSWORD"] and app.config["SECRET_KEY"] == "content-curation-blog-2026":
    raise RuntimeError("set a private SECRET_KEY before enabling admin login")
app.jinja_env.filters['markdown'] = _render_markdown
app.jinja_env.filters['strip_md'] = _strip_markdown


@app.context_processor
def admin_template_context():
    return {
        "is_admin": admin_auth.is_admin(),
        "admin_csrf_token": admin_auth.csrf_token() if admin_auth.is_admin() else "",
    }


@app.after_request
def prevent_admin_cache(response):
    if (
        request.path.startswith(("/admin/", "/ingest", "/signal/attention"))
        or (admin_auth.is_admin() and response.mimetype == "text/html")
    ):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_auth.validate_csrf()
        if not admin_auth.login_admin(request.form.get("password", "")):
            return render_template("admin_login.html", error="密码不正确", csrf_token=admin_auth.csrf_token()), 401
        return redirect(url_for("index"))
    return render_template("admin_login.html", error="", csrf_token=admin_auth.csrf_token())


@app.post("/admin/logout")
@admin_auth.admin_required
def admin_logout():
    admin_auth.logout_admin()
    return redirect(url_for("index"))

# ── 飞书 API（legacy，博客已改读本地 archive，不再调用）──────────────────────
_token_cache = {"token": "", "expiry": 0}


def get_access_token():
    if _token_cache["token"] and time.time() < _token_cache["expiry"] - 60:
        return _token_cache["token"]
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/",
        json={
            "app_id": app.config["FEISHU_APP_ID"],
            "app_secret": app.config["FEISHU_APP_SECRET"],
        },
        timeout=15,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"飞书 Token 获取失败: {data}")
    _token_cache["token"] = data["app_access_token"]
    _token_cache["expiry"] = time.time() + data["expire"]
    return _token_cache["token"]


# ── 数据缓存 ──────────────────────────────────────────────────────────────
_data_cache = {"records": [], "expiry": 0}


def fetch_records():
    now = time.time()
    if _data_cache["records"] and now < _data_cache["expiry"]:
        return _data_cache["records"]

    token = get_access_token()
    base_id = app.config["BASE_ID"]
    table_id = app.config["TABLE_ID"]

    # 使用 list API（比 search API 权限要求更低，且能直接返回字段内容）
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_id}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}

    all_records = []
    page_token = None

    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token

        resp = requests.get(url, headers=headers, params=params, timeout=15)
        data = resp.json()

        if data.get("code") != 0:
            raise RuntimeError(f"飞书查询失败: {data}")

        items = data.get("data", {}).get("items", [])
        for item in items:
            fields = item.get("fields", {})
            record_id = item.get("record_id", "")

            # 跳过空记录
            if not fields:
                continue

            # 处理封面附件 - 保存 file_token 用于代理下载
            cover_token = ""
            cover_field = fields.get("封面")
            if isinstance(cover_field, list) and cover_field:
                cover_token = cover_field[0].get("file_token", "")

            # 处理链接字段
            link = fields.get("原始链接", "")
            if isinstance(link, dict):
                link = link.get("link", "")

            # 处理日期字段（飞书返回 ms 时间戳）
            pub_date = fields.get("发布日期", "")
            if isinstance(pub_date, (int, float)):
                pub_date = time.strftime("%Y-%m-%d", time.localtime(pub_date / 1000))

            # 总分/评级作为兜底（archive 缺失时显示个大概）；评分细分维度统一由
            # _enrich_from_local 用本地 archive 的新评分体系填充。飞书表里的旧维度列
            # （AI相关性/故事性/加分项）已废弃，不再读取。
            score_total = _num_value(fields.get("总分"))

            all_records.append({
                "id": record_id,
                "title": _text_value(fields.get("标题", "")),
                "original_title": _text_value(fields.get("原标题", "")),
                "platform": _text_value(fields.get("来源平台", "")),
                "creator": _text_value(fields.get("创作者", "")),
                "pub_date": pub_date,
                "link": link,
                "duration": fields.get("时长（分钟）", 0),
                "guests": _text_value(fields.get("嘉宾", "")),
                "summary": _text_value(fields.get("深度摘要", "")),
                "cover_token": cover_token,
                "topic": _text_value(fields.get("话题", "")),
                "score_total": score_total,
                "score_verdict": _text_value(fields.get("评级", "")),
                "scores": {},
            })

        if not data.get("data", {}).get("has_more"):
            break
        page_token = data["data"].get("page_token")

    _data_cache["records"] = all_records
    _data_cache["expiry"] = now + app.config["CACHE_TTL"]
    return all_records


def _text_value(field):
    """提取飞书字段的文本值（可能是纯文本或富文本结构）"""
    if isinstance(field, str):
        return field
    if isinstance(field, list):
        # 富文本: [{"type": "text", "text": "..."}]
        return "".join(item.get("text", "") for item in field if isinstance(item, dict))
    if isinstance(field, dict):
        return field.get("text", "") or field.get("value", "") or str(field)
    return str(field) if field else ""


def _num_value(field):
    """提取飞书数字字段，无值/无法解析返回 None"""
    if isinstance(field, (int, float)):
        return field
    if isinstance(field, str) and field.strip():
        try:
            return float(field) if "." in field else int(field)
        except ValueError:
            return None
    return None


# ── 本地 archive 作为真相源（不依赖飞书）─────────────────────────────────────
_PLATFORM_LABELS = {"youtube": "YouTube", "bilibili": "Bilibili",
                    "xiaoyuzhou": "小宇宙", "audio": "音频"}
_archive_cache = {"records": [], "expiry": 0}


def load_archive_records():
    """直接从本地 archive/*/metadata.json 读取记录，作为博客真相源。
    metadata 已含全部展示字段（标题/评分/金句/嘉宾等），无需再 enrich。"""
    now = time.time()
    if _archive_cache["records"] and now < _archive_cache["expiry"]:
        return _archive_cache["records"]
    records = []
    root = Path(__file__).parent.parent / "archive"
    if root.exists():
        # 目录名以 upload_date 开头，倒序 = 最新在前
        for d in sorted((p for p in root.iterdir() if p.is_dir()),
                        key=lambda p: p.name, reverse=True):
            mp = d / "metadata.json"
            if not mp.exists():
                continue
            try:
                m = json.loads(mp.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not m.get("rewrite_complete"):
                continue
            up = str(m.get("upload_date") or "")
            pub = f"{up[:4]}-{up[4:6]}-{up[6:8]}" if len(up) == 8 else ""
            dur = m.get("duration") or 0
            cover = next((c.name for c in sorted(d.glob("cover.*"))), "")
            guests = m.get("guests") or []
            records.append({
                "id": m.get("id") or d.name,
                "title": m.get("chinese_title") or m.get("title", ""),
                "original_title": m.get("title", ""),
                "platform": _PLATFORM_LABELS.get(m.get("platform", ""), m.get("platform", "")),
                "creator": m.get("uploader", ""),
                "pub_date": pub,
                "link": m.get("url", ""),
                "duration": round(dur / 60) if dur else 0,
                "guests": "、".join(guests) if isinstance(guests, list) else (guests or ""),
                "summary": m.get("deep_summary", ""),
                "cover_url": f"/cover-local/{_urlquote(d.name)}" if cover else "",
                "topic": m.get("topic", ""),
                "score_total": m.get("score_total"),
                "score_verdict": m.get("score_verdict", ""),
                "scores": m.get("scores", {}),
                "key_quotes": m.get("key_quotes", []),
                "core_ideas": m.get("core_ideas", []),
                "key_insights": m.get("key_insights", ""),
                "summary_md": m.get("deep_summary", ""),
                "why_watch": m.get("why_watch", ""),
                "guest_info": m.get("guest_info", []),
            })
    _archive_cache["records"] = records
    _archive_cache["expiry"] = now + 30  # 30s 轻缓存，新抓内容很快可见
    return records


# ── 路由 ──────────────────────────────────────────────────────────────────
def _issue_store():
    return DailyIssueStore(
        Path(app.config["DAILY_ISSUES_DIR"]),
        app.config["BLOG_TIMEZONE"],
    )


def _local_now():
    return datetime.now(ZoneInfo(app.config["BLOG_TIMEZONE"]))


def _stable_issue_url(issue_date):
    base = str(app.config.get("PUBLIC_BASE_URL") or "").rstrip("/")
    if base:
        return f"{base}/daily/{issue_date}"
    return url_for("daily_issue", issue_date=issue_date, _external=True)


def _issue_view(issue, *, is_home, daily_error=""):
    today = _local_now().date().isoformat()
    issue_date = issue.get("issue_date") if issue else ""
    canonical = _stable_issue_url(issue_date) if issue_date else ""
    admin = admin_auth.is_admin()
    admin_action = "publish" if is_home and issue_date != today else ("revise" if issue else "publish")
    admin_target_date = issue_date if admin_action == "revise" else today
    public_base = str(app.config.get("PUBLIC_BASE_URL") or request.url_root).rstrip("/")
    draft_available = True
    draft_message = ""
    if admin:
        try:
            if admin_action == "revise":
                _issue_store().assert_revisable(admin_target_date)
            else:
                _issue_store().next_issue_number()
                import today_signal
                daily_editor.trusted_draft(
                    today_signal.read_signal_cache() or {}, expected_date=today
                )
        except (DailyIssueCorrupt, DailyIssueConflict, ValueError) as exc:
            draft_available = False
            draft_message = str(exc)
    return {
        "issue": issue,
        "daily_error": daily_error,
        "is_home": is_home,
        "is_current_day": issue_date == today,
        "canonical_url": canonical,
        "og_image_url": f"{public_base}/static/og-daily.png",
        "share_text": format_share_text(issue, canonical) if issue else "",
        "is_admin": admin,
        "admin_action": admin_action,
        "admin_target_date": admin_target_date,
        "current_issue_date": today,
        "csrf_token": admin_auth.csrf_token() if admin else "",
        "draft_available": draft_available,
        "draft_message": draft_message,
        "editor_limits": DAILY_TEXT_LIMITS if admin else {},
    }


def _trusted_editor_draft(issue_date, *, today, store):
    import today_signal
    published = store.get(issue_date)
    if published:
        published = store.assert_revisable(issue_date)
        current = None
        if issue_date == today:
            try:
                current = daily_editor.trusted_draft(
                    today_signal.read_signal_cache() or {}, expected_date=today
                )
            except ValueError:
                pass
        return daily_editor.revision_draft(published, current), published
    if issue_date != today:
        return None, None
    return daily_editor.trusted_draft(
        today_signal.read_signal_cache() or {}, expected_date=today
    ), None


def _selected_attention(draft, selected_topics):
    selected_ids = {str(row.get("topic_id") or "") for row in selected_topics}
    result, seen = [], set()
    for row in draft.get("attention") or []:
        topic_id = str(row.get("topic_id") or "")
        if not topic_id or topic_id in selected_ids or topic_id in seen or len(result) >= 3:
            continue
        item = dict(row)
        item["attention_status"] = item.get("attention_status") or "watch"
        result.append(item)
        seen.add(topic_id)
    return result


@app.get("/admin/daily/draft")
@admin_auth.admin_required
def admin_daily_draft():
    today = _local_now().date().isoformat()
    issue_date = request.args.get("date") or today
    try:
        validate_issue_date(issue_date)
        store = _issue_store()
        draft, published = _trusted_editor_draft(issue_date, today=today, store=store)
        if draft is None:
            return {"status": "not_found"}, 404
        issue_number = published["issue_number"] if published else store.next_issue_number()
    except DailyIssueValidationError as exc:
        return {"status": "bad_date", "message": str(exc)}, 400
    except DailyIssueCorrupt as exc:
        return {"status": "storage_corrupt", "code": "storage_corrupt", "message": str(exc)}, 503
    except ValueError as exc:
        return {"status": "unavailable", "message": str(exc)}, 409
    return {"status": "ok", "draft": draft, "published": published,
            "issue_meta": {"issue_date": issue_date, "issue_number": issue_number,
                           "revision": published["revision"] if published else 0,
                           "generated_at": draft.get("generated_at") or ""}}


def _editor_request(issue_date, action):
    today = _local_now().date().isoformat()
    body = request.get_json(silent=True)
    if body is None:
        body = {}
    if not isinstance(body, dict):
        return {"status": "bad_request", "message": "JSON 请求体必须为对象"}, 400
    try:
        validate_issue_date(issue_date)
        if action == "publish" and issue_date != today:
            return {"status": "unavailable", "message": "首次发布仅限当日"}, 409
        store = _issue_store()
        try:
            draft, published = _trusted_editor_draft(issue_date, today=today, store=store)
        except ValueError as exc:
            return {"status": "unavailable", "message": str(exc)}, 409
        if action == "publish" and published:
            return {"status": "conflict", "code": "already_published"}, 409
        if action in {"preview", "revise"} and issue_date != today and not published:
            return {"status": "not_found"}, 404
        if draft is None:
            return {"status": "unavailable"}, 409
        selected = daily_editor.apply_selection(draft, body.get("topics"))
        attention = _selected_attention(draft, selected)
        if action == "preview":
            surface = body.get("preview_surface")
            if surface not in {"home", "dated"}:
                return {"status": "bad_request", "message": "preview_surface 无效"}, 400
            issue = store.preview(issue_date, selected, attention, now=_local_now())
            rendered = render_template("_daily_brief.html", issue=issue, daily_error="",
                                       is_home=surface == "home", is_current_day=issue_date == today)
            return {"status": "ok", "html": rendered}
        if action == "publish":
            issue = store.publish(issue_date, selected, attention, now=_local_now())
            status_code, event_kind = 201, "publish"
        else:
            expected = body.get("expected_revision")
            if isinstance(expected, bool) or not isinstance(expected, int):
                return {"status": "bad_request", "message": "expected_revision 必须为整数"}, 400
            issue = store.revise(issue_date, selected, attention,
                                 expected_revision=expected, now=_local_now())
            status_code, event_kind = 200, "revise"
        audit_status = "ok"
        try:
            daily_editor.append_editor_event(Path(app.config["DAILY_EDITOR_LOG"]), {
                "kind": event_kind, "issue_date": issue_date, "revision": issue["revision"],
                "draft_topic_ids": [str(row.get("topic_id") or "") for group in ("topics", "candidates", "attention") for row in draft.get(group) or []],
                "published_topic_ids": [row["topic_id"] for row in selected],
            }, now=_local_now())
        except Exception:
            audit_status = "failed"
            app.logger.exception("daily issue committed but editor audit append failed")
        return {"status": "ok", "issue": issue,
                "redirect_url": _stable_issue_url(issue_date),
                "audit_status": audit_status}, status_code
    except DailyIssueCorrupt:
        return {"status": "storage_corrupt", "code": "storage_corrupt"}, 503
    except DailyIssueConflict:
        code = "already_published" if action == "publish" else "revision_conflict"
        return {"status": "conflict", "code": code}, 409
    except (DailyIssueValidationError, ValueError) as exc:
        return {"status": "bad_request", "message": str(exc)}, 400
    except Exception:
        app.logger.exception("daily editor persistence failed")
        return {"status": "error"}, 500


@app.post("/admin/daily/<issue_date>/preview")
@admin_auth.admin_required
def admin_daily_preview(issue_date):
    return _editor_request(issue_date, "preview")


@app.post("/admin/daily/<issue_date>/publish")
@admin_auth.admin_required
def admin_daily_publish(issue_date):
    return _editor_request(issue_date, "publish")


@app.post("/admin/daily/<issue_date>/revise")
@admin_auth.admin_required
def admin_daily_revise(issue_date):
    return _editor_request(issue_date, "revise")


@app.route("/")
def index():
    records = load_archive_records()
    # 只保留实际有内容的话题（带数量），按出现频次优先展示，方便顶部筛选栏先露出高频标签。
    raw_topic_counts = {t: sum(1 for r in records if r.get("topic") == t) for t in TOPICS}
    used_topics = sorted(
        [t for t in TOPICS if raw_topic_counts.get(t, 0) > 0],
        key=lambda t: (-raw_topic_counts.get(t, 0), TOPICS.index(t))
    )
    topic_counts = {t: raw_topic_counts[t] for t in used_topics}
    # 质量评级（按固定顺序，只保留出现过的，带数量）
    _verdict_order = ["必读", "强烈推荐", "推荐", "一般", "可跳过"]
    _vc = {}
    for r in records:
        v = r.get("score_verdict")
        if v:
            _vc[v] = _vc.get(v, 0) + 1
    verdicts = [{"name": v, "count": _vc[v]} for v in _verdict_order if v in _vc]
    store = _issue_store()
    issue = store.latest()
    unrecoverable = store.unrecoverable_dates()
    daily_error = ""
    if unrecoverable and (not issue or max(unrecoverable) >= issue["issue_date"]):
        issue = None
        daily_error = "最新一期暂时无法读取，请稍后再试。"
    return render_template("index.html", records=records, topics=used_topics,
                           topic_counts=topic_counts, verdicts=verdicts,
                           **_issue_view(issue, is_home=True, daily_error=daily_error))


@app.get("/daily")
def daily_archive():
    return render_template("daily_archive.html", issues=_issue_store().list_issues())


@app.get("/daily/<issue_date>")
def daily_issue(issue_date):
    try:
        validate_issue_date(issue_date)
    except (ValueError, DailyIssueValidationError):
        abort(404)
    try:
        issue = _issue_store().get(issue_date)
    except DailyIssueCorrupt:
        app.logger.exception("daily issue snapshot is corrupt")
        return render_template("daily_unavailable.html", issue_date=issue_date), 503
    if not issue:
        abort(404)
    return render_template("daily.html", **_issue_view(issue, is_home=False))


# 本地 archive 索引缓存：
#   by_rid: { feishu_record_id -> meta }（已同步内容）
#   by_key: { 内容键(视频id) -> meta }（按 URL 匹配，兼容重跑生成、未回填 record_id 的 archive）
# loaded 标记区分「尚未构建」与「构建结果为空」，避免空 archive 每次请求重复扫描
_local_index_cache = {"by_rid": {}, "by_key": {}, "expiry": 0, "loaded": False}


def _content_key(url):
    """从 URL 提取稳定内容键，用于把飞书记录与本地 archive 对应起来
    （视频 id 比 record_id 稳定，且能让同一视频的多条记录共享同一份归档）"""
    if not url:
        return ""
    m = _re.search(r'(?:youtu\.be/|[?&]v=|/embed/|/shorts/)([A-Za-z0-9_-]{11})', url)
    if m:
        return "yt:" + m.group(1)
    m = _re.search(r'xiaohongshu\.com/explore/([A-Za-z0-9]+)', url)
    if m:
        return "xhs:" + m.group(1)
    m = _re.search(r'(BV[A-Za-z0-9]+)', url)
    if m:
        return "bili:" + m.group(1)
    return url.split('?')[0].rstrip('/')


def _build_local_index():
    now = time.time()
    if _local_index_cache["loaded"] and now < _local_index_cache["expiry"]:
        return
    by_rid, by_key = {}, {}
    archive_root = Path(__file__).parent.parent / "archive"
    if archive_root.exists():
        for d in archive_root.iterdir():
            if not d.is_dir():
                continue
            meta_path = d / "metadata.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not meta.get("rewrite_complete"):
                continue  # 跳过转录/改写未完成的归档
            rid = meta.get("feishu_record_id")
            if rid:
                by_rid[rid] = meta
            key = _content_key(meta.get("url") or "")
            if key:
                by_key.setdefault(key, meta)  # 同一视频多份归档时，先扫到的优先
    _local_index_cache["by_rid"] = by_rid
    _local_index_cache["by_key"] = by_key
    _local_index_cache["loaded"] = True
    _local_index_cache["expiry"] = now + app.config["CACHE_TTL"]


def _enrich_from_local(article):
    """从本地 archive 的 metadata.json 补充金句、核心观点、评分等详细数据。
    先按 feishu_record_id 匹配，再按内容键(视频id)兜底。"""
    _build_local_index()
    meta = _local_index_cache["by_rid"].get(article["id"])
    if not meta:
        meta = _local_index_cache["by_key"].get(_content_key(article.get("link") or ""))
    if meta:
        # 优先使用本地中文标题（防止飞书中存的是英文标题）
        cn_title = meta.get("chinese_title", "")
        if cn_title and cn_title != article.get("title"):
            article["title"] = cn_title
        article["key_quotes"] = meta.get("key_quotes", [])
        article["core_ideas"] = meta.get("core_ideas", [])
        article["key_insights"] = meta.get("key_insights", "")
        article["summary_md"] = meta.get("deep_summary", "")
        article["why_watch"] = meta.get("why_watch", "")
        article["score_total"] = meta.get("score_total")
        article["score_verdict"] = meta.get("score_verdict", "")
        article["scores"] = meta.get("scores", {})
        article["guest_info"] = meta.get("guest_info", [])
        if not article["guests"] and meta.get("guests"):
            article["guests"] = "、".join(meta["guests"])
    else:
        article.setdefault("key_quotes", [])
        article.setdefault("core_ideas", [])
        article.setdefault("key_insights", "")
        article.setdefault("summary_md", "")
        article.setdefault("why_watch", "")
        article.setdefault("score_total", None)
        article.setdefault("score_verdict", "")
        article.setdefault("scores", {})
        article.setdefault("guest_info", [])
    return article


# 问句型查询的标志词（命中则走「AI 综合回答」，否则纯列卡片）
_Q_MARKERS = ("?", "？", "啥", "什么", "怎么", "如何", "为什么", "哪些", "哪几", "哪个",
              "对比", "区别", "总结", "概况", "趋势", "看法", "观点", "这周", "本周",
              "最近", "有什么", "讲了", "聊了", "发生", "盘点", "现状")


def _is_question(q):
    return any(m in q for m in _Q_MARKERS)


@app.route("/search")
def search():
    query = (request.args.get("q") or "").strip()
    if not query:
        return render_template("search.html", query="", results=[], answer="", error="")

    records = load_archive_records()
    import embeddings
    import today_signal
    try:
        hits = embeddings.search(query, records)
    except embeddings.EmbeddingError as e:
        return render_template("search.html", query=query, results=[], answer="", error=str(e))
    except Exception as e:
        print(f"[ERROR] 语义搜索失败: {e}")
        return render_template("search.html", query=query, results=[], answer="",
                               error="语义搜索出错，请稍后重试。")

    # 把相似度分附到 record 上，方便模板展示
    results = []
    for rec, score in hits:
        rec = dict(rec)
        rec["score"] = round(score * 100)
        results.append(rec)

    # 问句型查询 → 综合「库 + 本周 AI HOT」生成一段 AI 回答（智能判断；失败不影响列表）
    answer = ""
    if _is_question(query):
        try:
            answer = today_signal.answer_query(query, results)  # 用全量 top 结果作上下文
        except Exception as e:
            print(f"[WARN] AI 回答生成失败: {e}")
        if answer:
            results = results[:4]  # 有回答时，卡片只留少量「依据」，不刷屏

    return render_template("search.html", query=query, results=results, answer=answer, error="")


@app.route("/article/<record_id>")
def detail(record_id):
    records = load_archive_records()
    article = next((r for r in records if r["id"] == record_id), None)
    if not article:
        abort(404)

    # 相关推荐（基于向量索引，零 API 成本；索引缺失/出错时静默跳过）
    related = []
    try:
        import embeddings
        for rec, score in embeddings.related(record_id, records):
            rec = dict(rec)
            rec["score"] = round(score * 100)
            related.append(rec)
    except Exception as e:
        print(f"[WARN] 相关推荐生成失败: {e}")

    return render_template("detail.html", article=article, related=related)


@app.post("/ingest")
@admin_auth.admin_required
def ingest():
    """加入深度库：创建本地 job，后台抓取 YouTube → 改写 → 重建索引。"""
    import ingest_jobs
    body = request.get_json(silent=True) or {}
    url = body.get("url") or request.args.get("url", "")
    title = body.get("title") or request.args.get("title", "")
    job = ingest_jobs.start_job(url, title=title)
    if job.get("status") == "bad_url":
        return job, 400
    return job


@app.route("/ingest/status")
@admin_auth.admin_required
def ingest_status():
    import ingest_jobs
    job_id = request.args.get("job_id", "")
    job = ingest_jobs.get_job(job_id)
    if not job:
        return {"status": "not_found"}, 404
    return job


@app.route("/signal/attention", methods=["POST"])
@admin_auth.admin_required
def signal_attention():
    """处理“热议浮现”提示：用户可手动加入首页，或先不加。"""
    body = request.get_json(silent=True) or {}
    item_id = str(body.get("item_id") or "").strip()
    action = str(body.get("action") or "").strip()
    if not item_id or action not in {"promote", "dismiss"}:
        return {"status": "bad_request"}, 400
    try:
        import today_signal
        cache = today_signal.read_signal_cache() or {}
        if action == "promote":
            updated, changed = today_signal.promote_attention_item(cache, item_id)
            kind = "promote_attention"
        else:
            updated, changed = today_signal.dismiss_attention_item(cache, item_id)
            kind = "dismiss_attention"

        if changed:
            # 同步写一条正向/选择日志；先不加不作为负反馈，只记录真实生效的用户选择。
            log = Path(__file__).parent / "data" / "clicks.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            rec = {
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
                "kind": kind,
                "label": str(body.get("label", ""))[:120],
                "href": str(body.get("href", ""))[:300],
                "slot": "attention",
                "source": str(body.get("source", ""))[:80],
                "item_id": item_id[:80],
            }
            with open(log, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return {
            "status": "ok" if changed else "not_found",
            "signals": len(updated.get("signals") or []),
            "attention": len(updated.get("attention") or []),
        }
    except Exception as e:
        print(f"[WARN] 热议浮现处理失败: {e}")
        return {"status": "error"}, 500


@app.route("/track", methods=["POST"])
def track():
    """极轻点击埋点：记录今日必读/卡片被点了什么，写本地日志 data/clicks.log
    （供日后判断"哪些内容对 AI 产品人真有用"）。永不报错、不阻塞。"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        rec = {
            "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            "kind": str(data.get("kind", ""))[:20],
            "label": str(data.get("label", ""))[:120],
            "href": str(data.get("href", ""))[:300],
            "slot": str(data.get("slot", ""))[:40],
            "source": str(data.get("source", ""))[:80],
            "item_id": str(data.get("item_id", ""))[:80],
        }
        log = Path(__file__).parent / "data" / "clicks.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return ("", 204)


@app.route("/cover-local/<name>")
def cover_local(name):
    """从本地 archive 目录返回封面图（博客读 archive 模式下用）"""
    if "/" in name or ".." in name:
        abort(404)
    d = Path(__file__).parent.parent / "archive" / name
    covers = sorted(d.glob("cover.*")) if d.is_dir() else []
    if not covers:
        abort(404)
    return send_file(covers[0], max_age=86400)


@app.route("/cover/<file_token>")
def cover_proxy(file_token):
    """代理飞书附件下载（因为附件 URL 需要认证）"""
    try:
        token = get_access_token()
        resp = requests.get(
            f"https://open.feishu.cn/open-apis/drive/v1/medias/{file_token}/download",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "image/jpeg")
        return Response(resp.content, content_type=content_type,
                        headers={"Cache-Control": "public, max-age=86400"})
    except Exception:
        abort(404)


# ── 启动 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5055)
