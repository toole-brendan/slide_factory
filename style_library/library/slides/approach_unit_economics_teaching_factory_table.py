"""Teaching exemplar: unit-economics normalization matrix.

ROLE
  method_matrix / unit_economics_normalization

USE WHEN
  A slide needs to teach how price, variable-cost, and operating-expense inputs
  move from their native reporting frequency into a per-unit-of-cargo metric
  such as $ / TEU.

TEACHES
  - dense native PowerPoint table authored through low-level table()/trow()/tcell_rich()
  - fully inline table styling: borders, row spans, empty spacer cells, and cell
    padding live inside this module rather than in table_kit.py
  - a seven-column matrix pattern: row-label spine, separator tracks, Annual,
    Per Voyage, and Per Unit columns
  - section-color rules that act as table structure: green Price, gray
    shoreside variable costs, navy vessel-related variable costs, gray Opex
  - source-calibrated empty table-cell paragraphs: 9pt blanks for row fit, 1pt blanks for true spacers
  - dashed normalization callouts layered beside and over the table
  - compact legend keys with two-line no-wrap captions

TEXT-FIT PRECEDENT
  cost_matrix:
    geometry: 12.300in wide x 5.550in high
    columns: 1.500in label · 0.300in spacer · 3.300in Annual · 0.300in spacer ·
             3.300in Per Voyage · 0.300in spacer · 3.300in Per Unit (TEU)
    type: Arial 9pt in table cells, mostly bold, 100% table paragraph spacing
    content: header rows + Price / Variable Costs / Operating Expenses sections
    copy_when: the matrix is the main proof and the row/column intersections are
               more important than surrounding prose
  normalization_callouts:
    geometry: 3.453in x 1.318in and 3.836in x 1.313in explanatory boxes
    type: Arial 9pt italic, centered, 100% line spacing
    copy_when: a table needs procedural instructions that should read as overlay
               annotations rather than separate narrative rails
  legend:
    geometry: 0.200in square keys with 0.200in-high captions
    type: Arial 8pt, no-wrap, often split over two lines with line_break()

SOURCE NOTE
  Teaching rewrite of the source-faithful `approach_unit_economics.py` module.
  The table styling is intentionally inline, as in the teaching rewrite of
  `us_delivery_capacity.py`: borders, padding, empty cells, and rich-cell helpers
  live here so an AI author can study the mechanics without jumping to a central
  table kit. The surrounding slide contract (`LAYOUT`, `CHARTS`, `_body()`,
  `render()`), table geometry, row/column structure, normalization callouts, and
  legend are preserved.

FIDELITY NOTE
  This rewrite is intended to render equivalently to the source-faithful module.
  It keeps the dense native table and source paint order, while splitting the
  authoring code into teaching sections. The matrix remains a low-level OOXML
  table rebuild rather than a higher-level semantic table abstraction because the
  precise borders, row spans, and spacer cells are the lesson.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, run, table, tcell_rich,
    text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_5 = "263746"
GRAY_3 = "BFBFBF"
GRAY_4 = "7F7F7F"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: comments the module can expose programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "method_matrix",
    "use_when": (
        "Use for a dense methodology matrix where each row item must be placed "
        "in the frequency column where it is reported or incurred, then annotated "
        "with normalization logic."
    ),
    "teaches": [
        "native table primitive",
        "inline table-cell kit",
        "row spans and grid spans",
        "source-sized blank cells plus tiny true spacer cells",
        "section-colored border rules",
        "dense 9pt table labels",
        "dashed normalization callouts",
        "compact no-wrap legend captions",
    ],
}

TEXT_FIT = {
    "cost_matrix": {
        "box_in": (12.300, 5.550),
        "columns_in": (1.500, 0.300, 3.300, 0.300, 3.300, 0.300, 3.300),
        "font_pt": 9,
        "content": "dense Price / Variable Costs / Operating Expenses frequency matrix",
        "note": (
            "Most table rows have zero minimum height; the combination of rich "
            "cell content, 60960 EMU padding, source-sized 9pt blanks, and tiny "
            "1pt spacer blanks controls the apparent row heights."
        ),
    },
    "empty_matrix_cells": {
        "font_pt": "1 or 9",
        "content": "empty tpara([]) with end_size=PT(1) for spacers and PT(9) for source-sized blanks",
        "note": "Use PT(1) when spacer rows/cells must collapse; use PT(9) where the reference table relies on a blank cell to preserve row fit.",
    },
    "normalization_callouts": {
        "font_pt": 9,
        "content": "italic procedural instructions over dashed callout geometry",
        "note": "Centered 100% line spacing; zero left/right insets where text spans the full dashed region.",
    },
    "legend": {
        "key_in": (0.200, 0.200),
        "font_pt": 8,
        "content": "four category keys; captions are no-wrap and often split with line_break()",
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
class LegendKey:
    label: str
    box: Box
    fill: str
    fit_note: str


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: one full-width matrix plus right-side normalization overlays.
# ════════════════════════════════════════════════════════════════════════════
SLIDE_TITLE = TextZone(
    name="Title",
    box=Box(0.495, 0.607, 12.300, 0.650),
    font_pt=20,
    fit_note="House title placeholder; long subtitle is already tested in source.",
)

COST_MATRIX_TABLE = TextZone(
    name="CostCategoryMatrix",
    box=Box(0.517, 1.407, 12.300, 5.550),
    font_pt=9,
    fit_note="The primary object: a dense native table with explicit borders and spans.",
)

COST_MATRIX_COLUMNS: tuple[TableColumn, ...] = (
    TableColumn("row label", 1.500, "Section labels: Price / Variable Costs / Operating Expenses."),
    TableColumn("left separator", 0.300, "Spacer track that carries colored section rules."),
    TableColumn("Annual", 3.300, "Annual Opex items live here before normalization."),
    TableColumn("middle separator", 0.300, "Spacer / inner rule track."),
    TableColumn("Per Voyage", 3.300, "Per-voyage cost-of-sales items."),
    TableColumn("right separator", 0.300, "Spacer / inner rule track."),
    TableColumn("Per Unit (TEU)", 3.300, "Already-normalized price and variable-cost cells."),
)

PRICE_GREEN = "2E7D32"
OPEX_GRAY = "808080"
SECTION_RULE_W = 76_200       # 6pt section dividers, matching the source table
HAIRLINE_W = 6_350            # 0.5pt white hairline in the source grid
PAD = dict(l_ins=60_960, r_ins=60_960, t_ins=60_960, b_ins=60_960)

_KEY_W, _KEY_H = IN(0.2), IN(0.2)
_LEGEND_H = IN(0.2)

# The four cost-category keys appear as color keys; captions paint around them in
# the original order, so the caption text boxes remain explicit below.
_LEGEND_KEYS: tuple[tuple[float, float, str], ...] = (
    (9.919, 1.164, BLUE_5),    # Price components: navy in the source legend
    (8.880, 1.164, PRICE_GREEN),
    (11.058, 1.164, GRAY_3),
    (12.197, 1.164, GRAY_4),
)

OPEX_ANNUAL_ITEMS: tuple[str, ...] = (
    "Insurance",
    "Stores & Spares",
    "Lubricating Oils",
    "Repair & Maintenance",
    "Dry-dock",
    "Management & Administration",
    "Depreciation & Amortization",
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: intentionally local / inline for teaching.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def mt(align="ctr", *, end_size=PT(1)):
    """Empty matrix-cell paragraph.

    The default end_size=PT(1) is a table-fit trick: true spacer cells stay
    empty and do not expand to LibreOffice / PowerPoint's default text height.
    Use mt9() for the source-calibrated blank cells whose 9pt end paragraph
    participates in the row-height balance of the Matson reference render.
    """

    return tpara([], align=align, mar_l=0, indent=0, end_size=end_size)


def mt9(align="ctr"):
    """Source-sized empty matrix-cell paragraph (9pt end run).

    The source-faithful Matson module alternates 9pt blank cells with tiny 1pt
    spacer cells. Keeping that distinction preserves the table's PowerPoint row
    fitting while leaving the teaching call sites readable.
    """

    return mt(align, end_size=PT(9))


def tx(text, *, color=BLACK, align="ctr", bold=True, italic=False, size=PT(9)):
    """One-run matrix-cell paragraph: PT9 Arial, bold by default."""

    return tpara(
        [trun(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align,
        mar_l=0,
        indent=0,
    )


def rcell(
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

    Insets default to the primitive/table default; pass **PAD for the source's
    heavier 60_960 EMU matrix-cell padding. Borders stay inline via L/R/T/B.
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
        borders=bd(**edges),
    )


def paint_cost_matrix(out: list[str], ids: ShapeIds) -> None:
    """Paint the dense cost-category matrix.

    The matrix is deliberately low-level: spacer cells, border sides, row spans,
    and insets are the styling system. Keeping them inline makes this module a
    teaching example for future AI-authored native tables.
    """
    out.append(table(ids.next(), "UnitEconomicsCostMatrix", *COST_MATRIX_TABLE.box.emu(),
        col_widths=[IN(column.width_in) for column in COST_MATRIX_COLUMNS], rows=[
        # ── header: frequency banner over Annual / Per Voyage / Per Unit ──
        trow([
            rcell([tx("For each route and vessel size / type", align="l", bold=False, italic=True)], rowspan=2, anchor="b", B=edge(BLACK)),
            rcell([mt9()], anchor="b"),
            rcell([tx("Price / cost categories by frequency (reported or incurred)")], span=5, anchor="b", B=edge(DK)),
        ], h=IN(0.129)),
        trow([
            rcell([mt9()], anchor="b", B=edge(BLACK)),
            rcell([tx("Annual")], anchor="b", R=edge(WHITE), T=edge(DK), B=edge(BLACK)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(DK), B=edge(BLACK)),
            rcell([tx("Per Voyage")], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(DK), B=edge(BLACK)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(DK), B=edge(BLACK)),
            rcell([tx("Per Unit (TEU)")], anchor="b", **PAD, L=edge(WHITE), T=edge(DK), B=edge(BLACK)),
        ], h=IN(0)),
        # ── black top rule under the banner ──
        trow([
            rcell([mt("l")], T=edge(BLACK)),
            rcell([mt()], anchor="b", T=edge(BLACK)),
            rcell([mt()], anchor="b", R=edge(WHITE), T=edge(BLACK)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(BLACK)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(BLACK)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(BLACK)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(BLACK)),
        ], h=IN(0)),
        # ── Price (green section rule) ──
        trow([
            rcell([tx("Price", align="l")], anchor="t", R=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([tx("Basic Ocean Rate", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt9("l")], R=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([tx("Fuel Adjustment Factor", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt9("l")], R=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(WHITE, HAIRLINE_W)),
            rcell([tx("Terminal Handling / Stevedoring", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt9("l")], R=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge("2E7D32", SECTION_RULE_W)),
            rcell([mt9()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE, HAIRLINE_W), B=edge(WHITE, HAIRLINE_W)),
            rcell([tx("Wharfage / Other Fees", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE, HAIRLINE_W)),
        ], h=IN(0)),
        # ── spacer (Price → Variable Costs) ──
        trow([
            rcell([mt("l")], R=edge(WHITE)),
            rcell([mt()], anchor="b", L=edge(WHITE)),
            rcell([mt()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE, HAIRLINE_W), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE, HAIRLINE_W), B=edge(WHITE)),
        ], h=IN(0)),
        # ── Variable Costs (gray shoreside / blue vessel); label spans 2 rows ──
        trow([
            rcell([tx("Variable Costs ", align="l")], anchor="t", rowspan=2, R=edge(GRAY_3, SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge(GRAY_3, SECTION_RULE_W)),
            rcell([mt9()], anchor="b"),
            rcell([mt()], anchor="b", **PAD, T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Pilotage & Tugboats")], fill=GRAY_3, anchor="b", **PAD, R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Terminal Handling & Stevedoring", color=WHITE)], fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt9()], anchor="b", L=edge(GRAY_3, SECTION_RULE_W)),
            rcell([mt9()], anchor="b"),
            rcell([mt()], anchor="b", **PAD, T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Bunker fuel")], fill=GRAY_3, anchor="b", **PAD, R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Wharfage & Other Fees", color=WHITE)], fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt9("l")], R=edge(GRAY_3, SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge(GRAY_3, SECTION_RULE_W)),
            rcell([mt9()], anchor="b"),
            rcell([mt()], anchor="b", **PAD, T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Dockage & Other Usage Fees", color=WHITE)], fill=BLUE_5, anchor="b", **PAD, R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], fill=GRAY_3, anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        # ── spacer (Variable Costs → Operating Expenses) ──
        trow([
            rcell([mt("l")], R=edge(WHITE)),
            rcell([mt()], anchor="b", L=edge(WHITE)),
            rcell([mt()], anchor="b", R=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        # ── Operating Expenses (dark gray); label spans 8 rows. First row = Crew. ──
        trow([
            rcell([tx("Operating Expenses", align="l")], anchor="t", rowspan=8, R=edge(OPEX_GRAY, SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge(OPEX_GRAY, SECTION_RULE_W)),
            rcell([tx("Crew", color=WHITE)], fill=OPEX_GRAY, anchor="b", R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        # the remaining 7 Opex line items are one uniform family (label in the Annual column):
        *[trow([
            rcell([mt9()], anchor="b", L=edge(OPEX_GRAY, SECTION_RULE_W)),
            rcell([tx(_label, color=WHITE)], fill=OPEX_GRAY, anchor="b", R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)) for _label in OPEX_ANNUAL_ITEMS],
        # ── final Opex row (outside the 8-row span): Other ──
        trow([
            rcell([mt9("l")], R=edge(OPEX_GRAY, SECTION_RULE_W)),
            rcell([mt9()], anchor="b", L=edge(OPEX_GRAY, SECTION_RULE_W)),
            rcell([tx("Other (e.g., Travel)", color=WHITE)], fill=OPEX_GRAY, anchor="b", R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt9()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
    ]))


def paint_normalization_callouts(out: list[str], ids: ShapeIds) -> None:
    """Dashed boxes and arrows that explain how table cells normalize to $ / TEU."""
    # Normalization annotations retain explicit zero side padding where text
    # must span the full dashed region; anchor/paragraph align state vertical
    # and horizontal placement independently.
    out.append(text_box(ids.next(), "CostOfSalesNormalizationCallout", IN(5.827), IN(3.316), IN(3.453), IN(1.318), [paragraph([run("To find Normalized Cost of Sales: Divide by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("average cargo units per relevant voyage", size=PT(9), italic=True, underline=True, color=BLACK, font=FONT), run(" (route-specific volume)", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b", l_ins=0, r_ins=0))   # 000000 black outline
    out.append(text_box(ids.next(), "VariableCostNormalizationFrame", IN(2.25), IN(4.354), IN(3.453), IN(2.616), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b"))   # 000000 black outline
    out.append(connector(ids.next(), "NormalizedVariableCostLeader", IN(9.28), IN(3.975), IN(0.225), IN(0.124), color=BLACK, width=12700, arrow=True, prst="bentConnector3"))   # 000000 black
    out.append(text_box(ids.next(), "NormalizedVariableCostLabel", IN(9.505), IN(3.963), IN(3.289), IN(0.273), [paragraph([run("Normalized (per unit) Variable Costs", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="ctr"))   # 000000 black outline
    out.append(text_box(ids.next(), "NormalizedOpexPanel", IN(9.53), IN(4.411), IN(3.289), IN(2.347), [paragraph([run("Normalized (per unit) Opex", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=OPEX_GRAY, line_color=BLACK, dashed_line=True, anchor="ctr"))   # 808080 gray
    out.append(text_box(ids.next(), "OpexNormalizationNarrative", IN(5.697), IN(5.674), IN(3.836), IN(1.313), [paragraph([run("To find Normalized Opex:", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Multiply ", size=PT(9), italic=True, color=BLACK, font=FONT), run("annual Opex", size=PT(9), italic=True, underline=True, color=BLACK, font=FONT), run(" by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("proportion of relevant days", size=PT(9), italic=True, underline=True, color=BLACK, font=FONT), run(" to find annual Opex per route, then divide by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("annual relevant voyages", size=PT(9), italic=True, underline=True, color=BLACK, font=FONT), run(" to find Opex per voyage, then divide by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("average cargo units per relevant voyage", size=PT(9), italic=True, underline=True, color=BLACK, font=FONT), run(" (route-specific volume)", size=PT(9), italic=True, color=BLACK, font=FONT), line_break(), line_break(), run("To find proportion of relevant days: Days on route + days idle (loiter, maintenance, in port) attributable to a given route / 365 days", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))   # 000000 black
    out.append(connector(ids.next(), "OpexNormalizationLeader", IN(5.703), IN(5.585), IN(3.827), IN(0.077), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))   # 000000 black


def paint_cost_category_legend(out: list[str], ids: ShapeIds) -> None:
    """Compact cost-category keys and no-wrap captions."""
    out.append(text_box(ids.next(), "PriceComponentsLegendLabel", IN(9.1), IN(1.164), IN(0.8), _LEGEND_H, [paragraph([run("Price", size=PT(8), color=BLACK, font=FONT), line_break(), run("Components", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── legend: cost-category visual keys + captions ──
    # Keys use empty centered bodies; caption boxes are centered vertically,
    # no-wrap, and retain default internal padding.
    for _x, _y, _fill in _LEGEND_KEYS:
        out.append(text_box(ids.next(), "LegendColorKey", IN(_x), IN(_y), _KEY_W, _KEY_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(text_box(ids.next(), "ShoresideVariableCostLegendLabel", IN(10.139), IN(1.164), IN(0.9), _LEGEND_H, [paragraph([run("Shoreside ", size=PT(8), color=BLACK, font=FONT), line_break(), run("variable costs", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(ids.next(), "VesselVariableCostLegendLabel", IN(11.278), IN(1.165), IN(0.9), _LEGEND_H, [paragraph([run("Vessel-related ", size=PT(8), color=BLACK, font=FONT), line_break(), run("variable costs", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(ids.next(), "OpexLegendLabel", IN(12.417), IN(1.164), IN(0.4), _LEGEND_H, [paragraph([run("Opex", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_cost_matrix(out, ids)
    paint_normalization_callouts(out, ids)
    paint_cost_category_legend(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="Carrier Entry Point Attractiveness",
    topic="Matson Test Case",
    title="Approach (1/2)",
    takeaway="Determining unit economics requires normalizing annual operating expenses and per-voyage cost of sales to a per-unit of cargo basis ($ / TEU).",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
