#!/usr/bin/env python3
"""Launcher for the style-library reference-corpus build pipeline.

Run via:
    python3 build_deck.py

Output:
    library.pptx
    (at slide_factory/style_library/)

A growing library of styled slides - framework diagrams, value-chain maps,
definition tables, charted exhibits - ported 1:1 from the source market-analysis
decks into native deck_core modules, to serve as a reference corpus for AI agents
authoring custom slide modules. Surrounding shapes and pictures are emitted as
idiomatic deck_core primitives by the converter, which lives at
style_library/_tools/convert_slide.py.

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``library/lib.py`` and
the slide modules under ``library/slides/``. No vendored engine copy.
"""
import sys

from library.lib import build


if __name__ == "__main__":
    sys.exit(build())
