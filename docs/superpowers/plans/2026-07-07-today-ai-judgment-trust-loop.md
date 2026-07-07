# Today AI Judgment Trust Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the B-scope spec for 今日 AI 判断：freshness trust states, product schema consistency, behavior learning, attention evidence status, ingest job status, score wording cleanup, and related-cover rendering.

**Architecture:** Keep the existing Flask + archive-first architecture. Add small, testable helper modules for shared product schema and ingest job state; keep daily judgment generation in `blog/today_signal.py`; keep page requests read-only for signal generation; use local JSON files instead of databases or queues.

**Tech Stack:** Python 3 + Flask, existing plain Python test files, Node.js ESM scripts, local JSON files, existing `run.sh`, existing `blog/.venv` and root `.venv`.

## Global Constraints

- Scope is B: trusted daily judgment + data consistency + behavior learning + ingest status feedback.
- Do not add a user-visible Agent.
- Do not add instant push.
- Do not add multi-user login.
- Do not introduce Celery, Redis, SQLite, or any external queue.
- Do not refactor the whole CSS file.
- Do not rewrite the full README; only fix obviously stale scoring/runtime wording.
- Keep archive as the source of truth.
- Page requests must not generate 今日判断; they only read signal cache and job status.
- Attention items are not recommendations until the user promotes them.
- Behavior learning uses explicit positive actions only; `dismiss_attention` is not negative feedback.
- New content scoring dimensions are exactly: `insight/source/storytelling`, displayed as `洞察原创 / 信源质量 / 故事可读`.
- Supported topics are exactly: `AI 前沿`, `AI 编程`, `AI 产品`, `AI 创业`, `AI 商业`, `投资`, `个人效率`, `其他`.
- Because the current working tree has existing uncommitted product changes that this spec was based on, implementation must preserve them before using independent worktrees.

---

## Execution Prerequisite: protect current dirty base

The repository is currently on `master`, ahead of `origin/master` by 1 commit, with a committed spec plus existing uncommitted product work in:

- `CLAUDE.md`
- `blog/app.py`
- `blog/requirements.txt`
- `blog/static/css/style.css`
- `blog/templates/_card.html`
- `blog/templates/_signals.html`
- `blog/templates/base.html`
- `blog/templates/index.html`
- `blog/today_signal.py`
- `THIRD_PARTY_NOTICES.md`
- `blog/source_reader.py`
- `blog/test_today_signal.py`
- `blog/tool_probe.py`
- `blog/user_preferences.py`
- `config/preferences.json`

Implementation must not create an isolated worktree from a clean HEAD that lacks these files, because the spec references this WIP state. Before implementation, choose one of these:

1. Recommended for subagent-driven implementation: create a WIP base commit containing the current uncommitted product work, then create a feature worktree from that commit.
2. Inline execution fallback: implement in the current working tree and commit task-by-task, preserving user changes.

If using option 1, run these commands only after user approval:

```bash
git status --short --branch
git add CLAUDE.md blog/app.py blog/requirements.txt blog/static/css/style.css blog/templates/_card.html blog/templates/_signals.html blog/templates/base.html blog/templates/index.html blog/today_signal.py THIRD_PARTY_NOTICES.md blog/source_reader.py blog/test_today_signal.py blog/tool_probe.py blog/user_preferences.py config/preferences.json
git commit -m "chore: snapshot today judgment WIP base"
git worktree add ../content-curation-trust-loop -b feat/today-judgment-trust-loop
```

If the user declines the WIP snapshot commit, do not use a separate worktree that starts from HEAD; continue inline or ask for a different base branch.

## Evaluator Gate Required After Every Task

After each implementation task:

1. Run that task's tests.
2. Commit that task.
3. Dispatch an evaluator agent with this prompt:

```text
You are the evaluator for Task <N> of Today AI Judgment Trust Loop.
Review the diff against docs/superpowers/plans/2026-07-07-today-ai-judgment-trust-loop.md and docs/superpowers/specs/2026-07-07-today-ai-judgment-trust-loop-design.md.
Look for product-logic regressions, stale wording, missing edge cases, test gaps, and implementation shortcuts that violate "降噪优先".
Do not rewrite code. Return concrete findings with severity and exact file references.
```

4. Fix evaluator findings if valid.
5. Re-run tests.
6. Repeat review/fix loop at most 3 rounds for that task.

## File Structure

- Create `config/product_schema.json`: shared topics and score dimensions.
- Create `blog/product_schema.py`: Python reader/normalizer for product schema.
- Create `scripts/product-schema.js`: Node ESM reader/normalizer for product schema.
- Create `scripts/test-product-schema.mjs`: Node-side schema smoke test.
- Create `scripts/test-rewrite-format.mjs`: Node-side rewrite formatting test.
- Create `blog/test_product_schema.py`: Python-side schema tests.
- Create `blog/test_user_preferences.py`: behavior learning tests.
- Create `blog/ingest_jobs.py`: local JSON job state manager.
- Create `blog/ingest_worker.py`: background worker that runs fetch + refresh and updates job state.
- Create `blog/test_ingest_jobs.py`: ingest job state tests.
- Create `blog/test_app_routes.py`: Flask route/template smoke tests.
- Modify `blog/today_signal.py`: freshness state and attention evidence status.
- Modify `blog/app.py`: signal state rendering inputs, ingest status endpoints.
- Modify `blog/templates/_signals.html`: freshness banners, pending evidence, ingest status UI.
- Modify `blog/templates/detail.html`: related cover uses `cover_url` first.
- Modify `blog/user_preferences.py`: no logic change expected unless tests expose edge cases.
- Modify `config/preferences.json`: add missing event weights.
- Modify `scripts/rewrite.js`: new score labels and importable formatter.
- Modify `scripts/sync-feishu.js`: topic options from schema.
- Modify `README.md`: targeted stale scoring/runtime wording only.

## Task 1: Shared Product Schema

**Files:**
- Create: `config/product_schema.json`
- Create: `blog/product_schema.py`
- Create: `scripts/product-schema.js`
- Create: `blog/test_product_schema.py`
- Create: `scripts/test-product-schema.mjs`
- Modify: `blog/app.py`
- Modify: `scripts/sync-feishu.js`

**Interfaces:**
- Produces Python:
  - `product_schema.TOPICS: list[str]`
  - `product_schema.UNKNOWN_TOPIC: str`
  - `product_schema.SCORE_DIMENSIONS: list[dict]`
  - `product_schema.normalize_topic(value: str) -> str`
- Produces Node:
  - `loadProductSchema(): object`
  - `topics(): string[]`
  - `normalizeTopic(value: string): string`
  - `scoreDimensions(): Array<{key:string,label:string,max:number}>`
- Consumes existing topic usage in `blog/app.py` and `scripts/sync-feishu.js`.

- [ ] **Step 1: Write failing Python schema test**

Add `blog/test_product_schema.py`:

```python
"""Shared product schema tests.

Run: blog/.venv/bin/python blog/test_product_schema.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import product_schema as schema


def test_topics_include_ai_frontier_and_unknown_falls_back():
    assert schema.TOPICS == [
        "AI 前沿", "AI 编程", "AI 产品", "AI 创业",
        "AI 商业", "投资", "个人效率", "其他",
    ]
    assert schema.normalize_topic("AI 前沿") == "AI 前沿"
    assert schema.normalize_topic(" 不存在的话题 ") == "其他"
    assert schema.normalize_topic("") == "其他"
    print("✓ topics schema")


def test_score_dimensions_are_current_three_axis():
    assert schema.SCORE_DIMENSIONS == [
        {"key": "insight", "label": "洞察原创", "max": 50},
        {"key": "source", "label": "信源质量", "max": 25},
        {"key": "storytelling", "label": "故事可读", "max": 25},
    ]
    print("✓ score dimensions schema")


if __name__ == "__main__":
    test_topics_include_ai_frontier_and_unknown_falls_back()
    test_score_dimensions_are_current_three_axis()
    print("\n全部通过 ✅")
```

- [ ] **Step 2: Run Python schema test and verify it fails**

Run:

```bash
blog/.venv/bin/python blog/test_product_schema.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'product_schema'`.

- [ ] **Step 3: Add shared JSON schema**

Create `config/product_schema.json`:

```json
{
  "topics": [
    "AI 前沿",
    "AI 编程",
    "AI 产品",
    "AI 创业",
    "AI 商业",
    "投资",
    "个人效率",
    "其他"
  ],
  "unknown_topic": "其他",
  "score_dimensions": [
    { "key": "insight", "label": "洞察原创", "max": 50 },
    { "key": "source", "label": "信源质量", "max": 25 },
    { "key": "storytelling", "label": "故事可读", "max": 25 }
  ]
}
```

- [ ] **Step 4: Add Python schema helper**

Create `blog/product_schema.py`:

```python
"""Shared product schema for topics and score dimensions."""

import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
SCHEMA_PATH = ROOT / "config" / "product_schema.json"


def _load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


_SCHEMA = _load_schema()
TOPICS = list(_SCHEMA["topics"])
UNKNOWN_TOPIC = str(_SCHEMA.get("unknown_topic") or "其他")
SCORE_DIMENSIONS = list(_SCHEMA["score_dimensions"])


def normalize_topic(value):
    topic = str(value or "").strip()
    return topic if topic in TOPICS else UNKNOWN_TOPIC
```

- [ ] **Step 5: Replace hardcoded topics in Flask app**

In `blog/app.py`, add near other local imports:

```python
from product_schema import TOPICS
```

Then remove the hardcoded line:

```python
TOPICS = ['AI 前沿', 'AI 产品', 'AI 创业', 'AI 商业', 'AI 编程', '投资', '个人效率', '其他']
```

- [ ] **Step 6: Add Node schema helper**

Create `scripts/product-schema.js`:

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '..');
const SCHEMA_PATH = path.join(PROJECT_ROOT, 'config', 'product_schema.json');

export function loadProductSchema() {
  return JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf-8'));
}

export function topics() {
  return loadProductSchema().topics.slice();
}

export function normalizeTopic(value) {
  const schema = loadProductSchema();
  const topic = String(value || '').trim();
  return schema.topics.includes(topic) ? topic : schema.unknown_topic;
}

export function scoreDimensions() {
  return loadProductSchema().score_dimensions.slice();
}
```

- [ ] **Step 7: Add Node schema test**

Create `scripts/test-product-schema.mjs`:

```javascript
import assert from 'node:assert/strict';
import { topics, normalizeTopic, scoreDimensions } from './product-schema.js';

assert.deepEqual(topics(), [
  'AI 前沿', 'AI 编程', 'AI 产品', 'AI 创业',
  'AI 商业', '投资', '个人效率', '其他',
]);
assert.equal(normalizeTopic('AI 前沿'), 'AI 前沿');
assert.equal(normalizeTopic('未知话题'), '其他');
assert.deepEqual(scoreDimensions(), [
  { key: 'insight', label: '洞察原创', max: 50 },
  { key: 'source', label: '信源质量', max: 25 },
  { key: 'storytelling', label: '故事可读', max: 25 },
]);
console.log('✓ product schema');
```

- [ ] **Step 8: Use schema in Feishu sync**

In `scripts/sync-feishu.js`, add:

```javascript
import { topics, normalizeTopic } from './product-schema.js';
```

Change topic assignment in `buildBitableRecord`:

```javascript
if (metadata.topic) {
  record['话题'] = normalizeTopic(metadata.topic);
}
```

Replace:

```javascript
const TOPIC_OPTIONS = ['AI 编程', 'AI 产品', 'AI 创业', 'AI 商业', '投资', '个人效率', '其他'];
```

with:

```javascript
const TOPIC_OPTIONS = topics();
```

- [ ] **Step 9: Run schema tests**

Run:

```bash
blog/.venv/bin/python blog/test_product_schema.py
node scripts/test-product-schema.mjs
node --check scripts/sync-feishu.js
```

Expected: all pass; Node test prints `✓ product schema`.

- [ ] **Step 10: Commit Task 1**

```bash
git add config/product_schema.json blog/product_schema.py blog/test_product_schema.py scripts/product-schema.js scripts/test-product-schema.mjs blog/app.py scripts/sync-feishu.js
git commit -m "feat: share product schema across app and sync"
```

- [ ] **Step 11: Evaluator gate**

Run the evaluator prompt from the global gate for Task 1. Fix valid findings and recommit with:

```bash
git commit --amend --no-edit
```

## Task 2: Signal Freshness State and Homepage Messaging

**Files:**
- Modify: `blog/today_signal.py`
- Modify: `blog/app.py`
- Modify: `blog/templates/_signals.html`
- Modify: `blog/test_today_signal.py`
- Create or modify: `blog/test_app_routes.py`

**Interfaces:**
- Produces `today_signal.signal_freshness(payload: dict, now_ts: float | None = None, profile: dict | None = None) -> dict`
- Produces `today_signal.with_signal_freshness(payload: dict, now_ts: float | None = None, profile: dict | None = None) -> dict`
- Produces `today_signal.missing_signal_state(profile: dict | None = None) -> dict`
- `read_signal_cache()` returns enriched cache for valid/invalid cache; returns `None` only when file is missing.

- [ ] **Step 1: Add failing freshness tests**

Append to `blog/test_today_signal.py`:

```python
def test_signal_freshness_daily_window():
    profile = {"delivery": {"hour": 8, "minute": 30}}
    payload = {"generated_at": "2026-07-07 08:31", "signals": []}
    fresh = ts.signal_freshness(payload, now_ts=1783371600, profile=profile)
    assert fresh["status"] == "fresh", fresh
    assert fresh["label"] == "新鲜"
    expired = ts.signal_freshness(payload, now_ts=1783451461, profile=profile)
    assert expired["status"] == "expired", expired
    assert expired["is_expired"] is True
    print("✓ 今日判断按每日 8:30 窗口判断 freshness")


def test_missing_signal_state():
    state = ts.missing_signal_state({"delivery": {"hour": 8, "minute": 30}})
    assert state["freshness"]["status"] == "missing"
    assert state["signals"] == []
    assert state["attention"] == []
    print("✓ 缺失今日判断缓存有显式状态")
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```bash
blog/.venv/bin/python blog/test_today_signal.py
```

Expected: FAIL with `AttributeError` for `signal_freshness` or `missing_signal_state`.

- [ ] **Step 3: Implement freshness helpers**

Add to `blog/today_signal.py` near cache helpers:

```python
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
```

- [ ] **Step 4: Update cache reader**

Replace `read_signal_cache()` in `blog/today_signal.py` with:

```python
def read_signal_cache():
    """页面侧：只读完整缓存，永不触发生成（绝不阻塞网页请求）。"""
    if not SIGNAL_CACHE.exists():
        return None
    try:
        payload = json.loads(SIGNAL_CACHE.read_text(encoding="utf-8"))
    except Exception:
        state = missing_signal_state()
        state["freshness"] = {
            "status": "invalid",
            "is_expired": True,
            "age_hours": None,
            "expires_at": "",
            "label": "读取失败",
            "message": "今日判断读取失败，首页其他内容仍可查看。",
        }
        return state
    return with_signal_freshness(payload)
```

- [ ] **Step 5: Update Flask index fallback**

In `blog/app.py`, when `cached is None`, set `signal_meta` to `today_signal.missing_signal_state()` before rendering:

```python
cached = today_signal.read_signal_cache()
signal_ran = cached is not None
signal_meta = today_signal.enrich_cached_link_quotes(
    cached if cached is not None else today_signal.missing_signal_state(),
    records,
)
```

- [ ] **Step 6: Update signal template banner**

In `blog/templates/_signals.html`, inside `.signals-sub`, add status:

```jinja2
{% if signal_meta.freshness %}
 · {{ signal_meta.freshness.label }}
{% endif %}
```

Below the header, add:

```jinja2
{% if signal_meta.freshness and signal_meta.freshness.status in ['expired', 'missing', 'invalid'] %}
<div class="signals-state signals-state-{{ signal_meta.freshness.status }}">
    {{ signal_meta.freshness.message }}
</div>
{% endif %}
```

Add compact CSS to the existing signals CSS section:

```css
.signals-state {
    margin: 0 0 12px;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(255,255,255,.72);
    border: 1px solid rgba(37,99,235,.18);
    color: #61708A;
    font-size: 13px;
    line-height: 1.55;
}
.signals-state-expired,
.signals-state-invalid {
    border-color: rgba(245,158,11,.35);
    background: #FFF7ED;
    color: #92400E;
}
```

- [ ] **Step 7: Add Flask render smoke test**

Create or append to `blog/test_app_routes.py`:

```python
"""Flask route smoke tests.

Run: blog/.venv/bin/python blog/test_app_routes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import app


def test_homepage_renders():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "降噪" in resp.get_data(as_text=True)
    print("✓ homepage renders")


if __name__ == "__main__":
    test_homepage_renders()
    print("\n全部通过 ✅")
```

- [ ] **Step 8: Run tests**

```bash
blog/.venv/bin/python blog/test_today_signal.py
blog/.venv/bin/python blog/test_app_routes.py
```

Expected: both pass.

- [ ] **Step 9: Commit Task 2**

```bash
git add blog/today_signal.py blog/app.py blog/templates/_signals.html blog/static/css/style.css blog/test_today_signal.py blog/test_app_routes.py
git commit -m "feat: show trusted freshness state for today signals"
```

- [ ] **Step 10: Evaluator gate**

Run evaluator for Task 2. Fix valid findings and amend commit.

## Task 3: Behavior Learning Event Weights

**Files:**
- Modify: `config/preferences.json`
- Create: `blog/test_user_preferences.py`

**Interfaces:**
- Consumes existing `user_preferences.behavior_summary(profile=None) -> dict`.
- Produces no new public API.

- [ ] **Step 1: Add failing behavior test**

Create `blog/test_user_preferences.py`:

```python
"""User preference behavior-learning tests.

Run: blog/.venv/bin/python blog/test_user_preferences.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import user_preferences as prefs


def test_behavior_summary_covers_frontend_events():
    old_path = prefs.CLICK_LOG
    profile = {
        "learning": {
            "enabled": True,
            "days": 90,
            "event_weights": {
                "card": 0.3,
                "open_attention": 0.5,
                "open_news": 0.5,
                "watch_video": 1.0,
                "open_breaking": 1.5,
                "open_local": 1.5,
                "promote_attention": 2.0,
                "deep_library": 3.0,
            },
        }
    }
    with tempfile.TemporaryDirectory() as td:
        prefs.CLICK_LOG = Path(td) / "clicks.log"
        prefs.CLICK_LOG.write_text(
            "\n".join([
                '{"ts":"2026-07-07 08:31:00","kind":"card","slot":"library","source":"archive"}',
                '{"ts":"2026-07-07 08:32:00","kind":"open_attention","slot":"attention","source":"AI HOT"}',
                '{"ts":"2026-07-07 08:33:00","kind":"promote_attention","slot":"attention","source":"AI HOT"}',
                '{"ts":"2026-07-07 08:34:00","kind":"dismiss_attention","slot":"attention","source":"AI HOT"}',
            ]),
            encoding="utf-8",
        )
        summary = prefs.behavior_summary(profile)
    prefs.CLICK_LOG = old_path
    assert summary["events_considered"] == 3
    assert summary["slot_weights"]["attention"] == 2.5
    assert summary["slot_weights"]["library"] == 0.3
    print("✓ behavior weights cover frontend positive events")


if __name__ == "__main__":
    test_behavior_summary_covers_frontend_events()
    print("\n全部通过 ✅")
```

- [ ] **Step 2: Run behavior test**

```bash
blog/.venv/bin/python blog/test_user_preferences.py
```

Expected: test passes because it supplies its own profile. This proves behavior code is compatible before config change.

- [ ] **Step 3: Update `config/preferences.json` weights**

Replace `learning.event_weights` with:

```json
{
  "card": 0.3,
  "open_attention": 0.5,
  "open_news": 0.5,
  "watch_video": 1.0,
  "open_breaking": 1.5,
  "open_local": 1.5,
  "promote_attention": 2.0,
  "deep_library": 3.0
}
```

Do not add `dismiss_attention`.

- [ ] **Step 4: Add config-backed assertion**

Append to `blog/test_user_preferences.py`:

```python
def test_config_preferences_include_actual_positive_events():
    profile = prefs.load_profile()
    weights = (profile.get("learning") or {}).get("event_weights") or {}
    for key in ["card", "open_attention", "open_news", "watch_video", "open_breaking", "open_local", "promote_attention", "deep_library"]:
        assert float(weights.get(key, 0)) > 0, key
    assert float(weights.get("dismiss_attention", 0) or 0) == 0
    print("✓ config preferences include actual positive events")
```

Update the `__main__` block to call both tests:

```python
if __name__ == "__main__":
    test_behavior_summary_covers_frontend_events()
    test_config_preferences_include_actual_positive_events()
    print("\n全部通过 ✅")
```

- [ ] **Step 5: Run behavior tests**

```bash
blog/.venv/bin/python blog/test_user_preferences.py
```

Expected: all pass.

- [ ] **Step 6: Commit Task 3**

```bash
git add config/preferences.json blog/test_user_preferences.py
git commit -m "feat: close behavior learning event loop"
```

- [ ] **Step 7: Evaluator gate**

Run evaluator for Task 3. Fix valid findings and amend commit.

## Task 4: Attention Evidence Status

**Files:**
- Modify: `blog/today_signal.py`
- Modify: `blog/templates/_signals.html`
- Modify: `blog/static/css/style.css`
- Modify: `blog/test_today_signal.py`

**Interfaces:**
- Produces `today_signal.evidence_status(signal: dict) -> str`
- `promote_attention_item()` sets `evidence_status`.
- `enrich_cached_link_quotes()` refreshes `evidence_status` for cached signals.

- [ ] **Step 1: Add failing tests**

Append to `blog/test_today_signal.py`:

```python
def test_evidence_status_for_signal_shapes():
    assert ts.evidence_status({"links": [{"title": "库内"}]}) == "linked"
    assert ts.evidence_status({"suggest": {"title": "外部视频"}}) == "suggested"
    assert ts.evidence_status({"links": [], "suggest": None}) == "pending"
    print("✓ evidence status follows links/suggest/pending")


def test_promoted_attention_without_links_has_pending_evidence():
    old_write = ts._write_signal_cache
    try:
        ts._write_signal_cache = lambda payload: payload
        cache = {
            "signals": [],
            "attention": [{
                "item_id": "hot-pending",
                "title": "一条热议内容",
                "url": "https://example.com/hot",
                "source": "AI HOT",
                "summary": "很多人在讨论。",
                "why": "需要用户确认是否值得看。",
                "suggested_slot": "industry_trend",
            }],
        }
        updated, changed = ts.promote_attention_item(cache, "hot-pending")
    finally:
        ts._write_signal_cache = old_write
    assert changed is True
    assert updated["signals"][0]["manual_promoted"] is True
    assert updated["signals"][0]["evidence_status"] == "pending"
    print("✓ 手动加入但暂无证据时显示 pending")
```

- [ ] **Step 2: Run tests and verify failure**

```bash
blog/.venv/bin/python blog/test_today_signal.py
```

Expected: FAIL with `AttributeError: module 'today_signal' has no attribute 'evidence_status'`.

- [ ] **Step 3: Implement evidence helper**

Add to `blog/today_signal.py` near attention helpers:

```python
def evidence_status(signal):
    if (signal or {}).get("links"):
        return "linked"
    if (signal or {}).get("suggest"):
        return "suggested"
    return "pending"
```

In `promote_attention_item()`, after `manual_promoted` assignment:

```python
signal["evidence_status"] = evidence_status(signal)
```

In `enrich_cached_link_quotes()`, before returning a signal:

```python
signal["evidence_status"] = evidence_status(signal)
```

- [ ] **Step 4: Update template pending state**

In `blog/templates/_signals.html`, inside `render_deep(signal)` after the `elif signal.suggest` branch, add:

```jinja2
    {% elif signal.manual_promoted and signal.evidence_status == 'pending' %}
    <div class="signal-deep signal-deep-pending">
        <div class="signal-deep-label">你手动加入 · 待补证据</div>
        <div class="signal-pending-evidence">已加入判断，下一轮生成会尝试补库内金句或外部深度补充。</div>
    </div>
```

- [ ] **Step 5: Add CSS for pending evidence**

Add near signal deep CSS:

```css
.signal-pending-evidence {
    padding: 10px 12px;
    border-radius: 10px;
    background: #F8FAFC;
    border: 1px dashed rgba(37,99,235,.24);
    color: #61708A;
    font-size: 13px;
    line-height: 1.55;
}
.signal-breaking .signal-pending-evidence {
    background: rgba(255,255,255,.10);
    border-color: rgba(255,255,255,.22);
    color: rgba(255,255,255,.72);
}
```

- [ ] **Step 6: Run tests**

```bash
blog/.venv/bin/python blog/test_today_signal.py
```

Expected: all pass.

- [ ] **Step 7: Commit Task 4**

```bash
git add blog/today_signal.py blog/templates/_signals.html blog/static/css/style.css blog/test_today_signal.py
git commit -m "feat: show evidence state for promoted attention"
```

- [ ] **Step 8: Evaluator gate**

Run evaluator for Task 4. Fix valid findings and amend commit.

## Task 5: Ingest Job Status Feedback

**Files:**
- Create: `blog/ingest_jobs.py`
- Create: `blog/ingest_worker.py`
- Create: `blog/test_ingest_jobs.py`
- Modify: `blog/app.py`
- Modify: `blog/templates/_signals.html`

**Interfaces:**
- Produces `ingest_jobs.content_key(url: str) -> str`
- Produces `ingest_jobs.find_existing_archive(url: str) -> str`
- Produces `ingest_jobs.start_job(url: str, title: str = "", launch: bool = True) -> dict`
- Produces `ingest_jobs.get_job(job_id: str) -> dict | None`
- Produces `ingest_jobs.update_job(job_id: str, **patch) -> dict`
- Produces route `GET /ingest/status?job_id=<job_id>`
- Changes `POST /ingest` response from `{"status":"started"}` to full job JSON.

- [ ] **Step 1: Add failing job tests**

Create `blog/test_ingest_jobs.py`:

```python
"""Ingest job state tests.

Run: blog/.venv/bin/python blog/test_ingest_jobs.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ingest_jobs as jobs


def test_content_key_youtube():
    assert jobs.content_key("https://www.youtube.com/watch?v=abcdefghijk") == "yt:abcdefghijk"
    assert jobs.content_key("https://youtu.be/abcdefghijk") == "yt:abcdefghijk"
    print("✓ youtube content key")


def test_job_lifecycle_without_launch():
    old_path = jobs.JOBS_PATH
    try:
        with tempfile.TemporaryDirectory() as td:
            jobs.JOBS_PATH = Path(td) / "jobs.json"
            job = jobs.start_job("https://www.youtube.com/watch?v=abcdefghijk", "视频", launch=False)
            assert job["status"] == "queued"
            assert job["job_id"] == "yt:abcdefghijk"
            running = jobs.update_job(job["job_id"], status="running", message="正在抓取和改写")
            assert running["status"] == "running"
            done = jobs.update_job(job["job_id"], status="done", message="已加入深度库", return_code=0)
            assert done["status"] == "done"
            assert jobs.get_job(job["job_id"])["message"] == "已加入深度库"
    finally:
        jobs.JOBS_PATH = old_path
    print("✓ job lifecycle")


if __name__ == "__main__":
    test_content_key_youtube()
    test_job_lifecycle_without_launch()
    print("\n全部通过 ✅")
```

- [ ] **Step 2: Run job tests and verify failure**

```bash
blog/.venv/bin/python blog/test_ingest_jobs.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ingest_jobs'`.

- [ ] **Step 3: Implement `blog/ingest_jobs.py`**

Create `blog/ingest_jobs.py`:

```python
"""Local ingest job state for adding YouTube videos to the deep library."""

import json
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).parent.parent
DATA_DIR = Path(__file__).parent / "data"
JOBS_PATH = DATA_DIR / "ingest_jobs.json"
ARCHIVE_ROOT = ROOT / "archive"
YOUTUBE_RE = re.compile(r'^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})')
VALID_STATUSES = {"queued", "running", "done", "exists", "failed"}


def now_str():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def content_key(url):
    match = re.search(r'(?:youtu\.be/|[?&]v=)([A-Za-z0-9_-]{11})', str(url or ""))
    return "yt:" + match.group(1) if match else ""


def video_id_from_key(job_id):
    return job_id[3:] if str(job_id or "").startswith("yt:") else ""


def load_jobs():
    if not JOBS_PATH.exists():
        return {}
    try:
        return json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_jobs(jobs):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    JOBS_PATH.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")


def get_job(job_id):
    return load_jobs().get(str(job_id or ""))


def update_job(job_id, **patch):
    jobs = load_jobs()
    job = dict(jobs.get(job_id) or {"job_id": job_id, "created_at": now_str()})
    job.update(patch)
    job["updated_at"] = now_str()
    jobs[job_id] = job
    save_jobs(jobs)
    return job


def find_existing_archive(url):
    key = content_key(url)
    if not key or not ARCHIVE_ROOT.exists():
        return ""
    video_id = video_id_from_key(key)
    for mp in ARCHIVE_ROOT.glob("*/metadata.json"):
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if meta.get("id") == video_id or content_key(meta.get("url") or "") == key:
            return str(mp.parent)
    return ""


def launch_worker(job_id):
    subprocess.Popen(
        [str(Path(__file__).parent / ".venv" / "bin" / "python"), str(Path(__file__).parent / "ingest_worker.py"), job_id],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def start_job(url, title="", launch=True):
    if not YOUTUBE_RE.match(str(url or "")):
        return {"status": "bad_url", "message": "只支持 YouTube 视频链接"}
    job_id = content_key(url)
    existing_archive = find_existing_archive(url)
    if existing_archive:
        return update_job(
            job_id,
            url=url,
            title=title,
            status="exists",
            message="已在深度库",
            archive_dir=existing_archive,
            return_code=0,
        )
    current = get_job(job_id)
    if current and current.get("status") in {"queued", "running"}:
        return current
    job = update_job(
        job_id,
        url=url,
        title=title,
        status="queued",
        message="已提交",
        archive_dir="",
        return_code=None,
    )
    if launch:
        launch_worker(job_id)
    return job
```

- [ ] **Step 4: Implement worker**

Create `blog/ingest_worker.py`:

```python
"""Background ingest worker.

Run: blog/.venv/bin/python blog/ingest_worker.py yt:VIDEO_ID
"""

import subprocess
import sys
from pathlib import Path

import ingest_jobs as jobs


ROOT = Path(__file__).parent.parent


def _run(cmd):
    return subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=1800,
    )


def main(job_id):
    job = jobs.get_job(job_id)
    if not job:
        raise SystemExit(f"missing job: {job_id}")
    url = job.get("url") or ""
    jobs.update_job(job_id, status="running", message="正在抓取和改写")
    fetch_cmd = [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "fetch.py"), "--url", url]
    fetch = _run(fetch_cmd)
    if fetch.returncode != 0:
        detail = ((fetch.stderr or "") + "\n" + (fetch.stdout or "")).strip()[-500:]
        jobs.update_job(job_id, status="failed", message=f"入库失败：{detail}", return_code=fetch.returncode)
        return
    refresh = _run(["bash", str(ROOT / "run.sh"), "refresh"])
    if refresh.returncode != 0:
        detail = ((refresh.stderr or "") + "\n" + (refresh.stdout or "")).strip()[-500:]
        jobs.update_job(job_id, status="failed", message=f"刷新失败：{detail}", return_code=refresh.returncode)
        return
    archive = jobs.find_existing_archive(url)
    jobs.update_job(job_id, status="done", message="已加入深度库", archive_dir=archive, return_code=0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: ingest_worker.py <job_id>")
    main(sys.argv[1])
```

- [ ] **Step 5: Update Flask ingest routes**

In `blog/app.py`, import `ingest_jobs` inside routes. Replace `/ingest` body with:

```python
@app.route("/ingest", methods=["GET", "POST"])
def ingest():
    """加入深度库：创建本地 job，后台抓取 YouTube → 改写 → 重建索引。"""
    import ingest_jobs
    body = request.get_json(silent=True) or {}
    url = body.get("url") or request.args.get("url", "")
    title = body.get("title") or request.args.get("title", "")
    job = ingest_jobs.start_job(url, title=title)
    if job.get("status") == "bad_url":
        return job, 400
    return job


@app.route("/ingest/status")
def ingest_status():
    import ingest_jobs
    job_id = request.args.get("job_id", "")
    job = ingest_jobs.get_job(job_id)
    if not job:
        return {"status": "not_found"}, 404
    return job
```

- [ ] **Step 6: Update signal UI JavaScript**

In `blog/templates/_signals.html`, replace the `.signal-ingest-btn` fetch handling with polling logic:

```javascript
function renderIngestButton(b, job) {
    var status = job.status || '';
    b.dataset.jobId = job.job_id || b.dataset.jobId || '';
    if (status === 'queued') b.textContent = '已提交';
    else if (status === 'running') b.textContent = '入库中…';
    else if (status === 'done') { b.textContent = '已加入深度库'; b.disabled = true; }
    else if (status === 'exists') { b.textContent = '已在深度库'; b.disabled = true; }
    else if (status === 'failed') { b.textContent = '入库失败'; b.disabled = false; b.title = job.message || '入库失败'; }
}
function pollIngest(b) {
    var jobId = b.dataset.jobId || '';
    if (!jobId) return;
    fetch('/ingest/status?job_id=' + encodeURIComponent(jobId))
        .then(function (r) { return r.json(); })
        .then(function (job) {
            renderIngestButton(b, job);
            if (job.status === 'queued' || job.status === 'running') {
                setTimeout(function () { pollIngest(b); }, 3000);
            }
        })
        .catch(function () {
            b.textContent = '状态未知';
            b.disabled = false;
        });
}
```

Then after the `/ingest` fetch succeeds:

```javascript
.then(function (job) {
    renderIngestButton(b, job);
    if (job.job_id && (job.status === 'queued' || job.status === 'running')) {
        pollIngest(b);
    }
})
```

- [ ] **Step 7: Run ingest tests**

```bash
blog/.venv/bin/python blog/test_ingest_jobs.py
blog/.venv/bin/python -m py_compile blog/ingest_jobs.py blog/ingest_worker.py blog/app.py
```

Expected: all pass.

- [ ] **Step 8: Commit Task 5**

```bash
git add blog/ingest_jobs.py blog/ingest_worker.py blog/test_ingest_jobs.py blog/app.py blog/templates/_signals.html
git commit -m "feat: track deep-library ingest job status"
```

- [ ] **Step 9: Evaluator gate**

Run evaluator for Task 5. Fix valid findings and amend commit.

## Task 6: Score Wording and README Cleanup

**Files:**
- Modify: `scripts/rewrite.js`
- Create: `scripts/test-rewrite-format.mjs`
- Modify: `README.md`

**Interfaces:**
- Produces `formatScores(scores)` export from `scripts/rewrite.js`.
- Existing CLI behavior remains `node scripts/rewrite.js <archive_dir>`.

- [ ] **Step 1: Add failing rewrite format test**

Create `scripts/test-rewrite-format.mjs`:

```javascript
import assert from 'node:assert/strict';
import { formatScores } from './rewrite.js';

const markdown = formatScores({
  insight: { score: 42, reason: '有反直觉洞察' },
  source: { score: 23, reason: '一手信源' },
  storytelling: { score: 18, reason: '结构清晰' },
  total: 83,
  verdict: '强烈推荐',
});

assert.match(markdown, /洞察原创/);
assert.match(markdown, /信源质量/);
assert.match(markdown, /故事可读/);
assert.doesNotMatch(markdown, /AI 相关性/);
assert.doesNotMatch(markdown, /加分项/);
console.log('✓ rewrite score format');
```

- [ ] **Step 2: Run test and verify failure**

```bash
node scripts/test-rewrite-format.mjs
```

Expected: FAIL because `rewrite.js` does not export `formatScores` and still runs `main()` on import.

- [ ] **Step 3: Make `rewrite.js` import-safe**

At the top of `scripts/rewrite.js`, change import:

```javascript
import { fileURLToPath, pathToFileURL } from 'url';
import { scoreDimensions } from './product-schema.js';
```

At the bottom, replace:

```javascript
main();
```

with:

```javascript
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main();
}

export { formatScores };
```

- [ ] **Step 4: Update score formatter**

Replace the `dims` array in `formatScores` with:

```javascript
const dims = scoreDimensions().map(d => ({
  label: d.label,
  key: d.key,
  max: d.max,
}));
```

Remove `bonus.items` handling from `formatScores`; current dimensions only need `score` and `reason`.

Replace `scoreDetail` in `writeMetadataMd()` with rows built from `scoreDimensions()`:

```javascript
const scoreDetail = sc.total != null ? `
| 维度 | 得分 | 依据 |
|------|------|------|
${scoreDimensions().map(d => `| ${d.label} | ${sc[d.key]?.score ?? '—'}/${d.max} | ${sc[d.key]?.reason || ''} |`).join('\n')}
` : '';
```

Replace console score line with:

```javascript
console.log(`  评分: ${sc.total}/100 (${sc.verdict})  洞察原创:${sc.insight?.score}  信源质量:${sc.source?.score}  故事可读:${sc.storytelling?.score}`);
```

- [ ] **Step 5: Update README targeted stale wording**

In `README.md`, replace scoring field rows:

```markdown
| 洞察原创 | 数字 | 认知增量得分 0-50 |
| 信源质量 | 数字 | 一手性与稀缺性得分 0-25 |
| 故事可读 | 数字 | 叙事质量得分 0-25 |
```

Replace old document scoring example:

```text
[评分卡片]  综合评分 82/100 ⭐ 强烈推荐
            洞察原创 42/50 | 信源质量 22/25 | 故事可读 18/25
```

If README says blog reads Feishu or port 5000, change to:

```markdown
博客默认读取本地 `archive/`，开发端口为 `5055`。
```

- [ ] **Step 6: Run tests and checks**

```bash
node scripts/test-rewrite-format.mjs
node --check scripts/rewrite.js
rg -n "AI相关性|AI 相关性|加分项|故事性" scripts/rewrite.js README.md
```

Expected: Node test passes; `rg` returns no matches in the checked files.

- [ ] **Step 7: Commit Task 6**

```bash
git add scripts/rewrite.js scripts/test-rewrite-format.mjs README.md
git commit -m "fix: align rewrite scoring wording"
```

- [ ] **Step 8: Evaluator gate**

Run evaluator for Task 6. Fix valid findings and amend commit.

## Task 7: Related Cover Rendering

**Files:**
- Modify: `blog/templates/detail.html`
- Modify: `blog/test_app_routes.py`

**Interfaces:**
- No new public API.
- Template behavior: `r.cover_url` first, then legacy `r.cover_token`, then placeholder.

- [ ] **Step 1: Add failing template test**

Append to `blog/test_app_routes.py`:

```python
def test_detail_related_prefers_cover_url():
    from flask import render_template
    article = {
        "id": "a",
        "title": "主文章",
        "cover_url": "",
        "topic": "AI 前沿",
        "creator": "作者",
        "pub_date": "2026-07-07",
        "duration": 60,
        "link": "https://example.com",
        "platform": "YouTube",
        "score_total": None,
        "guest_info": [],
        "guests": "",
        "key_quotes": [],
        "summary_md": "正文",
        "summary": "正文",
        "why_watch": "",
        "key_insights": "",
    }
    related = [{
        "id": "b",
        "title": "相关文章",
        "cover_url": "/cover-local/archive-dir",
        "platform": "YouTube",
        "topic": "AI 前沿",
        "score": 88,
    }]
    with app.test_request_context("/article/a"):
        html = render_template("detail.html", article=article, related=related)
    assert 'src="/cover-local/archive-dir"' in html
    print("✓ detail related prefers cover_url")
```

Update `__main__` to call it:

```python
if __name__ == "__main__":
    test_homepage_renders()
    test_detail_related_prefers_cover_url()
    print("\n全部通过 ✅")
```

- [ ] **Step 2: Run test and verify failure**

```bash
blog/.venv/bin/python blog/test_app_routes.py
```

Expected: FAIL because template currently checks `r.cover_token`.

- [ ] **Step 3: Update detail related cover template**

In `blog/templates/detail.html`, replace the related cover block with:

```jinja2
{% if r.cover_url %}
<img src="{{ r.cover_url }}" alt="{{ r.title }}" loading="lazy">
{% elif r.cover_token %}
<img src="/cover/{{ r.cover_token }}" alt="{{ r.title }}" loading="lazy">
{% else %}<div class="d-related-ph"></div>{% endif %}
```

- [ ] **Step 4: Run route tests**

```bash
blog/.venv/bin/python blog/test_app_routes.py
```

Expected: all pass.

- [ ] **Step 5: Commit Task 7**

```bash
git add blog/templates/detail.html blog/test_app_routes.py
git commit -m "fix: render local covers in related cards"
```

- [ ] **Step 6: Evaluator gate**

Run evaluator for Task 7. Fix valid findings and amend commit.

## Task 8: Full Verification and Adversarial Pressure Test

**Files:**
- Modify only if verification reveals a valid bug from Tasks 1-7.

**Interfaces:**
- Produces no new API.

- [ ] **Step 1: Run full Python syntax checks**

```bash
blog/.venv/bin/python -m py_compile blog/app.py blog/today_signal.py blog/embeddings.py blog/user_preferences.py blog/source_reader.py blog/tool_probe.py blog/product_schema.py blog/ingest_jobs.py blog/ingest_worker.py blog/test_today_signal.py blog/test_embeddings.py blog/test_product_schema.py blog/test_user_preferences.py blog/test_ingest_jobs.py blog/test_app_routes.py
```

Expected: no output and exit code 0.

- [ ] **Step 2: Run all Python tests**

```bash
blog/.venv/bin/python blog/test_product_schema.py
blog/.venv/bin/python blog/test_user_preferences.py
blog/.venv/bin/python blog/test_ingest_jobs.py
blog/.venv/bin/python blog/test_today_signal.py
blog/.venv/bin/python blog/test_embeddings.py
blog/.venv/bin/python blog/test_app_routes.py
```

Expected: every file prints `全部通过 ✅`.

- [ ] **Step 3: Run Node checks**

```bash
node scripts/test-product-schema.mjs
node scripts/test-rewrite-format.mjs
node --check scripts/rewrite.js
node --check scripts/sync-feishu.js
node --check scripts/sync-feishu-doc.js
```

Expected: tests print success and syntax checks exit 0.

- [ ] **Step 4: Run Flask smoke**

```bash
blog/.venv/bin/python - <<'PY'
import sys
sys.path.insert(0, 'blog')
from app import app
client = app.test_client()
for path in ['/', '/search?q=AI', '/search?q=最近有什么AI产品趋势']:
    resp = client.get(path)
    print(path, resp.status_code, len(resp.data))
    assert resp.status_code == 200
PY
```

Expected: all three routes print status `200`.

- [ ] **Step 5: Run data consistency scan**

```bash
blog/.venv/bin/python - <<'PY'
import json
from pathlib import Path
schema = json.loads(Path('config/product_schema.json').read_text(encoding='utf-8'))
assert 'AI 前沿' in schema['topics']
assert [d['key'] for d in schema['score_dimensions']] == ['insight', 'source', 'storytelling']
prefs = json.loads(Path('config/preferences.json').read_text(encoding='utf-8'))
weights = prefs['learning']['event_weights']
for key in ['card','open_attention','open_news','watch_video','open_breaking','open_local','promote_attention','deep_library']:
    assert weights.get(key, 0) > 0, key
assert weights.get('dismiss_attention', 0) == 0
print('schema/preferences consistency ok')
PY
```

Expected: prints `schema/preferences consistency ok`.

- [ ] **Step 6: Adversarial pressure test**

Run this script to pressure-test stale/missing/invalid signal states and ingest route failure:

```bash
blog/.venv/bin/python - <<'PY'
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, 'blog')
import today_signal as ts
from app import app

profile = {'delivery': {'hour': 8, 'minute': 30}, 'editorial_rules': {'window_hours': 48}}
fresh = ts.signal_freshness({'generated_at': '2026-07-07 08:31'}, now_ts=1783371600, profile=profile)
expired = ts.signal_freshness({'generated_at': '2026-07-07 08:31'}, now_ts=1783451461, profile=profile)
assert fresh['status'] == 'fresh'
assert expired['status'] == 'expired'

client = app.test_client()
bad = client.post('/ingest', json={'url': 'https://example.com/not-youtube'})
assert bad.status_code == 400
print('adversarial pressure ok')
PY
```

Expected: prints `adversarial pressure ok`.

- [ ] **Step 7: Run whitespace diff check**

```bash
git diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 8: Final evaluator review**

Dispatch evaluator with:

```text
Final review for Today AI Judgment Trust Loop implementation.
Review the cumulative diff against the design spec and implementation plan.
Focus on stale daily judgment trust, behavior learning boundaries, accidental recommendation expansion, job state correctness, dirty-worktree safety, and test adequacy.
Return blocking/non-blocking findings with exact file references.
```

Fix blocking findings. Review/fix loop maximum: 3 rounds.

- [ ] **Step 9: Commit verification fixes if any**

If verification changed code:

```bash
git add <changed-files>
git commit -m "fix: address final trust loop review"
```

If no code changed, do not create an empty commit.

## Task 9: PR, Deploy, and Cleanup Handoff

**Files:**
- No source changes expected.

**Interfaces:**
- Produces final PR/deploy/cleanup handoff.

- [ ] **Step 1: Confirm final git state**

```bash
git status --short --branch
git log --oneline -8
```

Expected: working tree clean in implementation worktree except ignored generated files.

- [ ] **Step 2: Push branch**

```bash
git push -u origin feat/today-judgment-trust-loop
```

Expected: branch pushed.

- [ ] **Step 3: Create PR**

Use this PR title:

```text
Stabilize Today AI Judgment trust loop
```

Use this PR body:

```markdown
## What changed
- Adds trusted freshness states for 今日 AI 判断.
- Shares topic and score schema across Python/Node.
- Closes behavior learning event-weight gaps.
- Shows evidence status for promoted attention items.
- Adds local ingest job status feedback.
- Aligns rewrite score wording with current scoring model.
- Fixes related-card cover rendering from archive `cover_url`.

## Verification
- `blog/.venv/bin/python blog/test_product_schema.py`
- `blog/.venv/bin/python blog/test_user_preferences.py`
- `blog/.venv/bin/python blog/test_ingest_jobs.py`
- `blog/.venv/bin/python blog/test_today_signal.py`
- `blog/.venv/bin/python blog/test_embeddings.py`
- `blog/.venv/bin/python blog/test_app_routes.py`
- `node scripts/test-product-schema.mjs`
- `node scripts/test-rewrite-format.mjs`
- `node --check scripts/rewrite.js`
- `node --check scripts/sync-feishu.js`
- `node --check scripts/sync-feishu-doc.js`
- Flask smoke for `/`, `/search?q=AI`, `/search?q=最近有什么AI产品趋势`
- `git diff --check`

## Product notes
- No user-visible Agent added.
- No instant push added.
- Attention remains a user-confirmed candidate, not an automatic recommendation.
- Ingest status uses local JSON, not an external queue or database.
```

- [ ] **Step 4: Merge after review approval**

After approval and green checks:

```bash
git switch master
git pull --ff-only
git merge --ff-only feat/today-judgment-trust-loop
```

If the hosting platform merges the PR, use:

```bash
git switch master
git pull --ff-only
```

- [ ] **Step 5: Deploy/run local refresh**

Run:

```bash
./run.sh signals
```

Then start the local blog:

```bash
cd blog
.venv/bin/python app.py
```

Open:

```text
http://localhost:5055
```

Verify visually:

- 今日判断 freshness label appears.
- Expired/missing state is visible when applicable.
- Attention promoted item can show pending evidence.
- Ingest button shows submitted/running/done/exists/failed states.

- [ ] **Step 6: Cleanup implementation worktree**

If a linked worktree was used:

```bash
git worktree list
git worktree remove ../content-curation-trust-loop
git branch --delete feat/today-judgment-trust-loop
```

If branch is already merged and local deletion fails due remote tracking, inspect with:

```bash
git branch --merged
```

Then delete only the merged local branch.

## Self-Review

Spec coverage:

- Freshness states: Task 2.
- Topic schema: Task 1.
- Score schema/README cleanup: Task 6.
- Behavior event weights: Task 3.
- Attention evidence status: Task 4.
- Ingest job state: Task 5.
- Related cover rendering: Task 7.
- Verification/adversarial testing: Task 8.
- PR/deploy/cleanup: Task 9.

Placeholder scan:

- No banned placeholder markers or open-ended placeholder steps.
- All tests have exact commands and expected outcomes.
- Every implementation task has exact target files and commit commands.

Type consistency:

- Python schema API names are consistent across Task 1.
- Node schema API names are consistent across Task 1 and Task 6.
- Ingest job status names are consistent across spec, API, UI, and tests.
- `evidence_status` values are exactly `linked`, `suggested`, `pending`.
