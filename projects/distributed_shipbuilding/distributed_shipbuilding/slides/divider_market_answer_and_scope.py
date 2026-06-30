"""Section divider — Market Answer and Scope.

Section title (28pt) over an italic subtitle (20pt) on the Section Divider
layout (slideLayout2). No exhibit. Opens the section that defines the market and
states the answer.
"""
from __future__ import annotations

from deck_core.authoring import slide, section_divider_layout

LAYOUT = "slideLayout2"


def render() -> str:
    return slide(section_divider_layout(
        "Market Answer and Scope",
        "Define the market and state the answer.",
    ))
