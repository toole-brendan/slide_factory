"""Section divider — Methodology and Backup (appendix).

Section title (28pt) over an italic subtitle (20pt) on the Section Divider
layout (slideLayout2). No exhibit. Opens the diligence-ready appendix
(definitions, mappings, assumptions, sources).
"""
from __future__ import annotations

from deck_core.authoring import slide, section_divider_layout

LAYOUT = "slideLayout2"


def render() -> str:
    return slide(section_divider_layout(
        "Methodology and Backup",
        "Document definitions, mappings, assumptions, and sources.",
    ))
