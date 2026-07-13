#!/usr/bin/env python
"""
每日内容策展 - 内容抓取与归档脚本
用法:
  python scripts/fetch.py --batch [--limit N]
  python scripts/fetch.py --url URL [URL2 ...]
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import feedparser
import requests
import yaml
import yt_dlp
from dotenv import load_dotenv

# ── 路径 ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SOURCES_FILE = CONFIG_DIR / "sources.yaml"
STATE_FILE = CONFIG_DIR / "state.yaml"

load_dotenv(CONFIG_DIR / ".env")

BIBIGPT_TOKEN = os.getenv("BIBIGPT_API_TOKEN", "")
ARCHIVE_DIR = PROJECT_ROOT / os.getenv("ARCHIVE_DIR", "./archive")
# whisper 本地/Groq 云端共用的音频与转录缓存（按视频 id 免重复下载/转录）
WHISPER_CACHE_DIR = Path.home() / ".cache" / "whisper-cpp" / "jobs"

# 转录失败标记：写端（process_item）与读端（read_existing_transcript）共用。
# ⚠️ rewrite.js 里有一份 JS 拷贝按同样前缀识别失败转录，改动需同步。
FAIL_MARK_ERROR = "[转录获取失败"
FAIL_MARK_EMPTY = "[无可用转录"

# 国内 API（BibiGPT）需要直连，不走代理；海外 API 走系统代理
_no_proxy_session = requests.Session()
_no_proxy_session.trust_env = False


# ── 数据结构 ──────────────────────────────────────────────────────────────
@dataclass
class VideoItem:
    id: str
    url: str
    title: str
    uploader: str
    platform: str       # "youtube" | "bilibili" | "xiaoyuzhou"
    upload_date: str    # "YYYYMMDD"
    duration: int       # seconds
    thumbnail_url: str
    description: str


# ── 状态管理 ──────────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.exists():
        data = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8")) or {}
        return data.get("processed", {})
    return {}


def save_state(processed: dict):
    tmp = STATE_FILE.with_suffix(".yaml.tmp")
    tmp.write_text(yaml.dump({"processed": processed}, allow_unicode=True), encoding="utf-8")
    os.replace(tmp, STATE_FILE)


# ── 配置加载 ──────────────────────────────────────────────────────────────
def load_sources() -> dict:
    if not SOURCES_FILE.exists():
        print(f"[ERROR] 找不到订阅源配置: {SOURCES_FILE}")
        sys.exit(1)
    return yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8")) or {}


# ── 平台抓取 ──────────────────────────────────────────────────────────────
def _ydl_to_item(entry: dict, platform: str) -> VideoItem | None:
    """将 yt-dlp flat playlist entry 转换为 VideoItem"""
    vid_id = entry.get("id", "")
    if not vid_id:
        return None
    url = entry.get("url") or entry.get("webpage_url") or ""
    # yt-dlp flat entries often lack full URL; reconstruct
    if platform == "youtube" and not url.startswith("http"):
        url = f"https://www.youtube.com/watch?v={vid_id}"
    elif platform == "bilibili" and not url.startswith("http"):
        bv_id = re.sub(r'_p\d+$', '', vid_id)
        url = f"https://www.bilibili.com/video/{bv_id}"
    upload_date = entry.get("upload_date") or entry.get("timestamp", "")
    if isinstance(upload_date, (int, float)):
        upload_date = datetime.datetime.fromtimestamp(upload_date).strftime("%Y%m%d")
    thumbnails = entry.get("thumbnails") or []
    thumbnail = entry.get("thumbnail") or (thumbnails[-1].get("url", "") if thumbnails else "")
    return VideoItem(
        id=vid_id,
        url=url,
        title=entry.get("title", "未知标题"),
        uploader=entry.get("uploader") or entry.get("channel", "未知"),
        platform=platform,
        upload_date=str(upload_date),
        duration=int(entry.get("duration") or 0),
        thumbnail_url=str(thumbnail),
        description=entry.get("description") or "",
    )


def fetch_youtube_channel(cfg: dict, limit: int) -> list[VideoItem]:
    url = cfg["url"]
    # Ensure we're requesting the videos tab
    if not url.rstrip("/").endswith("/videos"):
        url = url.rstrip("/") + "/videos"
    print(f"  [YouTube] 抓取 {cfg['name']} ...")
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "playlistend": limit,
        "skip_download": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        entries = info.get("entries", [])
        items = [_ydl_to_item(e, "youtube") for e in entries if e]
        return [i for i in items if i]
    except Exception as e:
        print(f"  [WARN] YouTube 抓取失败 ({cfg['name']}): {e}")
        return []


def fetch_bilibili_up(cfg: dict, limit: int) -> list[VideoItem]:
    uid = cfg["id"]
    url = f"https://space.bilibili.com/{uid}/video"
    print(f"  [Bilibili] 抓取 {cfg['name']} ...")
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "playlistend": limit,
        "skip_download": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        entries = info.get("entries", [])
        items = [_ydl_to_item(e, "bilibili") for e in entries if e]
        return [i for i in items if i]
    except Exception as e:
        print(f"  [WARN] Bilibili 抓取失败 ({cfg['name']}): {e}")
        return []


def fetch_xiaoyuzhou_rss(cfg: dict, limit: int) -> list[VideoItem]:
    slug = cfg["id"]
    rss_url = cfg["rss_url"]
    print(f"  [小宇宙] 抓取 {cfg['name']} ...")
    try:
        feed = feedparser.parse(rss_url)
        items = []
        for entry in feed.entries[:limit]:
            # Audio URL from enclosure
            audio_url = ""
            if hasattr(entry, "enclosures") and entry.enclosures:
                audio_url = entry.enclosures[0].get("url", "")
            if not audio_url:
                continue
            # Episode GUID (namespaced to avoid collision with video IDs)
            raw_guid = entry.get("id") or entry.get("link") or entry.get("title", "")
            ep_id = f"{slug}:{raw_guid}"
            # Published date
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = time.strftime("%Y%m%d", entry.published_parsed)
            # Thumbnail: try image tag, then feed image
            thumbnail = ""
            if hasattr(entry, "image") and entry.image:
                thumbnail = entry.image.get("href", "")
            if not thumbnail and hasattr(feed, "feed") and hasattr(feed.feed, "image"):
                thumbnail = feed.feed.image.get("href", "")
            items.append(VideoItem(
                id=ep_id,
                url=audio_url,
                title=entry.get("title", "未知集"),
                uploader=cfg["name"],
                platform="xiaoyuzhou",
                upload_date=published,
                duration=0,
                thumbnail_url=thumbnail,
                description=entry.get("summary", ""),
            ))
        return items
    except Exception as e:
        print(f"  [WARN] 小宇宙 RSS 抓取失败 ({cfg['name']}): {e}")
        return []


def fetch_single_url(url: str) -> VideoItem | None:
    """自动识别平台并抓取单个 URL 的元数据"""
    platform = "youtube"
    if "bilibili.com" in url or "b23.tv" in url:
        platform = "bilibili"
    elif not ("youtube.com" in url or "youtu.be" in url):
        # Treat as direct audio URL (e.g. podcast episode)
        return VideoItem(
            id=f"audio-{hashlib.sha1(url.encode('utf-8')).hexdigest()[:16]}",
            url=url,
            title=url.split("/")[-1].split("?")[0] or "直接链接",
            uploader="直接输入",
            platform="audio",
            upload_date=datetime.datetime.now().strftime("%Y%m%d"),
            duration=0,
            thumbnail_url="",
            description="",
        )
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        thumbnail = info.get("thumbnail") or ""
        if not thumbnail and info.get("thumbnails"):
            thumbnail = info["thumbnails"][-1].get("url", "")
        return VideoItem(
            id=info.get("id", re.sub(r"[^\w]", "_", url)[:40]),
            url=url,
            title=info.get("title", "未知标题"),
            uploader=info.get("uploader") or info.get("channel", "未知"),
            platform=platform,
            upload_date=info.get("upload_date", datetime.datetime.now().strftime("%Y%m%d")),
            duration=int(info.get("duration") or 0),
            thumbnail_url=thumbnail,
            description=info.get("description") or "",
        )
    except Exception as e:
        print(f"  [WARN] 无法获取 URL 元数据: {e}")
        return None


# ── 转录获取 ──────────────────────────────────────────────────────────────
def _parse_detail_segments(detail) -> str:
    """将 BibiGPT 返回的字幕段列表拼接成纯文本，格式：[HH:MM:SS] text"""
    if not isinstance(detail, list) or not detail:
        return ""
    lines = []
    for seg in detail:
        if not isinstance(seg, dict):
            continue
        text = seg.get("text") or seg.get("content") or seg.get("subtitle") or ""
        if not text:
            continue
        start = seg.get("start") or seg.get("startTime") or seg.get("time") or 0
        try:
            start = float(start)
        except (TypeError, ValueError):
            start = 0.0
        h = int(start) // 3600
        m = (int(start) % 3600) // 60
        s = int(start) % 60
        lines.append(f"[{h:02d}:{m:02d}:{s:02d}] {text}")
    return "\n".join(lines)


def get_transcript_bibigpt(url: str) -> str:
    """通过 BibiGPT API 获取原始转录文本"""
    if not BIBIGPT_TOKEN or BIBIGPT_TOKEN == "your_bibigpt_token_here":
        raise RuntimeError("BIBIGPT_API_TOKEN 未配置")
    api_url = "https://api.bibigpt.co/api/v1/getSubtitle"
    headers = {"Authorization": f"Bearer {BIBIGPT_TOKEN}"}
    params = {"url": url, "audioLanguage": "zh"}
    for attempt in range(3):
        try:
            resp = _no_proxy_session.get(api_url, headers=headers, params=params, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            # BibiGPT may return {"subtitle": "..."} or {"data": {"subtitle": "..."}}
            if isinstance(data, dict):
                # Log fields on first call for debugging
                if attempt == 0:
                    print(f"  [DEBUG] BibiGPT 响应字段: {list(data.keys())}")
                detail = data.get("detail") or {}
                # 小红书/online-media 等：字幕分段在 detail.subtitlesArray
                detail_segments = detail.get("subtitlesArray") if isinstance(detail, dict) else None
                transcript = (
                    data.get("subtitle")
                    or data.get("text")
                    or (detail.get("subtitle") if isinstance(detail, dict) else None)
                    or (detail.get("text") if isinstance(detail, dict) else None)
                    or (detail.get("transcript") if isinstance(detail, dict) else None)
                    # detail.subtitlesArray 是分段列表（startTime/text）
                    or _parse_detail_segments(detail_segments)
                    # detail 本身也可能直接是分段列表
                    or _parse_detail_segments(detail)
                    # 纯文本兜底
                    or (detail.get("contentText") if isinstance(detail, dict) else None)
                    or data.get("data", {}).get("subtitle")
                    or data.get("data", {}).get("text")
                    or ""
                )
                if transcript:
                    return transcript
                raise RuntimeError(f"BibiGPT detail 结构未知: {str(detail)[:300]}")
            raise RuntimeError(f"BibiGPT 返回了意外结构: {str(data)[:200]}")
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            is_retryable = status_code == 429 or (status_code is not None and status_code >= 500)
            if not is_retryable:
                raise
            if attempt == 2:
                raise RuntimeError(f"BibiGPT 请求失败 (HTTP {status_code})，已重试 3 次: {e}") from e
            wait = 10 * (attempt + 1)
            print(f"  [WARN] BibiGPT 请求失败 (HTTP {status_code}，尝试 {attempt+1}/3)，{wait}s 后重试...")
            time.sleep(wait)
        except requests.RequestException as e:
            if attempt == 2:
                raise RuntimeError(f"BibiGPT 网络异常，已重试 3 次: {e}") from e
            wait = 10 * (attempt + 1)
            print(f"  [WARN] BibiGPT 网络异常 (尝试 {attempt+1}/3)，{wait}s 后重试...")
            time.sleep(wait)
    raise RuntimeError("BibiGPT 连续3次请求失败")


def get_transcript_baoyu(url: str, cache_dir: Path) -> str:
    """baoyu-youtube-transcript 免费降级方案（无需 API Key）"""
    skill_script = PROJECT_ROOT / "vendor" / "baoyu-youtube-transcript" / "scripts" / "main.ts"
    if not skill_script.exists():
        raise RuntimeError("baoyu 脚本不存在")
    bun_cmd = "bun"
    try:
        subprocess.run(["bun", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        bun_cmd = None
    if bun_cmd:
        cmd = ["bun", str(skill_script)]
    else:
        cmd = ["npx", "-y", "bun", str(skill_script)]
    out_dir = str(cache_dir / "baoyu-cache")
    result = subprocess.run(
        cmd + [url, "--languages", "zh-Hans,zh,en", "--output-dir", out_dir],
        capture_output=True, text=True, encoding="utf-8", timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    if result.returncode != 0:
        raise RuntimeError(f"baoyu 脚本失败: {result.stderr[:300]}")
    # 找到生成的 transcript.md
    out_path = Path(out_dir)
    md_files = list(out_path.rglob("transcript.md"))
    if not md_files:
        raise RuntimeError("baoyu 未生成 transcript.md")
    raw = md_files[0].read_text(encoding="utf-8")
    # 去掉 YAML frontmatter
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            raw = raw[end + 4:].lstrip()
    return raw.strip()


def get_transcript_ytapi(video_id: str) -> str:
    """YouTube transcript-api 降级方案"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id, languages=["zh-Hans", "zh-Hant", "zh", "en"])
        lines = []
        for item in transcript_list:
            start = int(item.start)
            h, m, s = start // 3600, (start % 3600) // 60, start % 60
            lines.append(f"[{h:02d}:{m:02d}:{s:02d}] {item.text}")
        return "\n".join(lines)
    except Exception as e:
        raise RuntimeError(f"youtube-transcript-api 也失败了: {e}")


def _is_original_audio(p: Path) -> bool:
    """原始下载音源判定：排除派生产物（whisper 的 wav/json、Groq 的 .groq.mp3）。
    直链音源本身可能就是 .mp3，不能按扩展名一刀切排除。"""
    return p.suffix not in (".wav", ".json") and not p.name.endswith(".groq.mp3")


def _download_audio(url: str, key: str, cdir: Path) -> Path:
    """下载音频到缓存目录（whisper 本地/Groq 云端共用；已下过不重下）。
    不再强制 android player_client——全局 yt-dlp 配置已有 js-runtimes 药方。"""
    dl = next((p for p in sorted(cdir.glob(f"{key}.*")) if _is_original_audio(p)), None)
    if dl:
        return dl
    ydl = str(PROJECT_ROOT / ".venv" / "bin" / "yt-dlp")
    if not Path(ydl).exists():
        ydl = "yt-dlp"
    subprocess.run([ydl, "-f", "ba/b", "-o", str(cdir / f"{key}.%(ext)s"), url],
                   capture_output=True, text=True, timeout=900)
    dl = next((p for p in sorted(cdir.glob(f"{key}.*")) if _is_original_audio(p)), None)
    if not dl:
        raise RuntimeError("音频下载失败")
    return dl


def _segments_to_lines(segments) -> list[str]:
    """把带 start 秒数的 segments 拼成与其他通道一致的 [HH:MM:SS] 行。"""
    lines = []
    for seg in segments or []:
        try:
            sec = int(float(seg.get("start") or 0))
        except (TypeError, ValueError):
            sec = 0
        txt = (seg.get("text") or "").strip()
        if txt:
            lines.append(f"[{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}] {txt}")
    return lines


def get_transcript_groq(url: str, video_id: str = "") -> str:
    """Groq Whisper 云端转录（whisper-large-v3-turbo，约 $0.04/小时音频）。
    音频下载复用本地缓存目录；转 16kHz 单声道 32kbps mp3 控制上传体积
    （2 小时 ≈ 28MB）。GROQ_API_KEY 缺失直接失败，流水线跳下一通道。"""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY 未配置")
    cdir = WHISPER_CACHE_DIR
    cdir.mkdir(parents=True, exist_ok=True)
    key = video_id or hashlib.sha1(url.encode()).hexdigest()[:16]
    # 独立命名：与「恰好是 mp3 的原始直链音源」区分，防止误传原始大文件
    mp3 = cdir / f"{key}.groq.mp3"
    if not mp3.exists():
        dl = _download_audio(url, key, cdir)
        subprocess.run(["ffmpeg", "-y", "-i", str(dl), "-ar", "16000", "-ac", "1",
                        "-b:a", "32k", str(mp3)], capture_output=True, text=True)
        if not mp3.exists():
            raise RuntimeError("ffmpeg 转 mp3 失败")
    with open(mp3, "rb") as f:
        resp = requests.post(  # 海外 API，走系统代理（默认 session）
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (mp3.name, f, "audio/mpeg")},
            data={"model": "whisper-large-v3-turbo",
                  "response_format": "verbose_json"},
            timeout=600,
        )
    if resp.status_code != 200:
        raise RuntimeError(f"Groq 转录失败 HTTP {resp.status_code}: {resp.text[:200]}")
    lines = _segments_to_lines(resp.json().get("segments"))
    if not lines:
        raise RuntimeError("Groq 返回空转录")
    return "\n".join(lines)


def get_transcript_whisper(url: str, video_id: str = "", lang: str = "auto") -> str:
    """本地 whisper.cpp 转录：任意平台、零 API 成本、中文质量好。
    按 video_id 缓存 wav + json 到 ~/.cache/whisper-cpp/jobs，避免重复转录/下载。
    需要 whisper-cli(brew install whisper-cpp) + 一个 ggml 模型(WHISPER_MODEL 可覆盖)。"""
    model = os.environ.get("WHISPER_MODEL") or str(
        Path.home() / ".cache" / "whisper-cpp" / "ggml-large-v3-turbo.bin")
    if not Path(model).exists():
        raise RuntimeError(f"whisper 模型不存在: {model}")
    if not shutil.which("whisper-cli"):
        raise RuntimeError("whisper-cli 未安装(brew install whisper-cpp)")

    cdir = WHISPER_CACHE_DIR
    cdir.mkdir(parents=True, exist_ok=True)
    key = video_id or hashlib.sha1(url.encode()).hexdigest()[:16]
    jf = cdir / f"{key}.json"

    if not jf.exists():  # 没缓存才下载+转录
        wav = cdir / f"{key}.wav"
        if not wav.exists():
            dl = _download_audio(url, key, cdir)
            subprocess.run(["ffmpeg", "-y", "-i", str(dl), "-ar", "16000", "-ac", "1",
                            str(wav)], capture_output=True, text=True)
            if not wav.exists():
                raise RuntimeError("ffmpeg 转 16k wav 失败")
        rr = subprocess.run(["whisper-cli", "-m", model, "-f", str(wav), "-l", lang,
                             "-oj", "-of", str(cdir / key)],
                            capture_output=True, text=True, timeout=7200)
        if not jf.exists():
            raise RuntimeError(f"whisper 转录失败: {(rr.stderr or '')[-300:]}")

    data = json.loads(jf.read_text(encoding="utf-8"))
    lines = []
    for seg in data.get("transcription", []):
        off = (seg.get("offsets") or {}).get("from")
        if isinstance(off, (int, float)):
            sec = int(off // 1000)
        else:
            t = (seg.get("timestamps") or {}).get("from", "00:00:00").split(",")[0]
            parts = (t.split(":") + ["0", "0", "0"])[:3]
            sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        txt = (seg.get("text") or "").strip()
        if txt:
            lines.append(f"[{sec//3600:02d}:{(sec%3600)//60:02d}:{sec%60:02d}] {txt}")
    if not lines:
        raise RuntimeError("whisper 输出为空")
    return "\n".join(lines)


# ── 工具函数 ──────────────────────────────────────────────────────────────
def sanitize_title(title: str) -> str:
    """将标题转换为安全的文件夹名"""
    # Remove characters not safe for filenames
    safe = re.sub(r'[\\/:*?"<>|]', "", title)
    safe = re.sub(r"\s+", "-", safe.strip())
    # Limit length
    return safe[:60] or "untitled"


def format_duration(seconds: int) -> str:
    if not seconds:
        return "未知"
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def make_archive_dir(upload_date: str, title: str, item_id: str) -> tuple[Path, bool]:
    """返回 (目录, 是否本次新建)。created 决定失败时能否 rmtree——
    mkdir(exist_ok=True) 可能落到既有目录（同日同名重跑、metadata 损坏
    未被 resolve 认领），这种目录不算本次新建、不可当空壳清理。"""
    date_str = upload_date[:8] if len(upload_date) >= 8 else datetime.datetime.now().strftime("%Y%m%d")
    # Include a stable id suffix to avoid collisions on same-day duplicate/truncated titles.
    unique_suffix = hashlib.sha1(item_id.encode("utf-8")).hexdigest()[:8]
    folder_name = f"{date_str}-{sanitize_title(title)}-{unique_suffix}"
    path = ARCHIVE_DIR / folder_name
    created = not path.exists()
    path.mkdir(parents=True, exist_ok=True)
    return path, created


def resolve_archive_dir(archive_root: Path, item_id: str) -> Path | None:
    """按 id 的 sha1 后缀查找既有归档目录，找到即复用、不再新建。

    同一视频的 upload_date/title 会随抓取来源漂移（flat entry 常缺日期，
    目录名落到当天日期），历史上导致同一 id 每天新建一个目录。目录名
    后缀只依赖 id，据此聚合；metadata 的 id 必须与 item_id 相等（防
    后缀撞车）。多个命中时优先 rewrite_complete=True，其次目录名最新。
    空 id 或无命中返回 None（走原新建逻辑）。"""
    if not item_id:
        return None
    suffix = hashlib.sha1(item_id.encode("utf-8")).hexdigest()[:8]
    candidates = []
    for d in Path(archive_root).glob(f"*-{suffix}"):
        if not d.is_dir():
            continue
        try:
            meta = json.loads((d / "metadata.json").read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(meta.get("id") or "") != str(item_id):
            continue
        candidates.append((bool(meta.get("rewrite_complete")), d.name, d))
    if not candidates:
        return None
    candidates.sort(key=lambda t: (t[0], t[1]), reverse=True)
    return candidates[0][2]


def discard_failed_archive(archive_dir: Path, dir_created: bool, reason: str):
    """失败清理的唯一出口：只删本次新建的空壳。

    ⚠️ 不变量：复用的既有目录（dir_created=False）含付费转录等资产，
    任何失败路径都必须原样保留。新增失败早退时一律调这里，不要手写 rmtree。"""
    if dir_created:
        shutil.rmtree(archive_dir, ignore_errors=True)
        print(f"  [清理] {reason}，已删除本次新建目录（下次可重试）")
    else:
        print(f"  [保留] {reason}，复用目录不删除（含既有资产，下次可重试）")


def read_existing_transcript(archive_dir: Path) -> tuple[str, str]:
    """读取复用目录里已有的有效转录正文，返回 (正文, 来源)。

    转录是最贵资产（BibiGPT 按时长计费）——复用目录时若已有有效转录，
    直接用正文、完全跳过转录链。失败标记/空正文视为无效，返回 ("", "")。"""
    tp = archive_dir / "transcript.md"
    if not tp.exists():
        return "", ""
    try:
        raw = tp.read_text(encoding="utf-8")
    except Exception:
        return "", ""
    body, source = raw, ""
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            header = raw[3:end]
            m = re.search(r"^transcript_source:\s*(\S+)", header, re.MULTILINE)
            if m:
                source = m.group(1)
            body = raw[end + 4:]
    body = body.strip()
    if not body or body.startswith((FAIL_MARK_ERROR, FAIL_MARK_EMPTY)):
        return "", ""
    return body, (source if source and source != "none" else "existing")


def download_thumbnail(url: str, dest: Path) -> bool:
    if not url:
        return False
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")
        suffix = ".jpg"
        if "webp" in content_type:
            suffix = ".webp"
        elif "png" in content_type:
            suffix = ".png"
        # rename dest with correct suffix if needed
        final_dest = dest.with_suffix(suffix)
        for stale_ext in (".jpg", ".jpeg", ".png", ".webp"):
            stale_path = dest.with_suffix(stale_ext)
            if stale_path != final_dest and stale_path.exists():
                stale_path.unlink()
        final_dest.write_bytes(resp.content)
        return True
    except Exception as e:
        print(f"  [WARN] 封面下载失败: {e}")
        return False


# ── 核心处理 ──────────────────────────────────────────────────────────────
def process_item(item: VideoItem) -> bool | None:
    """处理单个内容项，返回 True=完全成功, False=异常失败, None=转录失败可重试"""
    print(f"\n处理: {item.title[:60]}")
    try:
        # 1. 归档目录：先按 id 复用既有目录（防同一内容重复建目录），无命中才新建
        reused_dir = resolve_archive_dir(ARCHIVE_DIR, item.id)
        if reused_dir is not None:
            archive_dir = reused_dir
            dir_created = False
            print(f"  [复用] 已有归档目录: {archive_dir.name}")
        else:
            archive_dir, dir_created = make_archive_dir(item.upload_date, item.title, item.id)
        meta_path = archive_dir / "metadata.json"
        if meta_path.exists():
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
            if existing.get("rewrite_complete"):
                print(f"  [跳过] 已处理过")
                return True

        # 2. 获取转录（免费优先：YouTube 先试免费方案，失败/非 YouTube 才用 BibiGPT 付费）
        transcript = ""
        transcript_source = ""
        transcript_error = ""
        transcript_reused = False

        # 复用目录里已有的有效转录：直接用正文，跳过整条转录链（避免 BibiGPT 复费）
        if not dir_created:
            transcript, transcript_source = read_existing_transcript(archive_dir)
            if transcript:
                transcript_reused = True
                print(f"  [复用] 已有转录 ({len(transcript)} 字符, 来源: {transcript_source})")

        # 免费方案（仅 YouTube 可用）：baoyu → youtube-transcript-api
        if not transcript and item.platform == "youtube":
            try:
                print("  [免费1] baoyu-youtube-transcript ...")
                transcript = get_transcript_baoyu(item.url, archive_dir)
                transcript_source = "baoyu"
                print(f"  [OK] baoyu 转录成功 ({len(transcript)} 字符)")
            except Exception as e_baoyu:
                print(f"  [WARN] baoyu 失败: {e_baoyu}")
                try:
                    print("  [免费2] youtube-transcript-api ...")
                    transcript = get_transcript_ytapi(item.id)
                    transcript_source = "youtube-transcript-api"
                    print(f"  [OK] 免费转录成功 ({len(transcript)} 字符)")
                except Exception as e_ytapi:
                    print(f"  [WARN] 免费方案全失败: {e_ytapi}")

        # 云端优先原则（2026-07-11 用户拍板）：免费字幕 API → Groq 云端 whisper
        # （几分钱）→ BibiGPT 全托管付费 → whisper 本地（最最兜底）
        if not transcript:
            try:
                print("  [云端] Groq whisper 转录中（约 $0.04/小时音频）...")
                transcript = get_transcript_groq(item.url, item.id)
                transcript_source = "groq-whisper"
                print(f"  [OK] Groq 转录成功 ({len(transcript)} 字符)")
            except Exception as e_groq:
                print(f"  [WARN] Groq 失败: {e_groq}")

        # 全托管付费云（他们服务器抓取，本地下载被反爬拦时的接棒者）
        if not transcript:
            try:
                print("  [BibiGPT] 获取转录中（付费）...")
                transcript = get_transcript_bibigpt(item.url)
                transcript_source = "bibigpt"
                print(f"  [OK] BibiGPT 转录成功 ({len(transcript)} 字符)")
            except Exception as e_bibi:
                transcript_error = str(e_bibi)
                print(f"  [WARN] BibiGPT 失败: {e_bibi}")

        # 本地 whisper.cpp 最最兜底（零 API 成本但慢，首次约 10-15 分钟）
        if not transcript:
            try:
                print("  [本地兜底] whisper.cpp 转录中...")
                transcript = get_transcript_whisper(item.url, item.id)
                transcript_source = "whisper-local"
                print(f"  [OK] 本地 whisper 转录成功 ({len(transcript)} 字符)")
            except Exception as e_w:
                transcript_error = transcript_error or str(e_w)
                print(f"  [WARN] 本地 whisper 失败: {e_w}")

        # 3. 写 transcript.md
        transcript_path = archive_dir / "transcript.md"
        safe_title = (item.title or "").replace('"', '\\"')
        safe_uploader = (item.uploader or "").replace('"', '\\"')
        transcript_content = f"""---
source_url: "{item.url}"
platform: {item.platform}
uploader: "{safe_uploader}"
title: "{safe_title}"
upload_date: "{item.upload_date}"
duration: {item.duration}
fetched_at: "{datetime.datetime.utcnow().isoformat()}Z"
transcript_source: {transcript_source or 'none'}
---

"""
        if transcript:
            transcript_content += transcript
        elif transcript_error:
            transcript_content += f"{FAIL_MARK_ERROR}: {transcript_error}]"
        else:
            transcript_content += f"{FAIL_MARK_EMPTY}]"
        if not transcript_reused:
            # 复用的转录不重写文件：原 front-matter（真实抓取日期/来源）比
            # flat entry 的漂移信息更可信，且保证复用目录字节不变
            transcript_path.write_text(transcript_content, encoding="utf-8")

        # 4. 下载封面（复用目录已有封面时跳过）
        cover_path = archive_dir / "cover.jpg"
        if dir_created or not any(archive_dir.glob("cover.*")):
            download_thumbnail(item.thumbnail_url, cover_path)

        # 5. 写 metadata.json
        meta = {
            **asdict(item),
            "archive_dir": str(archive_dir),
        }
        if not dir_created and meta_path.exists():
            # flat entry 的元信息常缺失/漂移（upload_date 为空、duration=0、标题
            # 落到「未知标题」等占位值）；复用目录时，既有 metadata 里的有效值
            # 比新 item 的空值/占位值可信
            _PLACEHOLDERS = ("None", "未知", "未知标题", "未知集", "直接链接")
            try:
                prev = json.loads(meta_path.read_text(encoding="utf-8"))
                for k in ("upload_date", "title", "uploader", "thumbnail_url",
                          "description", "duration"):
                    prev_v, new_v = prev.get(k), meta.get(k)
                    if prev_v in (None, "", 0, "None"):
                        continue
                    if not new_v or str(new_v) in _PLACEHOLDERS:
                        meta[k] = prev_v
            except Exception:
                pass
        meta.update({
            "processed_at": datetime.datetime.utcnow().isoformat() + "Z",
            "transcript_available": bool(transcript),
            "transcript_source": transcript_source,
            "rewrite_complete": False,
            "feishu_synced": False,
            "feishu_record_id": None,
            "feishu_doc_synced": False,
            "feishu_doc_id": None,
            "feishu_doc_url": None,
        })
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        # 6. 调用 rewrite.js
        if transcript:
            print("  [AI] 调用改写脚本...")
            result = subprocess.run(
                ["node", "scripts/rewrite.js", str(archive_dir)],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if result.returncode == 0:
                print("  [OK] AI 改写完成")
            else:
                print(f"  [WARN] rewrite.js 失败 (exit {result.returncode})")
                if result.stderr:
                    print(f"       {result.stderr[:300]}")
                discard_failed_archive(archive_dir, dir_created, "改写失败")
                return False
        else:
            print("  [跳过] 无转录文本，跳过 AI 改写")
            discard_failed_archive(archive_dir, dir_created, "无可用转录")
            return None  # 转录失败，不写入 state，下次可重试

        return True

    except Exception as e:
        print(f"  [ERROR] 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False


# ── 批量模式 UI ────────────────────────────────────────────────────────────
def batch_confirm(items: list[VideoItem]) -> list[VideoItem]:
    """显示待处理列表，让用户选择"""
    print(f"\n找到 {len(items)} 条未处理内容：\n")
    for i, item in enumerate(items, 1):
        date_str = item.upload_date
        if len(date_str) == 8:
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        duration_str = format_duration(item.duration)
        platform_icons = {"youtube": "YouTube", "bilibili": "Bilibili", "xiaoyuzhou": "小宇宙", "audio": "音频"}
        platform_label = platform_icons.get(item.platform, item.platform)
        title_short = item.title[:50] + ("..." if len(item.title) > 50 else "")
        print(f"  [{i:2d}] ✓ {platform_label:8s} | {item.uploader[:15]:15s} | {date_str} | \"{title_short}\" ({duration_str})")

    print("\n操作：直接回车=全部处理  输入数字(如 1,3)=切换选择  n=取消\n")
    selected = list(range(len(items)))  # 默认全选

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已取消")
            return []

        if user_input.lower() == "n":
            print("已取消")
            return []
        elif user_input == "":
            break
        else:
            # Toggle specified indices
            try:
                nums = [int(x.strip()) - 1 for x in user_input.split(",")]
                for idx in nums:
                    if 0 <= idx < len(items):
                        if idx in selected:
                            selected.remove(idx)
                        else:
                            selected.append(idx)
                # Show updated selection
                print("当前选中：", ", ".join(str(i + 1) for i in sorted(selected)) or "（无）")
                print("直接回车确认，继续输入数字调整，n 取消")
            except ValueError:
                print("输入格式错误，请输入数字（如 1,3）或直接回车")

    return [items[i] for i in sorted(selected)]


# ── 命令：批量模式 ─────────────────────────────────────────────────────────
def cmd_batch(args):
    sources = load_sources()
    processed = load_state()
    limit = args.limit or 5

    all_items: list[VideoItem] = []

    for cfg in sources.get("youtube") or []:
        items = fetch_youtube_channel(cfg, cfg.get("limit", limit))
        all_items.extend(items)

    for cfg in sources.get("bilibili") or []:
        items = fetch_bilibili_up(cfg, cfg.get("limit", limit))
        all_items.extend(items)

    for cfg in sources.get("xiaoyuzhou") or []:
        items = fetch_xiaoyuzhou_rss(cfg, cfg.get("limit", limit))
        all_items.extend(items)

    # Filter already processed
    new_items = [item for item in all_items if item.id not in processed]

    if not new_items:
        print("\n没有新内容需要处理。")
        return

    auto = getattr(args, 'auto', False)
    if auto:
        to_process = new_items
        print(f"\n[AUTO] 自动处理全部 {len(new_items)} 条新内容")
    else:
        to_process = batch_confirm(new_items)
    if not to_process:
        return

    ok, fail, skipped = 0, 0, 0
    for item in to_process:
        result = process_item(item)
        if result is True:
            processed[item.id] = datetime.datetime.utcnow().isoformat()
            save_state(processed)
            ok += 1
        elif result is None:
            skipped += 1
            print(f"  [INFO] 转录失败，未标记已处理，下次运行可重试")
        else:
            fail += 1

    print(f"\n完成：成功 {ok}，失败 {fail}，待重试 {skipped}")


# ── 命令：URL 模式 ─────────────────────────────────────────────────────────
def cmd_url(args):
    processed = load_state()
    urls = args.urls
    ok, fail = 0, 0

    for url in urls:
        print(f"\n获取元数据: {url}")
        item = fetch_single_url(url)
        if not item:
            print(f"  [ERROR] 无法获取元数据，跳过")
            fail += 1
            continue

        result = process_item(item)
        if result is True:
            processed[item.id] = datetime.datetime.utcnow().isoformat()
            save_state(processed)
            ok += 1
        elif result is None:
            print(f"  [INFO] 转录失败，未标记已处理，下次运行可重试")
        else:
            fail += 1

    print(f"\n完成：成功 {ok}，失败 {fail}")


# ── 入口 ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="每日内容策展抓取工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--batch", action="store_true", help="扫描订阅源批量处理（交互选择）")
    group.add_argument("--url", nargs="+", dest="urls", metavar="URL", help="直接处理指定 URL")
    parser.add_argument("--limit", type=int, default=5, help="每个源检查最近几条（默认5）")
    parser.add_argument("--auto", action="store_true", help="自动处理全部新内容，不等待确认（适合定时任务）")

    args = parser.parse_args()

    if args.batch:
        cmd_batch(args)
    elif args.urls:
        cmd_url(args)


if __name__ == "__main__":
    main()
