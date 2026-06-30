"""Section divider — SAM Supplier Market Structure.

Section title (28pt) over an italic subtitle (20pt) on the Section Divider
layout (slideLayout2). No exhibit. Opens the observed-subaward supplier section
(annual activity, where-to-play, concentration, priority pools).
"""
from __future__ import annotations

from deck_core.authoring import slide, section_divider_layout

LAYOUT = "slideLayout2"


def render() -> str:
    return slide(section_divider_layout(
        "SAM Supplier Market Structure",
        "Use observed subawards to assess supplier pools.",
    ))
