"""Event topic draft tests.

Run: blog/.venv/bin/python blog/test_topic_drafts.py
"""

from topic_drafts import (
    build_clusters,
    build_daily_draft,
    dedupe_input_items_by_canonical_url,
    dedupe_source_items,
    normalize_source_item,
    split_attention_candidates,
    topic_source_keys,
)


def item(title, url, source, score=80, **extra):
    return {
        "id": extra.pop("id", title),
        "title": title,
        "url": url,
        "source": source,
        "score": score,
        "summary": extra.pop("summary", f"{title} 的摘要。"),
        **extra,
    }


def editor_topic(cluster_index, title):
    return {
        "cluster_index": cluster_index,
        "category": "模型发布",
        "title": title,
        "what_happened": f"{title} 发生了。",
        "discussion_focus": [],
        "why_ranked": f"{title} 值得知道。",
    }


def test_same_publisher_does_not_inflate_source_count():
    rows = [
        normalize_source_item(item("A", "https://example.com/a?utm_source=x", "Example")),
        normalize_source_item(item("B", "https://example.com/b", "Example")),
        normalize_source_item(item("C", "https://official.ai/release", "Official")),
    ]
    unique = dedupe_source_items(rows)
    assert [row["publisher_key"] for row in unique] == ["example.com", "official.ai"]


def test_tracking_variants_are_globally_deduped_before_clustering():
    rows = dedupe_input_items_by_canonical_url([
        item("A", "https://example.com/a?utm_source=x", "Example", score=80),
        item("A better", "https://example.com/a", "Example", score=90),
        item("B", "https://example.com/b", "Example", score=70),
    ])
    assert [row["title"] for row in rows] == ["A better", "B"]


def test_same_publisher_representative_is_stable_when_input_reverses():
    primary = normalize_source_item(item(
        "Official", "https://example.com/official", "Example",
        score=70, is_primary=True,
    ))
    recap = normalize_source_item(item(
        "Recap", "https://example.com/recap", "Example", score=99,
    ))
    assert dedupe_source_items([primary, recap])[0]["source_id"] == primary["source_id"]
    assert dedupe_source_items([recap, primary])[0]["source_id"] == primary["source_id"]


def test_cluster_indices_are_validated_and_omitted_items_survive():
    rows = [
        item("Release", "https://official.ai/release", "Official"),
        item("Analysis", "https://media.test/analysis", "Media"),
        item("Other", "https://other.test/news", "Other"),
    ]
    clusters = build_clusters(rows, [
        {"member_indices": [1, 2, 2, 99]},
        {"member_indices": [2]},
    ])
    assert [len(c["sources"]) for c in clusters] == [2, 1]
    assert clusters[1]["sources"][0]["title"] == "Other"


def test_llm_source_count_is_ignored_and_rank_is_contiguous():
    rows = [
        item("Release", "https://official.ai/release", "Official"),
        item("Analysis", "https://media.test/analysis", "Media"),
        item("Second", "https://second.test/news", "Second"),
    ]
    clusters = build_clusters(rows, [
        {"member_indices": [1, 2]},
        {"member_indices": [3]},
    ])
    draft = build_daily_draft(
        clusters,
        {"topics": [
            {
                "cluster_index": 1,
                "source_count": 99,
                "category": "模型发布",
                "title": "一次重大模型发布",
                "what_happened": "官方发布了新模型。",
                "discussion_focus": ["真实体验", "价格"],
                "why_ranked": "影响近期模型选择。",
            },
            {
                "cluster_index": 2,
                "category": "产品变化",
                "title": "第二个主题",
                "what_happened": "产品能力发生变化。",
                "discussion_focus": [],
                "why_ranked": "影响开发工作。",
            },
        ]},
        draft_date="2026-07-11",
        generated_at="2026-07-11 09:00",
        window_hours=48,
    )
    assert [topic["rank"] for topic in draft["topics"]] == [1, 2]
    assert draft["topics"][0]["independent_source_count"] == 2
    assert draft["topics"][1]["independent_source_count"] == 1


def test_topic_id_is_stable_when_cluster_input_order_changes():
    official = item("Official", "https://official.ai/release", "Official", score=100, is_primary=True)
    media = item("Media", "https://media.test/story", "Media", score=80)
    first = build_clusters([official, media], [{"member_indices": [1, 2]}])[0]
    second = build_clusters([media, official], [{"member_indices": [1, 2]}])[0]
    assert first["topic_id"] == second["topic_id"]


def test_duplicate_model_cluster_selection_is_ignored_and_reranked():
    rows = [
        item("One", "https://one.test/release", "One"),
        item("Two", "https://two.test/release", "Two"),
    ]
    clusters = build_clusters(rows, [{"member_indices": [1]}, {"member_indices": [2]}])
    payload = {"topics": [
        editor_topic(cluster_index=1, title="One"),
        editor_topic(cluster_index=1, title="Duplicate"),
        editor_topic(cluster_index=2, title="Two"),
    ]}
    draft = build_daily_draft(
        clusters, payload, draft_date="2026-07-11",
        generated_at="2026-07-11 09:00", window_hours=48,
    )
    assert [topic["title"] for topic in draft["topics"]] == ["One", "Two"]
    assert [topic["rank"] for topic in draft["topics"]] == [1, 2]


def test_candidate_defaults_and_topic_aliases_come_from_trusted_cluster():
    rows = [
        item(
            "Official release",
            "https://official.ai/release",
            "Official",
            summary="First sentence. Extra context.",
            is_primary=True,
        ),
        item("Candidate", "https://candidate.test/news", "Candidate", summary="Candidate fact"),
    ]
    clusters = build_clusters(rows, [{"member_indices": [1]}, {"member_indices": [2]}])
    draft = build_daily_draft(
        clusters,
        {"topics": [{
            **editor_topic(1, "Edited title"),
            "discussion_focus": [" one ", "", "two", "three", "four"],
            "missing_angle": "Real usage",
            "video_queries": [" query one ", "", "query two", "query three"],
        }]},
        draft_date="2026-07-11",
        generated_at="2026-07-11 09:00",
        window_hours=48,
    )
    selected = draft["topics"][0]
    assert selected["discussion_focus"] == ["one", "two", "three", "four"]
    assert selected["item_id"] == selected["topic_id"]
    assert selected["url"] == "https://official.ai/release"
    assert selected["source"] == "Official"
    assert selected["summary"] == selected["what_happened"]
    assert selected["why"] == selected["why_ranked"]
    assert selected["video_queries"] == ["query one", "query two"]

    candidate = draft["candidates"][0]
    assert candidate["rank"] == 0
    assert candidate["title"] == "Candidate"
    assert candidate["what_happened"] == "Candidate fact。"
    assert candidate["discussion_focus"] == []
    assert candidate["why_ranked"] == "等待编辑确认"


def test_attention_split_is_disjoint_and_uses_supported_statuses():
    rows = [
        item("High", "https://high.test/news", "High", score=95),
        item("Medium", "https://medium.test/news", "Medium", score=75),
        item("Low", "https://low.test/news", "Low", score=40),
    ]
    clusters = build_clusters(rows, [])
    draft = build_daily_draft(
        clusters,
        {"topics": []},
        draft_date="2026-07-11",
        generated_at="2026-07-11 09:00",
        window_hours=48,
    )
    attention, remaining = split_attention_candidates(draft["candidates"], limit=2)
    assert [topic["title"] for topic in attention] == ["High", "Medium"]
    assert [topic["attention_status"] for topic in attention] == ["rising", "watch"]
    assert {topic["topic_id"] for topic in attention}.isdisjoint(
        {topic["topic_id"] for topic in remaining}
    )
    assert all(topic["buzz_level"] in {1, 2, 3} for topic in attention)
    assert topic_source_keys(attention[0]) == {
        attention[0]["sources"][0]["source_id"],
        attention[0]["sources"][0]["canonical_url"],
    }


def test_explicit_zero_limits_select_nothing():
    clusters = build_clusters(
        [item("Only", "https://only.test/news", "Only")],
        [{"member_indices": [1]}],
    )
    draft = build_daily_draft(
        clusters,
        {"topics": [editor_topic(1, "Only")]},
        draft_date="2026-07-11",
        generated_at="2026-07-11 09:00",
        window_hours=48,
        max_topics=0,
    )
    assert draft["topics"] == []
    assert [topic["title"] for topic in draft["candidates"]] == ["Only"]
    attention, remaining = split_attention_candidates(draft["candidates"], limit=0)
    assert attention == []
    assert [topic["title"] for topic in remaining] == ["Only"]


if __name__ == "__main__":
    test_same_publisher_does_not_inflate_source_count()
    test_tracking_variants_are_globally_deduped_before_clustering()
    test_same_publisher_representative_is_stable_when_input_reverses()
    test_cluster_indices_are_validated_and_omitted_items_survive()
    test_llm_source_count_is_ignored_and_rank_is_contiguous()
    test_topic_id_is_stable_when_cluster_input_order_changes()
    test_duplicate_model_cluster_selection_is_ignored_and_reranked()
    test_candidate_defaults_and_topic_aliases_come_from_trusted_cluster()
    test_attention_split_is_disjoint_and_uses_supported_statuses()
    test_explicit_zero_limits_select_nothing()
    print("\n全部通过 ✅")
