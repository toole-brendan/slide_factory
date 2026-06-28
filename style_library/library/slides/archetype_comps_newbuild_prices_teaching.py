"""Teaching exemplar: archetype-comparison native bubble chart with external legend.

ROLE
  archetype_comparison / margin_recovery_timeline

USE WHEN
  A slide needs one large performance bubble chart, a compact manual archetype
  legend, and a constituent-company source note, but does NOT need a narrative
  rail. This is the cleaner, chart-dominant sibling of the VOCC performance
  teaching exemplar.

TEACHES
  - rebuilding a source bubble chart through the native `bubble_chart(...)` factory
  - embedding all chart data, point styles, axes, and bubble-size values in Python
  - generating an editable embedded `.xlsx` at build time with no sidecar assets
  - full-width bubble-chart placement for a chart-only archetype comparison
  - manual year ticks below a native chart with hidden native x-axis labels
  - manual y-axis title outside the chart frame
  - mixed legend grammar: solid archetype dots, a patterned archetype dot, and
    a revenue bubble-size ring
  - compact off-house source note with colored constituent labels

TEXT-FIT PRECEDENT
  chart_dominant_body:
    geometry: 12.540in wide x 5.200in high
    type: native editable bubble chart plus external labels
    content: 73 chart points across 2020-2024, encoded by x/y/bubble-size/color
    copy_when: the chart itself is the exhibit and the surrounding text should be
               limited to axis title, legend, and source detail

  manual_legend:
    geometry: approx. 2.46in wide x 1.50in high, bottom-right of chart body
    type: Arial 10pt no-wrap labels
    content: 5 archetype marks plus one $10B revenue bubble-size key
    copy_when: native chart legend is too opaque or template-driven to explain
               marker color, pattern, and size clearly

  source_note:
    geometry: 5.102in wide x 0.349in high
    type: Arial 7pt with colored bold archetype labels
    content: one dense constituent-company source line
    copy_when: source/constituent detail is important but should not occupy the
               locked house source band

SOURCE NOTE
  Teaching rewrite of the source-faithful `archetype_comps_newbuild_prices.py`
  module. The chart values and styling controls were transcribed from the source
  chart/workbook pair into explicit Python constants. This module does not read
  any chart asset files at runtime: `bubble_chart()` builds the chart XML and its
  editable embedded workbook directly from `CHART_STYLE`.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. It preserves the visible chart semantics, 73 source points, point fills,
  the standalone-terminal hatch, fixed axes, manual plot layout, bubble scale,
  manual year ticks, legend, source note, Preliminary chip, and body chrome.
  Tiny differences can remain in PowerPoint's native bubble rendering versus the
  original chart part.
"""
from __future__ import annotations

from dataclasses import dataclass
from deck_core.authoring import (
    Chrome, IN, PT, body_slide, bubble_chart, graphic_frame, paragraph, run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
DK = "162029"
FONT = "Arial"

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
    "role": "archetype_comparison / margin_recovery_timeline",
    "use_when": (
        "Use when a slide compares margin behavior across value-chain "
        "archetypes with one full-width, style-dense bubble chart and a "
        "manual legend, rather than a chart-plus-commentary-rail layout."
    ),
    "teaches": [
        "native editable bubble_chart rebuilt from source XML/XLSB",
        "source workbook rows embedded as Python constants",
        "point-level bubble colors through data_point_colors",
        "patterned bubble series for standalone terminal operators",
        "full-width chart-dominant layout",
        "manual year ticks over a native bubble chart",
        "manual y-axis title outside the chart frame",
        "external legend for marker color, hatch pattern, and bubble size",
        "compact colored source note",
    ],
    "source_module": "archetype_comps_newbuild_prices.py",
    "source_chart_assets": ("slide32_chart17.xml", "slide32_chart17.xlsb"),
    "rebuild_strategy": "replace bundled source-chart assets with native bubble_chart",
}

TEXT_FIT = {
    "chart_frame": {
        "box_in": (12.540, 5.200),
        "content": "native bubble chart with 73 bubble points and no text rail",
        "note": "The chart can span almost the full body because all explanation is externalized to legend + title.",
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
        "note": "Longest label fits because it starts at x=10.601in and uses a 2.139in box.",
    },
    "source_note": {
        "box_in": (5.102, 0.349),
        "font_pt": 7,
        "content": "one dense constituent-company source line",
    },
}

COPY_RULES = [
    "Use native bubble_chart() when the exhibit is a revenue-scaled x/y bubble chart and the source point styles can be expressed as series fills, data-point fills, or pattern fills.",
    "Use a full-width chart frame when the chart is the evidence and no explanatory right rail is needed.",
    "Use the slide-level legend as the semantic contract when the native chart series preserve source buckets rather than clean archetype groups.",
    "Keep manual ticks and y-axis title outside the chart when the source chart hid or suppressed native labels.",
    "Use a colored source note for constituent detail when a full appendix table would overtake the exhibit.",
]

NATIVE_CHART_CONTRACT = {
    "factory": "bubble_chart",
    "visible_encoding": {
        "x": "calendar year, 2020-2024",
        "y": "EBIT margin (%)",
        "bubble_size": "revenue, with $10B shown by the external ring key",
        "marker_color": "value-chain archetype",
    },
    "source_chart_xml": {
        "chart_type": "bubbleChart",
        "source_bucket_count": 7,
        "point_count": 73,
        "bubble_scale": 66,
        "x_axis_min_max": (2019, 2025),
        "y_axis_min_max": (-50, 70),
    },
    "manual_shapes": (
        "year ticks, EBIT Margin y-axis title, archetype legend, revenue ring key, "
        "compact source note, and Preliminary chip"
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
class BubbleSeries:
    """One source chart bucket expressed as native bubble-chart inputs.

    The source chart grouped points in seven sparse buckets. We keep that draw
    order for fidelity and use per-point fill overrides to carry the external
    legend's archetype semantics.
    """

    name: str
    x_values: tuple[int | float, ...]
    y_values: tuple[float, ...]
    bubble_sizes: tuple[float, ...]
    color: str | None = None
    pattern: dict[str, str] | None = None
    data_point_colors: tuple[str | None, ...] | None = None
    note: str = ""

    @property
    def point_count(self) -> int:
        return len(self.x_values)

    def chart_dict(self) -> dict:
        out = {
            "name": self.name,
            "x_values": list(self.x_values),
            "y_values": list(self.y_values),
            "bubble_sizes": list(self.bubble_sizes),
        }
        if self.color is not None:
            out["color"] = self.color
        if self.pattern is not None:
            out["pattern"] = dict(self.pattern)
        if self.data_point_colors is not None:
            out["data_point_colors"] = list(self.data_point_colors)
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
    fill: str | None
    line_color: str = DK
    pattern_fill: dict | None = None


@dataclass(frozen=True)
class SourceRun:
    """A run in the compact colored source note."""

    text: str
    color: str = BLACK
    bold: bool = False


@dataclass(frozen=True)
class ChartReading:
    """Human reading encoded for the teaching corpus; not painted."""

    observation: str
    authoring_use: str


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.373, 1.696, 12.540, 5.200)
Y_AXIS_TITLE = Box(0.533, 1.505, 1.064, 0.167)
YEAR_TICK_Y = 6.736
YEAR_TICK_SIZE = (0.306, 0.167)
LEGEND_ZONE = Box(10.283, 5.139, 2.457, 1.500)
LEGEND_LABEL_H = 0.167
SOURCE_NOTE = Box(0.495, 7.081, 5.102, 0.349)


# ════════════════════════════════════════════════════════════════════════════
# Native chart data and factory specification.
# ════════════════════════════════════════════════════════════════════════════
# Source-chart transcription summary:
#   chart part:       slide32_chart17.xml
#   source workbook:  slide32_chart17.xlsb
#   c:bubbleScale:    66
#   x axis:           min=2019, max=2025, major=1, labels hidden
#   y axis:           min=-50, max=70, major=10, labels shown
#   plot layout:      manual inner plot rectangle below
#   data layout:      source workbook column A carries years; each source bucket
#                     then uses a y-value / bubble-size column pair. The native
#                     workbook generated by bubble_chart() compacts those sparse
#                     buckets into editable columns.
SOURCE_PLOT_LAYOUT = {
    "x": 0.036134570123217497,
    "y": 0.032721202003338896,
    "w": 0.95666620517790391,
    "h": 0.92754590984974961,
}
SOURCE_BUBBLE_SCALE = 66
SOURCE_X_AXIS_MIN = 2019
SOURCE_X_AXIS_MAX = 2025
SOURCE_X_AXIS_MAJOR_UNIT = 1
SOURCE_Y_AXIS_MIN = -50
SOURCE_Y_AXIS_MAX = 70
SOURCE_Y_AXIS_MAJOR_UNIT = 10
SOURCE_AXIS_LINE_WIDTH = 9_525
SOURCE_BUBBLE_LINE_WIDTH = 3_175
STANDALONE_PATTERN = {"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"}

BUBBLE_SOURCE_SERIES: tuple[BubbleSeries, ...] = (
    BubbleSeries(
        name="Source bucket 1 — shipbuilder residuals",
        x_values=(2021, 2022, 2022),
        y_values=(-2.9787234042553195, -33.20027982387556, 1.9083969465648851),
        bubble_sizes=(19771.325688420737, 3856.7506229268834, 20790.68069640845),
        color=SHIPBUILDER_RED,
        note="Default red source bucket; three shipbuilder points.",
    ),
    BubbleSeries(
        name="Source bucket 2 — mixed shipbuilder / owner-operator",
        x_values=(2020, 2021, 2021, 2022, 2020, 2021, 2021, 2022, 2023, 2023, 2024, 2024),
        y_values=(
            -7.826086956521738,
            -38.99333333333333,
            4.1817392562581395,
            0.3434112180997913,
            10.954584404455868,
            54.245502842762605,
            37.24290927185272,
            45.33351996143019,
            -8.174809189880284,
            6.617537812379283,
            42.112632603175356,
            12.68588852038087,
        ),
        bubble_sizes=(
            21176.49225216599,
            3785.9985360805663,
            7821.8697999999995,
            11784.824390166483,
            29175.0,
            10729.0,
            48232.0,
            64299.0,
            5162.2,
            33653.0,
            8427.4,
            37388.0,
        ),
        color=OWNER_OPERATOR_BLUE,
        data_point_colors=(
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        note="Default owner/operator blue with first four shipbuilder points overridden red.",
    ),
    BubbleSeries(
        name="Source bucket 3 — mixed archetype operating margins",
        x_values=(
            2021,
            2022,
            2023,
            2024,
            2020,
            2020,
            2021,
            2022,
            2022,
            2023,
            2024,
            2021,
            2021,
            2022,
            2022,
            2022,
            2023,
            2023,
            2023,
            2024,
        ),
        y_values=(
            7.840197254431562,
            -0.13365410318096765,
            3.0864197530864197,
            2.3054755043227666,
            18.261523046092183,
            10.297043287370515,
            42.15738351798452,
            36.14512215764826,
            50.73212274388066,
            14.143675169182718,
            13.392813131562084,
            51.92159420289856,
            55.61092637836599,
            65.80422960725076,
            59.455101588262075,
            14.103882746207253,
            59.61611909650924,
            30.965074903765107,
            21.258235671389425,
            22.182558229929164,
        ),
        bubble_sizes=(
            1089.4355999999998,
            8004.243600000001,
            25097.40737584917,
            23479.89660725644,
            3992.0,
            14577.0,
            26356.0,
            3544.6,
            36401.0,
            19210.0,
            20287.0,
            690.0,
            793.639,
            993.0,
            1113.859,
            1555.6,
            974.0,
            1511.406,
            1715.1,
            2083.894,
        ),
        color=CHARTER_GREEN,
        data_point_colors=(
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            OWNER_OPERATOR_BLUE,
            OWNER_OPERATOR_BLUE,
            OWNER_OPERATOR_BLUE,
            OWNER_OPERATOR_BLUE,
            OWNER_OPERATOR_BLUE,
            OWNER_OPERATOR_BLUE,
            OWNER_OPERATOR_BLUE,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        note="Default charter green with shipbuilder and owner/operator point overrides.",
    ),
    BubbleSeries(
        name="Source bucket 4 — owner-operator / integrated-terminal mix",
        x_values=(2020, 2022, 2023, 2024, 2020, 2021, 2022, 2023, 2024, 2020, 2020, 2021, 2022, 2023, 2024),
        y_values=(
            2.517434937914611,
            3.845388188453882,
            1.324192336589031,
            5.615161719790116,
            13.204595717136847,
            36.315755873340144,
            48.91892752515603,
            11.90149374243036,
            17.827526070398974,
            13.105694094747339,
            31.652219595482006,
            29.325000000000003,
            19.03454587051018,
            25.494276795005206,
            29.764837625979844,
        ),
        bubble_sizes=(
            7190.017000000001,
            1025.5135,
            16496.1230702495,
            17280.39191804366,
            1853.9,
            3132.8,
            12561.6,
            2477.0,
            2809.7,
            460.319,
            3807.0,
            4000.0,
            4371.0,
            3844.0,
            4465.0,
        ),
        color=OWNER_OPERATOR_BLUE,
        data_point_colors=(
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            None,
            None,
            None,
            None,
            None,
            CHARTER_GREEN,
            TERMINAL_INTEGRATED_BLUE,
            TERMINAL_INTEGRATED_BLUE,
            TERMINAL_INTEGRATED_BLUE,
            TERMINAL_INTEGRATED_BLUE,
            TERMINAL_INTEGRATED_BLUE,
        ),
        note="Default owner/operator blue with shipbuilder, charter, and integrated-terminal overrides.",
    ),
    BubbleSeries(
        name="Source bucket 5 — standalone-terminal pattern bucket",
        x_values=(2020, 2023, 2024, 2024, 2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024),
        y_values=(
            2.1914285714285713,
            3.2152659783034894,
            1.9931102362204725,
            27.35885788449059,
            32.75701021875992,
            42.955828628362674,
            40.61280117184256,
            47.833780160857906,
            35.1868290838553,
            50.92657155595185,
            31.215682587438888,
            50.728753109918834,
            37.84991786980203,
            53.95908194270246,
        ),
        bubble_sizes=(
            6445.019381093996,
            8463.5362,
            8413.2928,
            2311.5,
            1380.7877834240462,
            1505.5,
            1698.04861787784,
            1865.0,
            1559.4693328206115,
            2243.0,
            1361.686873471687,
            2388.326,
            1489.1151821002356,
            2739.524,
        ),
        pattern=STANDALONE_PATTERN,
        data_point_colors=(
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            SHIPBUILDER_RED,
            CHARTER_GREEN,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        note="Default standalone-terminal pct50 pattern with shipbuilder and charter overrides.",
    ),
    BubbleSeries(
        name="Source bucket 6 — shipbuilder / charter mix",
        x_values=(2020, 2023, 2024, 2020, 2021, 2024),
        y_values=(6.697282816685799, 2.6524303821389523, 2.206755753526355, 42.43581410464738, 47.85417941916616, 53.34161735700197),
        bubble_sizes=(1410.0531899999999, 5738.553180941462, 7291.6243757866105, 1230.8, 1470.3, 1014.0),
        color=SHIPBUILDER_RED,
        data_point_colors=(None, None, None, CHARTER_GREEN, CHARTER_GREEN, CHARTER_GREEN),
        note="Default shipbuilder red with three charter-company overrides.",
    ),
    BubbleSeries(
        name="Source bucket 7 — shipbuilder / charter residuals",
        x_values=(2023, 2024, 2020),
        y_values=(1.7566688353936235, 5.16068282607375, 43.17748917748918),
        bubble_sizes=(1049.4636, 1018.11285, 462.0),
        color=SHIPBUILDER_RED,
        data_point_colors=(None, None, CHARTER_GREEN),
        note="Default shipbuilder red with one charter-company override.",
    ),
)

# Readable data mirror for agents/tools that expect the converted-slide dict
# shape. CHARTS consumes the same values through bubble_chart().
_CHART0_DATA = {
    "categories": None,
    "series": [series.chart_dict() for series in BUBBLE_SOURCE_SERIES],
}

CHART_STYLE = {
    "series": [series.chart_dict() for series in BUBBLE_SOURCE_SERIES],
    "show_legend": False,
    "x_axis_format": "General",
    "y_axis_format": '#,##0;"-"#,##0',
    "bubble_size_format": "General",
    "x_axis_min": SOURCE_X_AXIS_MIN,
    "x_axis_max": SOURCE_X_AXIS_MAX,
    "x_axis_major_unit": SOURCE_X_AXIS_MAJOR_UNIT,
    "y_axis_min": SOURCE_Y_AXIS_MIN,
    "y_axis_max": SOURCE_Y_AXIS_MAX,
    "y_axis_major_unit": SOURCE_Y_AXIS_MAJOR_UNIT,
    "show_x_axis_labels": False,
    "show_y_axis_labels": True,
    "show_gridlines": False,
    "axis_line_color": "scheme:tx1",
    "axis_line_width": SOURCE_AXIS_LINE_WIDTH,
    "axis_label_size_pt": 10,
    "axis_label_color": BLACK,
    "x_axis_crosses_at": 0,
    "y_axis_crosses": "min",
    "bubble_scale": SOURCE_BUBBLE_SCALE,
    "show_negative_bubbles": False,
    "bubble_line_color": "scheme:tx1",
    "bubble_line_width": SOURCE_BUBBLE_LINE_WIDTH,
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
}

CHARTS = [bubble_chart(**CHART_STYLE)]

CHART_READINGS: tuple[ChartReading, ...] = (
    ChartReading(
        "Shipbuilder margins recover by 2024 but remain low-to-mid-single-digit.",
        "Use the title for the takeaway; do not add a narrative rail unless the slide needs causality detail.",
    ),
    ChartReading(
        "Revenue bubble size is part of the comparison, so the $10B ring key is mandatory.",
        "Never remove the hollow ring legend when copying this chart grammar.",
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Manual labels and legend entries copied from source slide coordinates.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, *YEAR_TICK_SIZE), label)
    for x, label in (
        (2.674, "2020"),
        (4.672, "2021"),
        (6.672, "2022"),
        (8.672, "2023"),
        (10.670, "2024"),
    )
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Shipbuilders",
        "solid_archetype_dot",
        Box(10.373, 5.583, 0.146, 0.146),
        Box(10.601, 5.578, 0.760, LEGEND_LABEL_H),
        SHIPBUILDER_RED,
    ),
    LegendEntry(
        "Owner/Operator (Carrier Segment)",
        "solid_archetype_dot",
        Box(10.373, 5.806, 0.146, 0.146),
        Box(10.601, 5.800, 2.139, LEGEND_LABEL_H),
        OWNER_OPERATOR_BLUE,
    ),
    LegendEntry(
        "Charter Companies",
        "solid_archetype_dot",
        Box(10.373, 6.028, 0.146, 0.146),
        Box(10.601, 6.023, 1.200, LEGEND_LABEL_H),
        CHARTER_GREEN,
    ),
    LegendEntry(
        "Terminal Operators (Integrated)",
        "solid_archetype_dot",
        Box(10.373, 6.250, 0.146, 0.146),
        Box(10.601, 6.245, 1.944, LEGEND_LABEL_H),
        TERMINAL_INTEGRATED_BLUE,
    ),
    LegendEntry(
        "Terminal Operators (Standalone)",
        "hatched_archetype_dot",
        Box(10.373, 6.472, 0.146, 0.146),
        Box(10.601, 6.467, 2.021, LEGEND_LABEL_H),
        None,
        pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"},
    ),
    LegendEntry(
        "$10B (Revenue)",
        "revenue_bubble_ring",
        Box(10.283, 5.139, 0.326, 0.326),
        Box(10.667, 5.224, 1.005, LEGEND_LABEL_H),
        None,
    ),
)

SOURCE_RUNS: tuple[SourceRun, ...] = (
    SourceRun("Source: Company filings |   "),
    SourceRun("Shipbuilders:", SHIPBUILDER_RED, True),
    SourceRun(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. "),
    SourceRun("Owner/Operator", OWNER_OPERATOR_BLUE, True),
    SourceRun(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. "),
    SourceRun("Charter Companies", CHARTER_GREEN, True),
    SourceRun(": Danaos, Costamare, Seaspan. "),
    SourceRun("Terminal Operators (Integrated)", TERMINAL_INTEGRATED_BLUE, True),
    SourceRun(": Maersk Terminals.         "),
    SourceRun("Terminal Operators (Standalone)", TERMINAL_STANDALONE_GRAY, True),
    SourceRun(": Hutchison Ports, ICTS. Note: Segment margins not burdened by corporate"),
)


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
    align: str | None = None,
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


def _source_paragraph() -> str:
    return paragraph(
        [
            run(src.text, size=PT(7), bold=src.bold or None, color=src.color, font=FONT)
            for src in SOURCE_RUNS
        ],
        line_spacing=100000,
    )


def paint_native_bubble_chart(next_id) -> list[str]:
    """Native editable bubble chart: x = year, y = margin, size = revenue."""

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
    # Paint solid dots and the revenue-size ring first, then the hatch chip,
    # matching the original source stacking while keeping entries semantic.
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

    return [""]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    shapes.extend(paint_native_bubble_chart(next_id))
    shapes.extend(paint_manual_axis_labels(next_id))
    shapes.extend(paint_legend(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_preliminary_chip(next_id))
    return "".join(shapes)


CHROME = Chrome(
    section="Commercial Maritime Value Chain",
    topic="Performance",
    title="Archetype Comps (1/3)",
    takeaway="Despite seeing improvement from rising new build prices and increased orders, shipbuilders only achieved low-to-mid-single digit EBIT margins by ‘24.",
)


def render() -> str:
    return body_slide(CHROME, _body())
