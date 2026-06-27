# Session log & handoff — the big engine prune: `style.py`→`layout.py`, a `chrome.py` author-facing layer, hex-literal colors in modules, and the `body_slide(Chrome(...))` convention

**Date:** 2026-06-27 (a later session the same day as `2026-06-27_git_init_*` and `2026-06-27_teaching_module_curation_*`)
**Project:** `/Users/brendantoole/projects3/slide_factory/` — standalone, pure-stdlib OOXML→PPTX authoring workspace.
**Build:** `cd style_library && python3 build_deck.py` → `library.pptx`. Pure Python **3.9.6** stdlib, no deps.
**Status at handoff:** builds green — **40 slides, 22 charts, 23 embeddings**. **NOT committed** — the entire refactor below sits in the working tree uncommitted (the user explicitly asked me to stop running git and leave version control to them). The repo is git (`main`, GitHub `toole-brendan/slide_factory`); HEAD is still `2b76009` from the prior session.

Big picture: this session executed `projects3/transcript_prune.rtf` end-to-end — a directive to turn `deck_core` into **a boring compiler + a small primitive/chart runtime + tiny mechanical tokens**, and push *all* authoring judgment (colors, type sizes, insets, house chrome) into the slide modules / exemplars. Delivered in **3 sequenced, separately-verified stages**: (1) prune dead engine code, (2) rename `style.py`→`layout.py` and migrate every module to hex-literal colors + the `authoring` façade only, (3) build a `chrome.py` author-facing layer and convert every `render()` to `body_slide(CHROME, _body())`. Stages 1–2 and 3a are **byte-neutral** (proven 0/147 rendered parts changed); stage 3b is **visually-neutral** (chrome shapes reorder in z-order but the body box clears them). The user-approved plan lives at `~/.claude/plans/please-read-and-do-spicy-perlis.md`.

**Two explicit user constraints this session:** (a) SKIP the transcript's "keep old chrome names as temporary aliases" advice — rename directly, update all call-sites in lockstep; (b) force `edge/bd/cell/rcell` **module-local** (delete `table_kit.py`, don't re-export), not folded into core.

**Parallel-work caveat:** the user was editing the repo concurrently. `freight_charges_teaching.py` carries an unrelated glyph-geometry refactor (raw `_GEOM_CHECK/_GEOM_CROSS` custGeom blobs → a compact `_cust_geom_from_d` path-DSL) that is **theirs and intentional** ("here to stay"); I migrated on top of it. Two untracked files (`SLIDE_MODULE_ORIGINS.md`, `slide_factory_reference_originals.pptx`) are also theirs.

---

## 0. Pre-flight — the transcript is the spec, but its facts needed ground-truthing

`transcript_prune.rtf` (1918 lines, a multi-turn user↔AI design conversation) is the design. But its hex values, function names, and "what's used" claims were the other agent's recollection, so everything was verified against the real tree first (3 Explore agents + targeted greps). Key corrections to the transcript's assumptions:

- **`styled_chart`/`line_chart` appear in 5/2 modules — but only as docstring prose.** The real `CHARTS = [...]` bindings use only `column_chart`(12), `bubble_chart`(2), `bar_chart`(1), `combo_chart`(1), and a module-local `stacked_area_chart`(2). So all the "source-porting" + unused chart types are genuinely dead in the live corpus.
- **Modules already inline `PT(...)` and explicit insets** — they use **no** named type-size tokens and **no** `INSETS_*`. So the transcript's "delete the type hierarchy / inset presets" was a no-op at the module level; only **color** tokens needed migrating.
- **No module imports chrome geometry/ids/sizes, `LNSPC_*`, `DENSE_BODY_10PT`, `BODY_*`, or `LEFT_MARGIN`** — those count-1 `style` imports are all in engine files (`primitives`/`_build`/`slide_probe`). Every slide module's `style` import was just `IN, PT, <colors>, FONT`.
- **No module imports `deck_core.table_kit`** — `edge/bd/cell/rcell` reached modules only via the `authoring` re-export, so only ~8 façade modules needed local copies.

---

## 1. Stage 1 — engine prune (BYTE-NEUTRAL; 0/147 parts changed)

Removed only provably-dead code, touching no live call-site:

- **`charts.py` −628 lines.** Used an AST cross-reference tool (`ast` node spans + word-boundary ref counts) to prove each delete-target was referenced only by other delete-targets. Removed publics `styled_chart`, `editable_bundled_chart`, `extract_chart_data`, `line_chart`, `waterfall_chart`, `marimekko_chart`, `THINKCELL_BARS` + the privates only they used (`_rewrite_chart_caches`, `_set_cache`, `_series_name/_color`, `_iter_chart_series`, `_cache_node/_values`, `_waterfall_to_stacked_series`, `_allocate_bins`, `_marimekko_to_binned_series`, `_BUNDLED_EMBED_SPECS`). **GOTCHA — kept `_fmt_cache_num` and `_build_line_series`**: the analysis flagged them as referenced by *survivors* (`_sheet_cell`/`_num_cache_xml` for bubble; `_bars` for combo's line overlay), i.e. they're shared with live factories. Deleting them would have broken bubble/combo.
- Deleted `chart_key.py` (0 real uses), `new_slide.py` (starter template; exemplars supersede it).
- Removed unused `cover_layout`/`section_divider_layout` from `primitives.py`.
- `git mv deck_core/slide_probe.py tools/slide_probe.py` — its `parents[1]` sys.path bootstrap still resolves to repo root from `tools/` (both `deck_core/` and `tools/` are direct children of root).
- Replaced `deck_core/AUTHORING_API.md` with a short top-level `AUTHORING.md` (the slide-module contract + the curated import block).

**`_tools/` collateral (flagged, not fixed):** the dead/superseded `style_library/_tools/convert_slide_v1_flat.py` and the active `convert_slide.py` reference removed symbols (`editable_bundled_chart`, and later `deck_core.style`). They are dev converters **outside the build path** (build stays green); their imports are now stale. Left for the user to retire/update.

---

## 2. Stage 2 — `style.py`→`layout.py` + module token/import migration (BYTE-NEUTRAL; 0/147)

- **`layout.py` (NEW, ~50 lines)** holds only mechanical constants: `EMU_PER_INCH`, `IN`, `PT`, `SLIDE_W/H`, `LEFT/RIGHT_MARGIN`, `USABLE_W`, `CONTENT_W`, `BODY_*`/`BODY`/`BODY_R`/`BODY_B`, `DEFAULT_FONT="Arial"`. **`style.py` deleted.**
- **`primitives.py`** repointed to `layout` (only `DEFAULT_FONT as FONT` is still live — `SLIDE_W/H/LEFT_MARGIN/CONTENT_W` turned out to be comment-only once chrome moved). The line-spacing + default-body-size + the locked-chrome colors/geometry/ids were inlined as same-named module constants (names kept identical → zero downstream renaming → guaranteed byte-neutral).
- Repointed `_build.py` and `tools/slide_probe.py` `SLIDE_W/H`/`BODY_*` imports `style`→`layout`.
- **`authoring.py` cut 123→ (then 46) names**: dropped the entire palette, type scale, line-spacing, insets, chrome sizes/ids, `blue_pair/gray_pair/chart_accent_*`, and the `table_kit` re-export. Units/geometry now come from `layout`.
- **All 40 modules migrated by an AST script** (`scratchpad/migrate_modules.py`): consolidated `from deck_core.{primitives,style,charts}` → a single `from deck_core.authoring import (...)`; replaced imported palette tokens with **local hex literals** (`BLACK="000000"`, `BLUE_2="B6C8D8"`, …) + `FONT="Arial"`; injected module-local `edge/bd/cell/rcell` into the 8 façade modules that used them (wiring `tcell/tcell_rich/PT/BLACK/FONT` deps). The 2 `ships_act` stacked-area shims keep their documented private `from deck_core.charts import _build_embed_xlsx` + `from deck_core.ooxml import XML_DECL, NS_CHART`.
- Deleted `table_kit.py`.

**Hex map preserved verbatim from old `style.py`:** `BLUE_1..5 = E2E9EF/B6C8D8/6E91B1/3D5972/263746`; `GRAY_1..5 = F2F2F2/D9D9D9/BFBFBF/7F7F7F/646464`; `BLACK=000000 WHITE=FFFFFF DK=162029 BREADCRUMB=44505C PRELIM=FFFFCC`.

---

## 3. Stage 3a — `chrome.py` author-facing layer + rename (BYTE-NEUTRAL; 0/147)

- **`chrome.py` (NEW)**: moved the 4 chrome builders out of `primitives.py` and **renamed (no aliases)**: `title_placeholder`→`slide_title`, `prelim_chip`→`preliminary_chip`, `sources_line`→`source_note` (`breadcrumb` unchanged). Added `Chrome`/`Sources` frozen dataclasses, `body_slide(chrome, body_xml)`, and `layout_title`/`layout_placeholder` (readable wrappers over `placeholder_sp` for layout-inherited titles). **All chrome geometry/ids/colors/sizes are private** (`_TITLE_X`, `_SP_ID_*`, `_DK`, …).
- `authoring.py` re-exports the chrome layer; the old names removed from the `primitives` re-export.
- Global word-boundary rename of the 3 chrome calls across 39 modules (byte-identical: same output, new name).

---

## 4. Stage 3b — the `body_slide(Chrome(...))` render conversion (VISUALLY-NEUTRAL)

The centerpiece. Each module's `render()` became `return body_slide(CHROME, _body())` with a `CHROME = Chrome(section=…, topic=…, title=…, takeaway=…, preliminary=…, sources=…)` record, and chrome stripped out of `_body()`.

**The safe-conversion trick:** chrome builders return XML strings that get concatenated/joined into the body, so **replacing each chrome call with `""` removes the shape harmlessly** in any context (list element, `out.append(...)`, concat), and `body_slide` re-adds it. An AST converter (`scratchpad/convert_chrome.py`) extracts the breadcrumb/slide_title/preliminary_chip/source_note arg source verbatim into the `Chrome(...)` literal, neutralizes the calls, rewrites `slide(X)`→`body_slide(CHROME, X)`, and rewrites the `authoring` import (drop chrome funcs, add `body_slide, Chrome`).

**GOTCHA — `ast` `col_offset` is a UTF-8 BYTE offset, not a char offset.** The first converter run produced stray-comma syntax errors because slides contain multi-byte chars (curly quotes `'31-'50`). Fix: do all span slicing on `src.encode("utf-8")` (byte offsets) and `.decode()` at the end.

**Why visually-neutral, not byte-neutral:** `body_slide` emits chrome in a fixed position (breadcrumb, title, [prelim], body, [source]) whereas modules previously interleaved it, so the `<p:sp>` z-order changes. But chrome lives in the margins/corners and the BODY box is defined to clear them, so **disjoint regions ⇒ z-order is visually immaterial**. Verified by a **shape-multiset structural diff** (`scratchpad/verify/shapediff.py`): split each slide's `spTree` into top-level shapes, compare as sorted sets. **35 standard modules → 0 shape-set changes** (pure reorder).

---

## 5. The 5 non-standard-chrome modules (user: "make them do the convention too")

5 modules were skipped by the auto-converter because they carried **raw title/breadcrumb OOXML** instead of builder calls (exactly the "raw chrome in modules" the transcript targets). Converted by hand:

- **definitions_market_levels, tcv_approach_iamd** (LAYOUT4, breadcrumb + raw `RAW_TITLE_PLACEHOLDER`): swapped the raw-title append for a `slide_title("Topic", "Takeaway")` call (topic|takeaway split from the raw text), then ran the converter → `body_slide(Chrome(...))`.
- **assumptions_income_statement_1 / _2** (LAYOUT4): their "subtitle"/"body-crumb" placeholder (`<p:ph type="body" idx="10">`, bold "BuildCo Financial Projections" + "/ Assumptions & Methodology") **is a breadcrumb** → `breadcrumb("BuildCo Financial Projections", "Assumptions & Methodology")`; raw title → `slide_title(...)`; then converter.
- **overview** (the lone `slideLayout3` section-opener, bare "Overview" title, custom prelim banner, no breadcrumb): converted its raw `LAYOUT3_TITLE_PLACEHOLDER_XML` to **`layout_title("Overview", sp_id=2000, name="Title 4", body_pr_xml='<a:bodyPr vert="horz"/>')`** and **kept `render() = slide(_body())`**. It does NOT use `body_slide` — that would impose LAYOUT4 title geometry on a LAYOUT3 slide and add an inapplicable breadcrumb. **This is the only one of 40 not on `body_slide` (39/40).**

These 5 are the **only** intentional rendered changes of the whole refactor (5 shape-set diffs): raw black/layout-inherited titles → house `slide_title` (dark-navy `DK`, house geometry — which equals the template title geometry, so position is unchanged) + house breadcrumb. The house chrome geometry is verbatim from the locked slideLayout4 title placeholder, so the title does **not** move; only color/formatting normalize.

**GOTCHA — annotated assignments.** The first dead-constant remover only handled `ast.Assign`; assumptions_2's `TITLE_BLOCK_PLACEHOLDERS: tuple[...] = (...)` is an `ast.AnnAssign` and survived as orphaned raw XML. Removed it (and its now-unused `RawPlaceholder` class) in a follow-up.

To Chrome/Sources: `Chrome` made `section`/`topic` optional (default `None`; `body_slide` skips the breadcrumb when `section is None`) so the no-breadcrumb assumptions slides fit the convention. `Sources` is exported but unused — existing source modules (comparison_vs_ddgs, ships_act volume/plus) pass a pre-formatted string to `Chrome.sources`, which `body_slide` routes straight to `source_note`.

---

## 6. Final state & inventory

```
deck_core/
  _build.py        packager (unchanged but for the layout import)
  ooxml.py         namespaces (unchanged)
  layout.py        NEW  — units + canvas/BODY geometry + DEFAULT_FONT (~50 lines)
  primitives.py    raw emitters only (chrome moved out); 741 lines
  chrome.py        NEW  — Chrome/Sources/body_slide + breadcrumb/slide_title/
                         preliminary_chip/source_note + layout_title/layout_placeholder
  charts.py        native factories + _build_embed_xlsx chain only; 2173 lines (was ~2849)
  authoring.py     curated re-export, 46 names; 56 lines
tools/
  slide_probe.py   dev inspector, out of the runtime package
AUTHORING.md       NEW (replaces deck_core/AUTHORING_API.md)
```
Deleted: `style.py`, `table_kit.py`, `chart_key.py`, `new_slide.py`, `deck_core/AUTHORING_API.md`.

**`authoring` surface (46 names):** units/geometry (`IN, PT, EMU_PER_INCH, SLIDE_W/H, LEFT/RIGHT_MARGIN, USABLE_W, CONTENT_W, BODY*`), chrome (`Chrome, Sources, body_slide, breadcrumb, slide_title, preliminary_chip, source_note, layout_title, layout_placeholder`), primitives (`slide, esc, run, line_break, paragraph, text_box, custom_geometry, picture, connector, trun, tbreak, tpara, tcell, tcell_rich, trow, table`), charts (`graphic_frame, column_chart, bar_chart, combo_chart, bubble_chart`). **No** palette / type sizes / insets / chrome ids / `edge,bd,cell,rcell` / `chart_key`.

**Module corpus:** all 40 import only from `authoring` (the 2 `ships_act` shims excepted, by design); colors are local hex; `FONT="Arial"` local; `edge/bd/cell/rcell` local where used; no raw chrome OOXML anywhere; **39/40 render via `body_slide(CHROME, _body())`** (overview is the LAYOUT3 exception). Unused `slide` import stripped from all 39 converted modules (post-conversion `slide` is only called inside `body_slide`).

**Chart-route taxonomy (unchanged):** native factory (most), module-local `stacked_area_chart` helper (**only** `ships_act_volume_teaching_factory_chart` + `ships_act_plus_volume_teaching_factory_chart`, which still reach private `deck_core.charts._build_embed_xlsx`), `_src` (none).

---

## 7. Verification methodology (reusable; load-bearing this session)

- **Byte-diff harness** (`scratchpad/verify/`): `snapshot.sh` unzips `library.pptx`; `cmanifest.sh` makes a content manifest where each `ppt/embeddings/*.xlsx` is hashed by its **uncompressed** content (the xlsx are zips with embedded timestamps → non-deterministic bytes; hashing inner content removes the false positives). Stages 1/2/3a proved **0/147 parts changed**. **GOTCHA — don't byte-diff the raw .xlsx**; a no-op rebuild changes all 22 of them (timestamp noise).
- **Shape-multiset structural diff** (`shapediff.py`): for non-byte-neutral chrome work, compare each slide's top-level `<p:sp>/<p:pic>/<p:graphicFrame>/<p:cxnSp>` set order-independently. 35 standard modules = 0 changes; the 5 specials = the intended chrome swaps.
- **Invisible-text scanner**: re-run after chrome edits — only the known, intentionally-unfixed slide30 (`ships_act_plus` "(3) SHIPS Act "Plus" Scenario" near-black chip) flags.
- **AST analyzers in scratch** (reusable): `remove_defs.py` (delete named top-level defs by span — but extend it to `AnnAssign`, see §5 gotcha), `analyze_charts.py` (survivor-reference proof before deleting privates), `import_audit.py`/`permod_dump.py` (per-module deck_core import matrix), `migrate_modules.py`, `convert_chrome.py` (byte-offset!).
- Standing checks: 3.9 module-level `X | Y` union grep; "actual read vs comment-mention" grep; **unused-import AST scan** (caught the stale `slide` imports).

---

## 8. Open / deferred

- **NOT committed.** The whole refactor is uncommitted in the working tree (user is handling git, possibly via a branch — note the harness auto-mode blocks direct pushes to `main`). When committing, the suggested split mirrors the stages (engine prune / layout+migration / chrome layer), and `library.pptx` is a tracked build artifact entangled with the user's `freight_charges` glyph edits.
- **overview** stays on `layout_title` + `slide(_body())` (LAYOUT3). Decide whether to force it onto `body_slide` (would move/recolor its title) or leave it.
- **`_tools/` converters** (`convert_slide.py`, `convert_slide_v1_flat.py`) have stale imports to removed symbols (`deck_core.style`, `editable_bundled_chart`). Out of the build path; retire or update.
- **The 5 specials now render house chrome** (DK navy title vs source-black, house breadcrumb formatting) — a deliberate visual change per the user's "do the convention" instruction. Revertable per-module if any should stay source-faithful.
- Optional from before: add a native `stacked_area_chart` engine factory so `ships_act_volume`/`ships_act_plus_volume` drop their local shim (would make every chart module call a shared engine factory). The shims currently depend on private `_build_embed_xlsx`, which is intentionally retained.
- **`Sources` dataclass** is available but unused; future source slides can use `Chrome(sources=Sources(source=..., note=..., y=...))` instead of a raw string.

**The authoring rule now enforced by the corpus:** a slide module reads `from deck_core.authoring import (...)`, defines local hex colors, builds `CHROME = Chrome(...)` + semantic records + `paint_*` functions, and ends with `def render(): return body_slide(CHROME, _body())` — never raw `<p:sp>` chrome, never an imported `BLUE_2`.
