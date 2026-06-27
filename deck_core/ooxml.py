"""deck_core.ooxml - shared OOXML package plumbing (XML decl + namespaces).

Single source of truth for the XML declaration and the OpenXML namespace URIs
used across the build pipeline (primitives, lib, charts) and the probe parser,
so the same strings aren't redeclared (and silently drifting) per file.

Raw geometry / palette / type tokens live in deck_core.style; this module is
only the package-level XML plumbing. Pure data with no dependency on the rest
of deck_core, so importing it is cheap and cycle-free.
"""
from __future__ import annotations

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

# OpenXML namespace URIs.
NS_A  = "http://schemas.openxmlformats.org/drawingml/2006/main"                  # a:  DrawingML
NS_R  = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"    # r:  relationships
NS_P  = "http://schemas.openxmlformats.org/presentationml/2006/main"             # p:  PresentationML
NS_C  = "http://schemas.openxmlformats.org/drawingml/2006/chart"                 # c:  charts
NS_CX = "http://schemas.microsoft.com/office/drawing/2014/chartex"               # cx: chartex
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"            # mc: markup-compat

# Prefix -> URI map, the ElementTree parsing form (used by slide_probe.py).
NS_MAP = {"p": NS_P, "a": NS_A, "r": NS_R, "c": NS_C, "cx": NS_CX, "mc": NS_MC}

# Assembled xmlns attribute string for a <p:sld> / <p:presentation> root — the
# a/r/p trio in the order the locked template emits them (kept byte-stable).
NS = (f'xmlns:a="{NS_A}" '
      f'xmlns:r="{NS_R}" '
      f'xmlns:p="{NS_P}"')

# Assembled xmlns string for chart XML roots (c/a/r order, per charts.py).
NS_CHART = (f'xmlns:c="{NS_C}" '
            f'xmlns:a="{NS_A}" '
            f'xmlns:r="{NS_R}"')
