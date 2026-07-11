"""
内容策展博客 - 以本地 archive 为真相源的个人博客
"""

import hashlib
import json
import html
import time
from pathlib import Path

from flask import Flask, render_template, abort, request, send_file

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

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['markdown'] = _render_markdown
app.jinja_env.filters['strip_md'] = _strip_markdown
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
    # 今日判断（页面只读缓存，永不阻塞；缓存由 `run.sh signals` 后台生成）
    signals = []
    breaking = None
    attention = []
    signal_meta = {}
    signal_ran = False  # 区分「已生成但降噪后为 0」与「从未生成」
    try:
        import today_signal
        cached = today_signal.read_signal_cache()
        signal_ran = cached is not None
        signal_meta = today_signal.enrich_cached_link_quotes(
            cached if cached is not None else today_signal.missing_signal_state(),
            records,
        )
        signals = signal_meta.get("signals") or []
        breaking = signal_meta.get("breaking")
        attention = signal_meta.get("attention") or []
    except Exception as e:
        print(f"[WARN] 今日判断读取失败（不影响页面）: {e}")
    return render_template("index.html", records=records, topics=used_topics,
                           topic_counts=topic_counts, verdicts=verdicts,
                           breaking=breaking, signals=signals, attention=attention,
                           signal_meta=signal_meta, signal_ran=signal_ran)


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


@app.route("/ingest", methods=["GET", "POST"])
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
def ingest_status():
    import ingest_jobs
    job_id = request.args.get("job_id", "")
    job = ingest_jobs.get_job(job_id)
    if not job:
        return {"status": "not_found"}, 404
    return job


@app.route("/signal/attention", methods=["POST"])
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


# ── 启动 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5055)
