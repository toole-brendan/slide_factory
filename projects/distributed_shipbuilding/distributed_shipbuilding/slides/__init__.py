"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core._build.build_pptx reads to wire
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
    definitions_market_levels,
    approach_two_stage_teaching,
    slide1_outsourced_bc_walk_updated,
    slide3_outsourced_bc_annual_tam_ref,
    outsourced_spend_by_work_type,
    ddg51_swbs_dollar_mix_teaching_alternative,
    vendor_swbs_fingerprint_teaching,
    ddg51_hull_confidence_overlay_teaching_factory_chart,
    ddg_hull_linkage_methodology_v4_updated,
)

# Archived (moved to projects/distributed_shipbuilding/_archive/slides/, out of
# the build): ddg_subaward_hull_results, ddg51_hull_linkage_method,
# ddg_hull_linkage_methodology_v4, ddg_subaward_hull_linkage_results.
# Deleted: slide2_worktype_by_program, slide5_worktype_by_fy,
# slide1_outsourced_bc_walk (superseded by slide1_outsourced_bc_walk_updated).

# Cover + four core section dividers + an appendix divider, with the EXISTING
# content slides slotted under the best-matching section. The content set does not
# yet fill the target 13-slide structure (see DECK_STRUCTURE.md for the intended
# grid/reference per slide and the known content gaps) — this wiring sequences the
# slides we have today against that section spine.
SLIDE_RENDERS: list[tuple] = [
    (cover, cover.render),

    # 1 — Market Answer and Scope
    (divider_market_answer_and_scope, divider_market_answer_and_scope.render),
    (definitions_market_levels, definitions_market_levels.render),

    # 2 — TAM Sizing Build
    (divider_tam_sizing_build, divider_tam_sizing_build.render),
    (approach_two_stage_teaching, approach_two_stage_teaching.render),
    (slide1_outsourced_bc_walk_updated, slide1_outsourced_bc_walk_updated.render),

    # 3 — SAM Supplier Market Structure
    (divider_sam_supplier_market_structure, divider_sam_supplier_market_structure.render),
    (slide3_outsourced_bc_annual_tam_ref, slide3_outsourced_bc_annual_tam_ref.render),
    (vendor_swbs_fingerprint_teaching, vendor_swbs_fingerprint_teaching.render),

    # 4 — SAM Ship Construction Lens
    (divider_sam_ship_construction_lens, divider_sam_ship_construction_lens.render),
    (outsourced_spend_by_work_type, outsourced_spend_by_work_type.render),
    (ddg51_swbs_dollar_mix_teaching_alternative, ddg51_swbs_dollar_mix_teaching_alternative.render),

    # Appendix — Methodology and Backup
    (divider_appendix_methodology, divider_appendix_methodology.render),
    (ddg51_hull_confidence_overlay_teaching_factory_chart, ddg51_hull_confidence_overlay_teaching_factory_chart.render),
    (ddg_hull_linkage_methodology_v4_updated, ddg_hull_linkage_methodology_v4_updated.render),
]
