"""key_findings_what_must_be_true — Commercial Strategy Market Analysis deck (20260325), source slide 10.

EXHIBIT — "Key Findings (3/3)": the "what must be true to succeed" wrap-up for the
commercial oceangoing focus. The whole slide is one native table — a market ×
vessel-class matrix. Across the top, four market columns shade darker left-to-
right (CEDDEC → 99B9D8 → 447BB2 → 223E59): 1. Marine Highway · 2. Existing Jones
Act Routes · 3. US-Built & Flagged International Trade · 4. Foreign-Flagged
International Trade, each with a one-line Description row. Down the left spine,
vessel classes (All Vessels · Container → 350' Feeder / 900' Panamax · Tanker →
Product / Crude) key the rows. The cells carry the per-market "must be true"
bullet lists (Jones Act stays, autonomy pays for itself, SHIPS Act / Building
Ships in America Act / Tanker Security Program pass with revisions, ROK/Japan
yards build, …) plus italic competitiveness caveats. Two free-floating callouts
sit below the table.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ......... breadcrumb() + title_placeholder() + prelim_chip()
  • matrix ......... one table() (low-level table()/trow()/tcell()/tcell_rich();
                     merges via grid_span/row_span, rotated spine via cell anchor) —
                     market columns × vessel-class rows + the "must be true" bullets
  • callouts ....... "To determine market addressability" (centred italic note) and
                     "Further analysis required…" (dashed Rectangle 10)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=2, table=1, chrome_builders=3, dropped=1 (think-cell
OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun,
    breadcrumb, title_placeholder, prelim_chip, IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_3,
    FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (borders,
#    spans). Renders identically to the raw tcell()/tcell_rich() form — the only
#    change is legibility. ──


def r(text, *, b=False, i=False, u=False, color=BLACK, size=PT(10)):
    """One styled run (Arial FONT; size defaults to this matrix's dominant PT10)."""
    return trun(text, size=size, bold=b or None, italic=i or None, underline=u or None, color=color, font=FONT)


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
    out.append(breadcrumb("Commercial Strategy", "Research Overview"))
    out.append(title_placeholder("Key Findings (3/3)", "What must be true to succeed (commercial oceangoing focus)."))
    out.append(prelim_chip())
    # ── matrix — market columns × vessel-class rows + "must be true" bullets ──
    # col_widths defines the six market/spine tracks and trow(h=...) their
    # minimum heights. Repeated insets/anchor/align encode row/column padding
    # and vertical/horizontal alignment; tpara mar_l/indent carries bullets.
    # palette — text: 000000 black (labels/bullets) · FFFFFF white & F2F2F2 off-white (dark-cell text) · 162029 dark navy (cross-ref);
    #   fills (market cols L→R): CEDDEC pale blue · 99B9D8 light blue · 447BB2 blue · 223E59 navy; spine/caveat fills: F2F2F2 off-white · BFBFBF silver-gray · 808080 gray;
    #   rules: FFFFFF white (inner) · 000000 black (header/section) · 808080 gray (row).
    out.append(table(n(), "Table 4", IN(0.494), IN(1.495), IN(12.3), IN(5), col_widths=[IN(0.207), IN(0.804), IN(2.822), IN(2.822), IN(2.822), IN(2.822)], rows=[
        trow([cell("Market:", size=PT(10), italic=True, align="r", span=2), cell("1. Marine Highway", size=PT(10), bold=True, align="ctr", fill="CEDDEC", anchor="b", R=edge(WHITE), B=edge(WHITE)), cell("2. Existing Jones Act Routes", size=PT(10), bold=True, color=BLACK, align="ctr", fill="99B9D8", anchor="b", L=edge(WHITE), R=edge(WHITE), B=edge(WHITE)), rcell([tpara([r("3. US-Built & Flagged International Trade", b=1, color=GRAY_1)], align="ctr", mar_l=0, indent=0)], fill="447BB2", anchor="b", L=edge(WHITE), R=edge(WHITE), B=edge(WHITE)), rcell([tpara([r("4. Foreign-Flagged International Trade", b=1, color=GRAY_1)], align="ctr", mar_l=0, indent=0)], fill="223E59", anchor="b", L=edge(WHITE), B=edge(WHITE))], h=IN(0)),
        trow([cell("Description:", size=PT(10), italic=True, align="r", span=2, B=edge(BLACK)), rcell([tpara([r("Displaces domestic truck / rail", i=1)], align="ctr", mar_l=0, indent=0)], fill="CEDDEC", R=edge(WHITE), T=edge(WHITE), B=edge(BLACK)), cell("Current OCONUS routes", size=PT(10), italic=True, color=BLACK, align="ctr", fill="99B9D8", L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(BLACK)), rcell([tpara([r("SCF & other USG programs", i=1, color=WHITE)], align="ctr", mar_l=0, indent=0)], fill="447BB2", L=edge(WHITE), R=edge(WHITE), T=edge(WHITE), B=edge(BLACK)), rcell([tpara([r("Ex-SCF foreign trade", i=1, color=GRAY_1)], align="ctr", mar_l=0, indent=0)], fill="223E59", L=edge(WHITE), T=edge(WHITE), B=edge(BLACK))], h=IN(0)),
        trow([rcell([tpara([r("All Vessels", b=1)], mar_l=0, indent=0)], span=2, T=edge(BLACK), B=edge("808080", 6350)), rcell([tpara([r("Port Alpha drives 30-40%+ lower newbuild costs vs. US-based incumbents")], align="ctr", mar_l=0, indent=0)], span=3, T=edge(BLACK), B=edge("808080", 6350)), rcell([tpara([r("PA prices challenge competitiveness", i=1)], align="ctr", mar_l=0, indent=0)], fill=GRAY_1, T=edge(BLACK), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Container", b=1)], align="ctr", mar_l=0, indent=0)], fill=GRAY_3, rowspan=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("350’ Feeder", b=1)], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Jones Act remains in place ")], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Regulatory environment supports autonomy")], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Vessel ITC eligibility extends to domestic")], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Autonomy enables revenue growth and/or cost savings that offsets new expenses (i.e., SW license, remote ops. center)")], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Marine transport achieves lower end-to-end costs vs. onshore modes")], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Terminal access ensures requisite service level (e.g., rapid turns for fast deliveries)")], bullet=True, mar_l=112713, indent=-112713)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Size limits TEU capacity, challenging competitiveness", i=1)], align="ctr", level=2, mar_l=112713, indent=0)], fill=GRAY_1, span=3, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.625)),
        trow([rcell([tpara([r("900’ Panamax", b=1)], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([], align="ctr", mar_l=0, indent=0)], fill=GRAY_1, rowspan=3, T=edge("808080", 6350)), rcell([tpara([r("Same considerations as 350’ Maritime Highway", color=DK)], align="ctr", mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("SHIPS Act passes with revisions:", b=1)], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Universal fee imposed on all cargo imported by foreign-built ships")], bullet=True, bullet_char="−", level=2, mar_l=227013, indent=-114300),
            tpara([r("Subsidies cover full opex and D&A differential between US & foreign")], bullet=True, bullet_char="−", level=2, mar_l=227013, indent=-114300),
            tpara([r("Building Ships in America Act passes with revisions:", b=1)], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("ITC eligibility increases beyond ‘32 ")], bullet=True, bullet_char="−", level=2, mar_l=227013, indent=-114300),
            tpara([r("Tanker Security Program expands:", b=1)], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Fleet cap increases to 30 vessels with US-built requirement")], bullet=True, bullet_char="−", level=2, mar_l=227013, indent=-114300),
            tpara([r("Subsidies cover full opex and D&A differential between US & foreign")], bullet=True, bullet_char="−", level=2, mar_l=227013, indent=-114300)], rowspan=3, T=edge("808080", 6350)), rcell([tpara([r("ROK / Japan yards build vessels "), r("(to confirm price) ", i=1)], bullet=True, mar_l=112713, indent=-112713),
            tpara([r("Autonomy enables revenue growth and/or cost savings that offsets new expenses (i.e., SW license, remote ops. center)")], bullet=True, mar_l=112713, indent=-112713)], rowspan=3, T=edge("808080", 6350))], h=IN(0.14)),
        trow([rcell([tpara([r("Tanker", b=1, color=WHITE)], align="ctr", mar_l=0, indent=0)], fill="808080", rowspan=2, T=edge("808080", 6350)), rcell([tpara([r("Product", b=1)], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([], align="ctr", mar_l=0, indent=0)], fill=GRAY_1, rowspan=2, T=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Crude", b=1)], mar_l=0, indent=0)], T=edge("808080", 6350))], h=IN(0.83)),
    ]))
    # ── annotation boxes below the table ──
    # The first uses zero paragraph margins and centered horizontal alignment;
    # the dashed box uses centered paragraph alignment with default padding.
    out.append(text_box(n(), "TextBox 7", IN(3.078), IN(5.442), IN(3.112), IN(0.269), [paragraph([run("To determine market addressability", size=PT(10), italic=True, color=DK, font=FONT)], align="ctr", mar_l=0, indent=0, space_after=0, line_spacing=100000)], fill=None, line_color="none"))   # 162029 dark navy
    out.append(text_box(n(), "Rectangle 10", IN(7.143), IN(3.825), IN(2.805), IN(2.67), [paragraph([run("Further analysis required to determine attractiveness for OpCo", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True))   # 000000 black outline
    return "".join(out)


def render() -> str:
    return slide(_body())
