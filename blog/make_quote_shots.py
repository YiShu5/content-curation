"""金句卡参数化 CLI：对任意一条 rewrite_complete 记录抓「大佬说这句」的真实帧 + 烧字幕 → 成品 PNG。

用法（任意 cwd 均可）：
  blog/.venv/bin/python blog/make_quote_shots.py <record_id>
  blog/.venv/bin/python blog/make_quote_shots.py --dir archive/xxx
选项：
  --index 0,2   只做指定序号的金句（默认全部 key_quotes）
  --text  文案  覆盖金句文案（只出一张卡，序号取 --index 第一个，缺省 0）
  --name/--role 覆盖署名（默认 guest_info → guests → uploader 降级）
  --out   目录  输出目录（默认 blog/data/quote_cards/）
  --shift 秒    语义定位点之后再偏移几秒抽帧（默认 2.0）
  --force       无视已有 raw 帧缓存，重新定位+抽帧
  --strict      语义匹配分 < 0.35 时中止（默认只警告）

流程：语义定位（embeddings.embed_query + today_signal._locate_timestamp）→
低清整片按视频 id 缓存到 blog/data/video_cache/（同记录多金句只下载一次）→
ffmpeg 抽帧（raw-{record_id}-{i}.png，存在即复用）→ headless Chrome 烧字幕
（shot-{record_id}-{i}.png）。

退出码：0 成功；1 参数/元数据/工具缺失/非 YouTube；2 转录无时间戳；
3 下载失败；4 抽帧失败；5 渲染失败；6 --strict 匹配分不足。
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

import embeddings
import today_signal as T

# ── 模块级常量（测试会 monkeypatch，函数内必须引用这些名字而非局部拷贝）──────
ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = ROOT / "archive"
DEFAULT_OUT_DIR = ROOT / "blog" / "data" / "quote_cards"
VIDEO_CACHE_DIR = ROOT / "blog" / "data" / "video_cache"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MIN_MATCH_SCORE = 0.35
DEFAULT_SHIFT = 2.0

EXIT_USAGE = 1        # 参数/元数据/工具缺失/非 YouTube/--index 越界
EXIT_NO_TIMESTAMP = 2  # 转录无 [HH:MM:SS] 时间戳（沿用 grab_quote_frame 语义）
EXIT_DOWNLOAD = 3      # yt-dlp 下载失败（沿用）
EXIT_FRAME = 4         # ffmpeg 抽帧失败（沿用）
EXIT_RENDER = 5        # Chrome 渲染失败
EXIT_STRICT = 6        # --strict 且匹配分 < MIN_MATCH_SCORE

_TS_RE = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})\]")


def err(msg):
    print(msg, file=sys.stderr)


def hhmmss(s):
    s = int(s)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


# ── 文案与排版（纯函数）────────────────────────────────────────────────────
def normalize_quote(item):
    """归一化金句：dict 形态取 text/quote/content 键；strip 首尾中英文引号与空白。
    模板统一加「」，这里先去掉自带引号，避免出现 「“xxx”」。"""
    if isinstance(item, dict):
        raw = item.get("text") or item.get("quote") or item.get("content") or ""
    else:
        raw = str(item or "")
    return raw.strip().strip("“”\"'").strip()


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


def overlay_html(img, text, name, role):
    """1280x720 字幕卡 HTML。金句/署名做 HTML 转义防注入；text-wrap: balance 均衡换行。"""
    size = font_size_for(text)
    q = html.escape(text)
    nm = html.escape(name or "")
    rl = html.escape(role or "")
    byline = f"— <b>{nm}</b> · {rl}" if rl else f"— <b>{nm}</b>"
    return f"""<!doctype html><meta charset=utf-8><style>
html,body{{margin:0}}
.stage{{width:1280px;height:720px;position:relative;overflow:hidden;background:#000 url('file://{img}') center/cover no-repeat;font-family:"PingFang SC","Helvetica Neue",sans-serif}}
.cap{{position:absolute;left:0;right:0;bottom:0;padding:150px 70px 58px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.22) 36%,rgba(0,0,0,.92))}}
.q{{color:#fff;font-size:{size}px;font-weight:600;line-height:1.3;text-wrap:balance;text-shadow:0 2px 14px rgba(0,0,0,.65)}}
.nm{{color:#EBE3D7;font-size:30px;margin-top:28px}}
.nm b{{color:#fff;font-weight:600}}
</style>
<div class=stage>
  <div class=cap>
    <div class=q>「{q}」</div>
    <div class=nm>{byline}</div>
  </div>
</div>"""


# ── 记录解析 ────────────────────────────────────────────────────────────────
def load_metadata(archive_dir):
    mp = Path(archive_dir) / "metadata.json"
    if not mp.exists():
        err(f"错误：{mp} 不存在")
        sys.exit(EXIT_USAGE)
    try:
        return json.loads(mp.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"错误：{mp} 解析失败：{e}")
        sys.exit(EXIT_USAGE)


def resolve_record_dir(record_id):
    """record_id → archive 目录。与 app.py load_archive_records 同规则：
    目录名倒序、只认 rewrite_complete=True、按 metadata 的 id（缺失则目录名）相等匹配。
    返回 (Path, metadata) 或 (None, None)。"""
    root = Path(ARCHIVE_ROOT)
    if not root.exists():
        return None, None
    for mp in sorted(root.glob("*/metadata.json"),
                     key=lambda p: p.parent.name, reverse=True):
        try:
            m = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not m.get("rewrite_complete"):
            continue
        rid = m.get("id") or mp.parent.name
        if str(rid) == str(record_id):
            return mp.parent, m
    return None, None


def ensure_youtube(url):
    """metadata url 非 YouTube 直接退出（host 为 None/空串也不得 AttributeError）。"""
    host = (urlparse(url or "").hostname or "").lower()
    if host == "youtu.be" or host == "youtube.com" or host.endswith(".youtube.com"):
        return
    err(f"错误：仅支持 YouTube 视频抽帧，metadata url = {url!r}")
    sys.exit(EXIT_USAGE)


def has_timestamps(transcript_path):
    p = Path(transcript_path)
    if not p.exists():
        return False
    try:
        return bool(_TS_RE.search(p.read_text(encoding="utf-8")))
    except Exception:
        return False


# ── 定位 / 下载 / 抽帧 / 渲染 ────────────────────────────────────────────────
def require_tool(name, hint):
    """shutil.which 探测（附带根 .venv/bin，yt-dlp 装在那里）；缺失清晰报错退出。"""
    search = os.pathsep.join([str(ROOT / ".venv" / "bin"),
                              os.environ.get("PATH", "")])
    path = shutil.which(name, path=search)
    if not path:
        err(f"错误：找不到 {name}。{hint}")
        sys.exit(EXIT_USAGE)
    return path


def locate_quote(archive_dir, text):
    """语义定位金句时间点：embed_query + today_signal._locate_timestamp。
    返回 (sec, snippet, score) 或 None。"""
    vec = np.asarray(embeddings.embed_query(text), dtype=np.float32)
    return T._locate_timestamp(Path(archive_dir), vec)


def find_cached_video(video_id):
    """探测 video_cache 里的整片缓存：glob {id}.*，多命中取排序第一；0 字节视为无效。"""
    cache = Path(VIDEO_CACHE_DIR)
    hits = sorted(cache.glob(f"{video_id}.*"))
    if not hits:
        return None
    first = hits[0]
    try:
        if first.stat().st_size > 0:
            return first
        first.unlink()  # 0 字节 = 上次下载中断，删掉触发重下
    except OSError:
        pass
    return None


def _run_yt_dlp(url, out_tmpl):
    yt = require_tool("yt-dlp", "可在根 .venv 安装：.venv/bin/pip install yt-dlp")
    return subprocess.run(
        [yt, "-f", "bv*[height<=720]/b[height<=720]/bv*/b/wv*/w",
         "--extractor-args", "youtube:player_client=android",
         "--no-part", "-o", out_tmpl, url],
        capture_output=True, text=True)


def download_video(url, video_id):
    """低清整片按视频 id 缓存到 VIDEO_CACHE_DIR/{id}.%(ext)s；命中即复用不重下。"""
    cached = find_cached_video(video_id)
    if cached:
        print(f"复用缓存整片 {cached.name}")
        return cached
    cache = Path(VIDEO_CACHE_DIR)
    cache.mkdir(parents=True, exist_ok=True)
    print("下载低清整片（只下这一次，之后走缓存）...")
    r = _run_yt_dlp(url, str(cache / f"{video_id}.%(ext)s"))
    cached = find_cached_video(video_id)
    if not cached:
        err("DL_FAIL: " + (getattr(r, "stderr", "") or "")[-700:])
        sys.exit(EXIT_DOWNLOAD)
    return cached


def _run_ffmpeg(video, at, out):
    ff = require_tool("ffmpeg", "可用 brew install ffmpeg 安装")
    return subprocess.run(
        [ff, "-y", "-ss", hhmmss(at), "-i", str(video),
         "-frames:v", "1", "-q:v", "2", str(out)],
        capture_output=True, text=True)


def extract_frame(video, at, out):
    r = _run_ffmpeg(video, at, out)
    if not Path(out).exists():
        err("FRAME_FAIL: " + (getattr(r, "stderr", "") or "")[-700:])
        sys.exit(EXIT_FRAME)
    print(f"抽帧 OK -> {Path(out).name} @ {hhmmss(at)}")


def _run_chrome(html_path, out_png):
    chrome = Path(CHROME)
    if not chrome.exists():
        err(f"错误：未找到 Chrome（{CHROME}），无法合成字幕卡")
        sys.exit(EXIT_USAGE)
    return subprocess.run(
        [str(chrome), "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--window-size=1280,720",
         "--virtual-time-budget=2500", f"--screenshot={out_png}",
         f"file://{html_path}"],
        capture_output=True, text=True)


def render_card(raw_png, text, name, role, out_png):
    out_png = Path(out_png)
    html_path = out_png.with_suffix(".html")
    html_path.write_text(
        overlay_html(str(Path(raw_png).resolve()), text, name, role),
        encoding="utf-8")
    r = _run_chrome(html_path.resolve(), out_png)
    if not out_png.exists():
        err("RENDER_FAIL: " + (getattr(r, "stderr", "") or "")[-700:])
        sys.exit(EXIT_RENDER)  # html 留在原地便于排查
    html_path.unlink(missing_ok=True)


# ── CLI ─────────────────────────────────────────────────────────────────────
def parse_index(spec):
    idxs = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            idxs.append(int(part))
        except ValueError:
            err(f"错误：--index 需要逗号分隔的整数，收到 {part!r}")
            sys.exit(EXIT_USAGE)
    if not idxs:
        err("错误：--index 为空")
        sys.exit(EXIT_USAGE)
    return idxs


def build_parser():
    ap = argparse.ArgumentParser(
        description="为一条 rewrite_complete 记录的金句生成「真实帧+字幕」PNG 卡")
    ap.add_argument("record_id", nargs="?", help="metadata 的 id（视频 id）")
    ap.add_argument("--dir", help="直接指定 archive 目录（替代 record_id）")
    ap.add_argument("--index", help="逗号分隔的金句序号，默认全部 key_quotes")
    ap.add_argument("--text", help="覆盖金句文案（只出一张卡）")
    ap.add_argument("--name", help="覆盖署名人名")
    ap.add_argument("--role", help="覆盖署名头衔")
    ap.add_argument("--out", help="输出目录，默认 blog/data/quote_cards/")
    ap.add_argument("--shift", type=float, default=DEFAULT_SHIFT,
                    help=f"定位点之后偏移几秒抽帧（默认 {DEFAULT_SHIFT}）")
    ap.add_argument("--force", action="store_true", help="无视 raw 帧缓存重新抽帧")
    ap.add_argument("--strict", action="store_true",
                    help=f"匹配分 < {MIN_MATCH_SCORE} 时中止（默认只警告）")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)

    # 1) 解析记录目录 + metadata
    if a.dir:
        d = Path(a.dir)
        meta = load_metadata(d)
    elif a.record_id:
        d, meta = resolve_record_dir(a.record_id)
        if d is None:
            err(f"错误：archive 里没有 rewrite_complete 且 id={a.record_id!r} 的记录"
                f"（根目录 {ARCHIVE_ROOT}）")
            sys.exit(EXIT_USAGE)
    else:
        err("错误：需要 <record_id> 或 --dir <archive目录>")
        sys.exit(EXIT_USAGE)
    rid = str(meta.get("id") or d.name)

    # 2) fail-fast：非 YouTube 一律不做（在任何下载/定位之前）
    ensure_youtube(meta.get("url"))

    # 3) 选定金句
    if a.text:
        i0 = parse_index(a.index)[0] if a.index else 0
        text = normalize_quote(a.text)
        if not text:
            err("错误：--text 为空")
            sys.exit(EXIT_USAGE)
        selected = [(i0, text)]
    else:
        quotes = meta.get("key_quotes") or []
        if not quotes:
            err("错误：该记录没有 key_quotes；可用 --text 直接指定文案")
            sys.exit(EXIT_USAGE)
        indices = parse_index(a.index) if a.index else list(range(len(quotes)))
        selected = []
        for i in indices:
            if i < 0 or i >= len(quotes):
                err(f"错误：--index {i} 越界（该记录共 {len(quotes)} 条金句，"
                    f"有效范围 0..{len(quotes) - 1}）")
                sys.exit(EXIT_USAGE)
            text = normalize_quote(quotes[i])
            if not text:
                err(f"警告：金句 {i} 为空，跳过")
                continue
            selected.append((i, text))
        if not selected:
            err("错误：选中的金句全为空")
            sys.exit(EXIT_USAGE)

    out_dir = Path(a.out) if a.out else Path(DEFAULT_OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 4) raw 帧：存在即复用（--force 重做）；需要新帧时才定位+下载
    need = []  # (i, text, raw_path)
    for i, text in selected:
        raw = out_dir / f"raw-{rid}-{i}.png"
        if raw.exists() and not a.force:
            print(f"[{i}] 复用已有帧 {raw.name}")
        else:
            need.append((i, text, raw))

    if need:
        if not has_timestamps(d / "transcript.md"):
            err("NO_TIMESTAMP（该转录无 [HH:MM:SS] 时间戳，无法定位抽帧）")
            sys.exit(EXIT_NO_TIMESTAMP)
        located = []  # (i, text, raw, at)
        for i, text, raw in need:
            loc = locate_quote(d, text)
            if not loc:
                err(f"NO_TIMESTAMP（金句 {i} 无法在转录中定位）")
                sys.exit(EXIT_NO_TIMESTAMP)
            sec, snippet, score = loc
            print(f"[{i}] 定位: {hhmmss(sec)} (score={score:.3f}) 片段≈{snippet!r}")
            if score < MIN_MATCH_SCORE:
                err(f"警告：金句 {i} 匹配分 {score:.3f} < {MIN_MATCH_SCORE}，"
                    "定位可能不准（可用 --shift 微调或 --text 换定位句）")
                if a.strict:
                    err("--strict：中止")
                    sys.exit(EXIT_STRICT)
            located.append((i, text, raw, sec + a.shift))
        video = download_video(meta.get("url"), rid)  # 同记录多金句只下载一次
        for i, text, raw, at in located:
            extract_frame(video, at, raw)

    # 5) 烧字幕出成品
    name, role = resolve_attribution(meta, a.name, a.role)
    done = []
    for i, text in selected:
        raw = out_dir / f"raw-{rid}-{i}.png"
        out = out_dir / f"shot-{rid}-{i}.png"
        render_card(raw, text, name, role, out)
        print(f"OK -> {out}")
        done.append(out.name)
    print(f"\n完成 {len(done)} 张: {done}")


if __name__ == "__main__":
    main()
