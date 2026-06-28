"""Teaching exemplar: TCV to ACV approach — undersea Company ACV.

ROLE
  market_sizing_flow / tcv_to_acv_timing_bridge

USE WHEN
  A slide needs to explain how Company TCV turns into annual contract value using
  product-specific contract exercise timing.

TEACHES
  - top formula band: Company TCV × contract exercise timing = Company ACV by year
  - fully declarative native charting with column_chart(mode="stacked")
  - waterfall-like chart built from explicit hidden-offset and visible-segment series
  - manual category ticks and bar-value badges over a native chart
  - output cards for Year 1 through Year 5 ACV
  - dense exercise-timing table authored from semantic product timing rows

TEXT-FIT PRECEDENT
  exercise_timing_table:
    geometry: 12.482in wide x 2.100in high, eight columns
    type: Arial 10pt; 0.3in row minimums; 60960 EMU cell padding
    content: banner + header row + five product timing rows
    copy_when: a slide needs a compact assumptions table below a worked example

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_to_acv_company_acv_undersea.py`. The
  original converter table body is promoted into `TimingRow` records and the chart
  labels/cards are semantic data rather than shape clusters. This version
  intentionally replaces the source chart-template wrapper with a native
  `column_chart(mode="stacked", ...)` spec. The chart is authored from explicit
  categories, series values, per-point fills, axis settings, gap/overlap, and
  plot layout.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical
  chart-template port. It preserves the visible waterfall semantics, source
  chart frame, manual labels, cards, table dimensions, logo relationship,
  fixed 0-200 value axis, hidden native axes/legend, source gap/overlap, and
  the source chart part's per-point fills. Small differences in native column
  width or chart XML ordering may occur versus the bundled template.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, line_break,
    paragraph, picture, run, table, tcell, tcell_rich, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_4 = "3D5972"
BLUE_5 = "263746"
GRAY_1 = "F2F2F2"
FONT = "Arial"


# Local table-cell kit (was deck_core.table_kit).
def edge(color, w=12700):
    """One cell-border edge dict (default 1pt hairline)."""
    return {"color": color, "width": w}

def bd(L=None, R=None, T=None, B=None):
    """Border map from only the sides drawn; omitted sides render no-fill."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None

def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """Single-run text cell; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """Multi-paragraph rich cell; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

LAYOUT = "slideLayout4"

# Fully declarative native chart spec. The source chart was a stacked-column
# waterfall-like template: a white/no-outline offset series establishes each
# segment's starting height, while visible per-point fills create the SAM,
# Market Share, Company TCV, Initial, In-year, and Year 2-5 exercise bars.
# No chart XML template and no external workbook are bundled.
SAM_BLUE = "6E91B1"
COMPANY_TCV_BLUE = "3D5972"
COMPANY_ACV_BLUE = "263746"
MARKET_SHARE_GRAY = "C0C0C0"
INVISIBLE_OFFSET = WHITE

CHART_CATEGORIES: tuple[str, ...] = (
    "SAM",
    "Market Share",
    "Company TCV",
    "Initial exercise",
    "In-year exercise",
    "Year 2 exercise",
    "Year 3 exercise",
    "Year 4 exercise",
    "Year 5 exercise",
)

# Series are ordered bottom-to-top in the stacked columns. White points emulate
# the source chart's no-fill spacer blocks; all value labels are placed manually
# as slide text boxes, so native labels stay hidden.
ACV_WATERFALL_SERIES: tuple[dict, ...] = (
    {
        "name": "Totals and hidden waterfall offsets",
        "color": INVISIBLE_OFFSET,
        "values": [200, 100, 100, 50, 15, 15, 0, 0, 0],
        "data_point_colors": [
            SAM_BLUE,
            INVISIBLE_OFFSET,
            COMPANY_TCV_BLUE,
            INVISIBLE_OFFSET,
            INVISIBLE_OFFSET,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
        ],
        "hide_labels": True,
    },
    {
        "name": "Visible timing / share bridge segments",
        "color": COMPANY_ACV_BLUE,
        "values": [None, 100, None, 50, 35, None, None, None, None],
        "data_point_colors": [
            COMPANY_ACV_BLUE,
            MARKET_SHARE_GRAY,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
            COMPANY_ACV_BLUE,
        ],
        "hide_labels": True,
    },
)

# Readable data mirror for agents/tools that expect the converted-slide data-dict
# shape. CHARTS below uses the same values through column_chart().
ACV_WATERFALL_DATA = {
    "categories": CHART_CATEGORIES,
    "series": ACV_WATERFALL_SERIES,
}

_CHART0_DATA = ACV_WATERFALL_DATA

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in ACV_WATERFALL_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": "General",
    "value_label_format": "General",
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "cat_label_size_pt": 10,
    "gap_width": 80,
    "bar_overlap": 100,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9525,
    "value_axis_min": 0,
    "value_axis_max": 200,
    "value_axis_major_unit": 50,
    "plot_layout": {
        "x": 0.007129147244310392,
        "y": 0.052791878172588833,
        "w": 0.9857417055113792,
        "h": 0.8944162436548223,
    },
    "cat_header": "Bridge step",
}

CHARTS = [column_chart(**CHART_STYLE)]
IMAGES = [
    {"rId": "rId3", "file": "image6_3071a231.jpeg"},
]

RULE_GRAY = "808080"
PALE_SCOPE_BLUE = "CEDDEC"
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)
TIGHT_BADGE_INSETS = dict(l_ins=17463, t_ins=0, r_ins=17463, b_ins=0)


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class TextFitZone:
    name: str
    box: Box
    fit: str
    copy_when: str


@dataclass(frozen=True)
class AxisLabel:
    label: str
    box: Box


@dataclass(frozen=True)
class ValueBadge:
    label: str
    box: Box
    text_color: str
    fill: str | None = None


@dataclass(frozen=True)
class FormulaBox:
    role: str
    label: str
    box: Box
    fill: str
    text_color: str = WHITE
    line_color: str | None = BLACK
    line_width: int = 3175


@dataclass(frozen=True)
class AcvCard:
    role: str
    lead: str
    value: str
    box: Box


@dataclass(frozen=True)
class TimingRow:
    product: str
    rationale: str
    values: tuple[str, str, str, str, str, str]
    top_rule: str
    bottom_rule: str


TEACHING_METADATA = {
    "role": "market_sizing_flow / tcv_to_acv_timing_bridge",
    "use_when": "Translate total contract value into annual contract value using exercise timing.",
    "source_module": "tcv_to_acv_company_acv_undersea.py",
    "rebuild_strategy": "replace chart-template wrapper with native column_chart",
    "teaches": (
        "formula band above native factory chart",
        "fully declarative native stacked-column chart",
        "floating-waterfall columns via white spacer segments",
        "manual chart ticks and value badges",
        "explicit chart categories / series / colors / axis scale",
        "ACV by year output cards",
        "semantic assumptions table",
    ),
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_step", Box(0.425, 1.229, 2.291, 1.061), "Arial 10pt; one sentence below italic header", "copy for compact methodology headers"),
    TextFitZone("chart_axis_labels", Box(1.031, 4.634, 11.740, 0.167), "Arial 10pt, no-wrap, zero insets", "copy for manual labels under a native chart"),
    TextFitZone("exercise_timing_table", Box(0.495, 4.903, 12.482, 2.100), "Arial 10pt, 0.3in rows", "copy for dense contract-timing tables"),
)

COPY_RULES: tuple[str, ...] = (
    "Use cards to say what the chart means for each year; do not ask the chart to carry that conclusion alone.",
    "Keep timing assumptions in table rows, not buried in callout prose.",
    "Use white hidden-offset segments to teach the waterfall bridge without chart-template OOXML.",
)

FORMULA_BOXES: tuple[FormulaBox, ...] = (
    FormulaBox("input", "Company TCV ($)", Box(3.515, 1.760, 2.549, 0.359), BLUE_4),
    FormulaBox("factor", "Contract exercise timing (%)", Box(7.456, 1.760, 2.548, 0.359), DK, WHITE, DK, 12700),
    FormulaBox("output", "Company ACV by year ($)", Box(11.460, 1.760, 1.519, 0.359), BLUE_5),
)

DASHED_EXERCISE_ARROWS = (
    Box(1.573, 2.974, 0.616, 0.000),
    Box(2.960, 3.740, 0.616, 0.000),
    Box(4.347, 3.740, 0.616, 0.000),
    Box(5.734, 4.122, 0.616, 0.000),
    Box(7.122, 4.389, 0.615, 0.000),
)

CATEGORY_TICKS: tuple[AxisLabel, ...] = (
    AxisLabel("SAM", Box(1.031, 4.634, 0.314, 0.167)),
    AxisLabel("Market Share", Box(2.153, 4.634, 0.844, 0.167)),
    AxisLabel("Company TCV", Box(3.502, 4.634, 0.922, 0.167)),
    AxisLabel("Initial exercise", Box(4.905, 4.634, 0.891, 0.167)),
    AxisLabel("In-year exercise", Box(6.238, 4.634, 0.998, 0.167)),
    AxisLabel("Year 2 exercise", Box(7.635, 4.634, 0.974, 0.167)),
    AxisLabel("Year 3 exercise", Box(9.023, 4.634, 0.974, 0.167)),
    AxisLabel("Year 4 exercise", Box(10.410, 4.634, 0.974, 0.167)),
    AxisLabel("Year 5 exercise", Box(11.797, 4.634, 0.974, 0.167)),
)

BAR_VALUE_BADGES: tuple[ValueBadge, ...] = (
    ValueBadge("$200", Box(1.016, 3.655, 0.344, 0.167), WHITE),
    ValueBadge("$100", Box(2.403, 3.273, 0.344, 0.167), BLACK),
    ValueBadge("$100", Box(3.790, 4.038, 0.344, 0.167), WHITE),
    ValueBadge("$50", Box(5.215, 3.847, 0.267, 0.167), WHITE),
    ValueBadge("$35", Box(6.602, 4.172, 0.267, 0.167), WHITE),
    ValueBadge("$15", Box(7.988, 4.363, 0.267, 0.167), WHITE, BLUE_5),
)

ZERO_VALUE_BADGES: tuple[ValueBadge, ...] = (
    ValueBadge("0", Box(9.451, 4.420, 0.115, 0.167), WHITE, BLUE_5),
    ValueBadge("0", Box(10.839, 4.420, 0.115, 0.167), WHITE, BLUE_5),
    ValueBadge("0", Box(12.226, 4.420, 0.115, 0.167), WHITE, BLUE_5),
)

ACV_CARDS: tuple[AcvCard, ...] = (
    AcvCard("year1", "Company ACV:", "$85M in Year 1", Box(4.964, 2.980, 2.158, 0.385)),
    AcvCard("year2", "Year 2 ACV:", "$15M", Box(7.519, 2.980, 1.218, 0.385)),
    AcvCard("year3", "Year 3 ACV:", "$0M", Box(8.899, 2.980, 1.218, 0.385)),
    AcvCard("year4", "Year 4 ACV:", "$0M", Box(10.287, 2.980, 1.218, 0.385)),
    AcvCard("year5", "Year 5 ACV:", "$0M", Box(11.674, 2.980, 1.218, 0.385)),
)

TIMING_ROWS: tuple[TimingRow, ...] = (
    TimingRow("Corsair kits", "First tranche / subsequent (in line w/ OT)", ("100% / 50%", "0% / 35%", "0% / 15%", "- -", "- -", "- -"), DK, RULE_GRAY),
    TimingRow("Mirage kits", "In line with Surface Navy Mirage timing", ("50%", "35%", "15%", "- -", "- -", "- -"), RULE_GRAY, RULE_GRAY),
    TimingRow("Mirage COCO", "Quarter-long operations", ("100%", "- -", "- -", "- -", "- -", "- -"), RULE_GRAY, RULE_GRAY),
    TimingRow("TREX", "Expecting all CLINs exercised up front", ("100%", "- -", "- -", "- -", "- -", "- -"), RULE_GRAY, RULE_GRAY),
    TimingRow("LCUE", "Expecting all CLINs exercised up front", ("100%", "- -", "- -", "- -", "- -", "- -"), RULE_GRAY, WHITE),
)


def _shape_ids():
    return iter(range(100, 2000))


def _plain(text: str, *, size: int = PT(10), color: str = BLACK, bold: bool = False, italic: bool = False, align: str | None = "ctr") -> str:
    return paragraph([run(text, size=size, color=color, bold=bold or None, italic=italic or None, font=FONT)], align=align, line_spacing=100000)


def _draw_formula_box(out: list[str], n, spec: FormulaBox) -> None:
    out.append(text_box(
        n(), spec.role, *spec.box.emu(), [_plain(spec.label, color=spec.text_color)],
        fill=spec.fill, line_color=spec.line_color, line_width=spec.line_width, anchor="ctr",
    ))


def _draw_value_badge(out: list[str], n, badge: ValueBadge) -> None:
    if badge.label.startswith("$"):
        pieces = [run("$", size=PT(10), color=badge.text_color, font=FONT), run(badge.label[1:], size=PT(10), color=badge.text_color, font=FONT)]
    else:
        pieces = [run(badge.label, size=PT(10), color=badge.text_color, font=FONT)]
    out.append(text_box(
        n(), "ValueBadge", *badge.box.emu(),
        [paragraph(pieces, align="ctr", mar_l=0, indent=0, line_spacing=100000)],
        fill=badge.fill, line_color="none", anchor="ctr", wrap="none", **TIGHT_BADGE_INSETS,
    ))


def _timing_cell(text: str, *, top: str, bottom: str, bold: bool = False, italic: bool = False, align: str | None = None):
    if align == "ctr" or italic:
        return rcell([
            tpara([trun(text, size=PT(10), bold=bold or None, italic=italic or None, color=BLACK, font=FONT)], align=align, mar_l=0, indent=0)
        ], **PAD, T=edge(top), B=edge(bottom))
    return cell(text, size=PT(10), bold=bold or None, color=BLACK, **PAD, T=edge(top), B=edge(bottom))


def _timing_row(row: TimingRow) -> str:
    cells = [
        cell(row.product, size=PT(10), bold=True, color=BLACK, **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
        rcell([tpara([trun(row.rationale, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
    ]
    for value in row.values:
        cells.append(_timing_cell(value, top=row.top_rule, bottom=row.bottom_rule, italic=True, align="ctr"))
    return trow(cells, h=IN(0.3))


def _exercise_timing_table(sp_id: int) -> str:
    rows = [
        trow([
            rcell([tpara([trun("Contract exercise timing by product:", size=PT(10), italic=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], span=2, anchor="b", **PAD, B=edge(WHITE)),
            cell("Year 1", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, span=2, anchor="b", **PAD, R=edge(WHITE), B=edge(DK)),
            cell("Year 2", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(DK)),
            cell("Year 3", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(DK)),
            cell("Year 4", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(DK)),
            cell("Year 5", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), B=edge(DK)),
        ], h=IN(0.3)),
        trow([
            cell("Product", size=PT(10), bold=True, color=BLACK, anchor="b", T=edge(WHITE), B=edge(DK)),
            cell("Rationale", size=PT(10), bold=True, color=BLACK, anchor="b", **PAD, T=edge(WHITE), B=edge(DK)),
            cell("Initial exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("In-Year exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 2 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 3 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 4 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 5 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
        ], h=IN(0.3)),
    ]
    rows.extend(_timing_row(row) for row in TIMING_ROWS)
    return table(sp_id, "ExerciseTimingTable", IN(0.495), IN(4.903), IN(12.482), IN(2.1), col_widths=[IN(1.283), IN(2.993), IN(1.368), IN(1.368), IN(1.368), IN(1.368), IN(1.368), IN(1.368)], rows=rows)


def paint_approach_header(out: list[str], n) -> None:
    out.append(text_box(n(), "ApproachDescription", IN(0.425), IN(1.589), IN(2.289), IN(0.701), [_plain("Multiply Company TCV by contract exercise timing to find Company ACV", align=None)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "ApproachStepsHeader", IN(0.425), IN(1.229), IN(2.291), IN(0.359), [_plain("Approach steps", italic=True, align=None)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "ApproachHeaderRule", IN(0.426), IN(1.586), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))


def paint_formula_output_and_chart_arrows(out: list[str], n) -> None:
    _draw_formula_box(out, n, FORMULA_BOXES[2])
    for b in DASHED_EXERCISE_ARROWS:
        out.append(connector(n(), "DashedExerciseArrow", *b.emu(), color=DK, width=3175, dash="lgDash"))


def paint_worked_chart(out: list[str], n) -> None:
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.405), y=IN(2.884), cx=IN(12.663), cy=IN(1.710), rId="rId2"))
    _draw_value_badge(out, n, BAR_VALUE_BADGES[0])
    for tick in CATEGORY_TICKS:
        out.append(text_box(n(), "CategoryTick", *tick.box.emu(), [_plain(tick.label)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for badge in BAR_VALUE_BADGES[1:]:
        _draw_value_badge(out, n, badge)
    for badge in ZERO_VALUE_BADGES:
        _draw_value_badge(out, n, badge)


def paint_formula_inputs_and_timing_table(out: list[str], n) -> None:
    out.append(text_box(n(), "MultiplyGlyph", IN(6.575), IN(1.739), IN(0.400), IN(0.400), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(_exercise_timing_table(n()))
    _draw_formula_box(out, n, FORMULA_BOXES[0])
    out.append(text_box(n(), "EqualsGlyph", IN(10.548), IN(1.739), IN(0.400), IN(0.400), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    for card in ACV_CARDS[:2]:
        out.append(text_box(n(), card.role, *card.box.emu(), [paragraph([run(card.lead + " ", size=PT(10), color=WHITE, font=FONT), line_break(), run(card.value, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))
    out.append(connector(n(), "TimelineDivider", IN(0.495), IN(2.611), IN(12.339), IN(0.002), color=RULE_GRAY, width=12700))
    _draw_formula_box(out, n, FORMULA_BOXES[1])
    out.append(text_box(n(), "TimingDefinition", IN(6.427), IN(2.125), IN(4.607), IN(0.426), [paragraph([run("Defined as proportion of contract exercised each year ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., 85% in Year 1, 15% in Year 2 for Corsair) ", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "WorkedExampleCaption", IN(0.425), IN(2.253), IN(3.922), IN(0.359), [_plain("Company ACV estimation example ($M):", italic=True, align=None)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "ProgramsFrame", IN(6.063), IN(3.524), IN(6.914), IN(1.320), [_plain("For Programs to deliver", italic=True)], fill=None, line_color=RULE_GRAY, line_width=19050, dashed_line=True))


def paint_timeline_scope_cards_and_logo(out: list[str], n) -> None:
    out.append(connector(n(), "Year1Arrow", IN(0.540), IN(2.816), IN(6.582), IN(0), color=DK, width=12700, arrow=True))
    out.append(text_box(n(), "Year1Label", IN(3.516), IN(2.701), IN(0.747), IN(0.229), [_plain("Year 1", color=DK, bold=True)], fill=WHITE, line_color="none", anchor="ctr"))
    out.append(connector(n(), "SubsequentYearsArrow", IN(7.519), IN(2.816), IN(5.373), IN(0), color=DK, width=12700, arrow=True))
    out.append(text_box(n(), "SubsequentYearsLabel", IN(9.096), IN(2.701), IN(2.316), IN(0.229), [_plain("Subsequent years", color=DK, bold=True)], fill=WHITE, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "ScopeChip", IN(9.121), IN(0.074), IN(2.663), IN(0.500), [_plain("All archetypes", color=DK, bold=True, size=PT(12))], fill=PALE_SCOPE_BLUE, line_color=DK, line_width=3175, anchor="ctr"))
    for card in ACV_CARDS[2:]:
        out.append(text_box(n(), card.role, *card.box.emu(), [paragraph([run(card.lead + " ", size=PT(10), color=WHITE, font=FONT), line_break(), run(card.value, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))
    out.append(picture(n(), "NavyLogo", "rId3", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    out.append(text_box(n(), "ContractFootnote", IN(9.023), IN(3.959), IN(3.748), IN(0.403), [_plain("May be used if Weapons Procurement contract extends over 5-year period", italic=True)], fill=GRAY_1, line_color=GRAY_1, line_width=19050, anchor="ctr"))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_approach_header(out, n)
    paint_formula_output_and_chart_arrows(out, n)
    paint_worked_chart(out, n)
    paint_formula_inputs_and_timing_table(out, n)
    paint_timeline_scope_cards_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Undersea)",
    title="TCV to ACV Approach",
    takeaway="Finding Company ACV",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
