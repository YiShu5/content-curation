"""
今日信号 - 独立模块（失败不影响现有页面）

流程：拉取 AI HOT 过去 48h 精选 AI 新闻 → 核对原文 → 选出可空缺的
「1 条顶级大新闻 + 3 个固定判断位」→ 库内优先匹配深度内容，必要时补 1 条 YouTube。

约定：
- AI HOT 调用在后端做，带浏览器 User-Agent（否则 403），结果缓存 30 分钟
- transcript 切成 ~15s 小块向量化，按 archive 持久化（npy+json），复用
- 组装好的信号（含时间戳映射）持久化到 today_signal.json
- 每个信号最多 1 个本地关联；全页最多 1 个外部 YouTube 推荐
"""
import hashlib
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

try:
    import numpy as np
except ImportError:
    np = None

import embeddings  # 复用 embed_texts / load_index / 维度配置
from source_reader import read_original
from tool_probe import probe_command
from user_preferences import behavior_summary, load_profile, prompt_context

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
WINDOW_HOURS = 48
TOP_K = 3               # 三个固定日常判断位；允许为空
PRESELECT = 30          # AI HOT 粗筛后交给模型选原文核验候选
SHORTLIST_N = 12        # 真正读取原文的上限
MAX_LINKS = 1
CHUNK_SECONDS = 15      # transcript 切块窗口
MIN_DOC_SCORE = 0.60    # 新闻↔内容 匹配阈值；宁愿不推荐也不展示弱关联
MIN_CHUNK_SCORE = 0.20  # 块级时间戳匹配阈值（低于此说明定位不可靠，仍给链接但不带时间戳）

_TS_RE = re.compile(r'\[(\d{2}):(\d{2}):(\d{2})\]')
_aihot_cache = {}   # 按 hours 分桶：{hours: {"items", "expiry"}}

# 必读驱动建议入库
YT_DLP = str(Path(__file__).parent.parent / ".venv" / "bin" / "yt-dlp")
WHITELIST_HINTS = ("Y Combinator", "Lex Fridman", "a16z", "Tina", "DeepLearning", "Andrew Ng")
MIN_VIDEO_SEC = 900     # 候选视频至少 15 分钟（滤掉切片/快讯）
SEARCH_N = 4            # 每个搜索词取几条完整元数据（最多 2 个搜索词）
SUGGEST_MAX = 1         # 全页最多一个外部视频，避免“推荐本身成为噪音”
MIN_SUGGEST_SCORE = 75  # 低于此分不展示，避免“只是相关、不够互补”的视频
ATTENTION_MAX = 2       # 热议浮现最多 2 条：提醒用户，不把页面变回信息流

# 一手研究揭示“模型内部机制/隐性推理/可解释性/评估风控”的内容，虽然通常
# 不是新模型发布，但会直接影响 AI 产品经理接下来怎么设计评估与可信度机制。
# 这类内容必须有机会进入「1–3 个月行业趋势」，避免被泛商业/就业趋势挤掉。
MODEL_RESEARCH_SOURCES = (
    "anthropic", "openai", "deepmind", "google deepmind", "google research",
)
MODEL_INNER_WORKINGS_TERMS = (
    "global workspace", "j-space", "jacobian", "j-lens",
    "internal representation", "internal neural", "hidden reasoning",
    "latent reasoning", "workspace",
    "全局工作空间", "内部神经", "内部表征", "神经模式", "隐性推理",
    "隐藏目标", "潜意识", "私下察觉",
    "评估感知", "虚假数据", "思考但不说",
)
BUZZ_SOURCES = (
    "x：", "x:", "hacker news", "reddit", "v2ex", "微博", "即刻",
    "公众号", "techmeme", "product hunt",
)
BUZZ_TERMS = (
    "热议", "刷屏", "爆火", "全网", "都在讨论", "很多人在", "everyone is talking",
    "viral", "buzz", "debate", "controversy",
)


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
def _request_retry(method, url, *, tries=3, **kwargs):
    """带重试的请求：扛住 ChunkedEncodingError / 连接抖动等瞬时网络错误，
    别让一次网络抖动把整条每日任务整挂(今日必读就不更新了)。"""
    last = None
    for i in range(tries):
        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            last = e
            if i < tries - 1:
                time.sleep(1.5 * (i + 1))
    raise last


def fetch_aihot(hours=WINDOW_HOURS):
    """拉取过去 hours 小时的精选新闻，按 hours 分桶缓存 30 分钟。失败抛异常由调用方兜底。"""
    now = time.time()
    c = _aihot_cache.get(hours)
    if c and now < c["expiry"]:
        return c["items"]
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    resp = _request_retry(
        "GET", AIHOT_URL,
        params={"mode": "selected", "since": since, "take": 100 if hours > 48 else 50},
        headers={"User-Agent": AIHOT_UA},
        timeout=15,
    )
    items = resp.json().get("items", [])
    _aihot_cache[hours] = {"items": items, "expiry": now + AIHOT_TTL}
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


def _quote_text(item):
    """兼容 key_quotes 里是字符串或结构化 dict 的情况。"""
    if isinstance(item, dict):
        raw = (item.get("text") or item.get("quote") or item.get("content") or "")
    else:
        raw = str(item or "")
    # UI 会统一加中文引号，避免出现 ““xxx””。
    return raw.strip().strip("“”\"'").strip()


# 公共别名：金句归一化已是跨模块契约——app.quote_anchor 的锚点身份、
# make_quote_shots 的卡片文案都依赖同一语义。改动此函数需同步考虑三处。
quote_text = _quote_text


def _quote_speaker(record, quote_item=None):
    """从 quote/嘉宾/创作者里尽量取一个“谁说的”。"""
    if isinstance(quote_item, dict):
        speaker = (quote_item.get("speaker") or quote_item.get("author") or "").strip()
        if speaker:
            return speaker

    guests = record.get("guests") or record.get("guest") or []
    if isinstance(guests, str):
        for part in re.split(r"[、,，/|]", guests):
            part = part.strip()
            if part:
                return part
    elif isinstance(guests, list):
        for part in guests:
            if isinstance(part, dict):
                name = (part.get("name") or part.get("speaker") or "").strip()
            else:
                name = str(part or "").strip()
            if name:
                return name

    return (record.get("creator") or record.get("uploader") or "").strip()


def _pick_local_quote(record, news_vec=None):
    """从库内内容挑一句金句；有 news_vec 时尽量挑与当前热点最相关的一句。"""
    quotes = []
    for item in (record.get("key_quotes") or []):
        text = _quote_text(item)
        if text:
            quotes.append((text, item))
    if not quotes:
        return {}

    picked_text, picked_item = quotes[0]
    if news_vec is not None and np is not None and len(quotes) > 1:
        try:
            quote_vecs = np.asarray(
                embeddings.embed_texts([q[0] for q in quotes]),
                dtype=np.float32,
            )
            sims = _cos(quote_vecs, news_vec)
            idx = int(np.argmax(sims))
            picked_text, picked_item = quotes[idx]
        except Exception:
            # 金句只是展示增强，失败时不影响主流程。
            pass

    out = {"quote": picked_text}
    speaker = _quote_speaker(record, picked_item)
    if speaker:
        out["quote_speaker"] = speaker
    return out


def evidence_status(signal):
    if (signal or {}).get("links"):
        return "linked"
    if (signal or {}).get("suggest"):
        return "suggested"
    return "pending"


def enrich_cached_link_quotes(cache, records):
    """给旧缓存里的库内链接补上金句，避免必须等下一次后台生成才生效。"""
    cache = dict(cache or {})
    by_id = {str(r.get("id")): r for r in (records or []) if r.get("id")}

    def enrich_signal(signal):
        if not isinstance(signal, dict):
            return signal
        signal = dict(signal)
        enriched_links = []
        for link in (signal.get("links") or []):
            link = dict(link)
            rid = str(link.get("record_id") or "")
            if rid and not link.get("quote"):
                quote = _pick_local_quote(by_id.get(rid, {}))
                if quote:
                    link.update(quote)
            enriched_links.append(link)
        signal["links"] = enriched_links
        signal["evidence_status"] = evidence_status(signal)
        return signal

    if isinstance(cache.get("breaking"), dict):
        cache["breaking"] = enrich_signal(cache["breaking"])
    cache["signals"] = [enrich_signal(s) for s in (cache.get("signals") or [])]
    return cache


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


_SHORTLIST_PROMPT = """你是一个极度克制的 AI 产品资讯编辑。下面是 AI HOT 在过去
48 小时内发现的候选。先选出最多 {limit} 条值得进一步读取原文核验的候选。

用户上下文：
{user_context}

需要覆盖的栏目：
{slots}

规则：
- 优先一手信源、原始数据、可迁移方法论、能影响未来 1–3 个月产品判断的事实
- 特别优先官方研究中揭示模型内部机制、隐性推理、隐藏目标、可解释性、评估或风控方法的内容；
  这类内容默认属于「1–3 个月行业趋势」，即使它不是新模型发布
- 同时留意真正的顶级大新闻：正式发布的新模型、关键模态、价格或产品形态变化
- 排除营销软文、融资人事、工具清单、只有观点没有事实的内容
- 只做核验候选，不写结论；宁缺毋滥

只输出 JSON：{{"indices":[1,2]}}

候选：
{items}
"""


_EDITOR_PROMPT = """你是只服务一位 AI 产品经理的私人主编。你的任务不是提供更多新闻，
而是让用户在最少阅读量下判断“这件事值不值得继续看”。

用户上下文：
{user_context}

固定栏目：
{slots}

大新闻门槛：
{breaking_rules}

编辑规则：
1. 只能引用下面“已读取原文”的候选；原文没有支持的结论不能写。
2. breaking 最多一条，也可以为 null。必须达到全部大新闻门槛，并给出以下行动判断之一：
   {actions}
   解释模型内部机制/可解释性的新研究通常不是 breaking，除非同时伴随新模型、新产品或明确可用能力发布。
3. slots 的三个位置各最多一条，也可以为 null；绝不为了凑满而选弱内容。
4. 同一候选不能同时占两个位置，大新闻也不能与日常位重复。
5. summary 用 50–90 个汉字写完整一句，讲清“发生了什么 + 关键事实/数据”，不能截断。
6. why 用一句话说清它如何影响近期产品判断；不要复述 summary。
7. missing_angle 写这条短资讯仍缺的机制、案例或方法，供库内内容/视频补足。
8. video_queries 给两个英文 YouTube 搜索短语，围绕 missing_angle，不要机械翻译标题。
9. 官方发布可作为事实来源，但不能照搬宣传性结论。无法可靠判断就留空。
10. 如果已读取原文候选里出现“编辑优先级：模型内部机制与可解释性”，且原文支持，
    默认放入 industry_trend；不要让就业、融资、工具类趋势挤掉它。

只输出 JSON，结构必须是：
{{
  "breaking": null 或 {{
    "index": 1,
    "summary": "完整一句话。",
    "why": "为什么影响产品判断。",
    "action": "本周应该测试|值得持续关注|暂时知道即可",
    "missing_angle": "仍缺什么",
    "video_queries": ["query one", "query two"]
  }},
  "slots": {{
    "consumer_growth": null 或 {{
      "index": 2, "summary": "完整一句话。", "why": "为什么重要。",
      "missing_angle": "仍缺什么", "video_queries": ["query one", "query two"]
    }},
    "traffic_monetization": null,
    "industry_trend": null
  }}
}}

已读取原文候选：
{items}
"""


def _chat_json(prompt, temperature=0.2):
    """调用 DeepSeek（OpenAI 兼容）做重要性精排，强制 JSON 输出。"""
    key = os.getenv("OPENAI_API_KEY", "")
    base = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "deepseek-chat")
    resp = _request_retry(
        "POST", f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}],
              "response_format": {"type": "json_object"}, "temperature": temperature},
        timeout=60,
    )
    return json.loads(resp.json()["choices"][0]["message"]["content"])


def _one_sentence(text):
    """返回第一句完整文本；没有句末标点时补全，绝不按字符从中间切断。"""
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if not clean:
        return ""
    match = re.search(r"[。！？!?]", clean)
    if match:
        return clean[:match.end()]
    return clean.rstrip("，,；;：:") + "。"


def _item_text(item):
    return " ".join(str(item.get(k) or "") for k in (
        "title", "summary", "source", "url"
    )).lower()


def _priority_signal_kind(item):
    """识别必须优先进入行业趋势的一手模型机制研究。"""
    text = _item_text(item)
    source = str(item.get("source") or "").lower()
    url = str(item.get("url") or "").lower()
    has_research_source = any(term in source or term in url for term in MODEL_RESEARCH_SOURCES)
    has_inner_workings = any(term in text for term in MODEL_INNER_WORKINGS_TERMS)
    if has_research_source and has_inner_workings:
        return {
            "slot": "industry_trend",
            "label": "模型内部机制与可解释性",
            "reason": "一手研究揭示模型内部机制，可能改变 AI 产品评估、风控和可信度设计。",
        }
    return None


def _priority_rank(item):
    return 1 if _priority_signal_kind(item) else 0


def _buzz_signal_kind(item):
    """识别“很多人正在提，但系统未必选中”的浮现候选。"""
    text = _item_text(item)
    source = str(item.get("source") or "").lower()
    score = int(item.get("score") or 0)
    priority = _priority_signal_kind(item)
    if priority:
        return {
            "level": 3,
            "label": priority["label"],
            "reason": priority["reason"],
            "suggested_slot": priority["slot"],
            "why": "这类一手研究会影响接下来 AI 产品的评估、风控和可信度设计。",
        }
    source_buzz = any(term in source for term in BUZZ_SOURCES)
    text_buzz = any(term in text for term in BUZZ_TERMS)
    high_score = score >= 85
    if source_buzz and (score >= 65 or text_buzz):
        return {
            "level": 2,
            "label": "讨论度高",
            "reason": "这条来自高讨论度信源，且在 AI HOT 中热度较高。",
            "suggested_slot": "industry_trend",
            "why": "多人讨论本身不代表值得看，但值得让你决定是否升到首页判断。",
        }
    if high_score and text_buzz:
        return {
            "level": 1,
            "label": "全网热议",
            "reason": "标题或摘要显示它正在被集中讨论。",
            "suggested_slot": "industry_trend",
            "why": "热议内容可能影响近期产品判断，但需要你手动确认是否值得占首页位置。",
        }
    return None


def _make_attention_item(item, buzz):
    """把 AI HOT 项压缩成首页“热议浮现”提示。"""
    out = {
        "item_id": hashlib.sha1(
            (item.get("url") or item.get("title") or "").encode("utf-8")
        ).hexdigest()[:12],
        "id": item.get("id"),
        "title": item.get("title") or "",
        "url": item.get("url") or "",
        "source": item.get("source") or "",
        "summary": _one_sentence(item.get("summary")),
        "why": buzz.get("why") or "",
        "buzz_label": buzz.get("label") or "热议浮现",
        "buzz_reason": buzz.get("reason") or "",
        "buzz_level": buzz.get("level") or 1,
        "suggested_slot": buzz.get("suggested_slot") or "industry_trend",
        "score": int(item.get("score") or 0),
        "publishedAt": item.get("publishedAt") or item.get("published_at") or "",
        "verification_label": "待你确认",
    }
    return out


def _build_attention_candidates(news, selected_items, limit=ATTENTION_MAX):
    """把“热议但未入选”的内容浮出给用户确认。"""
    selected_keys = {
        _content_key(item.get("url") or "") or item.get("title")
        for item in selected_items if item
    }
    candidates = []
    for item in news:
        key = _content_key(item.get("url") or "") or item.get("title")
        if key in selected_keys:
            continue
        buzz = _buzz_signal_kind(item)
        if not buzz:
            continue
        candidates.append((_make_attention_item(item, buzz), buzz))
    candidates.sort(
        key=lambda pair: (
            pair[1].get("level") or 0,
            pair[0].get("score") or 0,
        ),
        reverse=True,
    )
    return [item for item, _buzz in candidates[:limit]]


def promote_attention_item(cache, item_id):
    """把一个浮现候选手动加入首页判断；供 Flask endpoint 调用。"""
    cache = dict(cache or {})
    attention = list(cache.get("attention") or [])
    signals = list(cache.get("signals") or [])
    picked = None
    rest = []
    for item in attention:
        if str(item.get("item_id")) == str(item_id):
            picked = item
        else:
            rest.append(item)
    if not picked:
        return cache, False

    signal = dict(picked)
    signal.update({
        "slot": picked.get("suggested_slot") or "industry_trend",
        "slot_label": "热议补充",
        "is_breaking": False,
        "verification_label": "你手动加入",
        "links": [],
        "manual_promoted": True,
    })
    signal["evidence_status"] = evidence_status(signal)
    if not any(s.get("item_id") == signal.get("item_id") for s in signals):
        signals.append(signal)
    cache["signals"] = signals
    cache["attention"] = rest
    return _write_signal_cache(cache), True


def dismiss_attention_item(cache, item_id):
    """忽略一个浮现候选。"""
    cache = dict(cache or {})
    before = len(cache.get("attention") or [])
    cache["attention"] = [
        item for item in (cache.get("attention") or [])
        if str(item.get("item_id")) != str(item_id)
    ]
    changed = len(cache["attention"]) != before
    if changed:
        return _write_signal_cache(cache), True
    return cache, False


def _pool_candidates(news):
    """保留高价值候选，同时让 category 只做轻量先验而不是最终判断。"""
    return sorted(
        news,
        key=lambda n: (
            _priority_rank(n),
            1 if n.get("category") == "tip" else 0,
            n.get("score") or 0,
        ),
        reverse=True,
    )[:PRESELECT]


def _candidate_lines(pool, include_original=False):
    lines = []
    for i, item in enumerate(pool, 1):
        summary = re.sub(r"\s+", " ", item.get("summary") or "").strip()[:500]
        base = (
            f"{i}. [{item.get('source') or '未知信源'}|"
            f"{item.get('publishedAt') or item.get('published_at') or '未知时间'}] "
            f"{item.get('title') or ''}\n"
            f"AI HOT 摘要：{summary}"
        )
        priority = _priority_signal_kind(item)
        if priority:
            base += (
                f"\n编辑优先级：{priority['label']}。{priority['reason']}"
            )
        if include_original:
            original = item.get("_original") or {}
            base += (
                f"\n原始链接：{item.get('url') or ''}"
                f"\n原文摘录：{(original.get('text') or '')[:3500]}"
            )
        lines.append(base)
    return "\n\n".join(lines)


def _shortlist_candidates(news, profile):
    """第一阶段只决定哪些原文值得读取，控制网络开销与上下文长度。"""
    pool = _pool_candidates(news)
    if not pool:
        return []
    slots = json.dumps(profile.get("daily_slots") or [], ensure_ascii=False)
    data = _chat_json(_SHORTLIST_PROMPT.format(
        limit=SHORTLIST_N,
        user_context=prompt_context(profile),
        slots=slots,
        items=_candidate_lines(pool),
    ), temperature=0.1)
    picked = []
    seen = set()
    for raw in data.get("indices") or []:
        try:
            idx = int(raw)
        except (TypeError, ValueError):
            continue
        if 1 <= idx <= len(pool) and idx not in seen:
            seen.add(idx)
            picked.append(dict(pool[idx - 1]))
        if len(picked) >= SHORTLIST_N:
            break
    return picked


def _read_candidate_originals(candidates):
    """并发核对原文；不可读的候选不会进入最终编辑。"""
    readable = []
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(candidates)))) as executor:
        futures = {
            executor.submit(read_original, item.get("url") or ""): item
            for item in candidates
        }
        for future in as_completed(futures):
            item = futures[future]
            try:
                original = future.result()
            except Exception:
                original = {"text": "", "method": "failed", "readable": False}
            if original.get("readable"):
                enriched = dict(item)
                enriched["_original"] = original
                readable.append(enriched)
    # 并发完成顺序不稳定，恢复 shortlist 顺序。
    order = {item.get("url"): i for i, item in enumerate(candidates)}
    readable.sort(key=lambda item: order.get(item.get("url"), 999))
    return readable


def _normalize_editor_pick(raw, candidates, *, slot="", slot_label="", breaking=False,
                           actions=None):
    if not isinstance(raw, dict):
        return None
    try:
        idx = int(raw.get("index"))
    except (TypeError, ValueError):
        return None
    if not 1 <= idx <= len(candidates):
        return None
    item = dict(candidates[idx - 1])
    item.pop("_original", None)
    item["item_id"] = hashlib.sha1(
        (item.get("url") or item.get("title") or "").encode("utf-8")
    ).hexdigest()[:12]
    item["summary"] = _one_sentence(raw.get("summary") or item.get("summary"))
    item["why"] = _one_sentence(raw.get("why"))
    item["missing_angle"] = str(raw.get("missing_angle") or "").strip()
    queries = raw.get("video_queries") or []
    item["video_queries"] = [
        re.sub(r"\s+", " ", str(query)).strip()
        for query in queries if str(query).strip()
    ][:2] if isinstance(queries, list) else []
    item["verification_label"] = "已核对原文"
    item["slot"] = slot
    item["slot_label"] = slot_label
    item["is_breaking"] = breaking
    if breaking:
        action = str(raw.get("action") or "").strip()
        if action not in (actions or []):
            return None
        item["action"] = action
    return item


def _build_priority_research_signal(item, slot_label):
    """兜底生成一条行业趋势信号：只用于已读原文的一手模型机制研究。"""
    signal = dict(item)
    signal.pop("_original", None)
    signal["item_id"] = hashlib.sha1(
        (signal.get("url") or signal.get("title") or "").encode("utf-8")
    ).hexdigest()[:12]
    signal["summary"] = _one_sentence(signal.get("summary"))
    signal["why"] = (
        "它把 AI 产品评估从只看输出推进到观察隐性推理，"
        "对可信度、风控和评测设计都有近期迁移价值。"
    )
    signal["missing_angle"] = "缺少可迁移到产品评估与风控流程的具体方法"
    signal["video_queries"] = [
        "language model interpretability global workspace hidden reasoning",
        "AI model internal representations monitoring safety evaluation",
    ]
    signal["verification_label"] = "已核对原文"
    signal["slot"] = "industry_trend"
    signal["slot_label"] = slot_label or "1–3 个月行业趋势"
    signal["is_breaking"] = False
    signal["priority_label"] = "模型内部机制与可解释性"
    return signal


def _ensure_priority_research_signal(signals, candidates, used_indices, slots):
    """确保一手模型机制研究不被普通趋势挤掉。"""
    priority_idx = None
    for i, item in enumerate(candidates, 1):
        if i in used_indices:
            continue
        priority = _priority_signal_kind(item)
        if priority and priority.get("slot") == "industry_trend":
            priority_idx = i
            break
    if priority_idx is None:
        return signals

    if any(_priority_signal_kind(signal) for signal in signals):
        return signals

    slot_label = next(
        (slot.get("label") for slot in slots if slot.get("key") == "industry_trend"),
        "1–3 个月行业趋势",
    )
    priority_signal = _build_priority_research_signal(
        candidates[priority_idx - 1], slot_label)

    replaced = False
    out = []
    for signal in signals:
        if signal.get("slot") == "industry_trend":
            if not replaced:
                out.append(priority_signal)
                replaced = True
            continue
        out.append(signal)
    if not replaced:
        out.append(priority_signal)
    used_indices.add(priority_idx)
    return out


def _select_editorial(news, profile):
    """两阶段编辑：先选核验候选，再基于原文生成大新闻与三个固定栏目。"""
    shortlist = _shortlist_candidates(news, profile)
    candidates = _read_candidate_originals(shortlist)
    if not candidates:
        return {"breaking": None, "signals": []}

    slots = profile.get("daily_slots") or []
    breaking_cfg = profile.get("breaking_news") or {}
    actions = breaking_cfg.get("actions") or []
    data = _chat_json(_EDITOR_PROMPT.format(
        user_context=prompt_context(profile),
        slots=json.dumps(slots, ensure_ascii=False),
        breaking_rules=json.dumps(
            breaking_cfg.get("requirements") or [], ensure_ascii=False),
        actions=" / ".join(actions),
        items=_candidate_lines(candidates, include_original=True),
    ), temperature=0.1)

    used_indices = set()
    raw_breaking = data.get("breaking")
    try:
        breaking_idx = int(raw_breaking.get("index")) if isinstance(raw_breaking, dict) else None
    except (TypeError, ValueError):
        breaking_idx = None
    breaking = _normalize_editor_pick(
        raw_breaking, candidates, breaking=True, actions=actions)
    # 模型机制/可解释性研究是高优先级行业趋势，但不是“大新闻横幅”。
    # 避免模型因为“重要”就把它误升为 breaking。
    if breaking and _priority_signal_kind(breaking):
        breaking = None
    elif breaking and breaking_idx:
        used_indices.add(breaking_idx)

    signals = []
    raw_slots = data.get("slots") if isinstance(data.get("slots"), dict) else {}
    for slot in slots:
        key = slot.get("key") or ""
        raw = raw_slots.get(key)
        try:
            idx = int(raw.get("index")) if isinstance(raw, dict) else None
        except (TypeError, ValueError):
            idx = None
        if idx in used_indices:
            continue
        normalized = _normalize_editor_pick(
            raw,
            candidates,
            slot=key,
            slot_label=slot.get("label") or key,
            actions=actions,
        )
        if normalized:
            used_indices.add(idx)
            signals.append(normalized)
    signals = _ensure_priority_research_signal(signals, candidates, used_indices, slots)
    return {"breaking": breaking, "signals": signals}


def _existing_video_ids():
    """已入库的视频 id 集合（去重用，避免重复建议）"""
    ids = set()
    if ARCHIVE_ROOT.exists():
        for mp in ARCHIVE_ROOT.glob("*/metadata.json"):
            try:
                m = json.loads(mp.read_text(encoding="utf-8"))
                if m.get("id"):
                    ids.add(str(m["id"]))
            except Exception:
                pass
    return ids


def _yt_search(query, n=SEARCH_N):
    """按 Agent-Reach 的 YouTube 路由调用 yt-dlp，返回带描述的候选元数据。"""
    probe = probe_command(YT_DLP, ["--version"], package="yt-dlp")
    if not probe.ok:
        print(f"[WARN] YouTube 搜索不可用（{probe.status}）：{probe.hint or probe.output}")
        return []

    try:
        result = subprocess.run(
            [
                YT_DLP,
                "--dump-json",
                "--skip-download",
                "--no-warnings",
                "--no-playlist",
                f"ytsearch{n}:{query}",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"[WARN] YouTube 搜索失败（{query}）：{e}")
        return []

    if result.returncode != 0:
        detail = (result.stderr or "").strip()[-300:]
        print(f"[WARN] YouTube 搜索失败（{query}）：{detail}")
        return []

    res = []
    for line in result.stdout.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        video_id = str(item.get("id") or "")
        if not video_id:
            continue
        res.append({
            "title": item.get("title") or "",
            "id": video_id,
            "duration": int(item.get("duration") or 0),
            "channel": item.get("channel") or item.get("uploader") or "",
            "description": re.sub(
                r"\s+", " ", item.get("description") or "").strip(),
            "upload_date": str(item.get("upload_date") or ""),
            "view_count": int(item.get("view_count") or 0),
            "url": item.get("webpage_url")
                   or f"https://www.youtube.com/watch?v={video_id}",
        })
    return res


_VIDEO_RANK_PROMPT = """你是「AI 产品人」的延伸阅读编辑。

热点标题：{title}
热点总结：{summary}
为什么重要：{why}
热点还缺少：{missing_angle}

从候选视频里最多选择 1 个，目标不是找“标题相似”的视频，而是找真正补足热点的信息：
- 优先补充背景、机制、真实案例、方法或行动框架
- 视频主题必须与热点核心问题直接相关，不能只沾一个关键词
- 信源可信、内容有深度；15 分钟以上只是入围条件，不因更长就加分
- 旧视频可以入选，但必须仍能解释当前热点
- 没有明显互补价值就返回 null，宁缺毋滥

给出 0–100 的 match_score；只有你认为达到 75 分才选择。
complement_reason 用 35–70 个汉字说清“热点讲了什么，视频又补了什么”，不能写泛泛的“帮助深入理解”。
必须写成「热点……；视频……。」这一句式，只能有最后一个句号，确保两部分都出现。

候选：
{candidates}

只输出 JSON：
{{"pick":{{"index":候选序号,"match_score":0到100,"complement_reason":"具体补足点"}}}}
或 {{"pick":null}}
"""


def _candidate_prompt(cands):
    """把候选压缩成可审阅文本，避免把整段 YouTube 描述塞给模型。"""
    lines = []
    for i, c in enumerate(cands, 1):
        date = c.get("upload_date") or "未知日期"
        desc = (c.get("description") or "")[:360]
        lines.append(
            f"{i}. {c.get('title', '')}｜{c.get('channel', '')}｜"
            f"{round((c.get('duration') or 0) / 60)}分钟｜{date}｜{desc}"
        )
    return "\n".join(lines)


def _format_publish_date(raw):
    raw = str(raw or "")
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return ""


def suggest_video(signal, used_ids):
    """为热点找一个真正互补的 YouTube 深度视频；低于阈值就不展示。"""
    queries = signal.get("video_queries") or []
    if not isinstance(queries, list):
        queries = []
    queries = [
        re.sub(r"\s+", " ", str(q)).strip()
        for q in queries
        if str(q).strip()
    ][:2]
    if not queries:
        queries = [signal.get("title") or ""]

    by_id = {}
    for query in queries:
        for candidate in _yt_search(query):
            video_id = candidate.get("id")
            if (
                video_id
                and video_id not in used_ids
                and candidate.get("duration", 0) >= MIN_VIDEO_SEC
            ):
                by_id.setdefault(video_id, candidate)
    cands = list(by_id.values())
    if not cands:
        return None

    def is_wl(c):
        return any(h.lower() in (c["channel"] or "").lower() for h in WHITELIST_HINTS)

    # 白名单只作为同质候选的轻量先验，最终仍由“互补性”决定。
    cands.sort(key=lambda c: (
        0 if is_wl(c) else 1,
        -(c.get("view_count") or 0),
    ))
    cands = cands[:8]

    data = _chat_json(_VIDEO_RANK_PROMPT.format(
        title=signal.get("title") or "",
        summary=signal.get("summary") or "",
        why=signal.get("why") or "",
        missing_angle=signal.get("missing_angle") or "需要更完整的背景或实践解释",
        candidates=_candidate_prompt(cands),
    ), temperature=0.1)
    pick = data.get("pick")
    if not isinstance(pick, dict):
        return None
    try:
        index = int(pick.get("index"))
        score = int(float(pick.get("match_score") or 0))
    except (TypeError, ValueError):
        return None
    if not 1 <= index <= len(cands) or score < MIN_SUGGEST_SCORE:
        return None

    c = dict(cands[index - 1])
    c["from_whitelist"] = is_wl(c)
    c["dur_min"] = round(c["duration"] / 60)
    c["published"] = _format_publish_date(c.get("upload_date"))
    c["match_score"] = min(score, 100)
    c["complement_reason"] = _one_sentence(
        pick.get("complement_reason") or "")
    return c


_ANSWER_PROMPT = """你是面向「AI 产品人」的资讯助手，读者是 AI 产品经理 / AI 创业者。用户问：{query}

只基于下面材料综合回答，别编造材料外的事实。要求：简洁、有判断、像跟同行聊天。
若是"本周大事 / 有哪些 / 趋势"类，按"对 AI 产品人的价值"从高到低列 2-4 条，每条一句点透 + 一句为什么对 AI 产品人重要，结尾给一句总判断。

【选材标准 · 按"对 AI 产品人的价值"取舍，不是按热度分】
- 优先：重大模型/能力发布（决定能做出什么产品）、AI 产品打法/商业模式、新范式或新概念、改变产品人工作方式的大事；偏 产品落地 / PMF / 用户体验 的优先
- 降权或不选：纯行业格局 / 政策法规 / 国标补贴 / 人事融资八卦、纯底层基础设施、纯安全红队、纯学术论文细节、教程、小工具、营销
- 宁缺毋滥：材料里没有够格的就直说"这周没看到对产品人够格的大事"，别为凑数硬列

只输出 JSON：{{"answer":"（简体中文，markdown：可用 - 列表、**加粗**）"}}

【你的深度库（已策展）】
{lib}

【本周全网 AI 资讯】
{news}
"""


def _top_news(news, n):
    return sorted(news, key=lambda x: (1 if x.get("category") == "tip" else 0,
                                       -(x.get("score") or 0)))[:n]


def answer_query(query, lib_results, days=7):
    """问答式搜索：综合「库结果 + AI HOT 近 days 天」，DeepSeek 生成一段回答（markdown）。"""
    try:
        news = fetch_aihot(hours=days * 24)
    except Exception:
        news = []
    lib = "\n".join(f"[库{i+1}] {r.get('title','')}｜{(r.get('summary') or '')[:120]}"
                    for i, r in enumerate(lib_results[:5])) or "（无）"
    nl = "\n".join(f"[资讯{i+1}] {n.get('title','')}｜{(n.get('summary') or '')[:80]}"
                   for i, n in enumerate(_top_news(news, 20))) or "（无）"
    data = _chat_json(_ANSWER_PROMPT.format(query=query, lib=lib, news=nl), temperature=0.3)
    return (data.get("answer") or "").strip()


def _parse_generated_at(value):
    try:
        return datetime.strptime(str(value or ""), "%Y-%m-%d %H:%M")
    except ValueError:
        return None


def _delivery_time(profile):
    delivery = (profile or {}).get("delivery") or {}
    hour = int(delivery.get("hour", 8) or 8)
    minute = int(delivery.get("minute", 30) or 30)
    return max(0, min(hour, 23)), max(0, min(minute, 59))


def _next_delivery_after(dt, profile):
    hour, minute = _delivery_time(profile)
    candidate = dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= dt:
        candidate = candidate + timedelta(days=1)
    return candidate


def signal_freshness(payload, now_ts=None, profile=None):
    profile = profile or load_profile()
    generated = _parse_generated_at((payload or {}).get("generated_at"))
    if not generated:
        return {
            "status": "invalid",
            "is_expired": True,
            "age_hours": None,
            "expires_at": "",
            "label": "读取失败",
            "message": "今日判断缓存缺少有效生成时间。",
        }
    now_dt = datetime.fromtimestamp(now_ts or time.time())
    expires = _next_delivery_after(generated, profile)
    age_hours = max(0, round((now_dt - generated).total_seconds() / 3600, 1))
    expired = now_dt >= expires
    return {
        "status": "expired" if expired else "fresh",
        "is_expired": expired,
        "age_hours": age_hours,
        "expires_at": expires.strftime("%Y-%m-%d %H:%M"),
        "label": "已过期" if expired else "新鲜",
        "message": (
            f"上次生成于 {generated.strftime('%Y-%m-%d %H:%M')}，已超过今日更新窗口。当前内容仅供回看，不代表今日判断。"
            if expired else
            f"今日判断生成于 {generated.strftime('%Y-%m-%d %H:%M')}，有效到 {expires.strftime('%Y-%m-%d %H:%M')}。"
        ),
    }


def with_signal_freshness(payload, now_ts=None, profile=None):
    out = dict(payload or {})
    out.setdefault("signals", [])
    out.setdefault("attention", [])
    out["freshness"] = signal_freshness(out, now_ts=now_ts, profile=profile)
    return out


def missing_signal_state(profile=None):
    window_hours = int(((profile or load_profile()).get("editorial_rules") or {}).get("window_hours") or WINDOW_HOURS)
    return {
        "window_hours": window_hours,
        "generated_at": "",
        "breaking": None,
        "signals": [],
        "attention": [],
        "freshness": {
            "status": "missing",
            "is_expired": True,
            "age_hours": None,
            "expires_at": "",
            "label": "未生成",
            "message": "还没有生成今日判断。运行 ./run.sh signals 后再查看。",
        },
    }


def _invalid_signal_state(message="今日判断读取失败，首页其他内容仍可查看。"):
    state = missing_signal_state()
    state["freshness"] = {
        "status": "invalid",
        "is_expired": True,
        "age_hours": None,
        "expires_at": "",
        "label": "读取失败",
        "message": message,
    }
    return state


def _has_malformed_signal_cache_fields(payload):
    for field in ("signals", "attention"):
        if field in payload and not isinstance(payload.get(field), list):
            return True
    if (
        "breaking" in payload
        and payload.get("breaking") is not None
        and not isinstance(payload.get("breaking"), dict)
    ):
        return True
    return False


def read_signal_cache():
    """页面侧：只读完整缓存，永不触发生成（绝不阻塞网页请求）。"""
    if not SIGNAL_CACHE.exists():
        return None
    try:
        payload = json.loads(SIGNAL_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return _invalid_signal_state()
    if not isinstance(payload, dict):
        return _invalid_signal_state("今日判断缓存格式异常，首页其他内容仍可查看。")
    if _has_malformed_signal_cache_fields(payload):
        return _invalid_signal_state("今日判断缓存字段格式异常，首页其他内容仍可查看。")
    try:
        return with_signal_freshness(payload)
    except (TypeError, ValueError):
        return _invalid_signal_state("今日判断缓存格式异常，首页其他内容仍可查看。")


def read_signals():
    """兼容旧调用：只返回三个日常判断位中实际入选的内容。"""
    cache = read_signal_cache()
    return None if cache is None else cache.get("signals", [])


def _write_signal_cache(payload):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_CACHE.write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def _prepare_library(records):
    arch_by_key = _archive_by_key()
    index = embeddings.load_index()
    matrix, ids, by_id = None, [], {}
    if np is not None and index and records:
        by_id = {record.get("id"): record for record in records}
        vectors = []
        for rid, item in index.items():
            if rid in by_id and item.get("vector"):
                ids.append(rid)
                vectors.append(item["vector"])
        if vectors:
            matrix = np.asarray(vectors, dtype=np.float32)
            matrix = matrix / (
                np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-8)
    return arch_by_key, matrix, ids, by_id


def _match_library(signal, library, used_record_ids):
    """库内优先找一个高质量补充；弱匹配直接为空。"""
    arch_by_key, matrix, ids, by_id = library
    if matrix is None:
        return []
    try:
        vector = np.asarray(embeddings.embed_query(
            ((signal.get("title") or "") + "。" +
             (signal.get("summary") or "")).strip()), dtype=np.float32)
        similarities = matrix @ (vector / (np.linalg.norm(vector) + 1e-8))
        for j in np.argsort(-similarities):
            score = float(similarities[j])
            if score < MIN_DOC_SCORE:
                break
            record = by_id[ids[j]]
            rid = record.get("id")
            if rid in used_record_ids:
                continue
            archive = arch_by_key.get(_content_key(record.get("link") or ""))
            if not archive:
                continue
            location = _locate_timestamp(archive, vector)
            if location is None:
                continue
            sec, _snippet, chunk_score = location
            url = record.get("link") or ""
            show_ts = _supports_ts(url) and chunk_score >= MIN_CHUNK_SCORE
            used_record_ids.add(rid)
            link = {
                "record_id": rid,
                "title": record.get("title", ""),
                "platform": record.get("platform", ""),
                "deeplink": _deeplink(url, sec) if show_ts else url,
                "ts": _fmt_ts(sec) if show_ts else "",
                # 分数只用于门槛判断，不进入 UI。
                "match": round(score * 100),
            }
            link.update(_pick_local_quote(record, vector))
            return [link]
    except Exception as exc:
        print(f"[WARN] 库内匹配失败（{signal.get('title', '')[:30]}）：{exc}")
    return []


def generate_signals(records):
    """后台生成（AI HOT + 原文核验 + 编辑判断 + 深度补充），写入缓存。
    由 `run.sh signals` / 每日定时调用，不在网页请求里跑。"""
    now = time.time()
    profile = load_profile()
    news = fetch_aihot(hours=int(
        (profile.get("editorial_rules") or {}).get("window_hours")
        or WINDOW_HOURS))
    editorial = _select_editorial(news, profile) if news else {
        "breaking": None, "signals": []}
    breaking = editorial.get("breaking")
    signals = editorial.get("signals") or []
    selected_items = ([breaking] if breaking else []) + signals
    attention = _build_attention_candidates(news, selected_items)

    # 库内优先；同一篇库内内容不会在多个判断位重复出现。
    library = _prepare_library(records)
    used_records = set()
    all_picks = selected_items
    for signal in all_picks:
        signal["links"] = _match_library(signal, library, used_records)

    # 只有库内补充不够时才搜索 YouTube，并且整页最多一条。
    existing = _existing_video_ids()
    suggestions = 0
    for signal in all_picks:
        if signal["links"] or suggestions >= SUGGEST_MAX:
            continue
        try:
            suggestion = suggest_video(signal, existing)
        except Exception as exc:
            print(
                f"[WARN] 延伸视频推荐失败（{signal.get('title', '')[:30]}）：{exc}")
            suggestion = None
        if suggestion:
            existing.add(suggestion["id"])
            signal["suggest"] = suggestion
            suggestions += 1

    payload = {
        "expiry": now + SIGNAL_TTL,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "window_hours": int(
            (profile.get("editorial_rules") or {}).get("window_hours")
            or WINDOW_HOURS),
        "breaking": breaking,
        "signals": signals,
        "attention": attention,
        "slots_total": len(profile.get("daily_slots") or []),
        "behavior": behavior_summary(profile),
    }
    return _write_signal_cache(payload)


if __name__ == "__main__":
    # 后台生成今日判断（run.sh signals / 每日定时调用）
    from app import load_archive_records
    print("[signals] 拉 AI HOT + 核对原文 + 编辑判断 + 深度补充...")
    cache = generate_signals(load_archive_records())
    count = len(cache.get("signals") or []) + (
        1 if cache.get("breaking") else 0)
    print(f"[signals] 生成 {count} 条判断 → {SIGNAL_CACHE}")
