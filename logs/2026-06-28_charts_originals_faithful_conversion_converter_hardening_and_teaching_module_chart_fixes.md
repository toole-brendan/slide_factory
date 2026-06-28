# Session log & handoff — `charts_originals` faithful conversions, a deep `convert_slide.py` hardening pass, additive engine params, and chart fixes to the 10 teaching modules

**Date:** 2026-06-28 (continues from the `2026-06-27_*` sessions)
**Project:** `/Users/brendantoole/projects3/slide_factory/` — standalone, pure-stdlib OOXML PowerPoint authoring workspace.
**Build:** `cd style_library && python3 build_deck.py` → `library.pptx`. Pure Python 3.9 stdlib, no deps.
**Status at handoff:** `library.pptx` builds green — **40 slides, 22 charts, 0 XML parse errors, all modules compile**. New `charts_originals/` reference deck builds + renders. **Open dispute:** after the teaching-module fixes the user reported *"most issues are still there"* — the fixes were verified by me via LibreOffice render, but are **not** accepted by the user. Treat the teaching-module work as unverified-by-user. Nothing was committed this session (working tree dirty).

Big picture: the user wanted a **faithful** reference of 10 chart-heavy source slides to compare the curated teaching modules against. We (1) ran the converter to produce `charts_originals/`, (2) discovered the converter was **mis-rendering** several things and did a deep **`convert_slide.py` hardening pass**, (3) added a handful of **additive engine params** to support faithful output, and (4) applied chart fixes to the **10 teaching modules**. At the end the user collected those 10 modules + an audit summary into `~/projects3/charts_to_fix/`.

---

## 0. The reference deck: `charts_originals/` (NEW, at project root)

`/Users/brendantoole/projects3/slide_factory/charts_originals/` — converter output for **10 source slides** of `/Users/brendantoole/projects3/slide_factory_reference_originals.pptx` (display positions = `slideN.xml` filenames 1:1, verified). Tool: `style_library/_tools/convert_slide.py`.

Mapping (source slide → module → the teaching module it is the faithful reference for):

| src | `charts_originals/*.py` | teaching counterpart |
|---|---|---|
| 2 | `status_quo_outlook_offshore_2` | `status_quo_outlook_offshore_2_teaching` |
| 3 | `archetype_comps_1` | `archetype_comps_newbuild_prices_teaching` |
| 5 | `fleet_overview` | `fleet_overview_teaching` |
| 6 | `status_quo_fleet_outlook` | `status_quo_fleet_outlook_teaching` |
| 27 | `archetype_comps_3` (5 charts) | `archetype_comps_shipbuilder_margins_teaching` |
| 29 | `ships_act_volume` | `ships_act_volume_teaching_factory_chart` |
| 30 | `ships_act_plus_volume` | `ships_act_plus_volume_teaching_factory_chart` |
| 31 | `ships_act_captive_demand` | `ships_act_captive_demand_teaching_factory_chart` |
| 35 | `freight_charges` | `freight_charges_teaching` |
| 40 | `production_outlook_separate` | `production_outlook_separate_teaching_factory_chart` |

- Contains `charts_originals/_src/` (the source chart `.xml` + `.xlsb` style templates) and `charts_originals/images/` (2 extracted media). **Per user request the `_src` files were renamed to the module they're used in** (e.g. `slide2_chart2.*` → `status_quo_outlook_offshore_2.*`; the 5 charts of `archetype_comps_3` → `archetype_comps_3_chart0..4.*`), and the `_SRC / "..."` references in each module were rewritten to match. **NOTE:** re-running the converter re-emits `slideN_chartM` names, so the rename script must be re-applied after any regeneration (it lives inline in the build commands; see §2).
- `charts_originals/charts_originals.pptx` — the built reference deck (10 slides, 14 charts).

### Critical architecture note (now in user memory: `converter-emits-pre-refactor-api`)
`convert_slide.py` emits modules against the **PRE-REFACTOR engine API**: `from deck_core.style import ...`, `from deck_core.charts import styled_chart`, and chrome builders (`breadcrumb`/`title_placeholder`/`prelim_chip`/`sources_line`) `from deck_core.primitives`. The **current** engine pruned all of these (`deck_core.style` gone → `deck_core.layout`; `styled_chart`/`_rewrite_chart_caches`/`editable_bundled_chart` removed; chrome moved to `deck_core/chrome.py` and renamed). **So `charts_originals` does NOT build against the current `deck_core`.**

## 1. The build harness for `charts_originals` (scratchpad, NOT in the repo)

To build `charts_originals` faithfully we use a **git-exported pre-prune `deck_core`**:

- Exported `deck_core` at commit **`2b76009`** (the commit just before `3e7dade "Engine prune"`) via `git archive 2b76009 deck_core | tar -x -C <scratch>/preprune_engine/`.
- Runner: `<scratch>/build_charts_originals.py` puts `<scratch>/preprune_engine` on `sys.path` (shadowing the repo `deck_core`), imports the 10 modules by file path, and calls the pre-prune `build_pptx(..., extracted=infra/template, assets=infra/assets, images=charts_originals/images)`.
- `<scratch>` = `/private/tmp/claude-501/-Users-brendantoole-projects3-slide-factory/1fe9c2ef-faf5-45ab-a48c-12431a6f6f1d/scratchpad/` — **ephemeral**; the pre-prune export + runner will need recreating in a future session. The pre-prune engine copy was **also patched** to mirror the engine additions in §3 (text_box `vert`, connector `grad`/`arrow="both"`, run/trun `hyperlink_rid`, `_build` HYPERLINKS, `title_placeholder(cx=)`) so the regenerated modules render.

Verification throughout = LibreOffice: `soffice --headless --convert-to pdf` + `pdftoppm -png`, then read the PNGs. The **true source** was also rendered (`soffice` on `slide_factory_reference_originals.pptx`) for ground-truth diffs.

---

## 2. `convert_slide.py` hardening pass (the bulk of the session)

All edits in `style_library/_tools/convert_slide.py`. Each was diagnosed by diffing the built `charts_originals` against the **true source render / source XML**, not by eye. The converter benefits **all future conversions**.

1. **Arrowhead over-detection** (`parse_cxn`): old code set `arrow=True` if a `<a:headEnd>`/`<a:tailEnd>` element merely *existed*. think-cell writes `<a:tailEnd type="none"/>` to *suppress* the theme default → spurious arrowheads on dashed rules. Fix: only count an end whose `type` is not `None`/`"none"`. Now also captures **head vs tail** separately → emits `arrow="both"/"head"/"tail"/False`.
2. **Dash pattern collapse** (`parse_cxn`/`render_cxn`): old code collapsed any `<a:prstDash>` to a boolean `dashed=True` (always rendered `val="dash"`). Source uses **21 `dash` + 21 `lgDash`**; the boolean mis-rendered every `lgDash`. Fix: capture the exact preset and emit `connector(dash="lgDash")` (skip `"solid"`).
3. **Border width from `lnRef`** (`parse_sp`): an `<a:ln>` with an explicit color but **no `w`** was dropped to the 1pt default. Fix: inherit width from `<p:style><a:lnRef idx>` via the theme `lnStyleLst` (the scenario chip's 1.5pt = idx 2 = 19050).
4. **Run color from `fontRef`** (`parse_run`, threaded `shape_el` through `parse_para`): a run with no explicit fill now inherits `<p:style><a:fontRef>` color (white chip text via `fontRef idx="minor"` → `schemeClr lt1`). **This also recovered the SHIPS Act legend label text** (the `<a:fld>` labels were rendering invisible).
5. **Shadow vs clustering** (`is_simple` + effect capture): shadowed callouts collapsed into a same-style loop lost their `effectLst`. Fix: exclude `rec.get("effects")` shapes from clustering — but **only when the `<a:effectLst>` is non-empty** (an *empty* `<a:effectLst/>` was a truthy string `"<a:effectLst />"` and over-excluded everything; that regressed slide-2 from 3 clusters to 0, then fixed).
6. **Vertical text** (`parse_sp`/`render_sp`/`const_key`): captured `<a:bodyPr vert>` (e.g. `vert270` rotated year ticks) which was being dropped → flattened to horizontal.
7. **Gradient + double-head line** (`parse_cxn`/`render_cxn`): the confidence-scale arrow is a `gradFill` line (`C30C3E`→`008600`, `lin ang=5400000`) with `headEnd`+`tailEnd` triangles. Old code only read `solidFill` → defaulted to BLACK single-arrow. Fix: capture `gradFill` stops + angle and emit `connector(grad=[(0,"C30C3E"),(100000,"008600")], grad_angle=5400000, arrow="both")`. **NB:** `<a:gs>` are under `<a:gsLst>` (initial bug used `gf.findall("gs")` and found none).
8. **Hyperlinks** (`parse_run` captures `hlinkClick r:id`; new `hyperlink_rels()`; `convert()` assigns module rIds **after** chart+image rIds and emits a module-level `HYPERLINKS = [...]` block; `render_run`/`render_trun` emit `run(hyperlink_rid=...)`). 43 external links wired across the deck, URLs XML-escaped, `TargetMode="External"`.
9. **Invisible `noFill` lines** (`parse_cxn`): think-cell stacks an **unfilled** `lgDash` "anchor" line under each visible `dash` rule. Old code ignored `<a:noFill/>`, defaulted to BLACK → **doubled every dashed rule** (this was the "chart lines still wrong" report). Fix: detect `<a:noFill/>` → `color="none"`.
10. **Cluster z-order safety** (new `_bbox_overlap` + `_cluster_z_safe`, gating `detect_clusters`): a cluster is emitted as one loop at the **first** member's z-position, so members jump ahead of any interleaved shape. If an interleaved non-member **overlaps** a later member, clustering is refused (members stay standalone in source order). This fixed the confidence arrow painting over its "Confidence level" label.
11. **Title width** (`detect_chrome`/`render_chrome` + new `HOUSE_TITLE_CX`): a source title narrowed to clear top-right logos was being forced to full house width by `title_placeholder()`, running text under the logos. Fix: carry the source `cx` and emit `title_placeholder(..., cx=IN(...))` when it differs from house width (`> TOL`).

---

## 3. Additive engine params (current `deck_core`, mirrored into the pre-prune harness)

All **backward-compatible**:

- `deck_core/primitives.py`
  - `text_box(..., vert=None)` → injects `<a:bodyPr vert="...">`.
  - `connector(..., arrow=False|True|"tail"|"head"|"both", grad=None, grad_angle=5400000)` → head/tail triangles independently; `grad` = list of `(pos, hex)` stops → `<a:gradFill>` line, overrides `color`.
  - (`run`/`trun` `hyperlink_rid` + `_build.py` `HYPERLINKS` already existed in current engine; **added** to the pre-prune harness copy.)
- `deck_core/chrome.py`
  - `slide_title(..., cx=None)` → overrides the title box width (else `_TITLE_CX`).
  - `Chrome.title_cx` field; `body_slide()` passes it through to `slide_title(cx=)`.
- `deck_core/charts.py`
  - `_bars(..., value_axis_line_color="inherit")` — the **value** axis line independent of the category spine. `"inherit"` = same as `axis_line_color` (back-compat); a hex = that color; `None`/`"none"` = emits an explicit `<a:ln><a:noFill/>` so the renderer does **not** fall back to its default axis line. Forwarded through `column_chart`/`bar_chart`/`combo_chart` `**kwargs`.

---

## 4. Teaching-module chart fixes (10 modules in `style_library/library/slides/`) — USER-DISPUTED

Driven by diffing the freshly-built `library.pptx` against `charts_originals` (the audit `slide_audit.md` is **partially stale** — several modules already carried fixes). Changes made:

- **`ships_act_volume_*` + `ships_act_plus_volume_*`**: `Rule` dataclass extended (`color`, `grad`, `grad_angle`, `arrow` accepts strings); `INITIAL_PHASE_RULES` → `color="none"` (undouble dashed rules); `CONFIDENCE_SCALE_ARROW` → `grad=((0,"C30C3E"),(100000,"008600")), arrow="both"`; `LabelBox` gained `vert`; year ticks → `vert="vert270"`; **paint order** of `CONFIDENCE_SCALE_ARROW` moved *before* `SCALE_LABELS` (label on top).
- **`fleet_overview_teaching`**: `axis_line_color` `WHITE`→`"162029"` (visible category spine), `value_axis_line_color="none"`, `axis_line_width` `3175`→`9525`.
- **`status_quo_fleet_outlook_teaching`**: `show_gridlines` `True`→`False` (source gridlines are `noFill`).
- **`freight_charges_teaching`**: `value_axis_line_color="none"`; moved `Rectangle 326` (gray legend box) paint *before* `_GROUP_CAPTIONS` so "Shoreside charges" sits in front.
- **`archetype_comps_shipbuilder_margins_teaching`**: `SOURCE_EBIT_MARKER_LINE_WIDTH` `9525`→`19050` (thicker gold markers).
- **`production_outlook_separate_*`**: `Chrome(title_cx=IN(10.9))` (clear logos).
- **`status_quo_outlook_offshore_2`** (combo duplicated axes), **`archetype_comps_newbuild_prices`** (bubble plot border), **`ships_act_captive_demand`** (tight-segment labels), **`production_outlook_separate`** (FY32/FY33 sub-labels): left as **accepted native-factory limitations** per the user's earlier decision.

I verified each via LibreOffice render and believed them correct. **The user subsequently reported the issues persist** — so this section is unverified-by-user and likely the next session's starting point.

---

## 5. `~/projects3/charts_to_fix/` (NEW, OUTSIDE this repo)

Per the user's final request: copied the **10 teaching modules** (as-is) to `/Users/brendantoole/projects3/charts_to_fix/` plus a single `AUDIT_ISSUES.md` that lists **every** `slide_audit.md` issue for each of those 10 modules (per-slide notes + the recurring scenario-chip / preliminary-banner / missing-shadow items that name them), **regardless of fix status**.

---

## 6. Handoff / open items

- **Teaching-module fixes are user-disputed.** Re-examine against `charts_to_fix/AUDIT_ISSUES.md` and the `charts_originals` reference renders. Possible causes to check: LibreOffice vs PowerPoint rendering differences (the user may be viewing in PowerPoint), or fixes that look right in `soffice` but not in PowerPoint.
- **Converter ↔ engine drift is unresolved** (memory `converter-emits-pre-refactor-api`). `charts_originals` only builds via the scratchpad pre-prune export, which is ephemeral. A durable fix is to either (a) re-add a `styled_chart` + `deck_core.style` + chrome shim to the current engine, or (b) update `convert_slide.py`'s emit layer to the current API. Neither was done.
- **`charts_originals/_src` rename must be re-applied** after any reconversion (converter re-emits `slideN_chartM`).
- **Nothing committed.** Working tree has the converter, the 4 engine files (`primitives.py`, `chrome.py`, `charts.py`, plus `_build.py` untouched here), the 10 teaching modules, and the new `charts_originals/` dir all dirty.
- Build/verify loop: `cd style_library && python3 build_deck.py` → render with `soffice`/`pdftoppm` → diff pages against `charts_originals`.
