# Daily NoiseFilter Editorial Home Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a manually published, date-stable NoiseFilter daily brief whose public homepage shows one large #1 topic card, two smaller #2/#3 cards, then “热议浮现” and the existing deep-content library.

**Architecture:** Keep the existing Flask + local JSON architecture, but separate mutable signal generation from immutable published issues. Add one pure topic-draft module for event/source normalization, one issue store for atomic publish/revise/history, one small admin-auth module, and focused public/admin templates with standalone JavaScript. The public homepage reads only the latest published issue; `today_signal.json` remains an administrator draft input.

**Tech Stack:** Python 3, Flask 3, Jinja2, standard-library `json` / `zoneinfo` / `hmac` / `secrets`, plain JavaScript and CSS, existing script-style Python tests, existing `blog/.venv`, local JSON files under `blog/data/`.

## Global Constraints

- The product entry point is: personal reading first, then direct sharing with colleagues.
- The ranked unit is an event topic, not an article.
- The public masthead is exactly `今天，哪些讨论值得知道？` for a current issue and uses `这一天` for a historical issue.
- Public layout is exactly one large left card for rank 1 and two stacked right cards for ranks 2 and 3 on desktop.
- Keep the approved warm beige background, rounded cards, blue auxiliary accents, and restrained red focal accents.
- Public content order is exactly `今日前三 → 热议浮现 → 深度内容库`.
- Ranking semantics are discussion breadth for discovery, importance for correction, source quality for trust, and human confirmation for final order.
- Never display `AI HOT`, internal numeric scores, heat dashboards, audience-mode switches, or the rejected newspaper layout.
- Publish 1–3 topics only; never pad weak topics and never publish an empty issue.
- Publishing is manual. Revising the same date keeps the issue number and URL, archives the previous revision, and shows the last revised time.
- `/` always shows the latest successfully published issue; `/daily/YYYY-MM-DD` is the stable share URL.
- Public readers must never see or invoke publish, reorder, replace, promote, dismiss, or ingest mutations.
- Independent source count is computed from server-normalized sources; never trust LLM output or browser-submitted counts.
- Keep `archive/` as the source of truth for the deep-content library and do not redesign its existing image cards.
- The first event-draft implementation reuses the existing AI HOT realtime candidate pool and the publishers/links it already aggregates. Direct RSS adapters or additional external-source connectors are future discovery improvements, not part of this UI/publication release; the public source count still reflects only real normalized evidence present in the current pool.
- Keep the blog on port `5055`; use `blog/.venv` for Flask and blog tests.
- Do not add a database, queue, frontend framework, test framework, or new third-party dependency.
- Secrets remain in `config/.env`, which must never be committed.
- `blog/data/` remains ignored; external deployment must mount `DAILY_ISSUES_DIR` on persistent storage before relying on dated links.

---

## Scope Check and Delivery Order

The design touches signal preparation, storage, authentication, public rendering, and admin editing, but these form one vertical publication workflow rather than independent products. The tasks are ordered so every trust boundary is implemented before the UI exposes it:

```text
source evidence → topic draft → atomic issue store → admin security
       → public dated routes → public card UI → publish/revise API → admin editor
```

Do not start the public “X 个来源已合并” UI before Task 1 passes. Do not expose publish controls before Tasks 2 and 3 pass.

## Execution Prerequisite

At execution time, first invoke `superpowers:using-git-worktrees` if implementation will run in an isolated worktree. The current main worktree has user-owned untracked files:

```text
.superpowers/
AGENTS.md
```

Do not stage, delete, move, or commit either path. A worktree can start from commit `72a3337` because all functional code and the approved design spec are committed; copy the user-supplied AGENTS instructions into the execution context rather than committing the file.

The verified pre-implementation baseline is:

```bash
set -e
for f in \
  blog/test_product_schema.py \
  blog/test_user_preferences.py \
  blog/test_embeddings.py \
  blog/test_ingest_jobs.py \
  blog/test_today_signal.py \
  blog/test_app_routes.py
do
  blog/.venv/bin/python "$f"
done
node scripts/test-product-schema.mjs
node scripts/test-rewrite-format.mjs
```

Expected: every script prints `全部通过 ✅` or its named success line and exits 0.

## File Structure

### New files

- `blog/topic_drafts.py` — deterministic source normalization, event-cluster validation, stable topic IDs, and draft serialization.
- `blog/test_topic_drafts.py` — event/source trust tests independent of Flask and network calls.
- `blog/daily_issues.py` — issue validation, atomic JSON persistence, revision history, latest/list lookup, and share text.
- `blog/test_daily_issues.py` — 1–3 topic validation, publish/revise/rollback/concurrency tests.
- `blog/admin_auth.py` — single-admin session, constant-time password check, CSRF, and decorators.
- `blog/test_admin_routes.py` — login, CSRF, permissions, publish/revise route tests.
- `blog/daily_editor.py` — server-side merge of administrator text edits with trusted draft evidence plus audit logging.
- `blog/test_daily_editor.py` — tamper resistance, reorder/replace, and audit-event tests.
- `blog/test_daily_routes.py` — latest/date/archive route and public-isolation tests.
- `blog/test_daily_templates.py` — 1/2/3-card rendering and source-label tests.
- `blog/templates/_daily_brief.html` — public masthead and 1+2 card grid.
- `blog/templates/_daily_topic_card.html` — one public topic card and evidence disclosure.
- `blog/templates/_daily_attention.html` — read-only “热议浮现”.
- `blog/templates/daily.html` — fixed-date issue page.
- `blog/templates/daily_archive.html` — dated issue index.
- `blog/templates/daily_unavailable.html` — friendly 503 page for an unrecoverable dated snapshot.
- `blog/templates/admin_login.html` — single-admin login page.
- `blog/templates/_admin_daily_dialog.html` — reorder/edit/replace/preview/publish interface.
- `blog/static/css/daily.css` — public daily-brief styles isolated under `.daily-*` selectors.
- `blog/static/css/admin-daily.css` — authenticated editor styles.
- `blog/static/js/daily.js` — copy-share behavior only.
- `blog/static/js/admin-daily.mjs` — authenticated draft editor and publish/revise requests.
- `blog/static/js/admin-daily-state.mjs` — DOM-free editor state normalization and collection mutations.
- `blog/test_admin_daily_state.mjs` — Node regression tests for candidate replacement payloads.
- `blog/static/og-daily.svg` — editable 1200×630 share artwork source.
- `blog/static/og-daily.png` — rendered Open Graph image.

### Modified files

- `blog/today_signal.py:374-447, 538-583, 632-875, 1297-1348` — replace fixed-slot article selection with topic clusters and persist `daily_draft` while retaining legacy fields during migration.
- `blog/test_today_signal.py:88-188, 372-426, 429-end` — update selection and public-management assumptions; keep freshness regression coverage.
- `config/preferences.json:9-63` — add explicit daily-brief limits and make old fixed slots legacy preferences rather than public ranks.
- `blog/config.py:3-21` — admin, timezone, persistent issue directory, public base URL, and secure cookie configuration.
- `blog/app.py:5-60, 257-298, 461-548` — issue routes, auth routes, protected mutations, draft/publish/revise APIs, and view-model helpers.
- `blog/test_app_routes.py:17-118` — public issue rendering, archive, stable dates, and old-public-signal regression tests.
- `blog/templates/base.html:1-30` — meta blocks, fused NoiseFilter logo, navigation slots, and page-specific script/head hooks.
- `blog/templates/index.html:1-80, 184-218` — replace `_signals.html` include with `_daily_brief.html`; preserve the existing library/filter/card grid.
- `blog/static/favicon.svg:1-4` — match the approved multi-in/one-out blue/red mark.
- `README.md:179-188` — update the homepage description and manual publish commands.
- `docs/产品定位与用户场景.md:9-84, 137-158` — record the confirmed “个人先读，顺手分享给同事” entry point.

---

### Task 1: Trustworthy Event Topic Drafts

**Files:**
- Create: `blog/topic_drafts.py`
- Create: `blog/test_topic_drafts.py`
- Modify: `blog/today_signal.py:374-447, 538-583, 632-875, 1099-1233, 1297-1348`
- Modify: `blog/test_today_signal.py:88-188, 372-426`
- Modify: `config/preferences.json:9-63`

**Interfaces:**
- Consumes: raw AI HOT item dictionaries returned by `today_signal.fetch_aihot()`.
- Produces:
  - `normalize_source_item(item: dict, verification_status: str = "unchecked") -> dict | None`
  - `dedupe_input_items_by_canonical_url(items: list[dict]) -> list[dict]`
  - `dedupe_source_items(items: list[dict]) -> list[dict]`
  - `build_clusters(items: list[dict], raw_clusters: list[dict]) -> list[dict]`
  - `normalize_editor_topic(raw: dict, clusters: list[dict], rank: int) -> dict | None`
  - `build_daily_draft(clusters: list[dict], editor_payload: dict, *, draft_date: str, generated_at: str, window_hours: int, max_topics: int = 3) -> dict`
  - `topic_source_keys(topic: dict) -> set[str]`
  - `split_attention_candidates(candidates: list[dict], limit: int = 3) -> tuple[list[dict], list[dict]]`
- `today_signal.generate_signals()` adds `daily_draft` with `topics`, `candidates`, `attention`, and `input_stats`; legacy `signals` mirrors `daily_draft.topics` for one migration cycle.

- [ ] **Step 1: Write failing source and cluster tests**

Create `blog/test_topic_drafts.py` using the repository’s executable script-test style:

```python
"""Event topic draft tests.

Run: blog/.venv/bin/python blog/test_topic_drafts.py
"""

from topic_drafts import (
    build_clusters,
    build_daily_draft,
    dedupe_input_items_by_canonical_url,
    dedupe_source_items,
    normalize_source_item,
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


if __name__ == "__main__":
    test_same_publisher_does_not_inflate_source_count()
    test_tracking_variants_are_globally_deduped_before_clustering()
    test_same_publisher_representative_is_stable_when_input_reverses()
    test_cluster_indices_are_validated_and_omitted_items_survive()
    test_llm_source_count_is_ignored_and_rank_is_contiguous()
    test_topic_id_is_stable_when_cluster_input_order_changes()
    test_duplicate_model_cluster_selection_is_ignored_and_reranked()
    print("\n全部通过 ✅")
```

- [ ] **Step 2: Run the new test and verify it fails**

Run:

```bash
blog/.venv/bin/python blog/test_topic_drafts.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'topic_drafts'`.

- [ ] **Step 3: Implement deterministic source normalization and clustering**

Create `blog/topic_drafts.py`. The core URL and publisher logic is:

```python
"""Deterministic event-topic draft normalization."""

import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


DROP_QUERY_KEYS = {"fbclid", "gclid", "ref", "source"}


def canonicalize_url(value):
    parsed = urlsplit(str(value or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    host = parsed.netloc.lower().removeprefix("www.")
    query = [
        (key, val) for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in DROP_QUERY_KEYS
    ]
    return urlunsplit((parsed.scheme.lower(), host, parsed.path.rstrip("/") or "/", urlencode(query), ""))


def _publisher_key(item, canonical_url):
    parsed = urlsplit(canonical_url)
    host = parsed.netloc
    source = re.sub(r"\s+", " ", str(item.get("source") or "")).strip().lower()
    if host in {"x.com", "twitter.com"}:
        handle = parsed.path.strip("/").split("/")[0].lower()
        return f"x:{handle}" if handle else f"x:{source}"
    if host in {"youtube.com", "youtu.be", "bilibili.com"} and source:
        return f"{host}:{source}"
    return host


def normalize_source_item(item, verification_status="unchecked"):
    canonical = canonicalize_url(item.get("url"))
    if not canonical:
        return None
    publisher_key = _publisher_key(item, canonical)
    return {
        "source_id": hashlib.sha1(canonical.encode("utf-8")).hexdigest()[:16],
        "provider_item_id": str(item.get("id") or ""),
        "title": str(item.get("title") or "").strip(),
        "url": str(item.get("url") or "").strip(),
        "canonical_url": canonical,
        "publisher": str(item.get("source") or urlsplit(canonical).netloc).strip(),
        "publisher_key": publisher_key,
        "published_at": str(item.get("publishedAt") or item.get("published_at") or ""),
        "is_primary": bool(item.get("is_primary") is True),
        "verification_status": verification_status,
        "provider_score": int(item.get("score") or 0),
    }


def dedupe_input_items_by_canonical_url(items):
    grouped = {}
    first_positions = {}
    for position, item in enumerate(items or []):
        canonical = canonicalize_url(item.get("url"))
        if not canonical:
            continue
        first_positions.setdefault(canonical, position)
        current = grouped.get(canonical)
        candidate_key = (bool(item.get("is_primary")), int(item.get("score") or 0))
        current_key = (bool((current or {}).get("is_primary")), int((current or {}).get("score") or 0))
        if current is None or candidate_key > current_key:
            grouped[canonical] = item
    return [grouped[key] for key in sorted(grouped, key=first_positions.get)]


def dedupe_source_items(items):
    def preference(item):
        return (
            0 if item.get("is_primary") else 1,
            0 if item.get("verification_status") == "readable" else 1,
            -int(item.get("provider_score") or 0),
            item["canonical_url"],
        )
    by_url = {}
    for item in sorted((item for item in items if item), key=preference):
        by_url.setdefault(item["canonical_url"], item)
    by_publisher = {}
    for item in sorted(by_url.values(), key=preference):
        by_publisher.setdefault(item["publisher_key"], item)
    return sorted(by_publisher.values(), key=lambda item: item["canonical_url"])


def _topic_id(sources):
    primary = sorted(
        sources,
        key=lambda source: (
            0 if source.get("is_primary") else 1,
            -int(source.get("provider_score") or 0),
            source["canonical_url"],
        ),
    )[0]
    return "topic-" + hashlib.sha1(primary["canonical_url"].encode("utf-8")).hexdigest()[:12]


def build_clusters(items, raw_clusters):
    normalized = [normalize_source_item(item) for item in items]
    claimed = set()
    clusters = []
    for raw in raw_clusters or []:
        members = []
        for value in raw.get("member_indices") or []:
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
            primary_source = sorted(
                sources,
                key=lambda source: (0 if source.get("is_primary") else 1, -source.get("provider_score", 0), source["canonical_url"]),
            )[0]
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
```

Add `normalize_editor_topic()`, `build_daily_draft()`, `topic_source_keys()`, and `split_attention_candidates()` below this code. They must accept only valid one-based `cluster_index` values, ignore count fields from the model, track used cluster/topic IDs so a repeated model selection is ignored, trim `discussion_focus` to three non-empty strings, derive `independent_source_count = len(sources)`, cap topics at three, and recompute contiguous ranks after rejection. Put unselected clusters in `candidates`. Persist the explicit blog-local `draft_date` separately from display-oriented `generated_at`. Every candidate receives editable defaults from its primary item (`title`, one-sentence `what_happened`, empty `discussion_focus`, and a non-assertive `why_ranked="等待编辑确认"`) so replacement never depends on missing keys.

For the migration cycle, each topic also exposes read-only legacy aliases derived from its trusted primary source: `item_id=topic_id`, `url`, `source`, `summary=what_happened`, and `why=why_ranked`. Never derive trusted evidence back from those aliases.

`split_attention_candidates()` takes topic-shaped candidates, selects at most three by existing priority/provider-score signals, sets `attention_status` to exactly one of `rising`, `watch`, or `stable` plus legacy `buzz_*` aliases, and returns `(attention, remaining_candidates)`. Thus the same `topic_id` cannot appear in both arrays.

- [ ] **Step 4: Replace fixed-slot prompts with cluster + ranked-topic prompts**

In `blog/today_signal.py:374-447`, replace `_SHORTLIST_PROMPT` with:

```python
_CLUSTER_PROMPT = """你是极度克制的 AI 资讯编辑。把下面最多 {pool_size} 条候选按“同一事实事件”合并，
再留下最多 {limit} 个值得读取原文的事件簇。相同产品名但不同发布日期或不同发布事件不能合并；宽泛主题相似也不能合并。

只输出 JSON：
{{"clusters":[{{"member_indices":[1,4,7]}},{{"member_indices":[2]}}]}}

候选：
{items}
"""
```

Replace `_EDITOR_PROMPT` with a ranked-topic schema. The model may write copy and choose cluster indices, but it must not return source counts:

```python
_EDITOR_PROMPT = """你是 NoiseFilter 主编。基于已经读取原文的事件簇，选出最多三个今天值得知道的讨论并按重要性排序。

排序原则：讨论广度负责发现，新闻重要性负责纠偏，信源质量负责兜底；重大模型发布、平台政策变化、关键产品停用可在讨论刚开始时进入高位。宁缺毋滥。

每个主题输出：cluster_index、category、title、what_happened、discussion_focus（最多三个短语）、why_ranked、missing_angle、video_queries。title 不超过 34 个中文字符；what_happened 只说一个核心事实；why_ranked 不重复事实。

只输出 JSON：
{{"topics":[{{"cluster_index":1,"category":"模型发布","title":"标题","what_happened":"一句核心事实。","discussion_focus":["焦点一","焦点二"],"why_ranked":"为什么值得今天先知道。","missing_angle":"仍缺什么","video_queries":["query one","query two"]}}]}}

事件簇：
{items}
"""
```

Add `_build_daily_draft(news, profile)` next to the editorial helpers. It calls `_pool_candidates()`, then globally removes exact canonical-URL duplicates with `dedupe_input_items_by_canonical_url()` before constructing the numbered cluster prompt. It calls `_chat_json(_CLUSTER_PROMPT)`, `topic_drafts.build_clusters()`, reads the primary source of at most 12 clusters with existing `read_original()`, drops clusters whose primary source is unreadable, marks the surviving primary evidence `verification_status="readable"`, calls the new `_EDITOR_PROMPT`, then returns `topic_drafts.build_daily_draft()`. Related sources may remain `unchecked`; at least one readable source is mandatory for a top-three topic. Global dedupe is by canonical URL only—never by publisher—so separate reporting from the same publisher can still be clustered before independent-publisher counting.

- [ ] **Step 5: Persist the new draft without breaking one migration cycle**

Make signal timestamps use `ZoneInfo(os.getenv("BLOG_TIMEZONE", "America/Los_Angeles"))` in both generation and freshness checks. `_parse_generated_at()` attaches that zone and `datetime.fromtimestamp()` receives the same zone; update freshness tests to use aware datetimes so CI host timezone cannot change the result.

Update `generate_signals()` at `blog/today_signal.py:1297-1348` so it writes:

```python
daily_draft = _build_daily_draft(news, profile) if news else {
    "schema_version": 1,
    "draft_date": local_now.date().isoformat(),
    "generated_at": local_now.strftime("%Y-%m-%d %H:%M"),
    "window_hours": window_hours,
    "topics": [],
    "candidates": [],
    "attention": [],
    "input_stats": {"raw_items": 0, "unique_sources": 0, "clustered_topics": 0},
}
topics = daily_draft.get("topics") or []
attention, remaining_candidates = topic_drafts.split_attention_candidates(
    daily_draft.get("candidates") or [], limit=ATTENTION_MAX
)
daily_draft["candidates"] = remaining_candidates
daily_draft["attention"] = attention

payload = {
    "expiry": now + SIGNAL_TTL,
    "generated_at": daily_draft["generated_at"],
    "window_hours": window_hours,
    "daily_draft": daily_draft,
    "breaking": None,
    "signals": topics,
    "attention": attention,
    "slots_total": 3,
    "behavior": behavior_summary(profile),
}
```

Keep `_build_attention_candidates()` and `promote_attention_item()` only for legacy compatibility; `generate_signals()` now uses topic-shaped `split_attention_candidates()`, and the new public UI never calls either legacy mutation. Add a test proving none of a selected topic’s canonical URLs or source IDs can reappear in `candidates` or `attention`, including tracking-parameter URL variants that the clustering model attempted to split across clusters.

Do not regress the existing deep-learning enrichment after topic selection. Run the current `_prepare_library()` / `_match_library()` loop over the selected event topics using their read-only legacy aliases, preserving one-record-per-page dedupe. Only when a topic has no library match may the existing `suggest_video()` path use its trusted `missing_angle` / `video_queries`, still respecting the page-wide suggestion cap and ≥75 threshold. Keep `links`, `suggest`, `missing_angle`, and `video_queries` in the mutable admin/legacy draft only; Task 2’s stored-issue validator whitelists public snapshot fields and strips those internal enrichment keys. Retain the existing library-match and video-gating regression tests in `test_today_signal.py`.

Allow `SIGNAL_CACHE` to be overridden by `SIGNAL_CACHE_PATH` while keeping `blog/data/today_signal.json` as the default. Replace `_write_signal_cache()` with same-directory temp-file + `flush()` + `os.fsync()` + `os.replace()` persistence, cleaning the temp file in `finally`. This prevents the admin draft reader from observing partial JSON while `run.sh signals` is writing and lets tests/QA avoid real `blog/data/`. Extend `_has_malformed_signal_cache_fields()` to reject a present `daily_draft` unless it is a dict whose `topics`, `candidates`, and `attention` are lists. Add a rollback test by patching `os.replace` and asserting the previous valid cache remains readable.

Add this object to `config/preferences.json`:

```json
"daily_brief": {
  "max_topics": 3,
  "max_candidates": 12,
  "min_sources_for_merged_label": 2,
  "lead_title_target_chars": 34,
  "side_title_target_chars": 24,
  "discussion_focus_max": 3
}
```

These 34/24 values guide model copy and layout warnings only. Hard persistence limits come from `DAILY_TEXT_LIMITS` in Task 2, so changing prompt preferences cannot weaken the stored schema.

- [ ] **Step 6: Update signal tests for event topics**

Stub `_chat_json` and `read_original` in `blog/test_today_signal.py`, then assert:

```python
assert len(cache["daily_draft"]["topics"]) <= 3
assert [t["rank"] for t in cache["daily_draft"]["topics"]] == list(
    range(1, len(cache["daily_draft"]["topics"]) + 1)
)
assert cache["daily_draft"]["topics"][0]["independent_source_count"] == len(
    cache["daily_draft"]["topics"][0]["sources"]
)
top_source_ids = {
    source["source_id"]
    for topic in cache["daily_draft"]["topics"]
    for source in topic["sources"]
}
other_source_ids = {
    source["source_id"]
    for group in ("candidates", "attention")
    for topic in cache["daily_draft"][group]
    for source in topic["sources"]
}
assert top_source_ids.isdisjoint(other_source_ids)
```

Also assert `draft_date` and `generated_at` use the configured blog-local date, a yesterday-generated cache that is still freshness-`fresh` before the delivery hour cannot become today’s first-publication draft, an expired cache cannot become a first-publication draft, and malformed `daily_draft` arrays produce freshness status `invalid`.

- [ ] **Step 7: Run focused and regression tests**

```bash
blog/.venv/bin/python blog/test_topic_drafts.py
blog/.venv/bin/python blog/test_today_signal.py
PYTHONDONTWRITEBYTECODE=1 blog/.venv/bin/python -m py_compile \
  blog/topic_drafts.py blog/today_signal.py blog/test_topic_drafts.py blog/test_today_signal.py
```

Expected: both tests print `全部通过 ✅`; `py_compile` exits 0 without output.

- [ ] **Step 8: Commit the topic-draft foundation**

```bash
git add blog/topic_drafts.py blog/test_topic_drafts.py blog/today_signal.py blog/test_today_signal.py config/preferences.json
git commit -m "feat: build trustworthy daily topic drafts"
```

---

### Task 2: Atomic Daily Issue Store and Revision History

**Files:**
- Create: `blog/daily_issues.py`
- Create: `blog/test_daily_issues.py`

**Interfaces:**
- Consumes: administrator-approved `topics` and `attention` derived from Task 1 draft evidence.
- Produces:
  - `DAILY_TEXT_LIMITS` — one server-owned mapping used by persistence validation, editor validation, and authenticated UI hints.
  - `validate_issue_date(value: str) -> str`
  - `DailyIssueStore(root: Path, timezone_name: str)`
  - `list_issues() -> list[dict]`
  - `unrecoverable_dates() -> list[str]`
  - `get(issue_date: str, *, fallback_revision: bool = True) -> dict | None`
  - `assert_revisable(issue_date: str) -> dict`
  - `latest() -> dict | None`
  - `next_issue_number() -> int`
  - `preview(issue_date: str, topics: list[dict], attention: list[dict], *, now: datetime) -> dict`
  - `publish(issue_date: str, topics: list[dict], attention: list[dict], *, now: datetime) -> dict`
  - `revise(issue_date: str, topics: list[dict], attention: list[dict], *, expected_revision: int, now: datetime) -> dict`
  - `format_share_text(issue: dict, stable_url: str) -> str`

- [ ] **Step 1: Write failing persistence tests**

Create `blog/test_daily_issues.py` with a valid-topic helper and these tests:

```python
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from daily_issues import DailyIssueConflict, DailyIssueStore, format_share_text


def topic(topic_id="topic-one", rank=1, publisher="Official", url="https://official.ai/release"):
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


def test_publish_latest_and_revise_keep_number_and_archive_old_revision():
    with TemporaryDirectory() as tmp:
        store = DailyIssueStore(Path(tmp), "America/Los_Angeles")
        first = store.publish(
            "2026-07-11", [topic()], [],
            now=datetime.fromisoformat("2026-07-11T09:00:00-07:00"),
        )
        assert first["issue_number"] == 1
        assert first["revision"] == 1
        assert first["topics"][0]["independent_source_count"] == 1
        revised_topic = topic()
        revised_topic["title"] = "修订后的标题"
        revised = store.revise(
            "2026-07-11", [revised_topic], [], expected_revision=1,
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
            store.revise("2026-07-11", [topic()], [], expected_revision=9, now=now)
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
        expected_count = f"本期仅有 {count} 个主题达到标准" if count < 3 else "本期留下 3 个主题"
        assert expected_count in text
        for index in range(1, count + 1):
            assert f"主题 {index}" in text
            assert f"判断 {index}" in text
        assert f"主题 {count + 1}" not in text
```

Add an executable `__main__` block that runs all tests and prints `全部通过 ✅`.

`format_share_text()` uses the exact real-count line tested above, then one numbered title plus its one-sentence `why_ranked` per selected topic, and finally the stable dated URL. It never says “三个” for a one- or two-topic issue and never copies `/`.

- [ ] **Step 2: Run the issue tests and verify they fail**

```bash
blog/.venv/bin/python blog/test_daily_issues.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'daily_issues'`.

- [ ] **Step 3: Implement strict validation and atomic writes**

Create `blog/daily_issues.py` with these errors:

```python
class DailyIssueError(RuntimeError):
    pass


class DailyIssueValidationError(DailyIssueError):
    pass


class DailyIssueConflict(DailyIssueError):
    pass


class DailyIssueCorrupt(DailyIssueError):
    pass


DAILY_TEXT_LIMITS = {
    "category_max": 20,
    "title_max": 60,
    "lead_title_warning": 34,
    "side_title_warning": 24,
    "what_happened_max": 160,
    "discussion_focus_max_items": 3,
    "discussion_focus_item_max": 32,
    "why_ranked_max": 120,
}
```

Implement strict calendar parsing with `datetime.strptime(value, "%Y-%m-%d")`, 1–3 topics, contiguous ranks, required `title` / `what_happened` / `why_ranked`, optional `category`, and `http(s)` sources. Enforce the hard `DAILY_TEXT_LIMITS` with Python `len()` after trimming; the 34/24 title values are warnings, while `title_max=60` is the hard rejection boundary. Validate zero-to-three attention topics, `attention_status` in `{rising, watch, stable}`, and no duplicate `topic_id` across top topics and attention. Rebuild `independent_source_count` from unique non-empty `publisher_key` values on every publish/revise; never mutate caller-owned input. A first publication requires at least one `verification_status="readable"` source per top-three topic. On revision, a newly selected topic must also have readable evidence; an existing topic may retain prior source IDs as `unavailable`, but it cannot replace all prior evidence with new unchecked sources.

Build each validated snapshot topic from an explicit allowlist: `topic_id`, `rank`, `category`, `title`, `what_happened`, `discussion_focus`, `why_ranked`, `sources`, and recalculated `independent_source_count`; attention additionally allows `attention_status`. Each source allowlist is `source_id`, `title`, `url`, `canonical_url`, `publisher`, `publisher_key`, `published_at`, `is_primary`, and `verification_status`. Strip draft-only legacy aliases, provider scores, library `links`, video `suggest`, `missing_angle`, and `video_queries` before persistence.

Factor validation and payload assembly into one private method used by `preview()`, `publish()`, and `revise()`. `unrecoverable_dates()` returns strictly parsed issue dates whose current snapshot is malformed and has no valid archived revision. `list_issues()` enumerates the union of current issue dates and revision dates, resolves every date through `get(..., fallback_revision=True)`, skips those unrecoverable dates, and sorts valid snapshots by `issue_date` descending; `latest()` returns its first item, never a max-mtime file. Before `next_issue_number()`, preview, publish, or revise, a private integrity scan raises `DailyIssueCorrupt` when `unrecoverable_dates()` is non-empty. Otherwise `next_issue_number()` uses the fallback-aware list and returns `max(issue_number) + 1`, or `1` when empty. This lets public routes distinguish “never published” from “latest snapshot damaged” while blocking every write that could reuse a number or compound damage; surface a recovery message without a filesystem path. `preview()` acquires the same read lock, calls `assert_revisable()` when that date already exists, derives the provisional next issue/revision number, returns `status="preview"`, and never writes or archives a file. Publication re-runs the same validation under the exclusive write lock, so preview and the editor’s displayed number are informative rather than promises in the presence of another worker.

Use a same-directory temporary file, flush, `os.fsync`, and `os.replace`:

```python
def _atomic_write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{secrets.token_hex(6)}.tmp")
    try:
        with temp.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()
```

`DailyIssueStore` must use a module-level `threading.RLock` shared by every store instance. On macOS/Linux it also holds an exclusive `fcntl.flock` on `<root>/.daily-issues.lock` around publish/revise so two Flask workers cannot both accept the same revision. Archive the current valid issue to `revisions/YYYY-MM-DD-rNN.json` before replacing it and reject a stale `expected_revision`. The `get()` contract is exact: a nonexistent date returns `None`; a malformed current file with a valid archive returns the newest valid archive when `fallback_revision=True`; a malformed current file without a valid archive raises `DailyIssueCorrupt`. `assert_revisable()` reads the target current file without fallback and returns it only when valid; missing or malformed current state raises a domain error even if public `get()` can show an archived fallback. `revise()` calls the same strict check under the exclusive lock and never overwrites damaged evidence.

The stored payload is exactly:

```python
{
    "schema_version": 1,
    "issue_date": issue_date,
    "issue_number": issue_number,
    "status": "published",
    "revision": revision,
    "published_at": published_at,
    "revised_at": revised_at,
    "timezone": self.timezone_name,
    "topics": validated_topics,
    "attention": validated_attention,
}
```

On revision, preserve the original `published_at`, `issue_date`, and `issue_number`; set only `revised_at` to the injected current time and increment `revision` by one. On first publication, `published_at == revised_at` and `revision == 1`.

- [ ] **Step 4: Add rollback and malformed-file tests**

Extend `blog/test_daily_issues.py` to:

- patch `daily_issues.os.replace` so replacing the current issue raises, then assert the previous issue still loads;
- corrupt current JSON and assert `get(..., fallback_revision=True)` returns the newest valid archive;
- assert `list_issues()`, `latest()`, and `next_issue_number()` also use that archived fallback;
- assert `assert_revisable()` still rejects the damaged current snapshot, and a failed revision leaves both current bytes and fallback archive unchanged;
- corrupt a first revision with no archive and assert preview/new publish raise `DailyIssueCorrupt` instead of reusing its issue number;
- directly assert `get(corrupt_date)` raises `DailyIssueCorrupt` when no valid archive exists;
- assert `unrecoverable_dates()` reports that date while returning an empty list for a corrupt current snapshot that has a valid revision fallback;
- assert zero topics and four topics raise `DailyIssueValidationError`;
- assert each text field accepts exactly its hard limit and rejects limit + 1; 35/25-character titles remain valid because those are layout warnings, not persistence failures;
- assert `2026-02-30` is rejected;
- assert `preview()` returns a renderable provisional issue but creates no issue or revision file;
- assert `next_issue_number()` is `1` when empty and advances only after first publication of a new date;
- assert two same-publisher sources count as one independent public source even if both evidence links are retained;
- assert first publication rejects a topic whose sources are all `unchecked`, while revision may mark an existing readable source `unavailable`;
- assert replacing a topic during revision still requires one readable source and cannot rely only on newly added unchecked evidence;
- assert publishing a second date increments `issue_number` and `latest()` chooses that date;
- create two store instances for the same root, submit revisions with the same `expected_revision`, and assert exactly one succeeds while the other raises `DailyIssueConflict`.

- [ ] **Step 5: Run focused tests**

```bash
blog/.venv/bin/python blog/test_daily_issues.py
PYTHONDONTWRITEBYTECODE=1 blog/.venv/bin/python -m py_compile \
  blog/daily_issues.py blog/test_daily_issues.py
```

Expected: tests print `全部通过 ✅`; compilation exits 0.

- [ ] **Step 6: Commit the issue store**

```bash
git add blog/daily_issues.py blog/test_daily_issues.py
git commit -m "feat: persist dated daily brief revisions"
```

---

### Task 3: Single-Administrator Authentication and Mutation Protection

**Files:**
- Create: `blog/admin_auth.py`
- Create: `blog/templates/admin_login.html`
- Create: `blog/test_admin_routes.py`
- Modify: `blog/config.py:3-21`
- Modify: `blog/app.py:5-60, 461-524`
- Modify: `blog/test_app_routes.py:78-111`

**Interfaces:**
- Consumes: `BLOG_ADMIN_PASSWORD` and `SECRET_KEY` loaded from `config/.env` before `Config` import.
- Produces:
  - `is_admin() -> bool`
  - `login_admin(password: str) -> bool`
  - `logout_admin() -> None`
  - `csrf_token() -> str`
  - `validate_csrf() -> None`
  - `admin_required(view)`
  - routes `GET|POST /admin/login`, `POST /admin/logout`
- Existing write routes `/ingest`, `/ingest/status`, and `/signal/attention` become administrator-only; `/track` remains public and non-blocking.

- [ ] **Step 1: Write failing authentication and permission tests**

Create `blog/test_admin_routes.py` with a temporary app configuration:

```python
"""Administrator route tests.

Run: blog/.venv/bin/python blog/test_admin_routes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import app


def configured_client():
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-not-for-production",
        BLOG_ADMIN_PASSWORD="correct horse",
    )
    return app.test_client()


def test_admin_json_route_rejects_anonymous_user():
    client = configured_client()
    response = client.post("/signal/attention", json={"action": "dismiss", "item_id": "x"})
    assert response.status_code == 401


def test_login_uses_csrf_and_creates_admin_session():
    client = configured_client()
    page = client.get("/admin/login")
    assert page.status_code == 200
    with client.session_transaction() as session:
        token = session["admin_csrf"]
    bad = client.post("/admin/login", data={"password": "wrong", "csrf_token": token})
    assert bad.status_code == 401
    good = client.post("/admin/login", data={"password": "correct horse", "csrf_token": token})
    assert good.status_code == 302
    with client.session_transaction() as session:
        assert session["daily_admin"] is True


def test_admin_post_rejects_missing_csrf_after_login():
    client = configured_client()
    with client.session_transaction() as session:
        session["daily_admin"] = True
        session["admin_csrf"] = "known-token"
    response = client.post("/signal/attention", json={"action": "dismiss", "item_id": "x"})
    assert response.status_code == 403
```

At this task boundary, add a table-driven permission matrix for the existing `POST /ingest`, `GET /ingest/status`, and `POST /signal/attention` routes. Each must return 401 without performing its underlying mutation. After injecting an admin session, every existing POST (including logout) must return 403 without CSRF and may proceed only with the known token. Keep a separate regression proving public `/track` still accepts telemetry without an admin session; it is intentionally not a privileged mutation. Task 6 extends the same matrix when the daily admin routes exist.

Add a `__main__` block that runs all tests and prints `全部通过 ✅`.

- [ ] **Step 2: Run the authentication test and verify it fails**

```bash
blog/.venv/bin/python blog/test_admin_routes.py
```

Expected: FAIL because anonymous `/signal/attention` currently returns 200/400 instead of 401 and `/admin/login` does not exist.

- [ ] **Step 3: Add explicit security configuration**

Extend `blog/config.py`:

```python
from pathlib import Path


ROOT = Path(__file__).parent.parent


class Config:
    # existing fields remain
    BLOG_ADMIN_PASSWORD = os.getenv("BLOG_ADMIN_PASSWORD", "")
    BLOG_TIMEZONE = os.getenv("BLOG_TIMEZONE", "America/Los_Angeles")
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    DAILY_ISSUES_DIR = os.getenv(
        "DAILY_ISSUES_DIR", str(ROOT / "blog" / "data" / "daily_issues")
    )
    DAILY_EDITOR_LOG = os.getenv(
        "DAILY_EDITOR_LOG", str(ROOT / "blog" / "data" / "daily_editor_events.jsonl")
    )
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "").lower() == "true"
```

Keep a local development fallback for `SECRET_KEY`, but add a startup guard in `blog/app.py`: if `BLOG_ADMIN_PASSWORD` is non-empty and `SECRET_KEY` equals the repository fallback, raise `RuntimeError("set a private SECRET_KEY before enabling admin login")`. Route tests set a private key before exercising login.

- [ ] **Step 4: Implement session, password, CSRF, and decorator helpers**

Create `blog/admin_auth.py`:

```python
import hmac
import secrets
from functools import wraps

from flask import abort, current_app, jsonify, redirect, request, session, url_for


def is_admin():
    return session.get("daily_admin") is True


def csrf_token():
    token = session.get("admin_csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        session["admin_csrf"] = token
    return token


def login_admin(password):
    expected = str(current_app.config.get("BLOG_ADMIN_PASSWORD") or "")
    valid = bool(expected) and hmac.compare_digest(str(password or ""), expected)
    if valid:
        session.clear()
        session["daily_admin"] = True
        session["admin_csrf"] = secrets.token_urlsafe(32)
    return valid


def logout_admin():
    session.clear()


def validate_csrf():
    supplied = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token") or ""
    expected = session.get("admin_csrf") or ""
    if not expected or not hmac.compare_digest(str(supplied), str(expected)):
        abort(403)


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not is_admin():
            if request.path.startswith(("/admin/", "/ingest", "/signal/")) or request.is_json:
                return jsonify({"status": "unauthorized"}), 401
            return redirect(url_for("admin_login", next=request.full_path))
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            validate_csrf()
        return view(*args, **kwargs)
    return wrapped
```

- [ ] **Step 5: Add login/logout routes and protect all existing mutations**

In `blog/app.py`, import the module and add:

```python
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_auth.validate_csrf()
        if not admin_auth.login_admin(request.form.get("password", "")):
            return render_template("admin_login.html", error="密码不正确", csrf_token=admin_auth.csrf_token()), 401
        return redirect(url_for("index"))
    return render_template("admin_login.html", error="", csrf_token=admin_auth.csrf_token())


@app.post("/admin/logout")
@admin_auth.admin_required
def admin_logout():
    admin_auth.logout_admin()
    return redirect(url_for("index"))
```

Change `/ingest` to POST-only and decorate `/ingest`, `/ingest/status`, and `/signal/attention` with `@admin_auth.admin_required`. Update any existing admin-side fetch to send `X-CSRF-Token`. Do not protect `/track`, `/search`, `/article`, or cover routes.

Add `Cache-Control: no-store` to `/admin/*`, `/ingest*`, and `/signal/attention` responses so authenticated draft data and CSRF-bearing pages are not cached. Add a route test for the header. Keep login failure responses generic and document reverse-proxy rate limiting for `/admin/login` in deployment notes; do not add a process-local limiter that would give false protection across workers.

- [ ] **Step 6: Add the login template**

Create `blog/templates/admin_login.html` extending `base.html`, with a native password input, hidden CSRF input, visible error text, and no password echo:

```html
{% extends "base.html" %}
{% block title %}管理员登录 · 降噪{% endblock %}
{% block content %}
<section class="admin-login" aria-labelledby="adminLoginTitle">
  <h1 id="adminLoginTitle">管理员登录</h1>
  {% if error %}<p class="admin-login-error" role="alert">{{ error }}</p>{% endif %}
  <form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <label>密码 <input type="password" name="password" required autocomplete="current-password"></label>
    <button type="submit">登录</button>
  </form>
</section>
{% endblock %}
```

- [ ] **Step 7: Run auth and route regressions**

```bash
blog/.venv/bin/python blog/test_admin_routes.py
blog/.venv/bin/python blog/test_app_routes.py
PYTHONDONTWRITEBYTECODE=1 blog/.venv/bin/python -m py_compile \
  blog/admin_auth.py blog/app.py blog/config.py blog/test_admin_routes.py
```

Expected: all tests pass. Update `test_missing_attention_promote_does_not_write_positive_log()` to authenticate and include CSRF when it is testing behavior; add a separate anonymous 401 assertion.

- [ ] **Step 8: Commit the security boundary**

```bash
git add blog/admin_auth.py blog/templates/admin_login.html blog/test_admin_routes.py blog/config.py blog/app.py blog/test_app_routes.py
git commit -m "feat: secure daily brief administration"
```

---

### Task 4: Public Latest Issue, Stable Date Routes, and Archive

**Files:**
- Create: `blog/test_daily_routes.py`
- Create: `blog/templates/_daily_brief.html`
- Create: `blog/templates/_daily_topic_card.html`
- Create: `blog/templates/_daily_attention.html`
- Create: `blog/templates/daily.html`
- Create: `blog/templates/daily_archive.html`
- Create: `blog/templates/daily_unavailable.html`
- Modify: `blog/app.py:257-298`
- Modify: `blog/templates/base.html:1-36`
- Modify: `blog/templates/index.html:1-80`
- Modify: `blog/test_app_routes.py:17-40`

**Interfaces:**
- Consumes: `DailyIssueStore.latest()`, `DailyIssueStore.get()`, and `DailyIssueStore.list_issues()` from Task 2.
- Produces routes:
  - `GET /` — latest published issue plus unchanged deep library.
  - `GET /daily` — date-descending archive.
  - `GET /daily/<YYYY-MM-DD>` — stable issue snapshot.
- Produces public template contract: `issue`, `daily_error`, `is_home`, `is_current_day`, `canonical_url`, `og_image_url`, `share_text`, `is_admin`, `admin_action`, `admin_target_date`, and `current_issue_date`. Task 6 extends the authenticated-only context with `csrf_token`, `draft_available`, and `draft_message`. Drafts and candidates are never passed to anonymous templates.

- [ ] **Step 1: Write failing public route tests**

Create `blog/test_daily_routes.py`. Use `TemporaryDirectory`, set `app.config["DAILY_ISSUES_DIR"]`, publish two fixtures with `DailyIssueStore`, and restore config in `finally`. Every test patches `app._local_now()` to an explicit aware `America/Los_Angeles` datetime; no test may depend on the wall-clock day when the plan is executed:

```python
def test_home_uses_latest_published_issue_not_signal_cache():
    client, store = issue_client()
    publish_fixture(store, "2026-07-10", "旧主题")
    publish_fixture(store, "2026-07-11", "最新主题")
    response = client.get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "最新主题" in html
    assert "旧主题" not in html
    assert "AI HOT" not in html
    assert "加入首页判断" not in html
    assert "先不加" not in html


def test_dated_issue_is_stable_and_uses_historical_wording():
    client, store = issue_client()
    publish_fixture(store, "2026-07-10", "固定主题")
    response = client.get("/daily/2026-07-10")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "这一天，哪些讨论值得知道？" in html
    assert '<link rel="canonical" href="https://noise.example/daily/2026-07-10">' in html


def test_archive_is_descending_and_unknown_date_is_404():
    client, store = issue_client()
    publish_fixture(store, "2026-07-10", "十号")
    publish_fixture(store, "2026-07-11", "十一号")
    html = client.get("/daily").get_data(as_text=True)
    assert html.index("2026-07-11") < html.index("2026-07-10")
    assert client.get("/daily/2026-02-30").status_code == 404
    assert client.get("/daily/2026-07-09").status_code == 404


def test_no_published_issue_keeps_deep_library_available():
    client, _store = issue_client()
    html = client.get("/").get_data(as_text=True)
    assert "还没有发布第一期" in html
    assert 'id="deep-library"' in html


def test_old_latest_is_labeled_and_published_snapshot_does_not_drift():
    client, store = issue_client(now="2026-07-12T09:00:00-07:00")
    publish_fixture(store, "2026-07-11", "稳定主题")
    first = client.get("/").get_data(as_text=True)
    write_isolated_signal_cache(title="不应该上首页的新主题")
    second = client.get("/").get_data(as_text=True)
    assert "最新一期 · 2026.07.11" in second
    assert "这一天，哪些讨论值得知道？" in second
    assert "稳定主题" in first and "稳定主题" in second
    assert "不应该上首页的新主题" not in second


def test_home_falls_back_to_archived_revision_when_current_json_is_corrupt():
    client, store = issue_client()
    publish_and_revise_fixture(store, "2026-07-11", "修订前", "修订后")
    corrupt_current_issue(store, "2026-07-11")
    html = client.get("/").get_data(as_text=True)
    assert "修订前" in html
    assert "修订后" not in html


def test_unrecoverable_dated_issue_is_friendly_503_not_404():
    client, store = issue_client()
    publish_fixture(store, "2026-07-11", "已损坏")
    corrupt_current_issue(store, "2026-07-11")
    response = client.get("/daily/2026-07-11")
    assert response.status_code == 503
    assert "这期简报暂时无法读取" in response.get_data(as_text=True)


def test_only_corrupt_first_issue_is_not_misreported_as_never_published():
    client, store = issue_client()
    publish_fixture(store, "2026-07-11", "唯一一期")
    corrupt_current_issue(store, "2026-07-11")
    html = client.get("/").get_data(as_text=True)
    assert "最新一期暂时无法读取" in html
    assert "还没有发布第一期" not in html
    assert 'id="deep-library"' in html
```

Set `PUBLIC_BASE_URL="https://noise.example"`, `BLOG_TIMEZONE="America/Los_Angeles"`, and patch `load_archive_records()` to a small deterministic fixture so the tests never scan the real archive. Patch `today_signal.SIGNAL_CACHE` to a file inside the same temporary test directory before writing the drift fixture; never touch real `blog/data/`.

- [ ] **Step 2: Run the route test and verify it fails**

```bash
blog/.venv/bin/python blog/test_daily_routes.py
```

Expected: FAIL because `DailyIssueStore` is not connected to `/`, and `/daily` routes do not exist.

- [ ] **Step 3: Add store and URL view helpers to Flask**

In `blog/app.py`, add:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

import admin_auth
from daily_issues import (
    DailyIssueCorrupt,
    DailyIssueStore,
    format_share_text,
    validate_issue_date,
)


def _issue_store():
    return DailyIssueStore(
        Path(app.config["DAILY_ISSUES_DIR"]),
        app.config["BLOG_TIMEZONE"],
    )


def _local_now():
    return datetime.now(ZoneInfo(app.config["BLOG_TIMEZONE"]))


def _stable_issue_url(issue_date):
    base = str(app.config.get("PUBLIC_BASE_URL") or "").rstrip("/")
    if base:
        return f"{base}/daily/{issue_date}"
    return url_for("daily_issue", issue_date=issue_date, _external=True)


def _issue_view(issue, *, is_home, daily_error=""):
    today = _local_now().date().isoformat()
    issue_date = issue.get("issue_date") if issue else ""
    canonical = _stable_issue_url(issue_date) if issue_date else ""
    admin = admin_auth.is_admin()
    admin_action = "publish" if is_home and issue_date != today else ("revise" if issue else "publish")
    admin_target_date = issue_date if admin_action == "revise" else today
    public_base = str(app.config.get("PUBLIC_BASE_URL") or request.url_root).rstrip("/")
    return {
        "issue": issue,
        "daily_error": daily_error,
        "is_home": is_home,
        "is_current_day": issue_date == today,
        "canonical_url": canonical,
        "og_image_url": f"{public_base}/static/og-daily.png",
        "share_text": format_share_text(issue, canonical) if issue else "",
        "is_admin": admin,
        "admin_action": admin_action,
        "admin_target_date": admin_target_date,
        "current_issue_date": today,
    }
```

Import `url_for` from Flask. `PUBLIC_BASE_URL` is mandatory for external deployment; request-host fallback exists only for local development.

- [ ] **Step 4: Replace the public `/` signal cache read with latest issue read**

Keep the existing archive/topic/verdict context calculation in `index()`, but remove the public `breaking/signals/attention/signal_meta` read at `blog/app.py:276-298`. Instead:

```python
store = _issue_store()
issue = store.latest()
unrecoverable = store.unrecoverable_dates()
daily_error = ""
if unrecoverable and (not issue or max(unrecoverable) >= issue["issue_date"]):
    issue = None
    daily_error = "最新一期暂时无法读取，请稍后再试。"
return render_template(
    "index.html",
    records=records,
    topics=used_topics,
    topic_counts=topic_counts,
    verdicts=verdicts,
    **_issue_view(issue, is_home=True, daily_error=daily_error),
)
```

Do not expose `today_signal.read_signal_cache()` in anonymous view context.

- [ ] **Step 5: Add dated and archive routes**

```python
@app.get("/daily")
def daily_archive():
    return render_template("daily_archive.html", issues=_issue_store().list_issues())


@app.get("/daily/<issue_date>")
def daily_issue(issue_date):
    try:
        validate_issue_date(issue_date)
    except ValueError:
        abort(404)
    try:
        issue = _issue_store().get(issue_date)
    except DailyIssueCorrupt:
        app.logger.exception("daily issue snapshot is corrupt")
        return render_template("daily_unavailable.html", issue_date=issue_date), 503
    if not issue:
        abort(404)
    return render_template("daily.html", **_issue_view(issue, is_home=False))
```

`daily.html` is the stable issue-only page; it does not need to repeat the mutable deep-content grid. The `/` page keeps the existing deep library immediately below the daily brief.

`daily_unavailable.html` extends `base.html`, gives the reader the dated issue URL and the message `这期简报暂时无法读取，请稍后再试。`, and links back to the latest valid homepage. It contains no exception text, path, recovery action, or admin data.

- [ ] **Step 6: Add public templates without styling or management data**

Add these blocks to `base.html` exactly once: `body_class` on `<body class="...">`; `extra_styles` and `extra_head` after the legacy stylesheet; `header_actions` after public navigation; and `scripts` immediately before `</body>`. Keep the existing global deep-library card script outside the child `scripts` block so a page override cannot remove it. `index.html`, `daily.html`, `daily_archive.html`, and `daily_unavailable.html` set `body_class` to `daily-page`. `daily.html` and `index.html` use the same partial:

```html
{% include "_daily_brief.html" %}
```

In `index.html`, wrap the existing filter and card grid in `<section id="deep-library" aria-labelledby="deepLibraryTitle">`, add a small `深度内容库` heading, and leave the existing `.home-filter`, `#card-grid`, `_card.html`, pocket-search, and filter JavaScript unchanged inside it.

`_daily_brief.html` must render:

```html
<section class="daily-brief" aria-labelledby="dailyTitle">
  {% if daily_error %}
  <div class="daily-empty daily-error" role="status">
    <h1 id="dailyTitle">最新一期暂时无法读取</h1>
    <p>{{ daily_error }}</p>
  </div>
  {% elif issue %}
  <header class="daily-masthead">
    <p class="daily-edition">{% if is_home and not is_current_day %}最新一期 · {% endif %}{{ issue.issue_date|replace('-', '.') }} · 第 {{ '%03d'|format(issue.issue_number) }} 期</p>
    <h1 id="dailyTitle">{% if is_current_day and is_home %}今天{% else %}这一天{% endif %}，哪些讨论值得知道？</h1>
    <p>不是热搜榜。把重复消息合并后，只留下可能影响下一步判断的变化。</p>
    <span>{% if issue.topics|length < 3 %}{% if is_current_day and is_home %}今天{% else %}这一天{% endif %}仅有 {{ issue.topics|length }} 个主题达到标准 · 不凑数{% else %}留下 3 个主题 · 不凑数{% endif %}{% if issue.revision > 1 %} · 最后修订 {{ issue.revised_at[11:16] }}{% endif %}</span>
  </header>
  <div class="daily-topic-grid daily-topic-count-{{ issue.topics|length }}">
    {% for topic in issue.topics %}
      {% include "_daily_topic_card.html" %}
    {% endfor %}
  </div>
  {% include "_daily_attention.html" %}
  {% else %}
  <div class="daily-empty">
    <h1 id="dailyTitle">还没有发布第一期</h1>
    <p>第一期发布后，这里会出现当天最值得知道的讨论。</p>
  </div>
  {% endif %}
</section>
```

`_daily_topic_card.html` uses `.daily-topic`, never `.card` or `.signal-*`, so the existing global card click script and legacy CSS cannot capture it. Sources use native `<details>` and show the merged count only when `independent_source_count >= 2`.

`_daily_attention.html` is read-only and contains no buttons. `daily_archive.html` lists stable date URLs newest-first.

- [ ] **Step 7: Add canonical and Open Graph metadata**

In `daily.html` and `index.html`, set the `title` block and fill `extra_head` only when `issue` exists:

```html
{% block title %}{% if issue %}降噪｜{{ issue.issue_date }} 值得知道的讨论{% else %}降噪{% endif %}{% endblock %}
<link rel="canonical" href="{{ canonical_url }}">
<meta name="description" content="{{ issue.topics[0].why_ranked }}">
<meta property="og:type" content="article">
<meta property="og:title" content="降噪｜{{ issue.issue_date }} 值得知道的讨论">
<meta property="og:description" content="{{ issue.topics[0].why_ranked }}">
<meta property="og:url" content="{{ canonical_url }}">
<meta property="og:image" content="{{ og_image_url }}">
```

Until a dedicated image is created, add `blog/static/og-daily.png` in Task 5 from the approved brand assets; never point to a missing file.

Extend the dated-route test to assert the HTML `<title>`, standard description meta, canonical URL, and OG URL all contain the same stable issue date; none may use `/` as the canonical share target.

- [ ] **Step 8: Run routes and existing regressions**

```bash
blog/.venv/bin/python blog/test_daily_routes.py
blog/.venv/bin/python blog/test_app_routes.py
blog/.venv/bin/python blog/test_today_signal.py
```

Expected: all pass. Replace old `test_homepage_shows_missing_signal_state_when_cache_absent()` with the “no published issue keeps deep library” semantics.

- [ ] **Step 9: Commit public issue routing**

```bash
git add blog/app.py blog/test_app_routes.py blog/test_daily_routes.py \
  blog/templates/base.html blog/templates/index.html blog/templates/daily.html \
  blog/templates/daily_archive.html blog/templates/_daily_brief.html \
  blog/templates/daily_unavailable.html blog/templates/_daily_topic_card.html \
  blog/templates/_daily_attention.html
git commit -m "feat: serve stable daily brief editions"
```

---

### Task 5: Approved Card Visual System, Brand Header, and Share Copy

**Files:**
- Create: `blog/static/css/daily.css`
- Create: `blog/static/js/daily.js`
- Create: `blog/static/og-daily.svg`
- Generate: `blog/static/og-daily.png`
- Create: `blog/test_daily_templates.py`
- Modify: `blog/templates/base.html:1-36`
- Modify: `blog/templates/index.html:1-103`
- Modify: `blog/templates/daily.html`
- Modify: `blog/templates/daily_archive.html`
- Modify: `blog/templates/daily_unavailable.html`
- Modify: `blog/templates/_daily_brief.html`
- Modify: `blog/templates/_daily_topic_card.html`
- Modify: `blog/templates/_daily_attention.html`
- Modify: `blog/static/favicon.svg:1-4`

**Interfaces:**
- Consumes: public template contract from Task 4 and server-generated `share_text`.
- Produces:
  - `.daily-topic-grid` with count-aware 1/2/3 layouts.
  - `#dailyCopyButton` and `<script id="dailySharePayload" type="application/json">`.
  - `daily.js` copy behavior with clipboard and textarea fallback.
  - fused blue/red multi-in/one-out NoiseFilter mark shared by header, favicon, and OG art.

- [ ] **Step 1: Write failing public template tests**

Create `blog/test_daily_templates.py` using `app.test_request_context()` and `render_template()`:

```python
def render_brief(issue, *, is_home=True, is_current_day=True):
    with app.test_request_context("/"):
        return render_template(
            "_daily_brief.html", issue=issue,
            is_home=is_home, is_current_day=is_current_day,
        )


def test_three_topics_render_one_lead_and_two_side_cards():
    issue = issue_fixture(topic_count=3)
    with app.test_request_context("/"):
        html = render_template(
            "_daily_brief.html",
            issue=issue,
            is_home=True,
            is_current_day=True,
        )
    assert 'class="daily-topic-grid daily-topic-count-3"' in html
    assert html.count('class="daily-topic ') == 3
    assert "daily-topic-rank-1" in html
    assert "daily-topic-rank-2" in html
    assert "daily-topic-rank-3" in html
    assert "2 个相关来源已合并" in html
    assert "2026.07.11" in html


def test_single_source_does_not_claim_sources_were_merged():
    issue = issue_fixture(topic_count=1, source_count=1)
    with app.test_request_context("/"):
        html = render_template("_daily_brief.html", issue=issue, is_home=True, is_current_day=True)
    assert "相关来源已合并" not in html
    assert "Official" in html


def test_public_template_contains_no_management_payload():
    issue = issue_fixture(topic_count=3)
    with app.test_request_context("/"):
        html = render_template("_daily_brief.html", issue=issue, is_home=True, is_current_day=True)
    assert "发布今日" not in html
    assert "修订本期" not in html
    assert "data-candidates" not in html
    assert "加入首页判断" not in html


def test_one_and_two_topic_states_do_not_render_phantom_slots():
    one = render_brief(issue_fixture(topic_count=1, attention=[]))
    assert "daily-topic-count-1" in one
    assert one.count('class="daily-topic ') == 1
    assert "今天仅有 1 个主题达到标准" in one
    assert "daily-attention" not in one
    two = render_brief(issue_fixture(topic_count=2, attention=[]))
    assert "daily-topic-count-2" in two
    assert two.count('class="daily-topic ') == 2
    assert "daily-topic-rank-3" not in two
    assert "今天仅有 2 个主题达到标准" in two
```

The fixture uses actual topic/source keys from the approved issue schema. Add a `__main__` runner and success output.

- [ ] **Step 2: Run template tests and verify they fail**

```bash
blog/.venv/bin/python blog/test_daily_templates.py
```

Expected: FAIL because the final card classes and source-display rules are not implemented.

- [ ] **Step 3: Implement the fused header mark and navigation slots**

In `base.html`, replace the old orange `降` square with inline SVG:

```html
<a href="{{ url_for('index') }}" class="logo" aria-label="降噪首页">
  <svg class="logo-mark" viewBox="0 0 36 36" aria-hidden="true">
    <circle cx="18" cy="18" r="16" fill="#E9F5FC"/>
    <path d="M7 11h8M7 16h12M7 21h9M7 26h6" stroke="#2E9FE6" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M20 10l6 8-6 8" fill="none" stroke="#17191C" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="28" cy="18" r="3" fill="#E85C55"/>
  </svg>
  <span class="logo-text">降噪</span>
  <span class="logo-en">NOISE<br>FILTER</span>
</a>
```

Add nav links for `往期简报` (`url_for('daily_archive')`), `深度内容库` (`url_for('index') ~ '#deep-library'`), and `搜索` (`url_for('search')`), then use the block contract established in Task 4. Keep the global deep-library card script intact.

Update `favicon.svg` to use the same paths and colors; do not use the old orange square or a Doraemon face/bell.

- [ ] **Step 4: Finish the public topic and attention markup**

`_daily_topic_card.html` must render these fields with semantic elements:

```html
<article class="daily-topic daily-topic-rank-{{ topic.rank }}" aria-labelledby="topic-{{ topic.topic_id }}">
  <div class="daily-topic-meta">
    <span class="daily-rank">{{ topic.rank }}</span>
    {% if topic.independent_source_count >= 2 %}
      <span class="daily-source-count">{{ topic.independent_source_count }} 个相关来源已合并</span>
    {% elif topic.sources %}
      <span class="daily-source-count">{{ topic.sources[0].publisher }}</span>
    {% endif %}
    {% if topic.category %}<span>{{ topic.category }}</span>{% endif %}
  </div>
  <h2 id="topic-{{ topic.topic_id }}">{{ topic.title }}</h2>
  <p class="daily-what">{{ topic.what_happened }}</p>
  {% if topic.rank == 1 and topic.discussion_focus %}
  <div class="daily-focus" aria-label="大家主要在讨论">
    <strong>大家主要在讨论</strong>
    <ul>{% for focus in topic.discussion_focus[:3] %}<li>{{ focus }}</li>{% endfor %}</ul>
  </div>
  {% endif %}
  <p class="daily-why"><span>为什么上榜</span>{{ topic.why_ranked }}</p>
  {% if topic.sources %}
  <details class="daily-evidence">
    <summary>查看依据</summary>
    <ul>{% for source in topic.sources %}<li>{% if source.verification_status == 'unavailable' %}<span>{{ source.publisher }} · {{ source.title }}（来源暂不可访问）</span>{% else %}<a href="{{ source.url }}" target="_blank" rel="noopener">{{ source.publisher }} · {{ source.title }}</a>{% endif %}</li>{% endfor %}</ul>
  </details>
  {% endif %}
</article>
```

`_daily_attention.html` renders nothing when `issue.attention` is empty. Otherwise it renders only title, one-sentence state, and `讨论上升中 / 继续观察 / 讨论稳定`; no action buttons or hidden management fields.

- [ ] **Step 5: Implement the approved desktop and mobile CSS in an isolated file**

Create `blog/static/css/daily.css` and load it once from `base.html` immediately after the legacy stylesheet because the fused logo and public navigation exist on every route. Put only the small global brand/header selectors (`.logo-mark`, `.logo-en`, `.site-nav`) outside the daily namespace; all page layout/color rules stay under `.daily-*` or `body.daily-page`, so article and search pages do not inherit the homepage. `index.html`, `daily.html`, `daily_archive.html`, and `daily_unavailable.html` each set `body_class` to `daily-page`. Keep `extra_styles` for authenticated `admin-daily.css`. The essential rules are:

```css
body.daily-page { background: #f7f3ed; color: #181a1d; }
.daily-brief { max-width: 1180px; margin: 0 auto 24px; }
.daily-masthead { padding: 28px 34px 22px; border-bottom: 1px solid #ddd7cf; }
.daily-masthead h1 { margin: 7px 0; font: 900 40px/1.08 var(--font-serif); letter-spacing: -.055em; }
.daily-topic-grid { display: grid; grid-template-columns: minmax(0, 1.44fr) minmax(280px, .8fr); gap: 12px; padding: 22px 0; }
.daily-topic { border: 1px solid #ddd6cd; border-radius: 15px; background: #fffdfa; padding: 17px; }
.daily-topic-rank-1 { grid-column: 1; grid-row: 1 / span 2; min-height: 276px; padding: 22px; background: #f0ddd0; border-color: #dfbba7; }
.daily-topic-rank-2 { grid-column: 2; grid-row: 1; }
.daily-topic-rank-3 { grid-column: 2; grid-row: 2; }
.daily-topic-count-1 { grid-template-columns: 1fr; }
.daily-topic-count-1 .daily-topic-rank-1 { grid-column: 1; grid-row: 1; }
.daily-topic-count-2 { grid-template-columns: minmax(0, 1.44fr) minmax(280px, .8fr); align-items: start; }
.daily-topic-count-2 .daily-topic-rank-2 { grid-column: 2; grid-row: 1; }
.daily-rank { display: inline-grid; place-items: center; width: 22px; height: 22px; border-radius: 50%; background: #191b1e; color: #fff; font-weight: 900; }
.daily-topic-rank-1 h2 { font: 850 28px/1.25 var(--font-serif); }
.daily-topic-rank-2 h2, .daily-topic-rank-3 h2 { font: 850 18px/1.3 var(--font-serif); }
.daily-topic h2, .daily-source-count, .daily-evidence a { overflow-wrap: anywhere; }
.daily-topic-rank-1 h2 { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; }
.daily-topic-rank-2 h2, .daily-topic-rank-3 h2 { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; }
.daily-topic-rank-2 .daily-what, .daily-topic-rank-3 .daily-what,
.daily-topic-rank-2 .daily-why, .daily-topic-rank-3 .daily-why { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; }
.daily-why { border-top: 1px solid rgba(139,88,58,.22); padding-top: 11px; color: #9b4b30; }
.daily-attention { margin-top: 4px; padding: 18px 20px; border: 1px solid #d8d1c8; border-radius: 14px; background: #ebe7e1; }
@media (max-width: 760px) {
  .daily-masthead { padding: 24px 18px 18px; }
  .daily-masthead h1 { font-size: 32px; }
  .daily-topic-grid, .daily-topic-count-2 { grid-template-columns: 1fr; padding: 18px; }
  .daily-topic-rank-1, .daily-topic-rank-2, .daily-topic-rank-3 { grid-column: 1; grid-row: auto; min-height: 0; }
}
@media (prefers-reduced-motion: reduce) {
  .daily-page *, .daily-page *::before, .daily-page *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; animation-duration: .01ms !important; }
}
```

Do not place these rules at the end of the 4,000-line legacy stylesheet. Namespaced CSS prevents legacy `.signals`, `.signal-*`, and `.card` overrides.

- [ ] **Step 6: Implement copy-current-issue behavior**

In `index.html` and `daily.html`, render the button and JSON only when `issue` exists:

```html
<button id="dailyCopyButton" type="button">复制本期 ↗</button>
<script id="dailySharePayload" type="application/json">{{ {'text': share_text}|tojson }}</script>
```

Create `blog/static/js/daily.js`:

```javascript
(function () {
  const button = document.getElementById('dailyCopyButton');
  const payload = document.getElementById('dailySharePayload');
  if (!button || !payload) return;
  const text = JSON.parse(payload.textContent || '{}').text || '';
  async function copy(value) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(value);
    const area = document.createElement('textarea');
    area.value = value;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand('copy');
    area.remove();
    if (!ok) throw new Error('copy failed');
  }
  button.addEventListener('click', async function () {
    try {
      await copy(text);
      button.textContent = '已复制';
    } catch (_error) {
      button.textContent = '复制失败，请重试';
    }
    window.setTimeout(function () { button.textContent = '复制本期 ↗'; }, 1600);
  });
})();
```

- [ ] **Step 7: Create a real OG image from the approved brand mark**

Create a 1200×630 `blog/static/og-daily.svg` using the same warm background, fused logo, `降噪每日简报`, and the date-neutral line `哪些讨论值得知道？`. The same image is reused by historical date pages, so it must not say `今天`. Convert it mechanically on macOS:

```bash
sips -s format png blog/static/og-daily.svg --out blog/static/og-daily.png
file blog/static/og-daily.png
```

Expected: `PNG image data, 1200 x 630`. If `sips` cannot render SVG on the execution machine, use headless Chrome to open the SVG and capture exactly 1200×630; do not substitute an unrelated image.

- [ ] **Step 8: Run template and JavaScript checks**

```bash
blog/.venv/bin/python blog/test_daily_templates.py
blog/.venv/bin/python blog/test_daily_routes.py
node --check blog/static/js/daily.js
```

Expected: Python tests pass and Node exits 0 without output.

- [ ] **Step 9: Commit the approved public visual system**

```bash
git add blog/templates/base.html blog/templates/index.html blog/templates/daily.html \
  blog/templates/daily_archive.html blog/templates/daily_unavailable.html \
  blog/templates/_daily_brief.html blog/templates/_daily_topic_card.html \
  blog/templates/_daily_attention.html blog/static/css/daily.css \
  blog/static/js/daily.js blog/static/favicon.svg blog/static/og-daily.svg \
  blog/static/og-daily.png blog/test_daily_templates.py
git commit -m "feat: render the NoiseFilter daily card homepage"
```

---

### Task 6: Trusted Admin Selection and Publish/Revise APIs

**Files:**
- Create: `blog/daily_editor.py`
- Create: `blog/test_daily_editor.py`
- Modify: `blog/app.py:257-298, 461-548`
- Modify: `blog/test_admin_routes.py`

**Interfaces:**
- Consumes: Task 1 `daily_draft`, Task 2 `DailyIssueStore`, Task 3 admin + CSRF, and Task 4 partial templates.
- Produces:
  - `trusted_draft(cache: dict, *, expected_date: str) -> dict`
  - `revision_draft(published_issue: dict, current_draft: dict | None = None) -> dict`
  - `apply_selection(draft: dict, rows: list[dict]) -> list[dict]`
  - `append_editor_event(path: Path, event: dict, *, now: datetime) -> None`
  - `GET /admin/daily/draft?date=YYYY-MM-DD`
  - `POST /admin/daily/<issue_date>/preview`
  - `POST /admin/daily/<issue_date>/publish`
  - `POST /admin/daily/<issue_date>/revise`

- [ ] **Step 1: Write failing tamper-resistance and selection tests**

Create `blog/test_daily_editor.py`:

```python
from daily_editor import apply_selection, trusted_draft


def draft_fixture():
    trusted_source = {
        "source_id": "real",
        "title": "Official release",
        "url": "https://official.ai/release",
        "canonical_url": "https://official.ai/release",
        "publisher": "Official",
        "publisher_key": "official.ai",
        "is_primary": True,
        "verification_status": "readable",
    }
    return {
        "schema_version": 1,
        "draft_date": "2026-07-11",
        "generated_at": "2026-07-11 09:00",
        "topics": [{
            "topic_id": "topic-a", "rank": 1, "title": "A",
            "what_happened": "A happened.", "discussion_focus": [],
            "why_ranked": "A matters.", "sources": [trusted_source],
            "independent_source_count": 1,
        }],
        "candidates": [{
            "topic_id": "topic-b", "rank": 0, "title": "B",
            "what_happened": "B happened.", "discussion_focus": [],
            "why_ranked": "B may matter.", "sources": [trusted_source | {"source_id": "b"}],
            "independent_source_count": 1,
        }],
        "attention": [],
    }


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


def test_unknown_topic_id_and_empty_selection_are_rejected():
    for rows in ([], [{"topic_id": "unknown"}]):
        try:
            apply_selection(draft_fixture(), rows)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid selection must fail")
```

Add tests for duplicate topic IDs, more than three rows, overlong title/summary/judgment, and `trusted_draft()` rejecting `missing`, `invalid`, and `expired` freshness, a generated date different from `expected_date`, or malformed draft arrays.

- [ ] **Step 2: Run editor tests and verify they fail**

```bash
blog/.venv/bin/python blog/test_daily_editor.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'daily_editor'`.

- [ ] **Step 3: Implement trusted evidence hydration and audit logging**

Create `blog/daily_editor.py`:

```python
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
    merged = {
        str(source.get("source_id")): deepcopy(source)
        for source in (result.get("sources") or [])
        if source.get("source_id")
    }
    for source in (current_topic or {}).get("sources") or []:
        source_id = str(source.get("source_id") or "")
        if not source_id:
            continue
        if source_id not in merged:
            merged[source_id] = deepcopy(source)
        elif source.get("verification_status") == "readable":
            merged[source_id]["verification_status"] = "readable"
    result["sources"] = list(merged.values())
    result["independent_source_count"] = len({
        source["publisher_key"] for source in result["sources"]
    })
    return result


def revision_draft(published_issue, current_draft=None):
    published_topics = deepcopy((published_issue or {}).get("topics") or [])
    if not published_topics:
        raise ValueError("已发布简报没有可修订主题")
    current_draft = deepcopy(current_draft or {})
    current_pool = {}
    for group in ("topics", "candidates", "attention"):
        for topic in current_draft.get(group) or []:
            topic_id = str(topic.get("topic_id") or "")
            if topic_id:
                current_pool.setdefault(topic_id, topic)

    topics = [
        _merge_trusted_sources(topic, current_pool.get(str(topic["topic_id"])))
        for topic in published_topics
    ]
    top_ids = {str(topic["topic_id"]) for topic in topics}

    attention = []
    attention_ids = set()
    for topic in (published_issue or {}).get("attention") or []:
        topic_id = str(topic.get("topic_id") or "")
        if not topic_id or topic_id in top_ids or topic_id in attention_ids:
            continue
        attention.append(_merge_trusted_sources(topic, current_pool.get(topic_id)))
        attention_ids.add(topic_id)
    for topic in current_draft.get("attention") or []:
        topic_id = str(topic.get("topic_id") or "")
        if len(attention) >= 3:
            break
        if not topic_id or topic_id in top_ids or topic_id in attention_ids:
            continue
        attention.append(deepcopy(topic))
        attention_ids.add(topic_id)

    candidates = []
    seen = top_ids | attention_ids
    for topic_id, topic in current_pool.items():
        if topic_id in seen:
            continue
        candidates.append(deepcopy(topic))
        seen.add(topic_id)
    return {
        "schema_version": 1,
        "draft_date": current_draft.get("draft_date") or published_issue.get("issue_date"),
        "generated_at": current_draft.get("generated_at") or published_issue.get("revised_at") or published_issue.get("published_at"),
        "topics": topics,
        "candidates": candidates,
        "attention": attention,
    }


def apply_selection(draft, rows):
    if not isinstance(rows, list) or not 1 <= len(rows) <= 3:
        raise ValueError("简报必须包含 1–3 个主题")
    pool = {}
    for group in ("topics", "candidates", "attention"):
        for topic in draft.get(group) or []:
            if topic.get("topic_id"):
                pool[str(topic["topic_id"])] = topic
    selected = []
    seen = set()
    for rank, row in enumerate(rows, 1):
        topic_id = str(row.get("topic_id") or "")
        if topic_id not in pool or topic_id in seen:
            raise ValueError("主题不存在或重复")
        seen.add(topic_id)
        topic = deepcopy(pool[topic_id])
        for field in EDITABLE_FIELDS:
            if field in row:
                topic[field] = deepcopy(row[field])
        source_updates = {
            str(update.get("source_id")): str(update.get("verification_status"))
            for update in (row.get("source_updates") or [])
            if str(update.get("verification_status")) == "unavailable"
        }
        requested_source_ids = {
            str(source_id) for source_id in (row.get("source_ids") or []) if source_id
        }
        if "source_ids" in row:
            topic["sources"] = [
                source for source in (topic.get("sources") or [])
                if str(source.get("source_id") or "") in requested_source_ids
            ]
        if not topic.get("sources"):
            raise ValueError("每个主题至少保留一个可追溯来源")
        for source in topic.get("sources") or []:
            source_id = str(source.get("source_id") or "")
            if source_id in source_updates:
                source["verification_status"] = source_updates[source_id]
        topic["rank"] = rank
        topic["independent_source_count"] = len({
            str(source.get("publisher_key") or "").strip()
            for source in (topic.get("sources") or [])
            if str(source.get("publisher_key") or "").strip()
        })
        selected.append(topic)
    return selected


def append_editor_event(path: Path, event: dict, *, now: datetime) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"ts": now.isoformat(timespec="seconds"), **event}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
```

In `apply_selection()`, calculate `independent_source_count` as `len({source["publisher_key"] for source in topic["sources"]})`, never as the number supplied by the browser. `source_ids` may select a non-empty subset of the trusted pool, but unknown IDs add nothing and raw browser-submitted source objects are ignored. Compare `source_id` values as strings before applying status updates. The browser may only downgrade a trusted source to `unavailable`; it cannot promote `unchecked` or previously unavailable evidence to `readable`. A later same-day signal regeneration may restore `readable` only after the server successfully reads that same source ID again. Apply the hard `DAILY_TEXT_LIMITS` before returning; test every boundary and boundary + 1. The trusted source IDs, URLs, publishers, `topic_id`, and source count can never be replaced from the browser payload. For a same-day revision, `revision_draft()` may merge newly regenerated evidence only when it has the same server-generated `topic_id`; arbitrary URL entry is deliberately excluded to avoid forged evidence and SSRF. Routes pass `_local_now()` to `append_editor_event()` so audit timestamps use the configured blog timezone and remain deterministic in tests.

- [ ] **Step 4: Write failing admin API tests**

Extend `blog/test_admin_routes.py` with temporary `SIGNAL_CACHE`, `DAILY_ISSUES_DIR`, and editor log paths. Authenticate by injecting `daily_admin` and a known CSRF token into the test session.

Test:

```python
draft = client.get("/admin/daily/draft?date=2026-07-11")
assert draft.status_code == 200
assert draft.get_json()["draft"]["topics"][0]["topic_id"] == "topic-a"

published = client.post(
    "/admin/daily/2026-07-11/publish",
    headers={"X-CSRF-Token": "known-token"},
    json={"topics": [{"topic_id": "topic-a", "title": "人工标题"}]},
)
assert published.status_code == 201
assert published.get_json()["issue"]["topics"][0]["title"] == "人工标题"
assert published.get_json()["issue"]["topics"][0]["sources"][0]["url"] == "https://official.ai/release"

duplicate = client.post(
    "/admin/daily/2026-07-11/publish",
    headers={"X-CSRF-Token": "known-token"},
    json={"topics": [{"topic_id": "topic-a"}]},
)
assert duplicate.status_code == 409
assert duplicate.get_json()["code"] == "already_published"
```

Also test preview does not write a file, revise requires `expected_revision`, revision conflict returns 409, missing/invalid/expired/wrong-date current draft blocks only first publication with 409, and zero topics returns 400. Preview accepts only `preview_surface="home"` or `"dated"`: a current-day home preview says `今天`, while the same date previewed from its stable date page says `这一天`. A same-day published issue with a missing cache must still return its stored revision draft with 200. When a current issue is corrupt but public reading falls back to a valid revision, the authenticated page must disable `修订本期`, draft GET and revise POST must return `503 storage_corrupt`, and no file may change. Extend the Task 3 permission matrix so anonymous draft GET and preview/publish/revise POSTs all return 401, while authenticated POSTs without CSRF return 403. Assert the success audit event uses an injected `_local_now()` timestamp. Add a historical revision test where today’s signal cache contains unrelated topic IDs: `GET /admin/daily/draft?date=<past>` and the revise POST must still use the stored historical issue as the trusted evidence pool. Assert the resulting revision draft has globally unique `topic_id` values across `topics`, `candidates`, and `attention`.

- [ ] **Step 5: Add draft, preview, publish, and revise routes**

In `blog/app.py`, add admin-only routes. Every POST is covered by `admin_required`, so CSRF is mandatory:

```python
@app.get("/admin/daily/draft")
@admin_auth.admin_required
def admin_daily_draft():
    import today_signal
    today = _local_now().date().isoformat()
    issue_date = request.args.get("date") or today
    try:
        validate_issue_date(issue_date)
    except ValueError:
        return {"status": "bad_date"}, 400
    store = _issue_store()
    try:
        published = store.get(issue_date)
        if published:
            published = store.assert_revisable(issue_date)
    except DailyIssueCorrupt as exc:
        return {"status": "storage_corrupt", "message": str(exc)}, 503
    if issue_date != today:
        if not published:
            return {"status": "not_found"}, 404
        draft = daily_editor.revision_draft(published)
    elif published:
        try:
            current = daily_editor.trusted_draft(
                today_signal.read_signal_cache() or {}, expected_date=today
            )
        except ValueError:
            current = None
        draft = daily_editor.revision_draft(published, current)
    else:
        try:
            current = daily_editor.trusted_draft(
                today_signal.read_signal_cache() or {}, expected_date=today
            )
        except ValueError as exc:
            return {"status": "unavailable", "message": str(exc)}, 409
        draft = current
    issue_number = published["issue_number"] if published else store.next_issue_number()
    return {
        "status": "ok",
        "draft": draft,
        "published": published,
        "issue_meta": {
            "issue_date": issue_date,
            "issue_number": issue_number,
            "revision": published["revision"] if published else 0,
            "generated_at": draft.get("generated_at") or "",
        },
    }
```

For all three POST routes:

1. validate `issue_date` and restrict first publish to the configured local current date;
2. for a first publish, re-read today’s trusted signal draft; for a revision, always build the trust pool from the stored published issue, optionally adding today’s candidates only when the revised date is today and that cache is valid;
3. call `daily_editor.apply_selection(draft, body["topics"])`;
4. pass trusted topics and selected attention to `DailyIssueStore`;
5. carry forward draft attention after removing any `topic_id` promoted into the top three;
6. append a successful event containing `kind`, `issue_date`, `revision`, `draft_topic_ids`, and `published_topic_ids` to `Path(app.config["DAILY_EDITOR_LOG"])`, passing `_local_now()` as the timestamp source;
7. return `{"status":"ok","issue":issue,"redirect_url":_stable_issue_url(issue_date)}` without the admin password, CSRF token, full draft pool, or unselected candidates.

Map domain errors explicitly: validation to 400, missing trusted first-publication draft to 409, stale revision to 409 with `code="revision_conflict"`, duplicate first publication to 409 with `code="already_published"`, storage corruption to 503 with `code="storage_corrupt"`, and unexpected persistence failures to a generic 500 response without filesystem paths or exception details. Log server-side exceptions through the existing Flask logger.

Preview validates the non-authoritative presentation hint `preview_surface` against `{"home", "dated"}`, then calls `DailyIssueStore.preview()` so the HTML receives a complete, validated provisional issue with issue number and revision metadata. It uses `render_template("_daily_brief.html", issue=preview_issue, daily_error="", is_home=(preview_surface == "home"), is_current_day=(issue_date == today))` and returns `{"status":"ok","html":html}` without writing disk. The hint changes wording only; it cannot change evidence, issue date, rank, or persistence.

- [ ] **Step 6: Update view context for authenticated controls only**

In `_issue_view()`, generate CSRF only for authenticated admins:

```python
admin = admin_auth.is_admin()
draft_available = True
draft_message = ""
if admin:
    try:
        if admin_action == "revise":
            _issue_store().assert_revisable(admin_target_date)
        else:
            _issue_store().next_issue_number()  # also performs the global write-integrity scan
            import today_signal
            daily_editor.trusted_draft(
                today_signal.read_signal_cache() or {}, expected_date=today
            )
    except (DailyIssueCorrupt, ValueError) as exc:
        draft_available = False
        draft_message = str(exc)
return {
    # existing public keys
    "is_admin": admin,
    "csrf_token": admin_auth.csrf_token() if admin else "",
    "admin_action": admin_action,
    "admin_target_date": admin_target_date,
    "current_issue_date": today,
    "draft_available": draft_available,
    "draft_message": draft_message,
    "editor_limits": DAILY_TEXT_LIMITS if admin else {},
}
```

Keep the Task 4 `admin_action` decision unchanged: an old latest issue on `/` offers `发布今日`, while any existing dated issue offers `修订本期`. Only a first publication depends on today’s mutable draft; historical revision remains available from stored evidence even when today’s cache is missing. Any unrecoverable issue-store corruption disables every write. A target date whose current file is corrupt also disables `修订本期` even when public readers are safely seeing an archived fallback. Anonymous HTML must not contain the token or draft URLs in data attributes.

- [ ] **Step 7: Run domain and route tests**

```bash
blog/.venv/bin/python blog/test_daily_editor.py
blog/.venv/bin/python blog/test_admin_routes.py
blog/.venv/bin/python blog/test_daily_issues.py
blog/.venv/bin/python blog/test_daily_routes.py
PYTHONDONTWRITEBYTECODE=1 blog/.venv/bin/python -m py_compile \
  blog/daily_editor.py blog/app.py blog/test_daily_editor.py blog/test_admin_routes.py
```

Expected: all tests pass; compilation exits 0.

- [ ] **Step 8: Commit trusted publication APIs**

```bash
git add blog/daily_editor.py blog/test_daily_editor.py blog/app.py blog/test_admin_routes.py
git commit -m "feat: publish and revise trusted daily issues"
```

---

### Task 7: Administrator Reorder/Edit/Replace/Preview Dialog

**Files:**
- Create: `blog/templates/_admin_daily_dialog.html`
- Create: `blog/static/css/admin-daily.css`
- Create: `blog/static/js/admin-daily.mjs`
- Create: `blog/static/js/admin-daily-state.mjs`
- Create: `blog/test_admin_daily_state.mjs`
- Modify: `blog/templates/index.html`
- Modify: `blog/templates/daily.html`
- Modify: `blog/templates/base.html`
- Modify: `blog/test_admin_routes.py`

**Interfaces:**
- Consumes: Task 6 admin endpoints and `csrf_token`, `admin_action`, current issue date/revision.
- Produces:
  - `#dailyAdminButton` visible only to authenticated admin.
  - native `<dialog id="dailyAdminDialog">`.
  - editor payload containing only topic IDs and editable copy fields.
  - mouse drag-and-drop plus keyboard/mobile `上移` / `下移` controls.

- [ ] **Step 1: Add failing authenticated-vs-public template tests**

Extend `blog/test_admin_routes.py`:

```python
def test_public_home_has_no_admin_dialog_or_csrf():
    client = configured_issue_client(authenticated=False)
    html = client.get("/").get_data(as_text=True)
    assert "dailyAdminButton" not in html
    assert "dailyAdminDialog" not in html
    assert "adminCsrfToken" not in html
    assert "adminEditorConfig" not in html
    assert "/admin/daily/draft" not in html


def test_authenticated_home_has_publish_dialog_without_password():
    client = configured_issue_client(authenticated=True)
    html = client.get("/").get_data(as_text=True)
    assert "dailyAdminButton" in html
    assert "dailyAdminDialog" in html
    assert "发布今日" in html
    assert "correct horse" not in html
```

Add these state assertions:

- authenticated `/daily/2026-07-11` shows `修订本期` and the current revision even if today’s signal cache is missing;
- authenticated `/` with an older latest issue shows `发布今日`, not `修订本期`;
- when today’s trusted draft is missing or invalid, the `发布今日` button has `disabled`, `aria-disabled="true"`, and a visible `draft_message`;
- anonymous HTML contains none of the button, dialog, CSRF, draft URL, or draft error text.

- [ ] **Step 2: Run the route tests and verify they fail**

```bash
blog/.venv/bin/python blog/test_admin_routes.py
```

Expected: FAIL because the admin button/dialog is not yet rendered.

- [ ] **Step 3: Add the authenticated dialog template**

Create `blog/templates/_admin_daily_dialog.html`:

```html
<button id="dailyAdminButton" class="daily-admin-open" type="button"
        data-action="{{ admin_action }}" data-date="{{ admin_target_date }}"
        data-preview-surface="{{ 'home' if is_home else 'dated' }}"
        {% if not draft_available %}disabled aria-disabled="true" aria-describedby="dailyAdminUnavailable"{% endif %}>
  <span aria-hidden="true">●</span>
  {{ '修订本期' if admin_action == 'revise' else '发布今日' }}
</button>
{% if not draft_available %}
<span id="dailyAdminUnavailable" class="daily-admin-unavailable" role="status">{{ draft_message }}</span>
{% endif %}
<script id="adminCsrfToken" type="application/json">{{ {'token': csrf_token}|tojson }}</script>
<script id="adminEditorConfig" type="application/json">{{ editor_limits|tojson }}</script>
<dialog id="dailyAdminDialog" class="daily-admin-dialog" aria-labelledby="dailyAdminTitle">
  <div class="daily-admin-shell">
    <header>
      <div><span>NOISEFILTER EDITOR</span><h2 id="dailyAdminTitle">{{ '修订本期' if admin_action == 'revise' else '发布今日简报' }}</h2></div>
      <button id="dailyAdminClose" type="button" aria-label="关闭">×</button>
    </header>
    <p id="dailyAdminMeta" class="daily-admin-meta"></p>
    <p id="dailyAdminState" role="status">正在读取今日候选…</p>
    <div id="dailyAdminRows" class="daily-admin-rows"></div>
    <label class="daily-admin-add">替换 / 补充候选
      <select id="dailyCandidateSelect"><option value="">选择候选</option></select>
      <button id="dailyCandidateAdd" type="button">加入</button>
    </label>
    <section id="dailyAdminPreview" class="daily-admin-preview" hidden></section>
    <footer>
      <button id="dailyPreviewButton" type="button">预览读者页面</button>
      <button id="dailyPublishButton" type="button">{{ '保存修订' if admin_action == 'revise' else '确认发布' }}</button>
    </footer>
  </div>
</dialog>
```

Include this partial only inside `{% if is_admin %}`. Pass `current_issue_date`, `draft_available`, `draft_message`, and server-owned `editor_limits` from `_issue_view()` even when there is no published issue. The unavailable message is escaped by Jinja and contains no draft payload.

- [ ] **Step 4: Implement safe DOM rendering and editor controls**

Create `blog/static/js/admin-daily-state.mjs` for the pure state helpers and import them from `blog/static/js/admin-daily.mjs`, which is loaded with `type="module"`. Do not build rows with unescaped `innerHTML`; use `createElement`, `textContent`, and input `.value`.

The state contract is:

```javascript
const state = {
  action: button.dataset.action,
  issueDate: button.dataset.date,
  previewSurface: button.dataset.previewSurface,
  revision: null,
  selected: [],
  candidates: [],
};
```

Implement these functions with exact responsibilities:

```javascript
function rowState(topic) {
  return {
    topic_id: topic.topic_id,
    category: topic.category || '',
    title: topic.title || '',
    what_happened: topic.what_happened || '',
    discussion_focus: (topic.discussion_focus || []).slice(0, 3),
    why_ranked: topic.why_ranked || '',
    sources: (topic.sources || []).map((source) => ({
      ...source,
      included: true,
      trusted_status: source.verification_status,
    })),
  };
}

function rowPayload(topic) {
  return {
    topic_id: topic.topic_id,
    category: topic.category,
    title: topic.title,
    what_happened: topic.what_happened,
    discussion_focus: topic.discussion_focus,
    why_ranked: topic.why_ranked,
    source_ids: (topic.sources || []).filter((source) => source.included).map((source) => source.source_id),
    source_updates: (topic.sources || [])
      .filter((source) => source.included && source.verification_status === 'unavailable' && source.trusted_status !== 'unavailable')
      .map((source) => ({ source_id: source.source_id, verification_status: 'unavailable' })),
  };
}

function moveTopic(from, to) {
  if (to < 0 || to >= state.selected.length) return;
  const [topic] = state.selected.splice(from, 1);
  state.selected.splice(to, 0, topic);
  renderRows();
}

function removeTopic(index) {
  state.candidates.push(state.selected[index]);
  state.selected.splice(index, 1);
  renderRows();
  renderCandidates();
}

function addCandidate(topicId) {
  if (state.selected.length >= 3) return;
  const index = state.candidates.findIndex((item) => item.topic_id === topicId);
  if (index < 0) return;
  state.selected.push(state.candidates.splice(index, 1)[0]);
  renderRows();
  renderCandidates();
}

function requestJson(url, options) {
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken,
      ...(options && options.headers ? options.headers : {}),
    },
  }).then(async (response) => {
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(body.message || `请求失败（HTTP ${response.status}）`);
      error.status = response.status;
      error.body = body;
      throw error;
    }
    return body;
  });
}
```

`renderRows()` creates editable inputs for `title`, `what_happened`, comma-separated `discussion_focus`, and `why_ranked`; it also creates `上移`, `下移`, `移除`, and per-row candidate replacement controls. Render each trusted source read-only with an `纳入本期依据` checkbox plus a one-way `来源暂不可访问` downgrade checkbox; URL and publisher are never editable. A source already stored as unavailable stays locked unless a regenerated trusted draft has restored it. Warn when a selected topic has zero readable sources (blocking) or only one independent publisher (non-blocking). Add HTML5 `dragstart`, `dragover`, and `drop` for desktop, but keep buttons as the accessible/mobile path. Every dynamically created button explicitly uses `type="button"`; `#dailyAdminClose` calls `dialog.close()` so pressing Enter in a text input cannot accidentally close or publish the dialog.

Parse `#adminEditorConfig` and use those values rather than duplicating numeric hard limits in JavaScript. The confirm button is disabled unless 1–3 rows exist, every row retains at least one source including one readable source for a first publication, no required field is blank, and no field exceeds a hard limit (`category=20`, title `60`, core fact `160`, each of at most three focus items `32`, judgment `120`). Show non-blocking layout warnings above 34 title characters for rank 1, above 24 for ranks 2/3, and for single-publisher evidence; the server remains authoritative.

- [ ] **Step 5: Implement draft loading, preview, publish, and revision**

On `dailyAdminButton` click:

```javascript
requestJson('/admin/daily/draft?date=' + encodeURIComponent(state.issueDate), { method: 'GET' }).then((body) => {
  state.action = body.published ? 'revise' : 'publish';
  state.selected = (body.draft.topics || []).map(rowState);
  const selectedIds = new Set(state.selected.map((item) => item.topic_id));
  state.candidates = [...(body.draft.candidates || []), ...(body.draft.attention || [])]
    .filter((item) => !selectedIds.has(item.topic_id))
    .map(rowState);
  state.revision = body.published ? body.published.revision : null;
  document.getElementById('dailyAdminMeta').textContent = [
    body.issue_meta.issue_date,
    `第 ${String(body.issue_meta.issue_number).padStart(3, '0')} 期`,
    body.issue_meta.generated_at ? `候选生成 ${body.issue_meta.generated_at}` : '',
  ].filter(Boolean).join(' · ');
  renderRows();
  renderCandidates();
  dialog.showModal();
}).catch(showError);
```

Preview POST body:

```javascript
{
  topics: state.selected.map(rowPayload),
  preview_surface: state.previewSurface,
}
```

Publish uses `/admin/daily/${date}/publish`. Revise uses `/admin/daily/${date}/revise` with `expected_revision`. If a publish returns `409` with `code="already_published"`, reload the draft, switch `state.action` to `revise`, and show `本期已发布，已切换为修订`; do not resubmit automatically. On success, navigate to the returned stable `redirect_url`; never optimistically rewrite public cards before the server confirms persistence.

Create `blog/test_admin_daily_state.mjs` against the exported state helpers. Assert that adding a raw trusted candidate first passes through `rowState()`, then `rowPayload()` retains a non-empty trusted `source_ids` list; removing and re-adding the same row preserves `included` and `trusted_status`.

- [ ] **Step 6: Add isolated admin styles**

Create `blog/static/css/admin-daily.css` with `.daily-admin-*` selectors only. Requirements:

- dialog max width 920px and max height 90vh;
- sticky header/footer;
- each row visibly numbered and draggable on desktop;
- full-width native inputs/textarea with clear labels;
- source evidence read-only;
- preview visually separated from editable form;
- unavailable-draft status remains legible beside the disabled header button;
- mobile rows stack; drag handle hidden, up/down buttons remain;
- `::backdrop` uses a translucent dark scrim;
- `prefers-reduced-motion` disables transitions.

Load admin CSS and JS only when `is_admin` is true through base template blocks.

- [ ] **Step 7: Run static and route checks**

```bash
node --check blog/static/js/admin-daily.mjs
node --check blog/static/js/admin-daily-state.mjs
node blog/test_admin_daily_state.mjs
blog/.venv/bin/python blog/test_admin_routes.py
blog/.venv/bin/python blog/test_daily_routes.py
blog/.venv/bin/python blog/test_daily_templates.py
```

Expected: Node exits 0; all Python scripts pass.

- [ ] **Step 8: Perform one authenticated browser smoke test**

Start the app only with disposable `DAILY_ISSUES_DIR`, `SIGNAL_CACHE_PATH`, and `DAILY_EDITOR_LOG` values (the complete fixture command is in Task 8); never point this smoke test at the real ignored `blog/data/`:

```bash
blog/.venv/bin/python blog/app.py
```

In the in-app browser at `http://127.0.0.1:5055/admin/login`, verify: login; open editor; move 2 above 1 and back; remove/add a topic; edit copy; preview; reject zero topics; publish; revise; confirm the date URL stays unchanged. Do not use real external publishing or messaging. If Task 8 follows immediately, perform this once there rather than starting a duplicate server.

- [ ] **Step 9: Commit the admin editor**

```bash
git add blog/templates/_admin_daily_dialog.html blog/templates/base.html \
  blog/templates/index.html blog/templates/daily.html \
  blog/static/css/admin-daily.css blog/static/js/admin-daily.mjs \
  blog/static/js/admin-daily-state.mjs blog/test_admin_daily_state.mjs \
  blog/test_admin_routes.py
git commit -m "feat: add the daily brief publication editor"
```

---

### Task 8: Product Documentation, Full Regression, and Visual Acceptance

**Files:**
- Modify: `README.md:179-188`
- Modify: `docs/产品定位与用户场景.md:9-84, 137-158`
- Verify: all files changed in Tasks 1–7

**Interfaces:**
- Consumes: the complete vertical workflow from Tasks 1–7.
- Produces: updated user-facing documentation, full offline regression evidence, public security checks, and desktop/mobile visual QA artifacts outside the repository.

- [ ] **Step 1: Update the README homepage and operating description**

Replace the old “首页：三列卡片网格” wording with:

```markdown
**首页**：展示最新一期「降噪每日简报」——左侧第 1 条大卡片、右侧第 2/3 条小卡片，下面依次是「热议浮现」和现有深度内容库。

- `/`：最新已发布一期
- `/daily`：往期简报
- `/daily/YYYY-MM-DD`：可稳定分享的日期页
- 管理员在右上角手动发布或修订；普通读者看不到管理操作

实时 `today_signal.json` 只提供发布草稿。公开首页只读取已发布快照，不会随缓存自动漂移。
```

Document required `config/.env` keys without values:

```dotenv
BLOG_ADMIN_PASSWORD=
SECRET_KEY=
BLOG_TIMEZONE=America/Los_Angeles
PUBLIC_BASE_URL=
# DAILY_ISSUES_DIR=/persistent/path/daily_issues
# SIGNAL_CACHE_PATH=/persistent-or-local/path/today_signal.json
# DAILY_EDITOR_LOG=/persistent-or-local/path/daily_editor_events.jsonl
```

State that external deployment must use a persistent `DAILY_ISSUES_DIR`, HTTPS with `SESSION_COOKIE_SECURE=true`, and reverse-proxy rate limiting on `/admin/login`.

- [ ] **Step 2: Update the product-positioning document**

In `docs/产品定位与用户场景.md`, add the confirmed entry point verbatim:

```markdown
> 给 AI 从业者的每日降噪简报：自己快速看懂，也能直接转给同事。
```

Update the scenario section to describe:

1. personal reading: open the latest issue and understand at most three event topics;
2. deeper learning: expand evidence or continue into the existing deep library;
3. company sharing: copy the dated issue link and send it to non-technical or technical colleagues without creating a second version;
4. future company-specific context is explicitly out of the current product scope.

Remove the “待产品化的被动读者” wording that contradicts the now-public daily issue, but keep the strategy that media/editorial judgment—not SaaS tooling—is the product advantage.

- [ ] **Step 3: Run the complete offline test suite**

```bash
set -e
for f in \
  blog/test_product_schema.py \
  blog/test_user_preferences.py \
  blog/test_embeddings.py \
  blog/test_ingest_jobs.py \
  blog/test_topic_drafts.py \
  blog/test_today_signal.py \
  blog/test_daily_issues.py \
  blog/test_daily_editor.py \
  blog/test_app_routes.py \
  blog/test_daily_routes.py \
  blog/test_daily_templates.py \
  blog/test_admin_routes.py
do
  blog/.venv/bin/python "$f"
done
node scripts/test-product-schema.mjs
node scripts/test-rewrite-format.mjs
node --check blog/static/js/daily.js
node --check blog/static/js/admin-daily.mjs
node --check blog/static/js/admin-daily-state.mjs
node blog/test_admin_daily_state.mjs
PYTHONDONTWRITEBYTECODE=1 blog/.venv/bin/python -m py_compile \
  blog/app.py blog/config.py blog/admin_auth.py blog/topic_drafts.py \
  blog/today_signal.py blog/daily_issues.py blog/daily_editor.py
```

Expected: every Python script prints `全部通过 ✅` or its existing named success output; Node and compilation commands exit 0.

- [ ] **Step 4: Start a disposable QA server with a three-topic fixture**

Create `/tmp/noisefilter-seed.py` with the same valid schema helpers used by `blog/test_daily_issues.py`; this file stays outside Git. It must be network-free and do exactly two things:

1. seed yesterday as issue 1 through `DailyIssueStore` if it does not exist;
2. atomically write today’s trusted `daily_draft` to `SIGNAL_CACHE_PATH`, using the configured timezone, `draft_date=today`, three top topics, one extra candidate, and either zero attention rows or three when called with `--attention`.

The fixture deliberately includes: a rank-1 topic with two independent publishers; a 55–60-character side-card title; one very long publisher name; a single-source rank 2; and `category=""` on rank 3. Every selected topic has at least one readable source. It calls `today_signal._write_signal_cache()` rather than hand-writing JSON, and it never touches archive, Feishu, AI HOT, or the network.

Use this complete `/tmp/noisefilter-seed.py` implementation so QA does not invent another schema:

```python
"""Seed disposable NoiseFilter QA data. Never point env paths at real blog/data."""

import argparse
import os
import time
from datetime import datetime, time as day_time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import today_signal
from daily_issues import DailyIssueStore


parser = argparse.ArgumentParser()
parser.add_argument("--attention", action="store_true")
args = parser.parse_args()
timezone_name = os.environ["BLOG_TIMEZONE"]
tz = ZoneInfo(timezone_name)
now = datetime.now(tz)
today = now.date()
yesterday = today - timedelta(days=1)


def source(source_id, publisher, host, *, title="Original source"):
    url = f"https://{host}/{source_id}"
    return {
        "source_id": source_id,
        "title": title,
        "url": url,
        "canonical_url": url,
        "publisher": publisher,
        "publisher_key": host,
        "published_at": now.isoformat(timespec="minutes"),
        "is_primary": True,
        "verification_status": "readable",
        "provider_score": 90,
    }


def topic(topic_id, rank, title, sources, *, category="模型发布"):
    return {
        "topic_id": topic_id,
        "rank": rank,
        "category": category,
        "title": title,
        "what_happened": f"{title[:36]} 发生了一项可核对的重要变化。",
        "discussion_focus": ["真实体验", "成本与边界"],
        "why_ranked": "它可能直接改变近期的产品选择和学习优先级。",
        "sources": sources,
        "independent_source_count": len({row["publisher_key"] for row in sources}),
    }


long_side_title = ("超长侧栏标题用于验证换行截断与依据按钮布局" * 4)[:58]
long_publisher = "一家名称非常非常长用于验证窄屏自动换行而不撑开卡片的独立研究出版方"
top_topics = [
    topic("topic-qa-lead", 1, "一个足以影响近期 AI 工作流的重要发布", [
        source("qa-lead-official", "Official Lab", "official.qa"),
        source("qa-lead-analysis", long_publisher, "analysis.qa", title="Independent analysis with a deliberately long source title"),
    ]),
    topic("topic-qa-side-long", 2, long_side_title, [
        source("qa-side-long", "Single Source", "single.qa"),
    ], category="产品变化"),
    topic("topic-qa-no-category", 3, "一项没有分类标签但仍值得关注的平台变化", [
        source("qa-no-category", "Platform Notes", "platform.qa"),
    ], category=""),
]
candidate = topic("topic-qa-candidate", 0, "额外候选主题", [
    source("qa-candidate", "Candidate Source", "candidate.qa"),
], category="继续观察")
attention = []
if args.attention:
    for index, status in enumerate(("rising", "watch", "stable"), 1):
        row = topic(
            f"topic-qa-attention-{index}", 0, f"热议浮现 {index}",
            [source(f"qa-attention-{index}", f"Attention Source {index}", f"attention{index}.qa")],
            category="热议",
        )
        row["attention_status"] = status
        attention.append(row)

root = Path(os.environ["DAILY_ISSUES_DIR"])
store = DailyIssueStore(root, timezone_name)
if store.get(yesterday.isoformat()) is None:
    old = topic("topic-qa-yesterday", 1, "昨天已发布的稳定主题", [
        source("qa-yesterday", "Yesterday Official", "yesterday.qa"),
    ])
    published_at = datetime.combine(yesterday, day_time(9, 0), tzinfo=tz)
    store.publish(yesterday.isoformat(), [old], [], now=published_at)

generated_at = now.strftime("%Y-%m-%d %H:%M")
draft = {
    "schema_version": 1,
    "draft_date": today.isoformat(),
    "generated_at": generated_at,
    "window_hours": 48,
    "topics": top_topics,
    "candidates": [candidate],
    "attention": attention,
    "input_stats": {"raw_items": 9, "unique_sources": 9, "clustered_topics": 7},
}
today_signal._write_signal_cache({
    "expiry": time.time() + 86400,
    "generated_at": generated_at,
    "window_hours": 48,
    "daily_draft": draft,
    "breaking": None,
    "signals": top_topics,
    "attention": attention,
    "slots_total": 3,
    "behavior": {},
})
print(f"seeded yesterday={yesterday.isoformat()} draft_date={today.isoformat()}")
```

Run everything under `/tmp`, never under the repository’s real `blog/data/`:

```bash
export QA_ROOT=/tmp/noisefilter-daily-qa
export TODAY="$(TZ=America/Los_Angeles date +%F)"
export YESTERDAY="$(TZ=America/Los_Angeles date -v-1d +%F)"
export BLOG_ADMIN_PASSWORD='qa-only-password'
export SECRET_KEY='qa-only-secret-key'
export PUBLIC_BASE_URL='http://127.0.0.1:5055'
export DAILY_ISSUES_DIR="$QA_ROOT/issues"
export SIGNAL_CACHE_PATH="$QA_ROOT/today_signal.json"
export DAILY_EDITOR_LOG="$QA_ROOT/daily_editor_events.jsonl"
export BLOG_TIMEZONE='America/Los_Angeles'
rm -rf /tmp/noisefilter-daily-qa
mkdir -p "$DAILY_ISSUES_DIR"
PYTHONPATH=blog blog/.venv/bin/python /tmp/noisefilter-seed.py --attention
blog/.venv/bin/python blog/app.py
```

Expected before UI publication: `/` shows the seeded yesterday issue as `最新一期`; today’s issue file does not exist; today’s three topics and three attention rows exist only in the isolated draft cache. The automated template test already covers the empty-attention state. Preserve these exported variables in the second shell.

- [ ] **Step 5: Verify public HTML, metadata, and mutation isolation**

```bash
curl -fsS http://127.0.0.1:5055/ > /tmp/noisefilter-home.html
curl -fsS "http://127.0.0.1:5055/daily/$YESTERDAY" > /tmp/noisefilter-daily.html
rg 'canonical|og:title|og:description|og:image' /tmp/noisefilter-daily.html
! rg -q 'AI HOT|今日 AI 判断|加入首页判断|先不加|dailyAdminDialog|adminCsrfToken' /tmp/noisefilter-home.html
test ! -e "$DAILY_ISSUES_DIR/$TODAY.json"
publish_code="$(curl -sS -o /tmp/noisefilter-admin-response -w '%{http_code}' \
  -X POST "http://127.0.0.1:5055/admin/daily/$TODAY/publish" \
  -H 'Content-Type: application/json' -d '{}')"
test "$publish_code" = 401
test ! -e "$DAILY_ISSUES_DIR/$TODAY.json"
before_hash="$(shasum "$DAILY_ISSUES_DIR/$YESTERDAY.json" | awk '{print $1}')"
revise_code="$(curl -sS -o /tmp/noisefilter-revise-response -w '%{http_code}' \
  -X POST "http://127.0.0.1:5055/admin/daily/$YESTERDAY/revise" \
  -H 'Content-Type: application/json' -d '{"expected_revision":1,"topics":[]}')"
test "$revise_code" = 401
after_hash="$(shasum "$DAILY_ISSUES_DIR/$YESTERDAY.json" | awk '{print $1}')"
test "$before_hash" = "$after_hash"
curl -fsS http://127.0.0.1:5055/static/og-daily.png > /tmp/noisefilter-og.png
file /tmp/noisefilter-og.png
test "$(sips -g pixelWidth /tmp/noisefilter-og.png | awk '/pixelWidth/{print $2}')" = 1200
test "$(sips -g pixelHeight /tmp/noisefilter-og.png | awk '/pixelHeight/{print $2}')" = 630
```

Expected:

- metadata scan returns canonical and all OG tags;
- negative `rg` exits 0 because none of the forbidden strings appear;
- anonymous publish and revise both return HTTP `401`; today’s nonexistent issue stays nonexistent and yesterday’s hash stays unchanged;
- the OG asset is a reachable 1200×630 PNG.

- [ ] **Step 6: Perform visual QA in the in-app browser**

First open `http://127.0.0.1:5055/` anonymously and confirm no admin control appears and yesterday is labeled `最新一期`. Log in at `/admin/login`, confirm the home button says `发布今日`, open the editor, and verify its date, provisional issue number, and candidate generation time. Move 2 above 1 and back, remove/re-add the extra candidate, preview the home surface (`今天` wording), and publish today. Confirm `/` now points to today while `/daily/$YESTERDAY` remains unchanged.

Inspect today’s published home at 1366×768:

- warm beige background and approved fused logo;
- masthead plus all three ranks in the first viewport;
- rank 1 is the large left rounded card;
- ranks 2 and 3 are stacked right rounded cards;
- source counts are truthful and single-source cards do not claim merging;
- “热议浮现” begins below the top-three block;
- the 55–60-character title, long publisher name, and missing category do not collide or overflow;
- the existing deep-content images/cards remain unchanged below it.

Inspect at 390×844:

- cards order is 1 → 2 → 3;
- rank 2 or a clear continuation cue is visible below rank 1;
- no horizontal overflow;
- side-card title/core fact/judgment clamp cleanly without covering evidence controls;
- evidence `<details>`, copy button, login, dialog, up/down controls, preview, publish, and revise are keyboard-operable.

Save screenshots to `/tmp/noisefilter-1366.png` and `/tmp/noisefilter-390.png`; do not commit QA screenshots.

- [ ] **Step 7: Verify revision and dated-link stability**

Using the admin UI:

1. record that seeded `/daily/$YESTERDAY` is issue 1 and unchanged after Step 6;
2. capture `/daily/$TODAY` after Step 6 publication and confirm it is issue 2, revision 1, while `/` has switched from yesterday to today;
3. open `/daily/$TODAY` as admin, confirm the button says `修订本期`, and confirm its preview says `这一天` rather than the home surface’s `今天`;
4. revise the rank order and one title;
5. confirm URL and issue number are unchanged, revision increments to 2, “最后修订” appears, the revision-1 archive file exists, and `/daily/$YESTERDAY` is byte-for-byte unchanged;
6. stop and restart the app with the same exported `/tmp/noisefilter-daily-qa` paths and confirm both dates remain readable and `/` still selects `$TODAY`.

- [ ] **Step 8: Inspect the final diff and repository state**

```bash
git diff --check
git status --short
git diff --stat HEAD~7..HEAD
rg -n 'AI HOT|今日 AI 判断|加入首页判断|先不加' \
  blog/templates/index.html blog/templates/daily.html \
  blog/templates/_daily_brief.html blog/templates/_daily_attention.html
```

Expected:

- `git diff --check` has no output;
- only the user-owned untracked `.superpowers/` and `AGENTS.md` remain outside committed work;
- the public-template terminology scan has no matches;
- legacy `_signals.html` may still contain old language but is no longer included by public routes.

- [ ] **Step 9: Commit documentation and handoff**

```bash
git add README.md docs/产品定位与用户场景.md
git commit -m "docs: describe the NoiseFilter daily brief workflow"
```

Before claiming completion, invoke `superpowers:verification-before-completion`, rerun the full commands from Steps 3 and 5, and report exact pass evidence plus any deployment requirement still external to the repository (persistent volume, HTTPS, public base URL).

---

## Implementation Completion Criteria

Implementation is complete only when all of the following are true:

- topic draft source counts are deterministic and covered by tests;
- the public homepage never reads mutable `today_signal.json` as a published issue;
- 1/2/3-topic snapshots publish atomically and survive restart;
- revision preserves date URL and issue number while archiving the previous revision;
- anonymous users cannot invoke any privileged/admin write or ingest route; `/track` remains public non-blocking telemetry;
- no draft, candidate pool, CSRF token, or management control leaks into anonymous HTML;
- the desktop layout matches the approved left-large/right-two-small card design;
- mobile, empty, one-topic, two-topic, no-attention, old-latest, corrupt-file, and conflict states pass;
- dated share text, canonical URL, OG metadata, and OG image are valid;
- all existing deep-library behavior and tests remain green;
- documentation explains the manual publication and persistence requirements.
