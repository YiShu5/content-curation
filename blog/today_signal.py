"""
今日信号 - 独立模块（失败不影响现有页面）

流程：拉取 AI HOT 过去 24h 精选 AI 新闻 → 与本地向量索引语义匹配找相关深度内容
→ 在该内容的 transcript.md 里定位最相关的时间戳 → 生成可跳转深链。

约定：
- AI HOT 调用在后端做，带浏览器 User-Agent（否则 403），结果缓存 30 分钟
- transcript 切成 ~15s 小块向量化，按 archive 持久化（npy+json），复用
- 组装好的信号（含时间戳映射）持久化到 today_signal.json
- 最多 5 条信号，每条最多 2 个本地关联；无时间戳的 transcript 跳过
"""
import hashlib
import json
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

try:
    import numpy as np
except ImportError:
    np = None

import embeddings  # 复用 embed_texts / load_index / 维度配置

AIHOT_URL = "https://aihot.virxact.com/api/public/items"
# /api/public/* 有 UA 黑名单，必须带浏览器 UA，否则 403
AIHOT_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 aihot-skill/0.2.0")

DATA_DIR = Path(__file__).parent / "data"
CHUNK_DIR = DATA_DIR / "transcript_chunks"
SIGNAL_CACHE = DATA_DIR / "today_signal.json"
ARCHIVE_ROOT = Path(__file__).parent.parent / "archive"

AIHOT_TTL = 1800        # AI HOT 缓存 30 分钟
SIGNAL_TTL = 1800       # 组装信号缓存 30 分钟
MAX_SIGNALS = 5
MAX_LINKS = 2
CHUNK_SECONDS = 15      # transcript 切块窗口
MIN_DOC_SCORE = 0.32    # 新闻↔内容 文档级匹配阈值
MIN_CHUNK_SCORE = 0.20  # 块级时间戳匹配阈值（低于此说明定位不可靠，仍给链接但不带时间戳）

_TS_RE = re.compile(r'\[(\d{2}):(\d{2}):(\d{2})\]')
_aihot_cache = {"items": None, "expiry": 0}


# ── 工具 ────────────────────────────────────────────────────────────────────
def _content_key(url):
    """从 URL 提取稳定内容键（与 app.py 同口径，避免循环 import 这里复制一份）"""
    if not url:
        return ""
    m = re.search(r'(?:youtu\.be/|[?&]v=|/embed/|/shorts/)([A-Za-z0-9_-]{11})', url)
    if m:
        return "yt:" + m.group(1)
    m = re.search(r'xiaohongshu\.com/explore/([A-Za-z0-9]+)', url)
    if m:
        return "xhs:" + m.group(1)
    m = re.search(r'(BV[A-Za-z0-9]+)', url)
    if m:
        return "bili:" + m.group(1)
    return url.split('?')[0].rstrip('/')


def _fmt_ts(sec):
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _supports_ts(url):
    """该平台是否支持带时间戳深链跳转"""
    return bool(url) and any(p in url for p in
                             ("youtube.com", "youtu.be", "bilibili.com", "xiaoyuzhou"))


def _deeplink(url, sec):
    """按平台拼带时间戳深链；不支持的平台返回原链接"""
    if not url or sec is None:
        return url
    if "youtube.com" in url or "youtu.be" in url:
        return url + ("&" if "?" in url else "?") + f"t={sec}s"
    if "bilibili.com" in url:
        return url + ("&" if "?" in url else "?") + f"t={sec}"
    if "xiaoyuzhou" in url:
        return url + ("&" if "?" in url else "?") + f"t={sec}"
    return url  # 小红书/音频等：无可靠时间戳深链


def _cos(mat, vec):
    mat = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-8)
    vec = vec / (np.linalg.norm(vec) + 1e-8)
    return mat @ vec


# ── AI HOT ──────────────────────────────────────────────────────────────────
def fetch_aihot():
    """拉取过去 24h 精选新闻，缓存 30 分钟。失败抛异常由调用方兜底。"""
    now = time.time()
    if _aihot_cache["items"] is not None and now < _aihot_cache["expiry"]:
        return _aihot_cache["items"]
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    resp = requests.get(
        AIHOT_URL,
        params={"mode": "selected", "since": since, "take": 50},
        headers={"User-Agent": AIHOT_UA},
        timeout=15,
    )
    resp.raise_for_status()
    items = resp.json().get("items", [])
    _aihot_cache["items"] = items
    _aihot_cache["expiry"] = now + AIHOT_TTL
    return items


# ── transcript 切块 + 向量缓存 ───────────────────────────────────────────────
def _parse_segments(text):
    """把 transcript 正文解析为 [{sec, text}]；无时间戳返回 []"""
    segs = []
    cur = None
    for line in text.splitlines():
        m = _TS_RE.search(line)
        if m:
            sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            clean = _TS_RE.sub("", line).replace("→", " ").strip().lstrip("-").strip()
            cur = {"sec": sec, "text": clean}
            segs.append(cur)
        elif cur is not None and line.strip():
            cur["text"] += " " + line.strip()
    return segs


def _chunk(segs, window=CHUNK_SECONDS):
    chunks = []
    cur = None
    for s in segs:
        if cur is None or s["sec"] - cur["sec"] >= window:
            cur = {"sec": s["sec"], "text": s["text"][:400]}
            chunks.append(cur)
        elif len(cur["text"]) < 400:
            cur["text"] = (cur["text"] + " " + s["text"])[:400]
    return chunks


def _load_or_build_chunks(archive_dir):
    """返回 (chunks_meta, vectors_np)；transcript 无时间戳返回 (None, None)。
    按 transcript 内容 hash 持久化到 CHUNK_DIR，复用。"""
    tpath = archive_dir / "transcript.md"
    if not tpath.exists():
        return None, None
    raw = tpath.read_text(encoding="utf-8")
    body = raw.split("---", 2)[-1] if raw.startswith("---") else raw
    segs = _parse_segments(body)
    if not segs:
        return None, None  # 无时间戳，跳过
    chunks = _chunk(segs)
    if not chunks:
        return None, None

    key = archive_dir.name
    h = hashlib.sha1(body.encode("utf-8")).hexdigest()[:12]
    meta_path = CHUNK_DIR / f"{key}.json"
    vec_path = CHUNK_DIR / f"{key}.npy"

    if meta_path.exists() and vec_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("hash") == h:
                return meta["chunks"], np.load(vec_path)
        except Exception:
            pass

    vecs = embeddings.embed_texts([c["text"] for c in chunks])
    arr = np.asarray(vecs, dtype=np.float32)
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    np.save(vec_path, arr)
    meta_path.write_text(json.dumps({"hash": h, "chunks": chunks}, ensure_ascii=False),
                         encoding="utf-8")
    return chunks, arr


def _locate_timestamp(archive_dir, news_vec):
    """在该内容里定位与新闻最相关的块，返回 (sec, snippet, score)；无时间戳返回 None"""
    chunks, vecs = _load_or_build_chunks(archive_dir)
    if not chunks:
        return None
    sims = _cos(vecs, news_vec)
    i = int(np.argmax(sims))
    return chunks[i]["sec"], chunks[i]["text"][:60], float(sims[i])


# ── 组装信号 ────────────────────────────────────────────────────────────────
def _archive_by_key():
    """content_key -> archive_dir（只收已改写完成的）"""
    out = {}
    if not ARCHIVE_ROOT.exists():
        return out
    for d in ARCHIVE_ROOT.iterdir():
        mp = d / "metadata.json"
        if not d.is_dir() or not mp.exists():
            continue
        try:
            m = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not m.get("rewrite_complete"):
            continue
        k = _content_key(m.get("url") or "")
        if k:
            out.setdefault(k, d)
    return out


def get_signals(records):
    """主入口。records = 已 enrich 的飞书记录列表（含 id/link/platform/title/cover_token）。
    返回信号列表；任何环节缺依赖/出错由调用方 try/except 兜底。"""
    if np is None:
        return []
    # 缓存
    now = time.time()
    if SIGNAL_CACHE.exists():
        try:
            c = json.loads(SIGNAL_CACHE.read_text(encoding="utf-8"))
            if now < c.get("expiry", 0):
                return c.get("signals", [])
        except Exception:
            pass

    news = fetch_aihot()
    index = embeddings.load_index()
    if not news or not index:
        return []

    by_id = {r.get("id"): r for r in records}
    arch_by_key = _archive_by_key()

    # 文档级向量矩阵（与新闻比对）
    ids, mat = [], []
    for rid, item in index.items():
        if rid in by_id and item.get("vector"):
            ids.append(rid)
            mat.append(item["vector"])
    if not ids:
        return []
    mat = np.asarray(mat, dtype=np.float32)
    mat_n = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-8)  # 归一化一次，循环内复用

    # 批量向量化新闻（标题 + 摘要）
    texts = [((n.get("title") or "") + "。" + (n.get("summary") or "")).strip() for n in news]
    news_vecs = np.asarray(embeddings.embed_texts(texts), dtype=np.float32)

    candidates = []
    for n, nv in zip(news, news_vecs):
        sims = mat_n @ (nv / (np.linalg.norm(nv) + 1e-8))
        order = np.argsort(-sims)
        links, seen = [], set()
        for j in order:
            score = float(sims[j])
            if score < MIN_DOC_SCORE or len(links) >= MAX_LINKS:
                break
            rec = by_id[ids[j]]
            title = rec.get("title", "")
            if title in seen:
                continue
            seen.add(title)
            # 时间戳定位
            arch = arch_by_key.get(_content_key(rec.get("link") or ""))
            if not arch:
                continue
            loc = _locate_timestamp(arch, nv)
            if loc is None:
                continue  # transcript 无时间戳 → 跳过这个关联
            sec, snippet, cscore = loc
            url = rec.get("link") or ""
            # 仅当平台支持深链跳转、且定位足够可靠时，才展示可跳转的时间戳
            show_ts = _supports_ts(url) and cscore >= MIN_CHUNK_SCORE
            links.append({
                "record_id": rec.get("id"),
                "title": title,
                "platform": rec.get("platform", ""),
                "cover_token": rec.get("cover_token", ""),
                "deeplink": _deeplink(url, sec) if show_ts else url,
                "ts": _fmt_ts(sec) if show_ts else "",
                "snippet": snippet if show_ts else "",
                "match": round(score * 100),
            })
        if links:  # 只保留能关联到本地深度内容的新闻
            candidates.append({
                "title": n.get("title", ""),
                "source": n.get("source", ""),
                "url": n.get("url", ""),
                "summary": (n.get("summary") or "")[:120],
                "category": n.get("category") or "",
                "score": n.get("score") or 0,
                "best": links[0]["match"],
                "links": links,
            })

    candidates.sort(key=lambda x: -x["best"])
    signals = candidates[:MAX_SIGNALS]

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_CACHE.write_text(
        json.dumps({"expiry": now + SIGNAL_TTL,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "signals": signals}, ensure_ascii=False),
        encoding="utf-8")
    return signals
