# Session log & handoff — full visual audit of all 40 slide modules vs. the original reference slides (findings tally only; no code changes)

**Date:** 2026-06-27 (a later session the same day as the engine-prune session)
**Project:** `/Users/brendantoole/projects3/slide_factory/` — standalone pure-stdlib OOXML→PPTX authoring workspace.
**Build:** `cd style_library && python3 build_deck.py` → `library.pptx`. Pure Python 3.9.6 stdlib, no deps.
**Status at handoff:** **no code changes made this session.** The working tree still carries the prior session's uncommitted engine-prune refactor (HEAD `2b76009`, `main`). Build remains **40 slides / 22 charts / 23 embeddings**.

Big picture: a **notes-only session.** The user visually audited each rendered slide against its **original, manually-created reference slide** (the `reference/*.pptx` ground-truth decks), going **in render order**, and dictated findings. I transcribed them into a running tally. **No modules, engine, or registry were touched.**

**Canonical findings file:** `/Users/brendantoole/projects3/slide_audit.md` — i.e. at **projects3 root, OUTSIDE the repo** (won't show as a repo change), kept live throughout. This log duplicates it for handoff; if they diverge, `slide_audit.md` is the source the user was editing against.

---

## 0. Method notes / gotchas

- **Render order is `SLIDE_RENDERS` in `style_library/library/slides/__init__.py`.** Current order (1-indexed) below. GOTCHA when scripting the map: the module docstring contains the phrase "(module, render_fn)", so a naïve `\(\w+,` regex picks up a phantom `module` entry and shifts every slide by one — match only 4-space-indented tuple lines.
- **The "scenario/scope chip"** (recurring finding) = the outlined no-fill text chip pinned top-right, immediately left of the Preliminary banner, slot `Box(8.069, ~0.17, 2.977, 0.217)`. Named inconsistently across modules: `ScenarioChip` (most), `ScopeChip` (us_delivery), or unnamed (ships_act volume/plus). No canonical name in the codebase.
- **Preliminary banner** is house chrome: `preliminary_chip` in `deck_core/chrome.py` (`_PRELIM_*` = x 10,267,829 / y 111,556 / cx 1,467,612 / cy 290,000).

### Render-order map (1–40)
1 archetype_comps_vocc_performance · 2 status_quo_outlook_offshore_2 · 3 archetype_comps_newbuild_prices · 4 status_quo_outlook_offshore_1 · 5 fleet_overview · 6 status_quo_fleet_outlook · 7 tcv_approach_manned_undersea · 8 approach_volume_and_price · 9 ships_act_overview · 10 tcv_approach_iamd · 11 tcv_approach_manned · 12 tcv_approach_unmanned_undersea · 13 tcv_approach_usv · 14 tcv_to_acv_company_acv · 15 tcv_to_acv_company_acv_undersea · 16 us_delivery_capacity_factory_chart · 17 addressable_demand · 18 value_chain_maritime_transport · 19 definitions_market_levels · 20 funding_components · 21 value_chain_participation · 22 overview · 23 key_terms_glossary · 24 key_findings_demand_build_economics · 25 key_findings_financial_outlook · 26 key_findings_what_must_be_true · 27 archetype_comps_shipbuilder_margins · 28 status_quo_outlook_oceangoing · 29 ships_act_volume · 30 ships_act_plus_volume · 31 ships_act_captive_demand · 32 assumptions_income_statement_1 · 33 assumptions_income_statement_2 · 34 approach_unit_economics · 35 freight_charges · 36 coordination_archetypes · 37 key_inputs · 38 comparison_vs_ddgs · 39 production_outlook_colocated · 40 production_outlook_separate

(Slides with **no** flagged issue: 1, 7, 8, 11, 12, 13, 14, 16, 20, 22, 23, 24, 25, 32, 36, 37.)

---

## 1. Recurring / cross-cutting issues

- **Scenario/scope chip** almost always wrong vs. original — **missing border** and/or **wrong text font color**. Affects: fleet_overview, status_quo_fleet_outlook, status_quo_outlook_offshore_1, status_quo_outlook_offshore_2, ships_act_captive_demand, ships_act_volume, ships_act_plus_volume, us_delivery_capacity.
- **Preliminary banner dimensions should be updated to mirror the reference deck.**
- **Missing shadow on light-blue-fill shapes** vs. original (slides 2, 4, 5, 28, 29, 30, 31).

---

## 2. Systemic themes (many findings share a root cause — fix once, not per-slide)

- **Stray arrowheads on connector / dashed / leader lines** — should be plain dashed lines, no arrowhead: slides 10 (wrong dash pattern), 15, 21 (legend dash), 27, 29, 30, 31 (label leader lines), 39, 40 (legend line symbol).
- **X-axis year labels need 270° rotation** (currently horizontal): slides 4, 28, 29, 30.
- **Source line missing hyperlinks**: slides 2, 9, 29, 30, 31, 38.
- **Chart axis/gridline correctness**: duplicated axes (2), missing axis (5), gridlines showing + y-axis misplaced (6 — slide 4 is the correct reference), stray y-axis line (35), missing exterior chart border (3).
- **Missing shadow on light-blue shapes** (see recurring).
- **z-order (push to front/back)**: labels behind connectors (9), dashed boxes to back (34), label to front over border (35), logos to back (38), "Confidence level" text to front over arrows (29, 30).
- **Table cell formatting** — intra-cell alignment / rotation / bold / padding / row height: 4, 17, 18, 19, 21, 26, 33, 34, 38.
- **Missing column number-labels**: 31 (left stacked column, 2 numbers missing), 40 (FY32 & FY33).

---

## 3. Per-slide findings (verbatim tally)

**2. status_quo_outlook_offshore_2** (combo: stacked bar + line) — chart **axes duplicated**; light-blue-fill shape **no shadow**; source line **no hyperlink**.

**3. archetype_comps_newbuild_prices** (bubble) — chart **missing exterior border**.

**4. status_quo_outlook_offshore_1** (stacked bar) — light-blue-fill shape **missing shadow**; shape overlaps RHS table text, root cause a **table issue: too much spacing between bullets** pushing text down; x-axis **year labels should be rotated 270°**.

**5. fleet_overview** (factory bar) — RHS shapes **all missing shadows**; chart **missing its axis**.

**6. status_quo_fleet_outlook** (factory stacked column) — **gridlines showing** when they shouldn't; **y-axis in wrong spot**. Same y-axis + off-white LHS band pattern as **slide 4, which is done correctly** — use as reference.

**9. ships_act_overview** (flow) — labels over connectors have **connector running over the label** (label should be pushed to front); one shape's text **missing a hyperlink**.

**10. tcv_approach_iamd** — "Domain allocations (%)" & "Kill chain role allocations (%)" text **hidden behind other shapes** (incorrect text alignment); those shapes' border is the **wrong dashed pattern**.

**15. tcv_to_acv_company_acv_undersea** — chart uses **connector lines with arrowheads**; should be **dashed lines, no arrowheads**.

**17. addressable_demand** (table) — first-column text **not bolded** (should be) and **misaligned** in cells; top-row text **not bolded** (should be).

**18. value_chain_maritime_transport** — "Cargo moved by one or more…" and "Value flow for owned vessels" shapes use **incorrect bg fill colors**; first-column "Value Chain Step" & "Archetypes" cells **mis-aligned**.

**19. definitions_market_levels** — **intra-cell text alignment all wrong**.

**21. value_chain_participation** — first-column **intra-cell alignment wrong**; "Integrated Shippers" legend **wrong dash pattern**.

**26. key_findings_what_must_be_true** — first-column "Container" & "Tanker" **should be rotated 270°**; currently not.

**27. archetype_comps_shipbuilder_margins** (charts) — random **connector lines with arrowheads** should be **plain dashed**; "gold" markers are correct to include but should be **a bit thicker**.

**28. status_quo_outlook_oceangoing** — bottom-RHS light-blue shape **needs shadow**; x-axis **years rotated 270°**.

**29. ships_act_volume** — light-blue shape **missing shadow**; **wrong dashed pattern + extra arrowheads**; **legend missing text**; "Confidence level" up/down arrows **black, should be red/green filled**; "Confidence level" text **to front** over arrows; x-axis **years 270°**; source **missing hyperlinks**.

**30. ships_act_plus_volume** — **same as slide 29** (all items).

**31. ships_act_captive_demand** — bottom-RHS light-blue shape **missing shadow**; source **missing hyperlinks**; **left** stacked column has **messed-up top number labels** (smaller segments) while the **right** column renders correctly — **2 numbers missing**, and labels use **leader lines with arrowheads** that should have **no arrowhead**.

**33. assumptions_income_statement_2** (table) — **left/right intra-cell padding** may need a small increase; text + Methodology-column bullet glyphs **too tight to border**.

**34. approach_unit_economics** (table; hard — many 1pt-font rows/cols for narrowness; LibreOffice imposes a min row/cell height when none set) — "To find Normalized Cost of Sales: Divide by average cargo units per relevant voyage (route-specific volume)" **missing underlines**; dashed-box shapes **to back**; "Annual" col + "Operating Expenses" row vertical "Crew…" content **doesn't fill its dashed box** (others fit); "To find Normalized Opex:" text box has **too much gap between its 2 text groups**.

**35. freight_charges** — "Shoreside charges" label **to front** over the border line; chart has a **y-axis line it shouldn't have**.

**38. comparison_vs_ddgs** — RHS table row between "4x Arleigh Burke-class destroyers" and "Up to 384 SM-3 / SM-6" **too tall** (same for "240x Marauders" → "3,840 SM-3 / SM-6"); top-right logo images **to back**; source **missing hyperlinks**.

**39. production_outlook_colocated** — legend **random arrowhead** in the line symbol for "Franklin capacity (vessel starts)".

**40. production_outlook_separate** — **same legend arrowhead** as 39; chart columns **FY32 & FY33 missing number labels**.

---

## 4. Open / next

- Nothing was fixed — this session only produced the findings list. The natural follow-up is to work the **systemic themes in §2 first** (arrowhead-on-line, x-axis 270° rotation, light-blue shadow, source hyperlinks, scenario-chip border/color, Preliminary-banner dims) since each spans many slides and is likely a single shared helper/engine fix; then the per-slide one-offs in §3.
- Verify every fix **against the `reference/*.pptx` original** (the audit's ground truth), per the project's standing "source is ground truth" rule.
- Repo is still on the **uncommitted prune refactor** (user handles git). `slide_audit.md` lives outside the repo at projects3 root.
