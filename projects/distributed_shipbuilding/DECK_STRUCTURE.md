# Distributed Shipbuilding — Deck Structure & Grid/Reference Plan

**Deck:** DDG-51 New-Construction Supplier Market
**Status:** target structure (aspirational). The cover and the five section
dividers are built and wired; the content slides are **not** yet a 1:1 match to
this plan.

> **Note — known mismatch (acknowledged by the user).** The content slides
> currently in the build do **not** line up with the 13-content-slide target
> below. Several target slides have no module yet (Executive Answer, Value Chain,
> TAM→SAM Bridge, Where-to-Play Scorecard, Capability×Output Map, Priority
> Supplier Pools, a dedicated Construction-Stage Supplier Map, and most of the
> appendix). The existing slides have been slotted under the closest-matching
> section divider as placeholders. This file documents the **intended** grid
> layout and corpus reference per slide so the deck can be filled in over time;
> it is not a description of what renders today. See **"Current build vs. target"**
> at the bottom for the actual wiring and the gap list.

The deck has **four core sections** plus an optional appendix:

1. **Market Answer and Scope**
2. **TAM Sizing Build**
3. **SAM Supplier Market Structure**
4. **SAM Ship Construction Lens**
5. *(Appendix)* **Methodology and Backup**

TAM gets its own build section; both supplier segmentation and
construction-process mapping stay explicitly under SAM. **Priority Supplier
Pools** is kept as the *closing content slide of SAM Supplier Market Structure*,
not its own section.

---

## Title page

| Page       | Title line                                  | Subtitle line                                                  | Layout                                                                         |
| ---------- | ------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Title page | **DDG-51 New-Construction Supplier Market** | **Size outsourced work and identify priority supplier pools.** | Two-line title lockup. No exhibit. Optional small project/date line at bottom. |

## Section divider pages

|  Section | Title line                        | Subtitle line                                                           |
| -------: | --------------------------------- | ----------------------------------------------------------------------- |
|        1 | **Market Answer and Scope**       | **Define the market and state the answer.**                             |
|        2 | **TAM Sizing Build**              | **Build the supplier-addressable opportunity from construction spend.** |
|        3 | **SAM Supplier Market Structure** | **Use observed subawards to assess supplier pools.**                    |
|        4 | **SAM Ship Construction Lens**    | **Map observed supplier work to ship systems and build stages.**        |
| Appendix | **Methodology and Backup**        | **Document definitions, mappings, assumptions, and sources.**           |

The split follows the core logic: **TAM** is the top-down denominator layer,
while **SAM** is the observed first-tier subaward evidence layer used to
characterize supplier structure, concentration, timing, systems, and
traceability.

---

## Full deck sequence (target — 13 content slides + title + dividers)

|  # | Page type | Slide title                                  | Section                       | Recommended grid layout                                                                          | Corpus reference pattern                                                                                                                                                                                |
| -: | --------- | -------------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  1 | Title     | **DDG-51 New-Construction Supplier Market**  | Front matter                  | Two-line title lockup                                                                            | Clean opener discipline from `overview.py`, simplified to title and subtitle only.                                                                                                                      |
|  2 | Divider   | **Market Answer and Scope**                  | Market Answer and Scope       | Large section title, one subtitle line, no chart                                                 | Same orientation role as `overview.py`, but as a divider rather than a two-column body slide.                                                                                                           |
|  3 | Content   | **Executive Answer**                         | Market Answer and Scope       | KPI-card opener: top answer line, 3–5 KPI cards, 2–3 finding cards                               | Closest anchor `fleet_overview.py`: compact exhibit plus right-side big-number KPI cards. KPI-card idea, not a full dashboard.                                                                          |
|  4 | Content   | **Market Scope and Sizing Levels**           | Market Answer and Scope       | Left nested funnel, right definition table                                                       | Directly anchored in `definitions_market_levels.py` (nested market-level funnel + formal definition table).                                                                                            |
|  5 | Content   | **DDG-51 New-Construction Value Chain**      | Market Answer and Scope       | Full-canvas value-chain swimlane: stages across columns, work categories down rows               | `value_chain_maritime_transport.py` for stage headers/nodes/connectors; `value_chain_participation.py` for matrix-style participation across stages.                                                    |
|  6 | Divider   | **TAM Sizing Build**                         | TAM Sizing Build              | Large section title, one subtitle line, no chart                                                 | Simple divider. No heavy exhibit.                                                                                                                                                                       |
|  7 | Content   | **Model Architecture: TAM and Observed SAM** | TAM Sizing Build              | System map: TAM denominator on left, observed SAM fact spine in center, analytical cuts on right | `tcv_approach_usv.py` for the Total Funding → TAM → SAM calculation-node grammar; `ships_act_overview.py` for flow-node logic.                                                                          |
|  8 | Content   | **TAM Build: Outsourced Opportunity**        | TAM Sizing Build              | Method rail + calculation flow + output stack                                                    | Direct match to the TCV approach family: left method rail, central calculation chain, right output stack.                                                                                               |
|  9 | Content   | **TAM to Observed SAM Bridge**               | TAM Sizing Build              | Bridge chart + compact KPI rail + small denominator table                                        | `tcv_to_acv_company_acv.py` for bridge-chart logic; `fleet_overview.py` for compact KPI cards. Keep the denominator note small.                                                                        |
| 10 | Divider   | **SAM Supplier Market Structure**            | SAM Supplier Market Structure | Large section title, one subtitle line, no chart                                                 | Simple divider.                                                                                                                                                                                         |
| 11 | Content   | **Observed SAM by Fiscal Year**              | SAM Supplier Market Structure | Dominant time-series column chart with small metric strip                                        | `status_quo_fleet_outlook.py`: dominant time-series chart, manual year ticks, manual total labels, compact legend and callouts.                                                                        |
| 12 | Content   | **SAM Where-to-Play Scorecard**              | SAM Supplier Market Structure | Full-width strategic matrix or heatmap                                                           | `key_findings_what_must_be_true.py` for matrix grammar; `funding_components.py` for fill-encoded matrix cells.                                                                                          |
| 13 | Content   | **Capability Domain by Primary Output Map**  | SAM Supplier Market Structure | D × P heatmap or bubble matrix with short interpretation rail                                    | `funding_components.py` for dense addressability grid grammar; `archetype_comps_newbuild_prices.py` if bubble encoding preferred.                                                                       |
| 14 | Content   | **Supplier and Parent Concentration**        | SAM Supplier Market Structure | Ranked bar or Pareto chart on left, concentration table on right                                 | `archetype_comps_vocc_performance.py` for chart + right narrative rail; `fleet_overview.py` for KPI-card emphasis.                                                                                      |
| 15 | Content   | **Priority Supplier Pools**                  | SAM Supplier Market Structure | Priority matrix or bubble map on left, short rationale table on right                            | Closing content slide (replaces the deleted divider). Summarizes large, growing, concentrated, open, or strategically important pools. "Where to Play" is the primary SAM answer.                       |
| 16 | Divider   | **SAM Ship Construction Lens**               | SAM Ship Construction Lens    | Large section title, one subtitle line, no chart                                                 | Simple divider.                                                                                                                                                                                         |
| 17 | Content   | **SWBS Ship-System View**                    | SAM Ship Construction Lens    | Chart plus right explanatory table                                                               | `freight_charges.py` for chart + explanatory table grammar; `ships_act_captive_demand.py` if the right-side table becomes more detailed.                                                                |
| 18 | Content   | **Construction-Stage Supplier Map**          | SAM Ship Construction Lens    | Stage-by-domain matrix or swimlane                                                               | `value_chain_participation.py` for stage headers and matrix participation; `value_chain_maritime_transport.py` for stage-flow logic.                                                                    |

---

## Appendix sequence (target — include only if the deck needs to be diligence-ready)

|   # | Page type | Slide title                          | Recommended grid layout                  | Corpus reference pattern                                                                                         |
| --: | --------- | ------------------------------------ | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
|  A1 | Divider   | **Methodology and Backup**           | Large section title, one subtitle line   | Simple divider.                                                                                                  |
|  A2 | Appendix  | **Key Terms and Market Definitions** | Two-column glossary tables               | `key_terms_glossary.py`                                                                                          |
|  A3 | Appendix  | **D and P Archetype Taxonomy**       | Full-width grouped taxonomy table        | `coordination_archetypes.py`                                                                                     |
|  A4 | Appendix  | **TAM Inputs and Sources**           | Full-width source-backed reference table | `key_inputs.py`                                                                                                  |
|  A5 | Appendix  | **TAM Sensitivity Scenarios**        | Scenario table or tornado-style matrix   | `assumptions_income_statement_1.py` and `assumptions_income_statement_2.py` for assumption-table grammar.        |
|  A6 | Appendix  | **Subaward Processing Logic**        | Full-canvas process flow                 | `ships_act_overview.py` for connector-flow grammar.                                                              |
|  A7 | Appendix  | **SWBS Mapping Rules**               | Full-width mapping table                 | `key_inputs.py` or `coordination_archetypes.py` table grammar.                                                   |
|  A8 | Appendix  | **Hull and Lifecycle Mapping Rules** | Rules table plus small timeline          | `assumptions_income_statement_1.py` for methodology table; `value_chain_participation.py` for stage structure.   |
|  A9 | Appendix  | **Supplier Detail**                  | Full-width ranked supplier table         | `key_inputs.py` table style or `coordination_archetypes.py` grouped table style.                                 |
| A10 | Appendix  | **Research Queue**                   | Prioritized worklist table               | Reference-table grid, not a caveat-heavy slide.                                                                  |

---

## Final section map (target)

| Section                           | Slides                                                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Market Answer and Scope**       | Executive Answer; Market Scope and Sizing Levels; DDG-51 New-Construction Value Chain                                                                         |
| **TAM Sizing Build**              | Model Architecture; TAM Build; TAM to Observed SAM Bridge                                                                                                     |
| **SAM Supplier Market Structure** | Observed SAM by Fiscal Year; SAM Where-to-Play Scorecard; Capability Domain by Primary Output Map; Supplier and Parent Concentration; Priority Supplier Pools |
| **SAM Ship Construction Lens**    | SWBS Ship-System View; Construction-Stage Supplier Map                                                                                                        |

One clean story: **scope → TAM → SAM supplier structure → SAM construction lens.**

---

## Current build vs. target (what actually renders today)

The build is **15 slides**: the cover, four section dividers, an appendix
divider, and the **9 existing content slides** slotted under the closest section.
This is **not** the 13-content-slide target — it is the current set sequenced
against the section spine.

| Build # | Module (or divider)                                | Section                       | Maps to target slide                         | Match quality |
| ------: | -------------------------------------------------- | ----------------------------- | -------------------------------------------- | ------------- |
|       1 | `cover`                                            | Front matter                  | #1 Title                                     | exact         |
|       2 | `divider_market_answer_and_scope`                  | Market Answer and Scope       | #2 Divider                                   | exact         |
|       3 | `definitions_market_levels`                        | Market Answer and Scope       | #4 Market Scope and Sizing Levels            | strong        |
|       4 | `divider_tam_sizing_build`                         | TAM Sizing Build              | #6 Divider                                   | exact         |
|       5 | `approach_two_stage_teaching`                      | TAM Sizing Build              | #7 Model Architecture (TAM and Observed SAM) | partial       |
|       6 | `slide1_outsourced_bc_walk_updated`                | TAM Sizing Build              | #8 TAM Build: Outsourced Opportunity         | strong        |
|       7 | `divider_sam_supplier_market_structure`            | SAM Supplier Market Structure | #10 Divider                                  | exact         |
|       8 | `slide3_outsourced_bc_annual_tam_ref`              | SAM Supplier Market Structure | #11 Observed SAM by Fiscal Year              | strong        |
|       9 | `vendor_swbs_fingerprint_teaching`                 | SAM Supplier Market Structure | #14 Supplier and Parent Concentration        | strong        |
|      10 | `divider_sam_ship_construction_lens`               | SAM Ship Construction Lens    | #16 Divider                                  | exact         |
|      11 | `outsourced_spend_by_work_type`                    | SAM Ship Construction Lens    | #18 Construction-Stage Supplier Map (work-type cut) | partial |
|      12 | `ddg51_swbs_dollar_mix_teaching_alternative`       | SAM Ship Construction Lens    | #17 SWBS Ship-System View                    | strong        |
|      13 | `divider_appendix_methodology`                     | Appendix                      | A1 Divider                                   | exact         |
|      14 | `ddg51_hull_confidence_overlay_teaching_factory_chart` | Appendix                  | ≈ A8 Hull and Lifecycle Mapping Rules        | partial       |
|      15 | `ddg_hull_linkage_methodology_v4_updated`          | Appendix                      | ≈ A8 / methodology backup                    | partial       |

### Target content slides with no module yet (gaps to author)

- **#3 Executive Answer** — KPI-card opener (`fleet_overview.py`)
- **#5 DDG-51 New-Construction Value Chain** — value-chain swimlane (`value_chain_maritime_transport.py`, `value_chain_participation.py`)
- **#9 TAM to Observed SAM Bridge** — bridge chart + KPI rail (`tcv_to_acv_company_acv.py`)
- **#12 SAM Where-to-Play Scorecard** — strategic matrix/heatmap (`key_findings_what_must_be_true.py`, `funding_components.py`)
- **#13 Capability Domain by Primary Output Map** — D×P heatmap/bubble (`funding_components.py`, `archetype_comps_newbuild_prices.py`)
- **#15 Priority Supplier Pools** — priority matrix + rationale table (closing SAM slide)
- **#18 Construction-Stage Supplier Map** — dedicated stage-by-domain matrix (currently approximated by the work-type slide)
- **Appendix A2–A7, A9, A10** — glossary, taxonomy, TAM inputs, sensitivity, subaward logic, SWBS rules, supplier detail, research queue
