"""Teaching exemplar: income-statement assumptions methodology slide (2/2).

ROLE
  methodology_reference / operating_expense_assumptions

USE WHEN
  A slide needs a dense model-assumptions reference table: one category spine,
  component rows, methodology bullet lists, visible section/column rules, and a
  small source note. This is the operating-expense sibling of the Income
  Statement (1/2) methodology table.

TEACHES
  - one large native table as a reference-document surface
  - explicit inline table styling without importing deck_core.table_kit
  - component rows generated from semantic assumption records
  - section-opening, interior, and open-foot row-rule grammar
  - methodology bullet lists inside tcell_rich()/tpara()/trun()
  - raw layout-placeholder residue kept isolated and documented
  - source footnote kept as a normal text_box at source geometry

TEXT-FIT PRECEDENT
  operating_expense_assumptions_table:
    geometry: 12.338in wide x 5.395in high
    type: Arial 12pt, DK component labels, black methodology bullets
    content: header + 12 visible component rows; methodology cells carry up to
             three bullet paragraphs
    copy_when: a dense appendix table must document modelling inputs line-by-line
               while preserving native table editability
  source_note:
    geometry: 12.367in wide x 0.317in high
    type: Arial 8pt source line preceded by a soft line break
    copy_when: source text sits off the house source placeholder and must remain
               visually aligned with a manually-created source slide

SOURCE NOTE
  Teaching rewrite of the source-faithful `assumptions_income_statement_2.py`
  module. The slide remains a native-table build plus two raw layout placeholders
  and one source text box. All table styling lives in this module: border helpers,
  table-style records, row-rule choices, insets, and rich-cell builders are local.

FIDELITY NOTE
  This is an authoring/readability refactor, not a visual redesign. Geometry,
  row heights, column widths, cell insets, table rules, raw placeholder XML,
  source note, Preliminary chip, shape ids, and paint order are preserved from
  the hand-polished source module. The category label is deliberately rendered in
  the first category cell with blank cells below, matching the source output.
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
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: slide-level guidance AI authors can inspect.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "methodology_reference_operating_expenses",
    "use_when": (
        "Use for a dense financial-model assumptions appendix where each line "
        "item needs a component label and one or more methodology bullets."
    ),
    "teaches": [
        "large native assumptions table",
        "inline table styling helpers",
        "semantic component-row records",
        "section/header/interior/open-foot border grammar",
        "bulleted methodology paragraphs in rich cells",
        "raw layout-placeholder containment",
        "off-house source-note preservation",
    ],
}

TEXT_FIT = {
    "operating_expense_assumptions_table": {
        "box_in": (12.338, 5.395),
        "font_pt": 12,
        "content": "header + 12 component rows; the Facilities row has three bullets",
        "note": (
            "Rows are intentionally tight. Keep methodology bullets short; add a "
            "third bullet only when the row height is at least the Facilities precedent."
        ),
    },
    "source_note": {
        "box_in": (12.367, 0.317),
        "font_pt": 8,
        "content": "one source line after a leading line break",
        "note": "Kept off the house source placeholder to match the source slide.",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records: geometry, rich table text, rows, and table style.
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
class TableRun:
    """One rich-text run inside a native-table cell."""

    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = BLACK
    size_pt: float = 12


@dataclass(frozen=True)
class TableParagraph:
    """One native-table paragraph; bullet geometry is kept with the content."""

    runs: tuple[TableRun, ...]
    bullet: bool = False
    bullet_char: str | None = None
    mar_l: int | None = None
    indent: int | None = None
    end_size_pt: float | None = None


@dataclass(frozen=True)
class AssumptionRow:
    """One component row in the Operating Expenses table."""

    component: str
    bullets: tuple[str, ...]
    row_h: float
    category_label: str | None = None
    opens_section: bool = False
    closes_section: bool = False


@dataclass(frozen=True)
class AssumptionsTableStyle:
    """All visible table styling choices, kept inline as teaching material."""

    label_color: str = DK
    body_color: str = BLACK
    section_rule_color: str = DK
    row_rule_color: str = GRAY_3
    column_rule_color: str = "79838F"
    rule_width: int = 12_700
    cell_l_ins: int = 45_720
    cell_r_ins: int = 45_720
    cell_t_ins: int = 45_720
    cell_b_ins: int = 45_720


@dataclass(frozen=True)
class AssumptionsTable:
    """The full Category / Component / Methodology table specification."""

    name: str
    box: Box
    col_widths: tuple[float, float, float]
    header_h: float
    style: AssumptionsTableStyle
    rows: tuple[AssumptionRow, ...]




@dataclass(frozen=True)
class SourceNote:
    name: str
    box: Box
    text: str
    font_pt: float = 8


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: intentionally inline, not imported from table_kit.py.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(L=None, R=None, T=None, B=None):
    """Border map from only the sides drawn; omitted sides render as no-fill."""

    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def rich_cell(
    paras,
    *,
    fill=None,
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    l_ins: int = 45_720,
    r_ins: int = 45_720,
    t_ins: int = 45_720,
    b_ins: int = 45_720,
    **edges,
):
    """Multi-paragraph native-table cell: content first, mechanics second."""

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
# Text helpers: local defaults keep the table data readable.
# ════════════════════════════════════════════════════════════════════════════
def tr(
    text: str,
    *,
    b: bool = False,
    i: bool = False,
    u: bool = False,
    color: str = BLACK,
    size_pt: float = 12,
) -> TableRun:
    """One table run; defaults match the source slide's PT12 Arial table."""

    return TableRun(text, bold=b, italic=i, underline=u, color=color, size_pt=size_pt)


def plain_para(*runs: TableRun, mar_l: int | None = 0, indent: int | None = 0) -> TableParagraph:
    """A non-bulleted table paragraph; labels usually pin mar_l/indent to zero."""

    return TableParagraph(tuple(runs), mar_l=mar_l, indent=indent)


def bullet_para(text: str, *, color: str = BLACK) -> TableParagraph:
    """A methodology bullet paragraph using the slide's 0.1875in hanging indent."""

    return TableParagraph((tr(text, color=color),), bullet=True, mar_l=171_450, indent=-171_450)


def empty_para() -> TableParagraph:
    """Runless spacer paragraph; PT1 end size keeps blank category cells compact."""

    return TableParagraph(tuple(), mar_l=0, indent=0, end_size_pt=1)


def _table_run_xml(spec: TableRun) -> dict:
    return trun(
        spec.text,
        size=PT(spec.size_pt),
        bold=spec.bold or None,
        italic=spec.italic or None,
        underline=spec.underline or None,
        color=spec.color,
        font=FONT,
    )


def _table_para_xml(spec: TableParagraph) -> dict:
    return tpara(
        [_table_run_xml(run_spec) for run_spec in spec.runs],
        bullet=spec.bullet,
        bullet_char=spec.bullet_char,
        mar_l=spec.mar_l,
        indent=spec.indent,
        end_size=PT(spec.end_size_pt) if spec.end_size_pt is not None else None,
    )


def _box_run(text: str, *, size_pt: float = 8, color: str = BLACK) -> str:
    return run(text, size=PT(size_pt), color=color, font=FONT)


# ════════════════════════════════════════════════════════════════════════════
# Raw title placeholders. They carry no explicit xfrm and bind to layout geometry,
# so the source-faithful module keeps them as literal OOXML.
# ════════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════════
# Table content: rows are semantic; table styling is applied by row role.
# ════════════════════════════════════════════════════════════════════════════
OPERATING_EXPENSE_ROWS: tuple[AssumptionRow, ...] = (
    AssumptionRow(
        component="Compensation",
        bullets=(
            "Bucketed across R&D Engineers, Manufacturing OH, G&A, and S&M",
            "5% YoY increase in rates",
        ),
        row_h=0.426,
        category_label="Operating Expenses",
        opens_section=True,
    ),
    AssumptionRow(component="Professional Services", bullets=("6-7% of revenue",), row_h=0.274),
    AssumptionRow(component="Fringe", bullets=("Fringe rate of 37.6% applied to Compensation",), row_h=0.274),
    AssumptionRow(component="Legal", bullets=("1.5-2.2% of revenue (decreases over time)",), row_h=0.274),
    AssumptionRow(component="IT & Software", bullets=("$25K / head in R&D. 5% YoY increase",), row_h=0.283),
    AssumptionRow(
        component="D&A",
        bullets=(
            "Construction depreciated over 40-yr. useful life",
            "Equipment depreciated over 15-yr. useful life",
        ),
        row_h=0.283,
    ),
    AssumptionRow(
        component="SBC",
        bullets=("10% rate applied to Compensation – extra incentives for hiring. Added back in Cash Flows",),
        row_h=0.283,
    ),
    AssumptionRow(
        component="Travel & Entertainment",
        bullets=("$12K / head in R&D and G&A. $60K / head in S&M. 5% YoY increase",),
        row_h=0.283,
    ),
    AssumptionRow(component="Equipment & Material Maintenance", bullets=("~1-2% of cumulative Capex",), row_h=0.283),
    AssumptionRow(
        component="Facilities",
        bullets=(
            "Utilities, Building Maintenance, Janitorial, Property Taxes, Other rates applied on a per sqft. Basis. Collectively $17 / sqft",
            "5% YoY increase (except Property Taxes - ~1%)",
            "Land Lease also included in cost at $7,500 / acre (rate kept constant YoY)",
        ),
        row_h=0.283,
    ),
    AssumptionRow(component="Marketing, PR, Events", bullets=("1.5-2% of revenue (decreases over time)",), row_h=0.395),
    AssumptionRow(
        component="Insurance",
        bullets=(
            "Applied on a per sqft basis - $1.20 / sqft",
            "5% YoY increase",
        ),
        row_h=0.395,
        closes_section=True,
    ),
)

ASSUMPTIONS_TABLE_STYLE = AssumptionsTableStyle()

ASSUMPTIONS_TABLE = AssumptionsTable(
    name="Table 3",
    box=Box(0.389, 1.146, 12.338, 5.395),
    col_widths=(1.805, 3.216, 7.317),
    header_h=0.5,
    style=ASSUMPTIONS_TABLE_STYLE,
    rows=OPERATING_EXPENSE_ROWS,
)

SOURCE_NOTE = SourceNote(
    name="Rectangle 8",
    box=Box(0.495, 6.681, 12.367, 0.317),
    text="Source: Internal Saronic data and estimates",
)


# ════════════════════════════════════════════════════════════════════════════
# Table builders. These are intentionally slide-local teaching examples.
# ════════════════════════════════════════════════════════════════════════════
def _cell_insets(style: AssumptionsTableStyle) -> dict[str, int]:
    return {
        "l_ins": style.cell_l_ins,
        "r_ins": style.cell_r_ins,
        "t_ins": style.cell_t_ins,
        "b_ins": style.cell_b_ins,
    }


def _label_cell(text: str, *, style: AssumptionsTableStyle, **edges):
    return rich_cell(
        [_table_para_xml(plain_para(tr(text, b=True, color=style.label_color)))],
        anchor="b",
        **_cell_insets(style),
        **edges,
    )


def _header_row(spec: AssumptionsTable) -> dict:
    style = spec.style
    section_rule = edge(style.section_rule_color, style.rule_width)
    column_rule = edge(style.column_rule_color, style.rule_width)
    return trow(
        [
            _label_cell("Category:", style=style, B=section_rule),
            _label_cell("Component", style=style, R=column_rule, B=section_rule),
            _label_cell("Methodology", style=style, L=column_rule, B=section_rule),
        ],
        h=IN(spec.header_h),
    )


def _category_cell(row: AssumptionRow, style: AssumptionsTableStyle):
    if row.category_label is None:
        return rich_cell([_table_para_xml(empty_para())], **_cell_insets(style))
    return rich_cell(
        [_table_para_xml(plain_para(tr(row.category_label, b=True, color=style.label_color)))],
        **_cell_insets(style),
        T=edge(style.section_rule_color, style.rule_width),
    )


def _component_edges(row: AssumptionRow, style: AssumptionsTableStyle) -> dict:
    column_rule = edge(style.column_rule_color, style.rule_width)
    section_rule = edge(style.section_rule_color, style.rule_width)
    row_rule = edge(style.row_rule_color, style.rule_width)
    if row.opens_section:
        return {"R": column_rule, "T": section_rule, "B": row_rule}
    if row.closes_section:
        return {"R": column_rule, "T": row_rule}
    return {"R": column_rule, "T": row_rule, "B": row_rule}


def _methodology_edges(row: AssumptionRow, style: AssumptionsTableStyle) -> dict:
    column_rule = edge(style.column_rule_color, style.rule_width)
    section_rule = edge(style.section_rule_color, style.rule_width)
    row_rule = edge(style.row_rule_color, style.rule_width)
    if row.opens_section:
        return {"L": column_rule, "T": section_rule, "B": row_rule}
    if row.closes_section:
        return {"L": column_rule, "T": row_rule}
    return {"L": column_rule, "T": row_rule, "B": row_rule}


def _component_cell(row: AssumptionRow, style: AssumptionsTableStyle):
    return rich_cell(
        [_table_para_xml(plain_para(tr(row.component, color=style.label_color)))],
        **_cell_insets(style),
        **_component_edges(row, style),
    )


def _methodology_cell(row: AssumptionRow, style: AssumptionsTableStyle):
    return rich_cell(
        [_table_para_xml(bullet_para(text, color=style.body_color)) for text in row.bullets],
        **_cell_insets(style),
        **_methodology_edges(row, style),
    )


def _assumption_row(row: AssumptionRow, style: AssumptionsTableStyle) -> dict:
    return trow(
        [
            _category_cell(row, style),
            _component_cell(row, style),
            _methodology_cell(row, style),
        ],
        h=IN(row.row_h),
    )


def paint_title_block(out: list[str]) -> None:
    # These placeholders intentionally remain raw. Rebuilding them with text_box()
    # would add explicit geometry and change how they inherit from slideLayout4.
    out.append("")
    out.append("")


def paint_assumptions_table(out: list[str], ids: ShapeIds) -> None:
    spec = ASSUMPTIONS_TABLE
    # col_widths defines the three table tracks and trow(h=...) their minimum
    # heights. rich_cell() owns insets/anchor/spans; tpara() owns paragraph
    # alignment, bullets, and hanging indents.
    out.append(
        table(
            ids.next(),
            spec.name,
            *spec.box.emu(),
            col_widths=[IN(width) for width in spec.col_widths],
            rows=[
                _header_row(spec),
                *[_assumption_row(row, spec.style) for row in spec.rows],
            ],
        )
    )


def paint_source_note(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            SOURCE_NOTE.name,
            *SOURCE_NOTE.box.emu(),
            [
                paragraph(
                    [line_break(), _box_run(SOURCE_NOTE.text, size_pt=SOURCE_NOTE.font_pt)],
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_title_block(out)
    paint_assumptions_table(out, ids)
    out.append("")
    paint_source_note(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="BuildCo Financial Projections",
    topic="Assumptions & Methodology",
    title="Assumptions & Methodology",
    takeaway="Income Statement (2/2).",
)


def render() -> str:
    return body_slide(CHROME, _body())
