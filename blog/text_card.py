"""文字金句卡：无视频帧的分享卡渲染（详情页「金句卡」按钮的后端）。

场景是「个人 + 同事看懂要点」而非对外发布——不抽视频帧，深色设计底 +
金句大字 + 署名 + 来源脚注，headless Chrome 渲染 1280×720 PNG。

排版纯函数（字号阶梯/归一化/署名降级链）以本模块为单一真相源，
帧版 CLI make_quote_shots.py 反向 import。本模块不 import numpy/embeddings
（文字卡无需语义定位），保持 Flask 请求路径轻量。
"""
import html
import os
import re
import subprocess
from pathlib import Path

# 默认 macOS 系统 Chrome；Linux/VPS 用环境变量覆盖，如 CHROME=/usr/bin/chromium
CHROME = os.getenv("CHROME") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CARD_W, CARD_H = 1280, 720
CHROME_TIMEOUT = 30  # 渲染在请求内同步执行，必须有超时


def normalize_quote(item):
    """归一化金句：dict 形态取正文，strip 首尾中英文引号与空白。
    委托 today_signal.quote_text（锚点/信号/卡片三处共用同一语义）；
    懒加载避免把 numpy 等重依赖拖进模块导入。"""
    import today_signal
    fn = getattr(today_signal, "quote_text", None) or today_signal._quote_text
    return fn(item)


def font_size_for(text):
    """按字数选字号：≤22 字 60px / ≤36 字 50px / ≤54 字 42px / 更长 36px。"""
    n = len(text or "")
    if n <= 22:
        return 60
    if n <= 36:
        return 50
    if n <= 54:
        return 42
    return 36


def first_guest(guests):
    """guests 可能是字符串（按 、,，/| 切第一个）或 list（取第一个非空）。"""
    if isinstance(guests, str):
        for part in re.split(r"[、,，/|]", guests):
            part = part.strip()
            if part:
                return part
    elif isinstance(guests, list):
        for part in guests:
            if isinstance(part, dict):
                name = str(part.get("name") or part.get("speaker") or "").strip()
            else:
                name = str(part or "").strip()
            if name:
                return name
    return ""


def resolve_attribution(meta, name_override=None, role_override=None):
    """署名降级链：guest_info[0].name → guests → uploader；头衔取 guest_info[0].title
    按 、 切第一段并截断约 20 字。返回 (name, role)，role 可为空串。"""
    gi = meta.get("guest_info") or []  # 兼容 null / 缺失
    g0 = gi[0] if isinstance(gi, list) and gi else {}
    if not isinstance(g0, dict):
        g0 = {"name": str(g0 or "")}

    name = name_override
    if name is None:
        name = str(g0.get("name") or "").strip()
        if not name:
            name = first_guest(meta.get("guests"))
        if not name:
            name = str(meta.get("uploader") or "").strip()

    role = role_override
    if role is None:
        role = str(g0.get("title") or "").strip()
        if role:
            role = re.split(r"、", role)[0].strip()[:20]
    return name, role


def text_card_html(text, name, role, title="", platform=""):
    """1280×720 文字卡 HTML：深色渐变底、金句大字、署名、来源脚注。全字段转义。"""
    size = font_size_for(text)
    q = html.escape(text)
    nm = html.escape(name or "")
    rl = html.escape(role or "")
    tt = html.escape(title or "")
    pf = html.escape(platform or "")
    byline = f"— <b>{nm}</b> · {rl}" if rl else f"— <b>{nm}</b>"
    footer_bits = [b for b in (f"《{tt}》" if tt else "", pf, "降噪 NoiseFilter") if b]
    footer = " · ".join(footer_bits)
    return f"""<!doctype html><meta charset=utf-8><style>
html,body{{margin:0}}
.stage{{width:{CARD_W}px;height:{CARD_H}px;position:relative;overflow:hidden;
  background:radial-gradient(1200px 800px at 88% -10%,rgba(184,95,66,.38),transparent 55%),
             radial-gradient(900px 700px at -8% 110%,rgba(184,95,66,.22),transparent 50%),
             linear-gradient(160deg,#191925 0%,#10101a 60%,#0b0b12 100%);
  font-family:"PingFang SC","Helvetica Neue",sans-serif}}
.mark{{position:absolute;top:44px;left:64px;font-size:150px;line-height:1;
  color:rgba(184,95,66,.5);font-family:Georgia,serif}}
.cap{{position:absolute;left:0;right:0;top:0;bottom:0;padding:170px 84px 96px;
  display:flex;flex-direction:column;justify-content:center}}
.q{{color:#fff;font-size:{size}px;font-weight:600;line-height:1.42;
  text-wrap:balance;letter-spacing:.5px}}
.nm{{color:#EBE3D7;font-size:30px;margin-top:34px}}
.nm b{{color:#fff;font-weight:600}}
.ft{{position:absolute;left:84px;right:84px;bottom:44px;color:rgba(235,227,215,.45);
  font-size:20px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
</style>
<div class=stage>
  <div class=mark>“</div>
  <div class=cap>
    <div class=q>「{q}」</div>
    <div class=nm>{byline}</div>
  </div>
  <div class=ft>{footer}</div>
</div>"""


def run_chrome_screenshot(html_path, out_png, chrome_path=None, timeout=CHROME_TIMEOUT,
                          size=(CARD_W, CARD_H)):
    """headless Chrome 截图。返回 CompletedProcess 形对象；Chrome 缺失抛 FileNotFoundError。"""
    chrome = Path(chrome_path or CHROME)
    if not chrome.exists():
        raise FileNotFoundError(f"未找到 Chrome（{chrome}），无法渲染金句卡")
    return subprocess.run(
        [str(chrome), "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={size[0]},{size[1]}",
         "--virtual-time-budget=2500", f"--screenshot={out_png}",
         f"file://{html_path}"],
        capture_output=True, text=True, timeout=timeout)


def _render_html_to_png(html_str, out_png, size):
    """把 HTML 渲染成 PNG。返回 (ok, err_msg)——服务端用，不 sys.exit。"""
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    out_png.unlink(missing_ok=True)  # 先清旧产物，避免残留掩盖本次失败
    html_path = out_png.with_suffix(".html")
    html_path.write_text(html_str, encoding="utf-8")
    try:
        r = run_chrome_screenshot(html_path.resolve(), out_png, size=size)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        out_png.unlink(missing_ok=True)
        return False, str(e)
    if getattr(r, "returncode", 1) != 0 or not out_png.exists():
        out_png.unlink(missing_ok=True)
        return False, (getattr(r, "stderr", "") or "")[-500:] or "Chrome 渲染失败"
    html_path.unlink(missing_ok=True)  # 失败时留 html 排查，成功即清
    return True, ""


def render_text_card(text, name, role, title, platform, out_png):
    """渲染文字金句卡（1280×720）。返回 (ok, err_msg)。"""
    return _render_html_to_png(text_card_html(text, name, role, title, platform),
                               out_png, (CARD_W, CARD_H))


# ── 今日 AI 判断日卡（1920×1080 横版，三栏并排 + breaking 顶条）────────────────
DAILY_W, DAILY_H = 1920, 1080


def daily_card_html(payload, date_str=""):
    """今日判断日卡 HTML。payload = today_signal 缓存（breaking + signals）。
    同事扫一眼等于看完当天判断——每栏只放 栏目/标题/一句总结/why。全字段转义。"""
    breaking = payload.get("breaking") or None
    signals = (payload.get("signals") or [])[:3]
    date = html.escape(date_str or str(payload.get("generated_at") or "")[:10])

    def col(s):
        label = html.escape(s.get("slot_label") or "")
        title = html.escape(s.get("title") or "")
        summary = html.escape(s.get("summary") or "")
        why = html.escape(s.get("why") or "")
        why_html = f'<div class=why><span>为什么值得看</span>{why}</div>' if why else ""
        return (f'<div class=col><div class=slot>{label}</div>'
                f'<div class=title>{title}</div>'
                f'<div class=sum>{summary}</div>{why_html}</div>')

    breaking_html = ""
    if breaking:
        b_title = html.escape(breaking.get("title") or "")
        b_sum = html.escape(breaking.get("summary") or "")
        b_action = html.escape(breaking.get("action") or "")
        chip = f'<span class=chip>{b_action}</span>' if b_action else ""
        breaking_html = (f'<div class=brk><span class=brklabel>顶级大新闻</span>'
                         f'<div class=brkbody><div class=brktitle>{b_title}{chip}</div>'
                         f'<div class=brksum>{b_sum}</div></div></div>')

    cols = "".join(col(s) for s in signals) or '<div class=col><div class=sum>今日无入选判断。</div></div>'
    return f"""<!doctype html><meta charset=utf-8><style>
html,body{{margin:0}}
.stage{{width:{DAILY_W}px;height:{DAILY_H}px;position:relative;overflow:hidden;box-sizing:border-box;
  padding:64px 80px 56px;display:flex;flex-direction:column;
  background:radial-gradient(1400px 900px at 92% -12%,rgba(184,95,66,.35),transparent 55%),
             radial-gradient(1000px 800px at -10% 112%,rgba(184,95,66,.2),transparent 50%),
             linear-gradient(160deg,#191925 0%,#10101a 60%,#0b0b12 100%);
  font-family:"PingFang SC","Helvetica Neue",sans-serif;color:#fff}}
.head{{display:flex;align-items:baseline;gap:18px;margin-bottom:34px}}
.brand{{font-size:26px;font-weight:800;color:rgba(235,227,215,.85)}}
.htitle{{font-size:40px;font-weight:800}}
.hdate{{margin-left:auto;font-size:24px;color:rgba(235,227,215,.5)}}
.brk{{display:flex;gap:22px;align-items:flex-start;background:rgba(184,95,66,.14);
  border:1px solid rgba(184,95,66,.35);border-radius:16px;padding:22px 28px;margin-bottom:30px}}
.brklabel{{flex-shrink:0;font-size:20px;font-weight:800;color:#E8A188;
  border:1px solid rgba(232,161,136,.5);border-radius:10px;padding:4px 12px}}
.brktitle{{font-size:28px;font-weight:700;line-height:1.35}}
.chip{{display:inline-block;margin-left:14px;font-size:18px;font-weight:700;color:#0b0b12;
  background:#E8A188;border-radius:9px;padding:2px 12px;vertical-align:middle}}
.brksum{{margin-top:8px;font-size:21px;line-height:1.5;color:rgba(235,227,215,.75)}}
.cols{{display:flex;gap:36px;flex:1;min-height:0}}
.col{{flex:1;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.08);
  border-radius:18px;padding:30px 30px 26px;display:flex;flex-direction:column;overflow:hidden}}
.slot{{font-size:19px;font-weight:800;color:#E8A188;letter-spacing:1px;margin-bottom:16px}}
.title{{font-size:30px;font-weight:700;line-height:1.4;margin-bottom:16px}}
.sum{{font-size:22px;line-height:1.6;color:rgba(255,255,255,.86)}}
.why{{margin-top:auto;padding-top:18px;font-size:20px;line-height:1.55;color:rgba(235,227,215,.62)}}
.why span{{display:block;font-size:16px;font-weight:800;color:rgba(232,161,136,.7);
  letter-spacing:1px;margin-bottom:6px}}
.foot{{margin-top:28px;font-size:19px;color:rgba(235,227,215,.4)}}
</style>
<div class=stage>
  <div class=head><span class=brand>降噪 NoiseFilter</span>
    <span class=htitle>今日 AI 判断</span><span class=hdate>{date}</span></div>
  {breaking_html}
  <div class=cols>{cols}</div>
  <div class=foot>每条只回答：值不值得继续看 · 降噪 NoiseFilter</div>
</div>"""


def render_daily_card(payload, out_png, date_str=""):
    """渲染今日判断日卡（1920×1080）。返回 (ok, err_msg)。"""
    return _render_html_to_png(daily_card_html(payload, date_str),
                               out_png, (DAILY_W, DAILY_H))
