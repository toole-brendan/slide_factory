"""status_quo_outlook_oceangoing — Commercial Strategy Market Analysis deck (20260325), source slide 44.

EXHIBIT — "Status Quo Outlook (Oceangoing Commercial)": replacing retirements
alone is unlikely to support serial production. A styled stacked-column chart
(left) plots Implied Retirements vs. Orderbook of US-Built, US-Flagged Oceangoing
Commercial Vessels (# hulls) across 2026–2050, with the four vessel archetypes
(Container / General / RORO / Tanker) keyed twice in a paired legend — once for
Retirements¹ (blue shades, below the axis) and once for Orderbook² (greys, above).
Bar-total labels (e.g. -9, -7, -5) flag the net hulls added (removed) each year,
and a wedge callout explains them. A native table (right) gives average retirement
replacements required per year ’26-’50 by archetype — Total and Net of Orderbook
Deliveries (~0.6/~0.4 Container … ~1.7/~1.2 Tanker) — over a banner concluding
~0.2-1.2 vessels/yr is insufficient for serial production (5+ hulls/yr needed).

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • orderbook-window box .. "Rectangle 30" left rail ("Years with orderbook data")
  • styled chart .......... graphic_frame(rId2) → CHARTS[0] = styled_chart(...);
                            the data is _CHART0_DATA (4 archetype series × 25 yrs),
                            the look is the source chart template
  • _CATEGORY_TICK_LABELS  category-axis year labels 2026–2050
  • chart title ........... "Implied Retirements vs. Orderbook …" placeholder
  • _DATA_LABELS ......... net-hull data labels riding the bars
  • per-bar "4" labels .... two standalone "4" data labels that interleave here
  • chrome ................ breadcrumb() + title_placeholder() (+ prelim_chip later)
  • table ................. retirement-replacements-per-year table (low-level
                            table()/trow()/tcell(); merges via grid_span)
  • legend ................ two outline frames (Retirements / Orderbook) +
                            _LEGEND_KEYS + _LEGEND_LABELS
                            + the bar-total wedge callout, all interleaved
  • takeaway banner ....... "~0.2-1.2 vessels per year …" insufficient-for-serial box
  • footnote .............. Note/Source line (kept verbatim, off house position)
  • serial-production key .. red "#" / green "#" legend ("Does not / Supports …")
  • Hanwha callout ........ wedge "12x purchased by Hanwha Shipping"
  • scenario chip ......... "(1) Status Quo Scenario" (top-right)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=17, chart=1, table=1, chrome_builders=3, clusters=4
(covering 50 shapes), frozen_fields=44, dropped=1 (think-cell OLE frame).
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
_CHART0_TPL = (_SRC / "slide44_chart26.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide44_chart26.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [1, 2, 2, 5, 5, -1, -1, -3, -2, None, -1, -1, -1, -2, -2, -2, -3, -2, -6, -5, -1, -2, -1, -1, -4]},
        {"values": [-1, -3, None, -1, -1, None, -1, None, None, None, None, None, -1, None, -1, None, None, -2, -1, -1, -1, None, None, None, None]},
        {"values": [-5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, -1, None, -1, None, None, None, None, None]},
        {"values": [-4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.026), IN(0.167), IN(0.306)   # x-axis year-label row [x25]
_BARVAL_W, _BARVAL_H = IN(0.161), IN(0.167)                   # bar-total value-label box [x9]
_SWATCH_W, _SWATCH_H = IN(0.196), IN(0.146)                   # legend colour-chip [x8]
_LEGEND_LBL_H = IN(0.167)                                     # legend caption height [x8]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the twenty-five year ticks (2026-2050) along the category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x25 — category-axis year labels 2026–2050
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
    (6.01, "2045"),
    (6.283, "2046"),
    (6.556, "2047"),
    (6.828, "2048"),
    (7.101, "2049"),
    (7.373, "2050"),
    (5.738, "2044"),
]

# local_meaning: the net-hull total printed on each of the nine bars.
_DATA_LABELS = [    # (x, y, label) x9 — net-hull data labels riding the bars
    (0.833, 5.812, "-9"),
    (1.106, 4.528, "-1"),
    (2.469, 4.344, "-2"),
    (4.104, 4.344, "-2"),
    (4.651, 4.528, "-3"),
    (5.469, 4.894, "-5"),
    (5.741, 5.262, "-7"),
    (6.014, 5.262, "-7"),
    (6.286, 4.344, "-2"),
]

# local_meaning: the paired legend chips: rows 1-4 are the Retirements ramp (blue shades), rows
#   5-8 the Orderbook ramp (greys->black), one per vessel archetype.
_LEGEND_KEYS = [    # (x, y, fill) x8 — Retirements legend (rows 1-4, blue shades) + Orderbook legend (rows 5-8, greys→black)
    (5.33, 2.618, "9DB1CF"),   # 9DB1CF light blue
    (5.33, 2.84, "6F8DB9"),   # 6F8DB9 blue
    (5.33, 3.062, "4C6C9C"),   # 4C6C9C blue
    (5.33, 3.285, "364D6E"),   # 364D6E dark blue
    (6.292, 2.618, "C0C0C0"),   # C0C0C0 silver
    (6.292, 2.84, "969696"),   # 969696 gray
    (6.292, 3.062, "808080"),   # 808080 gray
    (6.292, 3.285, BLACK),   # 000000 black
]

# local_meaning: the eight archetype captions: Retirements legend (left column) and Orderbook
#   legend (right column).
_LEGEND_LABELS = [    # (x, y, cx, label) x8 — archetype captions: Retirements legend (left col) + Orderbook legend (right col)
    (5.582, 2.613, 0.599, "Container"),
    (5.582, 2.835, 0.491, "General"),
    (5.582, 3.057, 0.417, "RORO"),
    (5.582, 3.28, 0.431, "Tanker"),
    (6.543, 2.613, 0.599, "Container"),
    (6.543, 2.835, 0.491, "General"),
    (6.543, 3.057, 0.417, "RORO"),
    (6.543, 3.28, 0.431, "Tanker"),
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
    # ── orderbook-window rail (grey band behind the chart's left years) ──
    out.append(text_box(n(), "Rectangle 30", IN(0.783), IN(2.104), IN(1.354), IN(4.276), [paragraph([run("Years with ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("orderbook ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("data", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), line_break(), line_break()], align="r", line_spacing=100000)], fill=GRAY_1, line_color="none", anchor="b"))   # F2F2F2 off-white
    # ── styled chart (data-over-template) + category axis ──
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.325), y=IN(1.866), cx=IN(7.359), cy=IN(4.165), rId="rId2"))
    # Tick labels are right-aligned, no-wrap, and zero-inset so their boxes
    # register precisely to the plotted categories.
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── chart title ──
    out.append(text_box(n(), "Text Placeholder 25", IN(0.484), IN(1.752), IN(6.707), IN(0.167), [paragraph([run("Implied Retirements vs. Orderbook of US-Built, US-Flagged Oceangoing Commercial Vessels (# Hulls)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── data labels: bar totals (net hulls added/removed) ──
    # Centered paragraphs use tight side insets in narrow source-fit boxes.
    for _x, _y, _t in _DATA_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _BARVAL_W, _BARVAL_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # two standalone "4" data labels (2028 orderbook), interleaved in paint order
    out.append(text_box(n(), "Text Placeholder 25", IN(1.674), IN(2.837), IN(0.115), IN(0.167), [paragraph([run("4", size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(1.946), IN(2.837), IN(0.115), IN(0.167), [paragraph([run("4", size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "Without SHIPS Act"))
    out.append(title_placeholder("Status Quo Outlook (Oceangoing Commercial)", "Replacing retirements unlikely to support serial production, preventing meaningful newbuild cost reductions."))
    # ── table — avg retirement replacements required per year ’26-’50 ──
    # col_widths fixes the three comparison columns and trow(h=...) their
    # row minima. Repeated cell insets/anchor/align encode row/column padding
    # and alignment; tpara mar_l/indent encodes commentary bullet margins.
    # palette — text: 000000 black (labels) · FFFFFF white (archetype cells) · C30C3E crimson (figures);
    #   fills: 9DB1CF light blue · 6F8DB9 blue · 4C6C9C blue · 364D6E dark blue; rules: 000000 black · 808080 gray.
    out.append(table(n(), "Table 769", IN(7.747), IN(1.685), IN(5.049), IN(3.867), col_widths=[IN(1.181), IN(1.723), IN(2.145)], rows=[
        trow([cell("Average retirement replacements required per year ’26-’50", bold=True, span=3, B=edge(BLACK))], h=IN(0)),
        trow([cell("Archetype", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)), cell("Total", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)), cell("Net of Orderbook Deliveries", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK))], h=IN(0)),
        trow([cell("Container", bold=True, color=WHITE, fill="9DB1CF", T=edge(BLACK), B=edge("808080", 6350)), cell("~0.6", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge(BLACK), B=edge("808080", 6350)), cell("~0.4", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge(BLACK), B=edge("808080", 6350))], h=IN(0.6)),
        trow([cell("General", bold=True, color=WHITE, fill="6F8DB9", T=edge("808080", 6350), B=edge("808080", 6350)), cell("~0.2", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)), cell("~0.2", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.6)),
        trow([cell("RORO", bold=True, color=WHITE, fill="4C6C9C", T=edge("808080", 6350), B=edge("808080", 6350)), cell("~0.2", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)), cell("~0.2", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.6)),
        trow([cell("Tanker", bold=True, color=WHITE, fill="364D6E", T=edge("808080", 6350), B=edge("808080", 6350)), cell("~1.7", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)), cell("~1.2", size=PT(16), bold=True, color="C30C3E", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.6)),
        trow([cell("Commentary", bold=True, T=edge("808080", 6350)), rcell([tpara([trun("Assumes owners replace retirements 1-for-1 and at the end of estimated service life", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450), tpara([], bullet=True, mar_l=171450, indent=-171450), tpara([trun("Tanker figures include multiple types, including product, chemical & oil, crude, and shuttle", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450)], span=2, T=edge("808080", 6350))], h=IN(0.6)),
    ]))
    # ── legend — Retirements frame + Orderbook frame, archetype keys +
    #    captions, and the bar-total wedge callout (all interleaved in paint order) ──
    out.append(text_box(n(), "Rectangle 840", IN(5.283), IN(2.488), IN(0.932), IN(0.98), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="121415", anchor="ctr"))   # 121415 near-black outline
    # Keys have empty centered text bodies; caption boxes below are centered,
    # no-wrap, zero-inset, and use zero paragraph margins.
    for _x, _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Speech Bubble: Rectangle 645", IN(5.193), IN(1.965), IN(2.382), IN(0.425), [paragraph([run("Bar total values indicate net hulls added (removed) each year", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val -19106", "adj2": "val -3267"}, anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "Rectangle 839", IN(5.325), IN(2.412), IN(0.849), IN(0.159), [paragraph([run("Retirements", size=PT(8), italic=True, color=BLACK, font=FONT), run("1", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "Rectangle 688", IN(6.247), IN(2.488), IN(0.932), IN(0.98), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="121415", anchor="ctr"))   # 121415 near-black outline
    out.append(text_box(n(), "Rectangle 689", IN(6.288), IN(2.412), IN(0.849), IN(0.159), [paragraph([run("Orderbook", size=PT(8), italic=True, color=BLACK, font=FONT), run("2", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    # ── takeaway banner ──
    out.append(text_box(n(), "Rectangle 690", IN(7.79), IN(5.652), IN(5.094), IN(0.68), [paragraph([run("~0.2-1.2 vessels per year is insufficient for serial production ", size=PT(12), bold=True, color=BLACK, font=FONT), run("(5+ hulls/yr. to achieve max labor efficiencies by end of year 2)", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color="none", anchor="ctr"))   # CEDDEC pale blue
    # ── footnote — kept verbatim (sits off the house Source position) ──
    out.append(text_box(n(), "Rectangle 694", IN(0.495), IN(6.68), IN(12.367), IN(0.317), [paragraph([run("Note: (1) Service life assumptions – 40 years for Bulk, Container, General Cargo, and RORO, 35 years for Tankers, 30 years for PSVs, and 25 years for Crew/FSVs; (2) All Oceangoing Commercial vessels in orderbook are built at Hanwha Philly, including containerships purchased by Matson and 12x tankers (10x Chemical & Oil and 2x LNG) purchased by Hanwha Shipping | Source: Clarksons (US fleet size and GT data)", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    # ── serial-production key — red "#" (does not support) / green "#" (supports) ──
    out.append(text_box(n(), "Rectangle 715", IN(10.438), IN(1.429), IN(0.301), IN(0.26), [paragraph([run("#", size=PT(16), bold=True, color="C30C3E", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # C30C3E crimson
    out.append(text_box(n(), "TextBox 716", IN(10.694), IN(1.442), IN(2.101), IN(0.234), [paragraph([run("Does not support serial production", size=PT(10), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "Rectangle 717", IN(10.438), IN(1.187), IN(0.301), IN(0.26), [paragraph([run("#", size=PT(16), bold=True, color="007770", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 007770 teal
    out.append(text_box(n(), "TextBox 718", IN(10.694), IN(1.2), IN(2.101), IN(0.234), [paragraph([run("Supports serial production", size=PT(10), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(prelim_chip())
    # ── Hanwha callout (wedge over the chart) ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 2", IN(2.239), IN(3.166), IN(1.501), IN(0.416), [paragraph([run("12x purchased by Hanwha Shipping", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -59329", "adj2": "val -21373"}, anchor="ctr"))   # 000000 black outline
    # ── scenario chip (top-right) ──
    out.append(text_box(n(), "Rectangle 4", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))   # CEDDEC pale blue
    return "".join(out)


def render() -> str:
    return slide(_body())
