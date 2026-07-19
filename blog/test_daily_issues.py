"""Executable tests for the local daily issue store.

Run: blog/.venv/bin/python blog/test_daily_issues.py
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import daily_issues
from daily_issues import (
    DAILY_TEXT_LIMITS,
    DailyIssueConflict,
    DailyIssueCorrupt,
    DailyIssueStore,
    DailyIssueValidationError,
    format_share_text,
    validate_issue_date,
)


def topic(
    topic_id="topic-one",
    rank=1,
    publisher="Official",
    url="https://official.ai/release",
):
    return {
        "topic_id": topic_id,
        "rank": rank,
        "category": "模型发布",
        "title": "重大模型发布",
        "what_happened": "官方发布了新模型。",
        "discussion_focus": ["真实体验"],
        "why_ranked": "影响近期模型选择。",
        "independent_source_count": 999,
        "sources": [{
            "source_id": topic_id,
            "title": "官方发布",
            "url": url,
            "canonical_url": url,
            "publisher": publisher,
            "publisher_key": publisher.lower(),
            "is_primary": True,
            "verification_status": "readable",
        }],
    }


def attention_topic(topic_id="attention-one", status="watch"):
    row = topic(topic_id=topic_id, rank=0, publisher="Attention")
    row["attention_status"] = status
    return row


def test_publish_latest_and_revise_keep_number_and_archive_old_revision():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        first = store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        assert first["issue_number"] == 1
        assert first["revision"] == 1
        assert first["topics"][0]["independent_source_count"] == 1
        revised_topic = topic()
        revised_topic["title"] = "修订后的标题"
        revised = store.revise(
            "2026-07-11",
            [revised_topic],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        assert revised["issue_number"] == 1
        assert revised["revision"] == 2
        assert store.latest()["topics"][0]["title"] == "修订后的标题"
        assert (Path(tmp) / "revisions" / "2026-07-11-r01.json").exists()


def test_revision_conflict_does_not_overwrite_current_issue():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        store.publish("2026-07-11", [topic()], [], now=now)
        try:
            store.revise(
                "2026-07-11",
                [topic()],
                [],
                expected_revision=9,
                now=now,
            )
        except DailyIssueConflict:
            pass
        else:
            raise AssertionError("expected revision conflict")
        assert store.get("2026-07-11")["revision"] == 1


def test_share_text_uses_stable_date_url():
    issue = {"issue_date": "2026-07-11", "topics": [topic()]}
    text = format_share_text(issue, "https://noise.example/daily/2026-07-11")
    assert "降噪｜2026 年 7 月 11 日" in text
    assert "① 重大模型发布" in text
    assert text.endswith("https://noise.example/daily/2026-07-11")


def test_share_text_uses_real_topic_count_and_each_judgment():
    for count in (1, 2, 3):
        topics = []
        for index in range(1, count + 1):
            row = topic(topic_id=f"topic-{index}", rank=index)
            row["title"] = f"主题 {index}"
            row["why_ranked"] = f"判断 {index}"
            topics.append(row)
        text = format_share_text(
            {"issue_date": "2026-07-11", "topics": topics},
            "https://noise.example/daily/2026-07-11",
        )
        expected_count = (
            f"本期仅有 {count} 个主题达到标准"
            if count < 3
            else "本期留下 3 个主题"
        )
        assert expected_count in text
        for index in range(1, count + 1):
            assert f"主题 {index}" in text
            assert f"判断 {index}" in text
        assert f"主题 {count + 1}" not in text


def test_publish_requires_one_to_three_topics():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        for rows in ([], [topic(f"topic-{index}", index) for index in range(1, 5)]):
            try:
                store.publish("2026-07-11", rows, [], now=now)
            except DailyIssueValidationError:
                pass
            else:
                raise AssertionError("expected topic-count validation error")


def test_publish_requires_contiguous_topic_ranks():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        rows = [topic("topic-one", 1), topic("topic-two", 3)]
        try:
            store.publish(
                "2026-07-11",
                rows,
                [],
                now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected contiguous-rank validation error")


def test_first_publish_requires_readable_evidence_for_every_topic():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        row = topic()
        row["sources"][0]["verification_status"] = "unchecked"
        try:
            store.publish(
                "2026-07-11",
                [row],
                [],
                now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected readable-source validation error")


def test_revision_may_retain_prior_evidence_as_unavailable():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        first_now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        store.publish("2026-07-11", [topic()], [], now=first_now)
        revised_topic = topic()
        revised_topic["sources"][0]["verification_status"] = "unavailable"
        revised = store.revise(
            "2026-07-11",
            [revised_topic],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        assert revised["topics"][0]["sources"][0]["verification_status"] == "unavailable"


def test_revision_cannot_launder_previously_unchecked_evidence_as_unavailable():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )

        second = topic()
        second["sources"][0]["verification_status"] = "unavailable"
        unchecked = dict(second["sources"][0])
        unchecked.update({
            "source_id": "unchecked-source",
            "title": "尚未核验的讨论",
            "url": "https://community.example/discussion",
            "canonical_url": "https://community.example/discussion",
            "publisher": "Community",
            "publisher_key": "community",
            "is_primary": False,
            "verification_status": "unchecked",
        })
        second["sources"].append(unchecked)
        store.revise(
            "2026-07-11",
            [second],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )

        third = topic()
        third["sources"] = [unchecked | {"verification_status": "unavailable"}]
        try:
            store.revise(
                "2026-07-11",
                [third],
                [],
                expected_revision=2,
                now=datetime.fromisoformat("2026-07-11T10:00:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("previously unchecked evidence must not become trusted")
        assert store.get("2026-07-11")["revision"] == 2


def test_invalid_revision_does_not_create_revision_history():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        invalid = topic()
        invalid["sources"][0]["verification_status"] = "unchecked"
        try:
            store.revise(
                "2026-07-11",
                [invalid],
                [],
                expected_revision=1,
                now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected invalid revision")
        assert store.get("2026-07-11")["revision"] == 1
        assert not (root / "revisions" / "2026-07-11-r01.json").exists()


def test_persistence_allowlists_fields_and_preserves_attention_status_without_mutation():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        selected = topic()
        selected.update({
            "provider_score": 98,
            "links": ["draft-only"],
            "suggest": {"video": True},
            "missing_angle": "draft-only",
            "video_queries": ["draft-only"],
        })
        selected["sources"][0]["provider_score"] = 100
        attention = attention_topic()
        attention["buzz_level"] = 3
        original = repr((selected, attention))
        issue = store.publish(
            "2026-07-11",
            [selected],
            [attention],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        assert issue["attention"][0]["attention_status"] == "watch"
        for field in ("provider_score", "links", "suggest", "video_queries"):
            assert field not in issue["topics"][0]
        assert issue["topics"][0]["missing_angle"] == "draft-only"  # 2026-07: 从剥离名单晋升为保留字段
        assert "provider_score" not in issue["topics"][0]["sources"][0]
        assert "buzz_level" not in issue["attention"][0]
        assert repr((selected, attention)) == original


def test_attention_accepts_zero_to_three_topics_only():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        attention = [attention_topic(f"attention-{index}") for index in range(1, 5)]
        try:
            store.publish(
                "2026-07-11",
                [topic()],
                attention,
                now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected attention-count validation error")


def test_attention_status_must_be_supported():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        try:
            store.publish(
                "2026-07-11",
                [topic()],
                [attention_topic(status="viral")],
                now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected attention-status validation error")


def test_topic_ids_cannot_repeat_across_selected_and_attention():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        try:
            store.publish(
                "2026-07-11",
                [topic("shared-topic")],
                [attention_topic("shared-topic")],
                now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected duplicate-topic validation error")


def test_text_fields_accept_hard_limit_and_reject_limit_plus_one():
    cases = (
        ("category", "category_max"),
        ("title", "title_max"),
        ("what_happened", "what_happened_max"),
        ("discussion_focus", "discussion_focus_item_max"),
        ("why_ranked", "why_ranked_max"),
        ("missing_angle", "missing_angle_max"),
    )
    now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
    for field, limit_name in cases:
        limit = DAILY_TEXT_LIMITS[limit_name]
        accepted = topic()
        accepted[field] = ["界" * limit] if field == "discussion_focus" else "界" * limit
        with TemporaryDirectory() as tmp:
            issue = DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                "2026-07-11", [accepted], [], now=now,
            )
            stored = issue["topics"][0][field]
            assert len(stored[0] if isinstance(stored, list) else stored) == limit

        rejected = topic()
        rejected[field] = ["界" * (limit + 1)] if field == "discussion_focus" else "界" * (limit + 1)
        with TemporaryDirectory() as tmp:
            try:
                DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                    "2026-07-11", [rejected], [], now=now,
                )
            except DailyIssueValidationError:
                pass
            else:
                raise AssertionError(f"expected {field} length validation error")


def test_issue_date_must_be_real_and_zero_padded():
    assert validate_issue_date("2026-07-11") == "2026-07-11"
    for invalid in ("2026-02-30", "2026-7-11", "not-a-date"):
        try:
            validate_issue_date(invalid)
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError(f"expected strict date validation for {invalid}")


def test_required_text_is_trimmed_and_layout_title_warnings_are_not_hard_limits():
    now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
    for title_length in (25, 35):
        row = topic()
        row.pop("category")
        row["title"] = f"  {'界' * title_length}  "
        row["what_happened"] = "  已发布。  "
        row["why_ranked"] = "  值得关注。  "
        with TemporaryDirectory() as tmp:
            issue = DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                "2026-07-11", [row], [], now=now,
            )
        assert issue["topics"][0]["category"] == ""
        assert issue["topics"][0]["title"] == "界" * title_length
        assert issue["topics"][0]["what_happened"] == "已发布。"
        assert issue["topics"][0]["why_ranked"] == "值得关注。"

    for field in ("title", "what_happened", "why_ranked"):
        row = topic()
        row[field] = "   "
        with TemporaryDirectory() as tmp:
            try:
                DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                    "2026-07-11", [row], [], now=now,
                )
            except DailyIssueValidationError:
                pass
            else:
                raise AssertionError(f"expected required-text validation for {field}")

    row = topic()
    row["discussion_focus"] = ["一", "二", "三", "四", "五", "六"]
    with TemporaryDirectory() as tmp:
        try:
            DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                "2026-07-11", [row], [], now=now,
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected discussion-focus count validation")


def test_duplicate_topic_ids_are_rejected_within_each_section():
    now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
    duplicate_sets = (
        ([topic("duplicate", 1), topic("duplicate", 2)], []),
        ([topic()], [attention_topic("duplicate"), attention_topic("duplicate")]),
    )
    for selected, attention in duplicate_sets:
        with TemporaryDirectory() as tmp:
            try:
                DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                    "2026-07-11", selected, attention, now=now,
                )
            except DailyIssueValidationError:
                pass
            else:
                raise AssertionError("expected duplicate-topic validation")


def test_sources_require_http_urls_and_valid_source_objects():
    now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
    invalid_sources = []
    invalid_url = topic()["sources"][0].copy()
    invalid_url["url"] = "ftp://official.ai/release"
    invalid_sources.append([invalid_url])
    invalid_canonical = topic()["sources"][0].copy()
    invalid_canonical["canonical_url"] = "javascript:alert(1)"
    invalid_sources.append([invalid_canonical])
    invalid_sources.append(["not-a-source-object"])
    for field in (
        "source_id", "title", "url", "canonical_url",
        "publisher", "publisher_key", "verification_status",
    ):
        missing = topic()["sources"][0].copy()
        missing[field] = ""
        invalid_sources.append([missing])
    invalid_status = topic()["sources"][0].copy()
    invalid_status["verification_status"] = "invented"
    invalid_sources.append([invalid_status])

    for sources in invalid_sources:
        row = topic()
        row["sources"] = sources
        with TemporaryDirectory() as tmp:
            try:
                DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
                    "2026-07-11", [row], [], now=now,
                )
            except DailyIssueValidationError:
                pass
            else:
                raise AssertionError("expected http(s) source validation")


def test_unique_non_empty_publisher_keys_define_independent_source_count():
    row = topic()
    second = row["sources"][0].copy()
    second.update({
        "source_id": "topic-one-copy",
        "url": "https://official.ai/release-copy",
        "canonical_url": "https://official.ai/release-copy",
        "publisher_key": " official ",
    })
    row["sources"].append(second)
    with TemporaryDirectory() as tmp:
        issue = DailyIssueStore(Path(tmp), "America/Los_Angeles").publish(
            "2026-07-11",
            [row],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
    assert len(issue["topics"][0]["sources"]) == 2
    assert issue["topics"][0]["independent_source_count"] == 1


def test_replacement_topic_on_revision_still_requires_readable_evidence():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        replacement = topic("topic-two")
        replacement["sources"][0]["verification_status"] = "unchecked"
        try:
            store.revise(
                "2026-07-11",
                [replacement],
                [],
                expected_revision=1,
                now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
            )
        except DailyIssueValidationError:
            pass
        else:
            raise AssertionError("expected readable evidence for replacement topic")
        assert store.get("2026-07-11")["revision"] == 1


def test_corrupt_current_uses_newest_valid_archive_everywhere_publicly_readable():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        revised = topic()
        revised["title"] = "第二版"
        store.revise(
            "2026-07-11",
            [revised],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        (root / "2026-07-11.json").write_text("{broken", encoding="utf-8")

        fallback = store.get("2026-07-11", fallback_revision=True)
        assert fallback["revision"] == 1
        assert fallback["topics"][0]["title"] == "重大模型发布"
        assert store.list_issues() == [fallback]
        assert store.latest() == fallback
        assert store.next_issue_number() == 2
        assert store.unrecoverable_dates() == []


def test_missing_current_with_valid_revision_stays_readable_and_date_reserved():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        store.revise(
            "2026-07-11",
            [topic()],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        (root / "2026-07-11.json").unlink()

        fallback = store.get("2026-07-11", fallback_revision=True)
        assert fallback["revision"] == 1
        assert store.list_issues() == [fallback]
        assert store.latest() == fallback
        assert store.next_issue_number() == 2

        for operation in (
            lambda: store.assert_revisable("2026-07-11"),
            lambda: store.preview(
                "2026-07-11",
                [topic()],
                [],
                now=datetime.fromisoformat("2026-07-11T10:00:00-07:00"),
            ),
            lambda: store.publish(
                "2026-07-11",
                [topic()],
                [],
                now=datetime.fromisoformat("2026-07-11T10:00:00-07:00"),
            ),
        ):
            try:
                operation()
            except DailyIssueConflict:
                pass
            else:
                raise AssertionError("revision-only date must remain reserved")

        next_issue = store.publish(
            "2026-07-12",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-12T09:00:00-07:00"),
        )
        assert next_issue["issue_number"] == 2


def test_unrecoverable_current_is_reported_and_blocks_number_reuse_and_writes():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        current_path = root / "2026-07-11.json"
        current_path.write_text("{broken", encoding="utf-8")

        assert store.unrecoverable_dates() == ["2026-07-11"]
        assert store.list_issues() == []
        assert store.latest() is None
        for operation in (
            lambda: store.get("2026-07-11"),
            store.next_issue_number,
            lambda: store.preview(
                "2026-07-12",
                [topic()],
                [],
                now=datetime.fromisoformat("2026-07-12T08:00:00-07:00"),
            ),
            lambda: store.publish(
                "2026-07-12",
                [topic()],
                [],
                now=datetime.fromisoformat("2026-07-12T09:00:00-07:00"),
            ),
        ):
            try:
                operation()
            except DailyIssueCorrupt as exc:
                assert str(root) not in str(exc)
            else:
                raise AssertionError("expected unrecoverable integrity error")
        assert not (root / "2026-07-12.json").exists()


def test_assert_revisable_requires_a_valid_current_snapshot_without_fallback():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        try:
            store.assert_revisable("2026-07-11")
        except DailyIssueConflict:
            pass
        else:
            raise AssertionError("expected missing-current revision error")

        first = store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        assert store.assert_revisable("2026-07-11") == first
        store.revise(
            "2026-07-11",
            [topic()],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        current_path = root / "2026-07-11.json"
        current_path.write_text("{broken-current", encoding="utf-8")
        current_bytes = current_path.read_bytes()
        revision_bytes = {
            path.name: path.read_bytes()
            for path in (root / "revisions").glob("*.json")
        }
        assert store.get("2026-07-11", fallback_revision=True)["revision"] == 1

        for operation in (
            lambda: store.assert_revisable("2026-07-11"),
            lambda: store.preview(
                "2026-07-11",
                [topic()],
                [],
                now=datetime.fromisoformat("2026-07-11T10:00:00-07:00"),
            ),
            lambda: store.revise(
                "2026-07-11",
                [topic()],
                [],
                expected_revision=1,
                now=datetime.fromisoformat("2026-07-11T10:00:00-07:00"),
            ),
        ):
            try:
                operation()
            except DailyIssueCorrupt:
                pass
            else:
                raise AssertionError("expected damaged-current revision error")
        assert current_path.read_bytes() == current_bytes
        assert {
            path.name: path.read_bytes()
            for path in (root / "revisions").glob("*.json")
        } == revision_bytes


def test_preview_is_renderable_provisional_and_never_persists_or_advances_number():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        first_now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        assert store.next_issue_number() == 1

        preview = store.preview("2026-07-11", [topic()], [], now=first_now)
        assert preview["status"] == "preview"
        assert preview["issue_number"] == 1
        assert preview["revision"] == 1
        assert preview["published_at"] == first_now.isoformat()
        assert preview["revised_at"] == first_now.isoformat()
        assert preview["topics"][0]["title"] == "重大模型发布"
        assert list(root.iterdir()) == []
        assert store.next_issue_number() == 1

        published = store.publish("2026-07-11", [topic()], [], now=first_now)
        current_path = root / "2026-07-11.json"
        current_bytes = current_path.read_bytes()
        preview_topic = topic()
        preview_topic["title"] = "预览修订"
        revision_preview = store.preview(
            "2026-07-11",
            [preview_topic],
            [],
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        assert revision_preview["status"] == "preview"
        assert revision_preview["issue_number"] == published["issue_number"]
        assert revision_preview["revision"] == 2
        assert revision_preview["published_at"] == published["published_at"]
        assert revision_preview["topics"][0]["title"] == "预览修订"
        assert current_path.read_bytes() == current_bytes
        assert not (root / "revisions").exists()
        assert store.next_issue_number() == 2


def test_issue_number_advances_only_for_new_dates_and_latest_sorts_by_date():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        first = store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        store.revise(
            "2026-07-11",
            [topic()],
            [],
            expected_revision=1,
            now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
        )
        assert store.next_issue_number() == 2
        second = store.publish(
            "2026-07-12",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-12T09:00:00-07:00"),
        )
        assert first["issue_number"] == 1
        assert second["issue_number"] == 2
        assert store.latest()["issue_date"] == "2026-07-12"
        assert store.next_issue_number() == 3


def test_failed_atomic_replace_leaves_previous_current_issue_loadable():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DailyIssueStore(root, "America/Los_Angeles")
        original = store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        current_path = root / "2026-07-11.json"
        current_bytes = current_path.read_bytes()
        real_replace = daily_issues.os.replace

        def fail_current_replace(source, destination):
            if Path(destination) == current_path:
                raise OSError("simulated current replace failure")
            return real_replace(source, destination)

        revised = topic()
        revised["title"] = "不应落盘的修订"
        with patch.object(
            daily_issues.os,
            "replace",
            side_effect=fail_current_replace,
        ):
            try:
                store.revise(
                    "2026-07-11",
                    [revised],
                    [],
                    expected_revision=1,
                    now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
                )
            except OSError as exc:
                assert "simulated current replace failure" in str(exc)
            else:
                raise AssertionError("expected atomic replace failure")

        assert current_path.read_bytes() == current_bytes
        assert store.get("2026-07-11") == original
        assert list(root.rglob("*.tmp")) == []


def test_two_store_revisions_use_flock_and_only_one_accepts_stale_revision():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        first_store = DailyIssueStore(root, "America/Los_Angeles")
        second_store = DailyIssueStore(root, "America/Los_Angeles")
        first_store.publish(
            "2026-07-11",
            [topic()],
            [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        assert (root / ".daily-issues.lock").exists()

        real_flock = daily_issues.fcntl.flock
        flock_operations = []
        outcomes = []
        result_lock = threading.Lock()
        barrier = threading.Barrier(3)

        def recording_flock(file_descriptor, operation):
            with result_lock:
                flock_operations.append(operation)
            return real_flock(file_descriptor, operation)

        def submit_revision(store, title):
            revised = topic()
            revised["title"] = title
            barrier.wait()
            try:
                issue = store.revise(
                    "2026-07-11",
                    [revised],
                    [],
                    expected_revision=1,
                    now=datetime.fromisoformat("2026-07-11T09:30:00-07:00"),
                )
            except DailyIssueConflict:
                outcome = ("conflict", None)
            except Exception as exc:  # pragma: no cover - assertion reports unexpected type
                outcome = ("unexpected", exc)
            else:
                outcome = ("success", issue)
            with result_lock:
                outcomes.append(outcome)

        threads = [
            threading.Thread(target=submit_revision, args=(first_store, "编辑甲")),
            threading.Thread(target=submit_revision, args=(second_store, "编辑乙")),
        ]
        with patch.object(daily_issues.fcntl, "flock", side_effect=recording_flock):
            for worker in threads:
                worker.start()
            barrier.wait()
            for worker in threads:
                worker.join(timeout=5)

        assert all(not worker.is_alive() for worker in threads)
        assert sorted(outcome for outcome, _ in outcomes) == ["conflict", "success"]
        success = next(value for outcome, value in outcomes if outcome == "success")
        assert success["revision"] == 2
        assert first_store.get("2026-07-11")["revision"] == 2
        assert flock_operations.count(daily_issues.fcntl.LOCK_EX) == 2
        assert flock_operations.count(daily_issues.fcntl.LOCK_UN) == 2


def test_issue_level_fields_round_trip_and_omit_empty():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        issue = store.publish("2026-07-11", [topic()], [], now=now,
                              main_line="  今天都在\n围绕算力展开  ", editor_note="")
        assert issue["main_line"] == "今天都在 围绕算力展开"  # 单行语义：内部换行折叠
        assert "editor_note" not in issue  # 空值省略键
        assert store.get("2026-07-11")["main_line"] == "今天都在 围绕算力展开"
        revised = store.revise("2026-07-11", [topic()], [], expected_revision=1,
                               now=now, main_line="", editor_note="人工补的一段手记。\n第二段保留换行。")
        assert "main_line" not in revised  # 显式传空 = 清除键
        assert revised["editor_note"] == "人工补的一段手记。\n第二段保留换行。"  # 手记合法多行
        assert store.get("2026-07-11")["editor_note"] == revised["editor_note"]
        # 修订历史里的 r01 也必须能通过快照校验（可选字段向前兼容）
        assert store.get("2026-07-11", fallback_revision=True)["revision"] == 2


def test_issue_level_fields_reject_overlength_and_non_text():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        for kwargs in (
            {"main_line": "长" * (DAILY_TEXT_LIMITS["main_line_max"] + 1)},
            {"editor_note": "长" * (DAILY_TEXT_LIMITS["editor_note_max"] + 1)},
            {"main_line": 123},
        ):
            try:
                store.publish("2026-07-11", [topic()], [], now=now, **kwargs)
            except DailyIssueValidationError:
                pass
            else:
                raise AssertionError(f"expected rejection: {kwargs}")
        assert store.get("2026-07-11") is None  # 全部被拒，没有半成品落盘


def test_snapshot_optional_field_must_match_cleaned_value_or_be_absent():
    # 逐字节 round-trip 契约：可选字段存盘值必须等于清洗结果；空值必须省键
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        now = datetime.fromisoformat("2026-07-11T09:00:00-07:00")
        store.publish("2026-07-11", [topic()], [], now=now, main_line="正常主线")
        path = Path(tmp) / "2026-07-11.json"
        good = json.loads(path.read_text(encoding="utf-8"))
        assert store.get("2026-07-11", fallback_revision=False)["main_line"] == "正常主线"
        for mutate in (
            lambda p: p.__setitem__("main_line", " 带空格的主线 "),
            lambda p: p.__setitem__("main_line", "换\n行主线"),
            lambda p: p.__setitem__("main_line", ""),
            lambda p: p.__setitem__("editor_note", 42),
            lambda p: p.__setitem__("surprise", "未知字段仍然拒绝"),
        ):
            bad = json.loads(json.dumps(good))
            mutate(bad)
            path.write_text(json.dumps(bad, ensure_ascii=False, indent=2),
                            encoding="utf-8")
            try:
                store.get("2026-07-11", fallback_revision=False)
            except DailyIssueCorrupt:
                pass
            else:
                raise AssertionError(f"expected corrupt snapshot: {bad.keys()}")


def test_share_text_leads_with_main_line_only_when_present():
    url = "https://noise.example/daily/2026-07-11"
    with_line = format_share_text(
        {"issue_date": "2026-07-11", "main_line": "都在等 agent 落地", "topics": [topic()]},
        url,
    )
    assert "今日主线｜都在等 agent 落地" in with_line
    assert with_line.splitlines()[0].startswith("降噪｜")  # 品牌行仍在最前
    without = format_share_text({"issue_date": "2026-07-11", "topics": [topic()]}, url)
    assert "今日主线" not in without


if __name__ == "__main__":
    test_publish_latest_and_revise_keep_number_and_archive_old_revision()
    test_revision_conflict_does_not_overwrite_current_issue()
    test_share_text_uses_stable_date_url()
    test_share_text_uses_real_topic_count_and_each_judgment()
    test_publish_requires_one_to_three_topics()
    test_publish_requires_contiguous_topic_ranks()
    test_first_publish_requires_readable_evidence_for_every_topic()
    test_revision_may_retain_prior_evidence_as_unavailable()
    test_revision_cannot_launder_previously_unchecked_evidence_as_unavailable()
    test_invalid_revision_does_not_create_revision_history()
    test_persistence_allowlists_fields_and_preserves_attention_status_without_mutation()
    test_attention_accepts_zero_to_three_topics_only()
    test_attention_status_must_be_supported()
    test_topic_ids_cannot_repeat_across_selected_and_attention()
    test_text_fields_accept_hard_limit_and_reject_limit_plus_one()
    test_issue_date_must_be_real_and_zero_padded()
    test_required_text_is_trimmed_and_layout_title_warnings_are_not_hard_limits()
    test_duplicate_topic_ids_are_rejected_within_each_section()
    test_sources_require_http_urls_and_valid_source_objects()
    test_unique_non_empty_publisher_keys_define_independent_source_count()
    test_replacement_topic_on_revision_still_requires_readable_evidence()
    test_corrupt_current_uses_newest_valid_archive_everywhere_publicly_readable()
    test_missing_current_with_valid_revision_stays_readable_and_date_reserved()
    test_unrecoverable_current_is_reported_and_blocks_number_reuse_and_writes()
    test_assert_revisable_requires_a_valid_current_snapshot_without_fallback()
    test_preview_is_renderable_provisional_and_never_persists_or_advances_number()
    test_issue_number_advances_only_for_new_dates_and_latest_sorts_by_date()
    test_failed_atomic_replace_leaves_previous_current_issue_loadable()
    test_two_store_revisions_use_flock_and_only_one_accepts_stale_revision()
    test_issue_level_fields_round_trip_and_omit_empty()
    test_issue_level_fields_reject_overlength_and_non_text()
    test_snapshot_optional_field_must_match_cleaned_value_or_be_absent()
    test_share_text_leads_with_main_line_only_when_present()
    print("全部通过 ✅")
