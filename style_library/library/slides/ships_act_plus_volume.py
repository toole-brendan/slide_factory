"""ships_act_plus_volume — Commercial Strategy Market Analysis deck (20260325), source slide 52.

EXHIBIT — "SHIPS Act “Plus” Volume": the upside ("Plus") scenario where revised
legislation lifts the subsidy pool, so modeled additions to the US-built,
oceangoing commercial fleet ramp higher before demand DECLINES after the
mid-2030s as SCF and other programs reach their fleet caps. A native styled bar
chart spans the build-out years 2026–2050 (the x-axis), stacking annual
deliveries under the "(3) SHIPS Act “Plus” Scenario" series. Two stacked
annotation systems read off the chart: on the LEFT, a small WHITE legend keys the
demand bands (Excess US capacity · Heritage Foundation target · SHIPS Act "Plus"
Scenario · Retirement replacements · Orderbook) plus a "Confidence level"
Higher/Lower scale; on the RIGHT, dashed capacity-phase rules carry right-arrow
markers and Port Alpha phase labels (Phase 1 6/yr. … Phase 5 125/yr.) up to the
"10M GT" target. Along the bottom, five ellipse badges give the modeled % of
deliveries attributable to Port Alpha (70% · 83% · 78% · 75% · 75%), with two
speech-bubble caveats (revisions to SHIPS Act / Building Ships in America Act;
universal cargo fees + MSTF cap increase).

CODE MAP (body follows source PAINT ORDER; headers mark roles in place; the
chrome and the two annotation systems interleave with the chart in paint order):
  • styled chart .......... graphic_frame(rId2) → CHARTS[0] = styled_chart(...);
                            the data is _CHART0_DATA (8 stacked series × 25 yrs),
                            the look is the source chart template
  • _REFERENCE_MARKERS ... right-arrow glyphs on capacity reference rules
  • _PHASE_RULES_X1 etc. .. six dashed phase divider connectors (shared coords)
  • _CATEGORY_TICK_LABELS  category-axis years 2026–2050
  • axis titles ........... "10M GT¹" right cap + "Additions to … fleet" y-title
  • _REFERENCE_LABELS .... Port Alpha phase/capacity rule captions
  • legend ................. _LEGEND_PANEL + _LEGEND_KEYS + _LEGEND_LABELS
  • chrome ................ breadcrumb() + title_placeholder() (interleaved here)
  • _SUMMARY_BADGES ...... ellipse % badges (Port Alpha share of deliveries)
  • pattern swatch ........ ltUpDiag pattern_fill chip in the legend
  • prelim/scenario chips .. prelim_chip() + "(3) SHIPS Act “Plus” Scenario"
  • _SCALE_LABELS ........ qualitative Higher / Lower confidence labels
  • notes/captions ........ sources_line() footnote, capacity caption, "% attributable"
                            caption, two wedgeRectCallout speech bubbles

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=9, connector=13, chart=1, chrome_builders=4,
clusters=6 (covering 54 shapes), frozen_fields=30, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line is folded into sources_line() verbatim; the
prelim_chip() marks this as a Preliminary exhibit.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder, prelim_chip,
    sources_line, graphic_frame, styled_chart, IN, PT, BLACK, WHITE, DK, FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide52_chart31.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide52_chart31.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [1, 2, 2, 5, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, 9, 10, 3, None, 2, 1, 2, 2, 4, 2, 4, 5, 7, 7, 1, 1, None, 2, 3]},
        {"values": [None, None, None, 7, 15, 30, 41, 59, 100, 69, 10, 6, 3, 1, 2, 8, None, 5, None, 5, None, 5, 1, None, 7]},
        {"values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, None, None, None, 48, 122, 130, 134, 153, 154, 151, 56, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 102, 154, 158, 154, 165, 160, 165, 164, 156]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates) ──
_ARROW_X, _ARROW_W, _ARROW_H = IN(11.717), IN(0.141), IN(0.167)   # right-arrow phase markers
_YEAR_Y, _YEAR_W, _YEAR_H = IN(5.479), IN(0.167), IN(0.306)       # x-axis year-label row
_ANNOT_LBL_H = IN(0.167)                                          # annotation-label height
_PCT_Y, _PCT_H = IN(5.868), IN(0.256)                             # % badge row
_PHASE_RULES_X1 = IN(0.911)   # phase divider start-x       [shared x8]
_PHASE_RULES_W1 = IN(10.75)   # phase divider width         [shared x6]
_ARROW_RULES_W2 = IN(10.9)    # arrow-rule width            [shared x6]
_ARROW_RULES_H1 = IN(0.008)   # arrow-rule height           [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the six right-arrow marks on the capacity reference rules (Port Alpha phase
#   targets).
_REFERENCE_MARKERS = [    # (y) x6 — right-arrow marks on capacity reference rules
    2.108,
    2.658,
    2.983,
    3.63,
    4.587,
    4.28,
]

# local_meaning: the twenty-five build-out year ticks 2026-2050.
_CATEGORY_TICK_LABELS = [    # (x, label) x25 — category-axis build-out years 2026–2050
    (5.755, "2037"),
    (6.203, "2038"),
    (6.651, "2039"),
    (7.099, "2040"),
    (7.547, "2041"),
    (8.443, "2043"),
    (8.891, "2044"),
    (9.339, "2045"),
    (9.786, "2046"),
    (2.62, "2030"),
    (10.682, "2048"),
    (11.13, "2049"),
    (11.578, "2050"),
    (10.234, "2047"),
    (0.828, "2026"),
    (1.276, "2027"),
    (1.724, "2028"),
    (2.172, "2029"),
    (3.068, "2031"),
    (3.516, "2032"),
    (7.995, "2042"),
    (3.964, "2033"),
    (4.411, "2034"),
    (4.859, "2035"),
    (5.307, "2036"),
]

# local_meaning: the five Port Alpha phase/capacity reference labels on the rules.
_REFERENCE_LABELS = [    # (x, y, cx, label) x5 — Port Alpha phase/capacity references
    (11.913, 2.658, 1.281, "PA Phase 5 (125/yr.)"),
    (11.913, 2.983, 1.281, "PA Phase 4 (105/yr.)"),
    (11.913, 3.63, 1.205, "PA Phase 3 (65/yr.)"),
    (11.913, 4.28, 1.205, "PA Phase 2 (25/yr.)"),
    (11.913, 4.587, 1.128, "PA Phase 1 (6/yr.)"),
]

# local_meaning: the five demand-band captions in the chart legend.
_LEGEND_LABELS = [    # (x, y, cx, label) x5 — demand-band captions in the chart legend
    (1.342, 1.922, 1.222, "Excess US capacity"),
    (1.342, 2.144, 2.488, "Heritage Foundation target (incremental)"),
    (1.342, 2.366, 1.641, "SHIPS Act \"Plus\" Scenario"),
    (1.342, 2.589, 1.545, "Retirement replacements"),
    (1.342, 2.811, 0.653, "Orderbook"),
]

_LEGEND_PANEL = (0.979, 1.85, 3.91, 1.191, WHITE)  # singular white backdrop; not a key

# local_meaning: the four demand-band colour chips.
_LEGEND_KEYS = [    # (x, y, cx, cy, fill) x4 — demand-band visual keys
    (1.09, 1.927, 0.196, 0.146, "C30C3E"),   # C30C3E crimson
    (1.09, 2.372, 0.196, 0.146, "364D6E"),   # 364D6E dark blue
    (1.09, 2.594, 0.196, 0.146, "C0C0C0"),   # C0C0C0 silver
    (1.09, 2.816, 0.196, 0.146, "808080"),   # 808080 gray
]

# local_meaning: the five Port Alpha share-of-deliveries badges.
_SUMMARY_BADGES = [    # (x, cx, label) x5 — Port Alpha share-of-deliveries badges
    (2.49, 0.451, "70%"),
    (4.717, 0.451, "83%"),
    (6.957, 0.451, "78%"),
    (9.196, 0.451, "75%"),
    (11.435, 0.452, "75%"),
]

# local_meaning: the Higher / Lower / Confidence-level scale labels beside the demand bands.
_SCALE_LABELS = [    # local extension: Higher / Lower / Confidence level labels
    (4.091, 2.912, 0.6, 0.1, None, "Higher"),   # 000000 black
    (4.091, 2.071, 0.6, 0.1, None, "Lower"),   # 000000 black
    (3.86, 2.475, 1.063, 0.133, WHITE, "Confidence level"),   # FFFFFF white
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
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.429), y=IN(1.696), cx=IN(11.323), cy=IN(3.906), rId="rId2"))
    # ── reference markers on capacity rules; empty centered bodies, padding inert ──
    for _y in _REFERENCE_MARKERS:
        out.append(text_box(n(), "LegendSwatch", _ARROW_X, IN(_y), _ARROW_W, _ARROW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=DK, line_color="none", prst="rightArrow", geom_adj={"adj1": "val 100000", "adj2": "val 100000"}, anchor="ctr", rot=10800000))   # 162029 dark navy
    # ── dashed phase divider rules (right side) ──
    out.append(connector(n(), "Straight Connector 451", _PHASE_RULES_X1, IN(3.066), _PHASE_RULES_W1, IN(0), color=BLACK, width=9525, dashed=True, arrow=True))   # 000000 black
    out.append(connector(n(), "Straight Connector 33", _PHASE_RULES_X1, IN(2.191), _PHASE_RULES_W1, IN(0), color=BLACK, width=9525, dashed=True, arrow=True))   # 000000 black
    out.append(connector(n(), "Straight Connector 50", _PHASE_RULES_X1, IN(2.741), _PHASE_RULES_W1, IN(0), color=BLACK, width=9525, dashed=True, arrow=True))   # 000000 black
    out.append(connector(n(), "Straight Connector 462", _PHASE_RULES_X1, IN(3.714), _PHASE_RULES_W1, IN(0), color=BLACK, width=9525, dashed=True, arrow=True))   # 000000 black
    out.append(connector(n(), "Straight Connector 473", _PHASE_RULES_X1, IN(4.363), _PHASE_RULES_W1, IN(0), color=BLACK, width=9525, dashed=True, arrow=True))   # 000000 black
    out.append(connector(n(), "Straight Connector 486", _PHASE_RULES_X1, IN(4.67), _PHASE_RULES_W1, IN(0), color=BLACK, width=9525, dashed=True, arrow=True))   # 000000 black
    # ── category-axis tick labels — right-aligned, no-wrap, zero-inset ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _YEAR_Y, _YEAR_W, _YEAR_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── axis titles: 10M GT right cap + y-axis title ──
    out.append(text_box(n(), "Text Placeholder 25", IN(11.913), IN(2.108), IN(0.552), IN(0.167), [paragraph([run("10M GT", size=PT(10), color=BLACK, font=FONT), run("1", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(0.542), IN(1.505), IN(4.347), IN(0.167), [paragraph([run("Additions to US-Built, Oceangoing Commercial Fleet (# deliveries)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── reference labels, then legend labels (same source paint order) ──
    # Both systems use centered vertical anchoring, no-wrap, zero shape insets,
    # and zero paragraph margins for exact rule/key registration.
    for _x, _y, _cx, _t in _REFERENCE_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _ANNOT_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    for _x, _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _ANNOT_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 556", IN(0.913), IN(2.729), _ARROW_RULES_W2, _ARROW_RULES_H1, color=BLACK, width=9525, dashed=True))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 531", IN(0.913), IN(2.183), _ARROW_RULES_W2, _ARROW_RULES_H1, color=BLACK, width=9525, dashed=True))   # 000000 black
    # ── legend panel + legend keys ──
    # These shapes have empty centered text bodies; padding is visually inert.
    _x, _y, _cx, _cy, _fill = _LEGEND_PANEL
    out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))   # FFFFFF white
    for _x, _y, _cx, _cy, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    # ── chrome (interleaved in paint order) ──
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    out.append(title_placeholder("SHIPS Act “Plus” Volume", "Demand declines after mid-2030s as SCF and other programs reach fleet caps; path to Phase 2 and beyond requires additional demand signals."))
    out.append(text_box(n(), "Rectangle 394", IN(0.249), IN(5.826), IN(1.923), IN(0.34), [paragraph([run("Modeled % deliveries attributable to Port Alpha:", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── summary badges: centered ellipse labels with explicit zero side padding ──
    for _x, _cx, _t in _SUMMARY_BADGES:
        out.append(text_box(n(), "ValueLabel", IN(_x), _PCT_Y, IN(_cx), _PCT_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=6350, prst="ellipse", anchor="ctr", l_ins=0, r_ins=0))   # 000000 black outline
    # ── pattern swatch (ltUpDiag legend chip) ──
    out.append(text_box(n(), "Rectangle 413", IN(1.09), IN(2.149), IN(0.196), IN(0.146), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="none", pattern_fill={"prst": "ltUpDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"}, anchor="ctr"))
    out.append(prelim_chip())
    # ── scenario chip (top-right) ──
    out.append(text_box(n(), "Rectangle 23", IN(8.069), IN(0.173), IN(2.977), IN(0.218), [paragraph([run("(3) SHIPS Act “Plus” Scenario", size=PT(12), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="0E1924", line_color=BLACK, anchor="ctr"))   # 0E1924 near-black navy
    out.append(connector(n(), "Straight Arrow Connector 559", IN(0.913), IN(3.052), _ARROW_RULES_W2, _ARROW_RULES_H1, color=BLACK, width=9525, dashed=True))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 562", IN(0.913), IN(3.712), _ARROW_RULES_W2, _ARROW_RULES_H1, color=BLACK, width=9525, dashed=True))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 566", _PHASE_RULES_X1, IN(4.35), _ARROW_RULES_W2, _ARROW_RULES_H1, color=BLACK, width=9525, dashed=True))   # 000000 black
    # ── qualitative scale labels — centered vertically/horizontally ──
    for _x, _y, _cx, _cy, _fill, _t in _SCALE_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 568", IN(4.391), IN(2.171), IN(0), IN(0.741), color=BLACK, width=28575, arrow=True))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 63", _PHASE_RULES_X1, IN(4.653), _ARROW_RULES_W2, _ARROW_RULES_H1, color=BLACK, width=9525, dashed=True))   # 000000 black
    # ── notes/captions: footnote + capacity caption + speech-bubble caveats ──
    out.append(sources_line("Note: (1) Assumes avg. 50K GT per newbuild (~13K higher than current fleet avg.); 10M GT target may be achieved with 140-160 deliveries / year with 60K-70K GT per newbuild | Source: MAP; SHIPS Act; Building Ships in America; 46 USC 53106 (MSP subsidy); 46 USC 53406 (TSP subsidy); MARAD (MSP / TSP participation); MARAD (vessel characteristics); MARAD (US vs. foreign-flag operating costs); GAO report on Maritime Security; FRED (PPI, BE Inflation); EIA AEO (Crude & LNG exports); BP (conversions); USTR (Section 301 Actions); USTR (Section 301 Action modifications); GAO (USG/USDA volume); IMF (Import forecast); S&P (Current and forecast prices, FX rates, US trade volumes and destinations); Drewry (foreign-flag opex; near-term cost growth outlook); Clarksons (Orderbook, current fleet, retirements, capacity, observed service life); Press releases (competitor expansion); Market participant feedback (Service life, build assumptions)"))
    out.append(text_box(n(), "Speech Bubble: Rectangle 8", IN(3.187), IN(4.815), IN(2.019), IN(0.448), [paragraph([run("Contingent upon revisions to SHIPS Act, Building Ships in America Act, and existing programs", size=PT(8), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val 19859", "adj2": "val -3695"}, anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "Rectangle 7", IN(5.133), IN(1.499), IN(5.268), IN(0.437), [paragraph([run("Demand modeled with Port Alpha Phase 5 capacity; demand would spread over more years if capacity held at earlier phases ", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color="none", anchor="ctr"))   # CEDDEC pale blue
    out.append(text_box(n(), "Rectangle 9", IN(10.5), IN(1.499), IN(2.694), IN(0.506), [paragraph([run("Total US delivery capacity by 2050 w/ PA phases and competitor expansion; PA deliveries in parenthetical", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Speech Bubble: Rectangle 12", IN(5.67), IN(4.901), IN(2.185), IN(0.278), [paragraph([run("Requires increased universal cargo fees and MSTF balance cap increase", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val 19859", "adj2": "val -3695"}, anchor="ctr"))   # FFFFFF white
    return "".join(out)


def render() -> str:
    return slide(_body())
