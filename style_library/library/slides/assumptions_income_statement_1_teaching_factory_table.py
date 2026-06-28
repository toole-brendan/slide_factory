"""Teaching exemplar: income-statement assumptions methodology table.

ROLE
  methodology_reference / income_statement_poc

USE WHEN
  A slide needs one compact methodology table that documents financial-model line
  items, paired with a short explanatory banner and minimal chrome.

TEACHES
  - native PowerPoint table authored through low-level table()/trow()/tcell_rich()
  - fully inline table styling: border sides, rule colors, bullet indents, and
    rich-cell helpers live in this module rather than in table_kit.py
  - three-column methodology table pattern: Category / Component / Methodology
  - position-driven border rules: dark-navy section rules, slate vertical column
    divider, and gray row separators
  - continuation-category rows, where blank Category cells preserve the visual
    grouping without introducing a row_span
  - RAW layout-placeholder preservation when a source placeholder has no explicit
    xfrm and therefore inherits geometry from the layout
  - a full-width explanatory banner below a reference table

TEXT-FIT PRECEDENT
  methodology_table:
    geometry: 12.338in wide x 3.655in high
    columns: 1.805in Category · 3.216in Component · 7.318in Methodology
    type: Arial 12pt, 100% table paragraph spacing
    content: header row + 1 Revenue row + 4 Direct Costs rows with bulleted
             methodology cells
    copy_when: the slide is a financial-model reference page and the table is
               the main proof, not a supporting exhibit beside a chart
  methodology_bullets:
    geometry: 7.318in Methodology column
    type: Arial 12pt, black, bullet hanging indent 171450 / -171450 EMU
    content: up to three bullets in a 0.955in row
  poc_banner:
    geometry: 12.362in wide x 0.825in high
    type: Arial 12pt bold italic, centered, 100% line spacing
    content: two short centered lines; suitable for an accounting-rule takeaway

SOURCE NOTE
  Teaching rewrite of the source-faithful `assumptions_income_statement_1.py`
  module. The table styling is intentionally inline, as in the teaching rewrite
  of `us_delivery_capacity.py`: edges, border dictionaries, rich cells, label
  paragraphs, and bullet paragraphs are local so an AI author can study the full
  table mechanics in one file. The surrounding slide contract (`LAYOUT`,
  `CHARTS`, `_body()`, `render()`), raw placeholders, table coordinates, POC
  banner, Preliminary chip, and source line are preserved.

FIDELITY NOTE
  This rebuild is intended to render identically to the source-faithful module.
  It keeps the two RAW placeholder shapes byte-for-byte because they have no
  explicit geometry, and it rebuilds the table from semantic row data while
  assigning the same border roles and row-height minima as the source.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, line_break, paragraph, run, table, tcell_rich, text_box,
    tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
DK = "162029"
BLUE_1 = "E2E9EF"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []


TEXT_FIT = {
    "methodology_table": {
        "box_in": (12.338, 3.655),
        "columns_in": (1.805, 3.216, 7.318),
        "font_pt": 12,
        "content": "header + Revenue row + four Direct Costs rows",
        "note": (
            "The Methodology column carries most of the content. Rows with three "
            "bullets use 0.682in or 0.955in minima, while single-bullet rows use "
            "0.409in."
        ),
    },
    "methodology_bullets": {
        "font_pt": 12,
        "bullet_indent_emu": (171_450, -171_450),
        "content": "bulleted cells, one to three bullets per row",
        "note": "This is the slide's dominant text-fit precedent.",
    },
    "poc_banner": {
        "box_in": (12.362, 0.825),
        "font_pt": 12,
        "content": "two centered bold-italic lines",
    },
    "source_line": {
        "box_in": (12.367, 0.317),
        "font_pt": 8,
        "content": "line_break() plus one Source run, matching the source offset.",
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
class TableColumn:
    name: str
    width_in: float
    fit_note: str


@dataclass(frozen=True)
class MethodologyRow:
    category: str | None
    component: str
    bullets: tuple[str, ...]
    height_in: float


class ShapeIds:
    """Tiny id allocator; chrome builders use fixed ids inside deck_core."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones and source constants.
# ════════════════════════════════════════════════════════════════════════════


METHODOLOGY_TABLE = TextZone(
    name="IncomeStatementMethodologyTable",
    box=Box(0.472, 1.115, 12.338, 3.655),
    font_pt=12,
    fit_note="Primary reference table; three columns, six rows including header.",
)

POC_BANNER = TextZone(
    name="POCBanner",
    box=Box(0.472, 4.928, 12.362, 0.825),
    font_pt=12,
    fit_note="Full-width centered accounting-rule takeaway under the table.",
)

SOURCE_LINE = TextZone(
    name="SourceLine",
    box=Box(0.495, 6.681, 12.367, 0.317),
    font_pt=8,
    fit_note="Off-house source line kept at the source slide position.",
)

TABLE_COLUMNS: tuple[TableColumn, ...] = (
    TableColumn("Category", 1.805, "Short section labels; Direct Costs uses blank continuation cells."),
    TableColumn("Component", 3.216, "Income-statement component labels, dark navy."),
    TableColumn("Methodology", 7.318, "Bulleted methodology notes; widest column."),
)

HEADER_LABELS = ("Category:", "Component")
METHODOLOGY_HEADER_RUNS = (
    ("Methodology – ", True, False),
    ("Revenue and Direct Costs recognized on POC basis", False, True),
)

COLUMN_RULE = "79838F"     # slate-gray vertical rule between Component and Methodology
BULLET_MAR_L = 171_450
BULLET_INDENT = -171_450

METHODOLOGY_ROWS: tuple[MethodologyRow, ...] = (
    MethodologyRow(
        category="Revenue (POC)",
        component="Vessel Sale Price",
        bullets=("Container: ~40-44% Gross Margin applied to Direct Costs to set sale price",),
        height_in=0.409,
    ),
    MethodologyRow(
        category="Direct Costs (POC)",
        component="Equipment ",
        bullets=(
            "Assumed to be ~65-75% of Total Equipment + Raw Materials costs",
            "3% YoY increase in equipment costs",
            "5% volume purchase discount applied on equipment",
        ),
        height_in=0.682,
    ),
    MethodologyRow(
        category=None,
        component="Direct Labor",
        bullets=(
            "Production tech labor rate * hours required to build vessel ",
            "5% YoY increase in labor rate ’26-’30; 3% ’31+",
        ),
        height_in=0.682,
    ),
    MethodologyRow(
        category=None,
        component="Direct Labor Fringe",
        bullets=("Fringe rate of 37.6% applied to Direct Labor",),
        height_in=0.409,
    ),
    MethodologyRow(
        category=None,
        component="Raw Materials (Steel)",
        bullets=(
            "Steel portion of hull estimated from LWT in units of MT. Multiplied with $1,200 / MT rate",
            "YoY price changes indexed to S&P steel price forecast",
            "5% volume purchase discount applied on raw materials",
        ),
        height_in=0.955,
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: intentionally local / inline for teaching.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def rich_cell(
    paras,
    *,
    fill=None,
    anchor="ctr",
    span=1,
    rowspan=1,
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    """tcell_rich wrapper: content first, cell mechanics second.

    This mirrors the old local rcell() helper but keeps the mechanics visible:
    fill, spans, vertical anchor, insets, and per-side borders all live here.
    """

    return tcell_rich(
        paras,
        fill=fill,
        grid_span=span,
        row_span=rowspan,
        anchor=anchor,
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=border_dict(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Table-text helpers: keep row construction readable.
# ════════════════════════════════════════════════════════════════════════════
def _tr(text: str, *, size_pt: float = 12, bold: bool = False, italic: bool = False, color: str = BLACK) -> str:
    return trun(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)


def _label_para(text: str, *, bold: bool = False, color: str = DK) -> dict:
    return tpara([_tr(text, bold=bold, color=color)], mar_l=0, indent=0)


def _blank_para() -> dict:
    return tpara([], mar_l=0, indent=0)


def _bullet_para(text: str) -> dict:
    return tpara(
        [_tr(text, color=BLACK)],
        bullet=True,
        mar_l=BULLET_MAR_L,
        indent=BULLET_INDENT,
    )


def _methodology_header_para() -> dict:
    return tpara(
        [
            _tr(text, bold=bold, italic=italic, color=DK)
            for text, bold, italic in METHODOLOGY_HEADER_RUNS
        ],
        mar_l=0,
        indent=0,
    )


def _header_row() -> dict:
    """Header row with dark-navy underline and slate vertical divider."""

    return trow(
        [
            rich_cell([_label_para(HEADER_LABELS[0], bold=True)], anchor="b", B=edge(DK)),
            rich_cell([_label_para(HEADER_LABELS[1], bold=True)], anchor="b", R=edge(COLUMN_RULE), B=edge(DK)),
            rich_cell([_methodology_header_para()], anchor="b", L=edge(COLUMN_RULE), B=edge(DK)),
        ],
        h=IN(0.5),
    )


def _category_cell(row_index: int, row: MethodologyRow):
    """Category column: populated only at group starts; later rows are blanks."""

    if row.category is None:
        return rich_cell([_blank_para()])

    category_edges = {"T": edge(DK)}
    if row_index == 0:
        category_edges["B"] = edge(DK)
    return rich_cell(
        [_label_para(row.category, bold=True)],
        **category_edges,
    )


def _row_rules(row_index: int) -> tuple[dict[str, int | str], dict[str, int | str] | None]:
    """Return top and bottom rules for Component/Methodology cells by position."""

    if row_index == 0:
        return edge(DK), edge(DK)
    if row_index == 1:
        return edge(DK), edge(GRAY_3)
    if row_index == len(METHODOLOGY_ROWS) - 1:
        return edge(GRAY_3), None
    return edge(GRAY_3), edge(GRAY_3)


def _income_statement_row(row_index: int, row: MethodologyRow) -> dict:
    """One table row: text comes from METHODOLOGY_ROWS; borders come from position."""

    top_rule, bottom_rule = _row_rules(row_index)
    component_edges = {"R": edge(COLUMN_RULE), "T": top_rule}
    methodology_edges = {"L": edge(COLUMN_RULE), "T": top_rule}
    if bottom_rule is not None:
        component_edges["B"] = bottom_rule
        methodology_edges["B"] = bottom_rule

    return trow(
        [
            _category_cell(row_index, row),
            rich_cell([_label_para(row.component)], **component_edges),
            rich_cell([_bullet_para(bullet) for bullet in row.bullets], **methodology_edges),
        ],
        h=IN(row.height_in),
    )


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_raw_placeholders(out: list[str]) -> None:
    """Preserve layout-inherited placeholders that have no explicit xfrm."""

    out.append("")
    out.append("")


def paint_methodology_table(out: list[str], ids: ShapeIds) -> None:
    """Paint the Category / Component / Methodology reference table.

    The table mechanics remain inline: row construction assigns the same border
    sides as the source, while METHODOLOGY_ROWS carries just the financial-model
    content. This is intentionally a low-level table rebuild, not a generic
    table abstraction.
    """

    out.append(
        table(
            ids.next(),
            "IncomeStatementMethodologyTable",
            *METHODOLOGY_TABLE.box.emu(),
            col_widths=[IN(column.width_in) for column in TABLE_COLUMNS],
            rows=[
                _header_row(),
                *[_income_statement_row(index, row) for index, row in enumerate(METHODOLOGY_ROWS)],
            ],
        )
    )


def paint_poc_banner(out: list[str], ids: ShapeIds) -> None:
    """Full-width explanatory banner under the table."""

    out.append(
        text_box(
            ids.next(),
            "MethodologyBanner",
            *POC_BANNER.box.emu(),
            [
                paragraph(
                    [
                        run(
                            "Revenue and Direct Costs are recognized on the Income Statement on a Percentage of Completion (POC) basis. Recognition is allocated ratably based on Build Time ",
                            size=PT(12),
                            bold=True,
                            italic=True,
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    align="ctr",
                    line_spacing=100000,
                ),
                paragraph(
                    [
                        run(
                            "(e.g., Build Time = 12 Months, Price = $120M, Monthly Revenue = $10M)",
                            size=PT(12),
                            bold=True,
                            italic=True,
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    align="ctr",
                    line_spacing=100000,
                ),
            ],
            fill=BLUE_1,
            line_color=BLACK,
            anchor="ctr",
            l_ins=91_440,
            t_ins=0,
            r_ins=91_440,
            b_ins=0,
        )
    )


def paint_preliminary_and_source(out: list[str], ids: ShapeIds) -> None:
    """House Preliminary chip plus the source line at its off-house source position."""

    out.append("")
    out.append(
        text_box(
            ids.next(),
            "SourceNote",
            *SOURCE_LINE.box.emu(),
            [
                paragraph(
                    [line_break(), run("Source: S&P Intelligence", size=PT(8), color=BLACK, font=FONT)],
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_raw_placeholders(out)
    paint_methodology_table(out, ids)
    paint_poc_banner(out, ids)
    paint_preliminary_and_source(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="BuildCo Financial Projections",
    topic="Assumptions & Methodology",
    title="Assumptions & Methodology",
    takeaway="Income Statement (1/2).",
)


def render() -> str:
    return body_slide(CHROME, _body())
