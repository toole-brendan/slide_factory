"""Hand-polished slide module: outsourced Basic Construction spend by work type.

Rebuilds source slide 2 from the Defense Demand Drivers New Construction deck.
The visual contract stays source-faithful; the code is organized to be read in
the same order as the exhibit:

    1. local palette and slide contract
    2. the native editable chart (stacked work-type spend per ship class)
    3. the classifier-methodology ledger and the methodology callout
    4. the manual chart overlays: on-bar value badges, class ticks, column totals,
       the work-type legend, leader lines, and the off-house source note
    5. paint functions in PowerPoint z-order

The chart is rebuilt natively through ``column_chart`` (no chart part, no ``_src``
bundle).  The source uses theme scheme colors, so each work-type series carries an
explicit color and the residual series carries its ``ltUpDiag`` hatch.  Every data
label and the whole legend are manual slide shapes layered over the chart frame,
exactly as in the source.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, paragraph,
    run, table, tcell, tcell_rich, text_box, trow,
)


# ════════════════════════════════════════════════════════════════════════════
# Slide contract and local palette
# ════════════════════════════════════════════════════════════════════════════
LAYOUT = "slideLayout4"

BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
FONT = "Arial"

DK2 = "44505C"          # slate breadcrumb gray, reused for the chart leader lines
GRAY_1 = "F2F2F2"       # methodology callout fill
LEDGER_RULE = "808080"  # light inter-row rules in the classifier ledger

# Work-type ramp: chart segments, legend swatches, and on-bar badge fills.
WT_ELECTRICAL = "79838F"
WT_HVAC = "1D4D68"
WT_STRUCTURAL = "486D82"
WT_MACHINING = "89A2B0"
WT_COATINGS = "AFC2CC"
WT_CASTINGS = "D8E3EB"
WT_PIPING = "1D4D68"    # the source deck paints piping the same slate-blue as HVAC
RESIDUAL_PATTERN = {"prst": "ltUpDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"}

SLIDE_METADATA = {
    "role": "supplier_tam / work_type_mix_by_class",
    "source_deck": "Defense Demand Drivers New Construction",
    "source_slide": 2,
    "visual_contract": "source-faithful layout with native editable chart rebuild",
    "primary_pattern": "stacked work-type column per ship class with a manual legend and a methodology ledger",
}

TEXT_FIT = {
    "work_type_chart": {
        "box_in": (4.748, 4.786),
        "content": "3 ship classes x 8 stacked work-type series; native cat/value labels hidden",
        "note": "Manual class ticks, on-bar value badges, column totals, and the legend sit over the native chart.",
    },
    "classifier_ledger": {
        "box_in": (5.134, 3.736),
        "font_pt": 10,
        "content": "seven-stage award-to-share methodology, one rule per stage",
    },
    "methodology_callout": {
        "box_in": (5.134, 1.203),
        "font_pt": 10,
        "content": "two italic notes on contract identity and order-timing accounting",
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
        return {"l_ins": self.left, "t_ins": self.top, "r_ins": self.right, "b_ins": self.bottom}


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
CHART_CATEGORIES: tuple[str, ...] = ("DDG-51", "Columbia", "Virginia")

# Each entry: (work-type series name, solid color, per-class values DDG-51/Columbia/Virginia).
CHART_SERIES: tuple[tuple[str, str, tuple[float, float, float]], ...] = (
    ("Electrical and power", WT_ELECTRICAL, (0.68784013200000005, 2.0152642570000001, 3.5796119719999999)),
    ("HVAC and ventilation", WT_HVAC, (0.60391566499999993, 0.91896297599999999, 2.7926330600000004)),
    ("Structural fabrication and pre-outfit", WT_STRUCTURAL, (0.37146878000000005, 0.69112669100000002, 2.9251053250000005)),
    ("Machining", WT_MACHINING, (2.2607818750000002, 0.10813463999999984, 0.60014579999999995)),
    ("Coatings and insulation", WT_COATINGS, (0.0096669270000000473, 0.068406289999999981, 0.89459187900000003)),
    ("Castings and forgings", WT_CASTINGS, (0.14655910400000005, 0.17871781699999989, 0.60710954199999989)),
    ("Piping, valves, and pumps", WT_PIPING, (0.98415003800000012, 0.086917623000000166, 0.10459976900000001)),
)
# The residual series is drawn as a hatch pattern rather than a solid color.
RESIDUAL_SERIES: tuple[str, tuple[float, float, float]] = (
    "Residual (incl. unassigned spend)",
    (1.3573471589999997, 0.43955620699999987, 2.1229626849999992),
)


def _chart_series() -> list[dict]:
    series = [{"name": name, "color": color, "values": list(values)}
              for name, color, values in CHART_SERIES]
    series.append({"name": RESIDUAL_SERIES[0], "pattern": dict(RESIDUAL_PATTERN),
                   "values": list(RESIDUAL_SERIES[1])})
    return series


CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": _chart_series(),
    "show_legend": False,            # the legend is drawn as manual shapes
    "show_cat_labels": False,        # class ticks are manual shapes
    "show_value_labels": False,      # value badges are manual shapes
    "show_value_axis_labels": True,
    "show_gridlines": False,         # source gridlines are present but noFill
    "value_axis_format": '#,##0;"-"#,##0',
    "value_axis_min": 0,
    "value_axis_max": 14,
    "value_axis_major_unit": 1,
    "cat_label_size_pt": 10,
    "value_label_size_pt": 10,
    "gap_width": 80,
    "bar_overlap": 100,
    "seg_line_color": None,          # segments carry no outline
    "axis_line_color": DK,
    "axis_line_width": 9_525,
    "cat_axis_crosses": "min",
    "value_axis_crosses": "min",
    "plot_layout": {
        "x": 0.085557586837294336,
        "y": 0.051505259339862171,
        "w": 0.8954296160877514,
        "h": 0.89698948132027567,
    },
    "cat_header": "Ship class",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Local table helpers (cell content vs. cell mechanics)
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, str | int]:
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", vert=None, span=1, rowspan=1,
         l_ins=45_720, r_ins=45_720, t_ins=45_720, b_ins=45_720, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, vert=vert, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", vert=None, span=1, rowspan=1,
          l_ins=45_720, r_ins=45_720, t_ins=45_720, b_ins=45_720, **edges):
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor, vert=vert,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ════════════════════════════════════════════════════════════════════════════
# Classifier ledger, methodology callout, and the two section title bars
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class LedgerRow:
    stage: str
    rule: str
    row_h: float
    top_rule: tuple          # (color, width)
    bottom_rule: tuple | None


CLASSIFIER_TABLE = Box(7.7, 1.689, 5.134, 3.736)
CLASSIFIER_COL_WIDTHS = (1.0, 4.134)
CLASSIFIER_ROWS: tuple[LedgerRow, ...] = (
    LedgerRow("1. Award pull", "Pull FFATA/FSRS subawards; collect visible supplier evidence (mix, not TAM)", 0.39, (BLACK, 19_050), (LEDGER_RULE, 6_350)),
    LedgerRow("2. PIID gate", "Gate to yard construction PIIDs per program (BIW / Ingalls; GDEB); GFE chains drop out", 0.39, (LEDGER_RULE, 6_350), (LEDGER_RULE, 6_350)),
    LedgerRow("3. Entity resolution", "Resolve the operating entity paid (UEI), not the parent brand", 0.39, (LEDGER_RULE, 6_350), (LEDGER_RULE, 6_350)),
    LedgerRow("4. Role filter", "Drop non-supplier / non-component roles from the addressable base", 0.39, (LEDGER_RULE, 6_350), (LEDGER_RULE, 6_350)),
    LedgerRow("5. Work-type assign", "First clean match wins one work-type home (vendor registry, NAICS-4)", 0.39, (LEDGER_RULE, 6_350), (LEDGER_RULE, 6_350)),
    LedgerRow("6. Residual discipline", "Keep unresolved dollars in the addressable base; residual dilutes named shares", 0.39, (LEDGER_RULE, 6_350), (LEDGER_RULE, 6_350)),
    LedgerRow("7. Share output", "Bucket dollars over the addressable base set the modeled work-type and residual shares, per class and per FY; FY26–27 share assumed at historical rate.", 0.55, (LEDGER_RULE, 6_350), None),
)

CLASSIFIER_HEADER = trow(
    [
        cell("Stage", size=PT(10), bold=True, B=edge(BLACK, 19_050)),
        cell("Rule applied", size=PT(10), bold=True, B=edge(BLACK, 19_050)),
    ],
    h=IN(0.251),
)


def _ledger_rule_kwargs(top: tuple, bottom: tuple | None) -> dict:
    kw = {"T": edge(*top)}
    if bottom is not None:
        kw["B"] = edge(*bottom)
    return kw


def _ledger_row(row: LedgerRow):
    rule = _ledger_rule_kwargs(row.top_rule, row.bottom_rule)
    return trow(
        [
            cell(row.stage, size=PT(10), bold=True, **rule),
            cell(row.rule, size=PT(10), **rule),
        ],
        h=IN(row.row_h),
    )


@dataclass(frozen=True)
class TitleBar:
    text: str
    box: Box
    col_w: float


CHART_TITLE_BAR = TitleBar(
    "Outsourced Basic Construction Spend by Work Type ($B, cumulative FY22–FY27, FY26 $)",
    Box(0.495, 1.385, 6.97, 0.275), 6.97,
)
METHOD_TITLE_BAR = TitleBar("Methodology", Box(7.7, 1.385, 5.134, 0.275), 5.134)

METHODOLOGY_CALLOUT = Box(7.7, 5.493, 5.134, 1.203)
METHODOLOGY_PARAGRAPHS = (
    "Subaward dollars are reported against program-specific yard construction contracts (PIIDs) — block-level masters for Virginia and Columbia, per-yard multiyear blocks for DDG-51 — with program identity confirmed in FPDS and the SCN contract-data exhibits.",
    "Dollars book in full to the fiscal year the order is placed (the FFATA action date): order timing across the block, not per-hull spend or in-year payment.",
)
METHODOLOGY_SPACE_AFTER = (600, 90)   # per-paragraph spcAft, in EMU points
METHODOLOGY_INSETS = Insets(45_720, 54_864, 45_720, 54_864)


# ════════════════════════════════════════════════════════════════════════════
# Manual chart overlays and the off-house source note
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class ChartFrame:
    name: str
    r_id: str
    box: Box


@dataclass(frozen=True)
class GuideConnector:
    name: str
    box: Box
    flip_h: bool = False
    flip_v: bool = False
    width: int = 6_350


@dataclass(frozen=True)
class ValueBadge:
    """An on-bar segment label: a small filled chip carrying the segment value."""

    label: str
    box: Box
    fill: str
    text_color: str | None   # WHITE over dark segments; None inherits the default


@dataclass(frozen=True)
class CategoryTick:
    label: str
    box: Box


@dataclass(frozen=True)
class TotalLabel:
    label: str
    box: Box


@dataclass(frozen=True)
class LegendSwatch:
    box: Box
    fill: str | None
    pattern: dict | None = None


@dataclass(frozen=True)
class LegendLabel:
    text: str
    box: Box


CHART_FRAME = ChartFrame("Chart", "rId2", Box(0.382, 1.821, 4.748, 4.786))

LEADER_CONNECTORS: tuple[GuideConnector, ...] = (
    GuideConnector("Straight Connector 40", Box(3.224, 5.205, 0.101, 0.045), flip_h=True, flip_v=True),
    GuideConnector("Straight Connector 39", Box(3.224, 5.083, 0.101, 0.043), flip_h=True),
)

# On-bar value badges, painted in source order: the three white-text chips first,
# then the six default-text chips.
ONBAR_VALUE_BADGES: tuple[ValueBadge, ...] = (
    ValueBadge("0.4", Box(1.382, 5.825, 0.229, 0.167), WT_STRUCTURAL, WHITE),
    ValueBadge("0.1", Box(4.415, 2.766, 0.229, 0.167), WT_PIPING, WHITE),
    ValueBadge("0.1", Box(2.997, 5.149, 0.229, 0.167), WT_MACHINING, WHITE),
    ValueBadge("0.0", Box(1.186, 5.073, 0.229, 0.167), WT_COATINGS, None),
    ValueBadge("0.1", Box(1.58, 5.049, 0.229, 0.167), WT_CASTINGS, None),
    ValueBadge("1.4", Box(1.382, 4.516, 0.229, 0.167), WHITE, None),
    ValueBadge("0.2", Box(2.602, 5.083, 0.229, 0.167), WT_CASTINGS, None),
    ValueBadge("0.4", Box(2.997, 4.962, 0.229, 0.167), WHITE, None),
    ValueBadge("2.1", Box(4.217, 2.424, 0.229, 0.167), WHITE, None),
)

CATEGORY_TICKS: tuple[CategoryTick, ...] = (
    CategoryTick("DDG-51", Box(1.236, 6.408, 0.523, 0.167)),
    CategoryTick("Columbia", Box(2.615, 6.408, 0.599, 0.167)),
    CategoryTick("Virginia", Box(4.094, 6.408, 0.476, 0.167)),
)

COLUMN_TOTALS: tuple[TotalLabel, ...] = (
    TotalLabel("6.4", Box(1.382, 4.198, 0.229, 0.167)),
    TotalLabel("4.5", Box(2.799, 4.785, 0.229, 0.167)),
    TotalLabel("13.6", Box(4.179, 1.988, 0.306, 0.167)),
)

# Legend, painted in source order: the residual hatch swatch first, then the
# seven solid swatches top-to-bottom, then the eight work-type labels.
LEGEND_SWATCHES: tuple[LegendSwatch, ...] = (
    LegendSwatch(Box(5.095, 4.595, 0.196, 0.146), None, RESIDUAL_PATTERN),
    LegendSwatch(Box(5.095, 4.818, 0.196, 0.146), WT_HVAC),
    LegendSwatch(Box(5.095, 5.04, 0.196, 0.146), WT_CASTINGS),
    LegendSwatch(Box(5.095, 5.262, 0.196, 0.146), WT_COATINGS),
    LegendSwatch(Box(5.095, 5.484, 0.196, 0.146), WT_MACHINING),
    LegendSwatch(Box(5.095, 5.707, 0.196, 0.146), WT_STRUCTURAL),
    LegendSwatch(Box(5.095, 5.929, 0.196, 0.146), WT_PIPING),
    LegendSwatch(Box(5.095, 6.151, 0.196, 0.146), WT_ELECTRICAL),
)

LEGEND_LABELS: tuple[LegendLabel, ...] = (
    LegendLabel("Residual (incl. unassigned spend)", Box(5.347, 4.59, 2.073, 0.167)),
    LegendLabel("HVAC and ventilation", Box(5.347, 4.812, 1.312, 0.167)),
    LegendLabel("Castings and forgings", Box(5.347, 5.035, 1.335, 0.167)),
    LegendLabel("Coatings and insulation", Box(5.347, 5.257, 1.434, 0.167)),
    LegendLabel("Machining", Box(5.347, 5.479, 0.63, 0.167)),
    LegendLabel("Structural fabrication and pre-outfit", Box(5.347, 5.701, 2.118, 0.167)),
    LegendLabel("Piping, valves, and pumps", Box(5.347, 5.924, 1.611, 0.167)),
    LegendLabel("Electrical and power", Box(5.347, 6.146, 1.245, 0.167)),
)

SOURCE_NOTE = Box(0.495, 6.68, 12.339, 0.322)
SOURCE_TEXT = (
    "Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and PB27 FYDP outyears "
    "(FY28–FY31); FY26, PL 119-21 Sec. 20002; PB27 SCN, Columbia P-10 Strategic Outsourcing "
    "narrative; OUSD(C) Green Book Procurement deflators; Navy Shipbuilding Plan; PB27 SCN "
    "Exhibit P-10, LI 2122 (AP/LLTM Ship Construction EOQ); FFATA/FSRS subaward records, "
    "yard-prime construction PIIDs, FY22–FY25 action years (work-type shares)"
)


# ════════════════════════════════════════════════════════════════════════════
# Paint helpers.  Each appends shapes in PowerPoint z-order.
# ════════════════════════════════════════════════════════════════════════════
def _paint_chart_frame(out: list[str], ids: ShapeIds) -> None:
    x, y, cx, cy = CHART_FRAME.box.emu()
    out.append(graphic_frame(sp_id=ids.next(), name=CHART_FRAME.name, x=x, y=y, cx=cx, cy=cy, rId=CHART_FRAME.r_id))


def _paint_leader_connectors(out: list[str], ids: ShapeIds) -> None:
    for c in LEADER_CONNECTORS:
        out.append(connector(ids.next(), c.name, *c.box.emu(), color=DK2, width=c.width,
                             flip_h=c.flip_h, flip_v=c.flip_v))


def _paint_onbar_value_badges(out: list[str], ids: ShapeIds) -> None:
    for badge in ONBAR_VALUE_BADGES:
        out.append(text_box(
            ids.next(),
            "Label",
            *badge.box.emu(),
            [paragraph([run(badge.label, size=PT(10), color=badge.text_color, font=FONT)],
                       align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=badge.fill,
            line_color="none",
            anchor="ctr",
            wrap="none",
            vert="horz",
            **VALUE_BADGE_INSETS.kwargs(),
        ))


def _paint_category_ticks(out: list[str], ids: ShapeIds) -> None:
    for tick in CATEGORY_TICKS:
        out.append(text_box(
            ids.next(),
            "Label",
            *tick.box.emu(),
            [paragraph([run(tick.label, size=PT(10), color=BLACK, font=FONT)],
                       align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=None,
            line_color="none",
            wrap="none",
            vert="horz",
            **ZERO_INSETS.kwargs(),
        ))


def _paint_column_totals(out: list[str], ids: ShapeIds) -> None:
    for total in COLUMN_TOTALS:
        out.append(text_box(
            ids.next(),
            "Label",
            *total.box.emu(),
            [paragraph([run(total.label, size=PT(10), font=FONT)],
                       align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            vert="horz",
            **VALUE_BADGE_INSETS.kwargs(),
        ))


def _paint_legend_swatches(out: list[str], ids: ShapeIds) -> None:
    for swatch in LEGEND_SWATCHES:
        out.append(text_box(
            ids.next(),
            "LegendSwatch",
            *swatch.box.emu(),
            [paragraph([], align="ctr", line_spacing=100_000)],
            fill=swatch.fill,
            pattern_fill=swatch.pattern,
            line_color="none",
            anchor="ctr",
        ))


def _paint_legend_labels(out: list[str], ids: ShapeIds) -> None:
    for label in LEGEND_LABELS:
        out.append(text_box(
            ids.next(),
            "Label",
            *label.box.emu(),
            [paragraph([run(label.text, size=PT(10), color=BLACK, font=FONT)],
                       mar_l=0, indent=0, line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
            vert="horz",
            **ZERO_INSETS.kwargs(),
        ))


def _paint_source_note(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(),
        "Sources",
        *SOURCE_NOTE.emu(),
        [paragraph([run(SOURCE_TEXT, size=PT(8), color=DK, font=FONT)], line_spacing=100_000)],
        fill=None,
        line_color="none",
        **SOURCE_NOTE_INSETS.kwargs(),
    ))


def _paint_classifier_table(out: list[str], ids: ShapeIds) -> None:
    out.append(table(
        ids.next(),
        "ClassifierLedger",
        *CLASSIFIER_TABLE.emu(),
        col_widths=[IN(w) for w in CLASSIFIER_COL_WIDTHS],
        rows=[CLASSIFIER_HEADER] + [_ledger_row(row) for row in CLASSIFIER_ROWS],
    ))


def _paint_methodology_callout(out: list[str], ids: ShapeIds) -> None:
    paragraphs = [
        paragraph([run(text, size=PT(10), italic=True, color=BLACK, font=FONT)],
                  align="ctr", space_after=space_after, line_spacing=105_000)
        for text, space_after in zip(METHODOLOGY_PARAGRAPHS, METHODOLOGY_SPACE_AFTER)
    ]
    out.append(text_box(
        ids.next(),
        "MethodFindings",
        *METHODOLOGY_CALLOUT.emu(),
        paragraphs,
        fill=GRAY_1,
        line_color=BLACK,
        anchor="ctr",
        **METHODOLOGY_INSETS.kwargs(),
    ))


def _paint_title_bars(out: list[str], ids: ShapeIds) -> None:
    for bar in (CHART_TITLE_BAR, METHOD_TITLE_BAR):
        out.append(table(
            ids.next(),
            "StepRationaleLedger",
            *bar.box.emu(),
            col_widths=[IN(bar.col_w)],
            rows=[trow([cell(bar.text, size=PT(10), bold=True, B=edge(BLACK))], h=IN(0))],
        ))


PAINT_ORDER: tuple[Callable[[list[str], ShapeIds], None], ...] = (
    _paint_chart_frame,
    _paint_leader_connectors,
    _paint_onbar_value_badges,
    _paint_category_ticks,
    _paint_column_totals,
    _paint_legend_swatches,
    _paint_legend_labels,
    _paint_source_note,
    _paint_classifier_table,
    _paint_methodology_callout,
    _paint_title_bars,
)


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds()
    for paint in PAINT_ORDER:
        paint(out, ids)
    return "".join(out)


CHROME = Chrome(
    section="Executive Summary",
    topic="Supplier TAM and SAM",
    title="Outsourced Spend by Work Type",
    takeaway="Electrical power leads the ~$18.1B submarine pool; machining leads the ~$6.4B DDG-51 pool.",
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
