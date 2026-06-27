"""Teaching exemplar: Golden Dome production outlook with separate platforms.

ROLE
  production_ramp / phased_capacity_forecast

USE WHEN
  A slide needs one dominant production-ramp chart, a phase legend, cumulative
  callout rings, a manually drawn capacity reference line, and forecast-assumption
  text blocks below the chart.

TEACHES
  - fully declarative native stacked-column charting with column_chart(mode="stacked")
  - point-level series coloring to model phase transitions inside a stacked bar
  - manual category ticks, in-year labels, cumulative labels, and ring callouts
  - manually overlaid reference line when the source was a combo chart
  - two-panel chart/backing geometry that doubles as assumptions-block background
  - off-house Preliminary and Note placement preserved when it is intentionally
    part of the source composition

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
  Teaching rewrite of the source-faithful `production_outlook_separate.py` module.
  This version intentionally replaces the bundled styled_chart template with a
  native `column_chart(mode="stacked", ...)` spec for the production-start bars.
  The source chart was a combo-style exhibit: stacked starts plus a Franklin
  capacity reference line. The bar stack is now native chart data; the capacity
  line is an explicit, editable set of dashed connectors over the chart.

FIDELITY NOTE
  This is a practical factory rebuild, not a byte-identical chart-template port.
  It preserves the visible chart semantics, the phase-colored stacked starts, the
  manual axis/year labels, cumulative rings, labels, assumption blocks, logos,
  footnote, and off-house Preliminary chip. Tiny differences can remain in the
  native chart's internal bar width/axis XML and in the overlaid capacity-line
  placement versus the source combo chart part.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    connector,
    picture,
    breadcrumb,
    title_placeholder,
)
from deck_core.charts import graphic_frame, column_chart
from deck_core.style import IN, PT, BLACK, PRELIM, GRAY_1, GRAY_2, FONT

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

LOWER_START_LAYER_VALUES = [None, 5, 18, 25, 26, 26, 21, 8, 35, 35]
UPPER_START_LAYER_VALUES = [None, None, None, None, None, None, 14, 27, None, None]
FRANKLIN_CAPACITY_VALUES = [8, 17, 28, 50, 50, 50, 50, 50, 50, 50]

# Point colors encode the phase schedule without turning every phase-year
# intersection into its own sparse series. This mirrors the converted source:
# FY32 and FY33 split across two stacked layers as the ramp crosses phase bounds.
PRODUCTION_START_SERIES: tuple[dict, ...] = (
    {
        "name": "Production starts lower layer",
        "color": PHASE_1,
        "values": LOWER_START_LAYER_VALUES,
        "data_point_colors": [
            PHASE_1,  # FY26 blank; harmless placeholder keeps list aligned
            PHASE_1, PHASE_1, PHASE_1, PHASE_1, PHASE_1, PHASE_1,
            PHASE_2,
            PHASE_3, PHASE_3,
        ],
        "hide_labels": True,
    },
    {
        "name": "Production starts upper layer",
        "color": PHASE_2,
        "values": UPPER_START_LAYER_VALUES,
        "data_point_colors": [
            PHASE_2, PHASE_2, PHASE_2, PHASE_2, PHASE_2, PHASE_2,
            PHASE_2,
            PHASE_3,
            PHASE_3, PHASE_3,
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
        {"name": "Starts lower layer", "values": LOWER_START_LAYER_VALUES},
        {"name": "Starts upper layer", "values": UPPER_START_LAYER_VALUES},
        {"name": "Franklin capacity", "values": FRANKLIN_CAPACITY_VALUES},
    ],
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in PRODUCTION_START_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": '#,##0;"-"#,##0',
    "cat_label_size_pt": 10,
    "gap_width": 180,
    "bar_overlap": 100,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9525,
    "value_axis_min": 0,
    "value_axis_max": 60,
    "value_axis_major_unit": 10,
    "plot_layout": {
        # Solved from the manual FY tick centers: first/last category centers land
        # at the same x positions as the source labels under the chart.
        "x": 0.0324,
        "y": 0.0681,
        "w": 0.9603,
        "h": 0.8616,
    },
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
        "manual combo-chart reference line",
        "manual category ticks",
        "manual cumulative data labels",
        "ellipse callout rings over a chart",
        "two-panel forecast assumptions",
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
        "content": "short cumulative totals: 5, 23, 48, 74, 100, 135, 170, 205, 240",
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
    fit_note="Short in-year starts label over FY32/FY33 bars.",
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
    AnnualStartLabel(Box(8.528, 3.502, 0.191, 0.167), "35"),
    AnnualStartLabel(Box(9.731, 3.502, 0.191, 0.167), "35"),
)

LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Phase 1", PHASE_1, Box(7.984, 1.811, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(8.236, 1.806, 0.505, LEGEND_LABEL_H)),
    LegendEntry("Phase 2", PHASE_2, Box(8.852, 1.811, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(9.104, 1.806, 0.505, LEGEND_LABEL_H)),
    LegendEntry("Phase 3", PHASE_3, Box(9.720, 1.811, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(9.972, 1.806, 0.505, LEGEND_LABEL_H)),
    LegendEntry("Franklin capacity (vessel starts)", None, None, Box(10.840, 1.806, 1.939, LEGEND_LABEL_H)),
)

# The native bar chart uses the same manual plot layout. These points translate
# Franklin capacity values to slide coordinates, using a 0-60 value axis. The
# resulting dashed connectors are deliberately authored as shapes: PowerPoint
# edits them directly, and authors can see exactly where the line lives.
_CAPACITY_PLOT_LEFT = 0.8035
_CAPACITY_PLOT_TOP = 2.1710
_CAPACITY_PLOT_W = 12.0310
_CAPACITY_PLOT_H = 3.0420
_CAPACITY_AXIS_MAX = 60.0
_CATEGORY_STEP = _CAPACITY_PLOT_W / 10.0
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
    CumulativeLabel(Box(8.417, 2.542, 0.435, 0.269), "135"),
    CumulativeLabel(Box(12.016, 2.542, 0.435, 0.269), "240"),
    CumulativeLabel(Box(9.612, 2.542, 0.435, 0.269), "170"),
    CumulativeLabel(Box(10.809, 2.542, 0.435, 0.269), "205"),
    CumulativeLabel(Box(7.205, 2.542, 0.435, 0.269), "100"),
    CumulativeLabel(Box(2.472, 2.542, 0.279, 0.269), "5"),
    CumulativeLabel(Box(3.646, 2.542, 0.358, 0.269), "23"),
    CumulativeLabel(Box(4.839, 2.542, 0.358, 0.269), "48"),
    CumulativeLabel(Box(6.032, 2.542, 0.358, 0.269), "74"),
)


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
        [_tight_para([_r(text, bold=bold, italic=italic)], align=align)],
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
                width=19_050,
                dashed=True,
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

    for label in ANNUAL_START_LABELS:
        out.append(
            _label_box(
                ids,
                ANNUAL_START_LABEL_ZONE.name,
                label.box,
                label.label,
                align="ctr",
                anchor="b",
                l_ins=17_463,
                r_ins=17_463,
            )
        )


def paint_chrome_and_logos(out: list[str], ids: ShapeIds) -> None:
    out.append(breadcrumb("Golden Dome Requirements", "Production Outlook"))
    out.append(
        title_placeholder(
            "Production Outlook (separate platforms)",
            "All Phase 1 vessels started by FY32, Phase 2 by FY33, and Phase 3 by FY35",
        )
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

    return "".join(out)


def render() -> str:
    return slide(_body())
