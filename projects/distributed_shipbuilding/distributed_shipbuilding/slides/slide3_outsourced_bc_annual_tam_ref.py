"""Production slide module: outsourced basic construction annual TAM reference.

This module rebuilds source slide 3 from the Distributed Shipbuilding New
Construction deck.  The visual contract stays source-faithful, while the code is
organized for agents and humans to inspect in the same order as the exhibit:

    1. native editable chart data and chart style
    2. bottom commentary ledger content
    3. manual chart overlays: retained-spend outlines, labels, legend, and notes
    4. paint functions in PowerPoint z-order

The native chart carries outsourced Basic Construction values plus a transparent
retained-spend scale carrier.  The retained-spend boxes and all chart labels are
manual slide shapes layered over the chart frame.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, paragraph,
    run, table, tcell, tcell_rich, text_box, tpara, trow, trun,
)


# ════════════════════════════════════════════════════════════════════════════
# Slide contract and local palette
# ════════════════════════════════════════════════════════════════════════════
LAYOUT = "slideLayout4"

BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
FONT = "Arial"

COLUMBIA_OUTSOURCED = "1D4D68"
COLUMBIA_OUTSOURCED_ESTIMATE = BLACK
VIRGINIA_OUTSOURCED = "486D82"
VIRGINIA_OUTSOURCED_ESTIMATE = "A1A1A1"
DDG51_OUTSOURCED = "89A2B0"
DDG51_OUTSOURCED_ESTIMATE = "BEBEBE"
RETAINED_SPEND_OUTLINE = DK

SLIDE_METADATA = {
    "role": "supplier_tam_forecast / annual_program_stack",
    "source_deck": "Distributed Shipbuilding New Construction",
    "source_slide": 3,
    "visual_contract": "source-faithful layout with native editable chart rebuild",
    "primary_pattern": "annual program TAM stack with manual retained-spend outlines and penetration ledger",
}

TEXT_FIT = {
    "annual_tam_chart": {
        "box_in": (12.168, 2.701),
        "content": "10 fiscal years × 3 program slots; native category labels hidden",
        "note": "Manual fiscal-year ticks, value labels, and retained-spend outlines sit above the native chart.",
    },
    "commentary_ledger": {
        "box_in": (12.339, 1.554),
        "font_pt": 8,
        "content": "two program-family rows, historical assumptions at left and forecast assumptions at right",
    },
    "penetration_strip": {
        "box_in": (12.694, 1.447),
        "font_pt": "8-8.5",
        "content": "historical ellipse badges plus assumed forecast penetration ranges",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small reusable records
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU at the primitive boundary."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class Insets:
    left: int = 45_720
    top: int = 45_720
    right: int = 45_720
    bottom: int = 45_720

    def kwargs(self) -> dict[str, int]:
        return {
            "l_ins": self.left,
            "t_ins": self.top,
            "r_ins": self.right,
            "b_ins": self.bottom,
        }


@dataclass(frozen=True)
class BorderEdge:
    color: str
    width: int = 12_700

    def dict(self) -> dict[str, str | int]:
        return {"color": self.color, "width": self.width}


class ShapeIds:
    """Sequential body-shape ids; chrome ids are owned by deck_core.chrome."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


ZERO_INSETS = Insets(0, 0, 0, 0)
VALUE_BADGE_INSETS = Insets(17_463, 0, 17_463, 0)
SOURCE_NOTE_INSETS = Insets(91_440, 45_720, 91_440, 45_720)


# ════════════════════════════════════════════════════════════════════════════
# Native chart data and chart specification
# ════════════════════════════════════════════════════════════════════════════
FISCAL_YEARS: tuple[int, ...] = tuple(range(2022, 2032))
PROGRAM_ORDER: tuple[str, ...] = ("DDG-51", "Virginia", "Columbia")


def _program_year_categories() -> tuple[str, ...]:
    """Three program slots per fiscal year plus spacer slots between years."""

    labels: list[str] = []
    for idx, year in enumerate(FISCAL_YEARS):
        labels.extend(f"FY{year} {program}" for program in PROGRAM_ORDER)
        if idx != len(FISCAL_YEARS) - 1:
            labels.append("")
    return tuple(labels)


CHART_CATEGORIES = _program_year_categories()

OUTSOURCED_BC_VALUES: tuple[float | None, ...] = (0.474364998,
 1.779597842,
 None,
 None,
 1.233631888,
 1.853723982,
 None,
 None,
 0.873986645,
 3.207421443,
 1.454272706,
 None,
 1.236388123,
 1.847245459,
 None,
 None,
 1.929240094,
 1.976853214,
 1.57514896,
 None,
 0.674117932,
 2.961918092,
 1.477664835,
 None,
 0.57735821,
 2.724439839400433,
 1.3594178717035803,
 None,
 0.61374443,
 2.8014719698262818,
 1.4527277602531905,
 None,
 0.98094076,
 2.6898411862948204,
 1.5299265978967191,
 None,
 1.05152976,
 2.9193127223,
 1.6367105235000001)

RETAINED_SPEND_VALUES: tuple[float | None, ...] = (4.0058052019999995,
 5.827734858,
 None,
 None,
 7.272375912000001,
 5.904395548,
 None,
 None,
 4.838036555,
 8.625327277,
 9.662090734,
 None,
 6.779602157,
 7.8432992210000005,
 None,
 None,
 3.7768849060000003,
 8.012255786,
 9.16916804,
 None,
 3.497657788,
 8.246377188,
 8.798976785,
 None,
 3.287794751642135,
 8.108991216542005,
 8.372177031450153,
 None,
 3.3431291679445443,
 7.631048484888731,
 8.286610386118376,
 None,
 5.1031581608136305,
 6.691042786981166,
 8.075794349527223,
 None,
 5.216266439324437,
 6.615494289463112,
 7.987063299792535)

PROGRAM_POINT_COLORS = {
    "DDG-51": (DDG51_OUTSOURCED, DDG51_OUTSOURCED_ESTIMATE),
    "Virginia": (VIRGINIA_OUTSOURCED, VIRGINIA_OUTSOURCED_ESTIMATE),
    "Columbia": (COLUMBIA_OUTSOURCED, COLUMBIA_OUTSOURCED_ESTIMATE),
}


def _outsourced_point_colors() -> tuple[str | None, ...]:
    """Per-category point fills: known-budget years through FY2027, estimates from FY2028."""

    colors: list[str | None] = []
    for category, value in zip(CHART_CATEGORIES, OUTSOURCED_BC_VALUES):
        if value is None or not category:
            colors.append(None)
            continue
        year = int(category[2:6])
        program = category.split(" ", 1)[1]
        actual, estimate = PROGRAM_POINT_COLORS[program]
        colors.append(actual if year <= 2027 else estimate)
    return tuple(colors)


OUTSOURCED_POINT_COLORS = _outsourced_point_colors()

SOURCE_PLOT_LAYOUT = {
    "x": 0.033385647025253248,
    "y": 0.091259640102827763,
    "w": 0.95919532030246824,
    "h": 0.81748071979434445,
}
SOURCE_GAP_WIDTH = 0
SOURCE_BAR_OVERLAP = 100
SOURCE_VALUE_AXIS_MAJOR_UNIT = 5
SOURCE_AXIS_LINE_WIDTH = 9_525
SOURCE_VALUE_AXIS_FORMAT = '#,##0;"-"#,##0'

_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": [
        {"name": "Outsourced Basic Construction", "values": list(OUTSOURCED_BC_VALUES)},
        {"name": "Retained spend", "values": list(RETAINED_SPEND_VALUES)},
    ],
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [
        {
            "name": "Outsourced Basic Construction",
            "color": VIRGINIA_OUTSOURCED,
            "data_point_colors": list(OUTSOURCED_POINT_COLORS),
            "values": list(OUTSOURCED_BC_VALUES),
            "hide_labels": True,
        },
        {
            "name": "Retained spend / scale carrier",
            "values": list(RETAINED_SPEND_VALUES),
            "no_fill": True,
            "hide_labels": True,
        },
    ],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": SOURCE_VALUE_AXIS_FORMAT,
    "value_label_format": '#,##0.0;"-"#,##0.0',
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "cat_label_size_pt": 10,
    "gap_width": SOURCE_GAP_WIDTH,
    "bar_overlap": SOURCE_BAR_OVERLAP,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": SOURCE_AXIS_LINE_WIDTH,
    "value_axis_min": 0,
    "value_axis_major_unit": SOURCE_VALUE_AXIS_MAJOR_UNIT,
    "cat_axis_crosses": "min",
    "value_axis_crosses": "min",
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
    "cat_header": "Program / fiscal year",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Local table helpers
# ════════════════════════════════════════════════════════════════════════════
PAD = dict(l_ins=60_960, r_ins=60_960, t_ins=60_960, b_ins=60_960)


def edge(color: str, w: int = 12_700) -> dict[str, str | int]:
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(
    text: str = "",
    *,
    fill=None,
    bold=None,
    italic=None,
    color=BLACK,
    size=PT(10),
    align="l",
    anchor="ctr",
    vert=None,
    span=1,
    rowspan=1,
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    return tcell(
        text,
        fill=fill,
        bold=bold,
        italic=italic,
        color=color,
        size=size,
        align=align,
        anchor=anchor,
        vert=vert,
        grid_span=span,
        row_span=rowspan,
        font=FONT,
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=bd(**edges),
    )


def rcell(
    paras,
    *,
    fill=None,
    anchor="ctr",
    vert=None,
    span=1,
    rowspan=1,
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    return tcell_rich(
        paras,
        fill=fill,
        grid_span=span,
        row_span=rowspan,
        anchor=anchor,
        vert=vert,
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=bd(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Commentary ledger table data
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class CellRun:
    text: str
    size_pt: float = 8
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = BLACK

    def emit(self):
        return trun(
            self.text,
            size=PT(self.size_pt),
            bold=self.bold or None,
            italic=self.italic or None,
            underline=self.underline or None,
            color=self.color,
            font=FONT,
        )


@dataclass(frozen=True)
class CellParagraph:
    runs: tuple[CellRun, ...]
    line_spacing: int = 115_000

    def emit(self):
        return tpara([r.emit() for r in self.runs], line_spacing=self.line_spacing)


@dataclass(frozen=True)
class CommentaryRow:
    program: str
    row_h: float
    border_side: str
    current_period_paragraphs: tuple[CellParagraph, ...]
    forecast_period_paragraphs: tuple[CellParagraph, ...]


def CR(text: str, *, bold: bool = False, italic: bool = False, underline: bool = False) -> CellRun:
    return CellRun(text, bold=bold, italic=italic, underline=underline)


def CP(*runs: CellRun) -> CellParagraph:
    return CellParagraph(tuple(runs))


COMMENTARY_ROWS: tuple[CommentaryRow, ...] = (
    CommentaryRow(
        program="Submarines",
        row_h=0.671,
        border_side="B",
        current_period_paragraphs=(
            CP(
                CR("Total Funding:", bold=True, underline=True),
                CR(" "),
                CR("Virginia", italic=True),
                CR(" funds annually (2/yr; 1x in FY25); "),
                CR("Columbia", italic=True),
                CR(" funds biennially (FY24 in window)"),
            ),
            CP(
                CR("Outsourcing:", bold=True, underline=True),
                CR(" "),
                CR("Virginia", italic=True),
                CR(" outsourced ~19-27% per year (FY22-25 avg. ~24%); "),
                CR("Columbia", italic=True),
                CR(" ~13% (FY24)"),
            ),
        ),
        forecast_period_paragraphs=(
            CP(
                CR("Total Funding:", bold=True, underline=True),
                CR(" OBBBA adds $4.6B for a second "),
                CR("Virginia", italic=True),
                CR(" in FY26 (Sec. 20002(16)); FYDP calls for 1x "),
                CR("Columbia", italic=True),
                CR(" p.a. from FY26 and 2x "),
                CR("Virginia", italic=True),
                CR(" p.a. from FY27"),
            ),
            CP(
                CR("Outsourcing:", bold=True, underline=True),
                CR(" Lower bound reflects FY22–25 avg. rate; Upper bound assumes penetration grows ~1.8 ppts p.a. for "),
                CR("Virginia", italic=True),
                CR(" and ~1.0 ppts p.a. for "),
                CR("Columbia", italic=True),
                CR(" (~7% CAGR), towards ~31% ("),
                CR("Virginia", italic=True),
                CR(") / ~17% ("),
                CR("Columbia", italic=True),
                CR(") targets, driven by “strategically outsourcing workload to qualified suppliers” (PB27 SCN, Columbia P-10)"),
            ),
        ),
    ),
    CommentaryRow(
        program="DDG-51",
        row_h=0.592,
        border_side="T",
        current_period_paragraphs=(
            CP(CR("Total Funding:", bold=True, underline=True), CR(" Procuring at 2-3x per year")),
            CP(
                CR("Outsourcing:", bold=True, underline=True),
                CR(" Outsourced 11-15% per year (FY22–25 avg. ~14%)"),
            ),
        ),
        forecast_period_paragraphs=(
            CP(
                CR("Total Funding:", bold=True, underline=True),
                CR(" OBBBA adds $5.4B for two additional DDG-51s in FY26 (Sec. 20002(17)); FYDP calls for ~1.5-ship buys p.a. FY27-FY31"),
            ),
            CP(
                CR("Outsourcing:", bold=True, underline=True),
                CR(" FY26 spike driven by OBBBA-related EOQ AP/LLTM (vendor-purchased LLTM bought ahead of the FY27-31 ramp flows almost entirely to suppliers); FY27–31 lower bound reflects FY22–25 avg. rate (i.e., reversion to mean); FY27-31 upper bound assumes ~1.1 ppts p.a. (~7% CAGR) towards a ~19% target using FY22-25 avg. as baseline, driven by stated intent to grow outsourced manhours ~30%"),
            ),
        ),
    ),
)

COMMENTARY_TABLE = Box(0.495, 5.464, 12.339, 1.554)
COMMENTARY_COL_WIDTHS = (0.841, 4.315, 7.182)
COMMENTARY_RULE = BorderEdge(BLACK, 9_525)


def _commentary_border_kwargs(row: CommentaryRow) -> dict:
    return {row.border_side: COMMENTARY_RULE.dict()}


def _commentary_row(row: CommentaryRow):
    rule = _commentary_border_kwargs(row)
    return trow(
        [
            cell(row.program, size=PT(8), bold=True, color=BLACK, **rule),
            rcell([p.emit() for p in row.current_period_paragraphs], **rule),
            rcell([p.emit() for p in row.forecast_period_paragraphs], **rule),
        ],
        h=IN(row.row_h),
    )


# ════════════════════════════════════════════════════════════════════════════
# Manual chart overlays and body labels
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class ChartFrame:
    name: str
    r_id: str
    box: Box


@dataclass(frozen=True)
class GuideRule:
    name: str
    box: Box
    width: int
    source_name: str
    color: str = RETAINED_SPEND_OUTLINE
    dash: str = "lgDash"


@dataclass(frozen=True)
class RetainedSpendOutlineBox:
    label: str
    box: Box
    line_width: int = 12_700


@dataclass(frozen=True)
class YearTick:
    label: str
    x: float


@dataclass(frozen=True)
class ValueBadge:
    label: str
    box: Box
    fill: str
    text_color: str | None


@dataclass(frozen=True)
class RetainedSpendLabel:
    label: str
    box: Box


@dataclass(frozen=True)
class PenetrationBadge:
    label: str
    box: Box
    prst: str
    geom_adj: dict[str, str] | None = None


@dataclass(frozen=True)
class LegendSwatch:
    box: Box
    fill: str


@dataclass(frozen=True)
class TextLabel:
    text: str
    box: Box
    font_pt: float
    bold: bool = False
    italic: bool = False
    align: str | None = None


CHART_FRAME = ChartFrame("AnnualTAMChart", "rId2", Box(0.707, 1.722, 12.168, 2.701))
CHART_TITLE = TextLabel(
    "Outsourced Basic Construction TAM ($B, FY26 $)",
    Box(0.819, 1.441, 3.257, 0.333),
    font_pt=10,
    bold=True,
)
SOURCE_NOTES = (
    TextLabel(
        "Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and PB27 FYDP outyears (FY28–FY31); FY26, PL 119-21 Sec. 20002; OUSD(C) Green Book Procurement deflators; Navy Shipbuilding Plan; HII FY24 Q3 / FY25 Q4 / FY26 Q1 earnings calls",
        Box(0.495, 6.978, 5.064, 0.511),
        font_pt=8,
    ),
)
FORECAST_REGION = TextLabel("Forecasted", Box(5.626, 1.857, 7.292, 3.559), font_pt=9, bold=True, italic=True, align="ctr")

PRE_FORECAST_OUTLINE_RULES: tuple[GuideRule, ...] = (
    GuideRule("RetainedSpendOutlineRule01", Box(12.486, 2.76, 0.299, 0.0), width=3175, source_name="Straight Connector 933"),
    GuideRule("RetainedSpendOutlineRule02", Box(12.486, 3.936, 0.299, 0.0), width=3175, source_name="Straight Connector 934"),
    GuideRule("RetainedSpendOutlineRule03", Box(12.486, 3.747, 0.0, 0.189), width=3175, source_name="Straight Connector 948"),
    GuideRule("RetainedSpendOutlineRule04", Box(12.486, 2.76, 0.0, 0.012), width=3175, source_name="Straight Connector 935"),
    GuideRule("RetainedSpendOutlineRule05", Box(12.785, 2.76, 0.0, 1.175), width=3175, source_name="Straight Connector 936"),
    GuideRule("RetainedSpendOutlineRule06", Box(12.186, 2.773, 0.3, 0.0), width=6350, source_name="Straight Connector 1068"),
    GuideRule("RetainedSpendOutlineRule07", Box(12.186, 3.747, 0.3, 0.0), width=6350, source_name="Straight Connector 1069"),
    GuideRule("RetainedSpendOutlineRule08", Box(12.186, 2.773, 0.0, 0.481), width=6350, source_name="Straight Connector 1070"),
    GuideRule("RetainedSpendOutlineRule09", Box(12.486, 2.773, 0.0, 0.974), width=6350, source_name="Straight Connector 1071"),
)

DDG_RETAINED_SPEND_OUTLINE_BOXES: tuple[RetainedSpendOutlineBox, ...] = (
    RetainedSpendOutlineBox("FY2031 DDG-51 retained spend", Box(11.887, 3.253, 0.299, 0.752)),
    RetainedSpendOutlineBox("FY2030 DDG-51 retained spend", Box(10.689, 3.281, 0.3, 0.74)),
    RetainedSpendOutlineBox("FY2029 DDG-51 retained spend", Box(9.493, 3.594, 0.299, 0.488)),
    RetainedSpendOutlineBox("FY2028 DDG-51 retained spend", Box(8.295, 3.608, 0.3, 0.483)),
    RetainedSpendOutlineBox("FY2027 DDG-51 retained spend", Box(7.099, 3.562, 0.299, 0.516)),
    RetainedSpendOutlineBox("FY2026 DDG-51 retained spend", Box(5.901, 3.337, 0.3, 0.556)),
    RetainedSpendOutlineBox("FY2025 DDG-51 retained spend", Box(4.705, 2.997, 0.299, 0.998)),
    RetainedSpendOutlineBox("FY2024 DDG-51 retained spend", Box(3.507, 3.337, 0.299, 0.712)),
    RetainedSpendOutlineBox("FY2023 DDG-51 retained spend", Box(2.311, 2.925, 0.299, 1.069)),
    RetainedSpendOutlineBox("FY2022 DDG-51 retained spend", Box(1.113, 3.517, 0.299, 0.59)),
)
DDG_RETAINED_SPEND_LEGEND_SWATCH = RetainedSpendOutlineBox("DDG-51 retained spend legend swatch", Box(11.023, 1.674, 0.156, 0.116))

POST_FORECAST_OUTLINE_RULES: tuple[GuideRule, ...] = (
    GuideRule("RetainedSpendOutlineRule10", Box(11.288, 2.762, 0.299, 0.0), width=3175, source_name="Straight Connector 929"),
    GuideRule("RetainedSpendOutlineRule11", Box(11.288, 3.951, 0.299, 0.0), width=3175, source_name="Straight Connector 930"),
    GuideRule("RetainedSpendOutlineRule12", Box(11.288, 2.762, 0.0, 0.035), width=3175, source_name="Straight Connector 931"),
    GuideRule("RetainedSpendOutlineRule13", Box(11.288, 3.781, 0.0, 0.17), width=3175, source_name="Straight Connector 947"),
    GuideRule("RetainedSpendOutlineRule14", Box(11.587, 2.762, 0.0, 1.189), width=3175, source_name="Straight Connector 932"),
    GuideRule("RetainedSpendOutlineRule15", Box(10.99, 2.797, 0.299, 0.0), width=6350, source_name="Straight Connector 1063"),
    GuideRule("RetainedSpendOutlineRule16", Box(10.99, 2.797, 0.0, 0.484), width=6350, source_name="Straight Connector 1065"),
    GuideRule("RetainedSpendOutlineRule17", Box(11.288, 2.797, 0.0, 0.984), width=6350, source_name="Straight Connector 1066"),
    GuideRule("RetainedSpendOutlineRule18", Box(10.99, 3.781, 0.299, 0.0), width=6350, source_name="Straight Connector 1064"),
    GuideRule("RetainedSpendOutlineRule19", Box(10.092, 2.743, 0.299, 0.0), width=3175, source_name="Straight Connector 926"),
    GuideRule("RetainedSpendOutlineRule20", Box(10.092, 3.964, 0.299, 0.0), width=3175, source_name="Straight Connector 927"),
    GuideRule("RetainedSpendOutlineRule21", Box(10.092, 3.764, 0.0, 0.2), width=3175, source_name="Straight Connector 946"),
    GuideRule("RetainedSpendOutlineRule22", Box(10.391, 2.743, 0.0, 1.22), width=3175, source_name="Straight Connector 928"),
    GuideRule("RetainedSpendOutlineRule23", Box(9.792, 2.641, 0.3, 0.0), width=6350, source_name="Straight Connector 1058"),
    GuideRule("RetainedSpendOutlineRule24", Box(9.792, 3.764, 0.3, 0.0), width=6350, source_name="Straight Connector 1059"),
    GuideRule("RetainedSpendOutlineRule25", Box(9.792, 2.641, 0.0, 0.953), width=6350, source_name="Straight Connector 1060"),
    GuideRule("RetainedSpendOutlineRule26", Box(10.092, 2.641, 0.0, 1.123), width=6350, source_name="Straight Connector 1061"),
    GuideRule("RetainedSpendOutlineRule27", Box(9.193, 2.745, 0.0, 1.233), width=3175, source_name="Straight Connector 925"),
    GuideRule("RetainedSpendOutlineRule28", Box(8.894, 3.776, 0.0, 0.201), width=3175, source_name="Straight Connector 945"),
    GuideRule("RetainedSpendOutlineRule29", Box(8.894, 3.977, 0.299, 0.0), width=3175, source_name="Straight Connector 924"),
    GuideRule("RetainedSpendOutlineRule30", Box(8.894, 2.745, 0.299, 0.0), width=3175, source_name="Straight Connector 923"),
    GuideRule("RetainedSpendOutlineRule31", Box(8.894, 2.582, 0.0, 1.194), width=6350, source_name="Straight Connector 1056"),
    GuideRule("RetainedSpendOutlineRule32", Box(8.595, 2.582, 0.0, 1.026), width=6350, source_name="Straight Connector 1055"),
    GuideRule("RetainedSpendOutlineRule33", Box(8.595, 3.776, 0.299, 0.0), width=6350, source_name="Straight Connector 1054"),
    GuideRule("RetainedSpendOutlineRule34", Box(8.595, 2.582, 0.299, 0.0), width=6350, source_name="Straight Connector 1053"),
    GuideRule("RetainedSpendOutlineRule35", Box(7.696, 3.96, 0.3, 0.0), width=3175, source_name="Straight Connector 921"),
    GuideRule("RetainedSpendOutlineRule36", Box(7.696, 3.741, 0.0, 0.219), width=3175, source_name="Straight Connector 942"),
    GuideRule("RetainedSpendOutlineRule37", Box(7.997, 2.665, 0.0, 1.295), width=3175, source_name="Straight Connector 922"),
    GuideRule("RetainedSpendOutlineRule38", Box(7.696, 2.665, 0.3, 0.0), width=3175, source_name="Straight Connector 920"),
    GuideRule("RetainedSpendOutlineRule39", Box(7.696, 2.528, 0.0, 1.214), width=6350, source_name="Straight Connector 1051"),
    GuideRule("RetainedSpendOutlineRule40", Box(7.398, 2.528, 0.0, 1.035), width=6350, source_name="Straight Connector 1050"),
    GuideRule("RetainedSpendOutlineRule41", Box(7.398, 3.741, 0.299, 0.0), width=6350, source_name="Straight Connector 1049"),
    GuideRule("RetainedSpendOutlineRule42", Box(7.398, 2.528, 0.299, 0.0), width=6350, source_name="Straight Connector 1048"),
    GuideRule("RetainedSpendOutlineRule43", Box(6.799, 2.595, 0.0, 1.349), width=3175, source_name="Straight Connector 919"),
    GuideRule("RetainedSpendOutlineRule44", Box(6.5, 3.885, 0.0, 0.059), width=3175, source_name="Straight Connector 941"),
    GuideRule("RetainedSpendOutlineRule45", Box(6.5, 2.595, 0.0, 0.111), width=3175, source_name="Straight Connector 918"),
    GuideRule("RetainedSpendOutlineRule46", Box(6.5, 3.944, 0.299, 0.0), width=3175, source_name="Straight Connector 917"),
    GuideRule("RetainedSpendOutlineRule47", Box(6.5, 2.595, 0.299, 0.0), width=3175, source_name="Straight Connector 916"),
    GuideRule("RetainedSpendOutlineRule48", Box(6.201, 2.707, 0.299, 0.0), width=6350, source_name="Straight Connector 1043"),
    GuideRule("RetainedSpendOutlineRule49", Box(6.201, 3.885, 0.299, 0.0), width=6350, source_name="Straight Connector 1044"),
    GuideRule("RetainedSpendOutlineRule50", Box(6.5, 2.707, 0.0, 1.179), width=6350, source_name="Straight Connector 1046"),
    GuideRule("RetainedSpendOutlineRule51", Box(6.201, 2.707, 0.0, 0.63), width=6350, source_name="Straight Connector 1045"),
    GuideRule("RetainedSpendOutlineRule52", Box(5.003, 3.905, 0.299, 0.0), width=6350, source_name="Straight Connector 1010"),
    GuideRule("RetainedSpendOutlineRule53", Box(5.003, 2.75, 0.0, 0.247), width=6350, source_name="Straight Connector 1011"),
    GuideRule("RetainedSpendOutlineRule54", Box(5.302, 2.75, 0.0, 1.155), width=6350, source_name="Straight Connector 1012"),
    GuideRule("RetainedSpendOutlineRule55", Box(5.003, 2.75, 0.299, 0.0), width=6350, source_name="Straight Connector 1009"),
    GuideRule("RetainedSpendOutlineRule56", Box(4.106, 2.54, 0.299, 0.0), width=3175, source_name="Straight Connector 913"),
    GuideRule("RetainedSpendOutlineRule57", Box(4.106, 3.964, 0.299, 0.0), width=3175, source_name="Straight Connector 914"),
    GuideRule("RetainedSpendOutlineRule58", Box(4.106, 3.705, 0.0, 0.259), width=3175, source_name="Straight Connector 940"),
    GuideRule("RetainedSpendOutlineRule59", Box(4.405, 2.54, 0.0, 1.424), width=3175, source_name="Straight Connector 915"),
    GuideRule("RetainedSpendOutlineRule60", Box(3.806, 2.436, 0.3, 0.0), width=6350, source_name="Straight Connector 994"),
    GuideRule("RetainedSpendOutlineRule61", Box(3.806, 2.436, 0.0, 0.901), width=6350, source_name="Straight Connector 999"),
    GuideRule("RetainedSpendOutlineRule62", Box(4.106, 2.436, 0.0, 1.269), width=6350, source_name="Straight Connector 1003"),
    GuideRule("RetainedSpendOutlineRule63", Box(3.806, 3.705, 0.3, 0.0), width=6350, source_name="Straight Connector 998"),
    GuideRule("RetainedSpendOutlineRule64", Box(2.908, 3.035, 0.0, 0.87), width=6350, source_name="Straight Connector 963"),
    GuideRule("RetainedSpendOutlineRule65", Box(2.609, 3.905, 0.299, 0.0), width=6350, source_name="Straight Connector 962"),
    GuideRule("RetainedSpendOutlineRule66", Box(2.609, 3.035, 0.299, 0.0), width=6350, source_name="Straight Connector 961"),
    GuideRule("RetainedSpendOutlineRule67", Box(1.411, 3.057, 0.3, 0.0), width=6350, source_name="Straight Connector 953"),
    GuideRule("RetainedSpendOutlineRule68", Box(1.411, 3.915, 0.3, 0.0), width=6350, source_name="Straight Connector 954"),
    GuideRule("RetainedSpendOutlineRule69", Box(1.411, 3.057, 0.0, 0.46), width=6350, source_name="Straight Connector 957"),
    GuideRule("RetainedSpendOutlineRule70", Box(1.712, 3.057, 0.0, 0.858), width=6350, source_name="Straight Connector 959"),
)

YEAR_TICKS: tuple[YearTick, ...] = (
    YearTick("FY2022", x=1.312),
    YearTick("FY2023", x=2.51),
    YearTick("FY2026", x=6.102),
    YearTick("FY2025", x=4.905),
    YearTick("FY2030", x=10.891),
    YearTick("FY2031", x=12.087),
    YearTick("FY2029", x=9.693),
    YearTick("FY2027", x=7.299),
    YearTick("FY2028", x=8.497),
    YearTick("FY2024", x=3.707),
)

OUTSOURCED_ACTUAL_VALUE_BADGES: tuple[ValueBadge, ...] = (
    ValueBadge("0.5", Box(1.148, 4.059, 0.229, 0.167), fill=DDG51_OUTSOURCED, text_color=WHITE),
    ValueBadge("0.7", Box(7.134, 4.043, 0.229, 0.167), fill=DDG51_OUTSOURCED, text_color=WHITE),
    ValueBadge("0.9", Box(3.542, 4.03, 0.229, 0.167), fill=DDG51_OUTSOURCED, text_color=WHITE),
)

OUTSOURCED_ESTIMATE_VALUE_BADGES: tuple[ValueBadge, ...] = (
    ValueBadge("0.6", Box(9.528, 4.045, 0.229, 0.167), fill=DDG51_OUTSOURCED_ESTIMATE, text_color=None),
    ValueBadge("0.6", Box(8.33, 4.05, 0.229, 0.167), fill=DDG51_OUTSOURCED_ESTIMATE, text_color=None),
)

RETAINED_SPEND_VALUE_LABELS: tuple[RetainedSpendLabel, ...] = (
    RetainedSpendLabel("4.5", Box(1.148, 3.323, 0.229, 0.167)),
    RetainedSpendLabel("7.6", Box(1.446, 2.863, 0.229, 0.167)),
    RetainedSpendLabel("8.5", Box(2.345, 2.731, 0.229, 0.167)),
    RetainedSpendLabel("7.8", Box(2.644, 2.84, 0.229, 0.167)),
    RetainedSpendLabel("5.7", Box(3.542, 3.142, 0.229, 0.167)),
    RetainedSpendLabel("11.8", Box(3.802, 2.241, 0.306, 0.167)),
    RetainedSpendLabel("11.1", Box(4.102, 2.345, 0.306, 0.167)),
    RetainedSpendLabel("8.0", Box(4.74, 2.802, 0.229, 0.167)),
    RetainedSpendLabel("9.7", Box(5.038, 2.556, 0.229, 0.167)),
    RetainedSpendLabel("5.7", Box(5.936, 3.142, 0.229, 0.167)),
    RetainedSpendLabel("10.0", Box(6.198, 2.512, 0.306, 0.167)),
    RetainedSpendLabel("10.7", Box(6.497, 2.401, 0.306, 0.167)),
    RetainedSpendLabel("4.2", Box(7.134, 3.368, 0.229, 0.167)),
    RetainedSpendLabel("10.3", Box(7.693, 2.47, 0.306, 0.167)),
    RetainedSpendLabel("3.9", Box(8.33, 3.413, 0.229, 0.167)),
    RetainedSpendLabel("10.8", Box(8.592, 2.387, 0.306, 0.167)),
    RetainedSpendLabel("9.7", Box(8.929, 2.55, 0.229, 0.167)),
    RetainedSpendLabel("4.0", Box(9.528, 3.399, 0.229, 0.167)),
    RetainedSpendLabel("10.4", Box(9.788, 2.446, 0.306, 0.167)),
    RetainedSpendLabel("9.7", Box(10.127, 2.549, 0.229, 0.167)),
    RetainedSpendLabel("6.1", Box(10.724, 3.087, 0.229, 0.167)),
    RetainedSpendLabel("9.4", Box(11.024, 2.602, 0.229, 0.167)),
    RetainedSpendLabel("9.6", Box(11.323, 2.568, 0.229, 0.167)),
    RetainedSpendLabel("6.3", Box(11.922, 3.059, 0.229, 0.167)),
    RetainedSpendLabel("9.5", Box(12.22, 2.578, 0.229, 0.167)),
    RetainedSpendLabel("9.6", Box(12.521, 2.566, 0.229, 0.167)),
    RetainedSpendLabel("11.2", Box(7.394, 2.333, 0.306, 0.167)),
)

HISTORICAL_PENETRATION_BADGES: tuple[PenetrationBadge, ...] = (
    PenetrationBadge("$2.3B", Box(1.274, 1.965, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("$3.1B", Box(2.47, 1.975, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("$5.5B", Box(3.666, 1.965, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("$3.1B", Box(4.85, 1.949, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("11%", Box(1.274, 4.504, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("15%", Box(2.47, 4.504, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("15%", Box(3.666, 4.504, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("15%", Box(4.85, 4.504, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("34%", Box(6.058, 4.504, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("23%", Box(1.274, 4.761, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("24%", Box(2.47, 4.761, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("27%", Box(3.666, 4.761, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("19%", Box(4.862, 4.761, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("20%", Box(6.058, 4.761, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("n/a", Box(1.274, 5.018, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("n/a", Box(2.47, 5.018, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("13%", Box(3.666, 5.018, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("n/a", Box(4.862, 5.018, 0.569, 0.191), prst="ellipse"),
    PenetrationBadge("15%", Box(6.058, 5.018, 0.569, 0.191), prst="ellipse"),
)

OUTSOURCED_LEGEND_SWATCHES: tuple[LegendSwatch, ...] = (
    LegendSwatch(Box(7.795, 1.295, 0.156, 0.116), fill=COLUMBIA_OUTSOURCED),
    LegendSwatch(Box(7.795, 1.484, 0.156, 0.116), fill=BLACK),
    LegendSwatch(Box(9.458, 1.295, 0.156, 0.116), fill=VIRGINIA_OUTSOURCED),
    LegendSwatch(Box(9.458, 1.484, 0.156, 0.116), fill=VIRGINIA_OUTSOURCED_ESTIMATE),
    LegendSwatch(Box(11.023, 1.295, 0.156, 0.116), fill=DDG51_OUTSOURCED),
    LegendSwatch(Box(11.023, 1.484, 0.156, 0.116), fill=DDG51_OUTSOURCED_ESTIMATE),
)

RETAINED_LEGEND_SWATCHES: tuple[RetainedSpendOutlineBox, ...] = (
    RetainedSpendOutlineBox("Columbia retained spend legend swatch", Box(7.795, 1.674, 0.156, 0.116), line_width=3_175),
    RetainedSpendOutlineBox("Virginia retained spend legend swatch", Box(9.458, 1.674, 0.156, 0.116), line_width=6_350),
)

LEGEND_LABELS: tuple[TextLabel, ...] = (
    TextLabel("Columbia outsourced", Box(8.007, 1.29, 1.056, 0.134), font_pt=8),
    TextLabel("Columbia outsourced (est.)", Box(8.007, 1.479, 1.34, 0.134), font_pt=8),
    TextLabel("Columbia retained spend", Box(8.007, 1.668, 1.243, 0.134), font_pt=8),
    TextLabel("Virginia outsourced", Box(9.67, 1.29, 0.957, 0.134), font_pt=8),
    TextLabel("Virginia outsourced (est.)", Box(9.67, 1.479, 1.241, 0.134), font_pt=8),
    TextLabel("Virginia retained spend", Box(9.67, 1.668, 1.144, 0.134), font_pt=8),
    TextLabel("DDG-51 outsourced", Box(11.234, 1.29, 0.993, 0.134), font_pt=8),
    TextLabel("DDG-51 outsourced (est.)", Box(11.234, 1.479, 1.278, 0.134), font_pt=8),
    TextLabel("DDG-51 retained spend", Box(11.234, 1.668, 1.181, 0.134), font_pt=8),
)

PENETRATION_STRIP_HEADER = TextLabel(
    "Outsourced penetration %",
    Box(0.164, 4.037, 0.275, 1.447),
    font_pt=8,
    bold=True,
    italic=True,
    align="l",
)

PENETRATION_ROW_LABELS: tuple[TextLabel, ...] = (
    TextLabel("DDG-51 %", Box(0.011, 4.479, 1.068, 0.241), font_pt=8, bold=True, italic=True, align="r"),
    TextLabel("Virginia %", Box(0.011, 4.736, 1.068, 0.241), font_pt=8, bold=True, italic=True, align="r"),
    TextLabel("Columbia %", Box(0.011, 4.993, 1.068, 0.241), font_pt=8, bold=True, italic=True, align="r"),
)

FORECAST_PENETRATION_BADGES: tuple[PenetrationBadge, ...] = (
    PenetrationBadge("14–19% (assumed)", Box(7.123, 4.504, 5.582, 0.191), prst="roundRect", geom_adj={"adj": "val 50000"}),
    PenetrationBadge("24–31% (assumed)", Box(7.123, 4.761, 5.582, 0.191), prst="roundRect", geom_adj={"adj": "val 50000"}),
    PenetrationBadge("13–17% (assumed)", Box(7.123, 5.018, 5.582, 0.191), prst="roundRect", geom_adj={"adj": "val 50000"}),
)

CHART_FOOTNOTES: tuple[TextLabel, ...] = (
    TextLabel(
        "Note: Columbia had no hull authorized in FY22/23/25 (hull costs shown in year of authorization)",
        Box(0.445, 5.283, 4.9, 0.131),
        font_pt=8,
        italic=True,
        align="l",
    ),
    TextLabel(
        "FY26/FY27 budgets known, penetration assumed.",
        Box(5.431, 5.25, 3.062, 0.131),
        font_pt=8,
        italic=True,
        align="ctr",
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Paint helpers.  Each function appends shapes in PowerPoint z-order.
# ════════════════════════════════════════════════════════════════════════════
def _paint_commentary_table(out: list[str], ids: ShapeIds) -> None:
    out.append(table(
        ids.next(),
        "BandCommentary",
        *COMMENTARY_TABLE.emu(),
        col_widths=[IN(w) for w in COMMENTARY_COL_WIDTHS],
        rows=[_commentary_row(row) for row in COMMENTARY_ROWS],
    ))


def _paint_chart_frame(out: list[str], ids: ShapeIds) -> None:
    out.append(graphic_frame(
        sp_id=ids.next(),
        name=CHART_FRAME.name,
        x=CHART_FRAME.box.emu()[0],
        y=CHART_FRAME.box.emu()[1],
        cx=CHART_FRAME.box.emu()[2],
        cy=CHART_FRAME.box.emu()[3],
        rId=CHART_FRAME.r_id,
    ))


def _paint_chart_title(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(),
        "ChartTitle",
        *CHART_TITLE.box.emu(),
        [
            paragraph(
                [run(CHART_TITLE.text, size=PT(CHART_TITLE.font_pt), bold=True, color=BLACK, font=FONT)],
                mar_l=0,
                indent=0,
                line_spacing=100_000,
            ),
            paragraph([], mar_l=0, indent=0, line_spacing=100_000),
        ],
        fill=None,
        line_color="none",
        anchor="b",
        wrap="none",
        vert="horz",
        **ZERO_INSETS.kwargs(),
    ))


def _paint_source_notes(out: list[str], ids: ShapeIds) -> None:
    for note in SOURCE_NOTES:
        out.append(text_box(
            ids.next(),
            "Sources",
            *note.box.emu(),
            [paragraph([run(note.text, size=PT(note.font_pt), color=DK, font=FONT)], line_spacing=100_000)],
            fill=None,
            line_color="none",
            **SOURCE_NOTE_INSETS.kwargs(),
        ))


def _paint_forecast_region(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(),
        "ForecastRegionFrame",
        *FORECAST_REGION.box.emu(),
        [paragraph([run(FORECAST_REGION.text, size=PT(FORECAST_REGION.font_pt), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=None,
        line_color=BLACK,
        dashed_line=True,
        **ZERO_INSETS.kwargs(),
    ))


def _draw_guide_rule(out: list[str], ids: ShapeIds, rule: GuideRule) -> None:
    out.append(connector(
        ids.next(),
        rule.name,
        *rule.box.emu(),
        color=rule.color,
        width=rule.width,
        dash=rule.dash,
    ))


def _draw_retained_outline_box(out: list[str], ids: ShapeIds, spec: RetainedSpendOutlineBox) -> None:
    out.append(text_box(
        ids.next(),
        "RetainedSpendOutlineBox",
        *spec.box.emu(),
        [paragraph([], align="ctr", line_spacing=100_000)],
        fill=None,
        line_color=RETAINED_SPEND_OUTLINE,
        line_width=spec.line_width,
        dashed_line=True,
        anchor="ctr",
    ))


def _paint_retained_spend_outlines(out: list[str], ids: ShapeIds) -> None:
    # The source paints the far-right connector fragments first, then the DDG-51
    # retained-spend outline boxes, then the remaining connector fragments.
    for rule in PRE_FORECAST_OUTLINE_RULES:
        _draw_guide_rule(out, ids, rule)
    for box in DDG_RETAINED_SPEND_OUTLINE_BOXES:
        _draw_retained_outline_box(out, ids, box)
    _draw_retained_outline_box(out, ids, DDG_RETAINED_SPEND_LEGEND_SWATCH)
    for rule in POST_FORECAST_OUTLINE_RULES:
        _draw_guide_rule(out, ids, rule)


def _paint_year_ticks(out: list[str], ids: ShapeIds) -> None:
    for tick in YEAR_TICKS:
        out.append(text_box(
            ids.next(),
            "YearTick",
            *Box(tick.x, 4.273, 0.497, 0.167).emu(),
            [paragraph([run(tick.label, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=None,
            line_color="none",
            wrap="none",
            vert="horz",
            **ZERO_INSETS.kwargs(),
        ))


def _paint_outsourced_value_badges(out: list[str], ids: ShapeIds) -> None:
    for badge in OUTSOURCED_ACTUAL_VALUE_BADGES + OUTSOURCED_ESTIMATE_VALUE_BADGES:
        out.append(text_box(
            ids.next(),
            "OutsourcedValueBadge",
            *badge.box.emu(),
            [paragraph([run(badge.label, size=PT(10), color=badge.text_color, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=badge.fill,
            line_color="none",
            anchor="ctr",
            wrap="none",
            vert="horz",
            **VALUE_BADGE_INSETS.kwargs(),
        ))


def _paint_retained_spend_labels(out: list[str], ids: ShapeIds) -> None:
    for label in RETAINED_SPEND_VALUE_LABELS:
        out.append(text_box(
            ids.next(),
            "RetainedSpendValueLabel",
            *label.box.emu(),
            [paragraph([run(label.label, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            vert="horz",
            **VALUE_BADGE_INSETS.kwargs(),
        ))


def _paint_historical_penetration_badges(out: list[str], ids: ShapeIds) -> None:
    for badge in HISTORICAL_PENETRATION_BADGES:
        out.append(text_box(
            ids.next(),
            "HistoricalPenetrationBadge",
            *badge.box.emu(),
            [paragraph([run(badge.label, size=PT(8.5), italic=True, color=BLACK, font=FONT)], align="ctr")],
            fill=WHITE,
            line_color=BLACK,
            prst=badge.prst,
            anchor="ctr",
            **ZERO_INSETS.kwargs(),
        ))


def _paint_legend(out: list[str], ids: ShapeIds) -> None:
    for swatch in OUTSOURCED_LEGEND_SWATCHES:
        out.append(text_box(
            ids.next(),
            "LegendColorKey",
            *swatch.box.emu(),
            [paragraph([], align="ctr", line_spacing=100_000)],
            fill=swatch.fill,
            line_color="none",
            anchor="ctr",
        ))
    for retained in RETAINED_LEGEND_SWATCHES:
        _draw_retained_outline_box(out, ids, retained)
    for label in LEGEND_LABELS:
        out.append(text_box(
            ids.next(),
            "LegendLabel",
            *label.box.emu(),
            [paragraph([run(label.text, size=PT(label.font_pt), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
            vert="horz",
            **ZERO_INSETS.kwargs(),
        ))


def _paint_penetration_strip(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(),
        "PenetrationStripHeader",
        *PENETRATION_STRIP_HEADER.box.emu(),
        [paragraph([run(PENETRATION_STRIP_HEADER.text, size=PT(8), bold=True, italic=True, color=BLACK, font=FONT)], align="l")],
        fill=None,
        line_color="none",
        vert="vert270",
        **ZERO_INSETS.kwargs(),
    ))
    for label in PENETRATION_ROW_LABELS:
        out.append(text_box(
            ids.next(),
            "PenetrationRowLabel",
            *label.box.emu(),
            [paragraph([run(label.text, size=PT(label.font_pt), bold=label.bold or None, italic=label.italic or None, color=BLACK, font=FONT)], align=label.align)],
            fill=None,
            line_color="none",
            anchor="ctr",
            **ZERO_INSETS.kwargs(),
        ))
    for badge in FORECAST_PENETRATION_BADGES:
        out.append(text_box(
            ids.next(),
            "ForecastPenetrationBadge",
            *badge.box.emu(),
            [paragraph([run(badge.label, size=PT(8.5), italic=True, color=BLACK, font=FONT)], align="ctr")],
            fill=WHITE,
            line_color=BLACK,
            prst=badge.prst,
            geom_adj=badge.geom_adj,
            anchor="ctr",
            **ZERO_INSETS.kwargs(),
        ))


def _paint_chart_footnotes(out: list[str], ids: ShapeIds) -> None:
    for note in CHART_FOOTNOTES:
        out.append(text_box(
            ids.next(),
            note.text.split(":", 1)[0] if note.text.startswith("Note:") else "ForecastNoteStrip",
            *note.box.emu(),
            [paragraph([run(note.text, size=PT(note.font_pt), italic=True, color=BLACK, font=FONT)], align=note.align)],
            fill=None,
            line_color="none",
            anchor="ctr",
            **ZERO_INSETS.kwargs(),
        ))


PAINT_ORDER: tuple[Callable[[list[str], ShapeIds], None], ...] = (
    _paint_commentary_table,
    _paint_chart_frame,
    _paint_chart_title,
    _paint_source_notes,
    _paint_forecast_region,
    _paint_retained_spend_outlines,
    _paint_year_ticks,
    _paint_outsourced_value_badges,
    _paint_retained_spend_labels,
    _paint_historical_penetration_badges,
    _paint_legend,
    _paint_penetration_strip,
    _paint_chart_footnotes,
)


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds()
    for paint in PAINT_ORDER:
        paint(out, ids)
    return "".join(out)


CHROME = Chrome(
    section="Executive Summary",
    topic="Outsourced BC Annual TAM",
    title="Outsourced Basic Construction (Annual TAM)",
    takeaway=(
        "After averaging ~$3.5B through FY2025, demand peaks at ~$5.5B in "
        "FY2024 and FY2026 and is expected to hold ~$4.3-5.7B a year through FY2031."
    ),
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
