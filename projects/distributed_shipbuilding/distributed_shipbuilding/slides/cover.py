"""Deck cover (title) slide — DDG-51 New-Construction Supplier Market.

A two-line title lockup on the Cover layout (slideLayout1): deck title (28pt)
over an italic subtitle (20pt), plus a small project/date footer line. No
exhibit, no breadcrumb, no Preliminary chip — cover/divider slides are exempt
from the body-slide chrome. The composition helper owns the locked geometry; the
module only supplies the three text lines.
"""
from __future__ import annotations

from deck_core.authoring import slide, cover_layout

LAYOUT = "slideLayout1"


def render() -> str:
    return slide(cover_layout(
        "DDG-51 New-Construction Supplier Market",
        "Size outsourced work and identify priority supplier pools.",
        footer="Distributed Shipbuilding · Preliminary · June 2026",
    ))
