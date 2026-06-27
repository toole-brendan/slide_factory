"""Teaching exemplar: archetype-comparison bubble chart with narrative rail.

ROLE
  archetype_comparison / performance_bubble_chart

USE WHEN
  A slide needs to compare performance behavior across several business
  archetypes using one style-dense bubble chart, an external archetype legend,
  and a right-hand commentary rail that explains the drivers behind the plotted
  movement.

TEACHES
  - rebuilding a source bubble chart with native `bubble_chart(...)`
  - documenting a dense native bubble-chart contract without hiding it in
    converter-era `_CHART0_DATA = [{"values": []}, ...]` noise
  - manual x-axis year ticks below a native chart
  - manual y-axis title outside the chart frame
  - mixed legend grammar: solid archetype dots, a patterned archetype dot, and
    a revenue bubble-size ring
  - dense no-fill narrative rail with bold archetype heads and hanging bullets
  - single-cell table used as a rail title band
  - compact off-house source note with colored constituent labels

TEXT-FIT PRECEDENT
  narrative_rail:
    geometry: 3.136in wide x 4.870in high
    type: Arial 10pt, black, 100% line spacing
    content: 4 archetype section heads + 7 hanging bullets
    copy_when: the chart carries the comparative evidence and the rail explains
               mechanism/timing rather than adding a second exhibit

  manual_legend:
    geometry: 2.4in wide x 1.5in high, below/right of plot area
    type: Arial 10pt, no-wrap labels
    content: 5 archetype marks plus one revenue bubble-size key
    copy_when: the native chart is too style-dense or semantically overloaded
               for a native chart legend

  source_note:
    geometry: 5.102in wide x 0.349in high
    type: Arial 7pt with colored bold archetype labels
    content: one dense constituent-company source line
    copy_when: source detail is needed but cannot occupy the house source band

SOURCE NOTE
  Teaching rewrite of the source-faithful `archetype_comps_vocc_performance.py`
  module. The provided `slide33_chart18.xml` + `slide33_chart18.xlsb` pair is
  rebuilt with native `bubble_chart(...)`; the source XML/XLSB values, point fills,
  axes, bubble scale, and plot layout are transcribed into Python constants.
  The surrounding slide contract (`LAYOUT`, `CHARTS`, `_body()`, `render()`),
  visible coordinates, legend, right rail, footnote, and chrome are preserved.

FIDELITY NOTE
  This is a practical teaching rewrite, not a byte-identical source port. It keeps
  the chart XML/workbook pair for visual fidelity and PowerPoint Edit Data support.
  The chart data is explicit in Python; the module exposes
  a semantic native-chart contract so future authors know why the chart is opaque and
  which manual labels/legend/rail belong outside the chart frame.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from deck_core.authoring import (
    IN,
    PT,
    BLACK,
    WHITE,
    DK,
    FONT,
    slide,
    run,
    paragraph,
    text_box,
    table,
    trow,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    graphic_frame,
    bubble_chart,
    edge,
    rcell,
)

LAYOUT = "slideLayout4"

# Local semantic palette. These are value-chain archetype colors, not house
# chrome colors. Keep them explicit so an authoring agent can copy the legend.
SHIPBUILDER_RED = "C30C3E"
OWNER_OPERATOR_BLUE = "364D6E"
CHARTER_GREEN = "27AE60"
TERMINAL_INTEGRATED_BLUE = "6F8DB9"
TERMINAL_STANDALONE_GRAY = "8A8F93"


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "archetype_comparison / performance_bubble_chart",
    "use_when": (
        "Use when a slide compares performance across business archetypes with "
        "a style-dense bubble chart, where marker position shows margin, bubble "
        "size shows revenue, and the right rail explains period-specific drivers."
    ),
    "teaches": [
        "native editable bubble chart",
        "opaque chart-cache contract documented in Python",
        "manual year ticks over a bubble chart",
        "manual y-axis title outside the chart frame",
        "external legend for marker color, hatch pattern, and bubble size",
        "dense narrative rail with section heads and hanging bullets",
        "single-cell table as rail header",
        "compact colored source note",
    ],
    "source_module": "archetype_comps_vocc_performance.py",
    "source_chart_assets": ("slide33_chart18.xml", "slide33_chart18.xlsb"),
    "rebuild_strategy": "rebuild source bubble chart with native bubble_chart",
}

TEXT_FIT = {
    "narrative_rail": {
        "box_in": (3.136, 4.870),
        "font_pt": 10,
        "content": "4 heads + 7 bullets with bold time-period labels",
        "note": "Works because prose is sentence-fragment style, not full paragraphs.",
    },
    "rail_header": {
        "box_in": (3.135, 0.300),
        "font_pt": 10,
        "content": "Revenue and EBIT margin drivers",
        "note": "Single-cell table gives exact top/bottom rule behavior.",
    },
    "manual_year_ticks": {
        "box_in": (0.306, 0.167),
        "font_pt": 10,
        "content": "four-digit year tick; five ticks only",
    },
    "legend_labels": {
        "box_in": "0.760-2.139 wide x 0.167 high",
        "font_pt": 10,
        "content": "no-wrap archetype captions",
    },
    "source_note": {
        "box_in": (5.102, 0.349),
        "font_pt": 7,
        "content": "one dense constituent-company source line",
    },
}

COPY_RULES = [
    "Keep a bubble chart native when the important precedent is marker size + per-point styling; do not force it into a line or column factory.",
    "Use the slide-level legend as the semantic contract when the native chart groups points by internal cache buckets instead of clean archetype series.",
    "Use a right commentary rail when the chart explains what happened and the rail explains why it happened.",
    "Do not place long narrative inside the chart area; reserve the plot for markers, axis ticks, and a compact legend.",
    "A colored source note can carry constituent detail when a full appendix table would overtake the slide.",
]

CHART_TEMPLATE_CONTRACT = {
    "why_native_bubble_chart": (
        "The chart is a native bubbleChart with seven source series buckets, many "
        "per-point styles, and revenue-scaled marker sizes. The chart data is "
        "explicit in Python and bubble_chart() generates the workbook."
    ),
    "visible_encoding": {
        "x": "calendar year, 2020-2024",
        "y": "EBIT margin (%)",
        "bubble_size": "revenue, with $10B shown by the external ring key",
        "marker_color": "value-chain archetype",
    },
    "template_chart_xml": {
        "chart_type": "bubbleChart",
        "internal_series_count": 7,
        "point_count": 73,
        "bubble_scale": 66,
        "x_axis_min_max": (2019, 2025),
        "y_axis_min_max": (-50, 70),
    },
    "manual_shapes": (
        "year ticks, EBIT Margin y-axis title, archetype legend, revenue ring key, "
        "right narrative rail, rail header, source note, and preliminary chip"
    ),
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records.
# ════════════════════════════════════════════════════════════════════════════
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
class BubbleTemplateSeries:
    """One internal series bucket in the preserved bubble-native chart.

    These buckets are a source-chart implementation detail, not the external
    legend. Some archetype colors are applied through per-point overrides in the
    chart XML, so the external legend remains the semantic source for authors.
    """

    order: int
    point_count: int
    default_style: str
    cache_columns: str
    note: str

@dataclass(frozen=True)
class NativeBubbleSeries:
    """One native bubble-chart series with sparse source-indexed points."""

    name: str
    default_fill: Optional[str]
    default_pattern: Optional[dict]
    x_values: tuple[Optional[float], ...]
    y_values: tuple[Optional[float], ...]
    bubble_sizes: tuple[Optional[float], ...]
    point_fills: tuple[Optional[str], ...]

    @property
    def point_count(self) -> int:
        return sum(value is not None for value in self.x_values)

    def chart_dict(self) -> dict:
        out = {
            "name": self.name,
            "x_values": list(self.x_values),
            "y_values": list(self.y_values),
            "bubble_sizes": list(self.bubble_sizes),
        }
        if self.default_pattern is not None:
            out["pattern"] = dict(self.default_pattern)
        elif self.default_fill is not None:
            out["color"] = self.default_fill
        if any(fill is not None for fill in self.point_fills):
            out["data_point_colors"] = list(self.point_fills)
        return out


@dataclass(frozen=True)
class YearTick:
    """Manual x-axis tick under the native chart."""

    box: Box
    label: str


@dataclass(frozen=True)
class LegendEntry:
    """One external legend entry beside/below the plot area."""

    label: str
    marker: str
    marker_box: Box
    label_box: Box
    fill: Optional[str]
    line_color: str = DK
    pattern_fill: Optional[dict] = None


@dataclass(frozen=True)
class NarrativeBullet:
    """One hanging bullet in the commentary rail."""

    prefix: Optional[str]
    text: str


@dataclass(frozen=True)
class NarrativeSection:
    """Section head plus bullets for the right rail."""

    title: str
    qualifier: Optional[str]
    bullets: tuple[NarrativeBullet, ...]


@dataclass(frozen=True)
class SourceRun:
    """A run in the compact colored source note."""

    text: str
    color: str = BLACK
    bold: bool = False


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.373, 1.696, 9.286, 5.200)
Y_AXIS_TITLE = Box(0.533, 1.505, 1.064, 0.167)
YEAR_TICK_Y = 6.736
YEAR_TICK_SIZE = (0.306, 0.167)
LEGEND_LABEL_H = 0.167
NARRATIVE_RAIL = Box(9.660, 1.866, 3.136, 4.870)
NARRATIVE_HEADER = Box(9.660, 1.563, 3.135, 0.300)
SOURCE_NOTE = Box(0.495, 7.081, 5.102, 0.349)


# ════════════════════════════════════════════════════════════════════════════
# Native bubble-chart data and factory spec transcribed from the source chart XML.
# No source XML/XLSB files are read at runtime; bubble_chart() builds the editable
# embedded workbook directly from these Python constants.
# ════════════════════════════════════════════════════════════════════════════
BUBBLE_POINT_COUNT = 73

BUBBLE_TEMPLATE_SERIES: tuple[BubbleTemplateSeries, ...] = (
    BubbleTemplateSeries(0, 3, f"solid {SHIPBUILDER_RED}", "A / B / C", "native bucket with red default marker"),
    BubbleTemplateSeries(1, 12, f"solid {OWNER_OPERATOR_BLUE}", "A / D / E", "native bucket with owner/operator default marker and red point overrides"),
    BubbleTemplateSeries(2, 20, f"solid {CHARTER_GREEN}", "A / F / G", "native bucket with charter default marker and multiple point overrides"),
    BubbleTemplateSeries(3, 15, f"solid {OWNER_OPERATOR_BLUE}", "A / H / I", "native bucket with per-point overrides"),
    BubbleTemplateSeries(4, 14, "pct50 hatch", "A / J / K", "native bucket for standalone terminal-operator hatch behavior"),
    BubbleTemplateSeries(5, 6, f"solid {SHIPBUILDER_RED}", "A / L / M", "native bucket with per-point overrides"),
    BubbleTemplateSeries(6, 3, f"solid {SHIPBUILDER_RED}", "A / N / O", "native bucket with per-point overrides"),
)


def _sparse_values(points: dict[int, float]) -> tuple[Optional[float], ...]:
    values: list[Optional[float]] = [None] * BUBBLE_POINT_COUNT
    for idx, value in points.items():
        values[idx] = value
    return tuple(values)


def _sparse_fills(points: dict[int, str]) -> tuple[Optional[str], ...]:
    fills: list[Optional[str]] = [None] * BUBBLE_POINT_COUNT
    for idx, value in points.items():
        fills[idx] = value
    return tuple(fills)


NATIVE_BUBBLE_SERIES: tuple[NativeBubbleSeries, ...] = (
    NativeBubbleSeries(
        name="Source bucket 1",
        default_fill='C30C3E',
        default_pattern=None,
        x_values=_sparse_values({0: 2021, 1: 2022, 2: 2022}),
        y_values=_sparse_values({0: -2.9787234042553195, 1: -33.20027982387556, 2: 1.9083969465648851}),
        bubble_sizes=_sparse_values({0: 19771.325688420737, 1: 3856.7506229268834, 2: 20790.68069640845}),
        point_fills=_sparse_fills({}),
    ),
    NativeBubbleSeries(
        name="Source bucket 2",
        default_fill='364D6E',
        default_pattern=None,
        x_values=_sparse_values({3: 2020,
 4: 2021,
 5: 2021,
 6: 2022,
 7: 2020,
 8: 2021,
 9: 2021,
 10: 2022,
 11: 2023,
 12: 2023,
 13: 2024,
 14: 2024}),
        y_values=_sparse_values({3: -7.826086956521738,
 4: -38.99333333333333,
 5: 4.1817392562581395,
 6: 0.3434112180997913,
 7: 10.954584404455868,
 8: 54.245502842762605,
 9: 37.24290927185272,
 10: 45.33351996143019,
 11: -8.174809189880284,
 12: 6.617537812379283,
 13: 42.112632603175356,
 14: 12.68588852038087}),
        bubble_sizes=_sparse_values({3: 21176.49225216599,
 4: 3785.9985360805663,
 5: 7821.8697999999995,
 6: 11784.824390166483,
 7: 29175,
 8: 10729,
 9: 48232,
 10: 64299,
 11: 5162.2,
 12: 33653,
 13: 8427.4,
 14: 37388}),
        point_fills=_sparse_fills({3: 'C30C3E', 4: 'C30C3E', 5: 'C30C3E', 6: 'C30C3E'}),
    ),
    NativeBubbleSeries(
        name="Source bucket 3",
        default_fill='27AE60',
        default_pattern=None,
        x_values=_sparse_values({15: 2021,
 16: 2022,
 17: 2023,
 18: 2024,
 19: 2020,
 20: 2020,
 21: 2021,
 22: 2022,
 23: 2022,
 24: 2023,
 25: 2024,
 26: 2021,
 27: 2021,
 28: 2022,
 29: 2022,
 30: 2022,
 31: 2023,
 32: 2023,
 33: 2023,
 34: 2024}),
        y_values=_sparse_values({15: 7.840197254431562,
 16: -0.13365410318096765,
 17: 3.0864197530864197,
 18: 2.3054755043227666,
 19: 18.261523046092183,
 20: 10.297043287370515,
 21: 42.15738351798452,
 22: 36.14512215764826,
 23: 50.73212274388066,
 24: 14.143675169182718,
 25: 13.392813131562084,
 26: 51.92159420289856,
 27: 55.61092637836599,
 28: 65.80422960725076,
 29: 59.455101588262075,
 30: 14.103882746207253,
 31: 59.61611909650924,
 32: 30.965074903765107,
 33: 21.258235671389425,
 34: 22.182558229929164}),
        bubble_sizes=_sparse_values({15: 1089.4355999999998,
 16: 8004.243600000001,
 17: 25097.40737584917,
 18: 23479.89660725644,
 19: 3992,
 20: 14577,
 21: 26356,
 22: 3544.6,
 23: 36401,
 24: 19210,
 25: 20287,
 26: 690,
 27: 793.639,
 28: 993,
 29: 1113.859,
 30: 1555.6,
 31: 974,
 32: 1511.406,
 33: 1715.1,
 34: 2083.894}),
        point_fills=_sparse_fills({15: 'C30C3E',
 16: 'C30C3E',
 17: 'C30C3E',
 18: 'C30C3E',
 19: '364D6E',
 20: '364D6E',
 21: '364D6E',
 22: '364D6E',
 23: '364D6E',
 24: '364D6E',
 25: '364D6E'}),
    ),
    NativeBubbleSeries(
        name="Source bucket 4",
        default_fill='364D6E',
        default_pattern=None,
        x_values=_sparse_values({35: 2020,
 36: 2022,
 37: 2023,
 38: 2024,
 39: 2020,
 40: 2021,
 41: 2022,
 42: 2023,
 43: 2024,
 44: 2020,
 45: 2020,
 46: 2021,
 47: 2022,
 48: 2023,
 49: 2024}),
        y_values=_sparse_values({35: 2.517434937914611,
 36: 3.845388188453882,
 37: 1.324192336589031,
 38: 5.615161719790116,
 39: 13.204595717136847,
 40: 36.315755873340144,
 41: 48.91892752515603,
 42: 11.90149374243036,
 43: 17.827526070398974,
 44: 13.105694094747339,
 45: 31.652219595482006,
 46: 29.325000000000003,
 47: 19.03454587051018,
 48: 25.494276795005206,
 49: 29.764837625979844}),
        bubble_sizes=_sparse_values({35: 7190.017000000001,
 36: 1025.5135,
 37: 16496.1230702495,
 38: 17280.39191804366,
 39: 1853.9,
 40: 3132.8,
 41: 12561.6,
 42: 2477,
 43: 2809.7,
 44: 460.319,
 45: 3807,
 46: 4000,
 47: 4371,
 48: 3844,
 49: 4465}),
        point_fills=_sparse_fills({35: 'C30C3E',
 36: 'C30C3E',
 37: 'C30C3E',
 38: 'C30C3E',
 44: '27AE60',
 45: '6F8DB9',
 46: '6F8DB9',
 47: '6F8DB9',
 48: '6F8DB9',
 49: '6F8DB9'}),
    ),
    NativeBubbleSeries(
        name="Source bucket 5",
        default_fill=None,
        default_pattern={'bg': 'scheme:bg1', 'fg': 'scheme:tx1', 'prst': 'pct50'},
        x_values=_sparse_values({50: 2020,
 51: 2023,
 52: 2024,
 53: 2024,
 54: 2020,
 55: 2020,
 56: 2021,
 57: 2021,
 58: 2022,
 59: 2022,
 60: 2023,
 61: 2023,
 62: 2024,
 63: 2024}),
        y_values=_sparse_values({50: 2.1914285714285713,
 51: 3.2152659783034894,
 52: 1.9931102362204725,
 53: 27.35885788449059,
 54: 32.75701021875992,
 55: 42.955828628362674,
 56: 40.61280117184256,
 57: 47.833780160857906,
 58: 35.1868290838553,
 59: 50.92657155595185,
 60: 31.215682587438888,
 61: 50.728753109918834,
 62: 37.84991786980203,
 63: 53.95908194270246}),
        bubble_sizes=_sparse_values({50: 6445.019381093996,
 51: 8463.5362,
 52: 8413.2928,
 53: 2311.5,
 54: 1380.7877834240462,
 55: 1505.5,
 56: 1698.04861787784,
 57: 1865,
 58: 1559.4693328206115,
 59: 2243,
 60: 1361.686873471687,
 61: 2388.326,
 62: 1489.1151821002356,
 63: 2739.524}),
        point_fills=_sparse_fills({50: 'C30C3E', 51: 'C30C3E', 52: 'C30C3E', 53: '27AE60'}),
    ),
    NativeBubbleSeries(
        name="Source bucket 6",
        default_fill='C30C3E',
        default_pattern=None,
        x_values=_sparse_values({64: 2020, 65: 2023, 66: 2024, 67: 2020, 68: 2021, 69: 2024}),
        y_values=_sparse_values({64: 6.697282816685799,
 65: 2.6524303821389523,
 66: 2.206755753526355,
 67: 42.43581410464738,
 68: 47.85417941916616,
 69: 53.34161735700197}),
        bubble_sizes=_sparse_values({64: 1410.0531899999999,
 65: 5738.553180941462,
 66: 7291.6243757866105,
 67: 1230.8,
 68: 1470.3,
 69: 1014}),
        point_fills=_sparse_fills({67: '27AE60', 68: '27AE60', 69: '27AE60'}),
    ),
    NativeBubbleSeries(
        name="Source bucket 7",
        default_fill='C30C3E',
        default_pattern=None,
        x_values=_sparse_values({70: 2023, 71: 2024, 72: 2020}),
        y_values=_sparse_values({70: 1.7566688353936235, 71: 5.16068282607375, 72: 43.17748917748918}),
        bubble_sizes=_sparse_values({70: 1049.4636, 71: 1018.11285, 72: 462}),
        point_fills=_sparse_fills({72: '27AE60'}),
    ),
)

SOURCE_CHART_AUDIT = {
    "source_xml": "slide33_chart18.xml",
    "chart_type": "bubbleChart",
    "internal_series_count": 7,
    "point_count": BUBBLE_POINT_COUNT,
    "bubble_scale": 66,
    "x_axis_min_max": (2019, 2025),
    "y_axis_min_max": (-50, 70),
    "plot_layout": {'h': 0.9275459098497496,
 'w': 0.9414843896055337,
 'x': 0.04879416713404375,
 'y': 0.032721202003338896},
}

CHART_STYLE = {
    "series": [series.chart_dict() for series in NATIVE_BUBBLE_SERIES],
    "show_legend": False,
    "x_axis_format": "General",
    "y_axis_format": "#,##0;\"-\"#,##0",
    "bubble_size_format": "General",
    "x_axis_min": 2019,
    "x_axis_max": 2025,
    "x_axis_major_unit": 1,
    "y_axis_min": -50,
    "y_axis_max": 70,
    "y_axis_major_unit": 10,
    "show_x_axis_labels": False,
    "show_y_axis_labels": True,
    "x_axis_crosses_at": 0,
    "y_axis_crosses": "min",
    "bubble_scale": 66,
    "show_negative_bubbles": False,
    "show_gridlines": False,
    "axis_line_color": "scheme:tx1",
    "axis_line_width": 9_525,
    "axis_label_size_pt": 10,
    "axis_label_color": BLACK,
    "bubble_line_color": "scheme:tx1",
    "bubble_line_width": 3_175,
    "plot_layout": dict(SOURCE_CHART_AUDIT["plot_layout"]),
}

CHARTS = [bubble_chart(**CHART_STYLE)]

_CHART0_DATA = {
    "categories": None,
    "series": [series.chart_dict() for series in NATIVE_BUBBLE_SERIES],
}


# ════════════════════════════════════════════════════════════════════════════
# Manual labels and legend entries copied from source slide coordinates.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, *YEAR_TICK_SIZE), label)
    for x, label in (
        (2.130, "2020"),
        (3.589, "2021"),
        (5.045, "2022"),
        (6.502, "2023"),
        (7.960, "2024"),
    )
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Shipbuilders",
        "solid_archetype_dot",
        Box(7.148, 5.583, 0.146, 0.146),
        Box(7.375, 5.578, 0.760, LEGEND_LABEL_H),
        SHIPBUILDER_RED,
    ),
    LegendEntry(
        "Owner/Operator (Carrier Segment)",
        "solid_archetype_dot",
        Box(7.148, 5.806, 0.146, 0.146),
        Box(7.375, 5.800, 2.139, LEGEND_LABEL_H),
        OWNER_OPERATOR_BLUE,
    ),
    LegendEntry(
        "Charter Companies",
        "solid_archetype_dot",
        Box(7.148, 6.028, 0.146, 0.146),
        Box(7.375, 6.023, 1.200, LEGEND_LABEL_H),
        CHARTER_GREEN,
    ),
    LegendEntry(
        "Terminal Operators (Integrated)",
        "solid_archetype_dot",
        Box(7.148, 6.250, 0.146, 0.146),
        Box(7.375, 6.245, 1.944, LEGEND_LABEL_H),
        TERMINAL_INTEGRATED_BLUE,
    ),
    LegendEntry(
        "Terminal Operators (Standalone)",
        "hatched_archetype_dot",
        Box(7.148, 6.472, 0.146, 0.146),
        Box(7.375, 6.467, 2.021, LEGEND_LABEL_H),
        None,
        pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"},
    ),
    LegendEntry(
        "$10B (Revenue)",
        "revenue_bubble_ring",
        Box(7.066, 5.139, 0.326, 0.326),
        Box(7.450, 5.224, 1.005, LEGEND_LABEL_H),
        None,
    ),
)

NARRATIVE_SECTIONS: tuple[NarrativeSection, ...] = (
    NarrativeSection(
        "Shipbuilders",
        "(relating to Commercial market)",
        (
            NarrativeBullet("’21-’22:", "While orders recovered from ’20, earnings remained pressured by input materials and labor cost growth."),
            NarrativeBullet("’23-’24:", "Improvement driven by performance against orderbook contracts and rising new build prices"),
        ),
    ),
    NarrativeSection(
        "Owner/Operators",
        None,
        (
            NarrativeBullet("’21-’22:", "Freight rates reached historic highs driven by post-COVID pent-up demand and shift toward goods consumption, while port congestion and operational disruptions constrained effective vessel supply amid below-trend capacity additions."),
            NarrativeBullet("’23-’24:", "Freight rates normalized as consumer demand softened under inflationary pressure, coinciding with acceleration in new vessel deliveries that expanded global fleet capacity."),
        ),
    ),
    NarrativeSection(
        "Charter Companies",
        None,
        (
            NarrativeBullet("’21-’22:", "Charter rates surged alongside freight rates as operators sought to secure tonnage in supply-constrained market."),
            NarrativeBullet("’23-’24:", "Earnings remained supported by multi-year charter contracts signed at peak market conditions ’21-’22, partially insulating results from lower charter rates."),
        ),
    ),
    NarrativeSection(
        "Terminal Operators",
        None,
        (
            NarrativeBullet(None, "Relatively more stable margins given ability to pass on costs to operators."),
        ),
    ),
)

SOURCE_RUNS: tuple[SourceRun, ...] = (
    SourceRun("Source: Company filings |   "),
    SourceRun("Shipbuilders:", SHIPBUILDER_RED, True),
    SourceRun(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. "),
    SourceRun("Owner/Operator", OWNER_OPERATOR_BLUE, True),
    SourceRun(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. "),
    SourceRun("Charter Companies", CHARTER_GREEN, True),
    SourceRun(": Danaos, "),
    SourceRun("Costamare"),
    SourceRun(", Seaspan. "),
    SourceRun("Terminal Operators (Integrated)", TERMINAL_INTEGRATED_BLUE, True),
    SourceRun(": Maersk Terminals.         "),
    SourceRun("Terminal Operators (Standalone)", TERMINAL_STANDALONE_GRAY, True),
    SourceRun(": Hutchison Ports, ICTS. Note: Segment margins not burdened by corporate"),
)



# ════════════════════════════════════════════════════════════════════════════
# Validation helpers. These keep the manual teaching contract synchronized with
# the native bubble chart and the surrounding slide furniture.
# ════════════════════════════════════════════════════════════════════════════
def _validate_semantics() -> None:
    expected_series = CHART_TEMPLATE_CONTRACT["template_chart_xml"]["internal_series_count"]
    expected_points = CHART_TEMPLATE_CONTRACT["template_chart_xml"]["point_count"]
    if len(BUBBLE_TEMPLATE_SERIES) != expected_series:
        raise ValueError("Bubble chart contract expects seven internal series buckets.")
    if len(NATIVE_BUBBLE_SERIES) != expected_series:
        raise ValueError("Native bubble chart must carry seven source series buckets.")
    if sum(series.point_count for series in NATIVE_BUBBLE_SERIES) != expected_points:
        raise ValueError("Bubble chart point-count contract should total 73 source workbook rows.")
    if CHART_STYLE["bubble_scale"] != 66:
        raise ValueError("Native bubble chart should keep the source bubble scale of 66.")
    if CHART_STYLE["x_axis_min"] != 2019 or CHART_STYLE["x_axis_max"] != 2025:
        raise ValueError("Native bubble chart x-axis bounds must match the source chart.")
    if CHART_STYLE["y_axis_min"] != -50 or CHART_STYLE["y_axis_max"] != 70:
        raise ValueError("Native bubble chart y-axis bounds must match the source chart.")
    if tuple(tick.label for tick in YEAR_TICKS) != ("2020", "2021", "2022", "2023", "2024"):
        raise ValueError("Manual year ticks should remain the five source years.")
    if len(LEGEND_ENTRIES) != 6:
        raise ValueError("Legend should include five archetype markers plus one revenue-size ring.")
    if next(entry for entry in LEGEND_ENTRIES if entry.marker == "hatched_archetype_dot").pattern_fill is None:
        raise ValueError("Standalone terminal-operator legend entry must keep the pct50 hatch fill.")


_validate_semantics()


# ════════════════════════════════════════════════════════════════════════════
# Tiny local authoring helpers.
# ════════════════════════════════════════════════════════════════════════════
def _textbox(sp_id: int, name: str, box: Box, paras: list[str], **kwargs) -> str:
    return text_box(sp_id, name, *box.emu(), paras, **kwargs)


def _one_line(
    text: str,
    *,
    size: int = PT(10),
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
    align: Optional[str] = None,
) -> str:
    return paragraph(
        [run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100000,
    )


def _empty_centered_paragraph() -> str:
    return paragraph([], align="ctr", line_spacing=100000)


def _narrative_head(section: NarrativeSection) -> str:
    runs = [run(section.title, size=PT(10), bold=True, color=BLACK, font=FONT)]
    if section.qualifier:
        runs.append(run(" ", size=PT(10), color=BLACK, font=FONT))
        runs.append(run(section.qualifier, size=PT(10), italic=True, color=BLACK, font=FONT))
    return paragraph(runs, line_spacing=100000)


def _narrative_bullet(bullet: NarrativeBullet) -> str:
    runs = []
    if bullet.prefix:
        runs.append(run(bullet.prefix, size=PT(10), bold=True, color=BLACK, font=FONT))
        runs.append(run(" ", size=PT(10), color=BLACK, font=FONT))
    runs.append(run(bullet.text, size=PT(10), color=BLACK, font=FONT))
    return paragraph(runs, mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)


def _narrative_paragraphs() -> list[str]:
    paras: list[str] = []
    for section in NARRATIVE_SECTIONS:
        paras.append(_narrative_head(section))
        paras.extend(_narrative_bullet(bullet) for bullet in section.bullets)
    return paras


def _source_paragraph() -> str:
    return paragraph(
        [
            run(src.text, size=PT(7), bold=src.bold or None, color=src.color, font=FONT)
            for src in SOURCE_RUNS
        ],
        line_spacing=100000,
    )


# ════════════════════════════════════════════════════════════════════════════
# Paint functions. Order follows the source's effective stacking: chrome,
# native bubble chart, manual axis furniture, legend, right rail, source note,
# and the Preliminary chip.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(next_id) -> list[str]:
    """House chrome for the value-chain performance section."""

    return [
        breadcrumb("Commercial Maritime Value Chain", "Performance"),
        title_placeholder(
            "Archetype Comps (2/3)",
            "VOCC performance ’21-’22 driven by historically high freight rates; charter companies benefitted through ’24 from leases locked in ’21-’22.",
        ),
    ]


def paint_native_bubble_chart(next_id) -> list[str]:
    """Opaque but editable bubble chart: position = margin, size = revenue."""

    x, y, w, h = CHART_FRAME.emu()
    return [
        graphic_frame(
            sp_id=next_id(),
            name="Chart",
            x=x,
            y=y,
            cx=w,
            cy=h,
            rId="rId2",
        )
    ]


def paint_manual_axis_labels(next_id) -> list[str]:
    """Five manual year ticks plus the outside y-axis title."""

    shapes: list[str] = []
    for tick in YEAR_TICKS:
        shapes.append(
            _textbox(
                next_id(),
                "YearLabel",
                tick.box,
                [_one_line(tick.label, align="ctr")],
                fill=None,
                line_color="none",
                wrap="none",
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )
    shapes.append(
        _textbox(
            next_id(),
            "YAxisTitle",
            Y_AXIS_TITLE,
            [_one_line("EBIT Margin (%)", bold=True)],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        )
    )
    return shapes


def paint_legend(next_id) -> list[str]:
    """External legend: archetype markers plus revenue bubble-size ring."""

    shapes: list[str] = []
    # Paint the revenue-size ring with the solid dots, matching the source order.
    for entry in LEGEND_ENTRIES:
        if entry.marker == "hatched_archetype_dot":
            continue
        shapes.append(
            _textbox(
                next_id(),
                "LegendMarker",
                entry.marker_box,
                [_empty_centered_paragraph()],
                fill=entry.fill,
                line_color=entry.line_color,
                line_width=3175,
                prst="ellipse",
                anchor="ctr",
            )
        )

    hatched = next(entry for entry in LEGEND_ENTRIES if entry.marker == "hatched_archetype_dot")
    shapes.append(
        _textbox(
            next_id(),
            "LegendMarkerHatched",
            hatched.marker_box,
            [_empty_centered_paragraph()],
            fill=None,
            line_color=hatched.line_color,
            pattern_fill=hatched.pattern_fill,
            line_width=3175,
            prst="ellipse",
            anchor="ctr",
        )
    )

    for entry in LEGEND_ENTRIES:
        shapes.append(
            _textbox(
                next_id(),
                "LegendLabel",
                entry.label_box,
                [_one_line(entry.label)],
                fill=None,
                line_color="none",
                anchor="ctr",
                wrap="none",
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )
    return shapes


def paint_narrative_rail(next_id) -> list[str]:
    """Right rail explaining the margin drivers by archetype and period."""

    return [
        _textbox(
            next_id(),
            "RevenueAndMarginDriversRail",
            NARRATIVE_RAIL,
            _narrative_paragraphs(),
            fill=None,
            line_color="none",
        )
    ]


def paint_narrative_header(next_id) -> list[str]:
    """Single-cell table header for the right narrative rail."""

    return [
        table(
            next_id(),
            "RevenueAndMarginDriversHeader",
            *NARRATIVE_HEADER.emu(),
            col_widths=[IN(NARRATIVE_HEADER.w)],
            rows=[
                trow(
                    [
                        rcell(
                            [
                                tpara(
                                    [trun("Revenue and EBIT margin drivers", size=PT(10), bold=True, color=BLACK, font=FONT)],
                                    mar_l=0,
                                    indent=0,
                                )
                            ],
                            l_ins=41564,
                            r_ins=41564,
                            T=edge(WHITE),
                            B=edge(BLACK),
                        )
                    ],
                    h=IN(NARRATIVE_HEADER.h),
                )
            ],
        )
    ]


def paint_source_note(next_id) -> list[str]:
    """Compact source/constituent line retained at the source position."""

    return [
        _textbox(
            next_id(),
            "SourceNote",
            SOURCE_NOTE,
            [_source_paragraph()],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    ]


def paint_preliminary_chip(next_id) -> list[str]:
    """House Preliminary chip, intentionally painted after body content."""

    return [prelim_chip()]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    shapes.extend(paint_chrome(next_id))
    shapes.extend(paint_native_bubble_chart(next_id))
    shapes.extend(paint_manual_axis_labels(next_id))
    shapes.extend(paint_legend(next_id))
    shapes.extend(paint_narrative_rail(next_id))
    shapes.extend(paint_narrative_header(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_preliminary_chip(next_id))
    return "".join(shapes)


def render() -> str:
    return slide(_body())
