"""production_outlook_separate — Market sizing Golden Dome deck (20260116), source slide 12.

EXHIBIT — "Production Outlook (separate platforms)": the Golden Dome Marauder
production ramp when sensor and interceptor platforms are built separately. A
styled stacked-column chart ("Golden Dome Marauder starts by phase") plots
cumulative vessel starts across FY26-FY35, against a Franklin yard-capacity line
(the 8/17/28/50… series). On-chart number callouts (ringed in ellipse outlines:
5 / 23 / 48 / 74 / 100 / 135 / 170 / 205 / 240, plus two "35" Phase-3 caps) read
out the cumulative totals; the subtitle states the takeaway — Phase 1 done by
FY32, Phase 2 by FY33, Phase 3 by FY35 (slower than the co-located sibling).
Two bullet blocks below give the FY27-FY31 and FY32-FY35 forecast assumptions.
This is the separate-platforms sibling of production_outlook_colocated.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place; groups
interleave — chrome and the value rings/labels land mid-paint):
  • background panels .. Rectangle 117/116 = the grey plot-area fills (GRAY_2/GRAY_1)
  • styled chart ....... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                        data is _CHART0_DATA (3 series), the look is the source template
  • chart title ........ "Golden Dome Marauder starts by phase" + footnote run "1"
  • _CATEGORY_TICK_LABELS  fiscal-year category-axis labels under the chart
  • on-bar "35" labels . the two Phase-3 cumulative-cap data labels (FY34/FY35)
  • chrome ............. breadcrumb() + title_placeholder()
  • logos .............. picture() x2 top-right (IMAGES rId3/rId4)
  • _LEGEND_KEYS ......... phase colour keys
  • connector .......... dashed arrow pointing at the Franklin-capacity line
  • _LEGEND_LABELS ....... captions paired with the phase keys/capacity mark
  • assumption blocks .. TextBox 268/270 = FY27-FY31 / FY32-FY35 forecast bullets
  • footnote ........... Rectangle 370 Note line (off house position)
  • _HIGHLIGHT_RINGS ..... empty ellipse outlines emphasizing chart values
  • _DATA_LABELS ......... cumulative-vessel labels attached to plotted bars
  • axis caption ....... "Cumulative vessels" (TextBox 398)
  • prelim chip ........ "Preliminary" (off house position)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=10, connector=1, chart=1, picture=2, chrome_builders=2,
clusters=5 (covering 36 shapes), frozen_fields=16, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line and the Preliminary chip both sit off the house
position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, picture, breadcrumb, title_placeholder,
    graphic_frame, styled_chart, IN, PT, BLACK, PRELIM, GRAY_1, GRAY_2, FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide12_chart3.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide12_chart3.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [None, 5, 18, 25, 26, 26, 21, 8, 35, 35]},
        {"values": [None, None, None, None, None, None, 14, 27, None, None]},
        {"values": [8, 17, 28, 50, 50, 50, 50, 50, 50, 50]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]
IMAGES = [
    {"rId": "rId3", "file": "image7_3071a231.jpeg"},
    {"rId": "rId4", "file": "image8_ffd85751.png"},
]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_YEAR_LBL_Y, _YEAR_LBL_W, _YEAR_LBL_H = IN(5.26), IN(0.344), IN(0.167)   # FY axis-label row  [x10]
_SWATCH_Y, _SWATCH_W, _SWATCH_H = IN(1.811), IN(0.196), IN(0.146)        # legend colour chip [x3]
_LEGEND_LBL_Y, _LEGEND_LBL_H = IN(1.806), IN(0.167)                      # legend caption row [x4]
_BARVAL_Y, _BARVAL_H = IN(2.542), IN(0.269)                              # bar value-label row [x9]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the ten fiscal-year ticks under the chart.
_CATEGORY_TICK_LABELS = [    # (x, label) x10 — fiscal-year category-axis labels under the chart
    (1.233, "FY26"),
    (2.436, "FY27"),
    (3.639, "FY28"),
    (4.842, "FY29"),
    (6.045, "FY30"),
    (7.248, "FY31"),
    (8.451, "FY32"),
    (9.655, "FY33"),
    (10.858, "FY34"),
    (12.061, "FY35"),
]

# local_meaning: the three phase colour chips.
_LEGEND_KEYS = [    # (x, fill) x3
    (7.984, "9DB1CF"),   # 9DB1CF light blue
    (8.852, "6F8DB9"),   # 6F8DB9 blue
    (9.72, "364D6E"),    # 364D6E dark blue
]

# local_meaning: the four legend captions - phase-colour keys plus the Franklin-capacity key.
_LEGEND_LABELS = [    # (x, cx, label) x4 — phase-colour legend keys + Franklin-capacity key
    (8.236, 0.505, "Phase 1"),
    (9.104, 0.505, "Phase 2"),
    (9.972, 0.505, "Phase 3"),
    (10.84, 1.939, "Franklin capacity (vessel starts)"),
]

# local_meaning: the ten empty ellipse outlines emphasizing the on-chart values.
_HIGHLIGHT_RINGS = [    # (x, y, cx, cy) x10 — empty ellipse outlines emphasizing on-chart values
    (8.334, 2.507, 0.602, 0.34),
    (11.933, 2.507, 0.602, 0.34),
    (9.529, 2.507, 0.602, 0.34),
    (10.726, 2.507, 0.602, 0.34),
    (7.121, 2.507, 0.602, 0.34),
    (2.311, 2.507, 0.602, 0.34),
    (3.524, 2.507, 0.602, 0.34),
    (4.717, 2.507, 0.602, 0.34),
    (5.91, 2.507, 0.602, 0.34),
    (6.382, 1.825, 0.211, 0.131),
]

# local_meaning: the nine cumulative-vessel counts riding the bars.
_DATA_LABELS = [    # (x, cx, label) x9 — cumulative-vessel data labels riding the bars
    (8.417, 0.435, "135"),
    (12.016, 0.435, "240"),
    (9.612, 0.435, "170"),
    (10.809, 0.435, "205"),
    (7.205, 0.435, "100"),
    (2.472, 0.279, "5"),
    (3.646, 0.358, "23"),
    (4.839, 0.358, "48"),
    (6.032, 0.358, "74"),
]
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
    # ── plot-area background panels (right GRAY_2, left GRAY_1) ──
    out.append(text_box(n(), "Rectangle 117", IN(8), IN(2.172), IN(4.835), IN(4.536), [paragraph([], line_spacing=100000)], fill=GRAY_2, line_color="none"))   # D9D9D9 light gray
    out.append(text_box(n(), "Rectangle 116", IN(1.794), IN(2.172), IN(6.206), IN(4.536), [paragraph([], line_spacing=100000)], fill=GRAY_1, line_color="none"))   # F2F2F2 off-white
    # ── styled chart (data-over-template) + its title ──
    # The title is bottom-anchored, no-wrap, and zero-inset so its baseline
    # registers exactly to the chart frame.
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.398), y=IN(1.931), cx=IN(12.528), cy=IN(3.53), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.51), IN(1.816), IN(2.667), IN(0.167), [paragraph([run("Golden Dome Marauder starts by phase", size=PT(10), bold=True, color=BLACK, font=FONT), run("1", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── chart axis: fiscal-year category labels ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _YEAR_LBL_Y, _YEAR_LBL_W, _YEAR_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── on-bar "35" data labels (Phase-3 cumulative caps, FY34/FY35) ──
    out.append(text_box(n(), "Text Placeholder 25", IN(8.528), IN(3.502), IN(0.191), IN(0.167), [paragraph([run("35", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(9.731), IN(3.502), IN(0.191), IN(0.167), [paragraph([run("35", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("Golden Dome Requirements", "Production Outlook"))
    out.append(title_placeholder("Production Outlook (separate platforms)", "All Phase 1 vessels started by FY32, Phase 2 by FY33, and Phase 3 by FY35"))
    # ── logos (top-right) ──
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(11.431), IN(0.048), IN(0.922), IN(0.922)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 8", "rId4", IN(12.372), IN(0.048), IN(0.922), IN(0.922)))
    # ── legend: phase colour chips + dashed pointer to Franklin-capacity line + caption keys ──
    for _x, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SWATCH_Y, _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 64", IN(10.599), IN(1.884), IN(0.175), IN(0), color=BLACK, width=19050, dashed=True, arrow=True))   # 000000 black
    for _x, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _LEGEND_LBL_Y, IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── forecast-assumption bullet blocks (left FY27-FY31, right FY32-FY35) ──
    out.append(text_box(n(), "TextBox 268", IN(1.794), IN(5.429), IN(6.206), IN(1.279), [paragraph([run("FY27-FY31 forecast assumes:", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Franklin Phase 2 completion pulled forward to JUN ‘28 (vs. DEC ‘28), increasing capacity to 50x vessels / year", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("US Navy purchases 10x MASC vessels / year, with FY29-FY31 vessels incremental to OBBBA amount", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("US Army purchases 14-15 ARV / year FY29-FY31 ", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Fulfilling MASC and ARV orders takes precedence and GD consumes remaining yard capacity", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)], fill=None, line_color="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 270", IN(8), IN(5.429), IN(4.835), IN(1.111), [paragraph([run("FY32-FY35 forecast assumes:", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Fulfilling GD orders takes precedence (70% of yard capacity), with remaining capacity for other customers", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Interceptor and sensor production constraints limit FOC node fielding, driving relatively even production distribution throughout period", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 370", IN(0.495), IN(6.79), IN(12.367), IN(0.206), [paragraph([run("Note: (1) Assumes vessels are only produced at Franklin facility ", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── cumulative-vessel callouts: ellipse rings, then the numbers they enclose ──
    for _x, _y, _cx, _cy in _HIGHLIGHT_RINGS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="ellipse", anchor="ctr"))   # 000000 black outline
    for _x, _cx, _t in _DATA_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), _BARVAL_Y, IN(_cx), _BARVAL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", wrap="none"))   # 000000 black
    # ── "Cumulative vessels" axis caption ──
    out.append(text_box(n(), "TextBox 398", IN(6.382), IN(1.791), IN(1.6), IN(0.2), [paragraph([run("Cumulative vessels", size=PT(10), color=BLACK, font=FONT)], align="r", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── Preliminary chip (off house position - kept verbatim) ──
    out.append(text_box(n(), "Rectangle 6", IN(7.911), IN(0.122), IN(1.605), IN(0.29), [paragraph([run("Preliminary", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=PRELIM, line_color="121415", line_width=19050, anchor="ctr"))   # FFFFCC pale yellow
    return "".join(out)


def render() -> str:
    return slide(_body())
