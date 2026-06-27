"""<slide_name> - ONE-SENTENCE INTENT: what this slide proves.

Start from an exemplar: copy the closest module in style_library/library/slides/
and adapt it. The full vocabulary is one import from deck_core.authoring.
"""
from __future__ import annotations

from deck_core.authoring import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
)

LAYOUT = "slideLayout4"

_SECTION  = "Section"
_TOPIC    = "Topic Label"
_TAKEAWAY = "the one-line finding."
_SOURCES  = "Source: ...; ..."


def _body() -> str:
    return ""   # build the body here


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
