"""slide1_outsourced_bc_walk — DDG-only outsourced Basic Construction walk.

Walk from total DDG-51 ship spend down to outsourced Basic Construction, paired
with a step-by-step rationale ledger. This DDG-only version expands the DDG waterfall chart across the
full original two-chart exhibit area. Anatomy, in paint order (back to front),
mirrors the layer sections in ``_body()``:

  1. tables ............ rationale ledger (right) + walk title bar (left)
  2. walk chart ........ one native stacked-bar waterfall (``CHARTS`` -> rId2 DDG)
  3. step rules ........ dashed per-step tick marks + coloured outsourced-BC end cap
  4. chart labels ...... footnote marker, DDG program chip, ``IN_YEAR_LABELS``
  5. source line
  6. callout ........... annualized outsourced-BC ``~$1.1B`` badge
  7. walk axis ......... ``WALK_STEP_LABELS`` + prime AP/LLTM label

The native walk chart is built by ``_walk_chart()`` from transcribed DDG source
values (no converter sidecars). The DDG overlays are scaled from the original
left chart into the full two-chart span so the chart fills the gap left by the
removed second exhibit.
"""

from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, bar_chart, body_slide, connector, graphic_frame, line_break,
    paragraph, run, table, tcell, tcell_rich, text_box, tpara, trow, trun,
)


LAYOUT = "slideLayout4"

# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
FONT = "Arial"

# Semantic colors from the source chart/table walk.
TOTAL_SHIP_SPEND = "79838F"
GFE_REMOVAL = "AFC2CC"
OTHER_NON_BC_REMOVAL = "89A2B0"
PRIME_BC_REMOVAL = "486D82"
PRIME_AP_LLTM = "1D4D68"
OUTSOURCED_BC = DK
RULE_GRAY = "808080"

TEACHING_METADATA = {
    "role": "cost_walk / outsourced_basic_construction_bridge",
    "use_when": (
        "Use when a slide needs to walk total ship spend through non-addressable "
        "deductions into outsourced basic construction for DDG-51."
    ),
    "rebuild_strategy": (
        "replace converter-era styled_chart XML/XLSB sidecars with native "
        "bar_chart(mode='stacked') waterfall-style specs"
    ),
    "teaches": (
        "horizontal stacked-bar waterfall bridge",
        "hidden-offset series for step-down bars",
        "manual step labels for a single expanded DDG chart",
        "off-house source line preservation",
        "right rationale ledger paired with left chart walk",
    ),
}

WALK_STEPS: tuple[str, ...] = (
    "Total Ship Spend",
    "Less: GFE",
    "Less: Other non-BC",
    "Basic Construction",
    "Less: Prime BC",
    "Less: Prime AP/LLTM",
    "Outsourced BC",
)

SOURCE_PLOT_LAYOUT = {
    "x": 0.030057803468208091,
    "y": 0.052052785923753668,
    "w": 0.93988439306358385,
    "h": 0.89589442815249265,
}


def _walk_chart(
    *,
    offset_values: list[float | None],
    total_values: list[float | None],
    reduction_values: list[float | None],
    value_axis_max: float,
    hide_total_label_points: tuple[int, ...] = (),
    ap_lltm_values: list[float | None] | None = None,
) -> dict:
    """Editable horizontal waterfall-style walk, rebuilt with native bar_chart().

    The source chart used a two-series think-cell-like native bar chart. The
    current factory expresses the same visible grammar more readably as hidden
    offsets + visible total/subtotal bars + visible removal bars, with AP/LLTM
    as a separate patterned top segment only where it exists in the DDG chart.
    """

    series: list[dict] = [
        {
            "name": "Hidden offsets",
            "values": offset_values,
            "no_fill": True,
            "hide_labels": True,
        },
        {
            "name": "Total / subtotal / outsourced BC",
            "values": total_values,
            "color": TOTAL_SHIP_SPEND,
            "data_point_colors": [
                TOTAL_SHIP_SPEND, None, None, TOTAL_SHIP_SPEND, None, None, OUTSOURCED_BC,
            ],
            "hide_label_points": list(hide_total_label_points),
        },
    ]
    if ap_lltm_values is not None:
        series.append({
            "name": "Prime AP/LLTM included in total spend",
            "values": ap_lltm_values,
            "pattern": {"prst": "ltUpDiag", "fg": BLACK, "bg": WHITE},
            "hide_labels": True,
        })
    series.append({
        "name": "Removal steps",
        "values": reduction_values,
        "color": PRIME_BC_REMOVAL,
        "data_point_colors": [
            None, GFE_REMOVAL, OTHER_NON_BC_REMOVAL, None, PRIME_BC_REMOVAL, None, None,
        ],
    })

    return bar_chart(
        mode="stacked",
        categories=list(WALK_STEPS),
        series=series,
        show_legend=False,
        show_cat_labels=False,
        show_value_axis_labels=False,
        show_gridlines=False,
        show_value_labels=True,
        value_axis_format="General",
        value_label_format="#,##0;#,##0",
        value_label_size_pt=10,
        value_label_bold=False,
        cat_label_size_pt=10,
        gap_width=80,
        bar_overlap=100,
        seg_line_color=None,
        axis_line_color=DK,
        axis_line_width=9_525,
        value_axis_line_color="none",
        value_axis_min=0,
        value_axis_max=value_axis_max,
        value_axis_position="t",
        cat_axis_crosses="min",
        value_axis_crosses="min",
        plot_layout=dict(SOURCE_PLOT_LAYOUT),
        cat_header="Bridge step",
    )


# DDG-51 walk. AP/LLTM is a patterned segment on the total-spend bar, matching
# the source chart part.
DDG_WALK_DATA = {
    "offset_values": [None, 24.866334960000003, 22.590654890000003, None, 6.4217296800000021, None, None],
    "total_values": [36.592092200000003, None, None, 22.590654890000003, None, None, 6.4217296800000057],
    "reduction_values": [None, 12.76808724, 2.2756800699999999, None, 16.168925210000001, None, None],
    "ap_lltm_values": [1.0423299999999998, None, None, None, None, None, None],
    "value_axis_max": 37.634422200000003,
    "hide_total_label_points": (3,),
}

_CHART0_DATA = {
    "categories": WALK_STEPS,
    "series": [
        {"name": "Hidden offsets", "values": DDG_WALK_DATA["offset_values"]},
        {"name": "Total / subtotal / outsourced BC", "values": DDG_WALK_DATA["total_values"]},
        {"name": "Prime AP/LLTM included in total spend", "values": DDG_WALK_DATA["ap_lltm_values"]},
        {"name": "Removal steps", "values": DDG_WALK_DATA["reduction_values"]},
    ],
}

CHARTS = [
    _walk_chart(**DDG_WALK_DATA),
]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets, borders,
#    spans). Renders identically to raw tcell()/tcell_rich(); hand-polish the cells from here. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


def edge(color, w=12700):
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", vert=None, span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, vert=vert, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", vert=None, span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor, vert=vert,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ════════════════════════════════════════════════════════════════════════════
# Overlay records — one frozen dataclass per repeated-shape cluster (inches;
# converted to EMU at emit). Field order matches the source tuples.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class StepTick:
    """A short dashed rule marking one walk-step level on a chart."""
    name: str
    x: float
    y: float


@dataclass(frozen=True)
class InYearLabel:
    """An italic "In-Year" / "AP/LLTM" caption above a chart bar."""
    x: float
    text: str


@dataclass(frozen=True)
class WalkStepLabel:
    """A left-axis label naming one walk step (Total Ship Spend, Less: GFE, ...)."""
    y: float
    text: str


# ── shared overlay geometry (inches + EMU) ──
# The source DDG chart occupied the left 3.003in chart frame. In this DDG-only
# version, the DDG chart spans the full original two-chart exhibit width; chart
# overlays are scaled horizontally by the same factor.
SOURCE_DDG_CHART_X, SOURCE_DDG_CHART_W = 1.556, 3.003
DDG_CHART_X, DDG_CHART_Y, DDG_CHART_W, DDG_CHART_H = 1.556, 1.981, 6.056, 4.736
_DDG_SPAN_SCALE = DDG_CHART_W / SOURCE_DDG_CHART_W


def _span_x(source_x: float) -> float:
    """Map an x-position from the original DDG chart to the expanded DDG chart."""

    return DDG_CHART_X + (source_x - SOURCE_DDG_CHART_X) * _DDG_SPAN_SCALE


def _span_box_x(source_x: float, width: float) -> float:
    """Map a fixed-width label box by preserving its source chart-relative centre."""

    return _span_x(source_x + width / 2) - width / 2


STEP_TICK_H = IN(0.269)                                  # dashed step-rule length
IN_YEAR_W_IN, IN_YEAR_H_IN = 0.875, 0.186
IN_YEAR_Y, IN_YEAR_W, IN_YEAR_H = IN(2.009), IN(IN_YEAR_W_IN), IN(IN_YEAR_H_IN)
STEP_LBL_X, STEP_LBL_W, STEP_LBL_H = IN(0.495), IN(1.531), IN(0.241)


# Dashed per-step tick rules, top→bottom, one per DDG walk-step transition.
STEP_TICKS_DDG = [
    StepTick("Straight Connector 27", _span_x(4.469), 2.698),
    StepTick("Straight Connector 28", _span_x(3.51), 3.304),
    StepTick("Straight Connector 36", _span_x(3.34), 3.91),
    StepTick("Straight Connector 37", _span_x(3.34), 4.517),
    StepTick("Straight Connector 38", _span_x(2.127), 5.123),
    StepTick("Straight Connector 39", _span_x(2.127), 5.729),
]


# ── repeated-shape data (verbatim source tuples wrapped in typed records) ──
IN_YEAR_LABELS = [InYearLabel(*_t) for _t in [
    (_span_box_x(2.813, IN_YEAR_W_IN), "In-Year"),
    (_span_box_x(3.85, IN_YEAR_W_IN), "AP/LLTM"),
]]

WALK_STEP_LABELS = [WalkStepLabel(*_t) for _t in [
    (2.403, "Total Ship Spend"),
    (3.01, "Less: GFE"),
    (3.618, "Less: Other non-BC"),
    (4.226, "Basic Construction"),
    (4.835, "Less: Prime BC"),
    (6.05, "Outsourced BC"),
]]


# ── emit helpers — one record -> one primitive call (n = sequential id source) ──
def _step_tick(n, s):
    return connector(n(), s.name, IN(s.x), IN(s.y), IN(0), STEP_TICK_H,
                     color=DK, width=3175, dash="lgDash")


def _in_year_label(n, l):
    return text_box(n(), "Label", IN(l.x), IN_YEAR_Y, IN_YEAR_W, IN_YEAR_H,
                    [paragraph([run(l.text, size=PT(8.5), italic=True, color=BLACK, font=FONT)],
                               align="ctr")],
                    fill=None, line_color="none", anchor="b",
                    l_ins=0, t_ins=0, r_ins=0, b_ins=0)


def _walk_step_label(n, l):
    return text_box(n(), "Label", STEP_LBL_X, IN(l.y), STEP_LBL_W, STEP_LBL_H,
                    [paragraph([run(l.text, size=PT(9), color=BLACK, font=FONT)], align="l")],
                    fill=None, line_color="none", anchor="ctr",
                    l_ins=0, t_ins=0, r_ins=0, b_ins=0)


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids

    # ── Layer 1 · rationale ledger (right) + walk title bar (left) ──
    out.append(table(n(), "StepRationaleLedger", IN(8.131), IN(1.385), IN(4.703), IN(5.332), col_widths=[IN(1.401), IN(3.301)], rows=[
        trow([cell("Step", size=PT(9), bold=True, color=BLACK, B=edge(BLACK)), cell("Rationale", size=PT(9), bold=True, color=BLACK, B=edge(BLACK))], h=IN(0)),
        trow([cell("Total Ship Spend", size=PT(9), bold=True, color=WHITE, fill="79838F", T=edge(BLACK), B=edge(WHITE, 6350)), rcell([tpara([trun("In-Year Spend:", size=PT(9), bold=True, underline=True, color=BLACK, font=FONT), trun(" FY2022–FY2027 SCN end cost (P-5c discretionary); OBBBA adds two FY2026 DDG-51s ($5.4B).", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875), tpara([trun("Advanced Procurement / Long-Lead Time Materials:", size=PT(9), bold=True, underline=True, color=BLACK, font=FONT), trun(" ", size=PT(9), bold=True, color=BLACK, font=FONT), trun("DDG-51 adds incremental FY2026 AP/LLTM ($1.8B); supplier long-lead materials are kept in the DDG outsourced-BC pool.", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875)], T=edge(BLACK), B=edge("808080", 6350))], h=IN(1.2)),
        trow([cell("Less: Government-Furnished Equipment", size=PT(9), bold=True, color=BLACK, fill="AFC2CC", T=edge(WHITE, 6350), B=edge(WHITE, 6350)), rcell([tpara([trun("Removes GFE (propulsion, electronics, and ordnance) the Navy buys directly and furnished to Primes ", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875), tpara([trun("GFE is non-addressable to outsourced Basic Construction players", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.65)),
        trow([cell("Less: Other non-BC", size=PT(9), bold=True, color=WHITE, fill="89A2B0", T=edge(WHITE, 6350), B=edge(WHITE, 6350)), rcell([tpara([trun("Removes engineering and program costs (", size=PT(9), color=BLACK, font=FONT), trun("e.g., plans, change orders, and other non-construction activities) ", size=PT(9), color=BLACK, font=FONT), trun("as these generally conducted by Primes", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.7)),
        trow([cell("Basic Construction", size=PT(9), bold=True, color=WHITE, fill="79838F", T=edge(WHITE, 6350), B=edge(WHITE, 6350)), cell("Calculation", size=PT(9), italic=True, color=BLACK, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.279)),
        trow([cell("Less: Prime BC", size=PT(9), bold=True, color=WHITE, fill="486D82", T=edge(WHITE, 6350), B=edge(WHITE, 6350)), rcell([tpara([trun("Removes construction the Primes perform in their own yards.", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875, line_spacing=115000), tpara([trun("BC spend x the announced outside-yard share from DoD award place-of-performance data: ~25% DDG-51 (FY22 ships 22%).", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875, line_spacing=115000)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.788)),
        trow([cell("Less: Prime AP/LLTM", size=PT(9), bold=True, color=WHITE, fill="1D4D68", T=edge(WHITE, 6350), B=edge(WHITE, 6350)), rcell([tpara([trun("DDG-51:", size=PT(9), bold=True, underline=True, color=BLACK, font=FONT), trun(" The P-10 EOQ base is vendor-purchased material, so Primes retain none — $0 removed; the full $1.0B flows to Outsourced BC.", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875, line_spacing=115000)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.711)),
        trow([cell("Outsourced BC", size=PT(9), bold=True, color=WHITE, fill=DK, T=edge(WHITE, 6350)), cell("Calculation", size=PT(9), italic=True, color=BLACK, T=edge("808080", 6350))], h=IN(0.3)),
    ]))
    out.append(table(n(), "StepRationaleLedger", IN(0.495), IN(1.385), IN(7.341), IN(0.258), col_widths=[IN(7.341)], rows=[
        trow([rcell([tpara([trun("Walk to Outsourced Basic Construction Spend ($B, cumulative FY22-FY27, FY26 $)", size=PT(9), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=115000, space_before=0, space_after=0)], B=edge(BLACK))], h=IN(0)),
    ]))

    # ── Layer 2 · native waterfall walk chart (rId2 DDG, expanded across old two-chart span) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(DDG_CHART_X), y=IN(DDG_CHART_Y), cx=IN(DDG_CHART_W), cy=IN(DDG_CHART_H), rId="rId2"))

    # ── Layer 3 · dashed per-step tick rules + coloured outsourced-BC end cap ──
    for _s in STEP_TICKS_DDG:
        out.append(_step_tick(n, _s))
    out.append(text_box(n(), "Rectangle 48", IN(_span_x(2.123)), IN(5.392), IN(0.007), IN(0.337), [paragraph([], align="ctr", line_spacing=100000)], fill="1D4D68", line_color="none", anchor="ctr"))

    # ── Layer 4 · chart annotations (footnote marker, DDG program chip, in-year labels) ──
    out.append(text_box(n(), "Text Placeholder 25", IN(_span_box_x(4.372, 0.115)), IN(2.446), IN(0.115), IN(0.167), [paragraph([run("1", size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr", wrap="none", vert="horz", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "ProgramChip", IN(DDG_CHART_X + (DDG_CHART_W - 2.078) / 2), IN(1.736), IN(2.078), IN(0.217), [paragraph([run("DDG-51", size=PT(9), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color=BLACK, anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for _l in IN_YEAR_LABELS:
        out.append(_in_year_label(n, _l))

    # ── Layer 5 · source line ──
    out.append(text_box(n(), "Sources", IN(0.495), IN(6.696), IN(12.339), IN(0.346), [paragraph([run("Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and PB27 FYDP outyears (FY28–FY31); FY26, PL 119-21 Sec. 20002; OUSD(C) Green Book Procurement deflators; Navy Shipbuilding Plan; PB27 SCN Exhibit P-10, LI 2122 (AP/LLTM Ship Construction EOQ); DoD contract award announcements (announced place-of-performance)", size=PT(8), color=DK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))

    # ── Layer 6 · annualized outsourced-BC callout ──
    out.append(text_box(n(), "AnnualizedCallout", IN(_span_box_x(3.273, 1.258)), IN(5.714), IN(1.258), IN(0.47), [paragraph([run("~$1.1B", size=PT(14), bold=True, color=BLACK, font=FONT)], align="ctr", space_after=20), paragraph([run("annualized", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color=BLACK, anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    # ── Layer 7 · walk axis (step labels, prime AP/LLTM label) ──
    for _l in WALK_STEP_LABELS:
        out.append(_walk_step_label(n, _l))
    out.append(text_box(n(), "StepLabel", IN(0.495), IN(5.443), IN(1.531), IN(0.241), [paragraph([run("Less: Prime", size=PT(9), color=BLACK, font=FONT), line_break(), run("AP/LLTM", size=PT(9), color=BLACK, font=FONT)], align="l")], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    return "".join(out)


CHROME = Chrome(
    section="Executive Summary",
    topic="Supplier TAM and SAM",
    title="Outsourced Basic Construction",
    takeaway=(
        "Across FY22-FY27, total ship spend narrows to an annualized ~$1.1B "
        "of outsourced work for DDG-51."
    ),
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
