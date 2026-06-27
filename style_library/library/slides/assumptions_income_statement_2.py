"""assumptions_income_statement_2 — Commercial Strategy Market Analysis deck (20260325), source slide 78.

EXHIBIT — "Assumptions & Methodology | Income Statement (2/2)": the second of two
methodology back-up pages for BuildCo's financial projections. The whole slide is
essentially one big reference table documenting how each Operating-Expense line of
the income statement is modelled. Three columns — Category / Component /
Methodology — with a single "Operating Expenses" category spanning thirteen
component rows (Compensation, Professional Services, Fringe, Legal, IT & Software,
D&A, SBC, Travel & Entertainment, Equipment & Material Maintenance, Facilities,
Marketing/PR/Events, Insurance), each Methodology cell a bulleted list of the rate
assumptions (e.g. "5% YoY increase in rates", "Fringe rate of 37.6% applied to
Compensation", "Construction depreciated over 40-yr. useful life"). A Preliminary
chip and a Source footnote close it out.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • title block ...... two RAW-verbatim <p:sp> layout placeholders (kept byte-for-
                       byte): the body crumb "BuildCo Financial Projections /
                       Assumptions & Methodology" and the title "… Income
                       Statement (2/2)." — both geometry-less (no explicit xfrm)
  • assumptions table  the one substantive object: table() "Table 3", Category /
                       Component / Methodology, built low-level via trow()/
                       tcell_rich()/tpara()/trun() so the Methodology cells can
                       carry bulleted multi-paragraph rate notes
  • prelim_chip ...... house "Preliminary" watermark (the only chrome builder)
  • source footnote .. "Rectangle 8" Source line, kept verbatim off the house
                       Source position (see Residue)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=1, table=1, chrome_builders=1, raw_verbatim=2,
dropped=1 (think-cell OLE frame).
Residue: two RAW-verbatim title/crumb placeholders carried as literal OOXML (no
explicit xfrm); the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara,
    trun, prelim_chip, IN, PT, BLACK, DK, GRAY_3, FONT, edge, bd, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a rich cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell_rich() form — the only
#    change is legibility. ──


# ── Operating-Expenses methodology rows (the uniform middle family of the table).
#    Each is (row height IN, Component label, [Methodology bullet texts]). The
#    "Operating Expenses" header row (top section rule) and the final "Insurance"
#    row (no bottom rule) carry distinct edges and stay inline below. ──
_OPEX_ROWS = [
    (0.274, "Professional Services", ["6-7% of revenue"]),
    (0.274, "Fringe", ["Fringe rate of 37.6% applied to Compensation"]),
    (0.274, "Legal", ["1.5-2.2% of revenue (decreases over time)"]),
    (0.283, "IT & Software", ["$25K / head in R&D. 5% YoY increase"]),
    (0.283, "D&A", ["Construction depreciated over 40-yr. useful life", "Equipment depreciated over 15-yr. useful life"]),
    (0.283, "SBC", ["10% rate applied to Compensation – extra incentives for hiring. Added back in Cash Flows"]),
    (0.283, "Travel & Entertainment", ["$12K / head in R&D and G&A. $60K / head in S&M. 5% YoY increase"]),
    (0.283, "Equipment & Material Maintenance", ["~1-2% of cumulative Capex"]),
    (0.283, "Facilities", ["Utilities, Building Maintenance, Janitorial, Property Taxes, Other rates applied on a per sqft. Basis. Collectively $17 / sqft", "5% YoY increase (except Property Taxes - ~1%)", "Land Lease also included in cost at $7,500 / acre (rate kept constant YoY)"]),
    (0.395, "Marketing, PR, Events", ["1.5-2% of revenue (decreases over time)"]),
]


# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── title block (RAW-verbatim layout placeholders: body crumb + title) ──
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Text Placeholder 1\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"body\" sz=\"quarter\" idx=\"10\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr /><a:lstStyle /><a:p><a:r><a:rPr lang=\"en-US\" b=\"1\" /><a:t>BuildCo Financial Projections </a:t></a:r><a:r><a:rPr lang=\"en-US\" /><a:t>/ Assumptions &amp; Methodology</a:t></a:r></a:p></p:txBody></p:sp>")
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2001\" name=\"Title 2\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"title\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr vert=\"horz\" rIns=\"0\"><a:normAutofit /></a:bodyPr><a:lstStyle /><a:p><a:r><a:rPr lang=\"en-US\" /><a:t>Assumptions &amp; Methodology | Income Statement (2/2).</a:t></a:r></a:p></p:txBody></p:sp>")
    # ── assumptions table — Category / Component / Methodology ──
    # col_widths is the column-level geometry and each trow(h=...) is a minimum.
    # Repeated cell insets/anchors establish row/column padding and vertical
    # alignment; tpara align/mar_l/indent carries text alignment and bullets.
    # palette — text: 162029 dark navy (labels/components) · 000000 black (body bullets);
    #   rules: 162029 dark navy (section) · BFBFBF silver-gray (inner) horizontal · 79838F slate gray (column); cell fills: none.
    out.append(table(n(), "Table 3", IN(0.389), IN(1.146), IN(12.338), IN(5.395), col_widths=[IN(1.805), IN(3.216), IN(7.317)], rows=[
        trow([
            rcell([tpara([trun("Category:", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], anchor="b", B=edge(DK)),
            rcell([tpara([trun("Component", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], anchor="b", R=edge("79838F"), B=edge(DK)),
            rcell([tpara([trun("Methodology", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], anchor="b", L=edge("79838F"), B=edge(DK)),
        ], h=IN(0.5)),
        # "Operating Expenses" header row — opens the section with a dark top rule.
        trow([
            rcell([tpara([trun("Operating Expenses", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], T=edge(DK)),
            rcell([tpara([trun("Compensation", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(DK), B=edge(GRAY_3)),
            rcell([tpara([trun("Bucketed across R&D Engineers, Manufacturing OH, G&A, and S&M", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("5% YoY increase in rates", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(DK), B=edge(GRAY_3)),
        ], h=IN(0.426)),
        # Uniform OpEx component rows: empty Category cell, Component label, bulleted
        # Methodology — content lives in _OPEX_ROWS; mechanics (insets/edges) here.
        *[trow([
            rcell([tpara([], mar_l=0, indent=0, end_size=PT(1))]),
            rcell([tpara([trun(_comp, size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(GRAY_3), B=edge(GRAY_3)),
            rcell([tpara([trun(_t, size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450) for _t in _bullets], L=edge("79838F"), T=edge(GRAY_3), B=edge(GRAY_3)),
        ], h=IN(_h)) for _h, _comp, _bullets in _OPEX_ROWS],
        # Final "Insurance" row — closes the section (no bottom rule).
        trow([
            rcell([tpara([], mar_l=0, indent=0, end_size=PT(1))]),
            rcell([tpara([trun("Insurance", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(GRAY_3)),
            rcell([tpara([trun("Applied on a per sqft basis - $1.20 / sqft", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("5% YoY increase", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(GRAY_3)),
        ], h=IN(0.395)),
    ]))
    # ── chrome ──
    out.append(prelim_chip())
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 8", IN(0.495), IN(6.681), IN(12.367), IN(0.317), [paragraph([line_break(), run("Source: Internal Saronic data and estimates", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    return "".join(out)


def render() -> str:
    return slide(_body())
