"""Target slide #5: DDG-51 New-Construction Value Chain.

Full-canvas value-chain swimlane adapted from the style-library value-chain
modules. The content ties the market-sizing denominator to the observed-SAM
supplier evidence and construction traceability layers.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, Box, DK, GRAY_1, GRAY_2,
    ORANGE, ShapeIds, WHITE, arrow, label, p, paras, shape,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="Market Answer and Scope",
    topic="Value Chain",
    title="DDG-51 New-Construction Value Chain",
    takeaway="TAM, observed SAM, and construction evidence sit at different points in the build chain.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/ddg_tam.py",
            "workbook_factory/ddg/sheets/prime_awards.py",
            "workbook_factory/ddg/sheets/ddg_subaward_transactions.py",
            "workbook_factory/ddg/sheets/kit/taxonomy.py",
        ),
        note="Value-chain slide is a market map; it is not a claim that every cell is observed in FFATA subaward data.",
    ),
)

STAGES = [
    ("Budget & program", "SCN, AP/LLTM, OBBBA streams", BLUE_5),
    ("Prime ship construction", "HII-Ingalls / GD-BIW hull-builder scope", BLUE_4),
    ("Supplier work packages", "Reported first-tier subawards", BLUE_3),
    ("Install & integrate", "Ship-system / SWBS application", BLUE_4),
    ("Hull timing evidence", "Hull family and lifecycle confidence", BLUE_5),
]

ROWS = [
    ("Hull / structures", ["TAM", "Prime", "D1 / P5", "SWBS 100", "A/B, C/D"]),
    ("Machinery / power / fluid", ["TAM", "Prime", "D2-D5 / P3", "SWBS 200/300/500", "Lifecycle"]),
    ("Combat / comms / electronics", ["Scope", "Prime", "D6-D7 / P4", "SWBS 400/700", "Evidence"]),
    ("Materials / precision processes", ["Coeff.", "Prime", "D9 / P1-P2", "System-dependent", "Candidate"]),
    ("Interiors / outfitting", ["TAM", "Prime", "D10 / P2-P5", "SWBS 600", "Hull-stage"]),
    ("Services / technical support", ["Outyear", "Prime", "D11 / P6", "SWBS 800/900", "Timing"]),
]


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "TopNote", Box(0.50, 1.22, 12.30, 0.38),
        [p("One chain, three analytical layers: TAM sizes outsourced construction spend; observed SAM shows reported supplier activity; SWBS/hull/lifecycle evidence maps only where traceability supports it.",
           size=10.8, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    x0 = 2.00
    y0 = 1.82
    stage_w = 2.12
    for i, (stage, subtitle, fill) in enumerate(STAGES):
        x = x0 + i * stage_w
        parts.append(shape(
            ids, f"Stage{i+1}", Box(x, y0, stage_w - 0.05, 0.54),
            [p(stage, size=8.8, bold=True, color=WHITE, align="ctr"),
             p(subtitle, size=6.6, color=WHITE, align="ctr")],
            fill=fill, line_color="none", anchor="ctr", prst="chevron",
        ))
        if i < len(STAGES) - 1:
            parts.append(arrow(ids, f"StageArrow{i+1}", x + stage_w - 0.06, y0 + 0.27, 0.23,
                               color=ORANGE, width=12_700))

    row_y = 2.58
    row_h = 0.42
    parts.append(label(ids, "RowsHeader", Box(0.50, 2.58, 1.32, 0.38), "Work category",
                       size=8, bold=True, color=WHITE, fill=BLUE_5, line_color=WHITE))
    for i in range(len(STAGES)):
        parts.append(label(ids, f"MiniHeader{i}", Box(x0 + i * stage_w, 2.58, stage_w - 0.05, 0.38),
                           "Evidence / handoff", size=7, bold=True, color=BLACK,
                           fill=GRAY_2, line_color=WHITE))

    y = row_y + 0.43
    for r, (row_label, cells) in enumerate(ROWS):
        fill = BLUE_1 if r % 2 == 0 else GRAY_1
        parts.append(shape(ids, f"RowLabel{r}", Box(0.50, y, 1.32, row_h),
                           paras(row_label, size=7.5, bold=True, color=BLACK, align="ctr"),
                           fill=fill, line_color=WHITE, anchor="ctr"))
        for c, value in enumerate(cells):
            if c == 0:
                cell_fill = BLUE_2
                color = BLACK
            elif c == 2:
                cell_fill = BLUE_4
                color = WHITE
            elif c >= 3:
                cell_fill = WHITE
                color = BLACK
            else:
                cell_fill = BLUE_1
                color = BLACK
            parts.append(shape(ids, f"Cell{r}_{c}", Box(x0 + c * stage_w, y, stage_w - 0.05, row_h),
                               paras(value, size=7.2, bold=(c == 2), color=color, align="ctr"),
                               fill=cell_fill, line_color=WHITE, anchor="ctr"))
        y += row_h + 0.03

    panels = [
        ("TAM layer", "Budget streams and supplier coefficients size the outsourced opportunity; they do not name suppliers."),
        ("SAM evidence layer", "First-tier subawards name suppliers and fiscal timing, enabling D/P where-to-play and parent concentration screens."),
        ("Construction lens", "SWBS, hull, and lifecycle are transaction-level evidence cuts; use them only where coverage supports interpretation."),
    ]
    for i, (head, body) in enumerate(panels):
        parts.append(shape(
            ids, f"Panel{i+1}", Box(0.50 + i * 4.12, 5.22, 3.83, 0.78),
            [p(head, size=8.5, bold=True, color=BLUE_4), p(body, size=7.6, color=BLACK)],
            fill=WHITE if i != 1 else BLUE_1, line_color=BLUE_2,
        ))

    parts.append(shape(
        ids, "BottomCue", Box(10.08, 4.55, 2.72, 0.40),
        [p("Stage-map slide should follow with the construction-lens version of this grid.",
           size=7.4, italic=True, color=DK, align="ctr")],
        fill=GRAY_1, line_color=ORANGE, dashed_line=True, anchor="ctr",
    ))
    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
