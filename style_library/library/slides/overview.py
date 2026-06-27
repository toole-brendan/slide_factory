"""overview — Commercial Strategy Market Analysis deck (20260325), source slide 2.

EXHIBIT — "Overview": a two-column text slide that frames the whole document. The
left column is a "Context" block stating the materials inform two key decisions —
where Saronic should play in the maritime value chain, and how Saronic will win —
plus the data sources the analysis leverages (S&P, Clarksons; EIA, FRED, GAO,
MARAD, USACE; Saronic experts; public filings and rate/tariff sheets). The right
column is an "Objectives of this document" block: a longer bulleted list of what
the deck delivers (define the strategy effort, synthesize archetype economics,
assess US-built vessel demand, compare build cost vs. Asian shipyards, project
BuildCo/OpCo financials, etc.), with the final three "(Ongoing effort)" items
italicized. A bottom-centre banner flags that answers are preliminary.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • title placeholder ... RAW-verbatim <p:sp> ("Overview"); the layout placeholder
                          carries no xfrm, so the converter kept the OOXML string
  • Context table ....... left table() — "Context" header + bulleted body cells via
                          tcell_rich()/tpara()/trun() (grey text, GRAY_1)
  • Objectives table .... right table() — "Objectives of this document" header +
                          bulleted body cells via tcell_rich()/tpara()/trun()
                          (black text; "(Ongoing effort)" runs italicized)
  • preliminary banner .. Rectangle 2 text_box() — bottom-centre PRELIM-fill note

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=1, table=2, raw_verbatim=1, dropped=1 (think-cell OLE
frame).
Residue: source layout '50% Block + Title' -> house slideLayout3 (was --layout
slideLayout4); the title placeholder is kept as a RAW-verbatim <p:sp> block (no
explicit xfrm on the layout placeholder).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun, IN, PT,
    BLACK, DK, PRELIM, GRAY_1, FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout3"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (borders,
#    spans). Renders identically to the raw tcell()/tcell_rich() form — the only
#    change is legibility. ──


def r(text, *, b=False, i=False, u=False, color=BLACK, size=PT(14)):
    """One styled run (Arial FONT; size defaults to this slide's dominant PT14)."""
    return trun(text, size=size, bold=b or None, italic=i or None, underline=u or None, color=color, font=FONT)


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
    # ── title placeholder ──
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Title 4\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"title\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr vert=\"horz\" /><a:lstStyle /><a:p><a:r><a:rPr lang=\"en-US\" /><a:t>Overview</a:t></a:r></a:p></p:txBody></p:sp>")
    # ── Context table (left column) ──
    # Table layout: the single col_width sets the column; trow(h=...) is the
    # row minimum. Cell insets/anchor govern internal padding and vertical
    # alignment; tpara mar_l/indent create the bullet margins.
    # palette — text: F2F2F2 off-white; rules: F2F2F2 off-white (header underline + body top); cell fills: none.
    out.append(table(n(), "Table 1", IN(0.498), IN(1.653), IN(5.7), IN(3.089), col_widths=[IN(5.7)], rows=[
        trow([cell("Context", size=PT(16), bold=True, color=GRAY_1, B=edge(GRAY_1))], h=IN(0.406)),
        trow([rcell([tpara([r("These materials provide foundational analysis to inform two key decisions:", color=GRAY_1)], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Determine where Saronic should play in the maritime value chain", color=GRAY_1)], bullet=True, bullet_char="-", mar_l=461963, indent=-174625),
            tpara([r("Understand how Saronic will win", color=GRAY_1)], bullet=True, bullet_char="-", mar_l=461963, indent=-174625),
            tpara([r("Analysis leverages data providers (S&P, Clarksons), US Government data and publications (EIA, FRED, GAO, MARAD, USACE), market participants (Saronic experts), public filings, published rate / tariff sheets, and other open-source research", color=GRAY_1)], bullet=True, mar_l=285750, indent=-285750)], T=edge(GRAY_1))], h=IN(0.406)),
    ]))
    # ── Objectives table (right column) ──
    # Same one-column layout contract: cell insets/anchor own internal
    # padding/vertical alignment; tpara alignment and mar_l/indent own the
    # horizontal text position and bullet margins.
    # palette — text: 000000 black; rules: 162029 dark navy (header underline + body top); cell fills: none.
    out.append(table(n(), "Table 9", IN(7.009), IN(1.653), IN(5.7), IN(4.522), col_widths=[IN(5.7)], rows=[
        trow([cell("Objectives of this document", size=PT(16), bold=True, color=BLACK, B=edge(DK))], h=IN(0.406)),
        trow([rcell([tpara([r("Define the commercial strategy effort, including objectives, key questions, focus areas, and timeline")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Introduce and synthesize current economics for relevant archetypes across the maritime value chain")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Assess US built vessel demand under different industrial policy scenarios")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Compare US build cost competitiveness vs. Asian shipyards ")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Compare US-flagged and foreign-flagged vessel costs")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Project BuildCo (Port Alpha) and OpCo financials")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("Delineate hypotheses for impact of automation on opex/fuel")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("(Ongoing effort) ", i=1), r("Determine attractive carrier entry points")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("(Ongoing effort)", i=1), r(" Assess attractiveness of alternative service models unlocked by automation")], bullet=True, mar_l=285750, indent=-285750),
            tpara([r("(Ongoing effort)", i=1), r(" Project ComboCo financials")], bullet=True, mar_l=285750, indent=-285750)], T=edge(DK))], h=IN(0.406)),
    ]))
    # ── preliminary banner (bottom-centre) — anchor/align center the text; default insets remain ──
    out.append(text_box(n(), "Rectangle 2", IN(7.009), IN(6.425), IN(5.7), IN(0.528), [paragraph([run("Answers shown are preliminary; fidelity and insights will increase with further analysis, additional data, and expert input", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=PRELIM, line_color="121415", line_width=19050, anchor="ctr"))   # FFFFCC pale yellow
    return "".join(out)


def render() -> str:
    return slide(_body())
