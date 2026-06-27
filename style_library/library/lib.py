"""Style-library reference-corpus pipeline bindings.

The OOXML engine lives in the shared ``deck_core`` package at the workspace root.
This module is intentionally thin: it binds the things specific to this deck (the
output path, the shared template + brand assets under ``infra/``, the per-deck
images dir, the docProps identity) and packages the registered SLIDE_RENDERS via
the shared builder ``deck_core._build.build_pptx``.

Slide modules import deck_core.* directly; the deck_core import path is set up in
library/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from deck_core._build import build_pptx

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

DECK_DIR = Path(__file__).resolve().parents[1]      # .../slide_factory/style_library/
ROOT = Path(__file__).resolve().parents[2]          # workspace root (holds deck_core/ + infra/)

OUT = DECK_DIR / "library.pptx"

# Shared build chrome lives once under infra/ (not vendored per program).
TEMPLATE = ROOT / "infra" / "template"   # unzipped pptx template (layouts/master/theme)
ASSETS = ROOT / "infra" / "assets"       # brand media/ + embeddings/
IMAGES = DECK_DIR / "library" / "slides" / "images"  # per-deck pictures (converter-populated)

_TITLE = "library"
_CREATOR = "library build_deck.py"
_APP = "library"


def build() -> int:
    """Render every registered slide and package into the output .pptx."""
    from library.slides import SLIDE_RENDERS
    if not SLIDE_RENDERS:
        raise SystemExit(
            "library/slides/__init__.py SLIDE_RENDERS is empty - "
            "convert a slide before building."
        )
    images = IMAGES if IMAGES.is_dir() else None
    build_pptx(SLIDE_RENDERS, out=OUT, extracted=TEMPLATE, assets=ASSETS,
               title=_TITLE, creator=_CREATOR, app=_APP, images=images)
    return 0
