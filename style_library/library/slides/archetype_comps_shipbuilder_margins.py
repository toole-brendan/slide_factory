"""archetype_comps_shipbuilder_margins — Commercial Strategy Market Analysis deck (20260325), source slide 34.

EXHIBIT — "Archetype Comps (3/3)": shipbuilder margin profile holds across
geographies and vessel types. The body is a small-multiples stack of FIVE
styled charts, one per fiscal year, drawn bottom-to-top in chronological order
(2020 · 2021 · 2022 · 2023 · 2024). Each panel is a Revenue ($B, bars) +
EBIT-Margin (%, line) combo across the same company set, which is grouped left-
to-right into archetype bands keyed by the bar fill — Shipbuilders (red C30C3E:
Austal · Hanwha Ocean · Fincantieri · HD Hyundai KSOE · Samsung Heavy), the
Owner/Operator carrier segment (blue 364D6E: Matson · ZIM · Hapag Lloyd · Maersk ·
Danaos · Costamare · Seaspan) and Terminal Operators (blue 6F8DB9: HPHT · ICTS ·
Maersk Terminals). Coloured banners head the bands ("Shipbuilders" · a green
"Charter Companies" tag + the blue "Owner/Operator (Carrier Segment)" header ·
"Terminal Operators"); per-bar revenue chips and per-point margin labels annotate
every panel; vertical rules and per-row dashed baselines separate the panels and
archetypes; the left margin carries one fill-coded year tag per panel. Axis
legends (top) read "Revenue ($B, bars)" and "EBIT Margin (%, lines)".

CODE MAP (body follows source PAINT ORDER; headers mark roles in place — note the
shared label tables are painted ONCE up front and span all five panels, so they
do NOT sit beside their charts):
  • chrome ................ breadcrumb() + title_placeholder() + prelim_chip()
  • Source line .......... "Source: Company filings" (off-house, kept verbatim)
  • chart 0 (2020) ....... graphic_frame(rId2) → CHARTS[0] = styled_chart(...)
  • _VALUE_TICK_LABELS ... shared value-axis numeric ticks across all panels
  • _CATEGORY_TICK_LABELS  company category labels in single/wrapped buckets
  • _DATA_LABELS ......... margin-point labels and revenue-chip labels
  • _GROUP_HEADERS ....... the three archetype band headers
  • _PANEL_LABELS ........ the five year tags in upper/lower paint-order buckets
  • carrier banner ....... "Owner/Operator (Carrier Segment)" archetype header
  • chart 1 (2021) ....... graphic_frame(rId3) + its connectors (rules/baselines)
  • chart 2 (2022) ....... graphic_frame(rId4) + its connectors
  • chart 3 (2023) ....... graphic_frame(rId5) + its connector
  • chart 4 (2024) ....... graphic_frame(rId6) + its connector
  • axis legends ......... "EBIT Margin (%, lines)" + "Revenue ($B, bars)"
  • archetype dividers ... 3 full-height vertical rules between the archetype bands

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated (applies
to all five _CHART*_DATA literals).

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=4, connector=13, chart=5, chrome_builders=3,
clusters=7 (covering 194 shapes), frozen_fields=186, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder, prelim_chip,
    graphic_frame, styled_chart, IN, PT, BLACK, WHITE, DK, BREADCRUMB, GRAY_1, GRAY_2,
    GRAY_3, FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide34_chart19.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide34_chart19.xlsb").read_bytes()
_CHART1_TPL = (_SRC / "slide34_chart20.xml").read_text(encoding="utf-8")
_XLSB1 = (_SRC / "slide34_chart20.xlsb").read_bytes()
_CHART2_TPL = (_SRC / "slide34_chart21.xml").read_text(encoding="utf-8")
_XLSB2 = (_SRC / "slide34_chart21.xlsb").read_bytes()
_CHART3_TPL = (_SRC / "slide34_chart22.xml").read_text(encoding="utf-8")
_XLSB3 = (_SRC / "slide34_chart22.xlsb").read_bytes()
_CHART4_TPL = (_SRC / "slide34_chart23.xml").read_text(encoding="utf-8")
_XLSB4 = (_SRC / "slide34_chart23.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [1410, 6445, 7190, None, 21176, 1854, 3992, 14577, 29175, 462, 460, 1231, 3807, 1381, 1506]},
        {"values": [6.7, 2.2, 2.5, None, -7.8, 13.2, 18.3, 10.3, 11, 43.2, 13.1, 42.4, 31.7, 32.8, 43]},
    ],
}

_CHART1_DATA = {
    "categories": None,
    "series": [
        {"values": [1089, 3786, 7822, None, 19771, 3133, 10729, 26356, 48232, 690, 794, 1470, 4000, 1698, 1865]},
        {"values": [7.8, -39, 4.2, None, -3, 36.3, 54.2, 42.2, 37.2, 51.9, 55.6, 47.9, 29.3, 40.6, 47.8]},
    ],
}

_CHART2_DATA = {
    "categories": None,
    "series": [
        {"values": [1026, 3857, 8004, 11785, 20791, 3545, 12562, 36401, 64299, 993, 1114, 1556, 4371, 1559, 2243]},
        {"values": [3.8, -33.2, -0.1, 0.3, 1.9, 36.1, 48.9, 50.7, 45.3, 65.8, 59.5, 14.1, 19, 35.2, 50.9]},
    ],
}

_CHART3_DATA = {
    "categories": None,
    "series": [
        {"values": [1049, 5739, 8464, 16496, 25097, 2477, 5162, 19210, 33653, 974, 1511, 1715, 3844, 1362, 2388]},
        {"values": [1.8, 2.7, 3.2, 1.3, 3.1, 11.9, -8.2, 14.1, 6.6, 59.6, 31, 21.3, 25.5, 31.2, 50.7]},
    ],
}

_CHART4_DATA = {
    "categories": None,
    "series": [
        {"values": [1018, 7292, 8413, 17280, 23480, 2810, 8427, 20287, 37388, 1014, 2084, 2312, 4465, 1489, 2740]},
        {"values": [5.2, 2.2, 2, 5.6, 2.3, 17.8, 42.1, 13.4, 12.7, 53.3, 22.2, 27.4, 29.8, 37.8, 54]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0), styled_chart(_CHART1_TPL, _CHART1_DATA, _XLSB1), styled_chart(_CHART2_TPL, _CHART2_DATA, _XLSB2), styled_chart(_CHART3_TPL, _CHART3_DATA, _XLSB3), styled_chart(_CHART4_TPL, _CHART4_DATA, _XLSB4)]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_TICK_H = IN(0.134)                  # y-axis numeric-tick box height
_COMPANY_LBL_Y, _COMPANY_LBL_H = IN(6.545), IN(0.134)   # x-axis company-name row
_MARGIN_LBL_H = IN(0.134)                 # EBIT-margin % label height
_BAR_CHIP_H = IN(0.134)                   # revenue bar-chip height
_COMPANY_WRAP_Y, _COMPANY_WRAP_H = IN(6.545), IN(0.267) # wrapped (two-line) names
_YEAR_X, _YEAR_W, _YEAR_H = IN(0.057), IN(0.609), IN(0.858)  # left-margin year tag box
_GRID_X = IN(0.939)   # shared x5 — left edge of the dashed panel baselines

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the shared EBIT-margin-% value-axis ticks, painted once and spanning all five
#   year panels.
_VALUE_TICK_LABELS = [    # shared value-axis numeric ticks across all five panels
    (0.804, 6.378, 0.062, "0"),
    (0.741, 6.155, 0.125, "20"),
    (0.741, 5.931, 0.125, "40"),
    (0.741, 5.707, 0.125, "60"),
    (0.741, 5.483, 0.125, "80"),
    (0.741, 5.123, 0.125, "20"),
    (0.741, 4.899, 0.125, "40"),
    (0.741, 4.675, 0.125, "60"),
    (0.741, 4.451, 0.125, "80"),
    (0.804, 5.347, 0.062, "0"),
    (0.741, 4.092, 0.125, "20"),
    (0.741, 3.868, 0.125, "40"),
    (0.741, 3.644, 0.125, "60"),
    (0.741, 3.42, 0.125, "80"),
    (0.804, 4.316, 0.062, "0"),
    (0.741, 3.061, 0.125, "20"),
    (0.741, 2.837, 0.125, "40"),
    (0.741, 2.613, 0.125, "60"),
    (0.741, 2.389, 0.125, "80"),
    (0.804, 3.285, 0.062, "0"),
    (0.741, 2.03, 0.125, "20"),
    (0.741, 1.806, 0.125, "40"),
    (0.741, 1.582, 0.125, "60"),
    (0.741, 1.358, 0.125, "80"),
    (0.804, 2.253, 0.062, "0"),
]

# local_meaning: per-panel x-axis company names (the shipbuilders compared), keyed by panel;
#   includes the three names that wrap to two lines.
_CATEGORY_TICK_LABELS = {
    # Buckets preserve the single-line loop and the later wrapped-label loop.
    "single_line": [
        (1.17, 0.325, "Austal"),
        (1.729, 0.785, "Hanwha Ocean"),
        (2.646, 0.528, "Fincantieri"),
        (4.957, 0.639, "Matson (OT)"),
        (5.962, 0.205, "ZIM"),
        (6.533, 0.642, "Hapag Lloyd"),
        (7.325, 0.637, "Maersk (OT)"),
        (8.231, 0.399, "Danaos"),
        (8.941, 0.559, "Costamare"),
        (9.781, 0.457, "Seaspan"),
        (11.429, 0.316, "HPHT"),
        (12.241, 0.267, "ICTS"),
    ],
    "wrapped": [
        (3.391, 0.615, "HD Hyundai KSOE"),
        (4.245, 0.486, "Samsung Heavy"),
        (10.51, 0.575, "Maersk (Terminals)"),
    ],
}

# local_meaning: per-panel on-plot annotations keyed by panel: the EBIT-margin-% point labels
#   and the revenue $B bar chips (white-on-fill, fill keys archetype).
_DATA_LABELS = {
    # Point labels and filled bar chips share the plotted-data role but retain
    # separate paint-order/style loops.
    "margin_points": [
        (2.026, 5.856, 0.193, "2%"),
        (2.816, 5.854, 0.193, "3%"),
        (4.373, 5.917, 0.229, "-8%"),
        (5.151, 5.792, 0.255, "13%"),
        (5.939, 5.76, 0.255, "18%"),
        (6.727, 5.809, 0.255, "10%"),
        (7.517, 5.804, 0.255, "11%"),
        (8.306, 5.611, 0.255, "43%"),
        (9.094, 5.792, 0.255, "13%"),
        (9.884, 5.616, 0.255, "42%"),
        (1.238, 5.83, 0.193, "7%"),
        (10.672, 5.681, 0.255, "32%"),
        (11.46, 5.674, 0.255, "33%"),
        (12.25, 5.613, 0.255, "43%"),
        (1.238, 4.792, 0.193, "8%"),
        (1.976, 5.071, 0.292, "-39%"),
        (2.816, 4.814, 0.193, "4%"),
        (4.373, 4.856, 0.229, "-3%"),
        (5.151, 4.622, 0.255, "36%"),
        (5.939, 4.516, 0.255, "54%"),
        (6.727, 4.587, 0.255, "42%"),
        (7.517, 4.616, 0.255, "37%"),
        (8.306, 4.528, 0.255, "52%"),
        (9.094, 4.507, 0.255, "56%"),
        (9.884, 4.552, 0.255, "48%"),
        (10.672, 4.663, 0.255, "29%"),
        (11.46, 4.595, 0.255, "41%"),
        (12.25, 4.554, 0.255, "48%"),
        (2.816, 3.807, 0.193, "0%"),
        (3.604, 3.806, 0.193, "0%"),
        (4.392, 3.795, 0.193, "2%"),
        (5.151, 3.592, 0.255, "36%"),
        (5.939, 3.516, 0.255, "49%"),
        (7.517, 3.536, 0.255, "45%"),
        (8.306, 3.415, 0.255, "66%"),
        (9.094, 3.451, 0.255, "60%"),
        (9.884, 3.722, 0.255, "14%"),
        (10.672, 3.694, 0.255, "19%"),
        (11.46, 3.597, 0.255, "35%"),
        (12.25, 3.503, 0.255, "51%"),
        (1.238, 3.785, 0.193, "4%"),
        (1.976, 4.005, 0.292, "-33%"),
        (6.727, 3.505, 0.255, "51%"),
        (1.238, 2.766, 0.193, "2%"),
        (2.026, 2.76, 0.193, "3%"),
        (2.816, 2.757, 0.193, "3%"),
        (3.604, 2.769, 0.193, "1%"),
        (4.392, 2.757, 0.193, "3%"),
        (5.151, 2.705, 0.255, "12%"),
        (5.951, 2.825, 0.229, "-8%"),
        (6.727, 2.691, 0.255, "14%"),
        (7.549, 2.736, 0.193, "7%"),
        (8.306, 2.42, 0.255, "60%"),
        (9.094, 2.59, 0.255, "31%"),
        (9.884, 2.649, 0.255, "21%"),
        (10.672, 2.623, 0.255, "26%"),
        (11.46, 2.59, 0.255, "31%"),
        (12.25, 2.474, 0.255, "51%"),
        (1.238, 1.714, 0.193, "5%"),
        (2.026, 1.731, 0.193, "2%"),
        (2.816, 1.733, 0.193, "2%"),
        (3.604, 1.712, 0.193, "6%"),
        (4.392, 1.731, 0.193, "2%"),
        (5.151, 1.639, 0.255, "18%"),
        (6.727, 1.665, 0.255, "13%"),
        (7.517, 1.668, 0.255, "13%"),
        (8.306, 1.427, 0.255, "53%"),
        (9.094, 1.613, 0.255, "22%"),
        (9.884, 1.582, 0.255, "27%"),
        (10.672, 1.566, 0.255, "30%"),
        (11.46, 1.519, 0.255, "38%"),
        (12.25, 1.422, 0.255, "54%"),
        (5.939, 1.493, 0.255, "42%"),
    ],
    "revenue_chips": [
        (2.075, 6.342, 0.094, "C30C3E", "6"),   # C30C3E crimson
        (2.863, 6.339, 0.094, "C30C3E", "7"),   # C30C3E crimson
        (4.41, 6.259, 0.156, "C30C3E", "21"),   # C30C3E crimson
        (5.229, 6.368, 0.094, "364D6E", "2"),   # 364D6E dark blue
        (6.017, 6.356, 0.094, "364D6E", "4"),   # 364D6E dark blue
        (6.776, 6.297, 0.156, None, "15"),   # FFFFFF white
        (7.564, 6.215, 0.156, None, "29"),   # FFFFFF white
        (8.384, 6.375, 0.094, "007770", "0"),   # 007770 teal
        (9.174, 6.375, 0.094, "007770", "0"),   # 007770 teal
        (10.75, 6.356, 0.094, "6F8DB9", "4"),   # 6F8DB9 blue
        (9.962, 6.372, 0.094, "007770", "1"),   # 007770 teal
        (12.328, 6.37, 0.094, "6F8DB9", "2"),   # 6F8DB9 blue
        (1.285, 6.37, 0.094, "C30C3E", "1"),   # C30C3E crimson
        (11.54, 6.37, 0.094, "6F8DB9", "1"),   # 6F8DB9 blue
        (1.285, 5.34, 0.094, "C30C3E", "1"),   # C30C3E crimson
        (2.075, 5.326, 0.094, "C30C3E", "4"),   # C30C3E crimson
        (2.863, 5.304, 0.094, "C30C3E", "8"),   # C30C3E crimson
        (4.41, 5.236, 0.156, None, "20"),   # FFFFFF white
        (5.229, 5.33, 0.094, "364D6E", "3"),   # 364D6E dark blue
        (5.986, 5.286, 0.156, None, "11"),   # FFFFFF white
        (7.564, 5.076, 0.156, None, "48"),   # FFFFFF white
        (8.384, 5.344, 0.094, "007770", "1"),   # 007770 teal
        (9.174, 5.342, 0.094, "007770", "1"),   # 007770 teal
        (9.962, 5.339, 0.094, "007770", "1"),   # 007770 teal
        (10.75, 5.325, 0.094, "6F8DB9", "4"),   # 6F8DB9 blue
        (11.54, 5.337, 0.094, "6F8DB9", "2"),   # 6F8DB9 blue
        (12.328, 5.337, 0.094, "6F8DB9", "2"),   # 6F8DB9 blue
        (6.776, 5.2, 0.156, None, "26"),   # FFFFFF white
        (2.075, 4.293, 0.094, "C30C3E", "4"),   # C30C3E crimson
        (2.863, 4.271, 0.094, "C30C3E", "8"),   # C30C3E crimson
        (3.62, 4.25, 0.156, None, "12"),   # FFFFFF white
        (4.41, 4.2, 0.156, None, "21"),   # FFFFFF white
        (5.229, 4.295, 0.094, "364D6E", "4"),   # 364D6E dark blue
        (5.986, 4.245, 0.156, None, "13"),   # FFFFFF white
        (6.776, 4.111, 0.156, None, "36"),   # FFFFFF white
        (7.564, 3.955, 0.156, None, "64"),   # FFFFFF white
        (8.384, 4.311, 0.094, "007770", "1"),   # 007770 teal
        (9.174, 4.309, 0.094, "007770", "1"),   # 007770 teal
        (9.962, 4.307, 0.094, "007770", "2"),   # 007770 teal
        (10.75, 4.292, 0.094, "6F8DB9", "4"),   # 6F8DB9 blue
        (11.54, 4.307, 0.094, "6F8DB9", "2"),   # 6F8DB9 blue
        (12.328, 4.304, 0.094, "6F8DB9", "2"),   # 6F8DB9 blue
        (1.285, 4.309, 0.094, "C30C3E", "1"),   # C30C3E crimson
        (1.285, 3.278, 0.094, "C30C3E", "1"),   # C30C3E crimson
        (2.075, 3.252, 0.094, "C30C3E", "6"),   # C30C3E crimson
        (2.863, 3.236, 0.094, "C30C3E", "8"),   # C30C3E crimson
        (3.62, 3.193, 0.156, None, "16"),   # FFFFFF white
        (4.41, 3.144, 0.156, None, "25"),   # FFFFFF white
        (5.229, 3.271, 0.094, "364D6E", "2"),   # 364D6E dark blue
        (6.776, 3.177, 0.156, None, "19"),   # FFFFFF white
        (7.564, 3.095, 0.156, None, "34"),   # FFFFFF white
        (8.384, 3.28, 0.094, "007770", "1"),   # 007770 teal
        (9.174, 3.276, 0.094, "007770", "2"),   # 007770 teal
        (9.962, 3.274, 0.094, "007770", "2"),   # 007770 teal
        (10.75, 3.262, 0.094, "6F8DB9", "4"),   # 6F8DB9 blue
        (11.54, 3.276, 0.094, "6F8DB9", "1"),   # 6F8DB9 blue
        (12.328, 3.271, 0.094, "6F8DB9", "2"),   # 6F8DB9 blue
        (6.017, 3.255, 0.094, "364D6E", "5"),   # 364D6E dark blue
        (1.285, 2.247, 0.094, "C30C3E", "1"),   # C30C3E crimson
        (2.075, 2.212, 0.094, "C30C3E", "7"),   # C30C3E crimson
        (2.863, 2.207, 0.094, "C30C3E", "8"),   # C30C3E crimson
        (3.62, 2.156, 0.156, None, "17"),   # FFFFFF white
        (4.41, 2.122, 0.156, None, "23"),   # FFFFFF white
        (5.229, 2.238, 0.094, "364D6E", "3"),   # 364D6E dark blue
        (6.017, 2.207, 0.094, "364D6E", "8"),   # 364D6E dark blue
        (6.776, 2.139, 0.156, None, "20"),   # FFFFFF white
        (7.564, 2.043, 0.156, None, "37"),   # FFFFFF white
        (8.384, 2.247, 0.094, "007770", "1"),   # 007770 teal
        (9.174, 2.241, 0.094, "007770", "2"),   # 007770 teal
        (9.962, 2.24, 0.094, "007770", "2"),   # 007770 teal
        (10.75, 2.227, 0.094, "6F8DB9", "4"),   # 6F8DB9 blue
        (11.54, 2.245, 0.094, "6F8DB9", "1"),   # 6F8DB9 blue
        (12.328, 2.238, 0.094, "6F8DB9", "3"),   # 6F8DB9 blue
    ],
}

# local_meaning: the three archetype band headers (Shipbuilders / Owner-Operators / Terminal
#   Operators) labeling the left-to-right archetype bands.
_GROUP_HEADERS = [    # archetype band headers
    (1.158, 6.822, 3.653, 0.155, "C30C3E", "Shipbuilders"),         # headers (rows 1-3) + the
    (8.21, 6.822, 2.102, 0.155, "207349", "Charter Companies"),      # 2023/2024 year tags (rows
    (10.617, 6.822, 2.102, 0.155, "6F8DB9", "Terminal Operators"),   # 4-5); grouped only by a
]

# local_meaning: per-panel labels keyed by panel: the fill-coded left-margin year tag
#   (2020-2024) for each panel plus the upper archetype-band caption.
_PANEL_LABELS = {
    # Upper two tags paint with the band headers; lower three paint after charts.
    "upper_panels": [
        (0.057, 2.474, 0.609, 0.858, "A6A6A6", "2023"),                  # shared ctr-anchored fill
        (0.057, 1.443, 0.609, 0.858, "808080", "2024"),                  # style, not by meaning
    ],
    "lower_panels": [
        (5.554, GRAY_1, "2020"),   # F2F2F2 off-white
        (4.457, GRAY_2, "2021"),   # D9D9D9 light gray
        (3.439, GRAY_3, "2022"),   # BFBFBF silver-gray
    ],
}

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Commercial Maritime Value Chain", "Performance"))
    out.append(title_placeholder("Archetype Comps (3/3)", "Shipbuilder margin profile holds across geographies and vessel types."))
    # Source line — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 1964", IN(0.495), IN(7.006), IN(5.102), IN(0.349), [paragraph([run("Source: Company filings", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── chart 0: 2020 panel (bottom) — bundled verbatim + .xlsb ("Edit Data" works) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.849), y=IN(5.41), cx=IN(12.318), cy=IN(1.175), rId="rId2"))
    # ── shared value-axis ticks (0/20/40/60/80 per band, all panels) ──
    for _x, _y, _cx, _t in _VALUE_TICK_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), _AXIS_TICK_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(connector(n(), "Straight Connector 2020", _GRID_X, IN(6.146), IN(11.832), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    # ── shared category labels (single-line) ──
    for _x, _cx, _t in _CATEGORY_TICK_LABELS["single_line"]:
        out.append(text_box(n(), "Label", IN(_x), _COMPANY_LBL_Y, IN(_cx), _COMPANY_LBL_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── plotted-data labels: EBIT-margin points ──
    for _x, _y, _cx, _t in _DATA_LABELS["margin_points"]:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _MARGIN_LBL_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=14288, t_ins=0, r_ins=14288, b_ins=0))   # 000000 black
    # ── plotted-data labels: revenue chips, white-on-fill ──
    for _x, _y, _cx, _fill, _t in _DATA_LABELS["revenue_chips"]:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), _BAR_CHIP_H, [paragraph([run(_t, size=PT(8), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=14288, t_ins=0, r_ins=14288, b_ins=0))
    # ── shared category labels that wrap to two lines ──
    for _x, _cx, _t in _CATEGORY_TICK_LABELS["wrapped"]:
        out.append(text_box(n(), "Label", IN(_x), _COMPANY_WRAP_Y, IN(_cx), _COMPANY_WRAP_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── archetype group headers, then upper-panel year labels ──
    for _x, _y, _cx, _cy, _fill, _t in _GROUP_HEADERS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _t in _PANEL_LABELS["upper_panels"]:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    # carrier-segment archetype header (interleaves with the banners in paint order)
    out.append(text_box(n(), "Rectangle 2147", IN(5.068), IN(6.822), IN(2.833), IN(0.155), [paragraph([run("Owner/Operator ", size=PT(10), bold=True, color=WHITE, font=FONT), run("(Carrier Segment)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="364D6E", line_color="none", anchor="ctr"))   # 364D6E dark blue
    # ── chart 1: 2021 panel + its connectors (panel rules / dashed baselines) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.849), y=IN(4.378), cx=IN(12.318), cy=IN(1.175), rId="rId3"))
    out.append(connector(n(), "Straight Connector 384", _GRID_X, IN(5.115), IN(1.024), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 2529", IN(2.28), IN(5.115), IN(5.273), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 2530", IN(7.733), IN(5.115), IN(5.038), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 2528", IN(2.122), IN(5.205), IN(0), IN(0.003), color=BREADCRUMB, width=6350, dashed=True, arrow=True))   # 44505C slate gray
    # ── chart 2: 2022 panel + its connectors ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.849), y=IN(3.347), cx=IN(12.318), cy=IN(1.175), rId="rId4"))
    out.append(connector(n(), "Straight Connector 2180", _GRID_X, IN(4.083), IN(1.024), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 2484", IN(2.28), IN(4.083), IN(5.273), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 2485", IN(7.733), IN(4.083), IN(5.038), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    # ── chart 3: 2023 panel + its connector ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.849), y=IN(2.316), cx=IN(12.318), cy=IN(1.175), rId="rId5"))
    out.append(connector(n(), "Straight Connector 2205", _GRID_X, IN(3.052), IN(11.832), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    # ── chart 4: 2024 panel (top) + its connector ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.849), y=IN(1.285), cx=IN(12.318), cy=IN(1.175), rId="rId6"))
    out.append(connector(n(), "Straight Connector 2230", _GRID_X, IN(2.021), IN(11.832), IN(0), color=DK, width=9525, dashed=True, arrow=True))   # 162029 dark navy
    # ── axis legends (top) ──
    out.append(text_box(n(), "Text Placeholder 25", IN(11.898), IN(1.135), IN(1.17), IN(0.134), [paragraph([run("EBIT Margin (%, lines)", size=PT(8), bold=True, color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(0.741), IN(1.135), IN(1.01), IN(0.134), [paragraph([run("Revenue ($B, bars)", size=PT(8), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── lower-panel year labels ──
    for _y, _fill, _t in _PANEL_LABELS["lower_panels"]:
        out.append(text_box(n(), "YearLabel", _YEAR_X, IN(_y), _YEAR_W, _YEAR_H, [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    # ── archetype dividers: full-height vertical rules between the bands ──
    out.append(connector(n(), "Straight Arrow Connector 2596", IN(4.939), IN(1.377), IN(0), IN(5.6), color="808080", width=12700))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 2598", IN(8.056), IN(1.377), IN(0), IN(5.6), color="808080", width=12700))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 2602", IN(10.465), IN(1.377), IN(0), IN(5.6), color="808080", width=12700))   # 808080 gray
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
