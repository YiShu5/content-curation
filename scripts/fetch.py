#!/usr/bin/env python
"""
每日内容策展 - 内容抓取与归档脚本
用法:
  python scripts/fetch.py --batch [--limit N]
  python scripts/fetch.py --url URL [URL2 ...]
"""

import argparse
import datetime
import json
import os
import re
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
            id=re.sub(r"[^\w]", "_", url)[:40],
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
                transcript = (
                    data.get("subtitle")
                    or data.get("text")
                    or (detail.get("subtitle") if isinstance(detail, dict) else None)
                    or (detail.get("text") if isinstance(detail, dict) else None)
                    or (detail.get("transcript") if isinstance(detail, dict) else None)
                    # detail may be a list of subtitle segments
                    or _parse_detail_segments(detail)
                    or data.get("data", {}).get("subtitle")
                    or data.get("data", {}).get("text")
                    or ""
                )
                if transcript:
                    return transcript
                raise RuntimeError(f"BibiGPT detail 结构未知: {str(detail)[:300]}")
            raise RuntimeError(f"BibiGPT 返回了意外结构: {str(data)[:200]}")
        except requests.HTTPError as e:
            if e.response.status_code < 500 or attempt == 2:
                raise
            print(f"  [WARN] BibiGPT 请求失败 (尝试 {attempt+1}/3)，10s 后重试...")
            time.sleep(10)
    raise RuntimeError("BibiGPT 连续3次请求失败")


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


def make_archive_dir(upload_date: str, title: str) -> Path:
    date_str = upload_date[:8] if len(upload_date) >= 8 else datetime.datetime.now().strftime("%Y%m%d")
    folder_name = f"{date_str}-{sanitize_title(title)}"
    path = ARCHIVE_DIR / folder_name
    path.mkdir(parents=True, exist_ok=True)
    return path


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
        # 1. 创建归档目录
        archive_dir = make_archive_dir(item.upload_date, item.title)
        meta_path = archive_dir / "metadata.json"
        if meta_path.exists():
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
            if existing.get("rewrite_complete"):
                print(f"  [跳过] 已处理过")
                return True

        # 2. 获取转录
        transcript = ""
        transcript_source = ""
        transcript_error = ""
        try:
            print("  [BibiGPT] 获取转录中...")
            transcript = get_transcript_bibigpt(item.url)
            transcript_source = "bibigpt"
            print(f"  [OK] 转录获取成功 ({len(transcript)} 字符)")
        except Exception as e:
            print(f"  [WARN] BibiGPT 失败: {e}")
            if item.platform == "youtube":
                try:
                    print("  [降级] 尝试 youtube-transcript-api ...")
                    transcript = get_transcript_ytapi(item.id)
                    transcript_source = "youtube-transcript-api"
                    print(f"  [OK] 降级转录成功 ({len(transcript)} 字符)")
                except Exception as e2:
                    transcript_error = str(e2)
                    print(f"  [WARN] 转录降级也失败: {e2}")
            else:
                transcript_error = str(e)

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
            transcript_content += f"[转录获取失败: {transcript_error}]"
        else:
            transcript_content += "[无可用转录]"
        transcript_path.write_text(transcript_content, encoding="utf-8")

        # 4. 下载封面
        cover_path = archive_dir / "cover.jpg"
        download_thumbnail(item.thumbnail_url, cover_path)

        # 5. 写 metadata.json
        meta = {
            **asdict(item),
            "archive_dir": str(archive_dir),
            "processed_at": datetime.datetime.utcnow().isoformat() + "Z",
            "transcript_available": bool(transcript),
            "transcript_source": transcript_source,
            "rewrite_complete": False,
            "feishu_synced": False,
            "feishu_record_id": None,
            "feishu_doc_synced": False,
            "feishu_doc_id": None,
            "feishu_doc_url": None,
        }
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
        else:
            print("  [跳过] 无转录文本，跳过 AI 改写")
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
