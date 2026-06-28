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
    ddg51_outsourced_market_lumpiness_teaching_factory_chart,   # market sizing: modeled outsourced TAM by stream vs. observed SAM overlay (combo_chart)
    ddg51_outsourced_systems_workshare_teaching_factory_chart,  # workshare composition: observed SWBS-coded outsourced spend (ranked bar_chart + tables)
)

SLIDE_RENDERS: list[tuple] = [
    (ddg51_outsourced_market_lumpiness_teaching_factory_chart, ddg51_outsourced_market_lumpiness_teaching_factory_chart.render),
    (ddg51_outsourced_systems_workshare_teaching_factory_chart, ddg51_outsourced_systems_workshare_teaching_factory_chart.render),
]
