"""Slide module: DDG-51 subaward-to-hull linkage - results readout.

ROLE
  attribution_results / coverage_plus_ranked_concentration

USE WHEN
  A slide needs to report an attribution result without grading language: a
  left column split into two stacked-column exhibits (a tier-coverage column on
  top, a ranked per-hull concentration column below), a right-hand
  interpretation table that tells the reader how to use each result surface, and
  a full-width caveat band that prevents the ranked chart from being read as
  total cost by hull.

TEACHES
  - two native editable column charts on one slide (rId2 + rId3) via CHARTS
  - a single-category stacked column used as a coverage bar, with grouped
    $/% brackets carried as manual slide text instead of native labels
  - a ranked single-series column with per-point block colors + native value
    labels and a wedge concentration callout over the leading columns
  - an external block color key (chips + captions) as slide text
  - a compact right-rail interpretation table built from the local table kit
  - an off-house caveat band that scopes the readout as coverage, not allocation

COMPOSITION (chart_plus_table; left split into two stacked exhibits)
  top-left   : attribution-tier coverage column  (column_chart, stacked, rId2)
  bottom-left: ranked exact-hull dollars by hull  (column_chart, ranked,  rId3)
  right      : "How the results should be used"   (native table)
  bottom     : coverage-not-allocation caveat band (full-width text band)

FIDELITY NOTE
  Practical factory-native build. Both charts are real column_chart() specs with
  embedded editable workbooks; all manual labels, brackets, keys, and the table
  are slide-level objects positioned in inches. Audience-facing taxonomy is
  Exact hull / Family-level / Review queue only - no grade letters anywhere.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, Sources, body_slide, column_chart, connector, graphic_frame,
    line_break, paragraph, run, table, tcell, tcell_rich, text_box, tpara, trow, trun,
)

# ── House colors (hex lives in the module; no shared palette) ────────────────
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_RULE = "808080"
GRAY_HAIR = "BFBFBF"
GRAY_1 = "F2F2F2"
PALE_BLUE = "CEDDEC"
FONT = "Arial"

LAYOUT = "slideLayout4"

# ── Semantic palette ────────────────────────────────────────────────────────
# Exact-hull tiers read blue; family-level tiers read gray; the review sliver is
# a muted neutral that the right-side callout, not the column, has to explain.
EXACT_DK = "364D6E"   # exact hull · direct in-family hull text (the large tier)
EXACT_MD = "4C6C9C"   # exact hull · single-ship contract
FAM_MD = "969696"     # family-level · requirement-text signal only
FAM_LT = "C0C0C0"     # family-level · contract family only
REVIEW = "B9A7AE"     # review queue · conflict / multi-hull (held out)

# Ranked-column block colors (contract block / MYP).
BLOCK_FY23_27 = "364D6E"   # FY23-27 HII   - darkest blue
BLOCK_FY18_22 = "4C6C9C"   # FY18-22 HII   - medium blue
BLOCK_FY13_17 = "9DB1CF"   # FY13-17 HII   - light blue
BLOCK_FY11 = "808080"      # FY11 single-ship - gray


# ════════════════════════════════════════════════════════════════════════════
# Data - coverage tiers (single stacked column, FY2026$M)
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Tier:
    name: str        # evidence-basis label (Edit-Data series name only)
    dollars: float   # FY2026$M
    fill: str


# Bottom-to-top stacking order: exact-hull block, then family-level block, then
# the review sliver at the very top.
COVERAGE_TIERS: tuple[Tier, ...] = (
    Tier("Exact hull / single-ship contract", 69.0, EXACT_MD),
    Tier("Exact hull / direct in-family hull text", 1200.6, EXACT_DK),
    Tier("Family-level / requirement-text signal only", 1787.9, FAM_MD),
    Tier("Family-level / contract family only", 965.2, FAM_LT),
    Tier("Review queue / conflict / multi-hull", 5.4, REVIEW),
)

COVERAGE_TOTAL = sum(t.dollars for t in COVERAGE_TIERS)   # 4028.1
EXACT_TOTAL = COVERAGE_TIERS[0].dollars + COVERAGE_TIERS[1].dollars     # 1269.6
FAMILY_TOTAL = COVERAGE_TIERS[2].dollars + COVERAGE_TIERS[3].dollars    # 2753.1
REVIEW_TOTAL = COVERAGE_TIERS[4].dollars                                # 5.4


# ════════════════════════════════════════════════════════════════════════════
# Data - ranked exact-hull dollars by hull (top 12)
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Hull:
    label: str
    dollars: float   # FY2026$M assigned to the exact hull
    block: str       # color key


RANKED_HULLS: tuple[Hull, ...] = (
    Hull("DDG 145", 244.3, BLOCK_FY23_27),
    Hull("DDG 146", 195.3, BLOCK_FY23_27),
    Hull("DDG 143", 144.8, BLOCK_FY23_27),
    Hull("DDG 149", 129.4, BLOCK_FY23_27),
    Hull("DDG 117", 72.7, BLOCK_FY13_17),
    Hull("DDG 137", 64.8, BLOCK_FY18_22),
    Hull("DDG 141", 63.0, BLOCK_FY23_27),
    Hull("DDG 142", 49.1, BLOCK_FY23_27),
    Hull("DDG 147", 44.8, BLOCK_FY23_27),
    Hull("DDG 114", 36.1, BLOCK_FY11),
    Hull("DDG 113", 32.9, BLOCK_FY11),
    Hull("DDG 139", 32.2, BLOCK_FY18_22),
)

TOP4_TOTAL = sum(h.dollars for h in RANKED_HULLS[:4])   # 713.8 -> ~$714M

BLOCK_KEY: tuple[tuple[str, str], ...] = (
    (BLOCK_FY23_27, "FY23-27 HII"),
    (BLOCK_FY18_22, "FY18-22 HII"),
    (BLOCK_FY13_17, "FY13-17 HII"),
    (BLOCK_FY11, "FY11 single-ship"),
)


# ════════════════════════════════════════════════════════════════════════════
# Chart frames (inches) and the native column-chart specs
# ════════════════════════════════════════════════════════════════════════════
# Coverage column - narrow, tall, single stacked bar.
COV_X, COV_Y, COV_W, COV_H = 0.55, 1.98, 1.45, 1.50
COV_PLOT = {"x": 0.08, "y": 0.04, "w": 0.86, "h": 0.92}
COV_MAX = 4100.0

# Ranked columns - wide, short, 12 categories.
RNK_X, RNK_Y, RNK_W, RNK_H = 0.55, 4.00, 6.70, 1.62
RNK_PLOT = {"x": 0.065, "y": 0.07, "w": 0.915, "h": 0.72}
RNK_MAX = 260.0


COVERAGE_STYLE = {
    "mode": "stacked",
    "categories": ["DDG subaward coverage"],
    "series": [
        {"name": t.name, "color": t.fill, "values": [t.dollars], "hide_labels": True}
        for t in COVERAGE_TIERS
    ],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_labels": False,
    "show_value_axis_labels": False,   # group $/% brackets carry the numbers
    "show_gridlines": False,
    "value_axis_format": '#,##0',
    "gap_width": 60,
    "bar_overlap": 100,
    "seg_line_color": WHITE,            # thin white dividers between tiers
    "seg_line_width": 9525,
    "axis_line_color": DK,
    "axis_line_width": 9525,
    "value_axis_min": 0,
    "value_axis_max": COV_MAX,
    "value_axis_major_unit": 1000,
    "plot_layout": dict(COV_PLOT),
    "cat_header": "Coverage",
}

RANKED_STYLE = {
    "mode": "ranked",
    "categories": [h.label for h in RANKED_HULLS],
    "series": [{
        "name": "Exact-hull assigned $M",
        "color": BLOCK_FY23_27,
        "values": [h.dollars for h in RANKED_HULLS],
        "data_point_colors": [h.block for h in RANKED_HULLS],
    }],
    "show_legend": False,
    "show_cat_labels": True,
    "cat_label_size_pt": 8,
    "show_value_labels": True,
    "value_label_size_pt": 8,
    "value_label_bold": False,
    "value_label_format": '#,##0.0',
    "show_value_axis_labels": False,    # value labels sit on each column
    "show_gridlines": False,
    "value_axis_format": '#,##0',
    "gap_width": 55,
    "seg_line_color": WHITE,
    "seg_line_width": 6350,
    "axis_line_color": DK,
    "axis_line_width": 9525,
    "value_axis_min": 0,
    "value_axis_max": RNK_MAX,
    "value_axis_major_unit": 50,
    "plot_layout": dict(RNK_PLOT),
    "cat_header": "Hull",
}

CHARTS = [column_chart(**COVERAGE_STYLE), column_chart(**RANKED_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Local table kit - content first, cell mechanics second (renders identically to
# raw tcell()/tcell_rich(); the only gain is legibility at the call site).
# ════════════════════════════════════════════════════════════════════════════
def edge(color, w=12700):
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(9.5),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=36576, r_ins=36576, t_ins=27432, b_ins=27432, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── small text helpers (keep paint functions at slide-intent level) ──────────
def _r(text, *, size_pt=10, bold=False, italic=False, color=BLACK, baseline=None):
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None,
               color=color, font=FONT, baseline=baseline)


def _tight(runs, *, align=None):
    return paragraph(runs, align=align, mar_l=0, indent=0, line_spacing=100000)


def _label_box(n, name, x, y, w, h, lines, *, size_pt=10, bold=False, italic=False,
               color=BLACK, align="ctr", anchor="ctr", wrap="none", inset_x=0):
    """A no-fill manual label; `lines` is a tuple of strings joined by line breaks."""
    runs = []
    for i, ln in enumerate(lines):
        if i:
            runs.append(line_break())
        runs.append(_r(ln, size_pt=size_pt, bold=bold, italic=italic, color=color))
    return text_box(n(), name, IN(x), IN(y), IN(w), IN(h), [_tight(runs, align=align)],
                    fill=None, line_color="none", anchor=anchor, wrap=wrap,
                    l_ins=inset_x, t_ins=0, r_ins=inset_x, b_ins=0)


# ── coverage column geometry: value -> y(inch) for bracket alignment ─────────
def _cov_y(cum_value: float) -> float:
    """Slide-space y (inches) of a cumulative coverage value, measured from the
    bottom of the stacked column up the fixed 0..COV_MAX axis."""
    plot_top = COV_Y + COV_PLOT["y"] * COV_H
    plot_h = COV_PLOT["h"] * COV_H
    return plot_top + plot_h * (1.0 - cum_value / COV_MAX)


# Cumulative tier boundaries (from the bottom), used by the brackets.
_C0 = 0.0
_C_EXACT = EXACT_TOTAL                       # 1269.6
_C_FAMILY = EXACT_TOTAL + FAMILY_TOTAL       # 4022.7
_C_TOP = COVERAGE_TOTAL                       # 4028.1

BRACKET_X = COV_X + COV_W + 0.04             # vertical brace spine, just right of the column
LABEL_X = BRACKET_X + 0.10
LABEL_W = 1.55


# ════════════════════════════════════════════════════════════════════════════
# Paint layer - appended in z-order (charts first, overlays on top)
# ════════════════════════════════════════════════════════════════════════════
def paint_coverage_exhibit(n) -> list[str]:
    out: list[str] = []
    # Title.
    out.append(_label_box(
        n, "CoverageTitle", 0.50, 1.71, 6.9, 0.20,
        ("DDG subaward dollar coverage by attribution tier, FY2026$M",),
        size_pt=10, bold=True, align="l", anchor="b"))
    # Native stacked coverage column.
    out.append(graphic_frame(sp_id=n(), name="CoverageColumn",
                             x=IN(COV_X), y=IN(COV_Y), cx=IN(COV_W), cy=IN(COV_H), rId="rId2"))

    # Group brace spines (exact-hull block, family-level block).
    exact_top, exact_bot = _cov_y(_C_EXACT), _cov_y(_C0)
    fam_top, fam_bot = _cov_y(_C_FAMILY), _cov_y(_C_EXACT)
    out.append(connector(n(), "ExactBrace", IN(BRACKET_X), IN(exact_top),
                         IN(0), IN(exact_bot - exact_top), color=GRAY_RULE, width=9525))
    out.append(connector(n(), "FamilyBrace", IN(BRACKET_X), IN(fam_top),
                         IN(0), IN(fam_bot - fam_top), color=GRAY_RULE, width=9525))

    # Group labels (two lines each), vertically centered on each block.
    ex_cy = (exact_top + exact_bot) / 2
    fam_cy = (fam_top + fam_bot) / 2
    out.append(_label_box(
        n, "ExactGroupLabel", LABEL_X, ex_cy - 0.18, LABEL_W, 0.36,
        ("Exact hull", "$1.27B / 31.5%"), size_pt=10, bold=True, align="l", anchor="ctr"))
    out.append(_label_box(
        n, "FamilyGroupLabel", LABEL_X, fam_cy - 0.18, LABEL_W, 0.36,
        ("Family-level", "$2.75B / 68.3%"), size_pt=10, bold=True,
        color=GRAY_RULE, align="l", anchor="ctr"))

    # Review-queue group label (one line, just below the chart title) + a wedge
    # callout in the open space to the right pointing back at the top sliver.
    review_y = _cov_y(_C_TOP)
    out.append(_label_box(
        n, "ReviewGroupLabel", LABEL_X, review_y - 0.02, LABEL_W + 0.4, 0.16,
        ("Review queue  $5M / 0.1%",), size_pt=9, italic=True, align="l", anchor="t"))
    out.append(text_box(
        n(), "ReviewCallout", IN(4.50), IN(review_y - 0.10), IN(1.95), IN(0.30),
        [_tight([_r("63 rows / $5.4M held for review", size_pt=9, italic=True)], align="l")],
        fill=WHITE, line_color=GRAY_RULE, prst="wedgeRectCallout",
        geom_adj={"adj1": "val -118000", "adj2": "val 30000"}, anchor="ctr"))
    return out


def paint_ranked_exhibit(n) -> list[str]:
    out: list[str] = []
    # Title + subtitle.
    out.append(_label_box(
        n, "RankedTitle", 0.50, 3.58, 4.6, 0.20,
        ("Exact-hull assigned subaward dollars by hull, FY2026$M",),
        size_pt=10, bold=True, align="l", anchor="b"))
    out.append(_label_box(
        n, "RankedSubtitle", 0.50, 3.78, 5.2, 0.18,
        ("Exact-hull rows only; family-level spend is not forced onto hulls",),
        size_pt=9, italic=True, align="l", anchor="b"))
    # Native ranked column chart.
    out.append(graphic_frame(sp_id=n(), name="RankedHullColumns",
                             x=IN(RNK_X), y=IN(RNK_Y), cx=IN(RNK_W), cy=IN(RNK_H), rId="rId3"))

    # Block color key - a vertical 4-row stack in the upper-right whitespace of
    # the ranked frame (the right columns are short, so this space is empty).
    key_chip_x, key_label_x = 6.32, 6.47
    key_y0, key_step, chip = 4.02, 0.175, 0.12
    for i, (fill, caption) in enumerate(BLOCK_KEY):
        ky = key_y0 + i * key_step
        out.append(text_box(n(), "BlockKeyChip", IN(key_chip_x), IN(ky + 0.01), IN(chip), IN(chip),
                            [paragraph([], line_spacing=100000)], fill=fill, line_color="none"))
        out.append(_label_box(n, "BlockKeyLabel", key_label_x, ky - 0.005, 0.92, 0.16,
                              (caption,), size_pt=8, align="l", anchor="ctr"))

    # Concentration callout over the four leading columns.
    out.append(text_box(
        n(), "Top4Callout", IN(2.62), IN(4.06), IN(2.18), IN(0.52),
        [_tight([_r("DDG 145 / 146 / 143 / 149", size_pt=9, bold=True), line_break(),
                 _r("= ~$714M, over half of", size_pt=9), line_break(),
                 _r("exact-hull dollars", size_pt=9)], align="ctr")],
        fill=WHITE, line_color=GRAY_RULE, prst="wedgeRectCallout",
        geom_adj={"adj1": "val -52000", "adj2": "val 26000"}, anchor="ctr"))

    # Footnote: hulls carrying no exact-hull dollars.
    out.append(_label_box(
        n, "ZeroExactFootnote", 0.50, 5.66, 6.9, 0.18,
        ("Eleven mapped hulls carry no exact-hull dollars under the attribution rule.",),
        size_pt=8, italic=True, align="l", anchor="b"))
    return out


# ── right-side interpretation table ──────────────────────────────────────────
TABLE_ROWS: tuple[tuple[str, str, str], ...] = (
    ("Coverage view", "$4.03B \u00b7 6,020 records",
     "Full mapped DDG subaward universe"),
    ("Exact-hull view", "$1.27B \u00b7 2,380 records \u00b7 24 hulls",
     "Hull-level dollars where evidence supports assignment"),
    ("Family-level view", "$2.75B",
     "Real spend retained at contract-family level"),
    ("Vendor \u00d7 Hull exposure", "1,193 rows \u00b7 281 vendors \u00b7 24 hulls",
     "Supplier exposure by assigned hull"),
    ("Hull \u00d7 SWBS view", "1,296 rows \u00b7 HII-Ingalls only",
     "Functional-system view; BIW too thin for comparable SWBS coverage"),
    ("Review queue", "63 rows \u00b7 $5.4M",
     "Excluded from hull totals pending review"),
)


def paint_results_table(n) -> list[str]:
    rows = [
        trow([cell("How the results should be used", bold=True, span=3,
                   size=PT(11), B=edge(DK))], h=IN(0.30)),
        trow([
            cell("Result surface", bold=True, T=edge(DK), B=edge(DK)),
            cell("Population / readout", bold=True, align="r", T=edge(DK), B=edge(DK)),
            cell("Interpretation", bold=True, T=edge(DK), B=edge(DK)),
        ], h=IN(0.28)),
    ]
    for i, (surface, readout, interp) in enumerate(TABLE_ROWS):
        rule = edge(GRAY_HAIR, 6350)
        rows.append(trow([
            cell(surface, bold=True, B=rule),
            cell(readout, align="r", B=rule),
            cell(interp, B=rule),
        ], h=IN(0.52)))
    return [table(n(), "ResultsUseTable", IN(7.78), IN(1.69), IN(5.00), IN(3.60),
                  col_widths=[IN(1.25), IN(1.62), IN(2.13)], rows=rows)]


def paint_caveat_band(n) -> list[str]:
    return [text_box(
        n(), "CaveatBand", IN(0.50), IN(6.00), IN(12.36), IN(0.36),
        [_tight([
            _r("Readout is coverage, not forced allocation: ", size_pt=10, bold=True),
            _r("exact rows enter hull totals; family-level rows remain at contract "
               "family; conflicts stay out of roll-ups.", size_pt=10),
        ], align="l")],
        fill=PALE_BLUE, line_color="none", anchor="ctr",
        l_ins=91440, r_ins=91440, t_ins=27432, b_ins=27432)]


# ════════════════════════════════════════════════════════════════════════════
# Slide render
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    _ids = iter(range(100, 4000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    out: list[str] = []
    out += paint_coverage_exhibit(n)
    out += paint_ranked_exhibit(n)
    out += paint_results_table(n)
    out += paint_caveat_band(n)
    return "".join(out)


CHROME = Chrome(
    section="DDG-51 Subaward Attribution",
    topic="Results Readout",
    title="Subaward-to-Hull Linkage Results",
    takeaway="$1.27B pins to exact hulls, led by recent HII FY23-27 ships, with "
             "the remaining $2.75B held at contract-family level.",
    preliminary=True,
    sources=Sources(
        source="DDG-51 subaward-to-hull attribution workbook (USAspending subaward "
               "records; HII-Ingalls and BIW contract families)"),
)


def render() -> str:
    return body_slide(CHROME, _body())
