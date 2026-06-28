# Session log — making the 10 chart-heavy teaching modules faithful + fully factory-native

**Date:** 2026-06-28 (continues the same day's `2026-06-28_charts_originals_*` session)
**Project:** `/Users/brendantoole/projects3/slide_factory/`
**Build:** `cd style_library && python3 build_deck.py` → `library.pptx` (pure Python 3.9 stdlib, no deps)
**End state:** `library.pptx` builds green — **40 slides, 22 charts, 0 XML errors**. All 10 target slides + 2 bonus slides verified faithful via LibreOffice A/B render. Nothing committed.

---

## Goal & how the approach evolved

Started from a plan to re-derive the 10 chart-heavy teaching modules from the corrected `charts_originals` so they'd be **faithful to the source AND fully factory-native** (no `_src` chart-XML dependency). I began by deriving fixes myself (pilot: `fleet_overview`, `status_quo_outlook_offshore_2`).

Mid-session the user **switched tactics**: they (and a second AI agent) hand-authored refreshed teaching modules in `~/Downloads/`, and my job became **apply + verify** each one. Per-slide workflow:

```
cp "~/Downloads/<module> (N).py"  style_library/library/slides/<module>.py
cd style_library && python3 build_deck.py
# render the new build AND the true source, same slide number:
soffice --headless -env:UserInstallation=file://<scratch>/lo_profile --convert-to pdf --outdir <scratch> library.pptx
pdftoppm -png -r 130 -f N -l N  <scratch>/library.pdf                          <scratch>/new
pdftoppm -png -r 130 -f N -l N  <scratch>/slide_factory_reference_originals.pdf <scratch>/ref
# view new vs ref, confirm match
```

**Key verification fact:** `/Users/brendantoole/projects3/slide_factory_reference_originals.pptx` (parent dir) is the **true source deck**, 40 slides, ordered **1:1 with `library.pptx`'s `SLIDE_RENDERS`** — so library slide N ↔ reference slide N. That's the ground truth for every A/B diff.

Reusable helper written this session: `<scratch>/chart_geom.py` — parses a chart XML and dumps plotArea `manualLayout`, `grouping`/`barDir`/`gapWidth`/`overlap`, per-series values + `dPt` colors, and each axis's `pos`/`delete`/`crosses`/`min`/`max`. Used to tune factory charts to the exact source geometry.

---

## Engine changes (`deck_core/charts.py`) — both backward-compatible

1. **`data_point_colors` `None` → inherit series color.** The per-point `dPt` loop emitted `<a:srgbClr val="{color}"/>` for every entry; a `None` produced `val="None"` (invalid hex → renders **black**). Now `if color is None: continue`, so that point inherits the series fill. Existing all-hex lists are unaffected. *(Needed by `status_quo_fleet_outlook`, whose retirement bars were rendering black.)* The **bubble** factory's `_bubble_dpts_xml` already handled `None` correctly (`continue`), so no change there.

2. **Dual-axis combo primary-axis crossing.** Added `value_axis_crosses: str = "autoZero"` and `cat_axis_crosses: str = "autoZero"` to `_bars(...)`, used in the primary `catAx`/`valAx` emission (replacing the hard-coded `crosses="autoZero"`). A source bar value axis that sits on the **right** uses `catAx crosses="min"` + `valAx crosses="max"`; the default preserves byte-identical output for every existing single-axis chart. *(Needed by `offshore_2`; also used by the archetype combos, `freight_charges`, and both production-outlook combos.)*

These were the only deck_core changes this session. (The combo dual-axis still leaves a **secondary category axis** visible by default → a doubled bottom axis; the user files handle that with a small module-level XML post-process rather than a third engine param — see below.)

---

## The 10 target slides (all verified faithful in LibreOffice)

| Lib # | Module | Chart type | Source | Notable fixes |
|---|---|---|---|---|
| 2 | `status_quo_outlook_offshore_2_teaching` | dual-axis combo (bar + 2 lines) | user file (v3) | crude axis left / adds axis right via `crosses`; **doubled bottom axis** fixed by `_source_align_combo_axes()` post-process (deletes secondary `catAx`, `delete="1"`); solid legend line-keys (were dashed+arrow); underlined "Moderate positive correlation"; native per-bar value labels (idx 16/28/29 suppressed → the 3 manual peak labels) |
| 3 | `archetype_comps_newbuild_prices_teaching` | bubble (73 pts, 7 buckets) | user file (v4) | sparse 73-row buckets; `data_point_colors` with `None` (bubble factory already OK); `_with_source_plot_area_border()` post-process injects the plot-area outline the factory doesn't expose |
| 5 | `fleet_overview_teaching` | single-series stacked bar | **my fix** | `gap_width` 95→**130**, `mode` clustered→**stacked**, exact source `plot_layout` (eyeballed values drifted the bottom bar ~0.09″) |
| 6 | `status_quo_fleet_outlook_teaching` | stacked column (+/− values) | user file (v2) | exact source `plot_layout`/gap/overlap; **needed the `data_point_colors` `None` engine fix** (retirement bars were black) |
| 27 | `archetype_comps_shipbuilder_margins_teaching` | 5 dual-axis combos | user file (v2) | bars native `column_chart`; **EBIT row now a native secondary-axis line** (noFill stroke + native `dash` markers via `line_overlay`); restored right **100/50/0/−50** axis (`show_line_value_axis_labels`); post-process noFills the line, weights the markers, and hides the duplicate `catAx`. *(v1 had drawn EBIT as manual connectors and dropped the right axis — caught and corrected.)* |
| 29 | `ships_act_volume_teaching_factory_chart` | stacked area | user file (v2) | bands + gradient red→green confidence arrow + phase reference lines + vert270 ticks + % badges; hyperlinks wired |
| 30 | `ships_act_plus_volume_teaching_factory_chart` | stacked area | user file (v1) | "Plus" scenario band peaks ~100 @2034 then declines |
| 31 | `ships_act_captive_demand_teaching_factory_chart` | stacked column (2 cats) | user file (v1) | per-point bridge colors, hatched "Other" `pattern`; `_patch_series_dlbls()` shim adds source-positioned native labels for the thin Bulk/Other top segments; mandate table + Port-Alpha outlines |
| 35 | `freight_charges_teaching` | single-bar stacked column | user file (v1) | uses `crosses="min"`; `custom_geometry` check/cross status icons; addressability table; dashed leaders |
| 40 | `production_outlook_separate_teaching_factory_chart` | combo (stacked col + line) | user file (v3) | Franklin capacity converted from **manual connectors → native `line_overlay`** (`line_overlay_axis="same"`, `crosses="min"`) |

## Bonus changes (self-made)

- **Slide 39 `production_outlook_colocated_teaching_factory_chart`** — same conversion as slide 40 v3: manual Franklin-capacity connectors → native `combo_chart` `line_overlay`; removed `paint_capacity_reference_line()`, the `CAPACITY_SEGMENTS`/`_CAPACITY_POINTS` math, and the `CapacitySegment` dataclass; updated docstring/metadata.
- **Slide 4 `status_quo_outlook_offshore_1_teaching`** — made the x-axis year ticks **vertical** (`vert="vert270"`) to match `tables_originals/status_quo_outlook_offshore_1.py`. Box geometry (`0.167×0.306`) and right-alignment already matched; only the rotation was missing. Kept tick size at `PT(8)` (reference uses `PT(10)`).

---

## Recurring pattern: module-level chart-XML post-processes

Several user files solve "the factory doesn't expose X" by patching the generated `chart_xml` in the module instead of adding an engine param. Examples seen this session:
- `offshore_2`: `_source_align_combo_axes()` — regex-rewrites the 4 axis blocks' `delete`/`crosses` to match the source (notably deletes the secondary `catAx`).
- `archetype_comps_newbuild_prices`: `_with_source_plot_area_border()` — inserts `<c:spPr>` before `</c:plotArea>`.
- `ships_act_captive_demand`: `_patch_series_dlbls()` — splices source-positioned `<c:dLbls>` into named series.
- `archetype_comps_shipbuilder_margins`: `_native_ebit_marker_chart()` — noFills the line stroke, re-weights native `dash` markers, hides the duplicate `catAx`.

---

## Working-tree state (nothing committed)

`git diff --stat` shows ~29 dirty files (this session **plus** the uncommitted prior `charts_originals` session):
- **`deck_core/charts.py`** — the 2 additive changes above (plus prior-session `value_axis_line_color`).
- `deck_core/_build.py`, `authoring.py`, `chrome.py`, `primitives.py` — from the prior session (unchanged here).
- The 12 slide modules touched this session (the 10 targets + slides 39 and 4), plus other modules dirty from the prior session.

## Open items
- **No commit yet** — offered; awaiting the user's go-ahead.
- Final **PowerPoint** sign-off is the user's (verification here is LibreOffice; the original cross-renderer dispute did not recur on these slides).
- All 10 targets are now both faithful and factory-native; remaining teaching modules in the deck were not in scope this session.
