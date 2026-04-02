"""
内容策展博客 - 基于飞书多维表格的个人博客
"""

import json
import os
import time
from pathlib import Path

import requests
from flask import Flask, render_template, abort, Response

import re as _re

try:
    import markdown as _md_lib
    def _render_markdown(text):
        return _md_lib.markdown(text or '', extensions=['extra'])
except ImportError:
    def _render_markdown(text):
        return (text or '').replace('\n', '<br>')

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


# ── 路由 ──────────────────────────────────────────────────────────────────
TOPICS = ['AI 编程', 'AI 产品', 'AI 创业', 'AI 商业', '投资', '个人效率', '其他']


@app.route("/")
def index():
    try:
        records = fetch_records()
    except Exception as e:
        records = []
        print(f"[ERROR] 获取数据失败: {e}")
    # 用本地 archive 的中文标题覆盖可能的英文标题
    for r in records:
        _enrich_from_local(r)
    # 只保留实际有内容的话题
    used_topics = [t for t in TOPICS if any(r.get("topic") == t for r in records)]
    return render_template("index.html", records=records, topics=used_topics)


# 本地 archive 索引缓存：{ feishu_record_id -> metadata dict }
_local_index_cache = {"index": {}, "expiry": 0}


def _build_local_index():
    now = time.time()
    if _local_index_cache["index"] and now < _local_index_cache["expiry"]:
        return
    archive_root = Path(__file__).parent.parent / "archive"
    if not archive_root.exists():
        _local_index_cache["expiry"] = now + app.config["CACHE_TTL"]
        return
    index = {}
    for d in archive_root.iterdir():
        if not d.is_dir():
            continue
        meta_path = d / "metadata.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            rid = meta.get("feishu_record_id")
            if rid:
                index[rid] = meta
        except Exception:
            continue
    _local_index_cache["index"] = index
    _local_index_cache["expiry"] = now + app.config["CACHE_TTL"]


def _enrich_from_local(article):
    """从本地 archive 的 metadata.json 补充金句、核心观点、评分等详细数据"""
    _build_local_index()
    meta = _local_index_cache["index"].get(article["id"])
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
    return article


@app.route("/article/<record_id>")
def detail(record_id):
    try:
        records = fetch_records()
    except Exception as e:
        abort(500)
        return

    article = next((r for r in records if r["id"] == record_id), None)
    if not article:
        abort(404)
    # 补充本地详细数据（金句、核心观点等）
    article = _enrich_from_local(article)
    return render_template("detail.html", article=article)


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
    app.run(debug=True, host="0.0.0.0", port=5000)
