"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core._build.build_pptx reads to wire
slide layouts, native chart parts, and pictures.

Curated, hand-polished reference corpus of styled slides ported 1:1 from the
source market-analysis decks. The converter (style_library/_tools/convert_slide.py)
emits the raw module; these registered copies are the frozen, hand-annotated
study versions.

Entries are grouped by source deck and kept in source-slide order so the corpus
reads coherently.
"""
from __future__ import annotations

from . import (
    # ── Teaching exemplars (render first) ──
    fleet_overview,                  # US-flagged/US-built fleet overview (factory bar_chart)
    status_quo_fleet_outlook,        # net fleet additions/retirements (factory stacked column_chart)
    tcv_approach_manned_undersea,    # undersea currently-manned TCV build-up (flow diagram)
    approach_volume_and_price,       # two-track volume/price build-up (operator-glyph schematic)
    ships_act_overview,              # policy money-flow diagram (foreign penalties -> SCF)
    tcv_approach_iamd,               # domain/role allocation TCV build-up (OBBBA + SHIELD)
    tcv_approach_manned,             # surface currently-manned TCV build-up (dense schematic)
    tcv_approach_unmanned_undersea,  # unmanned-undersea TCV build-up
    tcv_approach_usv,                # USV-specified TCV build-up (simple chain)
    tcv_to_acv_company_acv,          # TCV->ACV contract-timing bridge (styled chart + table)
    tcv_to_acv_company_acv_undersea,  # undersea TCV->ACV bridge (styled chart + Years 2-5 table)
    us_delivery_capacity,  # native column_chart() factory variant (no template, no _src)
    addressable_demand,     # role-based teaching rewrite of addressable_demand
    value_chain_maritime_transport,  # value chain (maritime transport) - who captures value (tables + shapes)
    definitions_market_levels,       # market broken into five levels (table + nested-circles image)
    funding_components,              # funding inputs/sources/colors of money (flow diagram)
    value_chain_participation,       # value-chain participation - grouped icons (picture-dense)
    # ── Commercial Strategy Market Analysis (20260325) ──
    overview,               # src 2:   Overview (2 summary tables)
    key_terms_glossary,  # src 5:   For Reference | Key Terms Glossary (native factory table)
    key_findings_demand_build_economics,  # src 8:   Key Findings (1/3) - demand, build cost, vessel economics (native factory table)
    key_findings_financial_outlook,  # src 9:   Key Findings (2/3) - ComboCo financial outlook (native factory table)
    key_findings_what_must_be_true,  # src 10:  Key Findings (3/3) - what must be true to succeed (native factory table)
    archetype_comps_newbuild_prices,  # src 32:  Archetype Comps (1/3) - improvement from rising new-build prices (chart)
    archetype_comps_vocc_performance,  # src 33:  Archetype Comps (2/3) - VOCC performance '21-'22 (chart + table)
    archetype_comps_shipbuilder_margins,  # src 34:  Archetype Comps (3/3) - shipbuilder margin profile across geographies (5 native factory charts, dense)
    # NOTE: fleet_overview (src 42) + status_quo_fleet_outlook (src 43) promoted to the render-first block
    status_quo_outlook_oceangoing,   # src 44:  Status Quo Outlook (Oceangoing Commercial) (native column_chart(stacked) + table)
    status_quo_outlook_offshore_1,   # src 45:  Status Quo Outlook (Addressable Offshore 1/2) (native column_chart(stacked) + table)
    status_quo_outlook_offshore_2,   # src 46:  Status Quo Outlook (Addressable Offshore 2/2) (chart)
    ships_act_volume,  # src 51:  SHIPS Act Volume - bill-specified subsidy funding (styled_chart + connectors)
    ships_act_plus_volume,  # src 52:  SHIPS Act "Plus" Volume - demand declines after mid-2030s (local stacked_area_chart + connectors)
    ships_act_captive_demand,  # src 60:  SHIPS Act Captive Demand - MSTF supports ~100 more vessels than mandated (native column_chart + mandate table)
    assumptions_income_statement_1,  # src 77:  Assumptions & Methodology - Income Statement (1/2) (native factory table)
    assumptions_income_statement_2,  # src 78:  Assumptions & Methodology - Income Statement (2/2) (native factory table)
    approach_unit_economics,  # src 120: Approach (1/2) - determining unit economics (native factory table)
    freight_charges,        # src 134: Freight Charges - ~70% of westbound charges are vessel-related (native factory chart + cost table)
    coordination_archetypes,  # src 166: Coordination Archetypes - entities in the Coordination step (native factory table)
    key_inputs,  # src 167: Key Inputs (native factory table)
    # ── Market Sizing: Golden Dome (20260116) ──
    comparison_vs_ddgs,  # src 8:   Comparison vs. DDGs - GD MR procurement cost vs four Arleigh Burkes (native factory chart + 2 tables)
    production_outlook_colocated,  # src 11:  Production Outlook - co-located sensors and interceptors (native column_chart)
    production_outlook_separate,  # src 12:  Production Outlook - separate platforms (native column_chart factory variant)
)

SLIDE_RENDERS: list[tuple] = [
    # ── Promoted to front (render first, in requested order) ──
    (archetype_comps_vocc_performance, archetype_comps_vocc_performance.render),
    (status_quo_outlook_offshore_2, status_quo_outlook_offshore_2.render),
    (archetype_comps_newbuild_prices, archetype_comps_newbuild_prices.render),
    (status_quo_outlook_offshore_1, status_quo_outlook_offshore_1.render),
    # ── Teaching exemplars (render first) ──
    (fleet_overview, fleet_overview.render),
    (status_quo_fleet_outlook, status_quo_fleet_outlook.render),
    (tcv_approach_manned_undersea, tcv_approach_manned_undersea.render),
    (approach_volume_and_price, approach_volume_and_price.render),
    (ships_act_overview, ships_act_overview.render),
    (tcv_approach_iamd, tcv_approach_iamd.render),
    (tcv_approach_manned, tcv_approach_manned.render),
    (tcv_approach_unmanned_undersea, tcv_approach_unmanned_undersea.render),
    (tcv_approach_usv, tcv_approach_usv.render),
    (tcv_to_acv_company_acv, tcv_to_acv_company_acv.render),
    (tcv_to_acv_company_acv_undersea, tcv_to_acv_company_acv_undersea.render),
    (us_delivery_capacity, us_delivery_capacity.render),
    (addressable_demand, addressable_demand.render),
    (value_chain_maritime_transport, value_chain_maritime_transport.render),
    (definitions_market_levels, definitions_market_levels.render),
    (funding_components, funding_components.render),
    (value_chain_participation, value_chain_participation.render),
    # ── Commercial Strategy Market Analysis (20260325) ──
    (overview, overview.render),
    (key_terms_glossary, key_terms_glossary.render),
    (key_findings_demand_build_economics, key_findings_demand_build_economics.render),
    (key_findings_financial_outlook, key_findings_financial_outlook.render),
    (key_findings_what_must_be_true, key_findings_what_must_be_true.render),
    # NOTE: archetype_comps_newbuild_prices + archetype_comps_vocc_performance promoted to the render-first block above
    (archetype_comps_shipbuilder_margins, archetype_comps_shipbuilder_margins.render),
    (status_quo_outlook_oceangoing, status_quo_outlook_oceangoing.render),
    (ships_act_volume, ships_act_volume.render),
    (ships_act_plus_volume, ships_act_plus_volume.render),
    (ships_act_captive_demand, ships_act_captive_demand.render),
    (assumptions_income_statement_1, assumptions_income_statement_1.render),
    (assumptions_income_statement_2, assumptions_income_statement_2.render),
    (approach_unit_economics, approach_unit_economics.render),
    (freight_charges, freight_charges.render),
    (coordination_archetypes, coordination_archetypes.render),
    (key_inputs, key_inputs.render),
    # ── Market Sizing: Golden Dome (20260116) ──
    (comparison_vs_ddgs, comparison_vs_ddgs.render),
    (production_outlook_colocated, production_outlook_colocated.render),
    (production_outlook_separate, production_outlook_separate.render),
]
