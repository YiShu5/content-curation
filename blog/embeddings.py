"""
语义搜索 - 基于智谱 embedding-3 的内容向量索引

- 索引键: feishu_record_id（与博客卡片/详情页同一主键）
- 存储: blog/data/embeddings.json，每项 {record_id, text_hash, model, dim, vector}
- 检索: numpy 暴力余弦相似度（内容规模小，无需向量数据库）
- 增量: 文本 sha1 未变且模型/维度一致则复用旧向量，避免重复调用 API
"""

import hashlib
import json
import os
import time
from pathlib import Path

import requests

try:
    import numpy as np
except ImportError:  # 构建/检索时才真正需要，导入失败给出清晰提示
    np = None

# 加载 config/.env（独立运行 CLI 时也能拿到密钥）
_env_path = Path(__file__).parent.parent / "config" / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass

from config import Config

ZHIPU_EMBED_URL = "https://open.bigmodel.cn/api/paas/v4/embeddings"
INDEX_PATH = Path(__file__).parent / "data" / "embeddings.json"
BATCH_SIZE = 32
MAX_DOC_CHARS = 3000  # embedding-3 上限 8192 token，中文留足余量


class EmbeddingError(RuntimeError):
    """语义搜索相关错误的基类，供路由层统一捕获转成友好提示"""


class EmbeddingConfigError(EmbeddingError):
    """配置/依赖问题：缺 ZHIPU_API_KEY、缺 numpy 等（用户需先配置）"""


class EmbeddingIndexMissing(EmbeddingError):
    """向量索引不存在或为空（用户需先运行 ./run.sh embed）"""


class EmbeddingAPIError(EmbeddingError):
    """智谱 API 调用失败（网络/鉴权/参数/响应结构异常）"""


# ── 文本组装 ────────────────────────────────────────────────────────────────
def compose_document(record):
    """把一条（已 enrich 的）记录拼成高信号 embedding 文本。
    缺失字段安全跳过——对仅有飞书数据的记录也能工作。"""
    parts = []
    title = record.get("title") or record.get("original_title") or ""
    if title:
        parts.append(title)

    meta_bits = []
    if record.get("topic"):
        meta_bits.append(f"话题: {record['topic']}")
    if record.get("creator"):
        meta_bits.append(f"创作者: {record['creator']}")
    if record.get("guests"):
        meta_bits.append(f"嘉宾: {record['guests']}")
    if meta_bits:
        parts.append(" ".join(meta_bits))

    if record.get("why_watch"):
        parts.append(record["why_watch"])

    core_ideas = record.get("core_ideas") or []
    if core_ideas:
        parts.append("核心观点: " + "；".join(core_ideas))

    key_quotes = record.get("key_quotes") or []
    if key_quotes:
        parts.append("金句: " + " ".join(key_quotes))

    if record.get("key_insights"):
        parts.append(record["key_insights"])

    # summary 来自飞书「深度摘要」，也可能被本地 deep_summary 覆盖为 summary_md
    summary = record.get("summary_md") or record.get("summary") or ""
    if summary:
        parts.append(summary)

    text = "\n".join(parts).strip()
    return text[:MAX_DOC_CHARS]


def _text_hash(text, model, dim):
    h = hashlib.sha1(f"{model}|{dim}|{text}".encode("utf-8"))
    return h.hexdigest()


# ── 智谱 API ────────────────────────────────────────────────────────────────
def embed_texts(texts):
    """批量向量化。返回与 texts 等长的 list[list[float]]。"""
    if not Config.ZHIPU_API_KEY:
        raise EmbeddingConfigError("未配置 ZHIPU_API_KEY，请在 config/.env 中填入智谱密钥")
    if not texts:
        return []

    headers = {
        "Authorization": f"Bearer {Config.ZHIPU_API_KEY}",
        "Content-Type": "application/json",
    }
    vectors = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]
        payload = {
            "model": Config.EMBED_MODEL,
            "input": batch,
            "dimensions": Config.EMBED_DIM,
        }
        for attempt in range(3):
            try:
                resp = requests.post(ZHIPU_EMBED_URL, headers=headers,
                                     json=payload, timeout=30)
                try:
                    data = resp.json()
                except ValueError:
                    raise EmbeddingAPIError(
                        f"智谱 API 返回非 JSON (HTTP {resp.status_code}): {resp.text[:200]}")
                # 鉴权/参数等错误：不重试，直接抛清晰信息
                if resp.status_code != 200 or data.get("error"):
                    raise EmbeddingAPIError(f"智谱 API 错误 (HTTP {resp.status_code}): {data}")
                # 校验响应结构，避免 KeyError 掩盖真实问题
                items = data.get("data")
                if not isinstance(items, list) or not items:
                    raise EmbeddingAPIError(f"智谱 API 响应结构异常: {str(data)[:200]}")
                # 按 index 排序，保证与输入顺序一致
                items = sorted(items, key=lambda x: x.get("index", 0))
                vectors.extend(item["embedding"] for item in items)
                break
            except EmbeddingError:
                raise  # 配置/API 错误不重试
            except Exception as e:  # 网络异常等，退避重试
                if attempt == 2:
                    raise EmbeddingAPIError(f"智谱 API 请求失败，已重试 3 次: {e}") from e
                time.sleep(1.5 * (attempt + 1))
    return vectors


def embed_query(query):
    return embed_texts([query])[0]


# ── 索引读写 ────────────────────────────────────────────────────────────────
def load_index():
    if not INDEX_PATH.exists():
        return {}
    try:
        raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        return {item["record_id"]: item for item in raw.get("items", [])}
    except Exception:
        return {}


def save_index(index):
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": Config.EMBED_MODEL,
        "dim": Config.EMBED_DIM,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "items": list(index.values()),
    }
    INDEX_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


# ── 构建 / 检索 ──────────────────────────────────────────────────────────────
def build_index(records):
    """对每条记录组装文本并向量化，增量复用未变的向量。返回统计 dict。"""
    old = load_index()
    new_index = {}
    to_embed = []          # [(record_id, text, text_hash)]
    built = reused = skipped = 0

    for r in records:
        rid = r.get("id")
        if not rid:
            skipped += 1
            continue
        text = compose_document(r)
        if not text:
            skipped += 1
            continue
        th = _text_hash(text, Config.EMBED_MODEL, Config.EMBED_DIM)
        prev = old.get(rid)
        if prev and prev.get("text_hash") == th and prev.get("vector"):
            new_index[rid] = prev
            reused += 1
        else:
            to_embed.append((rid, text, th))

    if to_embed:
        vectors = embed_texts([t for _, t, _ in to_embed])
        for (rid, _, th), vec in zip(to_embed, vectors):
            new_index[rid] = {
                "record_id": rid,
                "text_hash": th,
                "model": Config.EMBED_MODEL,
                "dim": Config.EMBED_DIM,
                "vector": vec,
            }
            built += 1

    save_index(new_index)
    return {"built": built, "reused": reused, "skipped": skipped,
            "total": len(new_index)}


def search(query, records, top_k=24, min_score=0.0):
    """对 records 做语义检索。返回 [(record, score), ...] 按相似度降序。
    索引为空或依赖缺失时抛 EmbeddingError，供路由层提示。"""
    if np is None:
        raise EmbeddingConfigError("缺少 numpy 依赖，请运行: pip install numpy")
    index = load_index()
    if not index:
        raise EmbeddingIndexMissing("向量索引为空，请先运行: ./run.sh embed")

    by_id = {r.get("id"): r for r in records}
    ids, mat = [], []
    for rid, item in index.items():
        if rid in by_id and item.get("vector"):
            ids.append(rid)
            mat.append(item["vector"])
    if not ids:
        return []

    mat = np.asarray(mat, dtype=np.float32)
    qv = np.asarray(embed_query(query), dtype=np.float32)

    # 余弦相似度
    mat_norm = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-8)
    qv_norm = qv / (np.linalg.norm(qv) + 1e-8)
    sims = mat_norm @ qv_norm

    order = np.argsort(-sims)[:top_k]
    results = []
    for i in order:
        score = float(sims[i])
        if score < min_score:
            continue
        results.append((by_id[ids[i]], score))
    return results


def related(record_id, records, top_k=3, min_score=0.30):
    """基于预建向量索引，返回与指定内容最相似的若干条 [(record, score), ...]。
    只用索引里已有的向量做余弦，不调用 API（零成本）。按标题去重，跳过同一视频的重复记录。"""
    if np is None:
        return []
    index = load_index()
    target = (index.get(record_id) or {}).get("vector")
    if not target:
        return []
    by_id = {r.get("id"): r for r in records}
    cur_title = (by_id.get(record_id) or {}).get("title", "")

    tv = np.asarray(target, dtype=np.float32)
    tv = tv / (np.linalg.norm(tv) + 1e-8)

    scored = []
    for rid, item in index.items():
        if rid == record_id or rid not in by_id:
            continue
        vec = item.get("vector")
        if not vec:
            continue
        vv = np.asarray(vec, dtype=np.float32)
        vv = vv / (np.linalg.norm(vv) + 1e-8)
        scored.append((by_id[rid], float(tv @ vv)))
    scored.sort(key=lambda x: -x[1])

    out, seen = [], {cur_title}
    for rec, score in scored:
        if score < min_score:
            break
        title = rec.get("title", "")
        if title in seen:
            continue
        seen.add(title)
        out.append((rec, score))
        if len(out) >= top_k:
            break
    return out


# ── CLI: python embeddings.py build ─────────────────────────────────────────
def _cli_build():
    # 惰性导入 app，避免 app <-> embeddings 模块级循环
    from app import fetch_records, _enrich_from_local
    print("[embed] 拉取飞书记录...")
    records = fetch_records()
    for r in records:
        _enrich_from_local(r)
    print(f"[embed] 共 {len(records)} 条记录，开始构建向量索引...")
    stats = build_index(records)
    print(f"[embed] 完成: 新建 {stats['built']}，复用 {stats['reused']}，"
          f"跳过 {stats['skipped']}，索引总数 {stats['total']}")
    print(f"[embed] 索引文件: {INDEX_PATH}")


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        _cli_build()
    else:
        print(f"未知命令: {cmd}（可用: build）")
        sys.exit(1)
