"""ships_act_captive_demand — Commercial Strategy market-analysis deck (20260325), source slide 60.

EXHIBIT — "SHIPS Act Captive Demand": the Maritime Security Trust Fund (MSTF) can
support ~100 more vessels (~200 total) than the SHIPS Act's legally-mandated
demand. Left: a styled stacked-bar chart comparing the MSTF-supported Strategic
Commercial Fleet vs. legally-mandated demand by vessel type (Container, LNG,
Crude / Product Tanker, Bulk, Ro-Ro, Other). Right: a mandate table mapping each
SHIPS Act provision (bill section) to its vessel type, cargo-% ramp, and US-built /
US-flagged requirement. A "(2) SHIPS Act Scenario" tag and an Opex/D&A-differential
caveat box annotate.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............. title_placeholder() + breadcrumb() + prelim_chip()
  • styled chart ....... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                         data (7 vessel-type series × 2 bars) is _CHART0_DATA
  • table ............. SHIPS Act provision → mandate table (low-level table())
  • _DATA_LABELS ....... small "1" data labels on thin bar segments
  • _LEGEND_KEYS ....... vessel-type colour chips; _LEGEND_LABELS = captions
  • connectors ........ dashed leader lines from labels to bar segments
  • pattern swatch .... the ltDnDiag legend swatch via text_box(pattern_fill=) —
                        a hatch fill now expressible without a per-module helper
  • annotations ....... scenario tag, caveat box, "Port Alpha production modeled"

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study (names and
comments made semantic, body grouped into sections) and retrofitted to the
text_box(pattern_fill=) primitive; paint order is unchanged and the render is
verified equivalent (the swatch position differs only by inch-rounding).

Converter stats: text_box=13, connector=5, chart=1, table=1, chrome_builders=3,
clusters=3 (covering 16 shapes), raw_verbatim=0 (the ltDnDiag swatch is now a
text_box(pattern_fill=)), dropped=1 (think-cell OLE frame), frozen_fields=14.
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, tcell_rich,
    tpara, trun, tbreak, breadcrumb, title_placeholder, prelim_chip, graphic_frame,
    styled_chart, IN, PT, BLACK, WHITE, BREADCRUMB, GRAY_2, FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide60_chart43.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide60_chart43.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [124, 46]},
        {"values": [46, 41]},
        {"values": [18, 15]},
        {"values": [9, 1]},
        {"values": [1, 1]},
        {"values": [1, None]},
        {"values": [2, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_MARK_W, _MARK_H = IN(0.115), IN(0.167)        # on-bar value-marker size
_SWATCH_W, _SWATCH_H = IN(0.196), IN(0.146)    # legend colour-chip size
_VLBL_X, _VLBL_H = IN(4.139), IN(0.167)        # vessel-label column x / height
_TXT_H = IN(0.167)        # chart-title / axis-label height        [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the small '1' data labels on the thin bar segments.
_DATA_LABELS = [    # (x, y, fill) x3 — small "1" data labels on thin bar segments
    (2.309, 2.21, "4C6C9C"),   # 4C6C9C blue
    (4.583, 3.997, BLACK),   # 000000 black
    (3.951, 4.016, "4C6C9C"),   # 4C6C9C blue
]

# local_meaning: the six vessel-type colour chips.
_LEGEND_KEYS = [    # (x, y, fill) x6 — vessel-type colour chips
    (3.887, 2.149, "969696"),   # 969696 gray
    (3.887, 2.372, BLACK),   # 000000 black
    (3.887, 2.594, "4C6C9C"),   # 4C6C9C blue
    (3.887, 2.816, "1D4D68"),   # 1D4D68 teal-blue
    (3.887, 3.038, "C0C0C0"),   # C0C0C0 silver
    (3.887, 3.26, "007770"),   # 007770 teal
]

# local_meaning: the seven vessel-type legend captions.
_LEGEND_LABELS = [    # (y, cx, label) x7 — vessel-type legend captions
    (1.922, 0.345, "Other"),
    (2.144, 0.401, "Ro-Ro"),
    (2.366, 0.269, "Bulk"),
    (2.589, 0.944, "Product Tanker"),
    (2.811, 0.845, "Crude Tanker"),
    (3.033, 0.285, "LNG"),
    (3.255, 0.599, "Container"),
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
    # ── chrome (title precedes the Note line + breadcrumb in paint order) ──
    out.append(title_placeholder("SHIPS Act Captive Demand", "MSTF can support ~100 more vessels than legally mandated demand for SHIPS Act."))
    out.append(text_box(n(), "Rectangle 4", IN(0.495), IN(6.675), IN(12.367), IN(0.322), [paragraph([run("Note: Captive demand considers current cargo volumes, growth rates, and annual vessel capacity (driven by number of trips / year, cargo capacity, and utilization)", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: S&P Panjiva; Clarksons; ", size=PT(8), color=BLACK, font=FONT), run("SHIPS Act text", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA AEO LNG Export Table", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA AEO Crude Export Table", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA Crude Tanker Descriptions", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("GAO Report on Government Preference Cargo", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    # Table layout: col_widths fixes the mandate columns and trow(h=...) their
    # minimum heights; each cell controls insets/anchor while tpara align,
    # mar_l, and indent control horizontal alignment and paragraph margins.
    # palette - text: 000000 black (headers/rates) · FFFFFF white (provision labels) · 007770 teal (Yes) · C00000 dark red (No);
    #   fills: D9D9D9 light gray (title banner) · FFFFFF white (body) · 1D4D68 teal-blue / C0C0C0 silver / 007770 teal (provisions);
    #   rules: 000000 black (header) · 808080 gray (inner).
    out.append(table(n(), "Table 10", IN(5.703), IN(1.483), IN(7.089), IN(4.007), col_widths=[IN(2.808), IN(1.799), IN(1.241), IN(1.241)], rows=[
        # ── title banner (spans all 4 columns) ──
        trow([cell("Legally mandated demand from SHIPS Act Provisions", size=PT(10), bold=True, color=BLACK, align="ctr", fill=GRAY_2, span=4, anchor="b")], h=IN(0)),
        # ── column headers (black bottom rule) ──
        trow([
            rcell([tpara([trun("Provision ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("(Bill Section)", size=PT(10), italic=True, color=BLACK, font=FONT), tbreak(), trun("Vessel Type Impacted", size=PT(10), color=BLACK, font=FONT)])], anchor="b", B=edge(BLACK)),
            rcell([tpara([trun("% of Cargo", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("(Start – ramp end)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], anchor="b", B=edge(BLACK)),
            cell("US-Built", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", B=edge(BLACK)),
            cell("US-Flagged", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", B=edge(BLACK)),
        ], h=IN(0)),
        # ── Crude Exports (SEC. 420) ──
        trow([
            rcell([tpara([trun("Crude Exports from the US", size=PT(10), bold=True, color=WHITE, font=FONT)]), tpara([trun("SEC. 420", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Crude Tankers", size=PT(10), color=WHITE, font=FONT)])], fill="1D4D68", T=edge(BLACK), B=edge("808080", 6350)),
            rcell([tpara([trun("3% to 10%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2027-2040", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, T=edge(BLACK), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge(BLACK), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge(BLACK), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── LNG Exports (SEC. 420) ──
        trow([
            rcell([tpara([trun("LNG Exports from the US", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("SEC. 420", size=PT(10), italic=True, color=BLACK, font=FONT), tbreak(), trun("LNG Ships", size=PT(10), color=BLACK, font=FONT)])], fill="C0C0C0", T=edge("808080", 6350), B=edge("808080", 6350)),
            rcell([tpara([trun("2% to 15%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2027-2047", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── China Imports (SEC. 415) ──
        trow([
            rcell([tpara([trun("China Imports to the US", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 415", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships", size=PT(10), color=WHITE, font=FONT)])], fill="007770", T=edge("808080", 6350), B=edge("808080", 6350)),
            rcell([tpara([trun("1% to 10%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2031-2040", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── US Government Cargo Preference (SEC. 411); %-of-cargo cell spans 2 rows ──
        trow([
            rcell([tpara([trun("US Government Cargo Preference", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 411", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships & Bulk", size=PT(10), color=WHITE, font=FONT)])], fill="007770", T=edge("808080", 6350), B=edge("808080", 6350)),
            rcell([tpara([trun("50% to 100%", size=PT(10), bold=True, color=BLACK, font=FONT), trun(" ", size=PT(10), color=BLACK, font=FONT), tbreak(), trun("180 days after bill passage", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, rowspan=2, T=edge("808080", 6350)),
            cell("No", size=PT(12), bold=True, color="C00000", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── USDA Program Exports (SEC. 418); col 1 is covered by the row-span above ──
        trow([
            rcell([tpara([trun("USDA Program Exports", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 418", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships", size=PT(10), color=WHITE, font=FONT)])], fill="007770", T=edge("808080", 6350)),
            cell("No", size=PT(12), bold=True, color="C00000", align="ctr", fill=WHITE, T=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350)),
        ], h=IN(0.661)),
    ]))
    # ── styled chart (data-over-template) → CHARTS[0] ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.429), y=IN(1.62), cx=IN(5.123), cy=IN(4.674), rId="rId2"))
    out.append(connector(n(), "Straight Connector 74", IN(2.599), IN(2.274), IN(0.101), IN(0.069), color=BREADCRUMB, width=6350, dashed=True, arrow=True, flip_h=True, flip_v=True))   # 44505C slate gray
    out.append(connector(n(), "Straight Connector 75", IN(2.599), IN(2.177), IN(0.101), IN(0.069), color=BREADCRUMB, width=6350, dashed=True, arrow=True, flip_h=True))   # 44505C slate gray
    out.append(text_box(n(), "Text Placeholder 25", IN(0.542), IN(1.505), IN(4.384), _TXT_H, [paragraph([run("SCF Supported by MSTF vs. Legally Mandated Demand (# vessels)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── on-bar value markers ──
    for _x, _y, _fill in _DATA_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), _MARK_W, _MARK_H, [paragraph([run("1", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.215), IN(6.094), IN(1.667), IN(0.333), [paragraph([run("Strategic Commercial Fleet (supported by MSTF)", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(3.493), IN(6.094), IN(1.663), _TXT_H, [paragraph([run("Legally Mandated Demand", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(1.915), IN(2.033), IN(0.267), _TXT_H, [paragraph([run("201", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(4.191), IN(3.83), IN(0.267), _TXT_H, [paragraph([run("104", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # pattern-fill legend swatch — text_box(pattern_fill=) for the ltDnDiag hatch
    out.append(text_box(n(), "Rectangle 109", IN(3.887), IN(1.927), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="none", pattern_fill={"prst": "ltDnDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"}, anchor="ctr"))
    # ── legend: vessel-type colour chips + names ──
    for _x, _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", _VLBL_X, IN(_y), IN(_cx), _VLBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Rectangle 329", IN(5.703), IN(5.56), IN(7.089), IN(0.867), [paragraph([run("Reaching ~200 vessels assumes owners accept Opex and D&A differential of operating US-built and flagged vessels vs. foreign-built and flagged", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))   # CEDDEC pale blue
    out.append(prelim_chip())
    out.append(text_box(n(), "Rectangle 336", IN(8.069), IN(0.173), IN(2.977), IN(0.218), [paragraph([run("(2) SHIPS Act Scenario", size=PT(12), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=BLACK, anchor="ctr"))   # 447BB2 blue
    out.append(connector(n(), "Straight Connector 351", IN(4.958), IN(2.188), IN(0.745), IN(1.927), color="808080", width=6350, dashed=True, flip_v=True))   # 808080 gray
    out.append(connector(n(), "Straight Connector 355", IN(4.958), IN(2.854), IN(0.745), IN(1.536), color="808080", width=6350, dashed=True, flip_v=True))   # 808080 gray
    out.append(connector(n(), "Straight Connector 358", IN(4.958), IN(3.487), IN(0.745), IN(1.683), color="808080", width=6350, dashed=True, flip_v=True))   # 808080 gray
    out.append(text_box(n(), "Rectangle 53", IN(10.635), IN(1.191), IN(0.1), IN(0.234), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="ctr"))   # FB6B3C orange outline
    out.append(text_box(n(), "TextBox 54", IN(10.691), IN(1.191), IN(2.101), IN(0.234), [paragraph([run("Port Alpha production modeled", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "Rectangle 55", IN(3.835), IN(2.569), IN(1.3), IN(0.426), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="b"))   # FB6B3C orange outline
    out.append(text_box(n(), "Rectangle 56", IN(3.835), IN(3.236), IN(1.3), IN(0.207), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="b"))   # FB6B3C orange outline
    return "".join(out)


def render() -> str:
    return slide(_body())
