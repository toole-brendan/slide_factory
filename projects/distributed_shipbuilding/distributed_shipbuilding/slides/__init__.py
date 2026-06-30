"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core._build reads to wire
slide layouts, native chart parts, and pictures.

Empty until the first slide is authored. To add a slide:
  1. Create distributed_shipbuilding/slides/<name>.py exporting LAYOUT and render().
  2. Import it below and append (<name>, <name>.render) to SLIDE_RENDERS.
"""
from __future__ import annotations

from . import (
    # Front matter + section dividers (chrome-only; cover=slideLayout1, dividers=slideLayout2).
    cover,
    divider_market_answer_and_scope,
    divider_tam_sizing_build,
    divider_sam_supplier_market_structure,
    divider_sam_ship_construction_lens,
    divider_appendix_methodology,
    # Content slides.
    executive_answer,
    definitions_market_levels,
    ddg51_new_construction_value_chain,
    approach_two_stage_teaching,
    slide1_outsourced_bc_walk_updated,
    tam_to_observed_sam_bridge,
    slide3_outsourced_bc_annual_tam_ref,
    sam_where_to_play_scorecard,
    vendor_swbs_fingerprint_teaching,
    construction_stage_supplier_map,
    outsourced_spend_by_work_type,
    ddg51_swbs_dollar_mix_teaching_alternative,
    ddg51_hull_confidence_overlay_teaching_factory_chart,
    ddg_hull_linkage_methodology_v4_updated,
)

# Archived (moved to projects/distributed_shipbuilding/_archive/slides/, out of
# the build): ddg_subaward_hull_results, ddg51_hull_linkage_method,
# ddg_hull_linkage_methodology_v4, ddg_subaward_hull_linkage_results.
# Deleted: slide2_worktype_by_program, slide5_worktype_by_fy,
# slide1_outsourced_bc_walk (superseded by slide1_outsourced_bc_walk_updated).

# Cover + four core section dividers + an appendix divider. New target modules
# are slotted beside the existing closest-match content slides; the deck still
# keeps a few partial/supporting modules until the remaining target gaps are built.
SLIDE_RENDERS: list[tuple] = [
    (cover, cover.render),

    # 1 — Market Answer and Scope
    (divider_market_answer_and_scope, divider_market_answer_and_scope.render),
    (executive_answer, executive_answer.render),
    (definitions_market_levels, definitions_market_levels.render),
    (ddg51_new_construction_value_chain, ddg51_new_construction_value_chain.render),

    # 2 — TAM Sizing Build
    (divider_tam_sizing_build, divider_tam_sizing_build.render),
    (approach_two_stage_teaching, approach_two_stage_teaching.render),
    (slide1_outsourced_bc_walk_updated, slide1_outsourced_bc_walk_updated.render),
    (tam_to_observed_sam_bridge, tam_to_observed_sam_bridge.render),

    # 3 — SAM Supplier Market Structure
    (divider_sam_supplier_market_structure, divider_sam_supplier_market_structure.render),
    (slide3_outsourced_bc_annual_tam_ref, slide3_outsourced_bc_annual_tam_ref.render),
    (sam_where_to_play_scorecard, sam_where_to_play_scorecard.render),
    (vendor_swbs_fingerprint_teaching, vendor_swbs_fingerprint_teaching.render),

    # 4 — SAM Ship Construction Lens
    (divider_sam_ship_construction_lens, divider_sam_ship_construction_lens.render),
    (construction_stage_supplier_map, construction_stage_supplier_map.render),
    (outsourced_spend_by_work_type, outsourced_spend_by_work_type.render),
    (ddg51_swbs_dollar_mix_teaching_alternative, ddg51_swbs_dollar_mix_teaching_alternative.render),

    # Appendix — Methodology and Backup
    (divider_appendix_methodology, divider_appendix_methodology.render),
    (ddg51_hull_confidence_overlay_teaching_factory_chart, ddg51_hull_confidence_overlay_teaching_factory_chart.render),
    (ddg_hull_linkage_methodology_v4_updated, ddg_hull_linkage_methodology_v4_updated.render),
]
