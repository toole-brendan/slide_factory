"""Teaching exemplar: market-addressability “must be true” matrix.

ROLE
  strategy_conditions / market_addressability_matrix

USE WHEN
  A slide needs to compare multiple market entry lanes against a shared set of
  vessel classes, while keeping each cell readable as a short list of necessary
  strategic conditions. This pattern uses one native table as the exhibit itself:
  market columns across the top, vessel-class rows down the side, and rich text
  bullets inside the decision cells.

TEACHES
  - a full-slide native table as a strategic matrix, not just a data grid
  - merged row/column headers with row_span and grid_span
  - shaded market columns with explicit white / black / gray rules
  - rich table cells containing bullets, dash sub-bullets, italic caveats, and
    multi-run emphasis
  - local inline table helpers instead of centralized table_kit imports
  - paint-order discipline for chrome -> matrix -> overlay callouts

TEXT-FIT PRECEDENT
  matrix_table:
    geometry: 12.300in wide x 5.000in high
    type: Arial 10pt, single-spaced native-table text
    content: 4 market columns, 6 vessel-class rows, one dense policy-conditions
             cell, one dense Marine Highway cell, plus merged caveat cells
    copy_when: the slide is meant to compare strategic conditions across market
               lanes; keep bullets clause-like and let row/column merges carry
               the structure instead of adding prose outside the table

SOURCE NOTE
  Teaching rewrite of the source-faithful `key_findings_what_must_be_true.py`
  module. There are no charts on this slide; CHARTS is intentionally empty. The
  central artifact is the market x vessel-class native table, with all table
  styling helpers inlined locally so agents can see how borders, spans, fills,
  anchors, and paragraph margins map to OOXML table behavior.

FIDELITY NOTE
  This is a readability refactor of the source-converted slide module. Coordinates,
  paint order, text, paragraph hierarchy, table spans, rules, fills, and the two
  free-floating callouts are preserved from the polished source module.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    table,
    trow,
    tcell,
    tcell_rich,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"
CHARTS: list = []

_SECTION = "Commercial Strategy"
_TOPIC = "Research Overview"
_TITLE = "Key Findings (3/3)"
_TAKEAWAY = "What must be true to succeed (commercial oceangoing focus)."

MARKET_1 = "CEDDEC"
MARKET_2 = "99B9D8"
MARKET_3 = "447BB2"
MARKET_4 = "223E59"
MID_GRAY = "808080"
RULE_GRAY = "808080"


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: useful for agents choosing an exemplar.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "strategy_conditions_matrix",
    "use_when": (
        "Use for a market-addressability or strategic-conditions matrix where "
        "columns are market lanes, rows are offer / vessel classes, and the "
        "body cells contain concise must-be-true bullets."
    ),
    "teaches": [
        "native table as a strategic matrix",
        "row_span and grid_span for multi-level row/column headers",
        "explicit per-cell rules and no-fill omitted sides",
        "rich table paragraphs with bullets and dash sub-bullets",
        "italic caveat cells",
        "inline table styling helpers",
        "overlay callouts painted after the table",
    ],
}

TEXT_FIT = {
    "matrix_table": {
        "box_in": (12.300, 5.000),
        "font_pt": 10,
        "content": (
            "4 market columns x vessel-class rows; dense Marine Highway and "
            "policy-conditions cells with merged caveat cells"
        ),
        "note": (
            "Keep individual bullets short. This table works because row/column "
            "labels carry most of the context and the bullet cells state only "
            "necessary conditions."
        ),
    },
    "addressability_note": {
        "box_in": (3.112, 0.269),
        "font_pt": 10,
        "content": "single centered italic line",
    },
    "further_analysis_callout": {
        "box_in": (2.805, 2.670),
        "font_pt": 10,
        "content": "single centered italic line inside dashed box",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Semantic records: geometry in inches, rich table text as data.
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
class TableZone:
    name: str
    box: Box
    col_widths: tuple[float, ...]
    fit_note: str


@dataclass(frozen=True)
class TextZone:
    name: str
    box: Box
    font_pt: float
    fit_note: str


@dataclass(frozen=True)
class MarketColumn:
    name: str
    description: str
    fill: str
    text_color: str
    description_color: str


@dataclass(frozen=True)
class RunSpec:
    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = BLACK
    size_pt: float = 10


@dataclass(frozen=True)
class ParagraphSpec:
    runs: tuple[RunSpec, ...]
    align: str = "l"
    bullet: bool = False
    bullet_char: str | None = None
    level: int = 0
    mar_l: int | None = None
    indent: int | None = None


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones and matrix columns.
# ════════════════════════════════════════════════════════════════════════════
MATRIX_TABLE = TableZone(
    name="MarketConditionsMatrix",
    box=Box(0.494, 1.495, 12.300, 5.000),
    col_widths=(0.207, 0.804, 2.822, 2.822, 2.822, 2.822),
    fit_note="One native matrix table: two left spine tracks + four market lanes.",
)

ADDRESSABILITY_NOTE = TextZone(
    name="AddressabilityNote",
    box=Box(3.078, 5.442, 3.112, 0.269),
    font_pt=10,
    fit_note="Centered italic overlay note with no fill / no border.",
)

FURTHER_ANALYSIS_CALLOUT = TextZone(
    name="FurtherAnalysisCallout",
    box=Box(7.143, 3.825, 2.805, 2.670),
    font_pt=10,
    fit_note="Dashed overlay box; painted after the table so it sits on top.",
)

MARKET_COLUMNS: tuple[MarketColumn, ...] = (
    MarketColumn("1. Marine Highway", "Displaces domestic truck / rail", MARKET_1, BLACK, BLACK),
    MarketColumn("2. Existing Jones Act Routes", "Current OCONUS routes", MARKET_2, BLACK, BLACK),
    MarketColumn("3. US-Built & Flagged International Trade", "SCF & other USG programs", MARKET_3, GRAY_1, WHITE),
    MarketColumn("4. Foreign-Flagged International Trade", "Ex-SCF foreign trade", MARKET_4, GRAY_1, GRAY_1),
)


# ════════════════════════════════════════════════════════════════════════════
# Rich text data. These constants keep table copy separate from table mechanics.
# ════════════════════════════════════════════════════════════════════════════
def T(
    text: str,
    *,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    color: str = BLACK,
    size_pt: float = 10,
) -> RunSpec:
    """Compact RunSpec constructor; data below reads like marked-up copy."""

    return RunSpec(text, bold=bold, italic=italic, underline=underline, color=color, size_pt=size_pt)


def P(
    *runs: RunSpec,
    align: str = "l",
    bullet: bool = False,
    bullet_char: str | None = None,
    level: int = 0,
    mar_l: int | None = None,
    indent: int | None = None,
) -> ParagraphSpec:
    """A rich table paragraph: runs + paragraph mechanics in one record."""

    return ParagraphSpec(
        runs=tuple(runs),
        align=align,
        bullet=bullet,
        bullet_char=bullet_char,
        level=level,
        mar_l=mar_l,
        indent=indent,
    )


NO_MARGINS = {"mar_l": 0, "indent": 0}
BULLET = {"bullet": True, "mar_l": 112_713, "indent": -112_713}
DASH_SUB_BULLET = {
    "bullet": True,
    "bullet_char": "−",
    "level": 2,
    "mar_l": 227_013,
    "indent": -114_300,
}

ALL_VESSELS_COST_ADVANTAGE = (P(T("Port Alpha drives 30-40%+ lower newbuild costs vs. US-based incumbents"), align="ctr", **NO_MARGINS),)
PA_COMPETITIVENESS_CAVEAT = (P(T("PA prices challenge competitiveness", italic=True), align="ctr", **NO_MARGINS),)

MARINE_HIGHWAY_FEEDER_CONDITIONS = (
    P(T("Jones Act remains in place "), **BULLET),
    P(T("Regulatory environment supports autonomy"), **BULLET),
    P(T("Vessel ITC eligibility extends to domestic"), **BULLET),
    P(T("Autonomy enables revenue growth and/or cost savings that offsets new expenses (i.e., SW license, remote ops. center)"), **BULLET),
    P(T("Marine transport achieves lower end-to-end costs vs. onshore modes"), **BULLET),
    P(T("Terminal access ensures requisite service level (e.g., rapid turns for fast deliveries)"), **BULLET),
)
FEEDER_COMPETITIVENESS_CAVEAT = (
    P(T("Size limits TEU capacity, challenging competitiveness", italic=True), align="ctr", level=2, mar_l=112_713, indent=0),
)
PANAMAX_JONES_ACT_ROUTE_NOTE = (
    P(T("Same considerations as 350’ Maritime Highway", color=DK), align="ctr", **NO_MARGINS),
)
INTERNATIONAL_TRADE_POLICY_CONDITIONS = (
    P(T("SHIPS Act passes with revisions:", bold=True), **BULLET),
    P(T("Universal fee imposed on all cargo imported by foreign-built ships"), **DASH_SUB_BULLET),
    P(T("Subsidies cover full opex and D&A differential between US & foreign"), **DASH_SUB_BULLET),
    P(T("Building Ships in America Act passes with revisions:", bold=True), **BULLET),
    P(T("ITC eligibility increases beyond ‘32 "), **DASH_SUB_BULLET),
    P(T("Tanker Security Program expands:", bold=True), **BULLET),
    P(T("Fleet cap increases to 30 vessels with US-built requirement"), **DASH_SUB_BULLET),
    P(T("Subsidies cover full opex and D&A differential between US & foreign"), **DASH_SUB_BULLET),
)
FOREIGN_FLAGGED_CONDITIONS = (
    P(T("ROK / Japan yards build vessels "), T("(to confirm price) ", italic=True), **BULLET),
    P(T("Autonomy enables revenue growth and/or cost savings that offsets new expenses (i.e., SW license, remote ops. center)"), **BULLET),
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: local by design, not imported from deck_core.table_kit.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def plain_cell(
    text: str = "",
    *,
    fill=None,
    bold=None,
    italic=None,
    color=BLACK,
    size=PT(10),
    align="l",
    anchor="ctr",
    span=1,
    rowspan=1,
    **edges,
):
    """Single-run tcell wrapper: content first, table mechanics second."""

    return tcell(
        text,
        fill=fill,
        bold=bold,
        italic=italic,
        color=color,
        size=size,
        align=align,
        anchor=anchor,
        grid_span=span,
        row_span=rowspan,
        font=FONT,
        borders=border_dict(**edges),
    )


def rich_cell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1, **edges):
    """Multi-paragraph tcell_rich wrapper; spans and borders stay local here."""

    return tcell_rich(
        paras,
        fill=fill,
        grid_span=span,
        row_span=rowspan,
        anchor=anchor,
        borders=border_dict(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Text emitters: convert semantic records into primitive paragraph/run dicts.
# ════════════════════════════════════════════════════════════════════════════
def _table_run(spec: RunSpec):
    return trun(
        spec.text,
        size=PT(spec.size_pt),
        bold=spec.bold or None,
        italic=spec.italic or None,
        underline=spec.underline or None,
        color=spec.color,
        font=FONT,
    )


def _table_para(spec: ParagraphSpec):
    return tpara(
        [_table_run(run_spec) for run_spec in spec.runs],
        align=spec.align,
        bullet=spec.bullet,
        bullet_char=spec.bullet_char,
        level=spec.level,
        mar_l=spec.mar_l,
        indent=spec.indent,
    )


def _paras(specs: tuple[ParagraphSpec, ...] | list[ParagraphSpec]):
    return [_table_para(spec) for spec in specs]


def _label_para(text: str, *, color: str = BLACK, bold: bool = True, align: str = "l"):
    return [_table_para(P(T(text, bold=bold, color=color), align=align, **NO_MARGINS))]


def _body_run(text: str, *, size_pt: float, color: str = BLACK, italic: bool = False):
    return run(text, size=PT(size_pt), italic=italic or None, color=color, font=FONT)


# ════════════════════════════════════════════════════════════════════════════
# Matrix row builders. Keeping rows named by meaning makes the table teachable
# while preserving the exact low-level row/cell mechanics of the source.
# ════════════════════════════════════════════════════════════════════════════
def _market_header_row():
    market3, market4 = MARKET_COLUMNS[2], MARKET_COLUMNS[3]
    return trow(
        [
            plain_cell("Market:", size=PT(10), italic=True, align="r", span=2),
            plain_cell(
                MARKET_COLUMNS[0].name,
                size=PT(10),
                bold=True,
                align="ctr",
                fill=MARKET_COLUMNS[0].fill,
                anchor="b",
                R=edge(WHITE),
                B=edge(WHITE),
            ),
            plain_cell(
                MARKET_COLUMNS[1].name,
                size=PT(10),
                bold=True,
                color=BLACK,
                align="ctr",
                fill=MARKET_COLUMNS[1].fill,
                anchor="b",
                L=edge(WHITE),
                R=edge(WHITE),
                B=edge(WHITE),
            ),
            rich_cell(
                _label_para(market3.name, color=market3.text_color, align="ctr"),
                fill=market3.fill,
                anchor="b",
                L=edge(WHITE),
                R=edge(WHITE),
                B=edge(WHITE),
            ),
            rich_cell(
                _label_para(market4.name, color=market4.text_color, align="ctr"),
                fill=market4.fill,
                anchor="b",
                L=edge(WHITE),
                B=edge(WHITE),
            ),
        ],
        h=IN(0),
    )


def _description_row():
    market1, market3, market4 = MARKET_COLUMNS[0], MARKET_COLUMNS[2], MARKET_COLUMNS[3]
    return trow(
        [
            plain_cell("Description:", size=PT(10), italic=True, align="r", span=2, B=edge(BLACK)),
            rich_cell(
                _paras((P(T(market1.description, italic=True), align="ctr", **NO_MARGINS),)),
                fill=market1.fill,
                R=edge(WHITE),
                T=edge(WHITE),
                B=edge(BLACK),
            ),
            plain_cell(
                MARKET_COLUMNS[1].description,
                size=PT(10),
                italic=True,
                color=BLACK,
                align="ctr",
                fill=MARKET_COLUMNS[1].fill,
                L=edge(WHITE),
                R=edge(WHITE),
                T=edge(WHITE),
                B=edge(BLACK),
            ),
            rich_cell(
                _paras((P(T(market3.description, italic=True, color=market3.description_color), align="ctr", **NO_MARGINS),)),
                fill=market3.fill,
                L=edge(WHITE),
                R=edge(WHITE),
                T=edge(WHITE),
                B=edge(BLACK),
            ),
            rich_cell(
                _paras((P(T(market4.description, italic=True, color=market4.description_color), align="ctr", **NO_MARGINS),)),
                fill=market4.fill,
                L=edge(WHITE),
                T=edge(WHITE),
                B=edge(BLACK),
            ),
        ],
        h=IN(0),
    )


def _all_vessels_row():
    thick_top = edge(BLACK)
    gray_bottom = edge(RULE_GRAY, 6_350)
    return trow(
        [
            rich_cell(_label_para("All Vessels"), span=2, T=thick_top, B=gray_bottom),
            rich_cell(_paras(ALL_VESSELS_COST_ADVANTAGE), span=3, T=thick_top, B=gray_bottom),
            rich_cell(_paras(PA_COMPETITIVENESS_CAVEAT), fill=GRAY_1, T=thick_top, B=gray_bottom),
        ],
        h=IN(0),
    )


def _container_feeder_row():
    gray_rule = edge(RULE_GRAY, 6_350)
    return trow(
        [
            rich_cell(_label_para("Container", align="ctr"), fill=GRAY_3, rowspan=2, T=gray_rule, B=gray_rule),
            rich_cell(_label_para("350’ Feeder"), T=gray_rule, B=gray_rule),
            rich_cell(_paras(MARINE_HIGHWAY_FEEDER_CONDITIONS), T=gray_rule, B=gray_rule),
            rich_cell(_paras(FEEDER_COMPETITIVENESS_CAVEAT), fill=GRAY_1, span=3, T=gray_rule, B=gray_rule),
        ],
        h=IN(0.625),
    )


def _panamax_policy_row():
    gray_rule = edge(RULE_GRAY, 6_350)
    return trow(
        [
            rich_cell(_label_para("900’ Panamax"), T=gray_rule, B=gray_rule),
            rich_cell([tpara([], align="ctr", mar_l=0, indent=0)], fill=GRAY_1, rowspan=3, T=gray_rule),
            rich_cell(_paras(PANAMAX_JONES_ACT_ROUTE_NOTE), T=gray_rule, B=gray_rule),
            rich_cell(_paras(INTERNATIONAL_TRADE_POLICY_CONDITIONS), rowspan=3, T=gray_rule),
            rich_cell(_paras(FOREIGN_FLAGGED_CONDITIONS), rowspan=3, T=gray_rule),
        ],
        h=IN(0.14),
    )


def _tanker_product_row():
    gray_rule = edge(RULE_GRAY, 6_350)
    return trow(
        [
            rich_cell(_label_para("Tanker", color=WHITE, align="ctr"), fill=MID_GRAY, rowspan=2, T=gray_rule),
            rich_cell(_label_para("Product"), T=gray_rule, B=gray_rule),
            rich_cell([tpara([], align="ctr", mar_l=0, indent=0)], fill=GRAY_1, rowspan=2, T=gray_rule),
        ],
        h=IN(0),
    )


def _tanker_crude_row():
    gray_rule = edge(RULE_GRAY, 6_350)
    return trow(
        [
            rich_cell(_label_para("Crude"), T=gray_rule),
        ],
        h=IN(0.83),
    )


def _matrix_rows():
    return [
        _market_header_row(),
        _description_row(),
        _all_vessels_row(),
        _container_feeder_row(),
        _panamax_policy_row(),
        _tanker_product_row(),
        _tanker_crude_row(),
    ]


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(out: list[str]) -> None:
    out.append(breadcrumb(_SECTION, _TOPIC))
    out.append(title_placeholder(_TITLE, _TAKEAWAY))
    out.append(prelim_chip())


def paint_matrix(out: list[str], ids: ShapeIds) -> None:
    # col_widths are column tracks; row builders carry spans, anchors, insets,
    # and rules. Every border side not listed renders as explicit no-fill.
    out.append(
        table(
            ids.next(),
            "Table 4",
            *MATRIX_TABLE.box.emu(),
            col_widths=[IN(width) for width in MATRIX_TABLE.col_widths],
            rows=_matrix_rows(),
        )
    )


def paint_callouts(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "TextBox 7",
            *ADDRESSABILITY_NOTE.box.emu(),
            [
                paragraph(
                    [_body_run("To determine market addressability", size_pt=10, italic=True, color=DK)],
                    align="ctr",
                    mar_l=0,
                    indent=0,
                    space_after=0,
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 10",
            *FURTHER_ANALYSIS_CALLOUT.box.emu(),
            [
                paragraph(
                    [_body_run("Further analysis required to determine attractiveness for OpCo", size_pt=10, italic=True)],
                    align="ctr",
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color=BLACK,
            dashed_line=True,
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    paint_chrome(out)
    paint_matrix(out, ids)
    paint_callouts(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
