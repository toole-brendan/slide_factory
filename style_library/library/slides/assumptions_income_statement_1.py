"""assumptions_income_statement_1 — Commercial Strategy Market Analysis deck (20260325), source slide 77.

EXHIBIT — "Assumptions & Methodology | Income Statement (1/2)": a single
three-column reference table documenting how BuildCo's projected income statement
is built, line by line. The columns are Category / Component / Methodology, and
the rows walk the income statement top-down: Revenue (POC) → Vessel Sale Price
(~40-44% gross margin on direct costs), then Direct Costs (POC) broken into
Equipment, Direct Labor, Direct Labor Fringe (37.6% rate), and Raw Materials
(Steel, ~$1,200/MT). A full-width blue banner below the table states the headline
rule — Revenue and Direct Costs are recognized on a Percentage-of-Completion
(POC) basis, allocated ratably over Build Time — with a worked $120M / 12-month
example. A Preliminary chip and a "Source: S&P Intelligence" line close it out.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • subtitle ph ...... RAW <p:sp> body placeholder ("BuildCo Financial Projections
                       / Assumptions & Methodology") — verbatim, no xfrm
  • title ph ......... RAW <p:sp> title placeholder ("Assumptions & Methodology |
                       Income Statement (1/2).") — verbatim, no xfrm
  • methodology table  the 3-column income-statement build (low-level table()/
                       trow()/tcell_rich(); merged Category cells via empty rows,
                       per-cell borders draw the rule lines)
  • POC banner ....... Rectangle 5 = full-width blue POC-recognition note + example
  • prelim chip ...... prelim_chip() (house builder)
  • source line ...... Rectangle 13 = "Source: S&P Intelligence"

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=2, table=1, chrome_builders=1, raw_verbatim=2,
dropped=1 (think-cell OLE frame).
Residue: two RAW-verbatim <p:sp> layout placeholders (title + subtitle) carry no
explicit xfrm and are kept byte-for-byte; the Note/Source line sits off the house
position, also kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara,
    trun, prelim_chip, IN, PT, BLACK, DK, BLUE_1, GRAY_3, FONT, edge, bd, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a rich cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell_rich() form — the only
#    change is legibility. ──


# ── table-cell layout commentary ──
# table(): col_widths are column-level sizing and trow(h=...) is a minimum row
# height. Each tcell/tcell_rich owns internal padding via l_ins/r_ins/t_ins/b_ins
# and vertical alignment via anchor=...; horizontal alignment and paragraph
# margins live in tcell(..., align=...) or tpara(..., align=..., mar_l=..., indent=...).

# ── text layout commentary ──
# text_box(): anchor controls vertical alignment inside the shape; paragraph(..., align=...)
# controls horizontal alignment. l_ins/t_ins/r_ins/b_ins are the internal padding;
# when omitted, the primitive defaults are intentional. paragraph mar_l/indent are
# used only when a text-bearing shape needs a hanging bullet/label margin.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── title + subtitle placeholders (RAW <p:sp>, no explicit xfrm — kept verbatim) ──
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Text Placeholder 1\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"body\" sz=\"quarter\" idx=\"10\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr /><a:lstStyle /><a:p><a:r><a:rPr lang=\"en-US\" b=\"1\" /><a:t>BuildCo Financial Projections </a:t></a:r><a:r><a:rPr lang=\"en-US\" /><a:t>/ Assumptions &amp; Methodology</a:t></a:r></a:p></p:txBody></p:sp>")
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2001\" name=\"Title 2\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"title\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr vert=\"horz\" rIns=\"0\"><a:normAutofit /></a:bodyPr><a:lstStyle /><a:p><a:r><a:rPr lang=\"en-US\" /><a:t>Assumptions &amp; Methodology | Income Statement (1/2).</a:t></a:r></a:p></p:txBody></p:sp>")
    # ── methodology table — income-statement build, line by line (low-level table()/trow()/tcell_rich(); merged Category cells + per-cell border rules) ──
    # palette — text: 162029 dark navy (labels/components) · 000000 black (body bullets);
    #   rules: 162029 dark navy (section) · BFBFBF silver-gray (inner) horizontal · 79838F slate gray (column); cell fills: none.
    out.append(table(n(), "Table 3", IN(0.472), IN(1.115), IN(12.338), IN(3.655), col_widths=[IN(1.805), IN(3.216), IN(7.318)], rows=[
        trow([
            rcell([tpara([trun("Category:", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], anchor="b", B=edge(DK)),
            rcell([tpara([trun("Component", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], anchor="b", R=edge("79838F"), B=edge(DK)),
            rcell([tpara([trun("Methodology – ", size=PT(12), bold=True, color=DK, font=FONT), trun("Revenue and Direct Costs recognized on POC basis", size=PT(12), italic=True, color=DK, font=FONT)], mar_l=0, indent=0)], anchor="b", L=edge("79838F"), B=edge(DK)),
        ], h=IN(0.5)),
        trow([
            rcell([tpara([trun("Revenue (POC)", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], T=edge(DK), B=edge(DK)),
            rcell([tpara([trun("Vessel Sale Price", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(DK), B=edge(DK)),
            rcell([tpara([trun("Container: ~40-44% Gross Margin applied to Direct Costs to set sale price", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(DK), B=edge(DK)),
        ], h=IN(0.409)),
        trow([
            rcell([tpara([trun("Direct Costs (POC)", size=PT(12), bold=True, color=DK, font=FONT)], mar_l=0, indent=0)], T=edge(DK)),
            rcell([tpara([trun("Equipment ", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(DK), B=edge(GRAY_3)),
            rcell([tpara([trun("Assumed to be ~65-75% of Total Equipment + Raw Materials costs", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("3% YoY increase in equipment costs", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("5% volume purchase discount applied on equipment", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(DK), B=edge(GRAY_3)),
        ], h=IN(0.682)),
        trow([
            rcell([tpara([], mar_l=0, indent=0)]),
            rcell([tpara([trun("Direct Labor", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(GRAY_3), B=edge(GRAY_3)),
            rcell([tpara([trun("Production tech labor rate * hours required to build vessel ", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("5% YoY increase in labor rate ’26-’30; 3% ’31+", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(GRAY_3), B=edge(GRAY_3)),
        ], h=IN(0.682)),
        trow([
            rcell([tpara([], mar_l=0, indent=0)]),
            rcell([tpara([trun("Direct Labor Fringe", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(GRAY_3), B=edge(GRAY_3)),
            rcell([tpara([trun("Fringe rate of 37.6% applied to Direct Labor", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(GRAY_3), B=edge(GRAY_3)),
        ], h=IN(0.409)),
        trow([
            rcell([tpara([], mar_l=0, indent=0)]),
            rcell([tpara([trun("Raw Materials (Steel)", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)], R=edge("79838F"), T=edge(GRAY_3)),
            rcell([tpara([trun("Steel portion of hull estimated from LWT in units of MT. Multiplied with $1,200 / MT rate", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("YoY price changes indexed to S&P steel price forecast", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([trun("5% volume purchase discount applied on raw materials", size=PT(12), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], L=edge("79838F"), T=edge(GRAY_3)),
        ], h=IN(0.955)),
    ]))
    # ── POC banner — full-width blue recognition note + worked $120M / 12-month example ──
    out.append(text_box(n(), "Rectangle 5", IN(0.472), IN(4.928), IN(12.362), IN(0.825), [paragraph([run("Revenue and Direct Costs are recognized on the Income Statement on a Percentage of Completion (POC) basis. Recognition is allocated ratably based on Build Time ", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("(e.g., Build Time = 12 Months, Price = $120M, Monthly Revenue = $10M)", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_1, line_color=BLACK, anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))   # E2E9EF pale blue
    # ── chrome — Preliminary chip + Source line (off the house position, kept verbatim) ──
    out.append(prelim_chip())
    out.append(text_box(n(), "Rectangle 13", IN(0.495), IN(6.681), IN(12.367), IN(0.317), [paragraph([line_break(), run("Source: S&P Intelligence", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    return "".join(out)


def render() -> str:
    return slide(_body())
