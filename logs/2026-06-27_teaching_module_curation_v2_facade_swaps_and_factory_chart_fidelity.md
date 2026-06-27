# Session log & handoff — teaching-module curation, v2 façade swaps, invisible-text fixes, and factory-chart fidelity (fleet_overview / status_quo)

**Date:** 2026-06-27
**Project:** `/Users/brendantoole/projects3/slide_factory/`
**Build:** `cd slide_factory/style_library && python3 build_deck.py` → `library.pptx`. Pure Python stdlib, no deps.
**Status at handoff:** builds green — **40 slides, 22 charts, 23 embeddings**. Not a git repo.
**Source reference decks (ground truth):** `/Users/brendantoole/projects3/reference/`
- `20251120_Market sizing_Navy (Surface incl MDA)_v2.1.pptx`
- `20251201_Market sizing_Navy (Undersea)_v1.6.pptx`
- `20260116_Market sizing_Golden Dome_v2.0.pptx`
- `20260325_Commercial Strategy_Market Analysis_vS.pptx`

Big picture: this session **curated the slide corpus down toward teaching modules** and **raised their fidelity to the source decks**. We (1) registered a first batch of market-sizing-flow teaching modules and made teaching modules render first; (2) fixed an invisible black-on-black text bug traced to a dropped `<p:style>` fontRef; (3) pruned the corpus by deleting source-faithful originals that had been promoted; (4) swapped in three batches of **v2 teaching modules that migrated to the `deck_core.authoring` façade**; (5) added two **factory-chart** teaching slides (`fleet_overview`, `status_quo_fleet_outlook`) and corrected their chart data/colors against the source chart parts; (6) fixed a legend-overlap regression in `approach_volume_and_price_teaching`. A late experiment to add no-fill axis lines + a plot-area border to the chart engine **was reverted** — see §8.

Environment note: the user's local shell is **TCC-blocked from `~/Downloads` directory listing** (`ls` → "Operation not permitted"), but `cp`/Read of explicit file paths work. Copy modules in with `cp <downloads-path> <dest>`, not globs.

---

## 1. First teaching batch + the render-first convention

Registered 9 market-sizing-flow teaching modules (copied from `~/Downloads/market_sizing_flow_teaching_modules/`) into `style_library/library/slides/` and placed them at the **front** of `SLIDE_RENDERS`. All depended only on assets already present (the source-faithful originals were already registered, so their `images/` and `_src/` assets existed). Two carried `styled_chart(...)` charts off `_src/slide19_chart3.*` and `_src/slide25_chart5.*`; the rest were flow diagrams (`CHARTS=[]`).

**Convention established (and held all session):** *teaching modules render first*, grouped in a single "Teaching exemplars (render first)" block at the top of both the `from . import (...)` block and `SLIDE_RENDERS` in `slides/__init__.py`. Every later teaching add/swap followed this.

---

## 2. Invisible black-on-black text — root cause + fix (GOTCHA)

User reported the `mUSV` box (and others) showing no text on `tcv_approach_usv_teaching`. Root cause, confirmed against the real source slides:

- In the source decks these dark (`fill=BLACK`) platform/ship-class boxes get their **white** text from the shape's `<p:style>` → `<a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef>` (lt1 = white).
- `convert_slide.py` dropped the `<p:style>`/`fontRef`, and `text_box()` emits no font-ref. Runs that had relied purely on that inherited color came out **colorless** → fell back to the theme's dark default → **black-on-black, invisible**. Sibling runs that happened to carry an explicit `FFFFFF` survived (which is why some boxes looked half-right).

**Fix:** add explicit `color=WHITE` to the colorless runs. Applied to the v1 modules on slides 1/5/7 (`Los Angeles`/`Virginia`, `Ticonderoga`/`Arleigh Burke`/`Zumwalt`, `sUSV`/`mUSV`). Later moot for those three because they were swapped to v2 (§4), which already ship the text white.

**Reusable invisible-text scanner** (used repeatedly): unzip `library.pptx`, and for each `<p:sp>` whose shape fill (the spPr `solidFill`, with `<a:ln>` stripped) has luminance < 0.4 and which has **no** `<p:style>`, flag any `<a:t>` run with neither `<a:srgbClr>` nor `<a:schemeClr>`. Scan lives in scratch; rerun after chart/text edits.

**Known, out-of-scope remaining hit:** slide ~30 `ships_act_plus_volume` (source-faithful) has `"(3) SHIPS Act "Plus" Scenario"` on a near-black chip with a colorless run. User explicitly said leave source-faithful slides alone, so it is **intentionally not fixed**.

---

## 3. Prune to teaching-first corpus (deletions)

Per the user, deleted the **11 source-faithful "original counterparts"** that had a teaching twin, plus **2 of the 3 `us_delivery_capacity` teaching variants** (`us_delivery_capacity_teaching.py`, `us_delivery_capacity_teaching_inline_chart.py`) — keeping `us_delivery_capacity_teaching_factory_chart.py`. Updated `slides/__init__.py` to drop all 13 from both blocks (this emptied the "Navy (Undersea)" source group, whose header was removed). Source-faithful modules that **never** had a teaching twin (overview, key_terms_glossary, value_chain comps, status_quo_outlook_*, comparison_vs_ddgs, production_outlook_*, etc.) were kept.

Shared assets under `slides/images/` and `slides/_src/` were left intact (teaching modules still reference them).

---

## 4. v2 swaps — migration to the `deck_core.authoring` façade

Three batches of **v2 teaching modules** were swapped in. These are full rewrites that import from the **`deck_core.authoring` façade** (the §7-deferred "align teaching modules to the façade" direction from the prior session) and use typed dataclasses (`Box`, `FlowNode`, `RunSpec`, `LegendEntry`, `GlyphSpec`, `ConnectorSpec`, etc.) with named `paint_*` layers.

- **In-place swaps (same module names → registry unchanged):**
  - `tcv_flow_teaching_modules_v2/`: `tcv_approach_manned`, `tcv_approach_manned_undersea`, `tcv_approach_usv`, `tcv_to_acv_company_acv_undersea` (`_teaching`). v2 ships the black-on-black text already white, so §2's manual fixes became baked-in.
  - `market_sizing_flow_remaining_teaching_modules_v2/`: `ships_act_overview`, `approach_volume_and_price`, `tcv_approach_iamd`, `tcv_approach_unmanned_undersea`, `tcv_to_acv_company_acv` (`_teaching`).
- **Replace-original swaps (delete source-faithful twin, add teaching to front block):**
  - `value_chain_picture_dense_teaching_modules_v2/`: `value_chain_maritime_transport`, `definitions_market_levels`, `funding_components`, `value_chain_participation` (`_teaching`). `value_chain_participation` is picture-dense (22 images, all already present).

Dependency rule that made every swap safe: the teaching twins reuse the originals' images/`_src`, which were already in the tree.

---

## 5. `fleet_overview_teaching` — factory chart + fidelity fix

Added `fleet_overview_teaching.py` (from `~/Downloads/`), made it **slide 1**, deleted source-faithful `fleet_overview.py`. It is a **factory** chart: `CHARTS = [bar_chart(**CHART_STYLE)]` with `data_point_colors` — no `_src` template/workbook bundled (same philosophy as `us_delivery_capacity_teaching_factory_chart`).

Compared against source `_src/slide42_chart24.xml` and corrected (the as-delivered factory rebuild was a loose approximation):
- **Values** rounded `6.6/3.3/…` → **exact GT** `6628515/3347252/739991/625304/334461/1581507` (renamed field `value_m_gt` → `value_gt`).
- **Total bar color** `BLACK` → **`4C6C9C`** slate-blue (source dPt idx 0). Other bars (`007770` teal, `FFC000` amber, `969696` grey default) already matched.
- **Value axis max** `7` → `6628515` (= the Total), so the Total bar fills the plot exactly as in the source — which also realigned the manual value labels (they'd been positioned for the source's max-equals-total geometry).

Method (reused for §7): unzip the source chart part, extract `barDir`/`grouping`, per-series values + `dPt` idx→color, series default fill, and value-axis min/max/major; then make the factory spec emit the same.

---

## 6. `approach_volume_and_price_teaching` — legend-overlap fix

The v2 swap (§4) introduced a regression: it kept the real track labels (`Price ($)` / `Volume (#)` / `Proportions (%)`) **and** added three invented legend captions (`Calculation output` / `Inputs` / `Solves / assumptions`) at the **same `y=1.163` coordinates**, so they overprinted each other. Source `slide121.xml` has a single interleaved row — `[chip] Price ($)  [chip] Volume (#)  [chip] Proportions (%)` — where the **chip captions ARE the track labels** and the chips carry no text of their own. Fix: simplified `LegendEntry` to a caption-less color-key chip, dropped the invented caption rendering. Verified the rebuilt top band reproduces the source's 6 shapes at the exact x-positions.

---

## 7. `status_quo_fleet_outlook_teaching` — factory chart + fidelity work (ALL reverted in §8)

Added `status_quo_fleet_outlook_teaching.py`, made it **slide 2** (thematic pair after `fleet_overview_teaching`), deleted source-faithful `status_quo_fleet_outlook.py`. Factory chart: `column_chart(mode="stacked")`, values in **K GT** (`÷1000`, exact — no precision loss), axis `−350..350` (proportionally identical to the source's raw `−350000..350000`).

**Color fidelity (done this session, then reverted in §8).** We matched the source's per-bar `dPt` coloring via `data_point_colors`: source recolors the first 5 (orderbook) columns and **swaps** the override between the two stacked series (ser0 default amber w/ idx0-4 teal; ser1 default teal w/ idx0-4 amber; ser2 all teal). This crosses the clean Commercial=teal / Offshore=amber legend in the retirement years — i.e. the **source coloring itself is "messy"**; reproducing it is faithful-to-source, not semantically clean. Note for a redo: the as-delivered Downloads module ships the **flattened** per-series colors (uniform teal/amber), so this dPt work must be re-applied if you want source-faithful coloring.

**Then the styling investigation (gridlines / y-axis / off-white band).** Against `_src/slide43_chart25.xml` + source `slide43.xml`:
- Source `majorGridlines` are `<a:ln><a:noFill/></a:ln>` (invisible); the teaching drew visible `D9D9D9`.
- Source cat+val **axis lines** are `<a:ln><a:noFill/></a:ln>` (invisible); the teaching drew a black cat-axis (zero) line + value-axis line. The y-tick **labels** were already correct (manual text boxes; positions matched the source exactly).
- Source left-side "Years with orderbook data" band is **`fill=None`** (transparent); the teaching filled it `GRAY_1` (the off-white the user saw).
- Source plot area has a **0.75pt black border** (`<c:plotArea>` own spPr, `w=9525`); the factory emits none.

We fixed band fill→None and gridlines off in the module, and **enhanced `deck_core/charts.py`** twice to match the rest: `axis_line_color="none"` → emit `<a:ln><a:noFill/></a:ln>`, and `plot_area_border_color`/`plot_area_border_width` for a plot frame.

---

## 8. The chart-engine experiment was REVERTED — engine is pristine

The plot-area border "looked even more wrong" to the user, who then asked to **undo the `charts.py` changes and revert the slide module to its `~/Downloads/status_quo_fleet_outlook_teaching.py` baseline**. Done:
- `deck_core/charts.py` restored to its pre-session state — **both** additions removed (the `axis_line_color == "none"` no-fill branch **and** the `plot_area_border_color`/`plot_area_border_width` params + plot-area border `spPr` logic + docstrings). Grep confirms zero leftover references.
- `status_quo_fleet_outlook_teaching.py` restored **byte-identical** to the Downloads copy (`diff -q` → IDENTICAL).

**Consequence:** that module is back at its v2 baseline — visible `D9D9D9` gridlines, **black** axis lines, **off-white (`GRAY_1`) band**, **flattened per-series colors** (not the source per-point dPt), and no plot frame. So the §7 fidelity work on this one slide is *not* in the tree. `fleet_overview` (§5) and `approach_volume_and_price` (§6) fixes **are** retained. `charts.py` carries **no** new chart features from this session — if you re-approach the status_quo chart, the `none`/border helpers no longer exist.

Why it looked wrong is unresolved (likely the factory plot-area border rect not aligning with the plotted bars under this `plot_layout`, and/or interaction with the manual axis labels). Re-investigate from a render, not just the XML, before re-adding engine features.

---

## 9. Final state — registry inventory

`slides/__init__.py` `SLIDE_RENDERS`: **40 entries = 17 teaching (render first) + 23 source-faithful.**

Teaching block (slides 1–17, in order):
1 `fleet_overview_teaching` · 2 `status_quo_fleet_outlook_teaching` · 3 `tcv_approach_manned_undersea_teaching` · 4 `approach_volume_and_price_teaching` · 5 `ships_act_overview_teaching` · 6 `tcv_approach_iamd_teaching` · 7 `tcv_approach_manned_teaching` · 8 `tcv_approach_unmanned_undersea_teaching` · 9 `tcv_approach_usv_teaching` · 10 `tcv_to_acv_company_acv_teaching` · 11 `tcv_to_acv_company_acv_undersea_teaching` · 12 `us_delivery_capacity_teaching_factory_chart` · 13 `addressable_demand_teaching` · 14 `value_chain_maritime_transport_teaching` · 15 `definitions_market_levels_teaching` · 16 `funding_components_teaching` · 17 `value_chain_participation_teaching`

Source-faithful (slides 18–40): overview, key_terms_glossary, key_findings_{demand_build_economics, financial_outlook, what_must_be_true}, archetype_comps_{newbuild_prices, vocc_performance, shipbuilder_margins}, status_quo_outlook_{oceangoing, offshore_1, offshore_2}, ships_act_volume, ships_act_plus_volume, ships_act_captive_demand, assumptions_income_statement_{1,2}, approach_unit_economics, freight_charges, coordination_archetypes, key_inputs, comparison_vs_ddgs, production_outlook_{colocated, separate}.

**Chart-delivery taxonomy now in the corpus:** factory (`column_chart`/`bar_chart`, no `_src`): `us_delivery_capacity_teaching_factory_chart`, `fleet_overview_teaching`, `status_quo_fleet_outlook_teaching`. data-over-template (`styled_chart` + bundled `_src` `.xml`/`.xlsb`): `tcv_to_acv_company_acv_teaching` (slide19_chart3), `tcv_to_acv_company_acv_undersea_teaching` (slide25_chart5). Pure table/flow (no chart): everything else.

**Façade status:** the v2 swaps (§4) + `fleet_overview`/`status_quo` import from `deck_core.authoring`. Still on direct `deck_core.primitives/charts/style` imports: `us_delivery_capacity_teaching_factory_chart` and `addressable_demand_teaching` (and the 23 source-faithful modules). A façade-alignment pass on those two would make the teaching corpus uniform.

---

## 10. Gotchas & methodology to reuse

- **Source is ground truth.** "Make it accurate" = match the source chart part / slide, even when the source is internally odd (status_quo's swapped per-bar coloring; raw-GT data under millions/K-GT labels; invisible gridlines/axes with a separate plot border). Verify by unzipping the relevant `reference/*.pptx` slide/chart and byte-comparing.
- **Factory vs styled_chart fidelity:** a factory rebuild is only as faithful as its transcribed spec. Check (a) exact values, (b) per-point `dPt` colors incl. exceptions, (c) axis min/max (proportions), (d) gridlines/axis-line visibility, (e) plot fill/border. `data_point_colors` must be `len == len(categories)`; the factory emits one `<c:dPt>` per index (extra dPt over `None` points are harmless — no bar renders).
- **`<p:style>` fontRef is invisible to the converter.** Any source run that relied on `fontRef lt1` for white text will port colorless → black-on-black on a dark fill. Always run the invisible-text scanner after swaps.
- **TCC:** `~/Downloads` directory listing is blocked; use explicit-path `cp`/Read.
- **Engine changes are reversible and were reverted this session** — `deck_core/charts.py` is back to baseline. Confirm with a render before re-adding axis-line/plot-border features.
- **Verification loop:** after every change, `python3 build_deck.py` (expect 40/22), then unzip + targeted XML extraction (chart values/colors/axes, slide top-band shapes) and the invisible-text scan.
