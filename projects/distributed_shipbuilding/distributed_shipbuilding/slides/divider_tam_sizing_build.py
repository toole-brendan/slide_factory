"""Section divider — TAM Sizing Build.

Section title (28pt) over an italic subtitle (20pt) on the Section Divider
layout (slideLayout2). No exhibit. Opens the top-down TAM build section.
"""
from __future__ import annotations

from deck_core.authoring import slide, section_divider_layout

LAYOUT = "slideLayout2"


def render() -> str:
    return slide(section_divider_layout(
        "TAM Sizing Build",
        "Build the supplier-addressable opportunity from construction spend.",
    ))
