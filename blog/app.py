"""
内容策展博客 - 基于飞书多维表格的个人博客
"""

import json
import os
import time
from pathlib import Path

import requests
from flask import Flask, render_template, abort, Response

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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

        resp = requests.get(url, headers=headers, params=params)
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
@app.route("/")
def index():
    try:
        records = fetch_records()
    except Exception as e:
        records = []
        print(f"[ERROR] 获取数据失败: {e}")
    return render_template("index.html", records=records)


def _enrich_from_local(article):
    """从本地 archive 的 metadata.json 补充金句、核心观点等详细数据"""
    archive_root = Path(__file__).parent.parent / "archive"
    if not archive_root.exists():
        return article
    for d in archive_root.iterdir():
        if not d.is_dir():
            continue
        meta_path = d / "metadata.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("feishu_record_id") == article["id"]:
                article["key_quotes"] = meta.get("key_quotes", [])
                article["core_ideas"] = meta.get("core_ideas", [])
                article["key_insights"] = meta.get("key_insights", "")
                if not article["guests"] and meta.get("guests"):
                    article["guests"] = "、".join(meta["guests"])
                return article
        except Exception:
            continue
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
