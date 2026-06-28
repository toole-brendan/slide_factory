"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core._build.build_pptx reads to wire
slide layouts, native chart parts, and pictures.

Empty until the first slide is authored. To add a slide:
  1. Create awards_methodology/slides/<name>.py exporting LAYOUT and render().
  2. Import it below and append (<name>, <name>.render) to SLIDE_RENDERS.
"""
from __future__ import annotations

from . import (
    contract_addressability_decision_framework,   # source slide 2: Contract Addressability decision framework (connectors + chrome)
    recompete_timing_color_of_money,              # source slide 3: Recompete Timing — color-of-money obligation windows
    recompete_timing_outlook,                     # source slide 7: Recompete Timing & Outlook — AN/SLQ-25 Nixie timeline (table)
)

SLIDE_RENDERS: list[tuple] = [
    (contract_addressability_decision_framework, contract_addressability_decision_framework.render),
    (recompete_timing_color_of_money, recompete_timing_color_of_money.render),
    (recompete_timing_outlook, recompete_timing_outlook.render),
]
