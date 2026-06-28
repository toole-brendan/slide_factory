"""Teaching exemplar: Archetype Comps (3/3) — shipbuilder margin small multiples.

ROLE
  archetype_comparison / margin_profile_small_multiples

USE WHEN
  A slide needs to compare a revenue scale and EBIT-margin profile across many
  companies, repeated across several fiscal-year panels, while keeping the
  archetype groupings visible.

TEACHES
  - fully declarative native column_chart panels instead of bundled chart XML
  - five aligned small-multiple chart frames sharing one category-label row
  - workbook-sourced revenue bars with source chart-part data-point colors
  - manually overlaid EBIT-margin dash markers from the source secondary axis
  - manually placed margin labels and revenue chips across all panels
  - archetype band headers, year tags, shared value-axis ticks, and dividers

TEXT-FIT PRECEDENT
  margin_point_labels:
    geometry: 0.193-0.292in wide x 0.134in high
    type: Arial 8pt, black, zero insets, no wrap
    content: one rounded whole-percent label; negative values need the wider box
  revenue_chips:
    geometry: 0.094-0.156in wide x 0.134in high
    type: Arial 8pt, white, centered
    content: one or two digits only, because values are shown in $B
  company_labels:
    geometry: 0.205-0.785in wide x 0.134in high; wrapped names use 0.267in high
    type: Arial 8pt, black, zero insets
    copy_when: a dense small-multiple chart needs exact category registration
               but native chart tick labels would be too loose or tall

SOURCE NOTE
  Teaching rewrite of source-faithful `archetype_comps_shipbuilder_margins.py`.
  The original used five `styled_chart(...)` calls backed by
  slide34_chart19.xml/.xlsb through slide34_chart23.xml/.xlsb. This version
  intentionally replaces those template dependencies with five native editable
  `column_chart(mode="stacked", ...)` specs for revenue bars. The EBIT-margin
  series from the source combo charts is preserved as explicit, editable yellow
  dash-marker connectors positioned from the source secondary-axis scale.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. It preserves the source workbook rows, chart XML layout/scales, gap and
  overlap, revenue bar point fills, manual labels/chips, year tags, group headers,
  baseline rules, source note, and off-house Preliminary chip. The source combo
  chart's EBIT line had `a:noFill` and per-point yellow `dash` markers; the
  markers are therefore drawn manually rather than as a native line chart.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, paragraph, run,
    text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BREADCRUMB = "44505C"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

# ════════════════════════════════════════════════════════════════════════════
# Source chart data and factory-native chart specifications.
# ════════════════════════════════════════════════════════════════════════════
SHIPBUILDER_RED = "C30C3E"
OWNER_OPERATOR_BLUE = "364D6E"
CHARTER_GREEN = "007770"
TERMINAL_BLUE = "6F8DB9"
EBIT_MARKER_YELLOW = "FFC000"

COMPANY_CATEGORIES: tuple[str, ...] = ('Austal',
 'Hanwha Ocean',
 'Fincantieri',
 'HD Hyundai KSOE',
 'Samsung Heavy',
 'Matson (OT)',
 'ZIM',
 'Hapag Lloyd',
 'Maersk (OT)',
 'Danaos',
 'Costamare',
 'Seaspan',
 'Maersk (Terminals)',
 'HPHT',
 'ICTS')

# The five workbook row pairs below were read from slide34_chart19.xlsb through
# slide34_chart23.xlsb, Sheet1. Row 1 = revenue ($M); row 2 = EBIT margin (%).
# The source XML numRef caches mirror these rows exactly.
SOURCE_XLSB_ROWS_BY_YEAR: dict[int, tuple[tuple[float | int | None, ...], tuple[float | int | None, ...]]] = {2020: ((1410, 6445, 7190, None, 21176, 1854, 3992, 14577, 29175, 462, 460, 1231, 3807, 1381, 1506),
        (6.7, 2.2, 2.5, None, -7.8, 13.2, 18.3, 10.3, 11, 43.2, 13.1, 42.4, 31.7, 32.8, 43)),
 2021: ((1089, 3786, 7822, None, 19771, 3133, 10729, 26356, 48232, 690, 794, 1470, 4000, 1698, 1865),
        (7.8, -39, 4.2, None, -3, 36.3, 54.2, 42.2, 37.2, 51.9, 55.6, 47.9, 29.3, 40.6, 47.8)),
 2022: ((1026, 3857, 8004, 11785, 20791, 3545, 12562, 36401, 64299, 993, 1114, 1556, 4371, 1559, 2243),
        (3.8, -33.2, -0.1, 0.3, 1.9, 36.1, 48.9, 50.7, 45.3, 65.8, 59.5, 14.1, 19, 35.2, 50.9)),
 2023: ((1049, 5739, 8464, 16496, 25097, 2477, 5162, 19210, 33653, 974, 1511, 1715, 3844, 1362, 2388),
        (1.8, 2.7, 3.2, 1.3, 3.1, 11.9, -8.2, 14.1, 6.6, 59.6, 31, 21.3, 25.5, 31.2, 50.7)),
 2024: ((1018, 7292, 8413, 17280, 23480, 2810, 8427, 20287, 37388, 1014, 2084, 2312, 4465, 1489, 2740),
        (5.2, 2.2, 2, 5.6, 2.3, 17.8, 42.1, 13.4, 12.7, 53.3, 22.2, 27.4, 29.8, 37.8, 54))}

FISCAL_YEARS: tuple[int, ...] = (2020, 2021, 2022, 2023, 2024)
REVENUE_VALUES_BY_YEAR = {year: rows[0] for year, rows in SOURCE_XLSB_ROWS_BY_YEAR.items()}
EBIT_MARGIN_VALUES_BY_YEAR = {year: rows[1] for year, rows in SOURCE_XLSB_ROWS_BY_YEAR.items()}

# Source chart-part styling values common to slide34_chart19.xml ... slide34_chart23.xml.
SOURCE_PLOT_LAYOUT = {
    "x": 0.0073291050035236083,
    "y": 0.11816838995568685,
    "w": 0.96053558844256515,
    "h": 0.76218611521418023,
}
SOURCE_REVENUE_AXIS_MIN = 0
SOURCE_REVENUE_AXIS_MAX = 80000
SOURCE_REVENUE_AXIS_MAJOR_UNIT = 20000
SOURCE_EBIT_AXIS_MIN = -50
SOURCE_EBIT_AXIS_MAX = 100
SOURCE_GAP_WIDTH = 80
SOURCE_BAR_OVERLAP = 100
SOURCE_AXIS_LINE_WIDTH = 9_525
SOURCE_EBIT_MARKER_LINE_WIDTH = 9_525
EBIT_MARKER_WIDTH_IN = 0.120

# Bar-series dPt color overrides in the source chart part: first five points use
# the series default red, then owner/operator blue, charter-company green, and
# terminal-operator blue.
REVENUE_POINT_COLORS: tuple[str, ...] = (
    SHIPBUILDER_RED,
    SHIPBUILDER_RED,
    SHIPBUILDER_RED,
    SHIPBUILDER_RED,
    SHIPBUILDER_RED,
    OWNER_OPERATOR_BLUE,
    OWNER_OPERATOR_BLUE,
    OWNER_OPERATOR_BLUE,
    OWNER_OPERATOR_BLUE,
    CHARTER_GREEN,
    CHARTER_GREEN,
    CHARTER_GREEN,
    TERMINAL_BLUE,
    TERMINAL_BLUE,
    TERMINAL_BLUE,
)


def _native_panel_chart_style(year: int) -> dict:
    """Return one editable revenue-bar chart spec for a small-multiple panel."""

    return {
        "mode": "stacked",
        "categories": list(COMPANY_CATEGORIES),
        "series": [
            {
                "name": f"{year} Revenue ($M)",
                "color": SHIPBUILDER_RED,
                "values": list(REVENUE_VALUES_BY_YEAR[year]),
                "data_point_colors": list(REVENUE_POINT_COLORS),
                "hide_labels": True,
            }
        ],
        "show_legend": False,
        "show_cat_labels": False,
        "show_value_axis_labels": False,
        "show_gridlines": False,
        "show_value_labels": False,
        "value_axis_format": '#,##0;"-"#,##0',
        "cat_label_size_pt": 8,
        "gap_width": SOURCE_GAP_WIDTH,
        "bar_overlap": SOURCE_BAR_OVERLAP,
        "seg_line_color": None,
        "axis_line_color": BLACK,
        "axis_line_width": SOURCE_AXIS_LINE_WIDTH,
        "value_axis_min": SOURCE_REVENUE_AXIS_MIN,
        "value_axis_max": SOURCE_REVENUE_AXIS_MAX,
        "value_axis_major_unit": SOURCE_REVENUE_AXIS_MAJOR_UNIT,
        "plot_layout": dict(SOURCE_PLOT_LAYOUT),
        "cat_header": "Company",
    }


CHART_STYLES_BY_YEAR = {year: _native_panel_chart_style(year) for year in FISCAL_YEARS}
CHARTS = [column_chart(**CHART_STYLES_BY_YEAR[year]) for year in FISCAL_YEARS]

# Readable data mirrors for agents/tools that expect the converter's _CHARTn_DATA
# shape. CHARTS consumes the revenue row; the EBIT row is rendered manually by
# paint_ebit_margin_markers().
_CHART0_DATA = {"categories": COMPANY_CATEGORIES, "series": [{"name": "2020 Revenue", "values": list(REVENUE_VALUES_BY_YEAR[2020])}, {"name": "2020 EBIT Margin", "values": list(EBIT_MARGIN_VALUES_BY_YEAR[2020])}]}
_CHART1_DATA = {"categories": COMPANY_CATEGORIES, "series": [{"name": "2021 Revenue", "values": list(REVENUE_VALUES_BY_YEAR[2021])}, {"name": "2021 EBIT Margin", "values": list(EBIT_MARGIN_VALUES_BY_YEAR[2021])}]}
_CHART2_DATA = {"categories": COMPANY_CATEGORIES, "series": [{"name": "2022 Revenue", "values": list(REVENUE_VALUES_BY_YEAR[2022])}, {"name": "2022 EBIT Margin", "values": list(EBIT_MARGIN_VALUES_BY_YEAR[2022])}]}
_CHART3_DATA = {"categories": COMPANY_CATEGORIES, "series": [{"name": "2023 Revenue", "values": list(REVENUE_VALUES_BY_YEAR[2023])}, {"name": "2023 EBIT Margin", "values": list(EBIT_MARGIN_VALUES_BY_YEAR[2023])}]}
_CHART4_DATA = {"categories": COMPANY_CATEGORIES, "series": [{"name": "2024 Revenue", "values": list(REVENUE_VALUES_BY_YEAR[2024])}, {"name": "2024 EBIT Margin", "values": list(EBIT_MARGIN_VALUES_BY_YEAR[2024])}]}


TEACHING_METADATA = {
    "role": "archetype_comparison / margin_profile_small_multiples",
    "use_when": (
        "Use for repeated company-comparison panels where revenue magnitude and "
        "EBIT-margin profile must both be visible, with manual labels carrying "
        "the analytical readout."
    ),
    "teaches": [
        "native revenue column charts",
        "manual secondary-axis EBIT markers",
        "small-multiple chart alignment",
        "manual value-axis ticks",
        "manual company labels",
        "manual data labels and revenue chips",
        "archetype band headers and dividers",
    ],
    "source_module": "archetype_comps_shipbuilder_margins.py",
    "rebuild_strategy": "replace five styled_chart combo templates with native column_chart panels plus manual EBIT markers",
}

TEXT_FIT = {
    "margin_point_labels": {
        "box_in": "0.193-0.292 wide x 0.134 high",
        "font_pt": 8,
        "content": "rounded EBIT margin percent label",
        "note": "Negative values need the wider 0.292in label box.",
    },
    "revenue_chips": {
        "box_in": "0.094-0.156 wide x 0.134 high",
        "font_pt": 8,
        "content": "revenue in $B, one or two digits only",
    },
    "company_labels": {
        "box_in": "single-line 0.134 high; wrapped names 0.267 high",
        "font_pt": 8,
        "content": "15 company names registered to chart category centers",
    },
}


@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU only at the primitive boundary."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class ChartPanel:
    year: int
    r_id: str
    box: Box

    @property
    def plot_x(self) -> float:
        return self.box.x + self.box.w * SOURCE_PLOT_LAYOUT["x"]

    @property
    def plot_y(self) -> float:
        return self.box.y + self.box.h * SOURCE_PLOT_LAYOUT["y"]

    @property
    def plot_w(self) -> float:
        return self.box.w * SOURCE_PLOT_LAYOUT["w"]

    @property
    def plot_h(self) -> float:
        return self.box.h * SOURCE_PLOT_LAYOUT["h"]


CHART_PANELS: tuple[ChartPanel, ...] = (
    ChartPanel(2020, "rId2", Box(0.849, 5.410, 12.318, 1.175)),
    ChartPanel(2021, "rId3", Box(0.849, 4.378, 12.318, 1.175)),
    ChartPanel(2022, "rId4", Box(0.849, 3.347, 12.318, 1.175)),
    ChartPanel(2023, "rId5", Box(0.849, 2.316, 12.318, 1.175)),
    ChartPanel(2024, "rId6", Box(0.849, 1.285, 12.318, 1.175)),
)


class ShapeIds:
    """Tiny id allocator; keeps the body loops readable."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


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


# ════════════════════════════════════════════════════════════════════════════
# Drawing helpers.
# ════════════════════════════════════════════════════════════════════════════
def _p(text: str, *, size_pt: int = 8, color: str = BLACK, bold: bool = False, italic: bool = False, align: str | None = "ctr") -> str:
    return paragraph(
        [run(text, size=PT(size_pt), color=color, bold=bold or None, italic=italic or None, font=FONT)],
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100_000,
    )


def _ebit_marker_y(panel: ChartPanel, value: float | int) -> float:
    scale = SOURCE_EBIT_AXIS_MAX - SOURCE_EBIT_AXIS_MIN
    return panel.plot_y + panel.plot_h * ((SOURCE_EBIT_AXIS_MAX - float(value)) / scale)


def _category_center_x(panel: ChartPanel, idx: int) -> float:
    return panel.plot_x + panel.plot_w * ((idx + 0.5) / len(COMPANY_CATEGORIES))


def paint_chrome(out: list[str], ids: ShapeIds) -> None:
    out.append("")
    out.append("")
    out.append(
        text_box(
            ids.next(),
            "Rectangle 1964",
            IN(0.495),
            IN(7.006),
            IN(5.102),
            IN(0.349),
            [paragraph([run("Source: Company filings", size=PT(8), color=BLACK, font=FONT)], line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )


def paint_chart_frames(out: list[str], ids: ShapeIds) -> None:
    for panel in CHART_PANELS:
        out.append(graphic_frame(sp_id=ids.next(), name="Chart", x=IN(panel.box.x), y=IN(panel.box.y), cx=IN(panel.box.w), cy=IN(panel.box.h), rId=panel.r_id))


def paint_panel_baselines(out: list[str], ids: ShapeIds) -> None:
    # Dashed baselines/rules copied from the source slide. The segmented 2021 and
    # 2022 baselines preserve gaps around labels and dividers.
    out.append(connector(ids.next(), "Straight Connector 2230", _GRID_X, IN(2.021), IN(11.832), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2205", _GRID_X, IN(3.052), IN(11.832), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2180", _GRID_X, IN(4.083), IN(1.024), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2484", IN(2.280), IN(4.083), IN(5.273), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2485", IN(7.733), IN(4.083), IN(5.038), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 384", _GRID_X, IN(5.115), IN(1.024), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2529", IN(2.280), IN(5.115), IN(5.273), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2530", IN(7.733), IN(5.115), IN(5.038), IN(0), color=DK, width=9525, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2528", IN(2.122), IN(5.205), IN(0), IN(0.003), color=BREADCRUMB, width=6350, dashed=True, arrow=True))
    out.append(connector(ids.next(), "Straight Connector 2020", _GRID_X, IN(6.146), IN(11.832), IN(0), color=DK, width=9525, dashed=True, arrow=True))


def paint_ebit_margin_markers(out: list[str], ids: ShapeIds) -> None:
    # The source combo chart line has no connecting stroke; every point is a
    # yellow `dash` marker on the secondary EBIT-margin axis. We draw each marker
    # explicitly so the chart can be factory-native and still preserve the source
    # EBIT values from the XLSB/XML cache.
    for panel in CHART_PANELS:
        for idx, value in enumerate(EBIT_MARGIN_VALUES_BY_YEAR[panel.year]):
            if value is None:
                continue
            x = _category_center_x(panel, idx) - EBIT_MARKER_WIDTH_IN / 2
            y = _ebit_marker_y(panel, value)
            out.append(
                connector(
                    ids.next(),
                    "EBIT margin dash marker",
                    IN(x),
                    IN(y),
                    IN(EBIT_MARKER_WIDTH_IN),
                    IN(0),
                    color=EBIT_MARKER_YELLOW,
                    width=SOURCE_EBIT_MARKER_LINE_WIDTH,
                )
            )


def paint_manual_axis_and_data_labels(out: list[str], ids: ShapeIds) -> None:
    # Shared revenue-axis ticks: 0/20/40/60/80 ($B) per panel.
    for _x, _y, _cx, _t in _VALUE_TICK_LABELS:
        out.append(text_box(ids.next(), "ValueLabel", IN(_x), IN(_y), IN(_cx), _AXIS_TICK_H, [_p(_t, size_pt=8, align="r")], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    # Shared company/category labels across the bottom.
    for _x, _cx, _t in _CATEGORY_TICK_LABELS["single_line"]:
        out.append(text_box(ids.next(), "Label", IN(_x), _COMPANY_LBL_Y, IN(_cx), _COMPANY_LBL_H, [_p(_t, size_pt=8)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    for _x, _cx, _t in _CATEGORY_TICK_LABELS["wrapped"]:
        out.append(text_box(ids.next(), "Label", IN(_x), _COMPANY_WRAP_Y, IN(_cx), _COMPANY_WRAP_H, [_p(_t, size_pt=8)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    # EBIT-margin point labels.
    for _x, _y, _cx, _t in _DATA_LABELS["margin_points"]:
        out.append(text_box(ids.next(), "Label", IN(_x), IN(_y), IN(_cx), _MARGIN_LBL_H, [_p(_t, size_pt=8)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=14288, t_ins=0, r_ins=14288, b_ins=0))

    # Revenue chips, shown in $B and filled by archetype color.
    for _x, _y, _cx, _fill, _t in _DATA_LABELS["revenue_chips"]:
        out.append(text_box(ids.next(), "ValueLabel", IN(_x), IN(_y), IN(_cx), _BAR_CHIP_H, [_p(_t, size_pt=8, color=WHITE)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=14288, t_ins=0, r_ins=14288, b_ins=0))


def paint_group_headers_and_panel_labels(out: list[str], ids: ShapeIds) -> None:
    for _x, _y, _cx, _cy, _fill, _t in _GROUP_HEADERS:
        out.append(text_box(ids.next(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [_p(_t, size_pt=10, bold=True, color=WHITE)], fill=_fill, line_color="none", anchor="ctr"))

    # The carrier segment header is split from the green charter-company tag in
    # the source, so it remains a standalone run with italic parenthetical text.
    out.append(
        text_box(
            ids.next(),
            "Rectangle 2147",
            IN(5.068),
            IN(6.822),
            IN(2.833),
            IN(0.155),
            [paragraph([run("Owner/Operator ", size=PT(10), bold=True, color=WHITE, font=FONT), run("(Carrier Segment)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100_000)],
            fill=OWNER_OPERATOR_BLUE,
            line_color="none",
            anchor="ctr",
        )
    )

    for _x, _y, _cx, _cy, _fill, _t in _PANEL_LABELS["upper_panels"]:
        out.append(text_box(ids.next(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [_p(_t, size_pt=10, bold=True, color=WHITE)], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _fill, _t in _PANEL_LABELS["lower_panels"]:
        out.append(text_box(ids.next(), "YearLabel", _YEAR_X, IN(_y), _YEAR_W, _YEAR_H, [_p(_t, size_pt=10, bold=True, color=BLACK)], fill=_fill, line_color="none", anchor="ctr"))


def paint_axis_legends_and_dividers(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(ids.next(), "Text Placeholder 25", IN(11.898), IN(1.135), IN(1.170), IN(0.134), [_p("EBIT Margin (%, lines)", size_pt=8, bold=True, align="r")], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(ids.next(), "Text Placeholder 25", IN(0.741), IN(1.135), IN(1.010), IN(0.134), [_p("Revenue ($B, bars)", size_pt=8, bold=True, align=None)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    out.append(connector(ids.next(), "Straight Arrow Connector 2596", IN(4.939), IN(1.377), IN(0), IN(5.600), color="808080", width=12700))
    out.append(connector(ids.next(), "Straight Arrow Connector 2598", IN(8.056), IN(1.377), IN(0), IN(5.600), color="808080", width=12700))
    out.append(connector(ids.next(), "Straight Arrow Connector 2602", IN(10.465), IN(1.377), IN(0), IN(5.600), color="808080", width=12700))


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order favors teaching readability: native charts and rules first,
    # then explicit EBIT markers and manual labels/chips, then headers/dividers.
    paint_chrome(out, ids)
    paint_chart_frames(out, ids)
    paint_panel_baselines(out, ids)
    paint_ebit_margin_markers(out, ids)
    paint_manual_axis_and_data_labels(out, ids)
    paint_group_headers_and_panel_labels(out, ids)
    paint_axis_legends_and_dividers(out, ids)
    out.append("")

    return "".join(out)


CHROME = Chrome(
    section="Commercial Maritime Value Chain",
    topic="Performance",
    title="Archetype Comps (3/3)",
    takeaway="Shipbuilder margin profile holds across geographies and vessel types.",
)


def render() -> str:
    return body_slide(CHROME, _body())
