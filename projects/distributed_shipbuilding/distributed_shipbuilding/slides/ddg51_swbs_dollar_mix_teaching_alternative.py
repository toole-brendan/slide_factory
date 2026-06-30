"""DDG-51 SWBS dollar mix — lead slide of the DDG subaward decklet.

ROLE
  market_mapping / swbs_dollar_mix

USE WHEN
  A slide must show ONE dollar base decomposed into a handful of ship-system
  groups: a single 100% stacked bar carries the composition, a top KPI row
  carries the headline numbers, a left reference table audits the dollars, and a
  right-hand commentary rail interprets what the mapped dollars are buying. A
  bracket under the bar reconciles the two denominators in play (share of total
  vs. share of mapped).

TEACHES
  - native editable 100% bar via bar_chart(mode="percent"); the factory
    auto-normalizes the fed percentages, so geometry stays a true 100% bar and
    the centered native labels read as the same percentages
  - a "caveat" segment (U00) drawn as a hatched pattern fill at the right end,
    visually NOT a ship-system group
  - hiding the native label on a too-thin segment (Other mapped, 4.5%) and
    letting the left reference table carry its value instead
  - a span bracket (connector ticks + caption) under the bar to reconcile
    "share of total HII DDG" with "share of SWBS-mapped" — derived from the data
    so the bracket boundary tracks the mapped fraction
  - fleet_overview-style KPI cards translating the chart into the four numbers
    that are the actual takeaway
  - a right-hand commentary rail (vocc_performance idiom): a single-cell title
    band (bottom rule matches the LHS table header), then bold section heads
    each over a bulleted
    full-sentence read (offshore_1 register) of what the mapped dollars buy

DENOMINATOR NOTE (the load-bearing caveat on this slide)
  Segment percentages (27.9 / 27.6 / 22.6 / 4.5 / 17.3) are shares of TOTAL HII
  DDG dollars, INCLUDING U00. The "94.9% in 500/200/300" KPI is a share of
  SWBS-MAPPED dollars only (denominator excludes U00). On a single 100% bar the
  three big groups sum to ~78% of the whole; they only reach ~95% once U00 is
  removed. The under-bar bracket exists to make that denominator switch explicit.

SOURCE NOTE
  Built directly as a native factory slide (no source chart-part transcription).
  Bar values are the SWBS-group shares of the $3.96B HII-Ingalls base; dollars in
  the left table are the observed-subaward figures in constant FY2026 dollars.
  Edit the Sources() string + breadcrumb to match the parent deck.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, Sources, IN, PT, bar_chart, body_slide, connector, graphic_frame,
    paragraph, run, table, tcell, text_box, trow,
)


# ── House colors (hex lives in the module; no shared palette) ───────────────
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_RULE = "808080"
GRAY_LINE = "BFBFBF"
GRAY_1 = "F2F2F2"
GRAY_SWATCH_U00 = "D9D9D9"
FONT = "Arial"

# SWBS-group ramp: a blue family for the three dominant ship-system groups, silver
# for the residual mapped bucket, and a hatch (not a solid) for the U00 caveat.
AUX_BLUE = "364D6E"        # 500 Auxiliary Systems
PROP_TEAL = "007770"       # 200 Propulsion Plant
ELEC_SLATE = "4C6C9C"      # 300 Electric Plant
OTHER_SILVER = "C0C0C0"    # Other mapped groups
SOFT_BLUE = "CEDDEC"       # pale callout fill
NEGATIVE_RED = "C00000"

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Semantic data records. The native chart, the left reference table, and the
# under-bar bracket all read from SWBS_GROUPS so they cannot desynchronize.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class SwbsGroup:
    """One bottom-to-top (left-to-right) segment of the 100% HII DDG bar."""

    name: str            # legend / table label
    dollars_m: float     # observed subaward $M (constant FY2026$)
    pct_of_hii: float    # share of the $3.96B HII base (incl. U00 in denominator)
    fill: str            # solid bar color
    mapped: bool         # True = a real SWBS ship-system group; False = U00 caveat
    on_bar_label: bool   # draw the native on-bar % label (off for thin segments)
    hatched: bool = False  # draw a pattern fill instead of a solid (U00)


# Order = descending dollars, with the U00 caveat pinned last (right end of bar).
SWBS_GROUPS: tuple[SwbsGroup, ...] = (
    SwbsGroup("500 Auxiliary Systems", 1_105.6, 27.9, AUX_BLUE, True, True),
    SwbsGroup("200 Propulsion Plant", 1_093.6, 27.6, PROP_TEAL, True, True),
    SwbsGroup("300 Electric Plant", 895.8, 22.6, ELEC_SLATE, True, True),
    SwbsGroup("Other mapped groups", 177.9, 4.5, OTHER_SILVER, True, False),
    SwbsGroup("U00 — No SWBS evidence", 684.4, 17.3, GRAY_SWATCH_U00, False, True, hatched=True),
)

HII_BASE_M = sum(g.dollars_m for g in SWBS_GROUPS)            # ≈ 3,957.3  ($3.96B)
MAPPED_M = sum(g.dollars_m for g in SWBS_GROUPS if g.mapped)  # ≈ 3,272.9  ($3.27B)
MAPPED_FRACTION = MAPPED_M / HII_BASE_M                       # ≈ 0.827


@dataclass(frozen=True)
class Kpi:
    """One top-row big-number card."""

    value: str
    value_color: str
    caption: str


KPIS: tuple[Kpi, ...] = (
    Kpi("$4.03B", BLACK, "Observed DDG-51 subawards across all primes (constant FY2026$)"),
    Kpi("$3.96B", BLACK, "HII-Ingalls base — 98.2% of all observed DDG dollars"),
    Kpi("82.7%", BLACK, "of HII-Ingalls dollars map to a SWBS ship-system group"),
    Kpi("94.9%", BLACK, "of mapped dollars sit in Auxiliary · Propulsion · Electric Plant"),
)


@dataclass(frozen=True)
class RailSection:
    """One block of the right-hand commentary rail: a group-colored head + a short
    qualifier, then one full-sentence read of what the mapped dollars buy. The head
    color IS the parent group's bar fill, so the rail ties back to the bar exactly
    as the old subsystem-table chips did."""

    head: str               # e.g. "500 Auxiliary Systems"
    head_fill: str          # the group's bar color (tie-back; unused while heads render black)
    qualifier: str          # short italic-gray phrase after the head
    point: str              # the full-sentence interpretation (figures inline)
    parenthetical: str | None = None  # optional muted (…) caveat, offshore_1 style


# Order matches the bar / left reference table (descending group dollars) so the
# rail reads column-for-column with the exhibit beside it. The dollar figures are
# subsystem-cluster subtotals from the SWBS crosswalk workbook — a finer cut than
# the group totals in the left table — rounded for the read.
RAIL_SECTIONS: tuple[RailSection, ...] = (
    RailSection(
        "500 Auxiliary Systems", AUX_BLUE, "cooling, control & survivability",
        "Cooling, air-conditioning and ventilation alone run to ~$484M (~15% of "
        "mapped dollars), and steering and ship-control add ~$141M \u2014 "
        "mission-enabling equipment, not a low-tech tail.",
    ),
    RailSection(
        "200 Propulsion Plant", PROP_TEAL, "a full drivetrain",
        "The dollars resolve into a full mechanical chain \u2014 gas turbines "
        "(~$552M), then reduction gears, shafting and propulsors (~$451M) \u2014 "
        "not a single prime-mover line item.",
    ),
    RailSection(
        "300 Electric Plant", ELEC_SLATE, "Flight III power architecture",
        "Spend splits into shipset-like generation (~$468M) and a broader "
        "distribution/conversion supply chain (~$409M) \u2014 the power-and-cooling "
        "architecture that Flight III radar loads require.",
    ),
)

# Closing thesis line under the rail sections (gray italic, full sentence).
RAIL_CLOSER = ("Read this way, each dominant SWBS group is a distinct shipbuilding "
               "demand cluster — a more actionable lens than an entity-level "
               "supplier archetype.")


# ════════════════════════════════════════════════════════════════════════════
# Native editable chart. Feed the percentages directly: percent mode normalizes
# geometry to a true 100% bar, and the centered native labels (showVal) read back
# as those same percentages under the 0.0"%" format. Dollars live in the table.
# ════════════════════════════════════════════════════════════════════════════
PCT_FORMAT = '0.0"%"'

CHART_SERIES: tuple[dict, ...] = tuple(
    {
        "name": g.name,
        "values": [g.pct_of_hii],
        **({"color": g.fill} if not g.hatched else {}),
        **({"pattern": {"prst": "ltDnDiag", "fg": GRAY_RULE, "bg": WHITE}} if g.hatched else {}),
        **({} if g.on_bar_label else {"hide_labels": True}),
    }
    for g in SWBS_GROUPS
)

# Chart frame + the inner plot rectangle (fractions of the frame). Both the bar
# and the under-bar bracket are positioned from these, so the bracket boundary
# tracks the bar geometry exactly.
CHART_FRAME = (0.45, 3.05, 7.40, 0.90)            # x, y, w, h (inches)
PLOT_FRAC = {"x": 0.012, "y": 0.04, "w": 0.976, "h": 0.92}

# House idiom: 100% bar = mode="stacked" with pct values that already sum to ~100
# (no library chart uses mode="percent"). value_axis_max == the pct total makes
# the bar fill the plot exactly, so the under-bar denominator bracket (pinned to
# MAPPED_FRACTION across PLOT_L..PLOT_R) stays aligned with the mapped/U00 seam.
_PCT_TOTAL = round(sum(g.pct_of_hii for g in SWBS_GROUPS), 1)   # 99.9

CHART_STYLE = {
    "mode": "stacked",
    "categories": ["HII-Ingalls DDG"],
    "series": [dict(s) for s in CHART_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_gridlines": False,
    "show_value_labels": True,
    "value_axis_format": PCT_FORMAT,
    "value_label_format": PCT_FORMAT,
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "value_axis_min": 0,
    "value_axis_max": _PCT_TOTAL,
    "value_axis_major_unit": 25,
    "gap_width": 40,                 # thin gap = chunky single bar
    "seg_line_color": "000000",      # thin black dividers (freight_charges 100%-mix idiom)
    "seg_line_width": 3_175,         # 0.25pt
    "axis_line_color": "162029",     # visible dark category baseline (house)
    "value_axis_line_color": "none",  # value axis hidden
    "plot_layout": dict(PLOT_FRAC),
    "cat_header": "HII-Ingalls DDG base",
}

CHARTS = [bar_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata + text-fit precedents (inspectable by a future agent).
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "market_mapping / swbs_dollar_mix",
    "use_when": (
        "Use to lead with a single dollar base decomposed into a few ship-system "
        "groups: KPI row on top, one 100% bar, a left audit table, a right "
        "commentary rail, and a bracket reconciling share-of-total vs "
        "share-of-mapped."
    ),
    "teaches": [
        "native 100% bar via bar_chart(mode='percent') with fed percentages",
        "hatched pattern-fill caveat segment (U00) pinned to the bar's right end",
        "hide_labels on a too-thin segment; defer its value to the table",
        "data-derived span bracket reconciling two denominators",
        "fleet_overview KPI cards as the real headline",
        "right commentary rail (vocc idiom): single-cell title band + bold heads "
        "over bulleted full-sentence reads (offshore_1 register), one table total",
    ],
}

TEXT_FIT = {
    "kpi_cards": {
        "box_in": (2.85, 1.00),
        "font_pt": "24 value / 10 caption",
        "content": "one short money/percent token + a one-clause caption",
    },
    "swbs_reference_table": {
        "box_in": (7.30, 1.45),
        "font_pt": 10,
        "content": "header + five SWBS-group rows (swatch · group · $M · % of HII)",
    },
    "commentary_rail": {
        "box_in": (4.78, 2.90),
        "font_pt": "10 body / 10 bold head / 9 italic closer (all black)",
        "content": "single-cell title band (rule matches LHS header) + three bold heads, "
                   "over one bulleted full-sentence read, then a closing line",
        "copy_when": "the bar + left table carry the evidence and the rail "
                     "interprets what the mapped dollars buy (vocc rail layout, "
                     "offshore_1 full-sentence register)",
    },
    "bracket_captions": {
        "box_in": [(5.97, 0.42), (1.25, 0.42)],
        "font_pt": 9,
        "content": "mapped-span reconciliation caption + U00 caveat caption",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small geometry helper + sequential shape ids.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU at the primitive call site."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


class ShapeIds:
    """Tiny sequential id allocator (chrome owns its own fixed ids)."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        v = self._next
        self._next += 1
        return v


# ── Layout zones (inches) ───────────────────────────────────────────────────
KPI_Y, KPI_W, KPI_H, KPI_STEP = 1.66, 2.85, 1.00, 3.105
KPI_XS = (0.495, 0.495 + KPI_STEP, 0.495 + 2 * KPI_STEP, 0.495 + 3 * KPI_STEP)

CHART_TITLE = Box(0.495, 2.84, 7.30, 0.20)
BRACKET_Y = 4.02            # bracket rule sits just under the bar bottom (3.95)
BRACKET_CAP_Y = 4.09
TICK_H = 0.052

SWBS_TABLE = Box(0.495, 4.66, 7.30, 1.46)

# Right commentary rail: a single-cell title band (bottom border matches the LHS header, vocc
# rail-header idiom) over a no-fill body. The band sits in the chart-title region;
# the body runs down so its foot aligns with the left reference table (≈ 6.12in).
RAIL_HEADER = Box(8.05, 2.80, 4.78, 0.30)
RAIL_BODY = Box(8.05, 3.18, 4.78, 2.90)

# SWBS reference-table column widths (EMU; sum ≈ 7.30in).
SWBS_COLS = [IN(0.32), IN(3.40), IN(1.78), IN(1.80)]


# Derived plot geometry (inches) — used to place the under-bar span bracket so it
# tracks the bar's mapped/U00 boundary.
_fx, _fy, _fw, _fh = CHART_FRAME
PLOT_L = _fx + PLOT_FRAC["x"] * _fw
PLOT_W = PLOT_FRAC["w"] * _fw
MAPPED_BOUNDARY = PLOT_L + MAPPED_FRACTION * PLOT_W
PLOT_R = PLOT_L + PLOT_W


# ════════════════════════════════════════════════════════════════════════════
# Local table kit: content first, mechanics (insets / borders / spans) second.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict:
    """One native-table border edge (12_700 EMU = 1pt)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the sides drawn; omitted sides render no-fill."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45_720, r_ins=45_720, t_ins=27_432, b_ins=27_432, **edges):
    """tcell with house defaults; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ════════════════════════════════════════════════════════════════════════════
# Tiny authoring helpers.
# ════════════════════════════════════════════════════════════════════════════
def _textbox(ids: ShapeIds, name: str, box: Box, paras, **kwargs) -> str:
    return text_box(ids.next(), name, *box.emu(), paras, **kwargs)


def _line(text, *, size=PT(10), bold=False, italic=False, color=BLACK, align=None):
    return paragraph(
        [run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align, mar_l=0, indent=0, line_spacing=100_000,
    )


def _money(m: float) -> str:
    """$M as the slide reads it: '$1,105.6M'."""
    return f"${m:,.1f}M"


def _pct(p: float) -> str:
    return f"{p:.1f}%"


# ════════════════════════════════════════════════════════════════════════════
# Paint functions (order = the slide's z-order: chart, then overlays).
# ════════════════════════════════════════════════════════════════════════════
def paint_chart(out: list[str], ids: ShapeIds) -> None:
    """Editable 100% bar + its external one-line title."""
    out.append(graphic_frame(
        sp_id=ids.next(), name="SwbsMixChart",
        x=IN(_fx), y=IN(_fy), cx=IN(_fw), cy=IN(_fh), rId="rId2",
    ))
    out.append(_textbox(
        ids, "ChartTitle", CHART_TITLE,
        [paragraph(
            [run("HII-Ingalls DDG-51 observed subawards by SWBS group ", size=PT(10), bold=True, color=BLACK, font=FONT),
             run("(% of the $3.96B HII base; segment % of total incl. U00)", size=PT(10), color=GRAY_RULE, font=FONT)],
            mar_l=0, indent=0, line_spacing=100_000)],
        fill=None, line_color="none", anchor="b", wrap="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))


def paint_kpis(out: list[str], ids: ShapeIds) -> None:
    """Top-row big-number cards — the four numbers that are the takeaway."""
    for kpi, x in zip(KPIS, KPI_XS):
        out.append(_textbox(
            ids, "KpiCard", Box(x, KPI_Y, KPI_W, KPI_H),
            [
                paragraph([run(kpi.value, size=PT(24), bold=True, color=kpi.value_color, font=FONT)],
                          align="ctr", line_spacing=100_000, space_after=300),
                paragraph([run(kpi.caption, size=PT(10), color=BLACK, font=FONT)],
                          align="ctr", line_spacing=104_000),
            ],
            fill=GRAY_1, line_color="none", anchor="ctr",
            l_ins=63_500, r_ins=63_500, t_ins=36_576, b_ins=36_576,
            effects=CALLOUT_SHADOW,
        ))


def paint_denominator_bracket(out: list[str], ids: ShapeIds) -> None:
    """The load-bearing caveat: a span bracket reconciling share-of-total with
    share-of-mapped. Mapped span sits under segments 1-4; U00 under segment 5."""
    # Mapped span rule + end ticks. Ticks rise from the rule UP toward the bar
    # (negative cy -> connector normalizes to a positive box + flipV), so the
    # bracket embraces the bar above it rather than hanging toward the caption.
    out.append(connector(ids.next(), "MappedBracketRule",
                         IN(PLOT_L), IN(BRACKET_Y), IN(MAPPED_BOUNDARY - PLOT_L), 0,
                         color=GRAY_RULE, width=9_525))
    out.append(connector(ids.next(), "MappedTickL",
                         IN(PLOT_L), IN(BRACKET_Y), 0, IN(-TICK_H),
                         color=GRAY_RULE, width=9_525))
    out.append(connector(ids.next(), "MappedTickR",
                         IN(MAPPED_BOUNDARY), IN(BRACKET_Y), 0, IN(-TICK_H),
                         color=GRAY_RULE, width=9_525))
    out.append(_textbox(
        ids, "MappedBracketCaption",
        Box(PLOT_L, BRACKET_CAP_Y, MAPPED_BOUNDARY - PLOT_L, 0.42),
        [paragraph(
            [run("SWBS-mapped: 82.7% of HII DDG ($3.27B) — ", size=PT(9), bold=True, color=DK, font=FONT),
             run("94.9% of mapped sits in Auxiliary · Propulsion · Electric Plant", size=PT(9), color=DK, font=FONT)],
            align="ctr", line_spacing=104_000)],
        fill=None, line_color="none", anchor="t",
        l_ins=18_288, r_ins=18_288, t_ins=18_288, b_ins=0,
    ))
    # U00 span rule + end ticks + caveat caption.
    out.append(connector(ids.next(), "U00BracketRule",
                         IN(MAPPED_BOUNDARY), IN(BRACKET_Y), IN(PLOT_R - MAPPED_BOUNDARY), 0,
                         color=GRAY_LINE, width=9_525))
    out.append(connector(ids.next(), "U00TickR",
                         IN(PLOT_R), IN(BRACKET_Y), 0, IN(-TICK_H),
                         color=GRAY_LINE, width=9_525))
    out.append(_textbox(
        ids, "U00BracketCaption",
        Box(MAPPED_BOUNDARY, BRACKET_CAP_Y, PLOT_R - MAPPED_BOUNDARY, 0.42),
        [_line("U00: 17.3%", size=PT(9), bold=True, color=GRAY_RULE, align="ctr"),
         _line("no SWBS evidence", size=PT(9), italic=True, color=GRAY_RULE, align="ctr")],
        fill=None, line_color="none", anchor="t",
        l_ins=9_144, r_ins=9_144, t_ins=18_288, b_ins=0,
    ))


def paint_swbs_table(out: list[str], ids: ShapeIds) -> None:
    """Left reference table: swatch · SWBS group · observed $M · % of HII DDG.
    This is the auditable record; the bar is the glance read."""
    rows = [trow([
        cell("", B=edge(DK)),
        cell("SWBS group", bold=True, B=edge(DK)),
        cell("Observed $M", bold=True, align="r", B=edge(DK)),
        cell("% of HII DDG", bold=True, align="r", B=edge(DK)),
    ], h=IN(0.28))]
    for i, g in enumerate(SWBS_GROUPS):
        last = i == len(SWBS_GROUPS) - 1
        rule = None if last else edge(GRAY_LINE, 6_350)
        italic = not g.mapped
        rows.append(trow([
            cell("", fill=g.fill, B=rule),
            cell(g.name, italic=italic or None, color=(GRAY_RULE if italic else BLACK), B=rule),
            cell(_money(g.dollars_m), align="r", B=rule),
            cell(_pct(g.pct_of_hii), align="r", B=rule),
        ], h=IN(0.255)))
    out.append(table(ids.next(), "SwbsReferenceTable", *SWBS_TABLE.emu(),
                     col_widths=SWBS_COLS, rows=rows))


def _rail_head(section: RailSection, first: bool) -> str:
    """Bold black head + a short italic qualifier (also black). space_before opens
    a gap above every head but the first."""
    return paragraph(
        [run(section.head, size=PT(10), bold=True, color=BLACK, font=FONT),
         run("  \u2014  ", size=PT(10), color=BLACK, font=FONT),
         run(section.qualifier, size=PT(10), italic=True, color=BLACK, font=FONT)],
        mar_l=0, indent=0, line_spacing=104_000,
        space_before=(0 if first else 700), space_after=100,
    )


def _rail_point(section: RailSection) -> str:
    """One bulleted full-sentence read (offshore_1 register): figures inline, with
    an optional muted parenthetical caveat trailing the claim."""
    runs = [run(section.point, size=PT(10), color=BLACK, font=FONT)]
    if section.parenthetical:
        runs.append(run(" " + section.parenthetical, size=PT(10), italic=True,
                        color=BLACK, font=FONT))
    return paragraph(runs, bullet=True, mar_l=171_450, indent=-171_450,
                     line_spacing=104_000)


def paint_rail(out: list[str], ids: ShapeIds) -> None:
    """Right commentary rail: the bar + left table carry the evidence; this rail
    interprets what the mapped dollars buy. vocc_performance rail layout (single-
    cell title band, then a no-fill body), offshore_1 full-sentence register."""
    # Title band: a single-cell table whose bottom border matches the left
    # reference-table header rule (edge(DK), 1pt). Cell left inset matches the body
    # text-box inset so the title aligns with the heads below; the border spans the
    # full rail width.
    out.append(table(
        ids.next(), "RailHeader", *RAIL_HEADER.emu(),
        col_widths=[IN(RAIL_HEADER.w)],
        rows=[trow([cell("What the mapped dollars are buying", bold=True,
                         l_ins=91_440, B=edge(DK))],
                   h=IN(RAIL_HEADER.h))],
    ))
    # Rail body: head + bulleted full-sentence read per section, then the closer.
    paras: list[str] = []
    for i, section in enumerate(RAIL_SECTIONS):
        paras.append(_rail_head(section, first=(i == 0)))
        paras.append(_rail_point(section))
    paras.append(paragraph(
        [run(RAIL_CLOSER, size=PT(9), italic=True, color=BLACK, font=FONT)],
        mar_l=0, indent=0, line_spacing=104_000, space_before=900,
    ))
    out.append(_textbox(ids, "CommentaryRail", RAIL_BODY, paras,
                        fill=None, line_color="none", anchor="t"))


# Reference drop-shadow on the KPI cards (verbatim source params: 0.056" blur,
# 0.03" offset down-right, black @ 40% alpha).
CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/>'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds()
    paint_chart(out, ids)
    paint_kpis(out, ids)
    paint_denominator_bracket(out, ids)
    paint_swbs_table(out, ids)
    paint_rail(out, ids)
    return "".join(out)


CHROME = Chrome(
    section="DDG-51 Subaward Mapping",
    topic="SWBS Dollar Mix",
    title="DDG-51 SWBS Dollar Mix",
    takeaway=("82.7% of observed HII-Ingalls dollars map to SWBS; 94.9% of mapped "
              "concentrate in Auxiliary, Propulsion, and Electric Plant."),
    sources=Sources(
        source="Project subaward workbook; USAspending.gov subaward records; SWBS ship-system crosswalk",
        note=("HII-Ingalls observed DDG-51 subawards, constant FY2026$; SWBS coverage = "
              "non-U00 dollars / total HII DDG dollars"),
    ),
)


def render() -> str:
    return body_slide(CHROME, _body())
