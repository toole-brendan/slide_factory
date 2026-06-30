"""DDG-51 vendor SWBS fingerprint: dollar-vs-count asymmetry + auditable vendor table.

ROLE
  share_asymmetry_comparison / vendor_evidence_fingerprint

USE WHEN
  A slide must show that a coverage metric is weak head-count-weighted but strong
  dollar-weighted, then back it with a dense, sortable vendor table whose evidence
  class doubles as the chart key. Two aligned 100% bars carry the asymmetry; the
  table makes it auditable; a pale-blue callout adds the incumbency context.

TEACHES
  - two separate native stacked bars (one category each) read as a paired
    100% comparison, with shared class colors and a shared manual legend
  - the library all-manual label idiom (freight_charges): native data labels are
    OFF (they char-wrap inside a thin bar), so the two dominant segments are
    hand-painted as % labels (uniform 1 decimal) — white on the dark HC navy,
    dark on the light Low/no gray
  - the two thin Mixed/Partial slivers get a small color-matched value chip just off
    the bar (Mixed above, Partial below), joined to the sliver by a short neutral
    leader line (ships_act_captive_demand thin-segment idiom)
  - a full-width vendor reference table (key_inputs / coordination_archetypes kit)
    whose Evidence-class cell is a colored chip matching the bar segments
  - flagging one worked-example row (SOCAIL, LDA) and footnoting it
  - keeping a separate-denominator finding (the FY23-27 MYP incumbency block) in a
    visually separate callout so it is not read against the 375-vendor base

TEXT-FIT PRECEDENT
  fingerprint_table:
    geometry: 12.340in wide x 2.730in high
    columns: 2.85 / 1.15 / 1.35 / 2.05 / 1.25 / 2.49 / 1.20 in
    type: Arial 10pt, single-spaced; header + 12 data rows at ~0.21in row pitch
    copy_when: a slide needs a dense vendor catalogue under a compact exhibit, and
               every row must be traceable to a vendor, a primary ship system, and
               an evidence class without leaving the slide
  share_bars:
    geometry: each bar frame 7.20in wide x 0.36in high; plot fills the frame so a
              segment's slide-x equals frame_x + cumulative_share * frame_w
    note: thin Mixed/Partial slivers (1-4%) cannot hold an in-bar label, so each
          gets a small color-matched value chip just off the bar with a short
          leader; the wide HC / Low-no segments carry hand-painted in-bar % labels.

SOURCE NOTE
  Built from the DDG-51 SWBS market-mapping write-up. Base = HII-Ingalls DDG
  subaward transactions, constant FY2026 dollars. The four-class vendor split
  (counts, $M, shares) and the FY23-27 MYP incumbency figures come from that
  write-up; the vendor-count shares are derived from the counts over the 375-vendor
  HII DDG base. The top-12 vendor rows are from the DDG Subaward Transactions table
  filtered to Builder = HII-Ingalls.

FIDELITY NOTE
  Charts are native editable bar_chart(mode="percent") factories, so data, colors,
  and axes are inspectable in Python and "Edit Data" stays live in PowerPoint.
  Thin-segment chip/leader positions are computed from the cumulative shares and an
  explicit full-frame plot_layout; if a renderer nudges the plot inset, the chip x
  values (see _share_x) are the single place to adjust.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, Sources, bar_chart, body_slide, connector, graphic_frame,
    paragraph, run, table, tcell, text_box, trow,
)


# ── House colors (hex lives in the module; no shared palette) ───────────────
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
FONT = "Arial"

RULE_GRAY = "808080"
GRIDLINE_W = 6_350
HAIRLINE = "808080"

# Evidence-class ramp: dark house blue -> pale blue -> gray. Low/no evidence is
# the caveat color (gray), matching the U00 treatment on the SWBS-mix slide.
CLASS_HC      = "1D4D68"   # High-confidence single SWBS  (dark navy; white labels)
CLASS_MIXED   = "4C6C9C"   # High-coverage mixed          (recurring mid chart blue; white labels)
CLASS_PARTIAL = "9DB1CF"   # Partial SWBS evidence        (recurring light chart blue; dark labels)
CLASS_LOWNO   = "BFBFBF"   # Low / no SWBS evidence        (caveat gray; dark labels)

CALLOUT_BLUE  = "CEDDEC"   # pale-blue incumbency note fill
SOCAIL_FILL   = "EAF1F8"   # very pale row highlight for the worked-example row

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Class model: one record drives both the bars and the legend.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class SwbsClass:
    key: str
    label: str           # legend / chip text
    color: str
    vendors: int
    dollars_m: float
    dollar_share: float  # % of HII DDG $
    count_share: float   # % of 375 vendors (derived)
    dominant: bool       # wide enough to hold an in-bar native label


# 77 / 5 / 14 / 279 vendors of 375; $ shares from the write-up; count shares
# derived (e.g., 77/375 = 20.5%). Order is bottom->top of the stack = left->right
# of the horizontal bar.
SWBS_CLASSES: tuple[SwbsClass, ...] = (
    SwbsClass("hc",      "High-confidence single SWBS", CLASS_HC,      77, 3_122.8, 78.9, 20.5, True),
    SwbsClass("mixed",   "High-coverage mixed",         CLASS_MIXED,    5,   112.1,  2.8,  1.3, False),
    SwbsClass("partial", "Partial SWBS evidence",       CLASS_PARTIAL, 14,   146.6,  3.7,  3.7, False),
    SwbsClass("lowno",   "Low / no SWBS evidence",      CLASS_LOWNO,  279,   575.8, 14.6, 74.4, True),
)

TOTAL_VENDORS = sum(c.vendors for c in SWBS_CLASSES)        # 375
TOTAL_DOLLARS_B = sum(c.dollars_m for c in SWBS_CLASSES) / 1000.0  # ~3.96


# ════════════════════════════════════════════════════════════════════════════
# Native charts: two single-category percent-stacked bars.
# ════════════════════════════════════════════════════════════════════════════
def _bar_series(value_attr: str) -> list[dict]:
    """One series per class. Value labels are hand-painted in paint_bars (native
    labels are off), so each series carries only name + color + value."""
    return [{"name": c.label, "color": c.color, "values": [getattr(c, value_attr)]}
            for c in SWBS_CLASSES]


def _percent_bar(value_attr: str, cat_header: str) -> dict:
    # House idiom: a 100% bar is mode="stacked" with values that already sum to
    # ~100 (no library chart uses mode="percent"). Setting value_axis_max to the
    # series total makes the stacked bar fill the frame exactly, so _share_x (which
    # normalizes by the same total) places the hand-painted segment labels on the
    # right segments. Native data labels are OFF — they char-wrap inside a 0.36in
    # bar; we paint them ourselves (freight_charges all-manual-label idiom).
    total = round(sum(getattr(c, value_attr) for c in SWBS_CLASSES), 1)
    return bar_chart(
        mode="stacked",
        categories=["Share"],
        series=_bar_series(value_attr),
        show_legend=False,
        show_cat_labels=False,
        show_value_axis_labels=False,
        show_gridlines=False,
        show_value_labels=False,
        value_axis_format="General",
        value_axis_min=0,
        value_axis_max=total,
        value_axis_major_unit=25,
        gap_width=20,                 # one category; small gap -> bar fills the frame
        bar_overlap=100,
        seg_line_color="000000",      # thin black dividers (freight_charges 100%-mix idiom)
        seg_line_width=3_175,         # 0.25pt
        axis_line_color="162029",     # visible dark category baseline (house)
        value_axis_line_color="none",
        plot_layout={"x": 0.0, "y": 0.0, "w": 1.0, "h": 1.0},  # plot fills frame
        cat_header=cat_header,
    )


# CHARTS order fixes the rIds: vendors -> rId2, dollars -> rId3.
CHARTS = [
    _percent_bar("count_share", "Vendor share"),
    _percent_bar("dollar_share", "Dollar share"),
]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "share_asymmetry_comparison",
    "use_when": (
        "Use for a 'weak by count, strong by dollars' coverage story: two aligned "
        "100% bars over an auditable reference table, with the table's class column "
        "as the shared color key."
    ),
    "teaches": [
        "two separate native stacked bars as a paired 100% comparison",
        "all-manual value labels (native labels off) per the freight_charges idiom",
        "hand-painted dominant labels in-bar; thin slivers get color chips + short leaders",
        "full-width vendor table with class-colored chip cells",
        "worked-example row highlight + footnote",
        "separate-denominator finding isolated in a callout",
    ],
}


# ════════════════════════════════════════════════════════════════════════════
# Geometry (inches; -> EMU at the last moment).
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        v = self._next
        self._next += 1
        return v


# Bars: category label on the left, bar frame to the right, legend further right.
BAR_X, BAR_W, BAR_H = 2.40, 7.20, 0.36       # thicker frame -> chunkier bar, centered % reads
BAR1_Y, BAR2_Y = 1.62, 2.34                  # vendors (top), dollars (bottom); bar2 raised for the thicker bar
CAT_LABEL = Box(0.50, 0.00, 1.78, 0.30)      # x/w fixed; y set per bar

LEGEND_X, LEGEND_W = 9.95, 2.85
LEGEND_Y0, LEGEND_DY = 1.55, 0.30
LEGEND_SWATCH = Box(0.0, 0.0, 0.17, 0.13)    # w/h only

# Table height is DERIVED from explicit single-line row heights so the callout
# can be pinned just below the real table bottom (no wraps now, so these minima
# are the actual heights). Mirrors the hull slide's derive-table-h-from-rows idiom.
HEADER_H = 0.24
ROW_H = 0.22
N_DATA_ROWS = 12
TABLE_H = HEADER_H + N_DATA_ROWS * ROW_H        # 2.88in
CALLOUT_GAP = 0.09

TABLE = Box(0.495, 3.05, 12.340, TABLE_H)
CALLOUT = Box(0.495, TABLE.y + TABLE_H + CALLOUT_GAP, 12.340, 0.40)  # ends ~6.42, clears the sources band

# Hand-painted in-bar value-label width (wrap="none", centered on the segment).
DOM_LABEL_W = 0.95
# Thin Mixed/Partial sliver value chips + short neutral leader (ships_act idiom).
# Canonical library label height = 0.167in. 0.08in reads like a tick; 0.14in reads
# like an intentional leader (and still clears the table: lower chip bottom ~3.01in
# vs table top 3.05in). Do not exceed ~0.16in without moving the table/chart.
THIN_TAG_W, THIN_TAG_H = 0.42, 0.167
THIN_LEADER_LEN = 0.14
LEADER_COLOR = "44505C"
LEADER_W = 6_350          # 0.5pt; keep thin / neutral
TAG_INS = 17_463


# ════════════════════════════════════════════════════════════════════════════
# Vendor table data (top 12 HII DDG vendors by dollars).
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class VendorRow:
    vendor: str
    dollars_m: str
    coverage: str
    primary_group: str
    primary_pct: str
    top_subsystem: str
    evidence: str          # one of the four class labels (drives chip color)
    worked_example: bool = False


VENDOR_ROWS: tuple[VendorRow, ...] = (
    VendorRow("Rolls-Royce Marine North America", "541.5", "98%", "300 Electric Plant",    "85%",  "310 Electric power generation",           "High-confidence single SWBS"),
    VendorRow("General Electric",                 "348.6", "100%", "200 Propulsion Plant",  "100%", "234 Propulsion gas turbines",             "High-confidence single SWBS"),
    VendorRow("York International",               "243.5", "88%",  "500 Auxiliary Systems", "88%",  "516 Refrigeration system",                "High-confidence single SWBS"),
    VendorRow("SOCAIL, LDA",                      "204.5", "100%", "200 Propulsion Plant",  "100%", "234 Propulsion gas turbines",             "High-confidence single SWBS", worked_example=True),
    VendorRow("Timken Gears & Services",          "174.5", "100%", "200 Propulsion Plant",  "100%", "241 Propulsion reduction gears",          "High-confidence single SWBS"),
    VendorRow("Johnson Controls Navy Systems",    "160.2", "99%",  "500 Auxiliary Systems", "99%",  "516 Refrigeration system",                "High-confidence single SWBS"),
    VendorRow("Northrop Grumman Systems",         "146.3", "93%",  "500 Auxiliary Systems", "90%",  "561 Steering and diving control systems", "High-confidence single SWBS"),
    VendorRow("L-3 Communications Westwood",      "118.6", "95%",  "300 Electric Plant",    "95%",  "324 Switchgear and panels",               "High-confidence single SWBS"),
    VendorRow("DRS Naval Power Systems",          "115.6", "97%",  "300 Electric Plant",    "97%",  "324 Switchgear and panels",               "High-confidence single SWBS"),
    VendorRow("Ellwood National Forge",           "98.6",  "100%", "200 Propulsion Plant",  "100%", "243 Propulsion shafting",                 "High-confidence single SWBS"),
    VendorRow("Engineered Coil",                  "83.4",  "95%",  "500 Auxiliary Systems", "95%",  "555 Fire extinguishing systems",          "High-confidence single SWBS"),
    VendorRow("Espey Mfg. & Electronics",         "56.1",  "84%",  "300 Electric Plant",    "84%",  "314 Power conversion equipment",          "High-confidence single SWBS"),
)

COL_W = (2.70, 1.15, 1.35, 2.05, 1.25, 2.64, 1.20)   # sums to 12.34
# Vendor col trimmed 2.85->2.70 (widest entry ~2.12in) and Top-subsystem col
# widened 2.49->2.64 so "561 Steering and diving control systems" (~2.45in) no
# longer wraps to a second line and inflates the table height into the callout.
HEADERS = ("Vendor", "DDG HII $M", "SWBS coverage", "Primary SWBS group",
           "Primary SWBS %", "Top SWBS subsystem", "Evidence class")
# Right-aligned numeric columns by index.
RIGHT_COLS = {1, 2, 4}

# Map a class label to its ramp color for the table chip.
CLASS_COLOR_BY_LABEL = {c.label: c.color for c in SWBS_CLASSES}


# ════════════════════════════════════════════════════════════════════════════
# Local table kit (inline by design; mirrors key_inputs / coordination).
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict:
    return {"color": color, "width": w}


def border_dict(**edges):
    return {k: v for k, v in edges.items() if v is not None} or None


def cell(text, *, fill=None, bold=None, color=BLACK, align="l", size=PT(10),
         t_ins=22_860, b_ins=22_860, l_ins=45_720, r_ins=45_720, **edges):
    return tcell(text, fill=fill, bold=bold, color=color, align=align, size=size,
                 anchor="ctr", font=FONT, l_ins=l_ins, r_ins=r_ins,
                 t_ins=t_ins, b_ins=b_ins, borders=border_dict(**edges))


def chip_cell(label, *, t_ins=18_000, b_ins=18_000, **edges):
    """Evidence-class chip: class-colored fill, white text, doubles as the key."""
    fill = CLASS_COLOR_BY_LABEL.get(label, CLASS_LOWNO)
    txt = WHITE if fill in (CLASS_HC, CLASS_MIXED) else BLACK
    # Shorten the printed chip text; full names live in the legend.
    short = {"High-confidence single SWBS": "High-confidence",
             "High-coverage mixed": "Mixed",
             "Partial SWBS evidence": "Partial",
             "Low / no SWBS evidence": "Low / no"}.get(label, label)
    return tcell(short, fill=fill, bold=True, color=txt, align="ctr", size=PT(9),
                 anchor="ctr", font=FONT, l_ins=18_000, r_ins=18_000,
                 t_ins=t_ins, b_ins=b_ins, borders=border_dict(**edges))


# ════════════════════════════════════════════════════════════════════════════
# Chart-zone helpers.
# ════════════════════════════════════════════════════════════════════════════
def _r(text, *, size=PT(10), bold=False, italic=False, color=BLACK):
    return run(text, size=size, bold=bold or None, italic=italic or None,
               color=color, font=FONT)


def _tight(paras_runs, *, align="l"):
    return paragraph(paras_runs, align=align, mar_l=0, indent=0, line_spacing=100_000)


def _label_box(out, ids, name, box: Box, runs, *, align="l", anchor="ctr",
               fill=None, line_color="none", wrap="square", effects=None):
    out.append(text_box(ids.next(), name, *box.emu(), [_tight(runs, align=align)],
                        fill=fill, line_color=line_color, anchor=anchor, wrap=wrap,
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0, effects=effects))


def _share_x(classes, idx: float, attr: str) -> float:
    """Slide-x (inches) of the cumulative-share point `idx` (a class index or a
    midpoint like 1.5) along a bar, given the plot fills the frame."""
    shares = [getattr(c, attr) for c in classes]
    total = sum(shares)
    whole = int(idx)
    frac = idx - whole
    cum = sum(shares[:whole]) + (shares[whole] * frac if whole < len(shares) else 0)
    return BAR_X + (cum / total) * BAR_W


def _pct(v: float) -> str:
    """Percentage label, uniform 1 decimal across the whole bar (consistent
    precision; the sub-5% slivers need the decimal, so all labels carry one)."""
    return f"{v:.1f}%"


def _chip_text_color(cls: SwbsClass) -> str:
    """White label on the dark HC/Mixed fills, dark label on the light
    Partial/Low-no fills (follow the fill brightness, not the class name)."""
    return WHITE if cls.key in {"hc", "mixed"} else DK


# ════════════════════════════════════════════════════════════════════════════
# Painters.
# ════════════════════════════════════════════════════════════════════════════
def _value_chip(out: list[str], ids: ShapeIds, *, name: str, cx: float, y: float,
                label: str, fill: str, text_color: str) -> None:
    """A chart value chip (freight_charges / ships_act idiom): a tight text_box
    overlay — no outline, centered, no wrap, small side insets, zero top/bottom
    insets, zero paragraph margins — NOT the heavier table-cell chip."""
    out.append(text_box(
        ids.next(), name,
        IN(cx - THIN_TAG_W / 2), IN(y), IN(THIN_TAG_W), IN(THIN_TAG_H),
        [_tight([_r(label, color=text_color)], align="ctr")],
        fill=fill, line_color="none", anchor="ctr", wrap="none",
        l_ins=TAG_INS, t_ins=0, r_ins=TAG_INS, b_ins=0,
    ))


def paint_bars(out: list[str], ids: ShapeIds) -> None:
    # Two graphic frames (rId2 vendors, rId3 dollars).
    out.append(graphic_frame(sp_id=ids.next(), name="VendorShareBar",
                             x=IN(BAR_X), y=IN(BAR1_Y), cx=IN(BAR_W), cy=IN(BAR_H), rId="rId2"))
    out.append(graphic_frame(sp_id=ids.next(), name="DollarShareBar",
                             x=IN(BAR_X), y=IN(BAR2_Y), cx=IN(BAR_W), cy=IN(BAR_H), rId="rId3"))

    # Left category labels (vertically centered on each bar).
    _label_box(out, ids, "VendorBarLabel", Box(CAT_LABEL.x, BAR1_Y + (BAR_H - 0.34) / 2, CAT_LABEL.w, 0.34),
               [_r("By vendor count", bold=True), run("  ", size=PT(10)),
                _r(f"(n = {TOTAL_VENDORS})", color=RULE_GRAY)], anchor="ctr")
    _label_box(out, ids, "DollarBarLabel", Box(CAT_LABEL.x, BAR2_Y + (BAR_H - 0.34) / 2, CAT_LABEL.w, 0.34),
               [_r("By DDG HII $", bold=True), run("  ", size=PT(10)),
                _r(f"(${TOTAL_DOLLARS_B:.2f}B)", color=RULE_GRAY)], anchor="ctr")

    # Hand-painted value labels on the two dominant segments (native labels are off
    # — they char-wrap in a 0.36in bar). White on the dark HC navy, dark on the
    # light Low/no gray; centered on the segment via _share_x, wrap="none".
    for bar_y, attr in ((BAR1_Y, "count_share"), (BAR2_Y, "dollar_share")):
        for idx, cls in enumerate(SWBS_CLASSES):
            if not cls.dominant:
                continue
            cx = _share_x(SWBS_CLASSES, idx + 0.5, attr)
            color = _chip_text_color(cls)
            _label_box(out, ids, f"{cls.key}Value",
                       Box(cx - DOM_LABEL_W / 2, bar_y, DOM_LABEL_W, BAR_H),
                       [_r(_pct(getattr(cls, attr)), color=color)],
                       align="ctr", anchor="ctr", wrap="none")

    # Thin Mixed/Partial slivers can't hold an in-bar label, so each gets a small
    # color-matched value chip in clear space (Mixed above, Partial below) joined to
    # the sliver by a short neutral leader — the ships_act_captive_demand thin-segment
    # idiom (chip h = 0.167in; leader 44505C @ 0.5pt). The chip fill matches the sliver.
    for bar_y, attr in ((BAR1_Y, "count_share"), (BAR2_Y, "dollar_share")):
        for idx, side in ((1, "above"), (2, "below")):
            cls = SWBS_CLASSES[idx]
            cx = _share_x(SWBS_CLASSES, idx + 0.5, attr)
            text_color = _chip_text_color(cls)
            if side == "above":
                y0 = bar_y - THIN_LEADER_LEN          # leader runs up from bar top
                ty = y0 - THIN_TAG_H                  # chip sits above the leader
            else:
                y0 = bar_y + BAR_H                    # leader runs down from bar bottom
                ty = y0 + THIN_LEADER_LEN             # chip sits below the leader
            out.append(connector(ids.next(), f"{cls.key}Leader",
                                  IN(cx), IN(y0), 0, IN(THIN_LEADER_LEN),
                                  color=LEADER_COLOR, width=LEADER_W))
            _value_chip(out, ids, name=f"{cls.key}Tag", cx=cx, y=ty,
                        label=_pct(getattr(cls, attr)), fill=cls.color, text_color=text_color)


def paint_legend(out: list[str], ids: ShapeIds) -> None:
    for i, c in enumerate(SWBS_CLASSES):
        y = LEGEND_Y0 + i * LEGEND_DY
        out.append(text_box(ids.next(), "LegendSwatch",
                            IN(LEGEND_X), IN(y + (LEGEND_DY - LEGEND_SWATCH.h) / 2),
                            IN(LEGEND_SWATCH.w), IN(LEGEND_SWATCH.h),
                            [_tight([], align="ctr")], fill=c.color, line_color=DK,
                            line_width=3_175, anchor="ctr"))
        _label_box(out, ids, "LegendLabel",
                   Box(LEGEND_X + 0.26, y, LEGEND_W - 0.26, LEGEND_DY),
                   [_r(c.label, size=PT(9), bold=True), run("   ", size=PT(9)),
                    _r(f"{_pct(c.count_share)} ct", size=PT(9), color=RULE_GRAY),
                    run(" · ", size=PT(9), color=RULE_GRAY),
                    _r(f"{_pct(c.dollar_share)} $", size=PT(9), color=RULE_GRAY)],
                   anchor="ctr", wrap="none")


def _header_row():
    cells = []
    for i, h in enumerate(HEADERS):
        align = "r" if i in RIGHT_COLS else ("ctr" if i == 6 else "l")
        cells.append(cell(h, bold=True, align=align, fill=WHITE, anchor="b",
                          B=edge(BLACK)))
    return trow(cells, h=IN(HEADER_H))


def _vendor_rows():
    rows = []
    hair = edge(HAIRLINE, GRIDLINE_W)
    n = len(VENDOR_ROWS)
    for ri, vr in enumerate(VENDOR_ROWS):
        bottom = None if ri == n - 1 else hair
        fill = SOCAIL_FILL if vr.worked_example else WHITE
        vendor_text = vr.vendor + ("¹" if vr.worked_example else "")
        cells = [
            cell(vendor_text, fill=fill, bold=vr.worked_example or None, align="l", B=bottom),
            cell(vr.dollars_m, fill=fill, align="r", B=bottom),
            cell(vr.coverage, fill=fill, align="r", B=bottom),
            cell(vr.primary_group, fill=fill, align="l", B=bottom),
            cell(vr.primary_pct, fill=fill, align="r", B=bottom),
            cell(vr.top_subsystem, fill=fill, align="l", B=bottom),
            chip_cell(vr.evidence, B=bottom),
        ]
        rows.append(trow(cells, h=IN(ROW_H)))
    return rows


def paint_table(out: list[str], ids: ShapeIds) -> None:
    out.append(table(ids.next(), "VendorFingerprintTable", *TABLE.emu(),
                     col_widths=[IN(w) for w in COL_W],
                     rows=[_header_row(), *_vendor_rows()]))


def paint_incumbency_callout(out: list[str], ids: ShapeIds) -> None:
    txt = ("FY23\u201327 MYP block (separate, recent universe): of 83 active vendors, "
           "80 continued from the prior block and only 1 was first-observed; "
           "~$996.7M of $1.18B flowed to continued (incumbent) suppliers.")
    out.append(text_box(ids.next(), "IncumbencyCallout", *CALLOUT.emu(),
                        [paragraph([_r("Recent block is incumbent-heavy:  ", bold=True),
                                    _r(txt)], align="l", line_spacing=100_000)],
                        fill=CALLOUT_BLUE, line_color=DK, line_width=9_525,
                        anchor="ctr", l_ins=91_440, r_ins=91_440, t_ins=27_432, b_ins=27_432))


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)
    # Paint order: later shapes sit on top. Table/callout first, then the chart
    # exhibit and its overlays so chips/labels are never occluded.
    paint_table(out, ids)
    paint_incumbency_callout(out, ids)
    paint_bars(out, ids)
    paint_legend(out, ids)
    return "".join(out)


CHROME = Chrome(
    section="DDG-51 Subaward Mapping",
    topic="Vendor SWBS Fingerprint",
    title="DDG-51 Supplier Fingerprint",
    takeaway=("Most vendors have limited SWBS evidence, but most dollars map cleanly "
              "to one SWBS group."),
    sources=Sources(
        source=("DDG Subaward Transactions (Builder = HII-Ingalls); constant FY2026 $"),
        note=("\u00b9 SOCAIL, LDA reads as an unresolved supplier archetype, but DDG SWBS "
              "resolves it to 234 propulsion gas turbines. "
              "Evidence class: High-confidence = \u226580% SWBS coverage and \u226570% of $ in one "
              "primary SWBS group; Mixed = \u226580% coverage, <70% concentration; "
              "Partial = 50\u201379% coverage; Low/no = <50%. Vendor-count shares are of the "
              "375-vendor HII DDG base."),
    ),
)


def render() -> str:
    return body_slide(CHROME, _body())
