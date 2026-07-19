"""Deterministic event-topic draft normalization."""

import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from daily_issues import DAILY_TEXT_LIMITS


DROP_QUERY_KEYS = {"fbclid", "gclid", "ref", "source"}


def _safe_int(value, default=0):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return default


def _clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _one_sentence(value):
    text = _clean_text(value)
    if not text:
        return ""
    match = re.search(r"[。！？!?]|\.(?=\s|$)", text)
    if match:
        return text[:match.end()]
    return text.rstrip("，,；;：:") + "。"


def canonicalize_url(value):
    parsed = urlsplit(str(value or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    host = parsed.netloc.lower().removeprefix("www.")
    query = [
        (key, val) for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in DROP_QUERY_KEYS
    ]
    return urlunsplit((
        parsed.scheme.lower(), host, parsed.path.rstrip("/") or "/",
        urlencode(query), "",
    ))


def _publisher_key(item, canonical_url):
    parsed = urlsplit(canonical_url)
    host = parsed.netloc
    source = _clean_text(item.get("source")).lower()
    if host in {"x.com", "twitter.com"}:
        handle = parsed.path.strip("/").split("/")[0].lower()
        return f"x:{handle}" if handle else f"x:{source}"
    if host in {"youtube.com", "youtu.be", "bilibili.com"} and source:
        return f"{host}:{source}"
    return host


def normalize_source_item(item, verification_status="unchecked"):
    if not isinstance(item, dict):
        return None
    canonical = canonicalize_url(item.get("url"))
    if not canonical:
        return None
    publisher_key = _publisher_key(item, canonical)
    return {
        "source_id": hashlib.sha1(canonical.encode("utf-8")).hexdigest()[:16],
        "provider_item_id": str(item.get("id") or ""),
        "title": _clean_text(item.get("title")),
        "url": str(item.get("url") or "").strip(),
        "canonical_url": canonical,
        "publisher": _clean_text(item.get("source") or urlsplit(canonical).netloc),
        "publisher_key": publisher_key,
        "published_at": str(item.get("publishedAt") or item.get("published_at") or ""),
        "is_primary": bool(item.get("is_primary") is True),
        "verification_status": str(verification_status or "unchecked"),
        "provider_score": _safe_int(item.get("score")),
    }


def dedupe_input_items_by_canonical_url(items):
    grouped = {}
    first_positions = {}
    for position, item in enumerate(items or []):
        if not isinstance(item, dict):
            continue
        canonical = canonicalize_url(item.get("url"))
        if not canonical:
            continue
        first_positions.setdefault(canonical, position)
        current = grouped.get(canonical)
        candidate_key = (
            bool(item.get("is_primary")),
            _safe_int(item.get("score")),
        )
        current_key = (
            bool((current or {}).get("is_primary")),
            _safe_int((current or {}).get("score")),
        )
        if current is None or candidate_key > current_key:
            grouped[canonical] = item
    return [grouped[key] for key in sorted(grouped, key=first_positions.get)]


def dedupe_source_items(items):
    def preference(item):
        return (
            0 if item.get("is_primary") else 1,
            0 if item.get("verification_status") == "readable" else 1,
            -_safe_int(item.get("provider_score")),
            item["canonical_url"],
        )

    valid = [item for item in (items or []) if isinstance(item, dict)]
    by_url = {}
    for item in sorted(valid, key=preference):
        by_url.setdefault(item["canonical_url"], item)
    by_publisher = {}
    for item in sorted(by_url.values(), key=preference):
        by_publisher.setdefault(item["publisher_key"], item)
    return sorted(by_publisher.values(), key=lambda item: item["canonical_url"])


def _preferred_source(sources):
    return sorted(
        sources,
        key=lambda source: (
            0 if source.get("is_primary") else 1,
            -_safe_int(source.get("provider_score")),
            source["canonical_url"],
        ),
    )[0]


def _topic_id(sources):
    primary = _preferred_source(sources)
    digest = hashlib.sha1(primary["canonical_url"].encode("utf-8")).hexdigest()[:12]
    return "topic-" + digest


def build_clusters(items, raw_clusters):
    items = list(items or [])
    normalized = [normalize_source_item(item) for item in items]
    claimed = set()
    clusters = []
    raw_clusters = raw_clusters if isinstance(raw_clusters, list) else []
    for raw in raw_clusters:
        if not isinstance(raw, dict):
            continue
        members = []
        values = raw.get("member_indices")
        values = values if isinstance(values, list) else []
        for value in values:
            try:
                idx = int(value) - 1
            except (TypeError, ValueError):
                continue
            if idx < 0 or idx >= len(items) or idx in claimed or normalized[idx] is None:
                continue
            claimed.add(idx)
            members.append(idx)
        sources = dedupe_source_items([normalized[idx] for idx in members])
        if sources:
            primary_source = _preferred_source(sources)
            primary_item = next(
                items[idx] for idx in members
                if normalized[idx]["canonical_url"] == primary_source["canonical_url"]
            )
            clusters.append({
                "topic_id": _topic_id(sources),
                "member_indices": members,
                "sources": sources,
                "primary_item": primary_item,
            })
    for idx, source in enumerate(normalized):
        if idx not in claimed and source:
            clusters.append({
                "topic_id": _topic_id([source]),
                "member_indices": [idx],
                "sources": [source],
                "primary_item": items[idx],
            })
    return clusters


def _cluster_primary_source(cluster):
    sources = [
        source for source in (cluster.get("sources") or [])
        if isinstance(source, dict) and source.get("canonical_url")
    ]
    if not sources:
        return None
    primary_url = canonicalize_url((cluster.get("primary_item") or {}).get("url"))
    return next(
        (source for source in sources if source.get("canonical_url") == primary_url),
        _preferred_source(sources),
    )


def _clean_list(value, limit):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        clean = _clean_text(item)
        if clean:
            result.append(clean)
        if len(result) >= limit:
            break
    return result


def _legacy_aliases(topic, primary_source):
    topic.update({
        "item_id": topic["topic_id"],
        "url": primary_source.get("url") or primary_source.get("canonical_url") or "",
        "source": primary_source.get("publisher") or "",
        "summary": topic.get("what_happened") or "",
        "why": topic.get("why_ranked") or "",
    })
    return topic


def _base_topic(cluster):
    sources = [dict(source) for source in (cluster.get("sources") or [])]
    primary_source = _cluster_primary_source(cluster)
    if not sources or primary_source is None:
        return None, None
    primary_item = cluster.get("primary_item") or {}
    priority_rank = _safe_int(
        primary_item.get("_priority_rank") or primary_item.get("priority_rank")
    )
    if primary_item.get("priority_label") and not priority_rank:
        priority_rank = 1
    topic = {
        "topic_id": str(cluster.get("topic_id") or ""),
        "rank": 0,
        "category": _clean_text(primary_item.get("category")),
        "title": _clean_text(primary_item.get("title")),
        "what_happened": _one_sentence(primary_item.get("summary")),
        "discussion_focus": [],
        "why_ranked": "等待编辑确认",
        "sources": sources,
        "independent_source_count": len(sources),
        "provider_score": _safe_int(primary_source.get("provider_score")),
        "priority_rank": priority_rank,
        "missing_angle": "",
        "video_queries": [],
    }
    if primary_item.get("priority_label"):
        topic["priority_label"] = _clean_text(primary_item.get("priority_label"))
    return topic, primary_source


def normalize_editor_topic(raw, clusters, rank):
    if not isinstance(raw, dict):
        return None
    try:
        cluster_index = int(raw.get("cluster_index"))
    except (TypeError, ValueError):
        return None
    if not 1 <= cluster_index <= len(clusters or []):
        return None
    cluster = clusters[cluster_index - 1]
    topic, primary_source = _base_topic(cluster)
    if topic is None or not topic.get("topic_id"):
        return None

    title = _clean_text(raw.get("title"))
    what_happened = _one_sentence(raw.get("what_happened"))
    why_ranked = _one_sentence(raw.get("why_ranked"))
    if not title or not what_happened or not why_ranked:
        return None

    topic.update({
        "cluster_index": cluster_index,
        "rank": _safe_int(rank, 1),
        "category": _clean_text(raw.get("category")),
        "title": title,
        "what_happened": what_happened,
        "discussion_focus": _clean_list(raw.get("discussion_focus"), 5),
        "why_ranked": why_ranked,
        "missing_angle": _clean_text(raw.get("missing_angle")),
        "video_queries": _clean_list(raw.get("video_queries"), 2),
    })
    return _legacy_aliases(topic, primary_source)


def _candidate_topic(cluster):
    topic, primary_source = _base_topic(cluster)
    if topic is None or not topic.get("topic_id"):
        return None
    return _legacy_aliases(topic, primary_source)


def topic_source_keys(topic):
    keys = set()
    if not isinstance(topic, dict):
        return keys
    for source in topic.get("sources") or []:
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id") or "").strip()
        canonical_url = str(source.get("canonical_url") or "").strip()
        if source_id:
            keys.add(source_id)
        if canonical_url:
            keys.add(canonical_url)
    return keys


def build_daily_draft(
    clusters,
    editor_payload,
    *,
    draft_date,
    generated_at,
    window_hours,
    max_topics=3,
):
    clusters = [cluster for cluster in (clusters or []) if isinstance(cluster, dict)]
    raw_topics = (editor_payload or {}).get("topics") if isinstance(editor_payload, dict) else []
    raw_topics = raw_topics if isinstance(raw_topics, list) else []
    topic_limit = min(3, max(0, _safe_int(max_topics, 3)))
    topics = []
    used_cluster_indices = set()
    used_topic_ids = set()
    selected_source_keys = set()

    for raw in raw_topics:
        if len(topics) >= topic_limit:
            break
        normalized = normalize_editor_topic(raw, clusters, len(topics) + 1)
        if normalized is None:
            continue
        cluster_index = normalized["cluster_index"]
        topic_id = normalized["topic_id"]
        source_keys = topic_source_keys(normalized)
        if (
            cluster_index in used_cluster_indices
            or topic_id in used_topic_ids
            or source_keys & selected_source_keys
        ):
            continue
        normalized["rank"] = len(topics) + 1
        topics.append(normalized)
        used_cluster_indices.add(cluster_index)
        used_topic_ids.add(topic_id)
        selected_source_keys.update(source_keys)

    candidates = []
    candidate_ids = set()
    candidate_source_keys = set()
    for cluster_index, cluster in enumerate(clusters, 1):
        if cluster_index in used_cluster_indices:
            continue
        candidate = _candidate_topic(cluster)
        if candidate is None:
            continue
        topic_id = candidate["topic_id"]
        source_keys = topic_source_keys(candidate)
        if (
            topic_id in used_topic_ids
            or topic_id in candidate_ids
            or source_keys & selected_source_keys
            or source_keys & candidate_source_keys
        ):
            continue
        candidates.append(candidate)
        candidate_ids.add(topic_id)
        candidate_source_keys.update(source_keys)

    raw_item_indices = {
        index
        for cluster in clusters
        for index in (cluster.get("member_indices") or [])
        if isinstance(index, int)
    }
    unique_source_ids = {
        source.get("source_id")
        for cluster in clusters
        for source in (cluster.get("sources") or [])
        if isinstance(source, dict) and source.get("source_id")
    }
    raw_main_line = (
        (editor_payload or {}).get("main_line")
        if isinstance(editor_payload, dict) else ""
    )
    if not isinstance(raw_main_line, str):
        raw_main_line = ""  # LLM 形状漂移（列表/字典）按空丢弃，否则 repr 垃圾会直达自动发布
    return {
        "schema_version": 1,
        "draft_date": str(draft_date or ""),
        "generated_at": str(generated_at or ""),
        "window_hours": _safe_int(window_hours),
        # 今日主线：主编 LLM 的跨主题定调，一句话；允许为空（宁缺毋滥）
        "main_line": _clean_text(raw_main_line)[:DAILY_TEXT_LIMITS["main_line_max"]],
        "topics": topics,
        "candidates": candidates,
        "attention": [],
        "input_stats": {
            "raw_items": len(raw_item_indices),
            "unique_sources": len(unique_source_ids),
            "clustered_topics": len(clusters),
        },
    }


def _attention_priority(topic):
    sources = topic.get("sources") or []
    provider_score = max(
        [_safe_int(topic.get("provider_score"))]
        + [_safe_int(source.get("provider_score")) for source in sources if isinstance(source, dict)]
    )
    priority_rank = max(
        _safe_int(topic.get("priority_rank")),
        _safe_int(topic.get("_priority_rank")),
        1 if topic.get("priority_label") else 0,
    )
    return priority_rank, provider_score


def _attention_status(priority_rank, provider_score):
    if priority_rank > 0 or provider_score >= 85:
        return "rising"
    if provider_score >= 65:
        return "watch"
    return "stable"


def split_attention_candidates(candidates, limit=3):
    candidates = [dict(topic) for topic in (candidates or []) if isinstance(topic, dict)]
    attention_limit = min(3, max(0, _safe_int(limit, 3)))
    ordered = sorted(
        enumerate(candidates),
        key=lambda pair: (
            -_attention_priority(pair[1])[0],
            -_attention_priority(pair[1])[1],
            pair[0],
        ),
    )

    selected_indices = []
    selected_topic_ids = set()
    selected_source_keys = set()
    for index, topic in ordered:
        if len(selected_indices) >= attention_limit:
            break
        topic_id = str(topic.get("topic_id") or "")
        source_keys = topic_source_keys(topic)
        if topic_id in selected_topic_ids or source_keys & selected_source_keys:
            continue
        selected_indices.append(index)
        selected_topic_ids.add(topic_id)
        selected_source_keys.update(source_keys)

    selected_index_set = set(selected_indices)
    attention = []
    for index in selected_indices:
        topic = dict(candidates[index])
        priority_rank, provider_score = _attention_priority(topic)
        status = _attention_status(priority_rank, provider_score)
        topic["attention_status"] = status
        topic["buzz_label"] = topic.get("priority_label") or {
            "rising": "热度上升",
            "watch": "值得观察",
            "stable": "稳定关注",
        }[status]
        topic["buzz_reason"] = topic.get("why_ranked") or "等待编辑确认"
        topic["buzz_level"] = {"rising": 3, "watch": 2, "stable": 1}[status]
        topic.setdefault("suggested_slot", "industry_trend")
        topic.setdefault("verification_label", "待你确认")
        topic.setdefault("score", provider_score)
        attention.append(topic)

    remaining = []
    seen_remaining_ids = set()
    seen_remaining_sources = set()
    for index, topic in enumerate(candidates):
        topic_id = str(topic.get("topic_id") or "")
        source_keys = topic_source_keys(topic)
        if (
            index in selected_index_set
            or topic_id in selected_topic_ids
            or source_keys & selected_source_keys
            or topic_id in seen_remaining_ids
            or source_keys & seen_remaining_sources
        ):
            continue
        remaining.append(topic)
        seen_remaining_ids.add(topic_id)
        seen_remaining_sources.update(source_keys)
    return attention, remaining
