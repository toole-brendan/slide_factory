"""Hand-polished slide module: market-sizing level definitions (Supplier TAM/SAM).

Rebuilds source slide 1 from the Defense Demand Drivers New Construction deck.
The visual contract stays source-faithful; the code is organized to be read in
the same order as the exhibit:

    1. local palette and slide contract
    2. the mirrored market-level definition table
    3. the nested market-level funnel (four concentric layers + level tags)
    4. the dashed "focus areas" callout over the lower table rows
    5. paint functions in PowerPoint z-order

This slide carries no native chart, so there is no chart part and no ``_src``
bundle: every shape is a deck_core primitive at the source EMU geometry, and the
house chrome (breadcrumb, title, Preliminary chip) is supplied by the Chrome
record rather than painted into the body.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, paragraph, run, table, tbreak, tcell, tcell_rich,
    text_box, tpara, trow, trun,
)


# ════════════════════════════════════════════════════════════════════════════
# Slide contract and local palette
# ════════════════════════════════════════════════════════════════════════════
LAYOUT = "slideLayout4"

BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
FONT = "Arial"

# Funnel depth ramp: progressively darker blue for each narrower market level.
BLUE_1 = "E2E9EF"   # Total Funding (widest layer)
BLUE_2 = "B6C8D8"   # TAM
BLUE_3 = "6E91B1"   # SAM
BLUE_4 = "3D5972"   # Available Spend (narrowest layer)

FUNNEL_OUTLINE = "202223"   # thin near-black ring drawn around each concentric layer
FOCUS_ACCENT = "FB6B3C"     # orange dashed "focus areas" callout and its caption
TABLE_RULE = DK             # horizontal rules in the definition table

SLIDE_METADATA = {
    "role": "definition_diagram / nested_market_level_funnel",
    "source_deck": "Defense Demand Drivers New Construction",
    "source_slide": 1,
    "visual_contract": "source-faithful layout, no native chart",
    "primary_pattern": "nested market-level funnel paired with a mirrored definition table",
}

TEXT_FIT = {
    "funnel_tag": {
        "box_in": (1.949, 0.386),
        "content": "one market-level name, bold, centered on its color band",
    },
    "definition_table": {
        "box_in": (6.257, 5.456),
        "font_pt": 14,
        "content": "header plus four market levels, each a one-to-three-line definition",
    },
}

CHARTS: list = []   # no native chart on this slide -> no chart part, no _src bundle


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


class ShapeIds:
    """Sequential body-shape ids; chrome ids are owned by deck_core.chrome."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Local table helpers (cell content vs. cell mechanics)
# ════════════════════════════════════════════════════════════════════════════
PAD = dict(l_ins=60_960, r_ins=60_960, t_ins=60_960, b_ins=60_960)   # the source's heavier cell padding


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
# Definition-table content
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class CellRun:
    text: str
    italic: bool = False
    size_pt: float = 14
    bold: bool = False
    color: str = BLACK

    def emit(self):
        return trun(self.text, size=PT(self.size_pt), bold=self.bold or None,
                    italic=self.italic or None, color=self.color, font=FONT)


@dataclass(frozen=True)
class CellParagraph:
    runs: tuple[CellRun, ...] = ()
    end_size_pt: float | None = None   # an empty spacer paragraph collapsed to this size

    def emit(self):
        if not self.runs and self.end_size_pt is not None:
            return tpara([], end_size=PT(self.end_size_pt))
        return tpara([r.emit() for r in self.runs])


def CR(text: str, *, italic: bool = False) -> CellRun:
    return CellRun(text, italic=italic)


def CP(*runs: CellRun) -> CellParagraph:
    return CellParagraph(tuple(runs))


SPACER = CellParagraph(end_size_pt=14)   # blank line between a definition's two clauses


@dataclass(frozen=True)
class DefinitionRow:
    level: str
    definition: tuple[CellParagraph, ...]
    row_h: float
    top_rule_width: int = 6_350
    bottom_rule_width: int | None = 6_350
    label_trailing_breaks: int = 0     # TAM pads its short label down to clear its taller definition
    label_zero_spacing: bool = False   # source pins these labels' marL/indent/spacing to zero


DEFINITION_TABLE = Box(6.577, 1.408, 6.257, 5.456)
DEFINITION_COL_WIDTHS = (1.749, 4.509)

DEFINITION_ROWS: tuple[DefinitionRow, ...] = (
    DefinitionRow(
        "Total Funding",
        (
            CP(
                CR("All appropriations for DDGs ("),
                CR("Arleigh Burke", italic=True),
                CR("-class), SSNs ("),
                CR("Virginia", italic=True),
                CR("-class), and SSBNs ("),
                CR("Columbia", italic=True),
                CR("-class)"),
            ),
        ),
        row_h=0.956,
        top_rule_width=12_700,   # heavier rule directly under the header
    ),
    DefinitionRow(
        "Total Addressable Market (TAM)",
        (
            CP(CR("Total spend on outsourced Basic Construction")),
            SPACER,
            CP(CR("Portion of Total Funding attributable to non-Primes and subcontractors (i.e., removes Prime-conducted Basic Construction and GFE)")),
        ),
        row_h=0.635,
        label_trailing_breaks=2,
    ),
    DefinitionRow(
        "Serviceable Addressable Market (SAM)",
        (
            CP(CR("Total spend on relevant work types ")),
            SPACER,
            CP(CR("Portion of TAM spent on different work types (e.g., structural fabrication, HVAC, electrical) ")),
        ),
        row_h=1.044,
        label_zero_spacing=True,
    ),
    DefinitionRow(
        "Available Spend",
        (
            CP(CR("Total spend Saronic can compete for each year")),
            SPACER,
            CP(CR("Portion of SAM available for new entrants, driven by (1) whitespace growth from increased outsourcing penetration, (2) contracts coming up for recompete, and (3) movement from sole-source to multi-source ")),
        ),
        row_h=1.044,
        label_zero_spacing=True,
        bottom_rule_width=None,   # last row carries no bottom rule
    ),
)


def _rule_kwargs(row: DefinitionRow) -> dict:
    rule = {"T": edge(TABLE_RULE, row.top_rule_width)}
    if row.bottom_rule_width is not None:
        rule["B"] = edge(TABLE_RULE, row.bottom_rule_width)
    return rule


def _label_cell(row: DefinitionRow):
    rule = _rule_kwargs(row)
    if row.label_trailing_breaks:
        runs = [trun(row.level, size=PT(14), color=BLACK, font=FONT)]
        runs += [tbreak() for _ in range(row.label_trailing_breaks)]
        return rcell([tpara(runs)], anchor="t", **PAD, **rule)
    if row.label_zero_spacing:
        para = tpara([trun(row.level, size=PT(14), color=BLACK, font=FONT)],
                     mar_l=0, indent=0, space_before=0, space_after=0)
        return rcell([para], anchor="t", **PAD, **rule)
    return cell(row.level, size=PT(14), color=BLACK, anchor="t", **PAD, **rule)


def _definition_cell(row: DefinitionRow):
    return rcell([p.emit() for p in row.definition], anchor="t", **PAD, **_rule_kwargs(row))


def _definition_row(row: DefinitionRow):
    return trow([_label_cell(row), _definition_cell(row)], h=IN(row.row_h))


DEFINITION_HEADER = trow(
    [
        cell("Level", size=PT(14), bold=True, anchor="b", **PAD, B=edge(TABLE_RULE)),
        cell("Definition", size=PT(14), bold=True, anchor="b", **PAD, B=edge(TABLE_RULE)),
    ],
    h=IN(0.359),
)


# ════════════════════════════════════════════════════════════════════════════
# Nested funnel layers, level tags, and the focus-areas callout
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class FunnelLevel:
    key: str
    name: str
    layer: Box          # the concentric color band
    tag: Box            # the centered label chip riding on that band
    fill: str
    tag_text_color: str


FUNNEL_LEVELS: tuple[FunnelLevel, ...] = (
    FunnelLevel("total_funding", "Total Funding", Box(0.477, 1.307, 5.700, 5.700), Box(2.352, 1.564, 1.949, 0.386), BLUE_1, BLACK),
    FunnelLevel("tam", "TAM", Box(0.927, 2.207, 4.800, 4.800), Box(2.352, 2.464, 1.949, 0.386), BLUE_2, BLACK),
    FunnelLevel("sam", "SAM", Box(1.377, 3.107, 3.900, 3.900), Box(2.352, 3.457, 1.949, 0.386), BLUE_3, WHITE),
    FunnelLevel("available_spend", "Available Spend", Box(1.777, 4.007, 3.100, 3.000), Box(2.352, 5.314, 1.949, 0.386), BLUE_4, WHITE),
)


@dataclass(frozen=True)
class Callout:
    text: str
    box: Box
    accent: str
    font_pt: float = 10
    line_width: int = 19_050


FOCUS_CALLOUT = Callout("Focus areas", Box(6.452, 2.753, 6.570, 4.111), accent=FOCUS_ACCENT)


# ════════════════════════════════════════════════════════════════════════════
# Paint helpers.  Each appends shapes in PowerPoint z-order.
# ════════════════════════════════════════════════════════════════════════════
def _paint_funnel_layers(out: list[str], ids: ShapeIds) -> None:
    # Largest band first so every narrower market level stays visible on top.
    for level in FUNNEL_LEVELS:
        out.append(text_box(
            ids.next(),
            f"FunnelLayer_{level.key}",
            *level.layer.emu(),
            [paragraph([], align="ctr", line_spacing=100_000)],
            fill=level.fill,
            line_color=FUNNEL_OUTLINE,
            line_width=3_175,
            prst="ellipse",
        ))


def _paint_definition_table(out: list[str], ids: ShapeIds) -> None:
    out.append(table(
        ids.next(),
        "MarketLevelDefinitionTable",
        *DEFINITION_TABLE.emu(),
        col_widths=[IN(w) for w in DEFINITION_COL_WIDTHS],
        rows=[DEFINITION_HEADER] + [_definition_row(row) for row in DEFINITION_ROWS],
    ))


def _paint_funnel_tags(out: list[str], ids: ShapeIds) -> None:
    for level in FUNNEL_LEVELS:
        out.append(text_box(
            ids.next(),
            f"FunnelTag_{level.key}",
            *level.tag.emu(),
            [paragraph([run(level.name, bold=True, color=level.tag_text_color, font=FONT)], align="ctr", line_spacing=100_000)],
            fill=level.fill,
            line_color="none",
            anchor="ctr",
        ))


def _paint_focus_callout(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(),
        "FocusAreaCallout",
        *FOCUS_CALLOUT.box.emu(),
        [paragraph([run(FOCUS_CALLOUT.text, size=PT(FOCUS_CALLOUT.font_pt), bold=True, italic=True, color=FOCUS_CALLOUT.accent, font=FONT)], line_spacing=100_000)],
        fill=None,
        line_color=FOCUS_CALLOUT.accent,
        line_width=FOCUS_CALLOUT.line_width,
        dashed_line=True,
        anchor="b",
    ))


PAINT_ORDER: tuple[Callable[[list[str], ShapeIds], None], ...] = (
    _paint_funnel_layers,
    _paint_definition_table,
    _paint_funnel_tags,
    _paint_focus_callout,
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
    title="Definitions",
    takeaway="Sizing breaks the market down into four levels and focuses on TAM, SAM, and Available Spend",
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
