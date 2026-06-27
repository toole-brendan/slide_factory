"""Teaching exemplar: addressable-demand scope / criteria table.

ROLE
  define_scope_or_taxonomy / inclusion_exclusion_filter

USE WHEN
  A slide needs to define what is in scope, what is out of scope, and why,
  using a left criteria stack plus a right rationale column.

TEACHES
  - pure table-and-box archetype: no chart, no image, no connectors
  - colored scope criteria chips backed by right-column rationale text
  - tier-spine labels as native one-cell tables with right-edge rules
  - empirical text-fit precedent for 14pt rationale sentences in 0.5in rows
  - when to use native table() for row/column labels vs. text_box() for chips

TEXT-FIT PRECEDENT
  rationale_row:
    geometry: 8.677in wide x 0.500in high
    type: Arial 14pt, black, 100% line spacing
    content: one vertically-centered sentence; longest row is roughly 25 words
    copy_when: the slide is a scope filter and each row needs one clear why
  criteria_chip:
    geometry: 2.200in wide x 0.500in high
    type: Arial 12pt bold; white on dark fills, black on amber fill
    content: one short label or two-line label with italic parenthetical
    copy_when: labels are categorical gates, not explanatory prose

SOURCE NOTE
  Teaching rewrite of the source-faithful `addressable_demand.py` module.
  It keeps the same coordinates, visible text, colors, layout, and render
  contract (`LAYOUT`, `CHARTS`, `_body()`, `render()`), but renames objects,
  groups content by slide role, and makes fit/meaning explicit for AI authors.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    line_break,
    table,
    trow,
    tcell,
    tcell_rich,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: deliberately programmatic so an exemplar index can read it.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "define_scope_or_taxonomy",
    "use_when": (
        "Use for inclusion/exclusion logic: left-side categorical gates, "
        "right-side rationale, and tier labels that explain how the gates group."
    ),
    "teaches": [
        "criteria stack",
        "right rationale column",
        "tier-spine labels as one-cell native tables",
        "column headers as rule-underlined native tables",
        "text-fit precedent for 14pt rationale rows",
        "scope taxonomy without charts or connectors",
    ],
}

TEXT_FIT = {
    "rationale_row": {
        "box_in": (8.677, 0.500),
        "font_pt": 14,
        "content": "one sentence, centered vertically; longest row roughly 25 words",
        "note": (
            "This is the key fit precedent. Keep each rationale to one direct "
            "sentence; do not turn the right column into paragraph prose."
        ),
    },
    "criteria_chip": {
        "box_in": (2.200, 0.500),
        "font_pt": 12,
        "content": "one short label, or two lines when the second line is an italic parenthetical",
    },
    "tier_spine_label": {
        "box_in": "1.263-1.264in wide; height spans its criteria tier",
        "font_pt": 12,
        "content": "tier name only; color matches the tier rule",
    },
    "column_header": {
        "box_in": ((2.200, 0.300), (8.677, 0.300)),
        "font_pt": 12,
        "content": "short header text, carried by a black bottom rule",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Semantic geometry/data records.
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
class CriteriaCell:
    key: str
    box: Box
    fill: str
    text_color: str
    primary: str
    secondary: str | None = None


@dataclass(frozen=True)
class RationaleCell:
    key: str
    box: Box
    text: str
    italic: bool = False


@dataclass(frozen=True)
class NativeLabelTable:
    key: str
    name: str
    box: Box
    color: str
    border_side: str
    border_color: str
    border_width: int
    text: tuple[str, ...]


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Palette roles used by this exemplar.
# ════════════════════════════════════════════════════════════════════════════
ADDRESSABLE_COMMERCIAL = "007770"
ADDRESSABLE_OFFSHORE = "FFC000"
NON_ADDRESSABLE = "969696"


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: the slide reads as tier spine + criteria stack + rationale column.
# ════════════════════════════════════════════════════════════════════════════
CRITERIA_HEADER = TextZone(
    name="CriteriaHeader",
    box=Box(1.792, 1.375, 2.200, 0.300),
    font_pt=12,
    fit_note="One short table header with black bottom rule.",
)
RATIONALE_HEADER = TextZone(
    name="RationaleHeader",
    box=Box(4.158, 1.375, 8.677, 0.300),
    font_pt=12,
    fit_note="One-line table header; do not wrap.",
)

CRITERIA_CHIP_ZONE = TextZone(
    name="CriteriaChip",
    box=Box(0.0, 0.0, 2.200, 0.500),
    font_pt=12,
    fit_note="One short criterion label; optional italic parenthetical on line 2.",
)
RATIONALE_ROW_ZONE = TextZone(
    name="RationaleRow",
    box=Box(4.158, 0.0, 8.677, 0.500),
    font_pt=14,
    fit_note="One sentence per row; centered vertically in a 0.5in row.",
)


# ════════════════════════════════════════════════════════════════════════════
# Criteria stack: all row gates, grouped by tier.
# ════════════════════════════════════════════════════════════════════════════
CRITERIA_CELLS: tuple[CriteriaCell, ...] = (
    CriteriaCell("us_built", Box(1.792, 1.746, 2.200, 0.500), BLACK, WHITE, "US-Built"),
    CriteriaCell("us_flagged", Box(1.793, 2.423, 2.200, 0.500), BLACK, WHITE, "US-Flagged"),
    CriteriaCell("commercially_viable", Box(1.793, 3.100, 2.200, 0.500), ADDRESSABLE_COMMERCIAL, WHITE, "Commercially Viable"),
    CriteriaCell("oceangoing", Box(1.793, 3.777, 2.200, 0.500), ADDRESSABLE_COMMERCIAL, WHITE, "Oceangoing"),
    CriteriaCell("high_volume_offshore", Box(1.793, 4.454, 2.200, 0.500), ADDRESSABLE_OFFSHORE, BLACK, "High Volume Offshore", "(PSV and FSV)"),
    CriteriaCell("great_lakes", Box(1.793, 5.131, 2.200, 0.500), NON_ADDRESSABLE, WHITE, "Great Lakes Commercial Vessels"),
    CriteriaCell("low_volume_offshore", Box(1.793, 5.808, 2.200, 0.500), NON_ADDRESSABLE, WHITE, "Low Volume Offshore ", "(ex-PSV and FSV)"),
    CriteriaCell("other_categories", Box(1.793, 6.485, 2.200, 0.500), NON_ADDRESSABLE, WHITE, "Other Categories"),
)


# ════════════════════════════════════════════════════════════════════════════
# Rationale column: one explanation per visible criteria row.
# ════════════════════════════════════════════════════════════════════════════
RATIONALE_CELLS: tuple[RationaleCell, ...] = (
    RationaleCell(
        "us_built",
        Box(4.158, 1.746, 8.677, 0.500),
        "Provides Jones Act protection or enables subsidy eligibility under pending legislation and potential expansion of other programs; required for certain export/import provisions",
    ),
    RationaleCell("us_flagged", Box(4.158, 2.422, 8.677, 0.500), "Same as above", italic=True),
    RationaleCell(
        "commercially_viable",
        Box(4.158, 3.097, 8.677, 0.500),
        "Meets capabilities and tonnage required for participation in subsidized programs; priced to achieve revenue targets",
    ),
    RationaleCell(
        "oceangoing",
        Box(4.158, 3.773, 8.677, 0.500),
        "Drives national shipbuilding capacity with avg. gross tonnage 15x+ that of offshore vessels",
    ),
    RationaleCell(
        "high_volume_offshore",
        Box(4.158, 4.448, 8.677, 0.500),
        "Large fleet size enables serial production (5+ hulls/yr to achieve max labor efficiencies); viable if owner/operators conduct 1-for-1 replacement of expected retirements",
    ),
    RationaleCell(
        "great_lakes",
        Box(4.158, 5.123, 8.677, 0.500),
        "Unlikely to drive meaningful demand given small fleet size (~37 vessels) and low retirement rates",
    ),
    RationaleCell(
        "low_volume_offshore",
        Box(4.158, 5.799, 8.677, 0.500),
        "Small fleet size precludes serial production; low gross tonnage per vessel limits national security utility and pricing",
    ),
    RationaleCell("other_categories", Box(4.158, 6.485, 8.677, 0.500), "Same as above", italic=True),
)


# ════════════════════════════════════════════════════════════════════════════
# Native one-cell tables: column headers and tier-spine labels.
# ════════════════════════════════════════════════════════════════════════════
COLUMN_HEADER_TABLES: tuple[NativeLabelTable, ...] = (
    NativeLabelTable(
        key="criteria",
        name="CriteriaColumnHeader",
        box=CRITERIA_HEADER.box,
        color=BLACK,
        border_side="B",
        border_color=BLACK,
        border_width=12_700,
        text=("Criteria",),
    ),
    NativeLabelTable(
        key="rationale",
        name="RationaleColumnHeader",
        box=RATIONALE_HEADER.box,
        color=BLACK,
        border_side="B",
        border_color=BLACK,
        border_width=12_700,
        text=("Inclusion / Exclusion Rationale",),
    ),
)

TIER_SPINE_TABLES: tuple[NativeLabelTable, ...] = (
    NativeLabelTable(
        key="table_stakes",
        name="TierSpine_TableStakes",
        box=Box(0.361, 1.746, 1.264, 1.175),
        color=BLACK,
        border_side="R",
        border_color=BLACK,
        border_width=38_100,
        text=("Table Stakes",),
    ),
    NativeLabelTable(
        key="addressable_commercial",
        name="TierSpine_AddressableCommercial",
        box=Box(0.361, 3.097, 1.264, 1.175),
        color=ADDRESSABLE_COMMERCIAL,
        border_side="R",
        border_color=ADDRESSABLE_COMMERCIAL,
        border_width=38_100,
        text=("Addressable", "Commercial"),
    ),
    NativeLabelTable(
        key="addressable_offshore",
        name="TierSpine_AddressableOffshore",
        box=Box(0.362, 4.454, 1.263, 0.500),
        color=ADDRESSABLE_OFFSHORE,
        border_side="R",
        border_color=ADDRESSABLE_OFFSHORE,
        border_width=38_100,
        text=("Addressable Offshore",),
    ),
    NativeLabelTable(
        key="non_addressable",
        name="TierSpine_NonAddressable",
        box=Box(0.362, 5.131, 1.263, 1.854),
        color=NON_ADDRESSABLE,
        border_side="R",
        border_color=NON_ADDRESSABLE,
        border_width=38_100,
        text=("Non-Addressable",),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: kept local so the module is ready against today's deck_core.
# Move this to deck_core.table_kit later if/when you centralize the authoring API.
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
    bold: bool | None = None,
    italic: bool | None = None,
    color: str = BLACK,
    size: int = PT(12),
    align: str = "l",
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    l_ins: int = 45_720,
    r_ins: int = 45_720,
    t_ins: int = 45_720,
    b_ins: int = 45_720,
    **edges,
):
    """tcell wrapper: cell content first, mechanics second."""

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
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    l_ins: int = 45_720,
    r_ins: int = 45_720,
    t_ins: int = 45_720,
    b_ins: int = 45_720,
    **edges,
):
    """tcell_rich wrapper: content paragraphs first, mechanics second."""

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
# Text helpers: keep paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _r(
    text: str,
    *,
    size_pt: float = 12,
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
) -> str:
    return run(
        text,
        size=PT(size_pt),
        bold=bold or None,
        italic=italic or None,
        color=color,
        font=FONT,
    )


def _tr(
    text: str,
    *,
    size_pt: float = 12,
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
):
    return trun(
        text,
        size=PT(size_pt),
        bold=bold or None,
        italic=italic or None,
        color=color,
        font=FONT,
    )


def _tight_para(runs, *, align=None) -> str:
    """100% line-spacing paragraph used by the source slide's labels."""

    return paragraph(runs, align=align, line_spacing=100_000)


def _criteria_paragraphs(cell: CriteriaCell) -> list[str]:
    runs = [_r(cell.primary, size_pt=12, bold=True, color=cell.text_color)]
    if cell.secondary:
        runs.extend(
            [
                line_break(),
                _r(cell.secondary, size_pt=12, italic=True, color=cell.text_color),
            ]
        )
        if cell.key == "low_volume_offshore":
            # Source carries one trailing bold space after the parenthetical.
            runs.append(_r(" ", size_pt=12, bold=True, color=cell.text_color))
    return [_tight_para(runs, align="ctr")]


def _native_label_paras(label: NativeLabelTable):
    return [
        tpara([_tr(line, size_pt=12, color=label.color)], mar_l=0, indent=0)
        for line in label.text
    ]


def _border_for(label: NativeLabelTable) -> dict[str, dict[str, int | str]]:
    return {label.border_side: edge(label.border_color, label.border_width)}


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(out: list[str]) -> None:
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(
        title_placeholder(
            "Addressable Demand",
            "US-built and flagged oceangoing commercial vessels and high-volume offshore vessels meet desired regulatory and/or serial production requirements.",
        )
    )


def paint_criteria_stack(out: list[str], ids: ShapeIds) -> None:
    for cell in CRITERIA_CELLS:
        out.append(
            text_box(
                ids.next(),
                f"Criteria_{cell.key}",
                *cell.box.emu(),
                _criteria_paragraphs(cell),
                fill=cell.fill,
                line_color="none",
                anchor="ctr",
            )
        )


def paint_tier_spines(out: list[str], ids: ShapeIds) -> None:
    for label in TIER_SPINE_TABLES:
        out.append(
            table(
                ids.next(),
                label.name,
                *label.box.emu(),
                col_widths=[IN(label.box.w)],
                rows=[
                    trow(
                        [
                            rich_cell(
                                _native_label_paras(label),
                                **_border_for(label),
                            )
                        ],
                        h=IN(label.box.h),
                    )
                ],
            )
        )


def paint_rationale_column(out: list[str], ids: ShapeIds) -> None:
    for row in RATIONALE_CELLS:
        out.append(
            text_box(
                ids.next(),
                f"Rationale_{row.key}",
                *row.box.emu(),
                [_tight_para([_r(row.text, size_pt=14, italic=row.italic)], align=None)],
                fill=None,
                line_color="none",
                anchor="ctr",
            )
        )


def paint_column_headers(out: list[str], ids: ShapeIds) -> None:
    for header in COLUMN_HEADER_TABLES:
        out.append(
            table(
                ids.next(),
                header.name,
                *header.box.emu(),
                col_widths=[IN(header.box.w)],
                rows=[
                    trow(
                        [
                            plain_cell(
                                header.text[0],
                                size=PT(12),
                                color=header.color,
                                **_border_for(header),
                            )
                        ],
                        h=IN(0),
                    )
                ],
            )
        )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Later elements paint on top. This module groups by role rather than by
    # converter cluster: chrome, criteria, spines, rationale, then headers.
    paint_chrome(out)
    paint_criteria_stack(out, ids)
    paint_tier_spines(out, ids)
    paint_rationale_column(out, ids)
    paint_column_headers(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
