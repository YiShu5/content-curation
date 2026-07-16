"""带闸门自动发布的离线测试。

运行：blog/.venv/bin/python blog/test_auto_publish.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

from auto_publish import auto_publish
from daily_issues import DailyIssueStore, DailyIssueValidationError

TZ = "Asia/Shanghai"
NOW = datetime(2026, 7, 14, 8, 45, tzinfo=ZoneInfo(TZ))
TODAY = "2026-07-14"


def source(source_id, *, publisher="Publisher A", status="readable"):
    return {
        "source_id": source_id,
        "title": f"Source {source_id}",
        "url": f"https://example.com/{source_id}",
        "canonical_url": f"https://example.com/{source_id}",
        "publisher": publisher,
        "publisher_key": publisher.lower().replace(" ", "-"),
        "published_at": "2026-07-14T07:00:00+08:00",
        "is_primary": True,
        "verification_status": status,
    }


def topic(topic_id, rank, *, source_status="readable"):
    return {
        "topic_id": topic_id,
        "rank": rank,
        "category": "AI 前沿",
        "title": f"主题 {topic_id}",
        "what_happened": "这是事件的准确摘要。",
        "discussion_focus": ["焦点一", "焦点二"],
        "why_ranked": "它可能影响下一步判断。",
        "missing_angle": "还缺一个未被说清的角度。",
        "sources": [source(f"{topic_id}-s1", status=source_status)],
        "independent_source_count": 1,
    }


def cache_fixture(*, draft_date=TODAY, topics=None, attention=None):
    return {
        "freshness": {"status": "fresh"},
        "daily_draft": {
            "draft_date": draft_date,
            "generated_at": f"{draft_date} 08:35",
            "topics": [] if topics is None else topics,
            "candidates": [],
            "attention": [] if attention is None else attention,
        },
    }


def run(cache, tmp):
    store = DailyIssueStore(Path(tmp) / "issues", TZ)
    log = Path(tmp) / "events.jsonl"
    code, message = auto_publish(cache=cache, store=store, editor_log=log, now=NOW)
    return code, message, store, log


def test_publishes_fresh_draft_with_attention_and_audit():
    topics = [topic("topic-a", 1), topic("topic-b", 2)]
    attention = [topic("topic-c", 3)]
    with TemporaryDirectory() as tmp:
        code, message, store, log = run(cache_fixture(topics=topics, attention=attention), tmp)
        assert code == 0, message
        issue = store.get(TODAY)
        assert issue is not None and issue["revision"] == 1
        assert [row["topic_id"] for row in issue["topics"]] == ["topic-a", "topic-b"]
        assert issue["topics"][0]["missing_angle"] == "还缺一个未被说清的角度。"
        assert [row["topic_id"] for row in issue["attention"]] == ["topic-c"]
        events = [json.loads(line) for line in log.read_text().splitlines()]
        assert events[-1]["kind"] == "auto_publish"
        assert events[-1]["issue_date"] == TODAY


def test_second_run_is_idempotent():
    topics = [topic("topic-a", 1)]
    with TemporaryDirectory() as tmp:
        cache = cache_fixture(topics=topics)
        store = DailyIssueStore(Path(tmp) / "issues", TZ)
        log = Path(tmp) / "events.jsonl"
        first = auto_publish(cache=cache, store=store, editor_log=log, now=NOW)
        second = auto_publish(cache=cache, store=store, editor_log=log, now=NOW)
        assert first[0] == 0 and second[0] == 0
        assert "跳过" in second[1]
        assert store.get(TODAY)["revision"] == 1


def test_no_qualified_topics_skips_without_error():
    with TemporaryDirectory() as tmp:
        code, message, store, _ = run(cache_fixture(topics=[]), tmp)
        assert code == 0
        assert "宁缺毋滥" in message
        assert store.get(TODAY) is None


def test_stale_draft_returns_alert_code():
    with TemporaryDirectory() as tmp:
        code, message, store, _ = run(
            cache_fixture(draft_date="2026-07-13", topics=[topic("topic-a", 1)]), tmp
        )
        assert code == 1
        assert store.get(TODAY) is None


def test_evidence_gate_blocks_unverified_only_topic():
    topics = [topic("topic-a", 1, source_status="unchecked")]
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp) / "issues", TZ)
        log = Path(tmp) / "events.jsonl"
        try:
            auto_publish(cache=cache_fixture(topics=topics), store=store, editor_log=log, now=NOW)
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected evidence gate to block publish")
        assert store.get(TODAY) is None


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"OK: {len(tests)} auto publish tests passed")
