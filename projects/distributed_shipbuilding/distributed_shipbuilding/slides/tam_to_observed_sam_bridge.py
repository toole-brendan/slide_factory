"""Target slide #9: TAM to Observed SAM Bridge.

Bridge-chart slide adapted from the tcv_to_acv_company_acv visual grammar: a top
formula band, a central bridge, KPI chips and a compact denominator ladder.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, Box, DK, GRAY_1, GRAY_2,
    ORANGE, PALE_ORANGE, ShapeIds, WHITE, arrow, card, label, metric_chip, p,
    paras, shape,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="TAM Sizing Build",
    topic="TAM to Observed SAM Bridge",
    title="TAM to Observed SAM Bridge",
    takeaway="The bridge is reporting reach into supplier evidence, not a market-penetration calculation.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/market_bridge.py",
            "workbook_factory/ddg/sheets/ddg_tam.py",
            "workbook_factory/ddg/docs/ddg_sam_model_goals.md",
        ),
        note="Dollar values should be pulled from the rendered workbook before final numerical charting.",
    ),
)


def _bridge_box(ids: ShapeIds, name: str, box: Box, title: str, subtitle: str,
                *, fill: str, accent: str) -> str:
    return shape(
        ids, name, box,
        [p(title, size=14, bold=True, color=WHITE if fill in (BLUE_4, BLUE_5) else BLACK, align="ctr"),
         p(subtitle, size=8.4, color=WHITE if fill in (BLUE_4, BLUE_5) else BLACK, align="ctr")],
        fill=fill, line_color=accent, line_width=12_700, anchor="ctr",
    )


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "FormulaBand", Box(0.50, 1.25, 12.30, 0.58),
        [p("DDG-51 TAM  ×  reported first-tier subaward visibility  =  observed SAM evidence layer",
           size=14, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    parts.append(_bridge_box(ids, "TamBlock", Box(0.78, 2.05, 2.55, 1.15),
                             "TAM", "Top-down supplier-addressable outsourced opportunity by FY",
                             fill=BLUE_4, accent=BLUE_4))
    parts.append(_bridge_box(ids, "VisibilityBlock", Box(3.98, 2.05, 2.55, 1.15),
                             "Reporting reach", "Observed first-tier subaward rows with supplier and timing evidence",
                             fill=BLUE_2, accent=BLUE_4))
    parts.append(_bridge_box(ids, "ObservedSamBlock", Box(7.18, 2.05, 2.55, 1.15),
                             "Observed SAM", "Bottom-up evidence subset for structure, concentration and timing",
                             fill=BLUE_3, accent=BLUE_4))
    parts.append(_bridge_box(ids, "CaveatBlock", Box(10.38, 2.05, 2.20, 1.15),
                             "Do not call it penetration", "Observed SAM / TAM is a reporting-and-reach bridge",
                             fill=PALE_ORANGE, accent=ORANGE))
    for i, x in enumerate([3.35, 6.55, 9.75], start=1):
        parts.append(arrow(ids, f"BridgeArrow{i}", x, 2.62, 0.55,
                           color=ORANGE if i == 3 else DK, width=19_050))

    chips = [
        ("BC", "Basic Construction stream"),
        ("AP/LLTM", "Ship Construction EOQ stream"),
        ("OBBBA", "mandatory overlay stream"),
        ("FY22-25", "observed-SAM bridge window"),
    ]
    for i, (val, lab) in enumerate(chips):
        parts.append(metric_chip(ids, f"BridgeChip{i+1}", Box(0.78 + i * 2.20, 3.42, 1.82, 0.58),
                                 val, lab, fill=BLUE_1 if i < 3 else PALE_ORANGE,
                                 accent=BLUE_5 if i < 3 else ORANGE))

    parts.append(card(
        ids, "UseCaseCard", Box(9.72, 3.36, 2.86, 1.05),
        "Use the bridge to", "Set boundaries", "Anchor the market size while making clear what the subaward corpus can and cannot support.",
        fill=WHITE, accent=BLUE_4, headline_size=13,
    ))

    parts.append(label(ids, "LadderHeader", Box(0.78, 4.56, 11.80, 0.30),
                       "Observed-SAM denominator ladder", size=10, bold=True,
                       color=WHITE, fill=BLUE_4))
    headers = ["Layer", "Supports", "Boundary"]
    widths = [2.40, 5.05, 4.35]
    x = 0.78
    for h, w in zip(headers, widths):
        parts.append(label(ids, f"LadderHeader{h}", Box(x, 4.90, w, 0.26), h,
                           size=8.3, bold=True, color=BLACK, fill=GRAY_2, line_color=WHITE))
        x += w

    rows = [
        ("Observed SAM", "Supplier ecosystem evidence", "Not the full outsourced-market total"),
        ("D/P classified", "Where-to-play by capability and output", "Depends on UEI × Program classification quality"),
        ("HII SWBS universe", "Ship-system application", "GD-BIW rows carry no SWBS classification"),
        ("Exact hull A/B", "Hull and hull-stage rollups", "C/D family-level dollars are not allocated"),
        ("C/D + review", "Candidate narrowing / research queue", "Candidate sets only; X rows remain conflicts or multi-hull rows"),
    ]
    y = 5.20
    for r, row in enumerate(rows):
        x = 0.78
        fill = WHITE if r % 2 == 0 else GRAY_1
        for c, (txt, w) in enumerate(zip(row, widths)):
            parts.append(shape(ids, f"LadderR{r}C{c}", Box(x, y, w, 0.30),
                               paras(txt, size=7.6, bold=(c == 0), color=BLACK),
                               fill=fill, line_color=WHITE, anchor="ctr"))
            x += w
        y += 0.32

    parts.append(shape(
        ids, "BottomNote", Box(0.78, 6.03, 11.80, 0.32),
        [p("Recommended finalization step: replace text-only bridge blocks with live FY values from Market Bridge §1 once the workbook is rendered, then keep this denominator ladder as the interpretation rail.",
           size=7.8, italic=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color="none", anchor="ctr",
    ))
    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
