"""comparison_vs_ddgs — Market sizing Golden Dome deck (20260116), source slide 8.

EXHIBIT — "Comparison vs. DDGs": frames Golden Dome Marauder (MR) procurement
cost as roughly equal to four Arleigh Burke-class destroyers while delivering 10x+
the interceptor capacity. A styled bar chart (left) stacks procurement cost ($M)
for 4x DDGs (~$10,800M across four destroyer bars) against the GD Marauders (two
MR tranches, #1-#120 co-located + #121-#240 separate platforms, ~$10,080M); white
"DDG #1/#2/#4" labels ride the destroyer bars and the totals sit above each stack.
Two supporting tables sit to the right: a one-row "Cost comparison" title bar, and
a "Capability comparison – Strike munitions capacity" table contrasting 4x DDGs
(up to 384 SM-3 / SM-6, total VLS capacity) vs. 240x Marauders (3,840 SM-3 / SM-6,
10x+ Arleigh Burke capacity). Two service-mark logos and a Source/Note line close
it out.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder() (house builders)
  • logos ............. two picture() service marks, top-right (IMAGES rId3/rId4)
  • styled chart ...... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                        data is _CHART0_DATA (DDG + Marauder procurement $M), the
                        look is the source chart template
  • chart labels ...... "Procurement cost ($M)" axis title; _DATA_LABELS loop =
                        white DDG #1/#2/#4 labels on the bars; standalone DDG #4,
                        Arleigh Burke / Golden Dome Marauders axis captions, the
                        10,800 / 10,080 totals, and the MR tranche annotations
  • cost table ........ Table 435 = one-row "Cost comparison" title bar
  • capability table .. Table 578 = "Strike munitions capacity" comparison (4x DDG
                        vs. 240x Marauders), low-level table()/trow()/tcell()
  • sources_line ...... house Source/Note footnote

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=8, chart=1, table=2, picture=2, chrome_builders=3,
clusters=1 (covering 3 shapes), frozen_fields=4, dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, picture, line_break, table, trow, tcell, tcell_rich,
    tpara, trun, tbreak, breadcrumb, title_placeholder, sources_line, graphic_frame,
    styled_chart, IN, PT, BLACK, WHITE, DK, GRAY_1, FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide8_chart1.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide8_chart1.xlsb").read_bytes()


def mt(align="ctr"):
    """An empty (text-free) cell paragraph — spacing/border only, no runs.
    Kept local (not in table_kit): unlike the matrix mt() elsewhere, this one does
    not pin <a:endParaRPr> to 1pt, so end_size varies by slide."""
    return tpara([], align=align, mar_l=0, indent=0)

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [2700, 5040]},
        {"values": [2700, 5040]},
        {"values": [2700, None]},
        {"values": [2700, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]
IMAGES = [
    {"rId": "rId3", "file": "image7_3071a231.jpeg"},
    {"rId": "rId4", "file": "image8_ffd85751.png"},
]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_DDG_LBL_X, _DDG_LBL_W, _DDG_LBL_H = IN(2.148), IN(0.538), IN(0.167)  # DDG bar-label box
_LABEL_ROW_H = IN(0.167)   # single-line chart-label row height        [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the three white data labels riding the destroyer (DDG) bars.
_DATA_LABELS = [    # (y, label) x3 — white data labels riding the destroyer bars
    (5.694, "DDG #1"),
    (4.88, "DDG #2"),
    (4.068, "DDG #4"),
]

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
    # ── chrome ──
    out.append(breadcrumb("Golden Dome Requirements", "Platform Quantities"))
    out.append(title_placeholder("Comparison vs. DDGs", "Total GD MR procurement cost is roughly the same as four Arleigh Burke-class destroyers while delivering 10x+ the interceptor capacity"))
    # ── logos (top-right) ──
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(11.431), IN(0.048), IN(0.922), IN(0.922)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 8", "rId4", IN(12.372), IN(0.048), IN(0.922), IN(0.922)))
    # ── styled chart (data-over-template) + its labels ──
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.418), y=IN(2.7), cx=IN(6.068), cy=IN(3.656), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.531), IN(2.509), IN(1.502), _LABEL_ROW_H, [paragraph([run("P", size=PT(10), bold=True, color=BLACK, font=FONT), run("rocurement cost ($M)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # white DDG #1/#2/#4 labels riding the destroyer bars
    for _y, _t in _DATA_LABELS:
        out.append(text_box(n(), "Label", _DDG_LBL_X, IN(_y), _DDG_LBL_W, _DDG_LBL_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    out.append(text_box(n(), "Text Placeholder 25", IN(2.148), IN(3.253), IN(0.538), _LABEL_ROW_H, [paragraph([run("DDG #4", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(1.446), IN(6.233), IN(1.943), _LABEL_ROW_H, [paragraph([run("Arleigh Burke-class destroyers", size=PT(10), color=BLACK, font=FONT), run("1", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(4.432), IN(5.175), IN(1.276), IN(0.5), [paragraph([run("MR #1-#120", size=PT(10), color=WHITE, font=FONT), line_break(), run("(Co-located sensors", size=PT(10), color=WHITE, font=FONT), line_break(), run("and interceptors)", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    out.append(text_box(n(), "Text Placeholder 25", IN(4.26), IN(6.233), IN(1.618), _LABEL_ROW_H, [paragraph([run("Golden Dome Marauders", size=PT(10), color=BLACK, font=FONT), run("2", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(2.188), IN(2.736), IN(0.458), _LABEL_ROW_H, [paragraph([run("10,800", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(4.84), IN(2.953), IN(0.458), _LABEL_ROW_H, [paragraph([run("10,080", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(4.42), IN(3.74), IN(1.299), IN(0.333), [paragraph([run("MR #121-#240 ", size=PT(10), color=BLACK, font=FONT), line_break(), run("(Separate platforms)", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── cost-comparison title bar ──
    # Column width and trow(h=...) set the outer cell; l/r/t/b insets and
    # anchor set internal padding/vertical alignment, while align/margins
    # on tcell/tpara place the text horizontally.
    # palette - text: 000000 black (title); rule: 162029 dark navy (bottom); cell fills: none.
    out.append(table(n(), "Table 435", IN(0.495), IN(1.694), IN(5.901), IN(0.333), col_widths=[IN(5.901)], rows=[
        trow([rcell([tpara([trun("Cost comparison – ", size=PT(12), bold=True, color=BLACK, font=FONT), trun("Arleigh Burke", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT), trun("-class destroyers ", size=PT(12), bold=True, color=BLACK, font=FONT), trun("vs. GD Marauders", size=PT(12), bold=True, color=BLACK, font=FONT)])], anchor="b", **PAD, B=edge(DK))], h=IN(0)),
    ]))
    # ── capability-comparison table — strike munitions capacity (low-level table()/trow()/tcell(); merges via grid_span/row_span) ──
    # palette - text: 000000 black (title/figures) · FFFFFF white (column heads);
    #   fills: 808080 gray (DDG head) · 4C6C9C blue (Marauder head) · F2F2F2 off-white (384 cell) · CEDDEC pale blue (3,840 cell);
    #   rules: 162029 dark navy (title/top).
    out.append(table(n(), "Table 578", IN(6.962), IN(1.694), IN(6), IN(4.5), col_widths=[IN(2.789), IN(0.423), IN(2.789)], rows=[
        # ── title bar (spans all 3 cols) ──
        trow([cell("Capability comparison – Strike munitions capacity", size=PT(12), bold=True, color=BLACK, span=3, anchor="b", **PAD, B=edge(DK))], h=IN(0.338)),
        # ── thin rule row (PT1 spacers carrying the top rule) ──
        trow([
            cell("", size=PT(1), align="ctr", anchor="b", **PAD, T=edge(DK)),
            cell("", size=PT(1), align="ctr", anchor="b", **PAD, T=edge(DK)),
            cell("", size=PT(1), align="ctr", anchor="b", **PAD, T=edge(DK)),
        ], h=IN(0.22)),
        # ── column heads: 4x DDGs | (gap) | 240x Marauders ──
        trow([
            rcell([tpara([trun("4x ", size=PT(12), bold=True, color=WHITE, font=FONT), trun("Arleigh Burke-", size=PT(12), bold=True, italic=True, color=WHITE, font=FONT), trun("class", size=PT(12), bold=True, color=WHITE, font=FONT), trun(" ", size=PT(12), bold=True, italic=True, color=WHITE, font=FONT), trun("destroyers", size=PT(12), bold=True, color=WHITE, font=FONT), trun("1", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill="808080", **PAD),
            cell("", size=PT(12), align="ctr", **PAD),
            rcell([tpara([trun("240x Marauders", size=PT(12), bold=True, color=WHITE, font=FONT), trun("3", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill="4C6C9C", **PAD),
        ], h=IN(0.54)),
        # ── spacer ──
        trow([rcell([mt()], **PAD), rcell([mt()], **PAD), rcell([mt()], **PAD)], h=IN(0.192)),
        # ── capacity figures: 384 (GRAY_1) | (gap) | 3,840 (CEDDEC); both span 5 rows ──
        trow([
            rcell([tpara([trun("Up to 384", size=PT(20), bold=True, color=BLACK, font=FONT), tbreak(), trun("SM-3 / SM-6", size=PT(12), color=BLACK, font=FONT), tbreak(), tbreak(), trun("(384 represents total VLS capacity; actual interceptor quantity dependent on mission) ", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], fill=GRAY_1, rowspan=5, **PAD),
            rcell([mt()], **PAD),
            rcell([tpara([trun("3,840 ", size=PT(20), bold=True, color=BLACK, font=FONT), tbreak(), trun("SM-3 / SM-6", size=PT(12), color=BLACK, font=FONT), tbreak(), tbreak(), trun("10x+ ", size=PT(12), color=BLACK, font=FONT), trun("Arleigh Burke", size=PT(12), italic=True, color=BLACK, font=FONT), trun(" capacity", size=PT(12), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], fill="CEDDEC", rowspan=5, **PAD),
        ], h=IN(0.732)),
        # ── middle "Vs." stack (cols 0 & 2 covered by the row-spans above) ──
        trow([rcell([mt()], **PAD)], h=IN(0.366)),
        trow([rcell([tpara([trun("Vs.", size=PT(12), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD)], h=IN(0.732)),
        trow([rcell([mt()], **PAD)], h=IN(0.366)),
        trow([rcell([mt()], **PAD)], h=IN(1.013)),
    ]))
    # ── house Source/Note footnote ──
    out.append(sources_line("Note: (1) Flight III destroyers; Assumes $2.7B unit price based on OBBBA ($5.4B for 2x), CRS estimate ($2.7B apiece), and FY26 Shipbuilding and Conversion, Navy Justification Book Exhibit P-5c, Ship Cost Analysis ($5.5B for 2x in FY24, $7.86B for 3x in FY25); (2) Marauder priced at $42M / unit excluding launcher costs; (3) 4x SM-3 or SM-6 per MK-70, with 4x MK-70 per Marauder for total of 16x SM-3 or SM-6 per Marauder | Source: Congressional Research Service; OBBBA text; FY26 Budget Estimate; Lockheed Martin MK 70 Product Card; Lockheed Martin MK 41 Product Card"))
    return "".join(out)


def render() -> str:
    return slide(_body())
