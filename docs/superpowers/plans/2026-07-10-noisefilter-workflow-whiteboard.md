# NoiseFilter Workflow Whiteboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create, visually verify, and publish an editable Feishu whiteboard that explains NoiseFilter's complete content curation and judgment-learning workflow.

**Architecture:** Compose one SVG-based system map in a 1680 × 1180 logical coordinate space using only Feishu-editable native shapes. Render and lint locally, create a Feishu document with a blank whiteboard block, convert the SVG to OpenAPI nodes, overwrite the blank board, then export and visually inspect the live board image.

**Tech Stack:** SVG, `@larksuite/whiteboard-cli@^0.2.12`, `lark-cli` 1.0.63, Feishu Docs and Whiteboard OpenAPI.

## Global Constraints

- Use the Riptide Cobalt palette: cream `#FDF0E0`, cobalt `#375DFE`, paper `#FFFFFF`, ink `#1A2240`, deep cobalt `#2741C0`.
- Use only `rect`, `circle`, `ellipse`, `line`, right-angled `polyline`, `text`, and `tspan`; do not set `font-family`.
- Do not use gradients, filters, patterns, clipping, masks, opacity, shadows, or decorative micro-chrome.
- All arrows must use `marker-end`; no separate arrowhead polygons or chevrons.
- Keep `archive` visually explicit as the current truth source; show Feishu Table and Feishu Docs only as optional outputs.
- Include the full feedback loop: click/adopt/dismiss/ingest → behavior record → judgment learning → next signal selection.
- Never place prompt text, file paths, tool instructions, citations, or the selected style name on the board.

---

### Task 1: Compose the editable SVG system map

**Files:**
- Create: `diagrams/2026-07-10T034507/diagram.svg`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-07-10-noisefilter-workflow-whiteboard-design.md`
- Produces: a self-contained SVG accepted by `whiteboard-cli` with a 1680 × 1180 viewBox

- [ ] **Step 1: Create the artifact directory**

Run: `mkdir -p diagrams/2026-07-10T034507`

Expected: directory exists and contains no files before SVG creation.

- [ ] **Step 2: Create the SVG with exact layout responsibilities**

Use this coordinate map:

```text
Canvas: 0,0 1680×1180 cream
Header: 70,55 1540×115 cobalt
Stage rail: x=70, y=205/505/805, width=190, height=230
Stage 1 panel: 290,205 1320×230
Stage 2 panel: 290,505 1320×230
Stage 3 panel: 290,805 1320×300

Stage 1 nodes:
Sources 330,285 230×92
Fetch 640,285 230×92
Transcribe 950,285 250×92
Raw package 1290,285 250×92

Stage 2 nodes:
Rewrite & score 330,585 245×100
Archive truth source 650,565 285×140
Enrichment 1020,585 230×100
Vector index 1340,585 220×100
Optional Feishu outputs below Archive, connected with dashed lines

Stage 3 nodes:
Flask site 330,875 245×105
Product surfaces 650,855 295×145
User actions 1030,875 245×105
Judgment learning 1350,855 220×145
Feedback connector returns from Judgment learning to Product surfaces
Ingest connector returns from User actions to Sources
```

Each node must have a 24–30 px title and a 17–19 px supporting label, with at least 24 px horizontal padding. Use solid cobalt blocks for stage rails and major emphasis, paper panels for dense labels, and ink borders of 3–4 px.

- [ ] **Step 3: Check SVG medium constraints**

Run:

```bash
rg -n '<polygon|<filter|<pattern|<clipPath|<mask|opacity=|font-family=' diagrams/2026-07-10T034507/diagram.svg
rg -n '<polyline' diagrams/2026-07-10T034507/diagram.svg
```

Expected: first command returns no matches; every polyline in the second command is a right-angled connector carrying `marker-end`.

- [ ] **Step 4: Render and lint the SVG**

Run:

```bash
npx -y @larksuite/whiteboard-cli@^0.2.12 -i diagrams/2026-07-10T034507/diagram.svg -o diagrams/2026-07-10T034507/diagram.png -f svg
npx -y @larksuite/whiteboard-cli@^0.2.12 -i diagrams/2026-07-10T034507/diagram.svg -f svg --check
```

Expected: PNG is created; the checker reports no `text-overflow` errors and no unintended `node-overlap` errors.

### Task 2: Perform local visual QA

**Files:**
- Modify if needed: `diagrams/2026-07-10T034507/diagram.svg`
- Verify: `diagrams/2026-07-10T034507/diagram.png`

**Interfaces:**
- Consumes: rendered PNG from Task 1
- Produces: a clean SVG and PNG ready for Feishu import

- [ ] **Step 1: Inspect the PNG at original resolution**

Check all three stage panels for text overflow, tight padding, accidental overlap, clipped edges, inconsistent arrow direction, and unclear optional-output styling.

Expected: the main path reads left-to-right and the two feedback loops are visible without crossing node text.

- [ ] **Step 2: Apply one targeted correction pass**

Patch only the coordinates, widths, line breaks, or font sizes of defective elements. Do not regenerate the whole SVG.

Expected: every observed issue is addressed in a single patch pass.

- [ ] **Step 3: Re-render and re-run all checks**

Run the two render/lint commands from Task 1 Step 4 and the forbidden-feature checks from Task 1 Step 3.

Expected: all checks pass and the revised PNG is visually clean.

### Task 3: Create and populate the Feishu whiteboard

**Files:**
- Create: `diagrams/2026-07-10T034507/diagram.json`
- Create: `diagrams/2026-07-10T034507/feishu-preview.png`

**Interfaces:**
- Consumes: verified `diagram.svg`
- Produces: Feishu document URL, whiteboard token, OpenAPI node JSON, and live-board preview

- [ ] **Step 1: Create the Feishu document and blank board**

Run:

```bash
lark-cli docs +create --api-version v2 --content '<title>降噪 NoiseFilter · 内容策展与判断学习工作流</title><p>NoiseFilter 当前完整工作流画板。</p><whiteboard type="blank"></whiteboard>' --as user
```

Expected: response has `ok: true`, a document URL, and one whiteboard `block_token` in `data.document.new_blocks`.

- [ ] **Step 2: Export SVG to OpenAPI JSON**

Run:

```bash
npx -y @larksuite/whiteboard-cli@^0.2.12 -i diagrams/2026-07-10T034507/diagram.svg -f svg --to openapi --format json -o diagrams/2026-07-10T034507/diagram.json
```

Expected: `diagram.json` is non-empty and valid JSON.

- [ ] **Step 3: Overwrite the blank board with editable nodes**

Pipe the converter output to `lark-cli whiteboard +update`, using the exact whiteboard token returned in Step 1 and idempotent token `20260710-noisefilter-workflow-v1`.

Expected: update response has `ok: true` and reports created whiteboard nodes.

- [ ] **Step 4: Export the live board image**

Run `lark-cli whiteboard +query` with `--output_as image`, relative output path `diagrams/2026-07-10T034507/feishu-preview.png`, `--overwrite`, and `--as user`.

Expected: `feishu-preview.png` exists and is non-empty.

### Task 4: Verify the live board and deliver

**Files:**
- Verify: `diagrams/2026-07-10T034507/feishu-preview.png`
- Verify: `diagrams/2026-07-10T034507/diagram.json`

**Interfaces:**
- Consumes: live board preview and raw nodes
- Produces: final user-facing Feishu link and rendered image

- [ ] **Step 1: Inspect the Feishu preview at original resolution**

Expected: layout, shapes, fills, connectors, and bounds match the local preview; no label is clipped or obscured.

- [ ] **Step 2: Verify live text colors using raw output**

Run `lark-cli whiteboard +query --output_as raw --as user` and confirm stored fills use the Riptide Cobalt hex values; do not judge text color from PNG export alone.

Expected: raw nodes contain the intended cream, cobalt, paper, ink, and deep-cobalt values.

- [ ] **Step 3: Correct and overwrite only if live QA finds a defect**

Patch the existing SVG in place, re-render locally, re-export OpenAPI JSON, overwrite the same whiteboard with idempotent token `20260710-noisefilter-workflow-v2`, and re-export the preview.

Expected: final live preview passes the same visual checks as the local PNG.

- [ ] **Step 4: Deliver both artifacts**

Return the Feishu document URL and embed `diagrams/2026-07-10T034507/diagram.png` in the response. Mention that the palette can be switched without changing the information architecture.
