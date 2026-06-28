"""Teaching exemplar: value-chain participation logo matrix.

ROLE
  value_chain_logo_matrix / integration_span_map

USE WHEN
  A slide needs to prove who participates across value-chain steps using a dense
  logo grid, semantic span boxes, and a few compact interpretation callouts.

TEACHES
  - logo-heavy evidence rows using `IMAGES` + `picture()` instead of text labels
  - value-chain chevrons with one home-plate entry step and four follow-on stages
  - semantic matrix cells for archetype participation, separate from logo slots
  - dashed integration-span boxes that state the claim while logos supply proof
  - small marker/caption grammar above the matrix
  - callouts layered after logos so the interpretation sits on top of evidence

TEXT-FIT PRECEDENT
  stage_headers:
    geometry: five 2.1in x 0.4in header shapes
    type: Arial 10pt bold, centered, 100% line spacing
    content: one value-chain step label; first header can wrap to two short lines
    copy_when: a horizontal value-chain map needs one compact label per stage

  integration_spans:
    geometry: long white outlined bands, 0.55-0.60in tall
    type: Arial 10pt; bold archetype name + italic explanation
    content: one claim per span; logos below/inside provide evidence
    copy_when: the slide argues that a player type spans multiple steps

SOURCE NOTE
  Teaching rewrite of source-faithful `value_chain_participation.py`. The original
  was already hand-polished from a converter output, but still read like clustered
  source shapes. This version promotes the slide into a reusable authored pattern:
  semantic records for stages, cells, spans, logo slots, markers, callouts, and
  connectors; a short paint API; and explicit copy rules.

FIDELITY NOTE
  Coordinates, colors, logo rIds, source crops, callout text, dividers, and table
  geometry are preserved. The paint order is simplified into conceptual layers:
  scaffolding -> headers/spans/cells -> logos -> callouts -> chrome. That is the
  more useful teaching contract; if byte-identical stacking is required, use the
  source-faithful module.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, paragraph, picture, run, table, tcell_rich,
    text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
GRAY_2 = "D9D9D9"
FONT = "Arial"


# Local table-cell kit (was deck_core.table_kit).
def edge(color, w=12700):
    """One cell-border edge dict (default 1pt hairline)."""
    return {"color": color, "width": w}

def bd(L=None, R=None, T=None, B=None):
    """Border map from only the sides drawn; omitted sides render no-fill."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None

def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """Multi-paragraph rich cell; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

LAYOUT = "slideLayout4"

CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image13_672efe4b.png"},
    {"rId": "rId3", "file": "image14_1bf4c99e.png"},
    {"rId": "rId4", "file": "image15_25624857.png"},
    {"rId": "rId5", "file": "image16_da5f3708.png"},
    {"rId": "rId6", "file": "image17_f373f1da.png"},
    {"rId": "rId7", "file": "image18_ddebb15f.png"},
    {"rId": "rId8", "file": "image19_84003496.png"},
    {"rId": "rId9", "file": "image21_0bacf462.png"},
    {"rId": "rId10", "file": "image22_9fb945dc.png"},
    {"rId": "rId11", "file": "image23_03c42e94.png"},
    {"rId": "rId12", "file": "image24_2778926d.png"},
    {"rId": "rId13", "file": "image25_bd50af1e.png"},
    {"rId": "rId14", "file": "image26_8d2caa7b.png"},
    {"rId": "rId15", "file": "image27_768e13fd.png"},
    {"rId": "rId16", "file": "image28_9cbe8d79.png"},
    {"rId": "rId17", "file": "image29_4d22badb.png"},
    {"rId": "rId18", "file": "image30_ee91678f.png"},
    {"rId": "rId19", "file": "image31_98d329b1.png"},
    {"rId": "rId20", "file": "image32_251526d6.png"},
    {"rId": "rId21", "file": "image33_f545c301.png"},
    {"rId": "rId22", "file": "image34_75574897.jpeg"},
    {"rId": "rId23", "file": "image35_b95a7460.jpeg"},
]

BLUE_STEP = "447BB2"
DARK_STEP = "0E1924"
DIVIDER_GRAY = "808080"


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class TextFitZone:
    name: str
    box: Box
    fit: str
    copy_when: str


@dataclass(frozen=True)
class StageHeader:
    label: str
    box: Box
    fill: str
    text_color: str
    prst: str = "chevron"


@dataclass(frozen=True)
class MatrixCell:
    label: str
    box: Box
    line: str
    fill: str = WHITE


@dataclass(frozen=True)
class IntegrationSpan:
    name: str
    box: Box
    line: str
    dashed: bool
    parts: tuple[tuple[str, bool, bool], ...]  # text, bold, italic


@dataclass(frozen=True)
class LogoSlot:
    role: str
    name: str
    r_id: str
    box: Box
    src_rect: dict[str, int] | None = None


@dataclass(frozen=True)
class Marker:
    meaning: str
    box: Box
    fill: str | None
    line: str
    dashed: bool = False


@dataclass(frozen=True)
class Caption:
    text: str
    box: Box
    italic: bool = False


@dataclass(frozen=True)
class Callout:
    text: str
    box: Box
    fill: str | None
    adj1: str = "val 44715"
    adj2: str = "val -24439"


@dataclass(frozen=True)
class ConnectorSpec:
    name: str
    box: Box
    color: str
    width: int = 12700
    dashed: bool = False
    arrow: bool = False
    prst: str = "line"
    flip_h: bool = False
    flip_v: bool = False
    rot: int = 0
    adj: dict[str, str] | None = None


TEACHING_METADATA = {
    "role": "value_chain_logo_matrix / integration_span_map",
    "use_when": "Prove participation patterns with logos first, then overlay span claims and callouts.",
    "teaches": (
        "logo slots are semantic evidence, not decoration",
        "integration spans should be claims, not data containers",
        "stage headers and row labels form the reading scaffold",
        "callouts are painted last because they interpret the logo evidence",
    ),
    "fidelity": "source coordinates and image relationships preserved; paint layers made conceptual",
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("stage_headers", Box(2.235, 1.641, 10.560, 0.400), "10pt bold; one step per 2.1in header", "copy for horizontal chain maps"),
    TextFitZone("representative_players", Box(0.495, 2.193, 1.600, 4.794), "10pt bold row label in a single native table cell", "copy for a logo row/field with a left spine"),
    TextFitZone("integration_spans", Box(2.490, 5.769, 10.305, 1.210), "10pt bold/italic mixed runs inside long bands", "copy when the conclusion is a cross-step span"),
    TextFitZone("callouts", Box(2.337, 2.320, 8.048, 2.330), "short 10pt italic; no more than one finding each", "copy when the matrix needs interpretation but no rail"),
)

COPY_RULES: tuple[str, ...] = (
    "Declare all logos in IMAGES first; each LogoSlot then references a meaningful rId.",
    "Let logos carry the evidence and use bands/callouts only to summarize the read.",
    "Keep value-chain step labels short enough to remain one or two lines in 2.1in headers.",
    "Document reused rIds and crop rectangles; they are intentional image wiring, not noise.",
)

STAGE_HEADERS: tuple[StageHeader, ...] = (
    StageHeader("Customer / Shipper Requires Cargo Shipment", Box(2.235, 1.641, 2.100, 0.400), GRAY_2, BLACK, "homePlate"),
    StageHeader("Coordination", Box(4.350, 1.641, 2.100, 0.400), GRAY_2, BLACK),
    StageHeader("Origin Shoreside Logistics", Box(6.465, 1.641, 2.100, 0.400), BLUE_STEP, WHITE),
    StageHeader("Maritime Transport", Box(8.580, 1.641, 2.100, 0.400), DARK_STEP, WHITE),
    StageHeader("Destination Shoreside Logistics", Box(10.695, 1.641, 2.100, 0.400), BLUE_STEP, WHITE),
)

DIVIDERS: tuple[ConnectorSpec, ...] = tuple(
    ConnectorSpec(f"StageDivider:{x}", Box(x, 2.087, 0.0, 4.900), DIVIDER_GRAY, width=3175, dashed=True, flip_h=True)
    for x in (4.291, 6.404, 8.526, 10.631)
)

ROW_LABELS: tuple[tuple[str, Box], ...] = (
    ("Value Chain Step", Box(0.495, 1.641, 1.600, 0.400)),
    ("Representative players", Box(0.495, 2.193, 1.600, 4.794)),
)

MATRIX_CELLS: tuple[MatrixCell, ...] = (
    MatrixCell("Terminal Operators", Box(6.527, 4.782, 1.876, 0.926), BLUE_STEP),
    MatrixCell("Charter Companies", Box(8.643, 4.782, 1.877, 0.926), DARK_STEP),
    MatrixCell("Pure-play Shipbuilders", Box(8.643, 2.193, 1.877, 0.885), DARK_STEP),
    MatrixCell("Integrated Shipbuilders", Box(8.643, 3.137, 1.877, 1.586), DARK_STEP),
    MatrixCell("Terminal Operators", Box(10.807, 4.782, 1.876, 0.926), BLUE_STEP),
)

INTEGRATION_SPANS: tuple[IntegrationSpan, ...] = (
    IntegrationSpan(
        "shippers_private_carriers",
        Box(2.490, 6.428, 10.305, 0.551),
        BLACK,
        True,
        (("Shippers / Private Carriers – ", True, False), ("Integrated across value chain steps", False, True)),
    ),
    IntegrationSpan(
        "vocc",
        Box(4.350, 5.769, 8.445, 0.600),
        DARK_STEP,
        False,
        (
            ("Vessel Operating Common Carriers", True, False),
            (" – ", True, True),
            ("Integrated across multiple value chain steps (largely Terminal Ops and/or Coordination)", False, True),
        ),
    ),
)

GROUP_CAPTIONS: tuple[Caption, ...] = (
    Caption("Primarily Maritime Transport Players", Box(0.684, 1.344, 2.018, 0.236)),
    Caption("Shoreside Logistics Players", Box(2.881, 1.344, 1.587, 0.236)),
    Caption("Integrated Shippers", Box(4.646, 1.344, 1.189, 0.236)),
)

MARKERS: tuple[Marker, ...] = (
    Marker("primarily maritime transport", Box(0.495, 1.361, 0.200, 0.200), None, DARK_STEP),
    Marker("integrated shippers", Box(4.457, 1.361, 0.200, 0.200), WHITE, BLACK, True),
    Marker("shoreside logistics", Box(2.691, 1.361, 0.200, 0.200), None, BLUE_STEP),
)

CALLOUTS: tuple[Callout, ...] = (
    Callout("Players shown own and operate their own vessels and charter additional ships ", Box(2.337, 2.320, 1.944, 0.482), WHITE),
    Callout("Entered shipping in ‘24", Box(8.778, 3.726, 1.607, 0.169), None),
    Callout("Chartering", Box(8.778, 4.482, 1.607, 0.168), None),
)

CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec(
        "primarily_maritime_to_matrix",
        Box(0.532, 3.999, 4.662, 0.746),
        BLACK,
        arrow=True,
        prst="bentConnector4",
        rot=5400000,
        adj={"adj1": "val 47046", "adj2": "val 133516"},
    ),
)

LOGO_SLOTS: tuple[LogoSlot, ...] = (
    LogoSlot("origin_terminal", "origin_terminal_logo_1", "rId2", Box(6.871, 5.382, 1.186, 0.273)),
    LogoSlot("origin_terminal", "origin_terminal_logo_2", "rId3", Box(6.854, 5.038, 1.221, 0.248), {"t": 39246, "b": 40454}),
    LogoSlot("coordination", "coordination_logo_1", "rId4", Box(4.778, 6.709, 1.240, 0.226)),
    LogoSlot("origin_terminal", "origin_terminal_logo_3", "rId5", Box(6.825, 6.703, 0.744, 0.237)),
    LogoSlot("shipper_private", "shipper_private_logo_1", "rId6", Box(2.733, 6.712, 1.157, 0.219)),
    LogoSlot("destination_terminal", "destination_terminal_logo_1", "rId7", Box(10.197, 6.698, 1.074, 0.248)),
    LogoSlot("destination_terminal", "destination_terminal_logo_2", "rId8", Box(11.902, 6.674, 0.661, 0.296)),
    LogoSlot("vocc_span", "vocc_logo_1", "rId9", Box(5.554, 6.043, 1.000, 0.244), {"t": 1, "b": 30297}),
    LogoSlot("vocc_span", "vocc_logo_2", "rId10", Box(9.303, 6.050, 1.500, 0.231)),
    LogoSlot("vocc_span", "vocc_logo_3", "rId11", Box(11.511, 6.027, 1.200, 0.276)),
    LogoSlot("vocc_span", "vocc_logo_4", "rId12", Box(4.464, 6.004, 0.331, 0.321), {"l": 16902, "t": 18159, "r": 16883, "b": 17525}),
    LogoSlot("vocc_span", "vocc_logo_5", "rId13", Box(7.279, 5.994, 1.300, 0.342), {"l": 1136, "t": 2363, "r": 1895}),
    LogoSlot("charter_companies", "charter_logo_1", "rId14", Box(8.693, 5.026, 1.380, 0.273)),
    LogoSlot("charter_companies", "charter_logo_2", "rId15", Box(9.458, 5.251, 1.000, 0.204)),
    LogoSlot("charter_companies", "charter_logo_3", "rId16", Box(8.705, 5.466, 0.884, 0.244)),
    LogoSlot("pure_play_shipbuilder", "pureplay_logo_1", "rId17", Box(9.609, 2.812, 0.800, 0.203)),
    LogoSlot("pure_play_shipbuilder", "pureplay_logo_2", "rId18", Box(9.559, 2.565, 0.900, 0.103)),
    LogoSlot("pure_play_shipbuilder", "pureplay_logo_3", "rId19", Box(8.843, 2.493, 0.500, 0.248)),
    LogoSlot("pure_play_shipbuilder", "pureplay_logo_4", "rId20", Box(8.693, 2.831, 0.800, 0.201), {"l": 6989, "t": 38971, "r": 6559, "b": 39290}),
    LogoSlot("integrated_shipbuilder", "integrated_logo_1", "rId21", Box(9.082, 3.377, 1.000, 0.277)),
    LogoSlot("integrated_shipbuilder", "integrated_logo_2", "rId22", Box(8.780, 3.968, 1.604, 0.205), {"t": 43928, "b": 43272}),
    LogoSlot("integrated_shipbuilder", "integrated_logo_3", "rId23", Box(8.782, 4.245, 1.600, 0.164), {"t": 44933, "b": 44796}),
    # rId2/rId3 are reused intentionally for the mirrored destination-terminal cells.
    LogoSlot("destination_terminal", "destination_terminal_reused_logo_1", "rId2", Box(11.151, 5.382, 1.186, 0.273)),
    LogoSlot("destination_terminal", "destination_terminal_reused_logo_2", "rId3", Box(11.134, 5.038, 1.221, 0.248), {"t": 39246, "b": 40454}),
)


def _xywh(box: Box) -> tuple[int, int, int, int]:
    return IN(box.x), IN(box.y), IN(box.w), IN(box.h)


def _p(text: str, *, size=PT(10), bold=False, italic=False, color=BLACK, align="ctr") -> str:
    return paragraph([run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)], align=align, line_spacing=100000)


def _mixed_p(parts: tuple[tuple[str, bool, bool], ...]) -> str:
    return paragraph(
        [run(text, size=PT(10), bold=bold or None, italic=italic or None, color=BLACK, font=FONT) for text, bold, italic in parts],
        align="ctr",
        line_spacing=100000,
    )


def paint_scaffold(out: list[str], n) -> None:
    for item in DIVIDERS:
        out.append(connector(n(), item.name, *_xywh(item.box), color=item.color, width=item.width, dashed=item.dashed, arrow=item.arrow, prst=item.prst, flip_h=item.flip_h, flip_v=item.flip_v, rot=item.rot, adj=item.adj))
    for span in INTEGRATION_SPANS:
        out.append(
            text_box(
                n(),
                f"IntegrationSpan:{span.name}",
                *_xywh(span.box),
                [_mixed_p(span.parts)],
                fill=WHITE,
                line_color=span.line,
                line_width=19050,
                dashed_line=span.dashed,
            )
        )


def paint_stage_headers(out: list[str], n) -> None:
    for header in STAGE_HEADERS:
        out.append(
            text_box(
                n(),
                f"StageHeader:{header.label}",
                *_xywh(header.box),
                [_p(header.label, bold=True, color=header.text_color)],
                fill=header.fill,
                line_color="none",
                prst=header.prst,
                geom_adj={"adj": "val 24929"},
                anchor="ctr",
                l_ins=144000,
                t_ins=108000,
                r_ins=144000,
                b_ins=108000,
            )
        )


def paint_row_labels(out: list[str], n) -> None:
    for label, box in ROW_LABELS:
        out.append(
            table(
                n(),
                f"RowLabel:{label}",
                *_xywh(box),
                col_widths=[IN(box.w)],
                rows=[trow([rcell([tpara([trun(label, size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, R=edge(BLACK, 38100))], h=IN(box.h))],
            )
        )


def paint_matrix_cells(out: list[str], n) -> None:
    for cell in MATRIX_CELLS:
        out.append(
            text_box(
                n(),
                f"ParticipationCell:{cell.label}",
                *_xywh(cell.box),
                [_p(cell.label, bold=True)],
                fill=cell.fill,
                line_color=cell.line,
                line_width=19050,
            )
        )


def paint_marker_key(out: list[str], n) -> None:
    for marker in MARKERS:
        out.append(text_box(n(), f"Marker:{marker.meaning}", *_xywh(marker.box), [paragraph([], align="ctr", line_spacing=100000)], fill=marker.fill, line_color=marker.line, line_width=19050, dashed_line=marker.dashed, anchor="ctr"))
    for caption in GROUP_CAPTIONS:
        out.append(text_box(n(), f"GroupCaption:{caption.text}", *_xywh(caption.box), [paragraph([run(caption.text, size=PT(8), italic=caption.italic or None, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))


def paint_logos(out: list[str], n) -> None:
    for logo in LOGO_SLOTS:
        out.append(picture(n(), f"Logo:{logo.role}:{logo.name}", logo.r_id, *_xywh(logo.box), src_rect=logo.src_rect))


def paint_connectors_and_callouts(out: list[str], n) -> None:
    for item in CONNECTORS:
        out.append(connector(n(), item.name, *_xywh(item.box), color=item.color, width=item.width, dashed=item.dashed, arrow=item.arrow, prst=item.prst, flip_h=item.flip_h, flip_v=item.flip_v, rot=item.rot, adj=item.adj))
    for callout in CALLOUTS:
        out.append(
            text_box(
                n(),
                "Callout:ParticipationRead",
                *_xywh(callout.box),
                [_p(callout.text, italic=True)],
                fill=callout.fill,
                line_color="none",
                prst="wedgeRectCallout",
                geom_adj={"adj1": callout.adj1, "adj2": callout.adj2},
                anchor="ctr",
            )
        )


def _body() -> str:
    out: list[str] = []
    ids = iter(range(100, 2000))
    n = lambda: next(ids)  # noqa: E731 - sequential shape ids
    paint_scaffold(out, n)
    paint_stage_headers(out, n)
    paint_row_labels(out, n)
    paint_matrix_cells(out, n)
    paint_marker_key(out, n)
    paint_logos(out, n)
    paint_connectors_and_callouts(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Commercial Maritime Value Chain",
    topic="Overview",
    title="Value Chain Participation",
    takeaway="Shipbuilders largely not observed to vertically integrate beyond chartering, whereas large shippers and VOCCs integrate across the value chain.",
)


def render() -> str:
    return body_slide(CHROME, _body())
