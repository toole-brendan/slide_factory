#!/usr/bin/env python3
"""Launcher for the awards_methodology deck build pipeline.

Run via:
    python3 build_deck.py

Output:
    awards_methodology.pptx
    (at slide_factory/projects/awards_methodology/)

Thin per-deck project on the shared raw-OOXML ``deck_core`` engine at the
workspace root. All pipeline-specific binding lives in
``awards_methodology/lib.py`` and the slide modules under
``awards_methodology/slides/``. No vendored engine copy.
"""
import sys

from awards_methodology.lib import build


if __name__ == "__main__":
    sys.exit(build())
