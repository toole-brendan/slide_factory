"""Section divider — SAM Ship Construction Lens.

Section title (28pt) over an italic subtitle (20pt) on the Section Divider
layout (slideLayout2). No exhibit. Opens the ship-system / build-stage view of
the observed supplier work.
"""
from __future__ import annotations

from deck_core.authoring import slide, section_divider_layout

LAYOUT = "slideLayout2"


def render() -> str:
    return slide(section_divider_layout(
        "SAM Ship Construction Lens",
        "Map observed supplier work to ship systems and build stages.",
    ))
