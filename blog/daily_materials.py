#!/usr/bin/env python3
"""每日讨论素材盘：AI HOT + AGI Hunt 各 Top10（共 20 条）原始榜单推飞书卡片。

定位是「素材层」——不是判断（终审官）也不是告警（hot-watch），而是把双源
未加工的原料摊给人看，由人当编辑决定今天还有什么值得补发。**零 LLM 调用**。
两源分区、各用原生量纲（AI HOT 0-100 分 / AGI Hunt heat 浮点），绝不混轨。
跨源同事件只标记 ↔ 不删除（「两边都上榜」本身是够热的信号，看全比去重重要）。

用法：blog/.venv/bin/python blog/daily_materials.py [--dry-run]
配合 cron 每天 8:50（简报 8:35 发布+终审之后）发一次。
"""
import base64
import hashlib
import hmac
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "config" / ".env")
except ImportError:
    pass

import os  # noqa: E402  在 dotenv 之后
from config import Config  # noqa: E402
from today_signal import fetch_aihot  # noqa: E402
from hot_watch import fetch_agihunt_trends, _similar, _safe_score, _safe_heat  # noqa: E402

TOP_N = int(os.getenv("MATERIALS_TOP_N", "5"))
WEBHOOK = os.getenv("FEISHU_BOT_WEBHOOK", "")
SECRET = os.getenv("FEISHU_BOT_SECRET", "")
APP_ID = os.getenv("FEISHU_APP_ID", "")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
# 前 3 热点海报图默认开；缺 Chrome/app 凭据会自动降级只发文字盘，不空窗
POSTERS_ENABLED = os.getenv("MATERIALS_POSTERS", "1") == "1"


def collect(aihot_items, trends, top_n=TOP_N):
    """两源各取 top_n，跨源相似的互标 dup=True（只标不删）。"""
    ai = sorted(aihot_items, key=lambda x: -_safe_score(x))[:top_n]
    ag = sorted(trends, key=lambda x: -_safe_heat(x))[:top_n]
    rows_ai = [{
        "title": str(i.get("title") or ""),
        "score": _safe_score(i),
        "source": str(i.get("source") or ""),
        "url": str(i.get("url") or i.get("permalink") or ""),
        "dup": False,
    } for i in ai]
    rows_ag = [{
        "title": str(t.get("term_zh") or t.get("term_en") or ""),
        "heat": round(_safe_heat(t), 1),
        "posts": len(t.get("post_ids") or []),
        "url": "https://agihunt.info/",
        "dup": False,
    } for t in ag]
    for a in rows_ai:
        for g in rows_ag:
            if _similar(a["title"], g["title"]):
                a["dup"] = g["dup"] = True
    return rows_ai, rows_ag


def _featured(rows_ai, rows_ag):
    """前 3 张卡片：两源各露头 + 偏 AGI Hunt 补一张（它抓 X 原生大事、AI HOT 常漏）。
    顺序：AGI Hunt#1 / AI HOT#1 / AGI Hunt#2（缺则 AI HOT#2）。"""
    picks = []
    if rows_ag:
        picks.append(("agihunt", rows_ag[0]))
    if rows_ai:
        picks.append(("aihot", rows_ai[0]))
    if len(rows_ag) > 1:
        picks.append(("agihunt", rows_ag[1]))
    elif len(rows_ai) > 1:
        picks.append(("aihot", rows_ai[1]))
    return picks[:3]


def build_card(rows_ai, rows_ag, date_str):
    dup = lambda r: " ↔" if r["dup"] else ""
    elements = []
    medals = ["①", "②", "③"]
    for idx, (kind, r) in enumerate(_featured(rows_ai, rows_ag)):
        if kind == "aihot":
            metric = f"AI HOT · 讨论度 {r['score']}｜{r['source']}"
        else:
            metric = f"AGI Hunt · heat {r['heat']}｜{r['posts']} 条帖子聚类"
        elements.append({"tag": "div", "text": {"tag": "lark_md",
                        "content": f"**{medals[idx]} {r['title']}**{dup(r)}\n{metric}"}})
        if r["url"]:
            elements.append({"tag": "action", "actions": [{"tag": "button",
                            "text": {"tag": "plain_text", "content": "查看原文"},
                            "url": r["url"], "type": "default"}]})
    elements.append({"tag": "hr"})

    def section(title, rows, line):
        body = "\n".join(f"{i}. {line(r)}{dup(r)}" for i, r in enumerate(rows, 1)) or "（暂无）"
        return {"tag": "div", "text": {"tag": "lark_md", "content": f"**{title}**\n{body}"}}

    elements.append(section(f"AI HOT · 讨论度 Top{len(rows_ai)}", rows_ai,
                            lambda r: f"{r['score']}分 {r['title']}"))
    elements.append(section(f"AGI Hunt · 趋势 Top{len(rows_ag)}", rows_ag,
                            lambda r: f"heat {r['heat']} {r['title']}"))
    elements.append({"tag": "note", "elements": [{"tag": "plain_text",
                    "content": "↔ = 两源都上榜｜原始榜单未经筛选，供你人工判断今天还有什么值得发"}]})
    return {
        "config": {"wide_screen_mode": True},
        "header": {"template": "wathet", "title": {"tag": "plain_text",
                   "content": f"📋 今日讨论素材 · 双源各Top{TOP_N} · {date_str}"}},
        "elements": elements,
    }


def build_text(rows_ai, rows_ag, date_str):
    dup = lambda r: " ↔" if r["dup"] else ""
    lines = [f"📋 今日讨论素材 · 双源各Top{TOP_N} · {date_str}", "", "【AI HOT · 讨论度】"]
    lines += [f"{i}. {r['score']}分 {r['title']}{dup(r)}" for i, r in enumerate(rows_ai, 1)]
    lines += ["", "【AGI Hunt · 趋势】"]
    lines += [f"{i}. heat {r['heat']} {r['title']}{dup(r)}" for i, r in enumerate(rows_ag, 1)]
    lines += ["", "↔=两源都上榜 · 原始榜单供人工判断"]
    return "\n".join(lines)


def _signed_payload(body):
    if not SECRET:
        return body
    ts = str(int(time.time()))
    sign = base64.b64encode(hmac.new(f"{ts}\n{SECRET}".encode("utf-8"),
                            b"", hashlib.sha256).digest()).decode("utf-8")
    return {"timestamp": ts, "sign": sign, **body}


def send(card, text, webhook=None, post=None):
    """先发交互卡片；被拒（非 code:0）降级发纯文本，绝不空窗。post 可注入供测试。"""
    webhook = webhook or WEBHOOK
    if not webhook:
        print("[materials] 未配置 FEISHU_BOT_WEBHOOK，跳过发送")
        return 0
    if post is None:
        import requests
        post = lambda url, payload: requests.post(url, json=payload, timeout=15).json()
    try:
        resp = post(webhook, _signed_payload({"msg_type": "interactive", "card": card}))
        if (resp or {}).get("code") == 0:
            print("[materials] 已发送素材卡片")
            return 0
        print(f"[materials] 卡片被拒（{resp}），降级纯文本", file=sys.stderr)
    except Exception as exc:
        print(f"[materials] 卡片发送异常（{exc}），降级纯文本", file=sys.stderr)
    try:
        resp = post(webhook, _signed_payload({"msg_type": "text", "content": {"text": text}}))
        if (resp or {}).get("code") == 0:
            print("[materials] 已降级发送纯文本")
            return 0
        print(f"[materials] 纯文本也失败：{resp}", file=sys.stderr)
    except Exception as exc:
        print(f"[materials] 纯文本发送异常：{exc}", file=sys.stderr)
    return 1


def _featured_posters(rows_ai, rows_ag, aihot_raw, trends_raw, date_str):
    """三合一热点板的素材：第 1 条为大热点。对外分享图**不带聚合源名与原始热度数字**
    （那些留在对内的飞书文字卡片里）。"""
    def ai_summary(title):
        for i in aihot_raw:
            if str(i.get("title") or "") == title:
                return str(i.get("summary") or "")
        return ""
    def ag_blurb(title):
        for t in trends_raw:
            if str(t.get("term_zh") or t.get("term_en") or "") == title:
                return str(t.get("blurb") or "")
        return ""
    items = []
    for kind, r in _featured(rows_ai, rows_ag):
        summary = ai_summary(r["title"]) if kind == "aihot" else ag_blurb(r["title"])
        items.append({"title": r["title"], "summary": summary, "date": date_str})
    return items


def _tenant_token():
    """用 app 凭据换 tenant_access_token（上传图片需要）。缺凭据返回 None。"""
    if not (APP_ID and APP_SECRET):
        return None
    import requests
    r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                      json={"app_id": APP_ID, "app_secret": APP_SECRET}, timeout=15).json()
    return r.get("tenant_access_token") if r.get("code") == 0 else None


def _upload_image(token, png_path):
    """上传图片换 image_key。返回 (image_key|None, 失败原因文本)。
    网络异常重试一次（实测 open.feishu.cn 上传通道偶发握手超时）。"""
    import time as _time
    import requests
    last_err = ""
    for attempt in range(2):
        try:
            with open(png_path, "rb") as f:
                r = requests.post("https://open.feishu.cn/open-apis/im/v1/images",
                                  headers={"Authorization": f"Bearer {token}"},
                                  data={"image_type": "message"}, files={"image": f},
                                  timeout=60).json()
            if r.get("code") == 0:
                return (r.get("data") or {}).get("image_key"), ""
            # API 明确拒绝（如 99991672 缺 im:resource:upload 权限）：重试无意义，原样透传
            return None, f"code={r.get('code')} {str(r.get('msg'))[:180]}"
        except Exception as exc:
            last_err = f"网络异常: {type(exc).__name__} {str(exc)[:80]}"
            _time.sleep(2)
    return None, last_err


def send_posters(items, webhook=None, post=None, token_fn=None, upload_fn=None, render_fn=None):
    """渲染前 3 热点海报 → 上传 → webhook 发图。任一环节缺失就整体跳过（文字盘已发，绝不空窗）。"""
    webhook = webhook or WEBHOOK
    if not (POSTERS_ENABLED and webhook):
        return 0
    token = (token_fn or _tenant_token)()
    if not token:
        print("[materials] 无 app 凭据或换 token 失败，跳过海报图（文字盘已发）", file=sys.stderr)
        return 0
    import tempfile
    import xhs_card
    render_fn = render_fn or xhs_card.render_hot_board
    upload_fn = upload_fn or _upload_image
    if post is None:
        import requests
        post = lambda url, payload: requests.post(url, json=payload, timeout=15).json()
    sent = 0
    with tempfile.TemporaryDirectory() as tmp:
        for png, ok, err in render_fn(items, tmp):
            if not ok:
                print(f"[materials] 海报渲染失败（可能缺 Chrome）：{str(err)[:80]}", file=sys.stderr)
                continue
            key, upload_err = upload_fn(token, png)
            if not key:
                print(f"[materials] 图片上传失败：{upload_err}", file=sys.stderr)
                if "99991672" in upload_err:
                    print("[materials] → 需到飞书开放平台给应用开通 im:resource:upload 权限并发布版本",
                          file=sys.stderr)
                continue
            resp = post(webhook, _signed_payload({"msg_type": "image", "content": {"image_key": key}}))
            if (resp or {}).get("code") == 0:
                sent += 1
            else:
                print(f"[materials] 发图被拒：{resp}", file=sys.stderr)
    if sent:
        print(f"[materials] 已发送三合一热点板（{sent} 张图）")
    return 0


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    date_str = datetime.now(ZoneInfo(Config.BLOG_TIMEZONE)).strftime("%m-%d")
    try:
        aihot = fetch_aihot(24) or []
    except Exception as exc:
        print(f"[materials] AI HOT 拉取失败：{exc}", file=sys.stderr)
        aihot = []
    try:
        trends = fetch_agihunt_trends() or []
    except Exception as exc:
        print(f"[materials] AGI Hunt 拉取失败：{exc}", file=sys.stderr)
        trends = []
    if not aihot and not trends:
        print("[materials] 两源都拉取失败，不发送", file=sys.stderr)
        return 1
    rows_ai, rows_ag = collect(aihot, trends)
    card = build_card(rows_ai, rows_ag, date_str)
    text = build_text(rows_ai, rows_ag, date_str)
    if "--dry-run" in args:
        print(text)
        return 0
    rc = send(card, text)
    # 文字盘发出后再发前 3 热点海报图（可发的图）；缺 Chrome/凭据会自动跳过
    send_posters(_featured_posters(rows_ai, rows_ag, aihot, trends, date_str))
    return rc


if __name__ == "__main__":
    sys.exit(main())
