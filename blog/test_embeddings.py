"""
embeddings.py 的离线逻辑测试（mock 智谱 API，不需要 key / 网络 / numpy 之外的依赖）。

验证：
  1. compose_document 字段组装 + 截断
  2. build_index 增量复用（文本未变则不重复调用 API）
  3. search 余弦排序正确（相关内容排前）
  4. search 跳过索引中已不存在于 records 的脏 record_id

运行: blog/.venv/bin/python blog/test_embeddings.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import embeddings as em


# ── 确定性假向量：按关键词出现次数构造，便于断言排序 ──────────────────────
_KEYWORDS = ["投资", "编程", "创业"]


def fake_embed_texts(texts):
    vecs = []
    for t in texts:
        vecs.append([float(t.count(k)) for k in _KEYWORDS] + [1.0])
    return vecs


_call_counter = {"n": 0}


def counting_embed_texts(texts):
    _call_counter["n"] += len(texts)
    return fake_embed_texts(texts)


def _records():
    return [
        {"id": "a", "title": "价值投资入门",
         "summary": "复利、长期投资与价值投资的完整指南 投资 投资"},
        {"id": "b", "title": "Rust 系统编程实战",
         "summary": "内存安全与系统编程 编程 编程"},
        {"id": "c", "title": "从零到一创业",
         "summary": "早期创业的融资与团队 创业 创业"},
    ]


def setup_tmp_index(tmpdir):
    em.INDEX_PATH = Path(tmpdir) / "embeddings.json"


def test_compose_document():
    r = {"id": "x", "title": "标题", "topic": "投资", "creator": "某人",
         "core_ideas": ["观点1", "观点2"], "key_quotes": ["金句A"],
         "summary": "深度摘要内容"}
    doc = em.compose_document(r)
    assert "标题" in doc and "话题: 投资" in doc and "创作者: 某人" in doc
    assert "核心观点: 观点1；观点2" in doc and "金句A" in doc and "深度摘要内容" in doc
    # 截断
    big = {"id": "y", "title": "T", "summary": "字" * 5000}
    assert len(em.compose_document(big)) <= em.MAX_DOC_CHARS
    # 不依赖 chinese_title：只有 original_title 时也能用
    assert em.compose_document({"id": "z", "original_title": "Orig"}) == "Orig"
    print("✓ compose_document")


def test_build_incremental():
    _call_counter["n"] = 0
    recs = _records()
    s1 = em.build_index(recs)
    assert s1["built"] == 3 and s1["reused"] == 0 and s1["total"] == 3, s1
    assert _call_counter["n"] == 3, _call_counter
    # 二次构建：文本未变 → 全部复用，0 次 API 调用
    s2 = em.build_index(recs)
    assert s2["built"] == 0 and s2["reused"] == 3, s2
    assert _call_counter["n"] == 3, "复用应不再调用 API"
    # 改动一条 → 只重嵌入这一条
    recs[0]["summary"] += " 新增内容"
    s3 = em.build_index(recs)
    assert s3["built"] == 1 and s3["reused"] == 2, s3
    print("✓ build_index 增量复用")


def test_search_ranking():
    em.build_index(_records())
    hits = em.search("投资 投资 投资", _records(), top_k=3)
    assert hits, "应有结果"
    assert hits[0][0]["id"] == "a", f"投资查询应命中 a，实际 {hits[0][0]['id']}"
    assert hits[0][1] >= hits[-1][1], "应按相似度降序"
    print("✓ search 余弦排序")


def test_search_skips_stale_ids():
    em.build_index(_records())
    # records 中删掉 c（模拟飞书里已删除），但索引里仍有 c
    recs = [r for r in _records() if r["id"] != "c"]
    hits = em.search("创业", recs, top_k=5)
    ids = {h[0]["id"] for h in hits}
    assert "c" not in ids, "已不存在于 records 的脏 id 不应出现"
    assert ids <= {"a", "b"}, ids
    print("✓ search 跳过脏 record_id")


if __name__ == "__main__":
    # mock 掉真实 API
    em.embed_texts = counting_embed_texts
    with tempfile.TemporaryDirectory() as tmp:
        setup_tmp_index(tmp)
        test_compose_document()
        test_build_incremental()
        test_search_ranking()
        test_search_skips_stale_ids()
    print("\n全部通过 ✅")
