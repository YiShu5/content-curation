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
import os
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
TOP_K = 3               # 每天「今日必读」条数（最狠降噪）
PRESELECT = 15          # AI HOT 分粗筛保留数，再交 DeepSeek 精排
MAX_LINKS = 2
CHUNK_SECONDS = 15      # transcript 切块窗口
MIN_DOC_SCORE = 0.45    # 新闻↔内容 文档级匹配阈值（宁可少而准）
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


_RANK_PROMPT = """你是 AI 行业主编。下面是今天全网抓取的 AI 资讯候选，请选出最重要的 {k} 条「今日必读」。

判定标准（重要性从高到低）：
- 最高：重大模型发布 / 能力突破（如某模型上多模态）、新范式或新概念（如 loop 工程）、影响全行业的大事
- 低（不要选）：教程、小工具、个人随感、八卦、营销

请选出**最多 {k} 条**真正重要的，按重要性从高到低排序（第 1 条最重磅）：
- 优先：重大模型发布/能力突破、新范式或新概念、影响全行业的大事
- 教程/工具：只有当它代表新范式或被业界广泛关注才选
- 纯营销、蹭节日活动、个人随感、八卦：一律不选
**条数可少于 {k}（哪怕只有 1 条）；绝不为凑数收录低价值内容。**

只输出 JSON：{{"top":[{{"index":序号,"why":"一句话说清为什么重要"}}, ...]}}（index 基于下面编号）

候选：
{items}
"""


def _chat_json(prompt, temperature=0.2):
    """调用 DeepSeek（OpenAI 兼容）做重要性精排，强制 JSON 输出。"""
    key = os.getenv("OPENAI_API_KEY", "")
    base = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "deepseek-chat")
    resp = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}],
              "response_format": {"type": "json_object"}, "temperature": temperature},
        timeout=60,
    )
    resp.raise_for_status()
    return json.loads(resp.json()["choices"][0]["message"]["content"])


def _rank_important(news, k=TOP_K):
    """AI HOT 分粗筛（tip 沉底）→ DeepSeek 按重要性精排，返回 top-k（带 why）。"""
    pool = sorted(news, key=lambda n: (1 if n.get("category") == "tip" else 0,
                                       -(n.get("score") or 0)))[:PRESELECT]
    if not pool:
        return []
    lines = [f"{i+1}. [{n.get('category') or '-'}|{n.get('score') or 0}分] "
             f"{n.get('title','')}｜{(n.get('summary') or '')[:80]}"
             for i, n in enumerate(pool)]
    data = _chat_json(_RANK_PROMPT.format(k=k, items="\n".join(lines)))
    out = []
    for item in (data.get("top") or [])[:k]:
        idx = item.get("index")
        if isinstance(idx, int) and 1 <= idx <= len(pool):
            n = dict(pool[idx - 1])
            n["why"] = (item.get("why") or "").strip()
            out.append(n)
    return out


def get_signals(records):
    """主入口：AI HOT 每日 AI 洪流 → DeepSeek 重要性精排出 top-K「今日必读」（降噪核心），
    每条再附上库里相关深度内容（可选）。任何环节缺依赖/出错由调用方 try/except 兜底。"""
    now = time.time()
    if SIGNAL_CACHE.exists():
        try:
            c = json.loads(SIGNAL_CACHE.read_text(encoding="utf-8"))
            if now < c.get("expiry", 0):
                return c.get("signals", [])
        except Exception:
            pass

    news = fetch_aihot()
    if not news:
        return []

    # ① 降噪核心：粗筛 + DeepSeek 精排出 top-K 必读
    top = _rank_important(news, TOP_K)
    if not top:
        return []

    # ② 附属：给每条必读找库里相关深度内容（向量匹配，全局去重；缺依赖/无匹配则不附）
    arch_by_key = _archive_by_key()
    index = embeddings.load_index()
    mat_n, ids, by_id = None, [], {}
    if np is not None and index and records:
        by_id = {r.get("id"): r for r in records}
        vecs = []
        for rid, item in index.items():
            if rid in by_id and item.get("vector"):
                ids.append(rid)
                vecs.append(item["vector"])
        if vecs:
            mat = np.asarray(vecs, dtype=np.float32)
            mat_n = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-8)

    used = set()
    signals = []
    for n in top:
        links = []
        if mat_n is not None:
            try:
                nv = np.asarray(embeddings.embed_query(
                    ((n.get("title") or "") + "。" + (n.get("summary") or "")).strip()),
                    dtype=np.float32)
                sims = mat_n @ (nv / (np.linalg.norm(nv) + 1e-8))
                for j in np.argsort(-sims):
                    if len(links) >= MAX_LINKS:
                        break
                    score = float(sims[j])
                    if score < MIN_DOC_SCORE:
                        break
                    rec = by_id[ids[j]]
                    rid = rec.get("id")
                    if rid in used:
                        continue
                    arch = arch_by_key.get(_content_key(rec.get("link") or ""))
                    if not arch:
                        continue
                    loc = _locate_timestamp(arch, nv)
                    if loc is None:
                        continue
                    sec, snippet, cscore = loc
                    url = rec.get("link") or ""
                    show_ts = _supports_ts(url) and cscore >= MIN_CHUNK_SCORE
                    used.add(rid)
                    links.append({
                        "record_id": rid,
                        "title": rec.get("title", ""),
                        "platform": rec.get("platform", ""),
                        "deeplink": _deeplink(url, sec) if show_ts else url,
                        "ts": _fmt_ts(sec) if show_ts else "",
                        "match": round(score * 100),
                    })
            except Exception:
                links = []
        signals.append({
            "title": n.get("title", ""),
            "source": n.get("source", ""),
            "url": n.get("url", ""),
            "summary": (n.get("summary") or "")[:120],
            "category": n.get("category") or "",
            "why": n.get("why", ""),
            "links": links,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_CACHE.write_text(
        json.dumps({"expiry": now + SIGNAL_TTL,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "signals": signals}, ensure_ascii=False),
        encoding="utf-8")
    return signals
