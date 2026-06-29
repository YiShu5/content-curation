"""
内容策展博客 - 基于飞书多维表格的个人博客
"""

import json
import html
import os
import time
from pathlib import Path

import requests
from flask import Flask, render_template, abort, Response, request, send_file

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

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['markdown'] = _render_markdown
app.jinja_env.filters['strip_md'] = _strip_markdown

# 启动时检查必要配置
_missing = [k for k in ("FEISHU_APP_ID", "FEISHU_APP_SECRET", "BASE_ID", "TABLE_ID")
            if not app.config.get(k)]
if _missing:
    import sys
    print(f"[ERROR] 缺少飞书配置项: {', '.join(_missing)}，请检查 config/.env", file=sys.stderr)

# ── 飞书 API ──────────────────────────────────────────────────────────────
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
TOPICS = ['AI 前沿', 'AI 产品', 'AI 创业', 'AI 商业', 'AI 编程', '投资', '个人效率', '其他']


@app.route("/")
def index():
    records = load_archive_records()
    # 只保留实际有内容的话题（带数量）
    used_topics = [t for t in TOPICS if any(r.get("topic") == t for r in records)]
    topic_counts = {t: sum(1 for r in records if r.get("topic") == t) for t in used_topics}
    # 质量评级（按固定顺序，只保留出现过的，带数量）
    _verdict_order = ["必读", "强烈推荐", "推荐", "一般", "可跳过"]
    _vc = {}
    for r in records:
        v = r.get("score_verdict")
        if v:
            _vc[v] = _vc.get(v, 0) + 1
    verdicts = [{"name": v, "count": _vc[v]} for v in _verdict_order if v in _vc]
    # 今日必读（页面只读缓存，永不阻塞；缓存由 `run.sh signals` 后台生成）
    signals = []
    signal_ran = False  # 区分「已生成但降噪后为 0」与「从未生成」
    try:
        import today_signal
        cached = today_signal.read_signals()
        signal_ran = cached is not None
        signals = cached or []
    except Exception as e:
        print(f"[WARN] 今日必读读取失败（不影响页面）: {e}")
    return render_template("index.html", records=records, topics=used_topics,
                           topic_counts=topic_counts, verdicts=verdicts,
                           signals=signals, signal_ran=signal_ran)


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


@app.route("/ingest")
def ingest():
    """必读驱动入库：抓取指定 YouTube 视频 → 改写 → 重建向量索引（后台跑，立即返回）。"""
    url = request.args.get("url", "")
    if not _re.match(r'^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}', url):
        return {"status": "bad_url"}, 400
    import subprocess
    import shlex
    root = Path(__file__).parent.parent
    cmd = (f'cd {shlex.quote(str(root))} && '
           f'.venv/bin/python scripts/fetch.py --url {shlex.quote(url)} && '
           f'bash run.sh refresh')
    subprocess.Popen(["bash", "-lc", cmd],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return {"status": "started"}


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
