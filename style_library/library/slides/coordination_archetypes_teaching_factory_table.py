"""Teaching exemplar: Coordination archetypes reference table.

ROLE
  reference_table / grouped_taxonomy

USE WHEN
  A slide needs one full-width taxonomy table with row-spanned category bands,
  dense 10pt text, and minimal supporting chrome.

TEACHES
  - native PowerPoint table authored directly from semantic row groups
  - local / inline table-cell kit instead of centralized table_kit.py helpers
  - row_span mechanics for grouped category bands
  - positional border rules: black header underline, gray hairline row rules,
    white right-column rule, and open table foot
  - how to keep row-height minima as explicit text-fit data
  - preserving source quirks when they are part of the faithful rebuild contract

TEXT-FIT PRECEDENT
  archetype_table:
    geometry: 12.300in wide x 4.800in high
    columns: 1.546in Categories · 2.588in Archetypes · 8.167in Responsibilities
    type: Arial 10pt, black, 100% table-cell line spacing
    content: header row + 18 data rows across 5 row-spanned category groups
    copy_when: a slide is primarily a dense reference table and the table itself
               is the proof, not a supporting exhibit beside prose
  responsibility_cells:
    geometry: 8.167in wide; mixed 0.000in and 0.174in minimum row heights
    type: Arial 10pt
    content: one-sentence definitions; rich-cell path supports split runs where
             source text was split by the conversion process

SOURCE NOTE
  Teaching rewrite of the source-faithful `coordination_archetypes.py` module.
  This slide has no charts or pictures; the teaching value is the table: grouped
  data is expressed semantically, while table mechanics remain local and explicit.
  The surrounding slide contract (`LAYOUT`, `CHARTS`, `_body()`, `render()`),
  table coordinates, row spans, text, and border roles are preserved.

FIDELITY NOTE
  This rebuild is intended to render identically to the source-faithful module:
  it preserves the full table geometry, row order, row spans, row-height minima,
  borders, and source text. The source typo "Financia & Risk Coordinators" is
  intentionally kept verbatim because changing it would change the slide.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, table, tcell, tcell_rich, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: these are comments the module can expose programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "reference_table",
    "use_when": (
        "Use for a full-width, dense taxonomy/reference table where category "
        "labels span multiple rows and the border system carries the grouping."
    ),
    "teaches": [
        "native table primitive",
        "inline table-cell kit",
        "row-spanned category bands",
        "position-driven borders",
        "dense 10pt table text",
        "source-faithful text quirks",
    ],
}

TEXT_FIT = {
    "archetype_table": {
        "box_in": (12.300, 4.800),
        "columns_in": (1.546, 2.588, 8.167),
        "font_pt": 10,
        "content": "header + 18 data rows, 5 category row-span groups",
        "note": (
            "Most rows rely on text height rather than a positive row minimum; "
            "wrapping definitions use 0.174in minima where the source did."
        ),
    },
    "category_spine": {
        "font_pt": 10,
        "content": "five row-spanned category cells with spans 2/5/4/3/3",
        "note": "Category cells get the group bottom rule, not every internal row rule.",
    },
    "responsibility_column": {
        "box_in": (8.167, 4.800),
        "font_pt": 10,
        "content": "single-sentence responsibilities, with two rich split-run cells",
        "note": "Right edge is an explicit white border to match the source table edge.",
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
class RichRun:
    text: str
    bold: bool = False
    italic: bool = False
    color: str = BLACK
    size_pt: float = 10


@dataclass(frozen=True)
class RichParagraph:
    runs: tuple[RichRun, ...]
    mar_l: int | None = None
    indent: int | None = None


RichCellContent = tuple[RichParagraph, ...]
CellContent = Union[str, RichCellContent]  # 3.9-compatible (runtime PEP 604 unions need 3.10+)


@dataclass(frozen=True)
class ArchetypeRow:
    archetype: str
    responsibility: CellContent
    height_in: float


@dataclass(frozen=True)
class ArchetypeGroup:
    category: str
    row_span: int
    rows: tuple[ArchetypeRow, ...]


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: chrome plus one full-width reference table.
# ════════════════════════════════════════════════════════════════════════════
SLIDE_TITLE = TextZone(
    name="Title",
    box=Box(0.495, 0.607, 12.300, 0.650),
    font_pt=20,
    fit_note="House title placeholder: short title + one-line subtitle.",
)

ARCHETYPE_TABLE = TextZone(
    name="CoordinationArchetypeTable",
    box=Box(0.495, 1.641, 12.300, 4.800),
    font_pt=10,
    fit_note="Single full-width reference table; no side prose, no chart.",
)

TABLE_COLUMNS: tuple[TableColumn, ...] = (
    TableColumn("Categories", 1.546, "Row-spanned category bands; keep labels compact."),
    TableColumn("Archetypes", 2.588, "Archetype names fit at 10pt with normal wrapping."),
    TableColumn("Responsibilities", 8.167, "One-sentence responsibility definitions."),
)

HEADER_LABELS: tuple[str, str, str] = ("Categories", "Archetypes", "Responsibilities")


# ════════════════════════════════════════════════════════════════════════════
# Table data: five category groups drive row spans and row-count validation.
# ════════════════════════════════════════════════════════════════════════════
def rich_cell_text(*runs: RichRun, mar_l: int | None = None, indent: int | None = None) -> RichCellContent:
    """Readable constructor for a one-paragraph rich responsibility cell."""

    return (RichParagraph(tuple(runs), mar_l=mar_l, indent=indent),)


ARCHETYPE_GROUPS: tuple[ArchetypeGroup, ...] = (
    ArchetypeGroup(
        "Strategic & Integrated Coordinators ",
        2,
        (
            ArchetypeRow(
                "Beneficial Cargo Owner (BCO)",
                "Owns cargo and manages logistics using internal staff and direct carrier contracts",
                0.000,
            ),
            ArchetypeRow(
                "Fourth-Party Logistics (4PL)",
                rich_cell_text(
                    RichRun("Manages and optimizes entire supply chain for shippers; "),
                    RichRun("does not own assets"),
                ),
                0.174,
            ),
        ),
    ),
    ArchetypeGroup(
        "Operational & Execution Coordinators",
        5,
        (
            ArchetypeRow(
                "Third-Party Logistics (3PL)",
                "Coordinates functional tasks such as warehousing, fulfillment, picking/packing, and regional distribution for shippers",
                0.000,
            ),
            ArchetypeRow(
                "Freight Forwarders",
                "Orchestrates multimodal transport and manages documentation; acts on behalf of shippers but does not assume liability of carriers",
                0.174,
            ),
            ArchetypeRow(
                "Intermodal Marketing Company",
                "Secures rail capacity by purchasing slots in bulk to provide inland rail transport",
                0.174,
            ),
            ArchetypeRow(
                "Domestic Freight Broker",
                "Coordinates domestic trucking capacity, matching independent drivers or small fleets with the inland needs of 3PLs or BCOs",
                0.174,
            ),
            ArchetypeRow(
                "Origin & Destination Drayage",
                "Moves containers between factories, rail ramps, and port terminals via truck",
                0.000,
            ),
        ),
    ),
    ArchetypeGroup(
        "Legal & Contractual Coordinators",
        4,
        (
            ArchetypeRow(
                "Non-Vessel Operating Common Carrier",
                rich_cell_text(
                    RichRun("Books space on operator vessels and resells to shippers without owning ships; a"),
                    RichRun("ssumes direct legal liability for cargo"),
                    mar_l=0,
                    indent=0,
                ),
                0.000,
            ),
            ArchetypeRow(
                "Customs Broker",
                "Manages import/export customs and compliance",
                0.000,
            ),
            ArchetypeRow(
                "Slot Charterer",
                "Purchases container space on another carrier’s vessel to expand network without capital risk of operating an entire ship",
                0.174,
            ),
            ArchetypeRow(
                "Shipbroker",
                "Negotiates \"Charter Parties\" (leasing contracts) and vessel sale-and-purchase transactions between owners and operators",
                0.174,
            ),
        ),
    ),
    ArchetypeGroup(
        "Asset & Equipment Coordinators",
        3,
        (
            ArchetypeRow(
                "IEP (Intermodal Equipment Provider)",
                "Owns and distributes chassis (trailers required to transport containers by road)",
                0.000,
            ),
            ArchetypeRow(
                "Container Leasing Companies",
                "Leases containers to ocean liners and NVOCCs, managing global inventory and repositioning of equipment",
                0.000,
            ),
            ArchetypeRow(
                "Empty Container Depots",
                "Coordinates storage, inspection, and repositioning of empty boxes",
                0.000,
            ),
        ),
    ),
    ArchetypeGroup(
        "Financia & Risk Coordinators",
        3,
        (
            ArchetypeRow(
                "Commercial Banks & Trade Finance ",
                "Facilitates movement of money via Letters of Credit (LC), ensuring payment only when proof of shipment (Bill of Lading) is provided",
                0.174,
            ),
            ArchetypeRow(
                "P&I Clubs / Marine Insurers ",
                "Provides liability coverage for global ocean tonnage, managing the \"legal safety net\" for cargo loss or ship collisions",
                0.174,
            ),
            ArchetypeRow(
                "Marine Cargo Surveyor",
                "Verifies cargo condition and proper stowage, providing data needed to coordinate insurance claims between carriers and shippers",
                0.174,
            ),
        ),
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
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    """tcell wrapper: content first, cell mechanics second."""

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
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=border_dict(**edges),
    )


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
    """tcell_rich wrapper: rich content first, cell mechanics second."""

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
# Table-text helpers: keep the row builder at semantic-table level.
# ════════════════════════════════════════════════════════════════════════════
def _tr(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False, color: str = BLACK) -> str:
    return trun(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)


def _rich_paragraph(spec: RichParagraph) -> dict:
    kwargs = {}
    if spec.mar_l is not None:
        kwargs["mar_l"] = spec.mar_l
    if spec.indent is not None:
        kwargs["indent"] = spec.indent
    return tpara([_tr(run_spec.text, size_pt=run_spec.size_pt, bold=run_spec.bold, italic=run_spec.italic, color=run_spec.color) for run_spec in spec.runs], **kwargs)


def _rich_content_paragraphs(content: RichCellContent) -> list[dict]:
    return [_rich_paragraph(paragraph_spec) for paragraph_spec in content]


def _header_cell(label: str, *, right_rule: bool = False):
    return rich_cell(
        [tpara([_tr(label, bold=True)], mar_l=0, indent=0)],
        fill=WHITE,
        anchor="b",
        R=edge(WHITE) if right_rule else None,
        B=edge(BLACK),
    )


def _responsibility_cell(content: CellContent, *, top_rule, bottom_rule) -> dict:
    border_kwargs = {"T": top_rule, "R": edge(WHITE)}
    if bottom_rule is not None:
        border_kwargs["B"] = bottom_rule
    if isinstance(content, tuple):
        return rich_cell(_rich_content_paragraphs(content), fill=WHITE, **border_kwargs)
    return plain_cell(content, fill=WHITE, **border_kwargs)


def _validate_group_spans() -> None:
    """Catch accidental edits where row_span stops matching the group data."""

    for group in ARCHETYPE_GROUPS:
        if group.row_span != len(group.rows):
            raise ValueError(
                f"{group.category!r} declares row_span={group.row_span} "
                f"but has {len(group.rows)} rows"
            )


# ════════════════════════════════════════════════════════════════════════════
# Table row construction: border roles are assigned by position, not row data.
# ════════════════════════════════════════════════════════════════════════════
def _archetype_rows() -> list[dict]:
    """Build the 18 data rows and apply table borders by row position.

    Rules:
      - First data row gets a BLACK top rule, becoming the heavy underline under
        the header row.
      - Interior rows get 808080 hairline separators.
      - Last row has no bottom rule, leaving the table foot open.
      - Responsibility cells always get a WHITE right rule.
      - Category cells draw only the group-level bottom rule, not every internal
        row separator inside the row span.
    """

    _validate_group_spans()
    hairline = edge("808080", 6_350)
    total_data_rows = sum(len(group.rows) for group in ARCHETYPE_GROUPS)
    rows: list[dict] = []
    data_index = 0

    for group_index, group in enumerate(ARCHETYPE_GROUPS):
        last_group = group_index == len(ARCHETYPE_GROUPS) - 1
        for row_index, row in enumerate(group.rows):
            top_rule = edge(BLACK) if data_index == 0 else hairline
            bottom_rule = None if data_index == total_data_rows - 1 else hairline
            row_cells: list[dict] = []

            if row_index == 0:
                category_bottom = None if last_group else hairline
                row_cells.append(
                    plain_cell(
                        group.category,
                        fill=WHITE,
                        rowspan=group.row_span,
                        T=top_rule,
                        B=category_bottom,
                    )
                )

            row_cells.append(
                plain_cell(
                    row.archetype,
                    fill=WHITE,
                    T=top_rule,
                    B=bottom_rule,
                )
            )
            row_cells.append(
                _responsibility_cell(row.responsibility, top_rule=top_rule, bottom_rule=bottom_rule)
            )
            rows.append(trow(row_cells, h=IN(row.height_in)))
            data_index += 1

    return rows


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(out: list[str]) -> None:
    out.append("")
    out.append(
        ""
    )


def paint_archetype_table(out: list[str], ids: ShapeIds) -> None:
    out.append(
        table(
            ids.next(),
            "Table 11",
            *ARCHETYPE_TABLE.box.emu(),
            col_widths=[IN(column.width_in) for column in TABLE_COLUMNS],
            rows=[
                trow(
                    [
                        _header_cell(HEADER_LABELS[0]),
                        _header_cell(HEADER_LABELS[1]),
                        _header_cell(HEADER_LABELS[2], right_rule=True),
                    ],
                    h=IN(0),
                ),
                *_archetype_rows(),
            ],
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_chrome(out)
    paint_archetype_table(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="Commercial Maritime Value Chain",
    topic="Coordination Archetypes",
    title="Coordination Archetypes",
    takeaway="Numerous entities play in the Coordination step of the value chain.",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
