# Dream Tapir Postcard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate one polished landscape postcard illustration of the original MENGMO dream tapir and its original pocket-tool collection.

**Architecture:** Use the built-in image-generation tool in generation mode, with both supplied images treated only as high-level mood/composition references. Keep the result preview-only, then visually inspect the generated image against the approved character, originality, composition, and text constraints.

**Tech Stack:** Built-in image generation, local visual inspection.

## Global Constraints

- Character: original dream tapir with cloud ears, a short upturned trunk, bean-shaped eyes, freckles, and a hexagonal amber-lit dream-pocket hatch.
- Palette: mist purple, apricot yellow, cream, charcoal, and minor sage accents.
- Format: landscape approximately 3:2, combining a vintage postcard layout with an object-assembled portrait.
- Do not reproduce any existing animated character, recognizable classic gadget, name, logo, silhouette, face construction, costume, or brand color combination.
- Do not use a round blue cat body, circular white face, red round nose, whiskers, red collar, bell, or white semicircular pocket.
- Do not copy the source postcard's text, signature, city postmark, character, or exact arrangement.

---

### Task 1: Generate the First Concept Image

**Files:**
- Reference: `docs/superpowers/specs/2026-07-12-dream-tapir-postcard-design.md`
- Output: preview-only built-in generated image

**Interfaces:**
- Consumes: approved visual design and two conversation reference images.
- Produces: one landscape raster illustration suitable for visual review.

- [ ] **Step 1: Generate one concept image with the built-in image tool**

Use this prompt:

```text
Use case: stylized-concept
Asset type: personal avatar artwork and social-media art postcard
Primary request: Create an original retro-futurist postcard illustration featuring MENGMO, a friendly dream-tapir companion whose portrait is partly assembled from a collection of tiny original dream tools. The result should feel like a private art postcard sent back from the future.
Input images: Image 1 is only a high-level reference for vintage postcard atmosphere, editorial object-collage portraiture, cream paper, and generous postal negative space; do not copy its character, text, signature, postmark, or exact layout. Image 2 is only an emotional reference for a friendly, slightly surprised expression; do not copy its character design, face, colors, pose, or identifiable traits.
Scene/backdrop: Warm cream vintage paper with subtle fibers and restrained offset-print registration; postal divider, a dotted stamp box, sparse address lines, and a small abstract postmark. No city name and no copied writing.
Subject: MENGMO is an unmistakably original dream tapir, not a cat robot: soft-square head, short upturned tapir trunk, asymmetrical cloud-shaped ears, bean-shaped dark eyes, tiny freckles, compact body, and a hexagonal chest hatch called the dream-pocket chamber with rotating petals and warm amber light. The face and silhouette remain readable while the crown, ears, and shoulders are partly constructed from small tools.
Tools: Include at least eight clearly different original objects: split magnetic flight rings, a fold-out polygon space window, inspiration film strips, amber echo capsules, a brass scale dial, translucent language cubes, a ribbon-like dream cassette, a weather tuning fork, an apricot courage button, a charcoal silence bubble, a time bookmark, firefly navigation tubes, asymmetric mood-filter lenses, and a frosted tube of spare moonlight. Their forms must be original small machinery, stationery, glassware, textile, and dream-material hybrids.
Style/medium: Fine ink drawing, colored pencil, restrained watercolor, vintage editorial collage, old magazine print texture, delicate mechanical detail, mostly two-dimensional illustration with a little soft volume. Do not imitate a named living artist.
Composition/framing: Landscape 3:2. MENGMO half-body portrait occupies roughly the left 45 percent; postal negative space occupies roughly the right 55 percent. Keep the eyes, trunk, cloud ears, and hexagonal pocket chamber legible at thumbnail size. Dense but not chaotic.
Lighting/mood: Warm, clever, curious, eccentric, comforting.
Color palette: Mist purple, apricot yellow, cream, charcoal, with small sage accents. Do not use blue-white-red as the dominant combination.
Text (verbatim): only three small labels: "MENGMO", "DREAM POCKET No.01", and "TOOLS FOR QUIET DAYS". Use neat hand-lettered black ink. Add no other readable words.
Constraints: Fully original character and original tools; no watermark; no artist signature; preserve ample clean postcard space; show at least eight distinct tools without hiding the main facial features.
Avoid: any existing copyrighted animated character; any recognizable classic cartoon gadget; round blue cat body; circular white face; red round nose; whiskers; red collar; bell; white semicircular pocket; propeller worn on the head; freestanding rounded rectangle door; bread-shaped memory device; flashlight-like size-changing tool; time machine; trademarked names or logos.
```

- [ ] **Step 2: Confirm the generated asset is visible in the conversation**

Expected: one rendered landscape postcard image appears inline.

### Task 2: Visual Acceptance Check

**Files:**
- Reference: `docs/superpowers/specs/2026-07-12-dream-tapir-postcard-design.md`
- Inspect: generated image from Task 1

**Interfaces:**
- Consumes: Task 1 generated image.
- Produces: acceptance or one targeted regeneration prompt.

- [ ] **Step 1: Check character identity and composition**

Expected observations:

- The subject reads as a tapir through its short trunk and cloud-shaped ears.
- The hexagonal amber dream-pocket hatch is visible.
- The postcard uses a left portrait and right postal-space balance.
- At least eight original tools can be visually distinguished.

- [ ] **Step 2: Check originality constraints**

Expected observations:

- No blue cat silhouette, circular white face, red nose, whiskers, collar, bell, or white semicircular pocket.
- No recognizable classic cartoon gadget shape or trademarked label.
- The source postcard's signature, city mark, receipt copy, and exact character arrangement are absent.

- [ ] **Step 3: Check labels and decide whether regeneration is needed**

Expected: the three requested labels are readable or decorative enough not to distract. If the character or originality checks fail, regenerate once with only the failed constraint strengthened. If only small text is imperfect but the artwork succeeds, accept the concept image as a first-round visual draft.
