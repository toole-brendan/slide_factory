"""Teaching exemplar: TCV to ACV approach — Company ACV.

ROLE
  market_sizing_bridge / contract_timing_to_acv

USE WHEN
  A slide needs to explain how Company TCV converts into annual contract
  value through product-specific contract exercise timing.

TEACHES
  - formula band: Company TCV × Contract exercise timing = Company ACV
  - fully declarative native charting with column_chart(mode="stacked")
  - waterfall-like chart built from explicit hidden-offset and visible-segment series
  - manual category ticks and dollar-value badges over a native chart
  - two-year ACV cards as the executive readout
  - dense exercise-timing table authored from semantic product records

TEXT-FIT PRECEDENT
  timing_table:
    geometry: 12.482in wide x 1.667in high, five columns
    type: Arial 10pt, 60960 EMU cell padding
    copy_when: a worked chart needs a compact assumptions table underneath

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_to_acv_company_acv.py`. The
  converter table and label clusters are promoted into `FormulaBox`,
  `ValueBadge`, `AxisLabel`, `AcvCard`, and `TimingRow` records. This version
  intentionally replaces the source chart-template wrapper with a native
  `column_chart(mode="stacked", ...)` spec. The chart is authored from explicit
  categories, series values, per-point fills, axis settings, gap/overlap, and
  plot layout.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical
  chart-template port. It preserves the visible waterfall semantics, source
  chart frame, manual labels, cards, table dimensions, scope-chip treatment,
  fixed 0-400 value axis, hidden native axes/legend, source gap/overlap, and
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
# Market Share, Company TCV, Initial, In-year, and Next-year bars. No chart XML
# template and no external workbook are bundled.
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
    "Next-year exercise",
)

# Series are ordered bottom-to-top in the stacked columns. White points emulate
# the source chart's no-fill spacer blocks; all value labels are placed manually
# as slide text boxes, so native labels stay hidden.
ACV_WATERFALL_SERIES: tuple[dict, ...] = (
    {
        "name": "Totals and hidden waterfall offsets",
        "color": INVISIBLE_OFFSET,
        "values": [400, 200, 200, 190, 100, 100],
        "data_point_colors": [
            SAM_BLUE,
            INVISIBLE_OFFSET,
            COMPANY_TCV_BLUE,
            INVISIBLE_OFFSET,
            INVISIBLE_OFFSET,
            COMPANY_ACV_BLUE,
        ],
        "hide_labels": True,
    },
    {
        "name": "Visible timing / share bridge segments",
        "color": COMPANY_ACV_BLUE,
        "values": [None, 200, None, 10, 90, None],
        "data_point_colors": [
            COMPANY_ACV_BLUE,
            MARKET_SHARE_GRAY,
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
    "value_axis_max": 400,
    "value_axis_major_unit": 100,
    "plot_layout": {
        "x": 0.007129147244310392,
        "y": 0.04410517387616624,
        "w": 0.9857417055113792,
        "h": 0.9117896522476675,
    },
    "cat_header": "Bridge step",
}

CHARTS = [column_chart(**CHART_STYLE)]
IMAGES = [{"rId": "rId3", "file": "image8_3071a231.jpeg"}]

PALE_SCOPE_BLUE = "CEDDEC"
RULE_GRAY = "808080"
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
    initial: str
    in_year: str
    next_year: str
    top_rule: str
    bottom_rule: str


TEACHING_METADATA = {
    "role": "market_sizing_bridge / contract_timing_to_acv",
    "use_when": "Company TCV must be translated into ACV by year.",
    "source_module": "tcv_to_acv_company_acv.py",
    "rebuild_strategy": "replace chart-template wrapper with native column_chart",
    "teaches": (
        "formula band over native factory chart",
        "fully declarative native stacked-column chart",
        "floating-waterfall columns via white spacer segments",
        "manual chart ticks and dollar badges",
        "explicit chart categories / series / colors / axis scale",
        "two-year ACV output cards",
        "semantic product timing table",
    ),
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("formula_band", Box(3.515, 1.760, 9.464, 0.359), "Arial 10pt variable labels", "copy for conversion bridge slides"),
    TextFitZone("chart_axis_labels", Box(1.378, 5.002, 11.144, 0.167), "Arial 10pt, no-wrap, zero insets", "copy for manual chart ticks"),
    TextFitZone("timing_table", Box(0.495, 5.318, 12.482, 1.667), "Arial 10pt table with 60960 EMU padding", "copy for compact assumptions tables"),
)

COPY_RULES: tuple[str, ...] = (
    "Use the formula band as the primary grammar; the chart is the worked proof.",
    "Keep dollar badges value-only so they do not compete with the table assumptions.",
    "Use white hidden-offset segments to teach the waterfall bridge without chart-template OOXML.",
    "Keep the timing table below the chart when it explains chart mechanics.",
)

FLOW_GRAMMAR = {
    "formula": "Company TCV × Contract exercise timing (%) = Company ACV by year",
    "worked_example": "SAM → Market Share → Company TCV → initial/in-year/next-year exercise",
    "supporting_table": "product-level timing assumptions",
}

FORMULA_BOXES: tuple[FormulaBox, ...] = (
    FormulaBox("output", "Company ACV by year ($)", Box(11.460, 1.760, 1.519, 0.359), BLUE_5),
    FormulaBox("input", "Company TCV ($)", Box(3.515, 1.760, 2.549, 0.359), BLUE_4),
    FormulaBox("factor", "Contract exercise timing (%)", Box(7.456, 1.760, 2.548, 0.359), DK, DK, 12700),
)

CATEGORY_TICKS: tuple[AxisLabel, ...] = (
    AxisLabel("SAM", Box(1.378, 5.002, 0.314, 0.167)),
    AxisLabel("Market Share", Box(3.193, 5.002, 0.844, 0.167)),
    AxisLabel("Company TCV", Box(5.236, 5.002, 0.922, 0.167)),
    AxisLabel("Initial exercise", Box(7.332, 5.002, 0.891, 0.167)),
    AxisLabel("In-year exercise", Box(9.358, 5.002, 0.998, 0.167)),
    AxisLabel("Next-year exercise", Box(11.354, 5.002, 1.168, 0.167)),
)

BAR_VALUE_BADGES: tuple[ValueBadge, ...] = (
    ValueBadge("$400", Box(1.363, 3.938, 0.344, 0.167), WHITE),
    ValueBadge("$200", Box(3.443, 3.472, 0.344, 0.167), BLACK),
    ValueBadge("$200", Box(5.524, 4.405, 0.344, 0.167), WHITE),
    ValueBadge("$10", Box(7.642, 3.962, 0.267, 0.167), WHITE, BLUE_5),
    ValueBadge("$90", Box(9.722, 4.194, 0.267, 0.167), WHITE),
    ValueBadge("$100", Box(11.766, 4.637, 0.344, 0.167), WHITE),
)

ACV_CARDS: tuple[AcvCard, ...] = (
    AcvCard("year1", "Company ACV:", "$100M in Year 1", Box(7.198, 3.083, 3.238, 0.512)),
    AcvCard("year2", "Company ACV:", "$100M in Year 2", Box(11.192, 3.083, 1.474, 0.512)),
)

TIMING_ROWS: tuple[TimingRow, ...] = (
    TimingRow("Corsair", "In line with Production OT", "50%", "35%", "15%", DK, RULE_GRAY),
    TimingRow("Mirage", "Assumes similar timing as Corsair Production OT because Mirage falls under sUSV funding", "50%", "35%", "15%", RULE_GRAY, RULE_GRAY),
    TimingRow("Marauder", "Based on estimated MASC contract exercise: MASC procured in 10-vessel block buys with each vessel a separate CLIN and CLINs are exercised evenly across 24-month period", "5%", "45%", "50%", RULE_GRAY, WHITE),
)


def _shape_ids():
    return iter(range(100, 2000))


def _plain(text: str, *, size: int = PT(10), color: str = BLACK, bold: bool = False, italic: bool = False, align: str | None = "ctr") -> str:
    return paragraph([run(text, size=size, color=color, bold=bold or None, italic=italic or None, font=FONT)], align=align, line_spacing=100000)


def _draw_formula_box(out: list[str], n, spec: FormulaBox) -> None:
    out.append(text_box(n(), spec.role, *spec.box.emu(), [_plain(spec.label, color=WHITE)], fill=spec.fill, line_color=spec.line_color, line_width=spec.line_width, anchor="ctr"))


def _draw_value_badge(out: list[str], n, badge: ValueBadge) -> None:
    if badge.label.startswith("$"):
        pieces = [run("$", size=PT(10), color=badge.text_color, font=FONT), run(badge.label[1:], size=PT(10), color=badge.text_color, font=FONT)]
    else:
        pieces = [run(badge.label, size=PT(10), color=badge.text_color, font=FONT)]
    out.append(text_box(n(), "ValueBadge", *badge.box.emu(), [paragraph(pieces, align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=badge.fill, line_color="none", anchor="ctr", wrap="none", **TIGHT_BADGE_INSETS))


def _timing_row(row: TimingRow) -> str:
    return trow([
        cell(row.product, size=PT(10), bold=True, color=BLACK, **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
        rcell([tpara([trun(row.rationale, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
        rcell([tpara([trun(row.initial, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
        rcell([tpara([trun(row.in_year, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
        rcell([tpara([trun(row.next_year, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(row.top_rule), B=edge(row.bottom_rule)),
    ], h=IN(0))


def _exercise_timing_table(sp_id: int) -> str:
    rows = [
        trow([
            rcell([tpara([trun("Contract exercise timing by product:", size=PT(10), italic=True, color=DK, font=FONT)], mar_l=0, indent=0)], span=2, anchor="b", **PAD, B=edge(WHITE)),
            cell("Year 1", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, span=2, anchor="b", **PAD, R=edge(WHITE), B=edge(DK)),
            cell("Year 2", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), B=edge(DK)),
        ], h=IN(0)),
        trow([
            cell("Product", size=PT(10), bold=True, color=BLACK, anchor="b", T=edge(WHITE), B=edge(DK)),
            cell("Rationale", size=PT(10), bold=True, color=BLACK, anchor="b", **PAD, T=edge(WHITE), B=edge(DK)),
            cell("Initial exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("In-Year exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Next-year exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
        ], h=IN(0)),
    ]
    rows.extend(_timing_row(row) for row in TIMING_ROWS)
    return table(sp_id, "ExerciseTimingTable", IN(0.495), IN(5.318), IN(12.482), IN(1.667), col_widths=[IN(0.851), IN(5.847), IN(1.812), IN(1.812), IN(2.160)], rows=rows)


def paint_approach_header(out: list[str], n) -> None:
    out.append(text_box(n(), "ApproachDescription", IN(0.425), IN(1.589), IN(2.289), IN(0.701), [_plain("Multiply Company TCV by contract exercise timing to find Company ACV", align=None)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "ApproachStepsHeader", IN(0.425), IN(1.229), IN(2.291), IN(0.359), [_plain("Approach steps", italic=True, align=None)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "ApproachHeaderRule", IN(0.426), IN(1.586), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))


def paint_formula_output_and_chart(out: list[str], n) -> None:
    _draw_formula_box(out, n, FORMULA_BOXES[0])
    for b in (Box(2.113, 3.089, 0.924, 0.000), Box(4.194, 4.023, 0.924, 0.000), Box(6.274, 4.023, 0.924, 0.000), Box(8.354, 4.068, 0.924, 0.000), Box(10.436, 4.488, 0.924, 0.000)):
        out.append(connector(n(), "DashedExerciseArrow", *b.emu(), color=DK, width=3175, dashed=True, arrow=True))
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.405), y=IN(2.998), cx=IN(12.663), cy=IN(2.047), rId="rId2"))
    _draw_value_badge(out, n, BAR_VALUE_BADGES[0])
    for tick in CATEGORY_TICKS:
        out.append(text_box(n(), "CategoryTick", *tick.box.emu(), [_plain(tick.label)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for badge in BAR_VALUE_BADGES[1:]:
        _draw_value_badge(out, n, badge)


def paint_formula_inputs_cards_and_table(out: list[str], n) -> None:
    out.append(text_box(n(), "MultiplyGlyph", IN(6.575), IN(1.739), IN(0.400), IN(0.400), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    _draw_formula_box(out, n, FORMULA_BOXES[1])
    out.append(text_box(n(), "EqualsGlyph", IN(10.548), IN(1.739), IN(0.400), IN(0.400), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    for card in ACV_CARDS:
        out.append(text_box(n(), card.role, *card.box.emu(), [paragraph([run(card.lead + " ", size=PT(10), color=WHITE, font=FONT), line_break(), run(card.value, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "ProgramsFrame", IN(9.167), IN(3.781), IN(3.479), IN(1.435), [_plain("For Programs to deliver", italic=True)], fill=None, line_color=RULE_GRAY, line_width=19050, dashed_line=True))
    out.append(connector(n(), "TimelineDivider", IN(0.495), IN(2.734), IN(12.339), IN(0.002), color=RULE_GRAY, width=12700))
    _draw_formula_box(out, n, FORMULA_BOXES[2])
    out.append(text_box(n(), "TimingDefinition", IN(6.427), IN(2.125), IN(4.607), IN(0.426), [paragraph([run("Defined as proportion of contract exercised each year ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., 50% in Year 1, 50% in Year 2 for Marauder) ", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "WorkedExampleCaption", IN(0.425), IN(2.377), IN(5.099), IN(0.359), [_plain("Company ACV estimation example ($M, presumed Marauder exercise timing):", italic=True, align=None)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Year1Arrow", IN(0.540), IN(2.885), IN(10.239), IN(0), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Year1Label", IN(5.078), IN(2.774), IN(1.162), IN(0.222), [_plain("Year 1", bold=True)], fill=WHITE, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Year2Arrow", IN(10.844), IN(2.885), IN(2.134), IN(0), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Year2Label", IN(11.470), IN(2.774), IN(0.920), IN(0.222), [_plain("Year 2", bold=True)], fill=WHITE, line_color="none", anchor="ctr"))
    out.append(_exercise_timing_table(n()))


def paint_scope_chip_and_logo(out: list[str], n) -> None:
    out.append(text_box(n(), "ScopeChip", IN(9.353), IN(0.137), IN(2.200), IN(0.375), [_plain("All archetypes", color=DK, bold=True)], fill=PALE_SCOPE_BLUE, line_color=DK, line_width=3175, anchor="ctr"))
    out.append(picture(n(), "Picture 2", "rId3", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_approach_header(out, n)
    paint_formula_output_and_chart(out, n)
    paint_formula_inputs_cards_and_table(out, n)
    paint_scope_chip_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Surface incl. MDA)",
    title="TCV to ACV Approach",
    takeaway="Finding Company ACV",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
