#!/usr/bin/env python3
"""Launcher for the distributed_shipbuilding deck build pipeline.

Run via:
    python3 build_deck.py

Output:
    distributed_shipbuilding.pptx
    (at slide_factory/projects/distributed_shipbuilding/)

Thin per-deck project on the shared raw-OOXML ``deck_core`` engine at the
workspace root. All pipeline-specific binding lives in
``distributed_shipbuilding/lib.py`` and the slide modules under
``distributed_shipbuilding/slides/``. No vendored engine copy.
"""
import sys

from distributed_shipbuilding.lib import build


if __name__ == "__main__":
    sys.exit(build())
