"""approach_unit_economics — Commercial Strategy market-analysis deck (20260325), source slide 120.

EXHIBIT — "Approach (1/2)": determining unit economics requires normalizing annual
operating expenses and per-voyage cost of sales to a per-unit-of-cargo basis
($ / TEU). The slide is dominated by one large price/cost-category matrix — rows
grouped into Price, Variable Costs, and Operating Expenses; columns by reporting/
incurred frequency (Annual / Per Voyage / Per Unit (TEU)); cells name the specific
line items (Basic Ocean Rate, Bunker fuel, Crew, Insurance, Dry-dock, …). Dashed
normalization callouts on the right explain how to convert to per-unit Variable
Costs and per-unit Opex; a colour legend keys the cost categories.

This is the table-heaviest module in the set: the matrix is a single low-level
table() with grid_span / row_span merges and per-cell borders — a worked example
of reconstructing a dense native <a:tbl>. Cell content is built with
tcell_rich()/tpara()/trun() (rich runs), not the plain tcell() helper.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder()
  • table ............ the cost-category matrix (the bulk of the slide)
  • normalization ..... dashed callout boxes + elbow connectors ($ → $ / TEU)
  • _LEGEND_KEYS ...... cost-category visual keys + caption text boxes

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic — NO coordinate, value, colour, or paint-order changed,
so the render is byte-identical to the raw port.

Converter stats: text_box=9, connector=2, table=1, chrome_builders=2,
clusters=1 (covering 4 shapes), dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, tcell_rich,
    tpara, trun, breadcrumb, title_placeholder, IN, PT, BLACK, WHITE, DK, BLUE_5, GRAY_3,
    GRAY_4, FONT, edge, bd, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell_rich() form — the only
#    change is legibility. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


def mt(align="ctr"):
    """An empty matrix-cell paragraph (borders/spacing only, no text). end_size=PT(1) keeps the
    cell's <a:endParaRPr> tiny so LibreOffice doesn't floor the row at its ~18pt default.
    Kept local (not in table_kit): the matrix end_size differs across slides."""
    return tpara([], align=align, mar_l=0, indent=0, end_size=PT(1))


def tx(text, *, color=BLACK, align="ctr", bold=True, italic=False, size=PT(9)):
    """A one-run matrix-cell paragraph (PT9 Arial, bold by default — the matrix norm)."""
    return tpara([trun(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
                 align=align, mar_l=0, indent=0)


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_SWATCH_W, _SWATCH_H = IN(0.2), IN(0.2)    # legend colour-chip size
_LEGEND_H = IN(0.2)       # legend caption height                 [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the four cost-category colour chips (price / shoreside / vessel / opex).
_LEGEND_KEYS = [    # (x, y, fill) x4 — cost-category visual keys (price / shoreside / vessel / opex)
    (9.919, 1.164, BLUE_5),    # 263746 navy
    (8.88, 1.164, "2E7D32"),   # 2E7D32 green
    (11.058, 1.164, GRAY_3),   # BFBFBF silver-gray
    (12.197, 1.164, GRAY_4),   # 7F7F7F gray
]
# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level layout convention is expressed by repeating the
# same l_ins/r_ins/t_ins/b_ins, anchor, and alignment across the affected cells.
# In tcell()/tcell_rich(), those insets are internal padding and anchor is vertical
# alignment; tcell align or tpara align/mar_l/indent controls horizontal alignment
# and paragraph margins (including hanging bullet indents).

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Explicit zero/tight insets and wrap="none"
# are alignment devices for chart/exhibit labels; omitted values retain the
# primitive defaults intentionally.


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Approach (1/2)", "Determining unit economics requires normalizing annual operating expenses and per-voyage cost of sales to a per-unit of cargo basis ($ / TEU)."))
    # Native matrix table: col_widths defines the seven column tracks and
    # trow(h=...) each row minimum. Repeated cell insets/anchor/align act as
    # row/column padding and alignment policies; tpara mar_l/indent owns
    # paragraph and bullet margins inside each cell.
    # The cost matrix: a 7-column grid (label | sep | Annual | sep | Per Voyage | sep |
    # Per Unit (TEU)). Most cells are empty and exist only to draw the white inner
    # gridlines / coloured section rules; the kit (rcell/tx/mt/edge/PAD) keeps each cell
    # one short line. Category labels span rows; the column banner spans 5 cols.
    # palette — text: 000000 black (labels) · FFFFFF white (in-fill labels); fills: 2E7D32 green (Price) ·
    #   BFBFBF silver-gray (shoreside) · 263746 navy (vessel) · 808080 gray (Opex);
    #   rules: 000000 black (top/banner) · 162029 dark navy (banner) · FFFFFF white (inner) · section: 2E7D32 green / BFBFBF silver-gray / 808080 gray.
    out.append(table(n(), "Table 8", IN(0.517), IN(1.407), IN(12.3), IN(5.55),
        col_widths=[IN(1.5), IN(0.3), IN(3.3), IN(0.3), IN(3.3), IN(0.3), IN(3.3)], rows=[
        # ── header: frequency banner over Annual / Per Voyage / Per Unit ──
        trow([
            rcell([tx("For each route and vessel size / type", align="l", bold=False, italic=True)], rowspan=2, anchor="b", B=edge(BLACK)),
            rcell([mt()], anchor="b"),
            rcell([tx("Price / cost categories by frequency (reported or incurred)")], span=5, anchor="b", B=edge(DK)),
        ], h=IN(0.129)),
        trow([
            rcell([mt()], anchor="b", B=edge(BLACK)),
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
            rcell([tx("Price", align="l")], R=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", L=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([tx("Basic Ocean Rate", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt("l")], R=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", L=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([tx("Fuel Adjustment Factor", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt("l")], R=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", L=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(WHITE, 6350)),
            rcell([tx("Terminal Handling / Stevedoring", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt("l")], R=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", L=edge("2E7D32", 76200)),
            rcell([mt()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE, 6350), B=edge(WHITE, 6350)),
            rcell([tx("Wharfage / Other Fees", color=WHITE)], fill="2E7D32", anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE, 6350)),
        ], h=IN(0)),
        # ── spacer (Price → Variable Costs) ──
        trow([
            rcell([mt("l")], R=edge(WHITE)),
            rcell([mt()], anchor="b", L=edge(WHITE)),
            rcell([mt()], anchor="b", R=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE, 6350), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE, 6350), B=edge(WHITE)),
        ], h=IN(0)),
        # ── Variable Costs (gray shoreside / blue vessel); label spans 2 rows ──
        trow([
            rcell([tx("Variable Costs ", align="l")], rowspan=2, R=edge(GRAY_3, 76200)),
            rcell([mt()], anchor="b", L=edge(GRAY_3, 76200)),
            rcell([mt()], anchor="b"),
            rcell([mt()], anchor="b", **PAD, T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Pilotage & Tugboats")], fill=GRAY_3, anchor="b", **PAD, R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Terminal Handling & Stevedoring", color=WHITE)], fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt()], anchor="b", L=edge(GRAY_3, 76200)),
            rcell([mt()], anchor="b"),
            rcell([mt()], anchor="b", **PAD, T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Bunker fuel")], fill=GRAY_3, anchor="b", **PAD, R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Wharfage & Other Fees", color=WHITE)], fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        trow([
            rcell([mt("l")], R=edge(GRAY_3, 76200)),
            rcell([mt()], anchor="b", L=edge(GRAY_3, 76200)),
            rcell([mt()], anchor="b"),
            rcell([mt()], anchor="b", **PAD, T=edge(WHITE), B=edge(WHITE)),
            rcell([tx("Dockage & Other Usage Fees", color=WHITE)], fill=BLUE_5, anchor="b", **PAD, R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], fill=GRAY_3, anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
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
            rcell([tx("Operating Expenses", align="l")], rowspan=8, R=edge("808080", 76200)),
            rcell([mt()], anchor="b", L=edge("808080", 76200)),
            rcell([tx("Crew", color=WHITE)], fill="808080", anchor="b", R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
        # the remaining 7 Opex line items are one uniform family (label in the Annual column):
        *[trow([
            rcell([mt()], anchor="b", L=edge("808080", 76200)),
            rcell([tx(_label, color=WHITE)], fill="808080", anchor="b", R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)) for _label in ("Insurance", "Stores & Spares", "Lubricating Oils",
                                   "Repair & Maintenance", "Dry-dock",
                                   "Management & Administration", "Depreciation & Amortization")],
        # ── final Opex row (outside the 8-row span): Other ──
        trow([
            rcell([mt("l")], R=edge("808080", 76200)),
            rcell([mt()], anchor="b", L=edge("808080", 76200)),
            rcell([tx("Other (e.g., Travel)", color=WHITE)], fill="808080", anchor="b", R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
            rcell([mt()], anchor="b", **PAD, L=edge(WHITE), T=edge(WHITE), B=edge(WHITE)),
        ], h=IN(0)),
    ]))
    # Normalization annotations retain explicit zero side padding where text
    # must span the full dashed region; anchor/paragraph align state vertical
    # and horizontal placement independently.
    out.append(text_box(n(), "Rectangle 19", IN(5.827), IN(3.316), IN(3.453), IN(1.318), [paragraph([run("To find Normalized Cost of Sales: Divide by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("average cargo units per relevant voyage", size=PT(9), italic=True, color=BLACK, font=FONT), run(" (route-specific volume)", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b", l_ins=0, r_ins=0))   # 000000 black outline
    out.append(text_box(n(), "Rectangle 20", IN(2.25), IN(4.354), IN(3.453), IN(2.616), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b"))   # 000000 black outline
    out.append(connector(n(), "Connector: Elbow 22", IN(9.28), IN(3.975), IN(0.225), IN(0.124), color=BLACK, width=12700, arrow=True, prst="bentConnector3"))   # 000000 black
    out.append(text_box(n(), "Rectangle 25", IN(9.505), IN(3.963), IN(3.289), IN(0.273), [paragraph([run("Normalized (per unit) Variable Costs", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="ctr"))   # 000000 black outline
    out.append(text_box(n(), "Rectangle 32", IN(9.53), IN(4.411), IN(3.289), IN(2.347), [paragraph([run("Normalized (per unit) Opex", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="808080", line_color=BLACK, dashed_line=True, anchor="ctr"))   # 808080 gray
    out.append(text_box(n(), "TextBox 41", IN(5.697), IN(5.674), IN(3.836), IN(1.313), [paragraph([run("To find Normalized Opex:", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Multiply ", size=PT(9), italic=True, color=BLACK, font=FONT), run("annual Opex", size=PT(9), italic=True, color=BLACK, font=FONT), run(" by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("proportion of relevant days", size=PT(9), italic=True, color=BLACK, font=FONT), run(" to find annual Opex per route, then divide by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("annual relevant voyages", size=PT(9), italic=True, color=BLACK, font=FONT), run(" to find Opex per voyage, then divide by ", size=PT(9), italic=True, color=BLACK, font=FONT), run("average cargo units per relevant voyage", size=PT(9), italic=True, color=BLACK, font=FONT), run(" (route-specific volume)", size=PT(9), italic=True, color=BLACK, font=FONT), line_break(), line_break(), run("To find proportion of relevant days: Days on route + days idle (loiter, maintenance, in port) attributable to a given route / 365 days", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 42", IN(5.703), IN(5.585), IN(3.827), IN(0.077), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))   # 000000 black
    out.append(text_box(n(), "TextBox 46", IN(9.1), IN(1.164), IN(0.8), _LEGEND_H, [paragraph([run("Price", size=PT(8), color=BLACK, font=FONT), line_break(), run("Components", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── legend: cost-category visual keys + captions ──
    # Keys use empty centered bodies; caption boxes are centered vertically,
    # no-wrap, and retain default internal padding.
    for _x, _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "TextBox 48", IN(10.139), IN(1.164), IN(0.9), _LEGEND_H, [paragraph([run("Shoreside ", size=PT(8), color=BLACK, font=FONT), line_break(), run("variable costs", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 51", IN(11.278), IN(1.165), IN(0.9), _LEGEND_H, [paragraph([run("Vessel-related ", size=PT(8), color=BLACK, font=FONT), line_break(), run("variable costs", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 53", IN(12.417), IN(1.164), IN(0.4), _LEGEND_H, [paragraph([run("Opex", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    return "".join(out)


def render() -> str:
    return slide(_body())
