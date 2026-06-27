"""production_outlook_colocated — Market sizing Golden Dome deck (20260116), source slide 11.

EXHIBIT — "Production Outlook (co-located sensors and interceptors)": the
Golden Dome Marauder production ramp, phased so all Phase 1 vessels start by FY30,
Phase 2 by FY31, and Phase 3 by FY32. A styled column chart ("Golden Dome
Marauder starts by phase", FY26–FY35 on the x-axis) stacks per-phase starts
against the Franklin yard capacity line; on-chart ellipse rings call out the
cumulative-vessel running total (5 · 23 · 48 · 74 · 100 · 120…) and the est. 120x
MR requirement is annotated as met in FY32. Two tinted panels back the chart, a
phase-colour legend keys the bars, and two stacked text blocks state the
FY27-FY31 and FY32-FY35 forecast assumptions. A "Preliminary" chip and two
top-right logos finish the chrome.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • background panels .... Rectangle 117/116 = two tinted rectangles behind the chart
  • styled chart ......... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                           data is _CHART0_DATA (3 series), the look is the template;
                           "Text Placeholder 25" is its title
  • _CATEGORY_TICK_LABELS . fiscal-year category-axis labels (FY26–FY35) → loop
  • "26" annotations ..... two Text Placeholder boxes = FY30/FY31 in-year starts
  • chrome ............... breadcrumb() + title_placeholder()
  • logos ................ picture() ×2 top-right (IMAGES rId3/rId4)
  • _LEGEND_KEYS ......... phase colour chips → loop; the dashed capacity mark
                           and _LEGEND_LABELS captions interleave immediately after
  • assumption blocks .... TextBox 268/270 = FY27-FY31 and FY32-FY35 bulleted notes
  • _HIGHLIGHT_RINGS ... empty ellipse outlines emphasizing chart values → loop
  • _DATA_LABELS ........ cumulative-vessel numbers attached to the plotted bars;
                           "Cumulative vessels" axis caption follows
  • callouts ............. "Preliminary" chip + "requirement met in FY32" box

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=11, connector=1, chart=1, picture=2, chrome_builders=2,
clusters=5 (covering 36 shapes), frozen_fields=16, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line and the Preliminary chip both sit off the house
position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, picture, breadcrumb, title_placeholder,
    graphic_frame, styled_chart, IN, PT, BLACK, DK, PRELIM, GRAY_1, GRAY_2, FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide11_chart2.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide11_chart2.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [None, 5, 18, 25, 17, 19, 20, None, None, None]},
        {"values": [None, None, None, None, 9, 7, None, None, None, None]},
        {"values": [8, 17, 28, 50, 50, 50, 50, 50, 50, 50]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]
IMAGES = [
    {"rId": "rId3", "file": "image7_3071a231.jpeg"},
    {"rId": "rId4", "file": "image8_ffd85751.png"},
]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(5.26), IN(0.344), IN(0.167)   # fiscal-year tick row
_SWATCH_Y, _SWATCH_W, _SWATCH_H = IN(1.811), IN(0.196), IN(0.146)   # legend colour chips
_PHASE_LBL_Y, _PHASE_LBL_H = IN(1.806), IN(0.167)   # phase-label row (legend captions)
_BARVAL_Y, _BARVAL_H = IN(2.542), IN(0.269)   # on-bar cumulative-vessel number row

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the ten fiscal-year ticks under the chart (FY26-FY35).
_CATEGORY_TICK_LABELS = [    # (x, label) x10 — category-axis labels under the chart (FY26–FY35)
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

# local_meaning: the three phase colour chips (light->dark = Phase 1->3).
_LEGEND_KEYS = [    # (x, fill) x3 — visual series keys (light→dark)
    (7.984, "9DB1CF"),   # 9DB1CF light blue
    (8.852, "6F8DB9"),   # 6F8DB9 blue
    (9.72, "364D6E"),    # 364D6E dark blue
]

# local_meaning: the four legend captions beside the chips.
_LEGEND_LABELS = [    # (x, cx, label) x4 — captions paired with legend keys/reference mark
    (8.236, 0.505, "Phase 1"),
    (9.104, 0.505, "Phase 2"),
    (9.972, 0.505, "Phase 3"),
    (10.84, 1.939, "Franklin capacity (vessel starts)"),
]

# local_meaning: the ten empty ellipse outlines ringing the on-chart numbers.
_HIGHLIGHT_RINGS = [    # (x, y, cx, cy) x10 — empty ellipse outlines emphasizing the on-chart numbers
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

# local_meaning: the nine cumulative-vessel numbers riding the bars.
_DATA_LABELS = [    # (x, cx, label) x9 — cumulative-vessel data labels riding the bars
    (8.417, 0.435, "120"),
    (12.016, 0.435, "120"),
    (9.612, 0.435, "120"),
    (10.809, 0.435, "120"),
    (7.205, 0.435, "100"),
    (2.472, 0.279, "5"),
    (3.646, 0.358, "23"),
    (4.839, 0.358, "48"),
    (6.032, 0.358, "74"),
]

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
    # ── background panels (two tinted rectangles behind the chart) ──
    out.append(text_box(n(), "Rectangle 117", IN(8), IN(2.172), IN(4.835), IN(4.536), [paragraph([], line_spacing=100000)], fill=GRAY_2, line_color="none"))   # D9D9D9 light gray
    out.append(text_box(n(), "Rectangle 116", IN(1.794), IN(2.172), IN(6.206), IN(4.536), [paragraph([], line_spacing=100000)], fill=GRAY_1, line_color="none"))   # F2F2F2 off-white
    # ── styled chart (data-over-template) + its title ──
    # Shape text: the chart title is bottom-anchored, no-wrap, and zero-inset so
    # its baseline aligns exactly with the chart frame.
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.398), y=IN(1.931), cx=IN(12.528), cy=IN(3.53), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.51), IN(1.816), IN(2.667), IN(0.167), [paragraph([run("Golden Dome Marauder starts by phase", size=PT(10), bold=True, color=BLACK, font=FONT), run("1", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── category-axis labels (fiscal years under the chart) ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── on-bar "26" annotations (FY30 / FY31 in-year starts) ──
    out.append(text_box(n(), "Text Placeholder 25", IN(6.122), IN(3.891), IN(0.191), IN(0.167), [paragraph([run("26", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(7.325), IN(3.891), IN(0.191), IN(0.167), [paragraph([run("26", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("Golden Dome Requirements", "Production Outlook"))
    out.append(title_placeholder("Production Outlook (co-located sensors and interceptors)", "All Phase 1 vessels started by FY30, Phase 2 by FY31, and Phase 3 by FY32"))
    # ── logos (top-right) ──
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(11.431), IN(0.048), IN(0.922), IN(0.922)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 8", "rId4", IN(12.372), IN(0.048), IN(0.922), IN(0.922)))
    # ── legend: visual keys + the dashed capacity reference + captions ──
    # Keys have empty text bodies. Captions are vertically centered, no-wrap,
    # and zero-inset; paragraph margins are explicitly zero.
    for _x, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SWATCH_Y, _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 64", IN(10.599), IN(1.884), IN(0.175), IN(0), color=BLACK, width=19050, dashed=True, arrow=True))   # 000000 black
    for _x, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _PHASE_LBL_Y, IN(_cx), _PHASE_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── forecast-assumption blocks (FY27-FY31 left · FY32-FY35 right) ──
    # Shape text: top anchoring and default internal padding are retained. Bullet
    # paragraphs use mar_l=171450 / indent=-171450 for a hanging-bullet margin.
    out.append(text_box(n(), "TextBox 268", IN(1.794), IN(5.429), IN(6.206), IN(1.279), [paragraph([run("FY27-FY31 forecast assumes:", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Franklin Phase 2 completion pulled forward to JUN ‘28 (vs. DEC ‘28), increasing capacity to 50x vessels / year", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("US Navy purchases 10x MASC vessels / year, with FY29-FY31 vessels incremental to OBBBA amount", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("US Army purchases 14-15 ARV / year FY29-FY31 ", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Fulfilling MASC and ARV orders takes precedence and GD consumes remaining yard capacity", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)], fill=None, line_color="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 270", IN(8), IN(5.429), IN(4.835), IN(1.111), [paragraph([run("FY32-FY35 forecast assumes:", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Fulfilling GD orders takes precedence (70% of yard capacity), with remaining capacity for other customers", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Interceptor and sensor production constraints limit FOC node fielding, driving relatively even production distribution throughout period", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 370", IN(0.495), IN(6.79), IN(12.367), IN(0.206), [paragraph([run("Note: (1) Assumes vessels are only produced at Franklin facility ", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── on-chart emphasis rings, then the data labels they surround ──
    # Rings carry empty centered paragraphs; data-label paragraphs are centered.
    # The data-label boxes retain default padding because their widths were source-fit.
    for _x, _y, _cx, _cy in _HIGHLIGHT_RINGS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="ellipse", anchor="ctr"))   # 000000 black outline
    for _x, _cx, _t in _DATA_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), _BARVAL_Y, IN(_cx), _BARVAL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 398", IN(6.382), IN(1.791), IN(1.6), IN(0.2), [paragraph([run("Cumulative vessels", size=PT(10), color=BLACK, font=FONT)], align="r", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── Preliminary chip (off house position) + "requirement met in FY32" callout ──
    out.append(text_box(n(), "Rectangle 16", IN(7.911), IN(0.122), IN(1.605), IN(0.29), [paragraph([run("Preliminary", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=PRELIM, line_color="121415", line_width=19050, anchor="ctr"))   # FFFFCC pale yellow
    out.append(text_box(n(), "Rectangle 4", IN(9.338), IN(2.24), IN(3.368), IN(0.694), [paragraph([run("Est. requirement of 120x MR met in FY32", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=DK))   # 162029 dark navy outline
    return "".join(out)


def render() -> str:
    return slide(_body())
