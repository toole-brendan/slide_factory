"""Teaching exemplar: key model inputs as a source-backed reference table.

ROLE
  reference_table / model_inputs_source_map

USE WHEN
  A slide needs to document model inputs and data provenance in one dense native
  table: a row-spanned category spine on the left, input definitions in the
  center, and source notes on the right. This pattern is optimized for auditability
  rather than persuasion: the table itself is the artifact.

TEACHES
  - a full-width native table as a data-source catalogue
  - row_span / grid_span mechanics for category spines and shared source cells
  - a four-column physical grid that reads as three semantic columns
  - local inline table helpers instead of centralized table_kit imports
  - rich table paragraphs with line breaks and bulleted sub-lists inside cells
  - explicit top / bottom rules, including 0.5pt inner gridlines
  - empirical text-fit precedent for a 21-row, Arial 10pt reference table

TEXT-FIT PRECEDENT
  inputs_table:
    geometry: 12.300in wide x 5.933in high
    type: Arial 10pt, single-spaced native-table text
    content: 4 category blocks, 20 input rows, shared source cells, and one
             fuel-cost row with two bulleted sub-lists
    copy_when: the slide is a model-audit appendix or reference page, and the
               viewer needs to trace every input back to an underlying source
               without leaving the slide

SOURCE NOTE
  Teaching rewrite of the source-faithful `key_inputs.py` module. There are no
  charts on this slide; CHARTS is intentionally empty. The core artifact is the
  Key Inputs native table, with all table styling helpers inlined locally so an
  authoring agent can see exactly how spans, borders, paragraph margins, and
  source-cell line breaks are represented.

FIDELITY NOTE
  This is a readability refactor of the source-converted slide module. Coordinates,
  paint order, text, row/column spans, paragraph hierarchy, fills, rules, and
  table insets are preserved from the polished source module.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide,
    table,
    trow,
    tcell_rich,
    tpara,
    trun,
    tbreak,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.style import IN, PT, BLACK, DK, FONT

LAYOUT = "slideLayout4"
CHARTS: list = []

_SECTION = "Carrier Entry Point Attractiveness"
_TOPIC = "Matson Test Case"
_TITLE = "Key Inputs"
_TAKEAWAY = ""

RULE_GRAY = "808080"
GRIDLINE_W = 6_350
BULLET_MAR_L = 171_450
BULLET_INDENT = -171_450


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: useful for agents choosing an exemplar.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "model_inputs_reference_table",
    "use_when": (
        "Use for a model-input appendix where the table must make each input, "
        "its category, and its data source auditable on the slide."
    ),
    "teaches": [
        "full-width native table as a reference exhibit",
        "row-spanned category spine",
        "grid-spanned semantic input column",
        "shared source cells with row spans",
        "rich table paragraphs with tbreak line breaks",
        "bulleted sub-lists inside table cells",
        "inline table styling helpers",
        "0.5pt inner gridline rules",
    ],
}

TEXT_FIT = {
    "inputs_table": {
        "box_in": (12.300, 5.933),
        "font_pt": 10,
        "content": (
            "21 native-table rows: header + Volume, Price, Variable Costs, "
            "and Operating Expenses blocks; one fuel-cost row carries five "
            "bulleted sub-items split across two input columns"
        ),
        "note": (
            "This dense reference table works because most cells are short noun "
            "phrases. Keep sources abbreviated and use line breaks rather than "
            "long prose sentences."
        ),
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Semantic records: geometry in inches; table copy represented as rich text.
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
class RunSpec:
    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = BLACK
    size_pt: float = 10


@dataclass(frozen=True)
class BreakSpec:
    """Line break inside one native-table paragraph."""


@dataclass(frozen=True)
class ParagraphSpec:
    items: tuple[RunSpec | BreakSpec, ...]
    align: str = "l"
    bullet: bool = False
    bullet_char: str | None = None
    level: int = 0
    mar_l: int | None = 0
    indent: int | None = 0


@dataclass(frozen=True)
class InputRow:
    """A plain input row that spans the two semantic input columns."""

    label: str
    color: str = BLACK


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones.
# ════════════════════════════════════════════════════════════════════════════
INPUTS_TABLE = TableZone(
    name="KeyInputsTable",
    box=Box(0.484, 1.059, 12.300, 5.933),
    col_widths=(1.505, 2.968, 2.968, 4.860),
    fit_note="Four physical grid columns: Category | Inputs left | Inputs right | Source.",
)


# ════════════════════════════════════════════════════════════════════════════
# Compact rich-text constructors. Data below should read like marked-up copy.
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
    return RunSpec(text, bold=bold, italic=italic, underline=underline, color=color, size_pt=size_pt)


BR = BreakSpec()


def P(
    *items: RunSpec | BreakSpec,
    align: str = "l",
    bullet: bool = False,
    bullet_char: str | None = None,
    level: int = 0,
    mar_l: int | None = 0,
    indent: int | None = 0,
) -> ParagraphSpec:
    """A rich table paragraph: text/break items plus paragraph mechanics."""

    return ParagraphSpec(
        tuple(items),
        align=align,
        bullet=bullet,
        bullet_char=bullet_char,
        level=level,
        mar_l=mar_l,
        indent=indent,
    )


def label_para(text: str, *, color: str = BLACK, bold: bool = False, align: str = "l") -> ParagraphSpec:
    """Most table cells are a single left-aligned label with explicit zero margins."""

    return P(T(text, bold=bold, color=color), align=align)


def source_para(*items: RunSpec | BreakSpec) -> ParagraphSpec:
    """Source cells use one paragraph with line breaks, not multiple paragraphs."""

    return P(*items)


# ════════════════════════════════════════════════════════════════════════════
# Source/input text constants. Keeping these separate from row mechanics makes
# the table easier for agents to audit and edit safely.
# ════════════════════════════════════════════════════════════════════════════
VOLUME_ROWS: tuple[InputRow, ...] = (
    InputRow("Number of voyages per vessel"),
    InputRow("Cargo capacity by vessel (TEUs, Reefer, and Autos) "),
    InputRow("Utilization levels by cargo type and route"),
    InputRow("Matson Hawaii and Guam service volumes (2024 and 2025)"),
    InputRow("Proportion of loaded Hawaii cargo by direction (WB and EB)"),
    InputRow("Composition of Hawaii cargo by direction (WB and EB)"),
    InputRow("TEU / FEU mix by cargo type "),
)

PRICE_ROWS: tuple[InputRow, ...] = (
    InputRow("Commodity-level TEU / FEU rates"),
    InputRow("Fuel Adjustment Factor", color=DK),
    InputRow("Shoreside charges (handling/stevedoring, wharfage, and other fees)", color=DK),
)

OPERATING_EXPENSE_ROWS: tuple[InputRow, ...] = (
    InputRow("Crew", color=DK),
    InputRow("Insurance", color=DK),
    InputRow("Stores & spares", color=DK),
    InputRow("R&M", color=DK),
    InputRow("Dry-dock (annualized)", color=DK),
    InputRow("Management & administrative", color=DK),
    InputRow("Depreciation & amortization", color=DK),
)

MATSON_SOURCE = source_para(
    T("Matson public filings"),
    BR,
    T("Matson investor presentations"),
    BR,
    T("Internal estimates (utilization levels and Q4 ’25 volume)"),
)

REEVE_USACE_SOURCE = source_para(
    T("Reeve & Associates"),
    BR,
    T("US Army Corps of Engineers (proportion of loaded cargo)"),
)

OPERATING_EXPENSE_SOURCE = source_para(
    T("Open-source research"),
    BR,
    T("Internal estimates (based on industry experience)"),
)

FUEL_COST_LEFT_PARAS = (
    label_para("Fuel Costs:", color=DK),
    P(T("Distance traveled by vessel and route", color=DK), bullet=True, mar_l=BULLET_MAR_L, indent=BULLET_INDENT),
    P(T("Transit speeds by vessel and route", color=DK), bullet=True, mar_l=BULLET_MAR_L, indent=BULLET_INDENT),
)

FUEL_COST_RIGHT_PARAS = (
    P(T("Fuel type used (scrubber presence)", color=DK), bullet=True, mar_l=BULLET_MAR_L, indent=BULLET_INDENT),
    P(T("Other fuel burn / engine parameters", color=DK), bullet=True, mar_l=BULLET_MAR_L, indent=BULLET_INDENT),
    P(T("Bunker fuel prices", color=DK), bullet=True, mar_l=BULLET_MAR_L, indent=BULLET_INDENT),
)

FUEL_SOURCE = source_para(
    T("Historical AIS data (accessed via Global Fishing Watch)"),
    T("; Open-source research; Internal estimates"),
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: local by design, not imported from deck_core.table_kit.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def grid_edge() -> dict[str, int | str]:
    """The source table's inner gridline: 0.5pt gray."""

    return edge(RULE_GRAY, GRIDLINE_W)


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def rich_cell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1, **edges):
    """Multi-paragraph table cell wrapper: content first, mechanics second."""

    return tcell_rich(
        paras,
        fill=fill,
        grid_span=span,
        row_span=rowspan,
        anchor=anchor,
        borders=border_dict(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Text emitters: convert semantic records into primitive table dictionaries.
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


def _table_item(item: RunSpec | BreakSpec):
    return tbreak() if isinstance(item, BreakSpec) else _table_run(item)


def _table_para(spec: ParagraphSpec):
    return tpara(
        [_table_item(item) for item in spec.items],
        align=spec.align,
        bullet=spec.bullet,
        bullet_char=spec.bullet_char,
        level=spec.level,
        mar_l=spec.mar_l,
        indent=spec.indent,
    )


def _paras(specs: tuple[ParagraphSpec, ...] | list[ParagraphSpec]):
    return [_table_para(spec) for spec in specs]


def _label_cell(text: str, *, color: str = BLACK, span: int = 1, rowspan: int = 1, **edges):
    return rich_cell(_paras((label_para(text, color=color),)), span=span, rowspan=rowspan, **edges)


def _input_cell(row: InputRow, *, span: int = 2, **edges):
    return _label_cell(row.label, color=row.color, span=span, **edges)


def _source_cell(paragraph: ParagraphSpec, *, rowspan: int = 1, **edges):
    return rich_cell(_paras((paragraph,)), rowspan=rowspan, **edges)


# ════════════════════════════════════════════════════════════════════════════
# Row builders. These preserve the exact low-level table mechanics while naming
# each row by its model-input meaning.
# ════════════════════════════════════════════════════════════════════════════
def _header_row():
    return trow(
        [
            rich_cell(_paras((label_para("Category", bold=True, align="ctr"),)), B=edge(DK)),
            rich_cell(_paras((label_para("Inputs", bold=True, align="ctr"),)), span=2, B=edge(DK)),
            rich_cell(_paras((label_para("Source", bold=True, align="ctr"),)), B=edge(DK)),
        ],
        h=IN(0),
    )


def _volume_rows():
    dark_top = edge(DK)
    gray = grid_edge()
    rows = [
        trow(
            [
                _label_cell("Volume", rowspan=7, T=dark_top, B=gray),
                _input_cell(VOLUME_ROWS[0], T=dark_top, B=gray),
                _source_cell(source_para(T("Historical AIS data (accessed via Global Fishing Watch)")), T=dark_top, B=gray),
            ],
            h=IN(0),
        ),
        trow(
            [
                _input_cell(VOLUME_ROWS[1], T=gray, B=gray),
                _source_cell(MATSON_SOURCE, rowspan=3, T=gray, B=gray),
            ],
            h=IN(0),
        ),
        trow([_input_cell(VOLUME_ROWS[2], T=gray, B=gray)], h=IN(0)),
        trow([_input_cell(VOLUME_ROWS[3], T=gray, B=gray)], h=IN(0)),
        trow(
            [
                _input_cell(VOLUME_ROWS[4], T=gray, B=gray),
                _source_cell(REEVE_USACE_SOURCE, rowspan=2, T=gray, B=gray),
            ],
            h=IN(0),
        ),
        trow([_input_cell(VOLUME_ROWS[5], T=gray, B=gray)], h=IN(0)),
        trow(
            [
                _input_cell(VOLUME_ROWS[6], T=gray, B=gray),
                _source_cell(source_para(T("Hapag-Lloyd (container payload); Internal estimates")), T=gray, B=gray),
            ],
            h=IN(0),
        ),
    ]
    return rows


def _price_rows():
    gray = grid_edge()
    return [
        trow(
            [
                _label_cell("Price", color=DK, rowspan=3, T=gray, B=gray),
                _input_cell(PRICE_ROWS[0], T=gray, B=gray),
                _source_cell(source_para(T("Pasha Hawaii")), rowspan=3, T=gray, B=gray),
            ],
            h=IN(0),
        ),
        trow([_input_cell(PRICE_ROWS[1], T=gray, B=gray)], h=IN(0)),
        trow([_input_cell(PRICE_ROWS[2], T=gray, B=gray)], h=IN(0)),
    ]


def _variable_cost_rows():
    gray = grid_edge()
    return [
        trow(
            [
                _label_cell("Variable Costs", color=DK, rowspan=3, T=gray, B=gray),
                rich_cell(_paras(FUEL_COST_LEFT_PARAS), T=gray, B=gray),
                rich_cell(_paras(FUEL_COST_RIGHT_PARAS), T=gray, B=gray),
                _source_cell(FUEL_SOURCE, T=gray, B=gray),
            ],
            h=IN(0),
        ),
        trow(
            [
                _label_cell("Pilotage, dockage, tugboat, and port due fees", color=DK, span=2, T=gray, B=gray),
                _source_cell(source_para(T("Open-source research")), T=gray, B=gray),
            ],
            h=IN(0),
        ),
        trow(
            [
                rich_cell(
                    _paras((P(T("Shoreside charges ", color=DK), T("(same as above)", italic=True, color=DK)),)),
                    span=2,
                    T=gray,
                    B=gray,
                ),
                _source_cell(source_para(T("Pasha Hawaii ")), T=gray, B=gray),
            ],
            h=IN(0),
        ),
    ]


def _operating_expense_rows():
    gray = grid_edge()
    rows = [
        trow(
            [
                _label_cell("Operating Expenses", color=DK, rowspan=7, T=gray),
                _input_cell(OPERATING_EXPENSE_ROWS[0], T=gray, B=gray),
                _source_cell(OPERATING_EXPENSE_SOURCE, rowspan=7, T=gray),
            ],
            h=IN(0),
        )
    ]
    for row in OPERATING_EXPENSE_ROWS[1:-1]:
        rows.append(trow([_input_cell(row, T=gray, B=gray)], h=IN(0)))
    rows.append(trow([_input_cell(OPERATING_EXPENSE_ROWS[-1], T=gray)], h=IN(0)))
    return rows


def _inputs_table_rows():
    return [
        _header_row(),
        *_volume_rows(),
        *_price_rows(),
        *_variable_cost_rows(),
        *_operating_expense_rows(),
    ]


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(out: list[str]) -> None:
    out.append(breadcrumb(_SECTION, _TOPIC))
    out.append(title_placeholder(_TITLE, _TAKEAWAY))
    out.append(prelim_chip())


def paint_inputs_table(out: list[str], ids: ShapeIds) -> None:
    # col_widths are physical grid tracks. Row builders carry row/column spans,
    # explicit borders, vertical anchors, and paragraph margins.
    out.append(
        table(
            ids.next(),
            "Table 610",
            *INPUTS_TABLE.box.emu(),
            col_widths=[IN(width) for width in INPUTS_TABLE.col_widths],
            rows=_inputs_table_rows(),
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
    paint_inputs_table(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
