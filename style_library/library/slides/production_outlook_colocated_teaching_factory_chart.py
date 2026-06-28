"""Teaching exemplar: Golden Dome production outlook with co-located sensors and interceptors.

ROLE
  production_ramp / phased_capacity_forecast

USE WHEN
  A slide needs one dominant production-ramp chart, a phase legend, cumulative
  callout rings, a manually drawn capacity reference line, and forecast-assumption
  text blocks below the chart.

TEACHES
  - fully declarative native stacked-column charting with column_chart(mode="stacked")
  - point-level series coloring to model phase transitions inside a stacked bar
  - manual category ticks, in-year total labels, source data labels, and cumulative callouts
  - manually overlaid solid reference line when the source was a combo chart
  - two-panel chart/backing geometry that doubles as assumptions-block background
  - source-positioned requirement-met callout and off-house Preliminary / Note placement

TEXT-FIT PRECEDENT
  forecast_assumptions_left:
    geometry: 6.206in wide x 1.279in high
    type: Arial 10pt, black, 100% line spacing
    content: one bold heading + four hanging bullets
    copy_when: the slide needs dense assumptions directly under a dominant chart
               and the panel is a continuation of the chart background
  forecast_assumptions_right:
    geometry: 4.835in wide x 1.111in high
    type: Arial 10pt, black, 100% line spacing
    content: one bold heading + two hanging bullets + one trailing blank paragraph
    copy_when: the right forecast period is shorter and the text block must align
               to the same top edge as the left block
  cumulative_callouts:
    geometry: 0.602in x 0.340in ellipse rings, labels at 10pt
    content: short cumulative totals only; three-digit values fit safely

SOURCE NOTE
  Teaching rewrite of the source-faithful `production_outlook_colocated.py` module.
  This version intentionally replaces the bundled styled_chart template with a
  native `column_chart(mode="stacked", ...)` spec for the production-start bars.
  The source chart was a combo-style exhibit: stacked starts plus a Franklin
  capacity reference line. The bar stack is now native chart data; the capacity
  line is an explicit, editable set of solid connectors over the chart,
  matching the source line series.

FIDELITY NOTE
  This is a practical factory rebuild, not a byte-identical chart-template port.
  It preserves the visible chart semantics, the phase-colored stacked starts, the
  manual axis/year labels, source chart data labels, cumulative rings, labels,
  assumption blocks, logos, footnote, off-house Preliminary chip, and FY32
  requirement-met callout. The source workbook rows and key XML style values are
  carried explicitly in the module as Python constants. Tiny differences can
  remain in native chart XML ordering and connector interpolation versus the
  source combo chart part.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, paragraph, picture,
    run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
PRELIM = "FFFFCC"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
FONT = "Arial"

LAYOUT = "slideLayout4"

# The two logos are slide-level picture relationships. They remain image parts
# because they are brand marks, not shapes/charts that should be rebuilt.
IMAGES = [
    {"rId": "rId3", "file": "image7_3071a231.jpeg"},
    {"rId": "rId4", "file": "image8_ffd85751.png"},
]

# Fully declarative chart data. The source chart used two stacked bar series with
# point-level colors to split years that straddle phases; a third series was the
# Franklin capacity line. The native factory rebuild keeps the bar stack native
# and draws the capacity line manually so the teaching module stays readable.
CHART_CATEGORIES: tuple[str, ...] = tuple(f"FY{year}" for year in range(26, 36))

PHASE_1 = "9DB1CF"
PHASE_2 = "6F8DB9"
PHASE_3 = "364D6E"
FRANKLIN_CAPACITY_COLOR = BLACK
FRANKLIN_CAPACITY_LINE_WIDTH = 19_050

# Exact chart-part styling values pulled from slide11_chart2.xml. Keeping these
# as named constants makes the native chart auditable against the source OOXML.
SOURCE_PLOT_LAYOUT = {
    "x": 0.03242793791574279,
    "y": 0.06984751598622725,
    "w": 0.9603658536585366,
    "h": 0.8603049680275455,
}
SOURCE_VALUE_AXIS_MIN = 0
SOURCE_VALUE_AXIS_MAX = 70
SOURCE_VALUE_AXIS_MAJOR_UNIT = 5
SOURCE_GAP_WIDTH = 80
SOURCE_BAR_OVERLAP = 100

# Exact rows read from slide11_chart2.xlsb Sheet1 and mirrored in the chart
# XML's cached values. Lists are passed to deck_core; tuples are retained for
# validation so future edits cannot silently drift from the workbook.
SOURCE_XLSB_LOWER_START_LAYER_VALUES = (None, 5, 18, 25, 17, 19, 20, None, None, None)
SOURCE_XLSB_UPPER_START_LAYER_VALUES = (None, None, None, None, 9, 7, None, None, None, None)
SOURCE_XLSB_FRANKLIN_CAPACITY_VALUES = (8, 17, 28, 50, 50, 50, 50, 50, 50, 50)

LOWER_START_LAYER_VALUES = list(SOURCE_XLSB_LOWER_START_LAYER_VALUES)
UPPER_START_LAYER_VALUES = list(SOURCE_XLSB_UPPER_START_LAYER_VALUES)
FRANKLIN_CAPACITY_VALUES = list(SOURCE_XLSB_FRANKLIN_CAPACITY_VALUES)

# Point colors encode the phase schedule without turning every phase-year
# intersection into its own sparse series. This mirrors the converted source:
# FY30 splits across Phase 1 / Phase 2 and FY31 splits across Phase 2 / Phase 3;
# FY32 is fully Phase 3.
PRODUCTION_START_SERIES: tuple[dict, ...] = (
    {
        "name": "Production starts lower layer",
        "color": PHASE_1,
        "values": LOWER_START_LAYER_VALUES,
        # Source dPt overrides: idx 4 = Phase 2; idx 5-6 = Phase 3.
        "data_point_colors": [
            PHASE_1,  # FY26 blank; harmless placeholder keeps list aligned
            PHASE_1, PHASE_1, PHASE_1,
            PHASE_2,
            PHASE_3, PHASE_3,
            PHASE_1, PHASE_1, PHASE_1,
        ],
        "hide_labels": True,
    },
    {
        "name": "Production starts upper layer",
        "color": PHASE_2,
        "values": UPPER_START_LAYER_VALUES,
        # Source dPt override: idx 4 = Phase 1; all other points use Phase 2.
        "data_point_colors": [
            PHASE_2, PHASE_2, PHASE_2, PHASE_2,
            PHASE_1,
            PHASE_2, PHASE_2, PHASE_2, PHASE_2, PHASE_2,
        ],
        "hide_labels": True,
    },
)

# Kept as a readable data mirror for agents/tools that expect the converted-slide
# data-dict shape. CHARTS consumes the two bar layers; the capacity series is
# rendered as editable connector geometry by paint_capacity_reference_line().
_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": [
        {"name": "Starts lower layer", "values": list(LOWER_START_LAYER_VALUES)},
        {"name": "Starts upper layer", "values": list(UPPER_START_LAYER_VALUES)},
        {"name": "Franklin capacity", "values": list(FRANKLIN_CAPACITY_VALUES)},
    ],
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in PRODUCTION_START_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    # The source chart XML used per-point data-label offsets and mixed label
    # color overrides; those labels are manualized as slide text below.
    "show_value_labels": False,
    "value_axis_format": '#,##0;"-"#,##0',
    "cat_label_size_pt": 10,
    "gap_width": SOURCE_GAP_WIDTH,
    "bar_overlap": SOURCE_BAR_OVERLAP,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9525,
    "value_axis_min": SOURCE_VALUE_AXIS_MIN,
    "value_axis_max": SOURCE_VALUE_AXIS_MAX,
    "value_axis_major_unit": SOURCE_VALUE_AXIS_MAJOR_UNIT,
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
    "cat_header": "Fiscal year",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: comments the module can expose programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "production_ramp",
    "use_when": (
        "Use for a phased production-ramp chart with cumulative milestone rings, "
        "manual fiscal-year ticks, phase legend keys, and short forecast "
        "assumption blocks under the exhibit."
    ),
    "teaches": [
        "native stacked column chart",
        "data-point colors for phase transitions",
        "manual solid combo-chart reference line",
        "manual category ticks",
        "manualized source chart data labels",
        "manual in-year total labels",
        "manual cumulative data labels",
        "ellipse callout rings over a chart",
        "two-panel forecast assumptions",
        "requirement-met callout",
        "off-house preliminary chip and footnote preservation",
    ],
}

TEXT_FIT = {
    "forecast_assumptions_left": {
        "box_in": (6.206, 1.279),
        "font_pt": 10,
        "content": "one bold heading + four hanging bullets",
        "note": "Uses 100% line spacing and the source hanging-bullet margin pair.",
    },
    "forecast_assumptions_right": {
        "box_in": (4.835, 1.111),
        "font_pt": 10,
        "content": "one bold heading + two hanging bullets + one blank paragraph",
        "note": "Shorter right block aligns top to the left block and inherits the panel background.",
    },
    "cumulative_callouts": {
        "ring_in": (0.602, 0.340),
        "label_font_pt": 10,
        "content": "short cumulative totals: 5, 23, 48, 74, 100, 120",
    },
    "footnote": {
        "box_in": (12.367, 0.206),
        "font_pt": 10,
        "content": "single Note line; kept off the house sources position",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic geometry/data records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU at the last possible moment."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class TextZone:
    name: str
    box: Box
    font_pt: float
    fit_note: str


@dataclass(frozen=True)
class Panel:
    name: str
    box: Box
    fill: str


@dataclass(frozen=True)
class YearTick:
    x: float
    label: str


@dataclass(frozen=True)
class AnnualStartLabel:
    box: Box
    label: str
    text_color: str = BLACK


@dataclass(frozen=True)
class LegendEntry:
    label: str
    fill: str | None
    swatch: Box | None
    caption: Box


@dataclass(frozen=True)
class CapacitySegment:
    start: tuple[float, float]
    end: tuple[float, float]


@dataclass(frozen=True)
class Ring:
    box: Box


@dataclass(frozen=True)
class CumulativeLabel:
    box: Box
    label: str


@dataclass(frozen=True)
class ForecastBlock:
    heading: str
    box: Box
    bullets: tuple[str, ...]
    trailing_blank: bool = False


@dataclass(frozen=True)
class ImageMark:
    name: str
    r_id: str
    box: Box


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: background panels, chart, manual labels, logos, and notes.
# ════════════════════════════════════════════════════════════════════════════
BACKGROUND_PANELS: tuple[Panel, ...] = (
    # Paint order matches the source: right panel first, then the left panel.
    Panel("ForecastPanel_FY32_FY35", Box(8.000, 2.172, 4.835, 4.536), GRAY_2),
    Panel("ForecastPanel_FY27_FY31", Box(1.794, 2.172, 6.206, 4.536), GRAY_1),
)

CHART_FRAME = Box(0.398, 1.931, 12.528, 3.530)
CHART_TITLE = TextZone(
    name="ChartTitle",
    box=Box(0.510, 1.816, 2.667, 0.167),
    font_pt=10,
    fit_note="Bottom-anchored, no-wrap external chart title with footnote run.",
)

YEAR_TICK_ZONE = TextZone(
    name="FiscalYearTick",
    box=Box(0.0, 5.260, 0.344, 0.167),
    font_pt=10,
    fit_note="10 centered FY labels; keep labels short and uniform.",
)

ANNUAL_START_LABEL_ZONE = TextZone(
    name="AnnualStartLabel",
    box=Box(0.0, 0.0, 0.191, 0.167),
    font_pt=10,
    fit_note="Short in-year total label over FY30/FY31 split bars.",
)

LEGEND_SWATCH_W = 0.196
LEGEND_SWATCH_H = 0.146
LEGEND_LABEL_H = 0.167

LEFT_FORECAST_BLOCK = TextZone(
    name="ForecastAssumptions_FY27_FY31",
    box=Box(1.794, 5.429, 6.206, 1.279),
    font_pt=10,
    fit_note="Heading + 4 bullets; 100% line spacing and source hanging indent.",
)
RIGHT_FORECAST_BLOCK = TextZone(
    name="ForecastAssumptions_FY32_FY35",
    box=Box(8.000, 5.429, 4.835, 1.111),
    font_pt=10,
    fit_note="Heading + 2 bullets + blank paragraph; top-aligned with left block.",
)

FOOTNOTE = TextZone(
    name="NoteLine",
    box=Box(0.495, 6.790, 12.367, 0.206),
    font_pt=10,
    fit_note="One-line note, source position intentionally below house sources line.",
)

CUMULATIVE_AXIS_CAPTION = TextZone(
    name="CumulativeAxisCaption",
    box=Box(6.382, 1.791, 1.600, 0.200),
    font_pt=10,
    fit_note="Right-aligned label above the cumulative ring row.",
)

PRELIM_CHIP = TextZone(
    name="OffHousePreliminaryChip",
    box=Box(7.911, 0.122, 1.605, 0.290),
    font_pt=12,
    fit_note="Off-house Preliminary chip kept at source position.",
)

REQUIREMENT_CALLOUT = TextZone(
    name="RequirementMetCallout",
    box=Box(9.338, 2.240, 3.368, 0.694),
    font_pt=10,
    fit_note="One centered italic sentence; keep to one line if possible.",
)

LOGOS: tuple[ImageMark, ...] = (
    ImageMark("Picture 2", "rId3", Box(11.431, 0.048, 0.922, 0.922)),
    ImageMark("Picture 8", "rId4", Box(12.372, 0.048, 0.922, 0.922)),
)


# ════════════════════════════════════════════════════════════════════════════
# Manual chart labels, legend keys, rings, and capacity reference line.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = (
    YearTick(1.233, "FY26"),
    YearTick(2.436, "FY27"),
    YearTick(3.639, "FY28"),
    YearTick(4.842, "FY29"),
    YearTick(6.045, "FY30"),
    YearTick(7.248, "FY31"),
    YearTick(8.451, "FY32"),
    YearTick(9.655, "FY33"),
    YearTick(10.858, "FY34"),
    YearTick(12.061, "FY35"),
)

ANNUAL_START_LABELS: tuple[AnnualStartLabel, ...] = (
    AnnualStartLabel(Box(6.122, 3.891, 0.191, 0.167), "26"),
    AnnualStartLabel(Box(7.325, 3.891, 0.191, 0.167), "26"),
)

# These were native chart dLbl entries in slide11_chart2.xml. The factory chart
# keeps native labels disabled because the source uses per-point manualLayout
# offsets and mixed label colors; re-authoring the visible labels as slide text
# keeps them editable and avoids losing the source's segment-level labels.
SOURCE_CHART_VALUE_LABELS: tuple[AnnualStartLabel, ...] = (
    AnnualStartLabel(Box(2.513, 4.802, 0.191, 0.167), "5"),
    AnnualStartLabel(Box(3.717, 4.239, 0.191, 0.167), "18"),
    AnnualStartLabel(Box(4.920, 3.934, 0.191, 0.167), "25"),
    AnnualStartLabel(Box(6.123, 4.760, 0.191, 0.167), "17", WHITE),
    AnnualStartLabel(Box(7.326, 4.717, 0.191, 0.167), "19", WHITE),
    AnnualStartLabel(Box(8.529, 4.152, 0.191, 0.167), "20"),
    AnnualStartLabel(Box(6.123, 4.196, 0.191, 0.167), "9", DK),
    AnnualStartLabel(Box(7.326, 4.153, 0.191, 0.167), "7", WHITE),
)

if tuple(label.label for label in SOURCE_CHART_VALUE_LABELS) != ("5", "18", "25", "17", "19", "20", "9", "7"):
    raise ValueError("Manualized source chart data labels no longer match slide11_chart2.xml")
if tuple(label.label for label in ANNUAL_START_LABELS) != ("26", "26"):
    raise ValueError("Manual stack-total labels no longer match the co-located source slide")

LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Phase 1", PHASE_1, Box(7.984, 1.811, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(8.236, 1.806, 0.505, LEGEND_LABEL_H)),
    LegendEntry("Phase 2", PHASE_2, Box(8.852, 1.811, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(9.104, 1.806, 0.505, LEGEND_LABEL_H)),
    LegendEntry("Phase 3", PHASE_3, Box(9.720, 1.811, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(9.972, 1.806, 0.505, LEGEND_LABEL_H)),
    LegendEntry("Franklin capacity (vessel starts)", None, None, Box(10.840, 1.806, 1.939, LEGEND_LABEL_H)),
)

# The native bar chart uses the exact manual plot layout from the source chart
# part. These points translate Franklin capacity values to slide coordinates
# using the source 0-70 value axis. The connectors are authored as regular slide
# shapes so the combo-chart line remains editable after the factory rebuild.
_CAPACITY_PLOT_LEFT = CHART_FRAME.x + SOURCE_PLOT_LAYOUT["x"] * CHART_FRAME.w
_CAPACITY_PLOT_TOP = CHART_FRAME.y + SOURCE_PLOT_LAYOUT["y"] * CHART_FRAME.h
_CAPACITY_PLOT_W = SOURCE_PLOT_LAYOUT["w"] * CHART_FRAME.w
_CAPACITY_PLOT_H = SOURCE_PLOT_LAYOUT["h"] * CHART_FRAME.h
_CAPACITY_AXIS_MAX = float(SOURCE_VALUE_AXIS_MAX)
_CATEGORY_STEP = _CAPACITY_PLOT_W / len(CHART_CATEGORIES)
_CAPACITY_POINTS: tuple[tuple[float, float], ...] = tuple(
    (
        _CAPACITY_PLOT_LEFT + _CATEGORY_STEP * (idx + 0.5),
        _CAPACITY_PLOT_TOP + (1.0 - value / _CAPACITY_AXIS_MAX) * _CAPACITY_PLOT_H,
    )
    for idx, value in enumerate(FRANKLIN_CAPACITY_VALUES)
)
CAPACITY_SEGMENTS: tuple[CapacitySegment, ...] = tuple(
    CapacitySegment(_CAPACITY_POINTS[idx], _CAPACITY_POINTS[idx + 1])
    for idx in range(len(_CAPACITY_POINTS) - 1)
)

HIGHLIGHT_RINGS: tuple[Ring, ...] = (
    Ring(Box(8.334, 2.507, 0.602, 0.340)),
    Ring(Box(11.933, 2.507, 0.602, 0.340)),
    Ring(Box(9.529, 2.507, 0.602, 0.340)),
    Ring(Box(10.726, 2.507, 0.602, 0.340)),
    Ring(Box(7.121, 2.507, 0.602, 0.340)),
    Ring(Box(2.311, 2.507, 0.602, 0.340)),
    Ring(Box(3.524, 2.507, 0.602, 0.340)),
    Ring(Box(4.717, 2.507, 0.602, 0.340)),
    Ring(Box(5.910, 2.507, 0.602, 0.340)),
    Ring(Box(6.382, 1.825, 0.211, 0.131)),
)

CUMULATIVE_LABELS: tuple[CumulativeLabel, ...] = (
    CumulativeLabel(Box(8.417, 2.542, 0.435, 0.269), "120"),
    CumulativeLabel(Box(12.016, 2.542, 0.435, 0.269), "120"),
    CumulativeLabel(Box(9.612, 2.542, 0.435, 0.269), "120"),
    CumulativeLabel(Box(10.809, 2.542, 0.435, 0.269), "120"),
    CumulativeLabel(Box(7.205, 2.542, 0.435, 0.269), "100"),
    CumulativeLabel(Box(2.472, 2.542, 0.279, 0.269), "5"),
    CumulativeLabel(Box(3.646, 2.542, 0.358, 0.269), "23"),
    CumulativeLabel(Box(4.839, 2.542, 0.358, 0.269), "48"),
    CumulativeLabel(Box(6.032, 2.542, 0.358, 0.269), "74"),
)

if tuple(label.label for label in CUMULATIVE_LABELS) != ("120", "120", "120", "120", "100", "5", "23", "48", "74"):
    raise ValueError("Cumulative callout labels must match the co-located source slide")


# ════════════════════════════════════════════════════════════════════════════
# Forecast assumption copy.
# ════════════════════════════════════════════════════════════════════════════
FORECAST_BLOCKS: tuple[ForecastBlock, ...] = (
    ForecastBlock(
        "FY27-FY31 forecast assumes:",
        LEFT_FORECAST_BLOCK.box,
        (
            "Franklin Phase 2 completion pulled forward to JUN ‘28 (vs. DEC ‘28), increasing capacity to 50x vessels / year",
            "US Navy purchases 10x MASC vessels / year, with FY29-FY31 vessels incremental to OBBBA amount",
            "US Army purchases 14-15 ARV / year FY29-FY31 ",
            "Fulfilling MASC and ARV orders takes precedence and GD consumes remaining yard capacity",
        ),
    ),
    ForecastBlock(
        "FY32-FY35 forecast assumes:",
        RIGHT_FORECAST_BLOCK.box,
        (
            "Fulfilling GD orders takes precedence (70% of yard capacity), with remaining capacity for other customers",
            "Interceptor and sensor production constraints limit FOC node fielding, driving relatively even production distribution throughout period",
        ),
        trailing_blank=True,
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Text helpers: keep the paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _r(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False, color: str = BLACK) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)


def _tight_para(runs, *, align=None, bullet=False):
    """100% line-spacing paragraph used by labels and source assumption bullets."""

    return paragraph(
        runs,
        align=align,
        mar_l=171_450 if bullet else 0,
        indent=-171_450 if bullet else 0,
        line_spacing=100_000,
        bullet=bullet,
    )


def _label_box(
    ids: ShapeIds,
    name: str,
    box: Box,
    text: str,
    *,
    align: str = "ctr",
    anchor: str = "ctr",
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
    wrap: str = "none",
    l_ins: int = 0,
    t_ins: int = 0,
    r_ins: int = 0,
    b_ins: int = 0,
) -> str:
    return text_box(
        ids.next(),
        name,
        *box.emu(),
        [_tight_para([_r(text, bold=bold, italic=italic, color=color)], align=align)],
        fill=None,
        line_color="none",
        anchor=anchor,
        wrap=wrap,
        l_ins=l_ins,
        t_ins=t_ins,
        r_ins=r_ins,
        b_ins=b_ins,
    )


def _forecast_paragraphs(block: ForecastBlock) -> list[str]:
    paras = [_tight_para([_r(block.heading, bold=True)])]
    paras.extend(_tight_para([_r(bullet)], bullet=True) for bullet in block.bullets)
    if block.trailing_blank:
        paras.append(paragraph([], line_spacing=100_000))
    return paras


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_background(out: list[str], ids: ShapeIds) -> None:
    for panel in BACKGROUND_PANELS:
        out.append(
            text_box(
                ids.next(),
                panel.name,
                *panel.box.emu(),
                [paragraph([], line_spacing=100_000)],
                fill=panel.fill,
                line_color="none",
            )
        )


def paint_chart(out: list[str], ids: ShapeIds) -> None:
    out.append(
        graphic_frame(
            sp_id=ids.next(),
            name="ProductionStartsChart",
            x=IN(CHART_FRAME.x),
            y=IN(CHART_FRAME.y),
            cx=IN(CHART_FRAME.w),
            cy=IN(CHART_FRAME.h),
            rId="rId2",
        )
    )


def paint_capacity_reference_line(out: list[str], ids: ShapeIds) -> None:
    for segment in CAPACITY_SEGMENTS:
        x1, y1 = segment.start
        x2, y2 = segment.end
        out.append(
            connector(
                ids.next(),
                "FranklinCapacityReferenceLine",
                IN(x1),
                IN(y1),
                IN(x2 - x1),
                IN(y2 - y1),
                color=FRANKLIN_CAPACITY_COLOR,
                width=FRANKLIN_CAPACITY_LINE_WIDTH,
            )
        )


def paint_chart_manual_labels(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            CHART_TITLE.name,
            *CHART_TITLE.box.emu(),
            [
                paragraph(
                    [
                        _r("Golden Dome Marauder starts by phase", bold=True),
                        _r("1", bold=True),
                    ],
                    mar_l=0,
                    indent=0,
                    line_spacing=100_000,
                )
            ],
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

    for tick in YEAR_TICKS:
        out.append(
            _label_box(
                ids,
                YEAR_TICK_ZONE.name,
                Box(tick.x, YEAR_TICK_ZONE.box.y, YEAR_TICK_ZONE.box.w, YEAR_TICK_ZONE.box.h),
                tick.label,
                align="ctr",
                wrap="none",
            )
        )

    for label in SOURCE_CHART_VALUE_LABELS:
        out.append(
            _label_box(
                ids,
                "SourceChartValueLabel",
                label.box,
                label.label,
                align="ctr",
                anchor="b",
                l_ins=17_463,
                r_ins=17_463,
                color=label.text_color,
            )
        )

    for label in ANNUAL_START_LABELS:
        out.append(
            _label_box(
                ids,
                ANNUAL_START_LABEL_ZONE.name,
                label.box,
                label.label,
                align="ctr",
                anchor="b",
                color=label.text_color,
                l_ins=17_463,
                r_ins=17_463,
            )
        )


def paint_chrome_and_logos(out: list[str], ids: ShapeIds) -> None:
    out.append("")
    out.append(
        ""
    )
    for logo in LOGOS:
        out.append(picture(ids.next(), logo.name, logo.r_id, *logo.box.emu()))


def paint_legend(out: list[str], ids: ShapeIds) -> None:
    # Swatches first, then the dashed capacity key, then captions — source paint order.
    for entry in LEGEND:
        if entry.swatch is None:
            continue
        out.append(
            text_box(
                ids.next(),
                "PhaseLegendSwatch",
                *entry.swatch.emu(),
                [paragraph([], align="ctr", line_spacing=100_000)],
                fill=entry.fill,
                line_color="none",
                anchor="ctr",
            )
        )

    out.append(
        connector(
            ids.next(),
            "FranklinCapacityLegendMark",
            IN(10.599),
            IN(1.884),
            IN(0.175),
            IN(0.000),
            color=BLACK,
            width=19_050,
            dashed=True,
            arrow=True,
        )
    )

    for entry in LEGEND:
        out.append(
            _label_box(
                ids,
                "LegendLabel",
                entry.caption,
                entry.label,
                align=None,
                anchor="ctr",
                wrap="none",
            )
        )


def paint_forecast_blocks(out: list[str], ids: ShapeIds) -> None:
    for block in FORECAST_BLOCKS:
        out.append(
            text_box(
                ids.next(),
                "ForecastAssumptions",
                *block.box.emu(),
                _forecast_paragraphs(block),
                fill=None,
                line_color="none",
            )
        )


def paint_footnote(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            FOOTNOTE.name,
            *FOOTNOTE.box.emu(),
            [_tight_para([_r("Note: (1) Assumes vessels are only produced at Franklin facility ")])],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )


def paint_cumulative_callouts(out: list[str], ids: ShapeIds) -> None:
    for ring in HIGHLIGHT_RINGS:
        out.append(
            text_box(
                ids.next(),
                "CumulativeValueRing",
                *ring.box.emu(),
                [paragraph([], align="ctr", line_spacing=100_000)],
                fill=None,
                line_color=BLACK,
                prst="ellipse",
                anchor="ctr",
            )
        )

    for label in CUMULATIVE_LABELS:
        out.append(
            text_box(
                ids.next(),
                "CumulativeValueLabel",
                *label.box.emu(),
                [_tight_para([_r(label.label)], align="ctr")],
                fill=None,
                line_color="none",
                wrap="none",
            )
        )

    out.append(
        text_box(
            ids.next(),
            CUMULATIVE_AXIS_CAPTION.name,
            *CUMULATIVE_AXIS_CAPTION.box.emu(),
            [_tight_para([_r("Cumulative vessels")], align="r")],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
        )
    )


def paint_preliminary_chip(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            PRELIM_CHIP.name,
            *PRELIM_CHIP.box.emu(),
            [paragraph([_r("Preliminary", size_pt=12, bold=True)], align="ctr", line_spacing=100_000)],
            fill=PRELIM,
            line_color="121415",
            line_width=19_050,
            anchor="ctr",
        )
    )


def paint_requirement_callout(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            REQUIREMENT_CALLOUT.name,
            *REQUIREMENT_CALLOUT.box.emu(),
            [_tight_para([_r("Est. requirement of 120x MR met in FY32", italic=True)], align="ctr")],
            fill=None,
            line_color=DK,
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_background(out, ids)
    paint_chart(out, ids)
    paint_capacity_reference_line(out, ids)
    paint_chart_manual_labels(out, ids)
    paint_chrome_and_logos(out, ids)
    paint_legend(out, ids)
    paint_forecast_blocks(out, ids)
    paint_footnote(out, ids)
    paint_cumulative_callouts(out, ids)
    paint_preliminary_chip(out, ids)
    paint_requirement_callout(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="Golden Dome Requirements",
    topic="Production Outlook",
    title="Production Outlook (co-located sensors and interceptors)",
    takeaway="All Phase 1 vessels started by FY30, Phase 2 by FY31, and Phase 3 by FY32",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
