"""
内容策展博客 - 以本地 archive 为真相源的个人博客
"""

import hashlib
import json
import html
import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, render_template, abort, request, send_file, redirect, url_for

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

def _quote_anchor(quote):
    """金句锚点 id：归一化文本的短 hash。信号链接与详情页两端用同一 filter
    计算，文本一致即命中；不按 index 定位（金句会被 select-quotes 重排、
    rescore 重建，index 含义会漂移）。任何异常返回空串——锚点是增强功能，
    不能让 today_signal 的导入问题把详情页打成 500。"""
    try:
        import today_signal
        norm = today_signal.quote_text(quote)
        if not norm:
            return ""
        return "q-" + hashlib.sha1(norm.encode("utf-8")).hexdigest()[:8]
    except Exception as e:
        app.logger.warning(f"quote_anchor 降级为空锚点: {e}")
        return ""


def _quote_display(quote):
    """金句展示文本：dict 形态取正文；取不到正文时返回空串，绝不渲染 repr。"""
    try:
        import today_signal
        text = today_signal.quote_text(quote)
    except Exception as e:
        app.logger.warning(f"quote_display 归一化失败: {e}")
        text = ""
    if text:
        return text
    return "" if isinstance(quote, dict) else str(quote or "")

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


def _article_attribution(article):
    """金句卡署名（guest_info→guests→uploader 降级链），供模板拼「复制文字版」。"""
    try:
        import text_card
        name, role = text_card.resolve_attribution({
            "guest_info": article.get("guest_info"),
            "guests": article.get("guests"),
            "uploader": article.get("creator"),
        })
        return f"{name} · {role}" if role else name
    except Exception:
        return str(article.get("creator") or "")


app.jinja_env.filters['quote_anchor'] = _quote_anchor
app.jinja_env.filters['quote_display'] = _quote_display
app.jinja_env.filters['attribution'] = _article_attribution


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
        "current_revision": issue.get("revision") if issue and admin_action == "revise" else None,
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
    # 首页只做一件事：当天的简报（一屏三条），深度库整体在 /library
    store = _issue_store()
    issue = store.latest()
    unrecoverable = store.unrecoverable_dates()
    daily_error = ""
    if unrecoverable and (not issue or max(unrecoverable) >= issue["issue_date"]):
        issue = None
        daily_error = "最新一期暂时无法读取，请稍后再试。"
    return render_template("index.html", library_count=len(load_archive_records()),
                           **_issue_view(issue, is_home=True, daily_error=daily_error))


@app.route("/library")
def library():
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
    return render_template("library.html", records=records, topics=used_topics,
                           topic_counts=topic_counts, verdicts=verdicts)


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


@app.route("/article/<record_id>/quote-card.png")
def quote_card(record_id):
    """文字金句卡（无视频帧）：按（记录, 序号, 金句文本 hash）缓存，
    未命中时 headless Chrome 同步渲染（1-2 秒，单人使用可接受）。
    金句 hash 进缓存键——select-quotes 重排后不会出旧卡。"""
    article = next((r for r in load_archive_records() if r["id"] == record_id), None)
    if not article:
        abort(404)
    quotes = article.get("key_quotes") or []
    try:
        i = int(request.args.get("i", "0"))
    except ValueError:
        abort(404)
    if not (0 <= i < len(quotes)):
        abort(404)

    import text_card
    text = text_card.normalize_quote(quotes[i])
    if not text:
        abort(404)
    h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    out = Path(__file__).parent / "data" / "quote_cards" / f"textcard-{record_id}-{i}-{h}.png"
    if not out.exists():
        name, role = text_card.resolve_attribution({
            "guest_info": article.get("guest_info"),
            "guests": article.get("guests"),
            "uploader": article.get("creator"),
        })
        ok, err_msg = text_card.render_text_card(
            text, name, role, article.get("title", ""),
            article.get("platform", ""), out)
        if not ok:
            print(f"[WARN] 金句卡渲染失败: {err_msg}")
            abort(503)
    # max_age=0：金句 hash 只在服务端文件名里，URL 不变——浏览器缓存会在
    # select-quotes 重排后拆穿「不出旧卡」的承诺，禁用浏览器缓存（服务端有文件缓存）
    return send_file(out, max_age=0)


def _daily_card_key(cached):
    """日卡缓存键：generated_at + 信号/breaking 的 item_id 摘要。
    只用 generated_at 不够——手动 promote 会改 signals 但不改生成时间，
    纯时间键会把 promote 前的旧卡分享出去。"""
    gen = str(cached.get("generated_at") or "")
    sig_ids = ",".join(str(s.get("item_id") or "") if isinstance(s, dict) else ""
                       for s in (cached.get("signals") or []))
    brk = str(((cached.get("breaking") or {}) or {}).get("item_id") or "")
    return hashlib.sha1(f"{gen}|{brk}|{sig_ids}".encode("utf-8")).hexdigest()[:8]


@app.route("/signal-card.png")
def signal_card():
    """今日 AI 判断日卡：横版 1920×1080，同事扫一眼等于看完当天判断。
    缓存按内容键（一天正常只渲一次）；过期缓存照常出卡（用户可能晚发），
    卡上日期如实标注。"""
    import today_signal
    cached = today_signal.read_signal_cache()
    if not cached or not (cached.get("signals") or cached.get("breaking")):
        abort(404)
    import text_card
    gen = str(cached.get("generated_at") or "")
    out = Path(__file__).parent / "data" / "quote_cards" / f"dailycard-{_daily_card_key(cached)}.png"
    if not out.exists():
        ok, err_msg = text_card.render_daily_card(cached, out, date_str=gen[:10])
        if not ok:
            print(f"[WARN] 今日卡渲染失败: {err_msg}")
            abort(503)
    return send_file(out, max_age=0)


# ── 启动 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 默认只监听本机且关闭 debug：Werkzeug 调试器可执行任意代码，
    # 配 0.0.0.0 等于向所在网络开远程后门。开发需要热重载/局域网访问时
    # 用 FLASK_DEBUG=true / BLOG_HOST=0.0.0.0 显式打开。
    app.run(
        debug=os.getenv("FLASK_DEBUG", "").lower() == "true",
        host=os.getenv("BLOG_HOST", "127.0.0.1"),
        port=int(os.getenv("BLOG_PORT", "5055")),
    )
