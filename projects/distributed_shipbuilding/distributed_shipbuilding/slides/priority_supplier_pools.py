"""Target slide #15: Priority Supplier Pools.

Closing SAM Supplier Market Structure slide: priority matrix + rationale table.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, Box, DK, GRAY_1,
    GRAY_2, ORANGE, PALE_ORANGE, ShapeIds, WHITE, hline, label, p, paras,
    shape, vline,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="SAM Supplier Market Structure",
    topic="Priority Supplier Pools",
    title="Priority Supplier Pools",
    takeaway="The strongest first-pass pools combine observed scale, construction relevance and a plausible access route.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/where_to_play.py",
            "workbook_factory/ddg/sheets/domain_concentration.py",
            "workbook_factory/ddg/sheets/supplier_year_activity.py",
            "workbook_factory/ddg/docs/ddg_sam_model_goals.md",
        ),
        note="Priority labels are a screen for diligence sequencing; final prioritization should use rendered workbook values and supplier-level review.",
    ),
)

POOLS = [
    ("Machinery / power / fluid equipment", "D2-D5 × P3", 7.05, 2.35, BLUE_4, "Scale + recurring equipment"),
    ("Mission / combat configured systems", "D6-D7 × P4", 6.45, 4.00, BLUE_5, "Strategic but control-sensitive"),
    ("Hull / outfitted modules", "D1 × P5", 4.35, 4.28, BLUE_3, "Construction-critical"),
    ("Precision parts / materials", "D8-D9 × P1-P2", 3.65, 2.68, BLUE_2, "Fragmented diligence lane"),
    ("Services / technical support", "D11 × P6", 5.12, 1.88, GRAY_2, "Useful, less hardware leverage"),
]

TABLE_ROWS = [
    ("1", "Machinery / power / fluid equipment", "High", "Medium", "Prioritize OEMs and recurring equipment suppliers; verify parent concentration and retention."),
    ("2", "Mission / combat configured systems", "High", "Low-Med", "Strategic pool; likely partnership or long-cycle lane when parent control is tight."),
    ("3", "Hull / outfitted modules", "Medium", "Medium", "Construction-critical but evidence must distinguish parts, modules and prime-retained work."),
    ("4", "Precision parts / materials", "Medium", "Medium-High", "Good supplier-screening lane; map ship application before over-weighting generic process firms."),
    ("5", "Services / technical support", "Medium", "Medium", "Keep as support lane unless tied to repeatable build-stage bottlenecks."),
]


def _bubble(ids: ShapeIds, idx: int, title: str, code: str, x: float, y: float,
            fill: str, caption: str) -> str:
    return shape(
        ids, f"Bubble{idx}", Box(x, y, 1.78, 0.78),
        [p(title, size=7.4, bold=True, color=WHITE if fill in {BLUE_3, BLUE_4, BLUE_5} else BLACK, align="ctr"),
         p(code, size=6.4, color=WHITE if fill in {BLUE_3, BLUE_4, BLUE_5} else BLACK, align="ctr"),
         p(caption, size=5.8, italic=True, color=WHITE if fill in {BLUE_3, BLUE_4, BLUE_5} else BLACK, align="ctr")],
        fill=fill, line_color=WHITE, line_width=12_700, anchor="ctr", prst="roundRect",
    )


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "TopNote", Box(0.50, 1.22, 12.30, 0.36),
        [p("Priority pool = attractive observed SAM + construction relevance + an access route; concentrated pools may still matter, but the path is different.",
           size=10.5, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    # Matrix frame.
    mx, my, mw, mh = 0.62, 1.92, 7.88, 3.25
    parts.append(shape(ids, "MatrixFrame", Box(mx, my, mw, mh), [p("", size=1)],
                       fill=WHITE, line_color=DK, line_width=12_700))
    parts.append(shape(ids, "TopRightQuadrant", Box(mx + mw / 2, my, mw / 2, mh / 2), [p("", size=1)],
                       fill=BLUE_1, line_color="none", fill_alpha=65000))
    parts.append(shape(ids, "UpperLeftQuadrant", Box(mx, my, mw / 2, mh / 2), [p("", size=1)],
                       fill=GRAY_1, line_color="none", fill_alpha=65000))
    parts.append(shape(ids, "LowerRightQuadrant", Box(mx + mw / 2, my + mh / 2, mw / 2, mh / 2), [p("", size=1)],
                       fill=PALE_ORANGE, line_color="none", fill_alpha=65000))
    parts.append(hline(ids, "MatrixMidH", mx, my + mh / 2, mw, color=DK, width=9_525))
    parts.append(vline(ids, "MatrixMidV", mx + mw / 2, my, mh, color=DK, width=9_525))
    parts.append(label(ids, "AxisY", Box(mx - 0.42, my + 0.72, 0.34, 1.84),
                       "Market attractiveness", size=7.4, bold=True,
                       color=DK, fill=None, line_color="none"))
    parts.append(label(ids, "AxisX", Box(mx + 2.60, my + mh + 0.10, 2.72, 0.26),
                       "Accessibility / plausible route", size=7.4, bold=True,
                       color=DK, fill=None, line_color="none"))
    parts.append(label(ids, "Q1", Box(mx + mw / 2 + 0.12, my + 0.10, 1.78, 0.25),
                       "Prioritize first", size=7.2, bold=True, color=BLUE_5,
                       fill=WHITE, line_color="none"))
    parts.append(label(ids, "Q2", Box(mx + 0.10, my + 0.10, 1.92, 0.25),
                       "Strategic / controlled", size=7.2, bold=True, color=BLUE_5,
                       fill=WHITE, line_color="none"))
    parts.append(label(ids, "Q3", Box(mx + 0.10, my + mh / 2 + 0.10, 1.90, 0.25),
                       "Watch / research", size=7.2, bold=True, color=DK,
                       fill=WHITE, line_color="none"))
    parts.append(label(ids, "Q4", Box(mx + mw / 2 + 0.12, my + mh / 2 + 0.10, 2.18, 0.25),
                       "Diligence sequence", size=7.2, bold=True, color=DK,
                       fill=WHITE, line_color="none"))

    for i, pool in enumerate(POOLS, start=1):
        parts.append(_bubble(ids, i, *pool))

    # Rationale table.
    tx, ty = 8.76, 1.92
    parts.append(label(ids, "TableTitle", Box(tx, ty, 4.04, 0.32),
                       "Priority-pool rationale", size=8.5, bold=True,
                       color=WHITE, fill=BLUE_4, line_color=WHITE))
    headers = ["#", "Pool", "Attract.", "Access", "Diligence action"]
    widths = [0.32, 1.14, 0.52, 0.52, 1.54]
    x = tx
    for i, (h, w) in enumerate(zip(headers, widths)):
        parts.append(label(ids, f"TableHeader{i}", Box(x, ty + 0.36, w, 0.25),
                           h, size=6.4, bold=True, color=BLACK, fill=GRAY_2, line_color=WHITE))
        x += w

    y = ty + 0.64
    for r, row in enumerate(TABLE_ROWS):
        fill = WHITE if r % 2 == 0 else GRAY_1
        x = tx
        for c, (txt, w) in enumerate(zip(row, widths)):
            parts.append(shape(
                ids, f"TableR{r}C{c}", Box(x, y, w, 0.45),
                paras(txt, size=5.8 if c == 4 else 6.0, bold=c in (0, 1), color=BLACK, align="ctr" if c != 4 else "l"),
                fill=fill, line_color=WHITE, anchor="ctr",
            ))
            x += w
        y += 0.47

    parts.append(shape(
        ids, "BottomNote", Box(0.62, 5.62, 12.18, 0.36),
        [p("Use this slide as the SAM-section closer: it turns Where-to-Play metrics and D×P structure into a diligence queue, while keeping final numeric rank dependent on workbook-rendered evidence.",
           size=7.6, italic=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color="none", anchor="ctr",
    ))

    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
