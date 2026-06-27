"""status_quo_outlook_offshore_1 — Commercial Strategy Market Analysis deck (20260325), source slide 45.

EXHIBIT — "Status Quo Outlook (Addressable Offshore 1/2)": argues that achieving
serial FSV production requires capturing 60%+ of the market plus a more favorable
upstream-capex outlook. The hero is a styled bar chart titled "Implied Retirements
vs. Orderbook of US-Built, US-Flagged Offshore FSV/PSV (# Hulls)" — two negative-
value series (retirements and orderbook) plotted across a 25-year axis (2026-2050),
with per-bar net-hull labels riding the bars and two wedge-callouts annotating it
("Bar total values indicate net hulls added (removed) each year" and a retirement-
backlog note). Right side carries a native table of average yearly retirement
replacements by archetype (Crew/Fast Supply ~4.2, PSV ~8.2 incl. Net of Orderbook)
plus a commentary cell, a Crew/Fast Supply vs. PSV legend, a "#" serial-production
key, and a CEDDEC takeaway banner ("Achieving PSV serial production requires
capturing 60%+ of the market…").

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • orderbook note ..... "Rectangle 702" left-margin "No orderbook orders for FSV/PSV"
  • styled chart ....... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the data
                         is _CHART0_DATA (two negative series), look is the template
  • _CATEGORY_TICK_LABELS ........ category-axis year labels 2026-2050 → loop
  • _DATA_LABELS .. net-hull data labels riding the bars (-32, -11, …) → loop
  • chart title ........ "Implied Retirements vs. Orderbook…" placeholder
  • chrome ............. breadcrumb() + title_placeholder() (house builders)
  • table .............. average retirement-replacements table (low-level table/trow/tcell)
  • callouts + legend .. two wedgeRectCallout speech bubbles, the two legend chips
                         (Crew/Fast Supply · PSV) + caption boxes, all standalone
                         and interleaved with the chrome below in paint order
  • footnote ........... Note/Source line (kept verbatim, off house position)
  • serial-prod key .... "#" markers + "Supports / Potentially supports serial production"
  • takeaway banner .... "Rectangle 776" CEDDEC 60%+ summary
  • scenario chip ...... prelim_chip() + "(1) Status Quo Scenario" (top-right)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=15, chart=1, table=1, chrome_builders=3,
clusters=2 (covering 43 shapes), frozen_fields=45, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara,
    trun, breadcrumb, title_placeholder, prelim_chip, graphic_frame, styled_chart, IN, PT,
    BLACK, WHITE, GRAY_1, FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide45_chart27.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide45_chart27.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [-2, -3, -8, -12, -9, -3, -8, -14, -5, -5, -5, -11, -9, -9, -14, -4, -8, -14, -27, -17, -9, -4, -4, -2, -1]},
        {"values": [-30, None, -3, -3, -7, -4, -7, -9, -7, -2, -3, -5, -4, -6, -6, -2, -2, -1, -1, None, None, None, None, None, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_YEAR_Y, _YEAR_W, _YEAR_H = IN(6.028), IN(0.167), IN(0.306)   # x-axis year-label box [shared x25]
_BARVAL_H = IN(0.167)     # bar value-label box height                                 [shared x18]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the twenty-five year ticks (2026-2050) along the category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x25 — category-axis year labels 2026-2050
    (0.83, "2026"),
    (1.102, "2027"),
    (1.375, "2028"),
    (1.648, "2029"),
    (1.92, "2030"),
    (2.193, "2031"),
    (2.465, "2032"),
    (2.738, "2033"),
    (3.01, "2034"),
    (3.283, "2035"),
    (3.556, "2036"),
    (3.828, "2037"),
    (4.101, "2038"),
    (4.375, "2039"),
    (4.648, "2040"),
    (4.92, "2041"),
    (5.193, "2042"),
    (5.465, "2043"),
    (5.738, "2044"),
    (6.01, "2045"),
    (6.283, "2046"),
    (6.556, "2047"),
    (6.828, "2048"),
    (7.101, "2049"),
    (7.373, "2050"),
]

# local_meaning: the net-hull value printed on each of the eighteen offshore bars.
_DATA_LABELS = [    # (x, y, cx, label) x18 — net-hull data labels riding the bars
    (0.795, 5.75, 0.238, "-32"),
    (1.34, 3.946, 0.238, "-11"),
    (1.613, 4.29, 0.238, "-15"),
    (1.885, 4.375, 0.238, "-16"),
    (2.196, 3.602, 0.161, "-7"),
    (2.431, 4.29, 0.238, "-15"),
    (2.703, 4.977, 0.238, "-23"),
    (2.976, 4.031, 0.238, "-12"),
    (3.559, 3.688, 0.161, "-8"),
    (3.793, 4.375, 0.238, "-16"),
    (4.066, 4.118, 0.238, "-13"),
    (4.34, 4.29, 0.238, "-15"),
    (3.286, 3.602, 0.161, "-7"),
    (4.924, 3.516, 0.161, "-6"),
    (5.158, 3.859, 0.238, "-10"),
    (5.431, 4.29, 0.238, "-15"),
    (5.703, 5.406, 0.238, "-28"),
    (4.613, 4.719, 0.238, "-20"),
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
    # ── orderbook note (left margin) ──
    out.append(text_box(n(), "Rectangle 702", IN(0.783), IN(2.104), IN(1.354), IN(4.276), [paragraph([run("No orderbook orders for ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("FSV / PSV", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), line_break(), line_break()], align="r", line_spacing=100000)], fill=GRAY_1, line_color="none"))   # F2F2F2 off-white
    # ── styled chart (data-over-template), bundled verbatim + .xlsb ("Edit Data" works) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.325), y=IN(1.866), cx=IN(7.359), cy=IN(4.361), rId="rId2"))
    # ── category-axis year labels (2026-2050) ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _YEAR_Y, _YEAR_W, _YEAR_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── bar value labels (net hulls added/removed per year) ──
    for _x, _y, _cx, _t in _DATA_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _BARVAL_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chart title ──
    out.append(text_box(n(), "Text Placeholder 25", IN(0.484), IN(1.752), IN(5.726), IN(0.167), [paragraph([run("Implied Retirements vs. Orderbook of US-Built, US-Flagged Offshore FSV/PSV (# Hulls)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("Status Quo Outlook (Addressable Offshore 1/2)", "Achieving serial production of FSVs requires capturing 60%+ of the market and more favorable upstream player capex outlook."))
    # ── average retirement-replacements table (low-level table()/trow()/tcell(); merges via grid_span/row_span) ──
    # Table layout: col_widths and trow(h=...) establish the comparison grid;
    # cell insets/anchor govern padding and vertical alignment, while tpara
    # align/mar_l/indent govern horizontal alignment and paragraph margins.
    # palette — text: 000000 black (labels/figures) · FFFFFF white (archetype cells) · 007770 teal (PSV figures);
    #   fills: 9DB1CF light blue · 4C6C9C blue; rules: 000000 black · 808080 gray.
    out.append(table(n(), "Table 769", IN(7.747), IN(1.685), IN(5.049), IN(3.833), col_widths=[IN(1.181), IN(1.723), IN(2.145)], rows=[
        trow([cell("Average retirement replacements required per year ’26-’50", bold=True, span=3, B=edge(BLACK))], h=IN(0)),
        trow([cell("Archetype", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)), cell("Total", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)), cell("Net of Orderbook Deliveries", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK))], h=IN(0)),
        trow([cell("Crew/Fast Supply", bold=True, color=WHITE, fill="9DB1CF", T=edge(BLACK), B=edge("808080", 6350)), cell("~4.2", size=PT(16), bold=True, align="ctr", T=edge(BLACK), B=edge("808080", 6350)), cell("~4.2", size=PT(16), bold=True, align="ctr", T=edge(BLACK), B=edge("808080", 6350))], h=IN(0.6)),
        trow([cell("PSV", bold=True, color=WHITE, fill="4C6C9C", T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([trun("~8.2", size=PT(16), bold=True, color="007770", font=FONT)], align="ctr", mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([trun("~8.2", size=PT(16), bold=True, color="007770", font=FONT)], align="ctr", mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.6)),
        trow([cell("Commentary", bold=True, T=edge("808080", 6350)), rcell([tpara([trun("1-for-1 retirement replacements potentially challenged by O&G sector maintaining capital discipline that drives retirement deferrals ", size=PT(10), color=BLACK, font=FONT), trun("(potentially mitigated if crude prices remain high due to Persian Gulf disruptions)", size=PT(10), italic=True, color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([], bullet=True, mar_l=171450, indent=-171450), tpara([trun("Only Offshore O&G vessel types with orders are Multipurpose Support Vessels (2x on order), providing evidence of constrained upstream capex environment", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([], bullet=True, mar_l=171450, indent=-171450), tpara([trun("Other Offshore O&G vessel types have smaller fleet counts than PSV and Crew/Fast Supply (1-66 vs. 206 and 105, respectively), likely precluding serial production", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], span=2, T=edge("808080", 6350))], h=IN(0.6)),
    ]))
    # ── chart callout + legend (net-hulls note, Crew/Fast Supply vs. PSV chips + captions) ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 645", IN(5.087), IN(1.965), IN(2.488), IN(0.425), [paragraph([run("Bar total values indicate net hulls added (removed) each year", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val -19106", "adj2": "val -3267"}, anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "Rectangle 661", IN(5.194), IN(2.451), IN(0.196), IN(0.146), [paragraph([], align="ctr", line_spacing=100000)], fill="9DB1CF", line_color="none", anchor="ctr"))   # 9DB1CF light blue
    out.append(text_box(n(), "Rectangle 662", IN(5.194), IN(2.674), IN(0.196), IN(0.146), [paragraph([], align="ctr", line_spacing=100000)], fill="4C6C9C", line_color="none", anchor="ctr"))   # 4C6C9C blue
    out.append(text_box(n(), "Text Placeholder 25", IN(5.446), IN(2.446), IN(1.092), IN(0.167), [paragraph([run("Crew/Fast Supply", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(5.446), IN(2.668), IN(0.276), IN(0.167), [paragraph([run("PSV", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── footnote — kept verbatim (sits off the house Source position) ──
    out.append(text_box(n(), "Rectangle 701", IN(0.495), IN(6.692), IN(12.367), IN(0.306), [paragraph([run("Note: Service life assumptions – 30 years for PSVs and 25 years for Crew/FSVs ", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: Clarksons (US fleet size and GT data); ", size=PT(8), color=BLACK, font=FONT), run("McKinsey article on O&G sector operating model", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    # ── retirement-backlog callout (over the chart) ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 771", IN(1.271), IN(5.231), IN(2.012), IN(0.561), [paragraph([run("Retirement backlog suggests owners likely to keep vessels in service despite age", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="121415", prst="wedgeRectCallout", geom_adj={"adj1": "val -60475", "adj2": "val 8630"}, anchor="ctr"))   # FFFFFF white
    # ── serial-production key ("#" markers: black = potentially supports, teal = supports) ──
    out.append(text_box(n(), "Rectangle 772", IN(10.438), IN(1.429), IN(0.301), IN(0.26), [paragraph([run("#", size=PT(16), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "TextBox 773", IN(10.694), IN(1.442), IN(2.101), IN(0.234), [paragraph([run("Potentially supports serial production", size=PT(10), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "Rectangle 774", IN(10.438), IN(1.187), IN(0.301), IN(0.26), [paragraph([run("#", size=PT(16), bold=True, color="007770", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 007770 teal
    out.append(text_box(n(), "TextBox 775", IN(10.694), IN(1.2), IN(2.101), IN(0.234), [paragraph([run("Supports serial production", size=PT(10), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── takeaway banner (60%+ market-capture summary) ──
    out.append(text_box(n(), "Rectangle 776", IN(7.79), IN(5.652), IN(5.094), IN(0.68), [paragraph([run("Achieving PSV serial production requires capturing 60%+ of the market; potential to serve international demand as US remains competitive in OSVs", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color="none", anchor="ctr"))   # CEDDEC pale blue
    # ── scenario chip (top-right) ──
    out.append(prelim_chip())
    out.append(text_box(n(), "Rectangle 2", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))   # CEDDEC pale blue
    return "".join(out)


def render() -> str:
    return slide(_body())
