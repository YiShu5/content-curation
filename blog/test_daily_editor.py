"""Trusted daily editor domain tests. Run: blog/.venv/bin/python blog/test_daily_editor.py"""

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from daily_editor import apply_selection, append_editor_event, revision_draft, trusted_draft


def source(source_id="real", status="readable", publisher_key="official.ai"):
    return {
        "source_id": source_id,
        "title": "Official release",
        "url": "https://official.ai/release",
        "canonical_url": "https://official.ai/release",
        "publisher": "Official",
        "publisher_key": publisher_key,
        "is_primary": True,
        "verification_status": status,
    }


def topic(topic_id="topic-a", rank=1, source_id="real"):
    return {
        "topic_id": topic_id,
        "rank": rank,
        "category": "AI",
        "title": "A",
        "what_happened": "A happened.",
        "discussion_focus": [],
        "why_ranked": "A matters.",
        "sources": [source(source_id)],
        "independent_source_count": 1,
    }


def draft_fixture():
    return {
        "schema_version": 1,
        "draft_date": "2026-07-11",
        "generated_at": "2026-07-11 09:00",
        "topics": [topic()],
        "candidates": [topic("topic-b", 0, "b")],
        "attention": [topic("topic-c", 0, "c") | {"attention_status": "rising"}],
    }


def assert_raises(callable_, message="must fail"):
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError(message)


def test_selection_can_reorder_replace_and_edit_copy_only():
    selected = apply_selection(draft_fixture(), [{
        "topic_id": "topic-b",
        "title": "编辑后的 B",
        "what_happened": "编辑后的核心事实。",
        "discussion_focus": ["焦点"],
        "why_ranked": "编辑后的判断。",
        "sources": [{"url": "https://evil.test"}],
        "source_ids": ["b"],
        "independent_source_count": 999,
        "source_updates": [{"source_id": "b", "verification_status": "unavailable"}],
    }])
    assert selected[0]["rank"] == 1
    assert selected[0]["title"] == "编辑后的 B"
    assert selected[0]["sources"][0]["url"] == "https://official.ai/release"
    assert selected[0]["independent_source_count"] == 1
    assert selected[0]["sources"][0]["verification_status"] == "unavailable"


def test_invalid_selection_shape_is_rejected():
    for rows in ([], [topic("unknown")], [{"topic_id": "topic-a"}] * 2,
                 [{"topic_id": "topic-a"}] * 4):
        assert_raises(lambda rows=rows: apply_selection(draft_fixture(), rows))


def test_untrusted_source_mutations_are_ignored_or_rejected():
    result = apply_selection(draft_fixture(), [{
        "topic_id": "topic-a", "source_ids": ["unknown", "real"],
        "source_updates": [{"source_id": "real", "verification_status": "readable"}],
    }])
    assert result[0]["sources"] == draft_fixture()["topics"][0]["sources"]
    assert_raises(lambda: apply_selection(draft_fixture(), [{
        "topic_id": "topic-a", "source_ids": ["unknown"]
    }]))


def test_text_limits_accept_boundary_and_reject_boundary_plus_one():
    fields = {
        "category": 20, "title": 60, "what_happened": 160, "why_ranked": 120,
        "missing_angle": 80,
    }
    for field, limit in fields.items():
        assert apply_selection(draft_fixture(), [{"topic_id": "topic-a", field: "x" * limit}])
        assert_raises(lambda field=field, limit=limit: apply_selection(
            draft_fixture(), [{"topic_id": "topic-a", field: "x" * (limit + 1)}]
        ))
    assert apply_selection(draft_fixture(), [{
        "topic_id": "topic-a", "discussion_focus": ["x" * 32] * 5
    }])
    assert_raises(lambda: apply_selection(draft_fixture(), [{
        "topic_id": "topic-a", "discussion_focus": ["x"] * 6
    }]))
    assert_raises(lambda: apply_selection(draft_fixture(), [{
        "topic_id": "topic-a", "discussion_focus": ["x" * 33]
    }]))


def test_trusted_draft_requires_fresh_matching_well_formed_cache():
    valid = {"freshness": {"status": "fresh"}, "daily_draft": draft_fixture()}
    result = trusted_draft(valid, expected_date="2026-07-11")
    result["topics"][0]["title"] = "changed"
    assert valid["daily_draft"]["topics"][0]["title"] == "A"
    for status in ("missing", "invalid", "expired"):
        bad = deepcopy(valid); bad["freshness"]["status"] = status
        assert_raises(lambda bad=bad: trusted_draft(bad, expected_date="2026-07-11"))
    bad = deepcopy(valid); bad["daily_draft"]["draft_date"] = "2026-07-10"
    assert_raises(lambda: trusted_draft(bad, expected_date="2026-07-11"))
    for key in ("topics", "candidates", "attention"):
        bad = deepcopy(valid); bad["daily_draft"][key] = {}
        assert_raises(lambda bad=bad: trusted_draft(bad, expected_date="2026-07-11"))


def test_revision_draft_preserves_history_and_only_merges_same_topic_evidence():
    published = {
        "issue_date": "2026-07-10", "published_at": "2026-07-10T09:00:00",
        "topics": [topic()], "attention": [topic("topic-c", 0, "old-c") | {"attention_status": "watch"}],
    }
    current = draft_fixture()
    current["topics"][0]["sources"].append(source("new", publisher_key="second.ai"))
    result = revision_draft(published, current)
    ids = [row["topic_id"] for group in ("topics", "candidates", "attention") for row in result[group]]
    assert len(ids) == len(set(ids))
    assert {s["source_id"] for s in result["topics"][0]["sources"]} == {"real", "new"}
    assert result["attention"][0]["sources"][0]["source_id"] == "old-c"


def test_append_editor_event_uses_supplied_clock():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "events.jsonl"
        append_editor_event(path, {"kind": "publish"}, now=datetime(2026, 7, 11, 9, 30))
        assert path.read_text(encoding="utf-8") == '{"ts": "2026-07-11T09:30:00", "kind": "publish"}\n'


if __name__ == "__main__":
    for name, value in sorted(globals().copy().items()):
        if name.startswith("test_") and callable(value):
            value()
    print("全部通过 ✅")
