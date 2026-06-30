# Session log — planning: visual-grammar index, legend de-jargon, file-name cleanup, canonical render order

**Date:** 2026-06-28 (continues the same day's semantic shape-name cleanup session)
**Project:** `/Users/brendantoole/projects3/slide_factory/`
**Build:** `cd style_library && python3 build_deck.py` → `library.pptx` (pure Python 3.9 stdlib, no deps)
**End state:** **Planning only — no code changes, nothing committed this session.** A full execution plan was written to **`/Users/brendantoole/projects3/slide_library_index_and_cleanup_plan.md`** (projects3 root, outside the repo, per user request) and is ready to execute. `library.pptx` is unchanged from commit `214034e` (40 slides, 22 charts).

---

## What this session was

A pure **planning / design** session for the next body of work on the slide library. No edits to slide modules; the deliverable is the standalone markdown plan document above. This log captures the exploration findings and the confirmed decisions so the next session can execute without re-deriving them.

The prompt was a detailed design spec from the user proposing (a) a scannable per-slide metadata **index** built on `canonical_category` + `visual_grammar` tags, and (b) replacing the `LegendSwatch` design-jargon with semantic legend-key names. During planning the user added two more scope items: (c) clean up the module **file names**, and (d) **reorder the render sequence** to follow the canonical grouping.

---

## Exploration findings (read-only, via 3 Explore agents)

1. **`TEACHING_METADATA` is inert.** All 40 modules carry a `TEACHING_METADATA` dict (`role`/`use_when`/`teaches`/`source_module`/`rebuild_strategy`). A repo-wide grep found **zero reads** — the build pipeline (`deck_core/_build.py`) only consumes `LAYOUT` (required), `CHARTS`, `IMAGES`, `HYPERLINKS`, and `CHROME`. So `TEACHING_METADATA` is pure (unused) documentation. `TEXT_FIT` / `COPY_RULES` dicts are separate authoring precedents (also inert).
2. **No central index exists.** The only catalog is the `SLIDE_RENDERS` list + inline one-line comments in `style_library/library/slides/__init__.py`. No YAML/JSON/MD/`canonical_category`/`visual_grammar` anywhere.
3. **`LegendSwatch` is pervasive — ~34 emit sites across ~20 modules.** Almost all are filled color chips. Variants by visual type:
   - filled color rect → `LegendSwatch`, `LegendBarSwatch`, `DemandLegendSwatch` (record name), `PhaseLegendSwatch`, `ShipyardLegendSwatch`
   - pattern fill → `HeritageTargetPatternSwatch` / `HeritagePatternSwatch`, `LegendMarkerHatched`
   - line sample → `LegendLineRule`, `FranklinCapacityLegendMark`
   - bubble-size ring → `LegendMarker` (ellipse)
   - arrow glyph → emitted as literal `"LegendSwatch"` with `prst="rightArrow"` in ships_act_volume/plus
   - **Field names:** `swatch_box` in only 3 modules (`fleet_overview`, `status_quo_fleet_outlook`, `status_quo_outlook_offshore_1`); offshore_2 already uses `key_box`; many others use `swatch`, `box`, `marker_box`, or `swatch_x`.
   - **Gotcha:** `ships_act_volume` / `ships_act_plus_volume` paint loops emit the **hardcoded** literal `"LegendSwatch"` for three different things (white panel, color chips, arrow glyph), ignoring the record `name` field — so those need per-call-site disambiguation, not a blanket swap.
4. **Slide classification material** gathered for all 40 (docstring ROLE/TEACHES + dominant exhibit type) → fed the proposed canonical grouping below.

---

## Decisions confirmed (with the user)

| Question | Decision |
|---|---|
| Legend rename scope/precision | **Precise, Swatch-only** — rename only the "Swatch"/"swatch" jargon to the precise key type by what it draws; **leave** the already-clear `LegendMarker` / `LegendMarkerHatched` / `LegendLineRule` / `FranklinCapacityLegendMark` / `*LegendLabel`. |
| Index format/location | **YAML file** at `style_library/library/slides/INDEX.yaml` (purely a human/agent navigational doc — nothing parses it, so no new dependency). |
| Inert `TEACHING_METADATA` | **Strip** it from all 40 modules (keep prose docstrings + `TEXT_FIT`/`COPY_RULES`). |
| (added) file names | **Clean up** — drop `_teaching` / `_teaching_factory_table` / `_teaching_factory_chart` suffixes so the file stem == the index `id`. |
| (added) render order | **Reorder** `SLIDE_RENDERS` to render grouped by `canonical_category`. |

---

## The plan (5 parts) — see the projects3-root markdown for full detail

1. **Legend de-jargon** (render-affecting, names-only): `LegendSwatch`/`LegendBarSwatch` → `LegendColorKey`; `Demand/Phase/Shipyard…Swatch` → `…ColorKey`; `Heritage*PatternSwatch` → `…PatternKey`; `class LegendSwatch` → `class LegendKey`; fields `swatch_box`/`swatch`/`swatch_x` → `key_box`/`key`/`key_x`. ships_act_volume/plus emit the record `name` so the panel→`LegendPanel`, chips→`DemandLegendColorKey`, arrow→`LegendGlyphKey`.
2. **Strip `TEACHING_METADATA`** (source-only, no output change).
3. **`INDEX.yaml`** — `canonical_category_allowed` (6 values) + `visual_grammar_allowed` (user's vocab verbatim) + all 40 slides classified, ordered to match the new render order. `id` = cleaned module stem.
4. **File-name cleanup** (source-only) — `git mv` each module to the clean stem; update `__init__.py` imports + check `style_library/_tools/convert_slide.py`.
5. **Render reorder** (changes slide numbers) — group `SLIDE_RENDERS` by canonical category.

### Proposed canonical grouping (drives both index and render order)
- **forecasts_scenarios_and_capacity:** fleet_overview, status_quo_fleet_outlook, status_quo_outlook_offshore_1/2, status_quo_outlook_oceangoing, ships_act_volume, ships_act_plus_volume, ships_act_captive_demand, us_delivery_capacity, production_outlook_colocated/separate
- **market_sizing_and_tcv_buildup:** addressable_demand, definitions_market_levels, approach_volume_and_price, tcv_approach_manned/manned_undersea/unmanned_undersea/usv/iamd, tcv_to_acv_company_acv/undersea
- **benchmarking_and_archetypes:** archetype_comps_vocc_performance/newbuild_prices/shipbuilder_margins, comparison_vs_ddgs
- **unit_economics_and_financials:** approach_unit_economics, freight_charges, assumptions_income_statement_1/2, key_findings_demand_build_economics/financial_outlook/what_must_be_true
- **value_chain_and_policy_flows:** ships_act_overview, funding_components, value_chain_maritime_transport, value_chain_participation
- **frameworks_and_reference:** overview, key_terms_glossary, coordination_archetypes, key_inputs

(`comparison_vs_ddgs` folded into benchmarking with a `cost_capability_comparison` grammar tag. Categories + intra-group order are a first pass to confirm before executing.)

---

## Key constraints / caveats for the executing session

- **Order of operations matters:** legend rename **first** (stable slide numbers → clean `verify_names.py`), then the source-only changes (strip, index, file renames), then the **reorder last** (it renumbers everything). Five commits.
- **Faithful-output rule still holds:** the legend rename may change **only** `p:cNvPr@name` on legend shapes; the index/strip/file-renames change no output; the reorder changes only slide *order* (per-module content byte-identical).
- **The reorder breaks the reference-deck 1:1 mapping.** `/Users/brendantoole/projects3/slide_factory_reference_originals.pptx` is currently ordered 1:1 with `SLIDE_RENDERS`. After grouping, library slide N ≠ reference slide N — record a `module → original reference slide #` map (comment in `__init__.py` or this log) so future A/B fidelity checks still work.
- **Verification tooling** is the existing `scratchpad/verify_names.py` (normalizes build-clock timestamps in `core.xml` + `.xlsx` embeddings; reports NAMES-ONLY per slide). The index needs a tiny no-dependency line-based validator (no yaml in stdlib) to assert every tag ∈ vocabulary and all 40 ids present/ordered.

## Git state
Unchanged this session — `main` is at `214034e` (the prior semantic-rename + render-fixes session log), pushed to `origin/main`. This planning log and the projects3-root plan markdown are **not yet committed**.
