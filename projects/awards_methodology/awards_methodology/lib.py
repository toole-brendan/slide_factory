"""awards_methodology deck pipeline bindings.

The OOXML engine lives in the shared ``deck_core`` package at the workspace root.
This module is intentionally thin: it binds the things specific to this deck (the
output path, the shared template + brand assets under ``infra/``, the per-deck
images dir, the docProps identity) and packages the registered SLIDE_RENDERS via
the shared builder ``deck_core._build.build_pptx``.

Slide modules import deck_core.* directly; the deck_core import path is set up in
awards_methodology/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from deck_core._build import build_pptx

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

DECK_DIR = Path(__file__).resolve().parents[1]   # .../projects/awards_methodology/
ROOT = Path(__file__).resolve().parents[3]       # workspace root (holds deck_core/ + infra/)

OUT = DECK_DIR / "awards_methodology.pptx"

# Shared build chrome lives once under infra/ (not vendored per program).
TEMPLATE = ROOT / "infra" / "template"   # unzipped pptx template (layouts/master/theme)
ASSETS = ROOT / "infra" / "assets"       # brand media/ + embeddings/
IMAGES = DECK_DIR / "awards_methodology" / "slides" / "images"  # per-deck pictures

_TITLE = "Awards Methodology"
_CREATOR = "awards_methodology build_deck.py"
_APP = "awards_methodology"


def build() -> int:
    """Render every registered slide and package into the output .pptx."""
    from awards_methodology.slides import SLIDE_RENDERS
    if not SLIDE_RENDERS:
        raise SystemExit(
            "awards_methodology/slides/__init__.py SLIDE_RENDERS is empty - "
            "add a slide before building."
        )
    images = IMAGES if IMAGES.is_dir() else None
    build_pptx(SLIDE_RENDERS, out=OUT, extracted=TEMPLATE, assets=ASSETS,
               title=_TITLE, creator=_CREATOR, app=_APP, images=images)
    return 0
