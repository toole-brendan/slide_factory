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
    vendor_swbs_fingerprint_teaching,
    ddg51_hull_confidence_overlay_teaching_factory_chart,
    approach_two_stage_teaching,
    ddg51_swbs_dollar_mix_teaching_alternative,
    ddg_subaward_hull_results,
    ddg51_hull_linkage_method,
    ddg_hull_linkage_methodology_v4,
)

SLIDE_RENDERS: list[tuple] = [
    (vendor_swbs_fingerprint_teaching, vendor_swbs_fingerprint_teaching.render),
    (ddg51_hull_confidence_overlay_teaching_factory_chart, ddg51_hull_confidence_overlay_teaching_factory_chart.render),
    (approach_two_stage_teaching, approach_two_stage_teaching.render),
    (ddg51_swbs_dollar_mix_teaching_alternative, ddg51_swbs_dollar_mix_teaching_alternative.render),
    (ddg_subaward_hull_results, ddg_subaward_hull_results.render),
    (ddg51_hull_linkage_method, ddg51_hull_linkage_method.render),
    (ddg_hull_linkage_methodology_v4, ddg_hull_linkage_methodology_v4.render),
]
