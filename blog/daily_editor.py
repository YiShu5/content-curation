"""Trusted server-side editing helpers for daily issues."""

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from daily_issues import DAILY_TEXT_LIMITS


EDITABLE_FIELDS = {"title", "what_happened", "discussion_focus", "why_ranked", "category"}


def trusted_draft(cache, *, expected_date):
    freshness = (cache or {}).get("freshness") or {}
    if freshness.get("status") != "fresh":
        raise ValueError(freshness.get("message") or "今日候选不可用")
    draft = (cache or {}).get("daily_draft")
    if not isinstance(draft, dict):
        raise ValueError("今日信号尚未生成事件主题草稿")
    if str(draft.get("draft_date") or "") != expected_date:
        raise ValueError("候选不是今日生成，请先重新生成今日信号")
    if any(not isinstance(draft.get(key), list) for key in ("topics", "candidates", "attention")):
        raise ValueError("今日候选数据结构异常")
    return deepcopy(draft)


def _merge_trusted_sources(base_topic, current_topic=None):
    result = deepcopy(base_topic)
    merged = {str(s.get("source_id")): deepcopy(s) for s in result.get("sources") or [] if s.get("source_id")}
    for source in (current_topic or {}).get("sources") or []:
        source_id = str(source.get("source_id") or "")
        if not source_id:
            continue
        if source_id not in merged:
            merged[source_id] = deepcopy(source)
        elif source.get("verification_status") == "readable":
            merged[source_id]["verification_status"] = "readable"
    result["sources"] = list(merged.values())
    result["independent_source_count"] = len({s.get("publisher_key") for s in result["sources"] if s.get("publisher_key")})
    return result


def revision_draft(published_issue, current_draft=None):
    published_topics = deepcopy((published_issue or {}).get("topics") or [])
    if not published_topics:
        raise ValueError("已发布简报没有可修订主题")
    current_draft = deepcopy(current_draft or {})
    current_pool = {}
    for group in ("topics", "candidates", "attention"):
        for row in current_draft.get(group) or []:
            topic_id = str(row.get("topic_id") or "")
            if topic_id:
                current_pool.setdefault(topic_id, row)
    topics = [_merge_trusted_sources(row, current_pool.get(str(row["topic_id"]))) for row in published_topics]
    top_ids = {str(row["topic_id"]) for row in topics}
    attention, attention_ids = [], set()
    for row in (published_issue or {}).get("attention") or []:
        topic_id = str(row.get("topic_id") or "")
        if topic_id and topic_id not in top_ids and topic_id not in attention_ids:
            attention.append(_merge_trusted_sources(row, current_pool.get(topic_id)))
            attention_ids.add(topic_id)
    for row in current_draft.get("attention") or []:
        topic_id = str(row.get("topic_id") or "")
        if len(attention) >= 3:
            break
        if topic_id and topic_id not in top_ids and topic_id not in attention_ids:
            attention.append(deepcopy(row)); attention_ids.add(topic_id)
    seen = top_ids | attention_ids
    candidates = []
    for topic_id, row in current_pool.items():
        if topic_id not in seen:
            candidates.append(deepcopy(row)); seen.add(topic_id)
    return {
        "schema_version": 1,
        "draft_date": current_draft.get("draft_date") or published_issue.get("issue_date"),
        "generated_at": current_draft.get("generated_at") or published_issue.get("revised_at") or published_issue.get("published_at"),
        "topics": topics, "candidates": candidates, "attention": attention,
    }


def _validate_editable_text(topic):
    checks = (
        ("category", DAILY_TEXT_LIMITS["category_max"], False),
        ("title", DAILY_TEXT_LIMITS["title_max"], True),
        ("what_happened", DAILY_TEXT_LIMITS["what_happened_max"], True),
        ("why_ranked", DAILY_TEXT_LIMITS["why_ranked_max"], True),
    )
    for field, limit, required in checks:
        value = topic.get(field, "")
        if not isinstance(value, str) or len(value.strip()) > limit or (required and not value.strip()):
            raise ValueError(f"{field} 内容无效")
        topic[field] = value.strip()
    focus = topic.get("discussion_focus")
    if not isinstance(focus, list) or len(focus) > DAILY_TEXT_LIMITS["discussion_focus_max_items"]:
        raise ValueError("讨论焦点数量无效")
    cleaned = []
    for item in focus:
        if not isinstance(item, str) or not item.strip() or len(item.strip()) > DAILY_TEXT_LIMITS["discussion_focus_item_max"]:
            raise ValueError("讨论焦点内容无效")
        cleaned.append(item.strip())
    topic["discussion_focus"] = cleaned


def apply_selection(draft, rows):
    if not isinstance(rows, list) or not 1 <= len(rows) <= 3:
        raise ValueError("简报必须包含 1–3 个主题")
    pool = {}
    for group in ("topics", "candidates", "attention"):
        for row in draft.get(group) or []:
            if row.get("topic_id"):
                pool[str(row["topic_id"])] = row
    selected, seen = [], set()
    for rank, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError("主题选择无效")
        topic_id = str(row.get("topic_id") or "")
        if topic_id not in pool or topic_id in seen:
            raise ValueError("主题不存在或重复")
        seen.add(topic_id)
        topic = deepcopy(pool[topic_id])
        for field in EDITABLE_FIELDS:
            if field in row:
                topic[field] = deepcopy(row[field])
        requested = {str(value) for value in row.get("source_ids") or [] if value}
        if "source_ids" in row:
            topic["sources"] = [s for s in topic.get("sources") or [] if str(s.get("source_id") or "") in requested]
        if not topic.get("sources"):
            raise ValueError("每个主题至少保留一个可追溯来源")
        downgrade_ids = {
            str(update.get("source_id")) for update in row.get("source_updates") or []
            if isinstance(update, dict) and str(update.get("verification_status")) == "unavailable"
        }
        for trusted_source in topic["sources"]:
            if str(trusted_source.get("source_id") or "") in downgrade_ids:
                trusted_source["verification_status"] = "unavailable"
        _validate_editable_text(topic)
        topic["rank"] = rank
        topic["independent_source_count"] = len({
            str(s.get("publisher_key") or "").strip() for s in topic["sources"]
            if str(s.get("publisher_key") or "").strip()
        })
        selected.append(topic)
    return selected


def append_editor_event(path: Path, event: dict, *, now: datetime) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"ts": now.isoformat(timespec="seconds"), **event}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
