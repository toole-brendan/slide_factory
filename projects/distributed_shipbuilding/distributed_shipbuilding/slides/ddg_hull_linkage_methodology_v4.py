"""Teaching exemplar: DDG Hull Linkage Methodology.

ROLE
  method_slide / evidence_gate_allocation

USE WHEN
  A methodology slide must explain how subaward evidence is linked to a specific
  ship hull, where exact hulls are assigned only when an independent contract-
  family signal and a direct order-level signal agree, and unresolved cases are
  held out rather than force-fit.

TEACHES
  - left approach rail describing the analyst's method, not the math itself
    (verb-first StepCards, copied from tcv_approach_usv / tcv_approach_manned);
    the rail header + rule share the body's top line (y=1.55 / rule y=1.88) with
    the centre "Evidence evaluation" header so the two header rules align and the
    rail clears a two-line title
  - two horizontal evidence lanes (contract family + hull evidence) that
    converge through orthogonal bentConnector3 routes into a single Confidence
    Gate, copied from the allocation-filter + connector grammar of
    tcv_approach_iamd; connectors are crooked (elbow) only, never diagonal
  - a Confidence Gate drawn as a plain rectangle (the deck's shape vocabulary is
    rect / ellipse / glyphs; no hexagon is used anywhere in the deck); the gate
    emits to the three outcome tiers as three clean horizontal arrows, each at a
    card's vertical centre, instead of elbows crowding the gutter
  - a right-hand output stack where colour intensity carries the confidence
    tier: dark = assigned, pale = family-level, red/dashed = exception. The stack
    is pulled inside the right margin (ends 12.75in, not off-slide)
  - a dashed annotation callout for the gate rule (tcv_approach_iamd dashed
    allocation-note idiom), centred under the gate
  - a 2x2 construction-hierarchy mini-table marking the attribution boundary
    (functional hull/SWBS evidence vs. physical module/block), built with the
    native table() primitive in the ruled-header idiom of coordination_archetypes
    (white fill, bold header carried by a black bottom rule, hairline column
    divider) rather than four bordered text-boxes

TEXT-FIT PRECEDENT
  approach_rail:
    geometry: 2.100in wide x 0.701in high cards, flush to the 0.495in left margin
    type: Arial 10pt, left aligned, one numbered verb-first method step
    copy_when: the slide teaches a method while the body shows the evidence flow
  evidence_node:
    geometry: 1.85-1.95in wide x 0.42-0.52in high, Arial 10pt centered
    content: short evidence variable, optional italic signal-strength line
    copy_when: the flow is an evidence test, not a narrative process map
  confidence_gate:
    geometry: 1.95in wide x 2.45in high rectangle, Arial 11pt white centered
    copy_when: two independent signals are weighed before any assignment
  outcome_card:
    geometry: 2.40in wide x 0.74in high, Arial 10pt, two lines (grade + result)
    copy_when: confidence tiers branch into assigned / inferred / held-out
  construction_table:
    geometry: 7.05in wide x ~0.74in high, native 2-col x 2-row table, Arial 10pt
    copy_when: a method must state what its evidence can and cannot place

SOURCE NOTE
  Authored in the teaching-exemplar grammar shared by tcv_approach_iamd,
  tcv_approach_usv, definitions_market_levels, and addressable_demand. The
  converter-era tuple buckets are expressed as typed records (`StepCard`,
  `FlowNode`, `TextSpec`, `ConnectorSpec`, `OutcomeCard`) and paint order is
  grouped into named `paint_*` layers. The attribution boundary uses the native
  table() ruled-header idiom from coordination_archetypes.

FIDELITY NOTE
  Visible copy stays at the evidence level ("Contract family", "Order-level
  hull mention", "Requirement-text signal", "Exact hull", "Family-level",
  "Exception queue", "No forced assignment"). No parsing syntax, workbook
  internals, or build-process mechanics appear in slide copy. The gate is a
  rectangle (no hexagon); every cross-row connector is an orthogonal
  bentConnector3 or a pure horizontal line (no diagonal segments).
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, run,
    table, tcell, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
BLUE_5 = "263746"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
HAIRLINE = "808080"          # 0.5pt table column divider / mute rule
MUTE = "808080"              # "not supported" body text — readable but secondary
RED = "C00000"
SURFACE_BLUE = "447BB2"
FONT = "Arial"
NO_BORDER = "none"

LAYOUT = "slideLayout4"

CHARTS: list = []


# ════════════════════════════════════════════════════════════════════════════
# Semantic geometry / data records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class TextFitZone:
    name: str
    box: Box
    fit: str
    copy_when: str


@dataclass(frozen=True)
class RunSpec:
    text: str
    size: int = PT(10)
    color: str | None = BLACK
    bold: bool = False
    italic: bool = False
    break_before: bool = False


@dataclass(frozen=True)
class TextSpec:
    role: str
    name: str
    box: Box
    runs: tuple[RunSpec, ...]
    fill: str | None = None
    line_color: str | None = NO_BORDER
    line_width: int = 3175
    align: str | None = "ctr"
    anchor: str = "ctr"
    prst: str = "rect"
    rot: int = 0
    geom_adj: dict[str, str] | None = None
    dashed_line: bool = False
    wrap: str = "square"


@dataclass(frozen=True)
class StepCard:
    step: int
    box: Box
    label: str


@dataclass(frozen=True)
class FlowNode:
    role: str
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str
    primary: str
    secondary: str | None = None
    line_width: int = 3175
    size: int = PT(10)


@dataclass(frozen=True)
class OutcomeCard:
    role: str
    box: Box
    fill: str | None
    line_color: str
    text_color: str
    grade: str
    result: str
    dashed: bool = False
    line_width: int = 3175


@dataclass(frozen=True)
class ConnectorSpec:
    role: str
    name: str
    box: Box
    color: str = BLACK
    width: int = 12700
    arrow: bool = True
    prst: str = "line"            # "line" for horizontal rules/arrows only
    dashed: bool = False
    flip_h: bool = False
    flip_v: bool = False
    rot: int = 0
    adj: dict[str, str] | None = None


# ════════════════════════════════════════════════════════════════════════════
# Documentation tuples (mirrors the exemplar family contract).
# ════════════════════════════════════════════════════════════════════════════
TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_rail", Box(0.495, 1.55, 2.100, 4.170), "Arial 10pt; one verb-first method step per card", "copy for method spines"),
    TextFitZone("evidence_lanes", Box(2.95, 1.96, 5.05, 3.42), "Arial 10pt centered nodes; optional italic signal line", "copy for evidence tests"),
    TextFitZone("confidence_gate", Box(7.95, 2.55, 1.95, 2.45), "Arial 11pt white centered, rectangle", "copy for two-signal decision gates"),
    TextFitZone("outcome_stack", Box(10.35, 2.55, 2.40, 2.62), "Arial 10pt two-line cards; colour = confidence tier", "copy for tiered assignment outcomes"),
    TextFitZone("construction_table", Box(2.95, 5.66, 7.05, 0.74), "Arial 10pt native 2x2 table; attribution boundary", "copy for evidence-scope boundaries"),
)

COPY_RULES: tuple[str, ...] = (
    "Keep visible copy at the evidence level; never expose parsing or workbook mechanics.",
    "Assign an exact hull only when the contract-family signal and a direct order-level signal agree.",
    "Let colour intensity carry the confidence tier: dark = assigned, pale = inferred, red = held out.",
    "Treat order-level hull fields as the strongest signal and requirement text as a weaker, family-level signal.",
    "State the attribution boundary explicitly: subaward evidence places hull / SWBS / vendor / timing, not physical module / block.",
    "Route every cross-row connector as an orthogonal bentConnector3 (crooked, no diagonal) or a pure horizontal line; the gate is a rectangle, never a hexagon.",
)

FLOW_GRAMMAR = {
    "layer_a": "Prime PIID -> candidate hull family (single-ship contract or MYP hull family)",
    "layer_b": "subaward order text -> order-level hull mention (strong) + requirement-text mention (weak)",
    "gate": "two independent layers weighed; no forced assignment",
    "outcomes": "A/B exact hull | C/D family-level | X exception queue",
}


# ════════════════════════════════════════════════════════════════════════════
# Paint helpers.
# ════════════════════════════════════════════════════════════════════════════
def _shape_ids():
    return iter(range(100, 2000))


def _p(runs: tuple[RunSpec, ...], *, align: str | None = None) -> str:
    pieces: list[str] = []
    for spec in runs:
        if spec.break_before:
            pieces.append(line_break())
        pieces.append(run(
            spec.text,
            size=spec.size,
            color=spec.color,
            bold=spec.bold or None,
            italic=spec.italic or None,
            font=FONT,
        ))
    kwargs = {"line_spacing": 100000}
    if align is not None:
        kwargs["align"] = align
    return paragraph(pieces, **kwargs)


def _draw_text(out: list[str], n, spec: TextSpec) -> None:
    out.append(text_box(
        n(), spec.name, *spec.box.emu(),
        [_p(spec.runs, align=spec.align)],
        fill=spec.fill,
        line_color=spec.line_color,
        line_width=spec.line_width,
        anchor=spec.anchor,
        prst=spec.prst,
        rot=spec.rot,
        geom_adj=spec.geom_adj,
        dashed_line=spec.dashed_line,
        wrap=spec.wrap,
    ))


def _draw_step(out: list[str], n, step: StepCard) -> None:
    _draw_text(out, n, TextSpec(
        "approach_step", "ApproachStep", step.box,
        (RunSpec(f"{step.step}. {step.label}", PT(10)),),
        align=None,
    ))


def _draw_node(out: list[str], n, node: FlowNode) -> None:
    runs = [RunSpec(node.primary, node.size, node.text_color)]
    if node.secondary:
        runs.append(RunSpec(node.secondary, PT(8), node.text_color, italic=True, break_before=True))
    _draw_text(out, n, TextSpec(
        node.role, "EvidenceNode", node.box, tuple(runs),
        fill=node.fill, line_color=node.line_color, line_width=node.line_width,
        align="ctr", anchor="ctr",
    ))


def _draw_outcome(out: list[str], n, card: OutcomeCard) -> None:
    runs = (
        RunSpec(card.grade, PT(10), card.text_color, bold=True),
        RunSpec(card.result, PT(9), card.text_color, break_before=True),
    )
    _draw_text(out, n, TextSpec(
        card.role, "OutcomeCard", card.box, runs,
        fill=card.fill, line_color=card.line_color, line_width=card.line_width,
        align="ctr", anchor="ctr", dashed_line=card.dashed,
    ))


def _draw_connector(out: list[str], n, c: ConnectorSpec) -> None:
    out.append(connector(
        n(), c.name, *c.box.emu(),
        color=c.color, width=c.width, arrow=c.arrow, prst=c.prst,
        dashed=c.dashed, flip_h=c.flip_h, flip_v=c.flip_v, rot=c.rot, adj=c.adj,
    ))


# Native-table cell helpers (coordination_archetypes idiom).
def _edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    return {"color": color, "width": w}


def _border(**edges):
    return {k: v for k, v in edges.items() if v is not None} or None


# ════════════════════════════════════════════════════════════════════════════
# Zone 1 — Left approach rail. Header + rule share the body top line (y=1.55 /
# rule 1.88) with the centre header, and the rail is flush to the 0.495in margin
# so it lines up with the title/breadcrumb and clears a two-line title.
# ════════════════════════════════════════════════════════════════════════════
RAIL_X = 0.495
RAIL_W = 2.100

RAIL_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(RAIL_X, 1.550, RAIL_W, 0.300), (RunSpec("Approach steps", PT(10), BLACK, italic=True),), align=None)
RAIL_UNDERLINE = ConnectorSpec("approach_header_rule", "ApproachUnderline", Box(RAIL_X, 1.880, RAIL_W, 0.002), DK, 12700, arrow=False, prst="line", flip_h=True)

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(1, Box(RAIL_X, 1.960, RAIL_W, 0.701), "Define DDG subaward universe"),
    StepCard(2, Box(RAIL_X, 2.724, RAIL_W, 0.701), "Map prime contract to candidate hull family"),
    StepCard(3, Box(RAIL_X, 3.488, RAIL_W, 0.701), "Read order-level hull mentions"),
    StepCard(4, Box(RAIL_X, 4.252, RAIL_W, 0.701), "Compare hull evidence to contract family"),
    StepCard(5, Box(RAIL_X, 5.016, RAIL_W, 0.701), "Assign confidence tier and roll up exact matches"),
)


# ════════════════════════════════════════════════════════════════════════════
# Zone 2 — Centre evidence diagram (two lanes -> confidence gate).
# ════════════════════════════════════════════════════════════════════════════
DIAGRAM_HEADER = TextSpec("diagram_header", "EvidenceHeader", Box(2.95, 1.550, 3.000, 0.300), (RunSpec("Evidence evaluation", PT(10), BLACK, italic=True),), align=None)
DIAGRAM_UNDERLINE = ConnectorSpec("diagram_header_rule", "EvidenceUnderline", Box(2.95, 1.880, 3.000, 0.002), DK, 12700, arrow=False, prst="line", flip_h=True)

LANE_A_LABEL = TextSpec("lane_label", "LayerALabel", Box(2.95, 1.960, 2.300, 0.300), (RunSpec("Layer A — Contract family", PT(10), DK, italic=True),), align=None)
LANE_B_LABEL = TextSpec("lane_label", "LayerBLabel", Box(2.95, 3.520, 2.300, 0.300), (RunSpec("Layer B — Hull evidence", PT(10), DK, italic=True),), align=None)

LANE_A_NODES: tuple[FlowNode, ...] = (
    FlowNode("source_node", Box(2.95, 2.30, 1.85, 0.42), BLACK, BLACK, WHITE, "Prime PIID"),
    FlowNode("evidence_node", Box(5.25, 2.30, 1.95, 0.42), BLUE_2, BLUE_4, BLACK, "Candidate hull family"),
)

LANE_A_SUBCHIPS: tuple[FlowNode, ...] = (
    FlowNode("subchip", Box(5.25, 2.82, 0.95, 0.34), GRAY_1, GRAY_2, BLACK, "Single-ship contract", size=PT(8)),
    FlowNode("subchip", Box(6.25, 2.82, 0.95, 0.34), GRAY_1, GRAY_2, BLACK, "MYP hull family", size=PT(8)),
)

LANE_B_NODES: tuple[FlowNode, ...] = (
    FlowNode("source_node", Box(2.95, 4.04, 1.85, 0.52), BLACK, BLACK, WHITE, "Subaward order text"),
    FlowNode("evidence_node", Box(5.25, 3.74, 1.95, 0.52), BLUE_2, BLUE_4, BLACK, "Order-level hull mention", "Strongest direct signal"),
    FlowNode("evidence_node", Box(5.25, 4.34, 1.95, 0.52), BLUE_1, BLUE_4, BLACK, "Requirement-text mention", "Family-level signal"),
)

# Confidence gate — large rectangle both lanes feed (no hexagon; heavier border
# and full height set it apart from the 0.42in evidence nodes).
CONFIDENCE_GATE = TextSpec(
    "confidence_gate", "ConfidenceGate", Box(7.95, 2.55, 1.95, 2.45),
    (
        RunSpec("Confidence", PT(11), WHITE, bold=True),
        RunSpec("Gate", PT(11), WHITE, bold=True, break_before=True),
        RunSpec("Two independent", PT(9), WHITE, break_before=True),
        RunSpec("evidence layers", PT(9), WHITE, break_before=True),
    ),
    fill=BLUE_4, line_color=DK, line_width=12700, align="ctr", anchor="ctr", prst="rect",
)

GATE_NOTE = TextSpec(
    "gate_note", "GateRuleNote", Box(7.825, 5.070, 2.200, 0.420),
    (RunSpec("No forced assignment when layers disagree", PT(9), DK, italic=True),),
    line_color=DK, dashed_line=True, anchor="t", align="ctr",
)

# Lane-A internal arrow: same row -> pure horizontal "line" (not diagonal).
LANE_A_ARROW = ConnectorSpec("lane_a_flow", "LaneAArrow", Box(4.80, 2.51, 0.45, 0.000), prst="line")

# Lane-B split: crooked elbow connectors (bentConnector3), no diagonal.
LANE_B_SPLIT: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("lane_b_flow", "LaneBToOrderLevel", Box(4.80, 4.00, 0.45, 0.30), prst="bentConnector3", flip_v=True),
    ConnectorSpec("lane_b_flow", "LaneBToRequirement", Box(4.80, 4.30, 0.45, 0.30), prst="bentConnector3"),
)

# Both lanes converge into the gate (left edge x=7.95) via crooked elbows.
CONVERGE: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("converge", "FamilyToGate", Box(7.20, 2.51, 0.75, 0.59), prst="bentConnector3"),
    ConnectorSpec("converge", "OrderLevelToGate", Box(7.20, 3.65, 0.75, 0.35), prst="bentConnector3", flip_v=True),
    ConnectorSpec("converge", "RequirementToGate", Box(7.20, 4.25, 0.75, 0.35), prst="bentConnector3", flip_v=True),
)


# ════════════════════════════════════════════════════════════════════════════
# Zone 3 — Right outcome stack (colour intensity = confidence tier). Pulled
# inside the right margin: x=10.35, w=2.40 -> ends 12.75in.
# ════════════════════════════════════════════════════════════════════════════
OUTCOME_X = 10.35
OUTCOME_W = 2.40

OUTCOME_CARDS: tuple[OutcomeCard, ...] = (
    OutcomeCard("outcome_assigned", Box(OUTCOME_X, 2.55, OUTCOME_W, 0.74), DK, DK, WHITE, "A / B — Exact hull", "Assigned to hull"),
    OutcomeCard("outcome_family", Box(OUTCOME_X, 3.49, OUTCOME_W, 0.74), BLUE_1, BLUE_4, BLACK, "C / D — Family-level", "Retained at contract family"),
    OutcomeCard("outcome_exception", Box(OUTCOME_X, 4.43, OUTCOME_W, 0.74), WHITE, RED, RED, "X — Exception queue", "Held out of roll-up", dashed=True, line_width=19050),
)

# Gate -> outcomes: three clean horizontal arrows, each at a card's vertical
# centre (2.92 / 3.86 / 4.80), from the gate right edge (9.90) to the card
# (10.35). No elbows crowding the gutter; the exception arrow is red.
GATE_TO_OUTCOME: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("gate_branch", "GateToAssigned", Box(9.90, 2.92, 0.45, 0.000), prst="line"),
    ConnectorSpec("gate_branch", "GateToFamily", Box(9.90, 3.86, 0.45, 0.000), prst="line"),
    ConnectorSpec("gate_branch", "GateToException", Box(9.90, 4.80, 0.45, 0.000), prst="line", color=RED),
)


# ════════════════════════════════════════════════════════════════════════════
# Bottom — construction-hierarchy attribution boundary (native 2x2 table).
# Built with table() in the coordination_archetypes ruled-header idiom: white
# fill, bold header carried by a black bottom rule, a hairline column divider,
# muted "not supported" body text. One frame -> no doubled borders.
# ════════════════════════════════════════════════════════════════════════════
TABLE_CAPTION = TextSpec(
    "grid_caption", "ConstructionCaption", Box(2.95, 5.360, 4.550, 0.260),
    (RunSpec("Construction hierarchy — attribution boundary", PT(10), BLACK, italic=True),),
    align=None,
)

CONSTR_BOX = Box(2.95, 5.660, 7.050, 0.740)
CONSTR_COLS = (3.10, 3.95)            # left = supported, right = not supported
CONSTR_HEADER_H = 0.340
CONSTR_BODY_H = 0.400
CONSTR_HEADERS = ("Supported by subaward evidence", "Not supported by subaward evidence")
CONSTR_BODY = ("Hull · SWBS · Vendor · Timing", "Physical module · Grand block · Structural unit")

FOOTNOTE = TextSpec(
    "footnote", "OutcomeFootnote", Box(0.495, 6.660, 12.340, 0.300),
    (RunSpec("Note: A and B populate an assigned hull; C and D are inferred at the contract family; X is multi-hull or conflicting and is held out of the roll-up.", PT(9), BLACK),),
    align=None,
)


# ════════════════════════════════════════════════════════════════════════════
# Chrome footnote.
# ════════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════════
# Paint layers.
# ════════════════════════════════════════════════════════════════════════════
def paint_approach_rail(out: list[str], n) -> None:
    _draw_text(out, n, RAIL_HEADER)
    _draw_connector(out, n, RAIL_UNDERLINE)
    for step in APPROACH_STEPS:
        _draw_step(out, n, step)


def paint_evidence_lanes(out: list[str], n) -> None:
    _draw_text(out, n, DIAGRAM_HEADER)
    _draw_connector(out, n, DIAGRAM_UNDERLINE)
    _draw_text(out, n, LANE_A_LABEL)
    _draw_text(out, n, LANE_B_LABEL)
    for node in LANE_A_NODES:
        _draw_node(out, n, node)
    for chip in LANE_A_SUBCHIPS:
        _draw_node(out, n, chip)
    for node in LANE_B_NODES:
        _draw_node(out, n, node)
    _draw_connector(out, n, LANE_A_ARROW)
    for c in LANE_B_SPLIT:
        _draw_connector(out, n, c)


def paint_confidence_gate(out: list[str], n) -> None:
    for c in CONVERGE:
        _draw_connector(out, n, c)
    _draw_text(out, n, CONFIDENCE_GATE)
    _draw_text(out, n, GATE_NOTE)


def paint_outcome_stack(out: list[str], n) -> None:
    for c in GATE_TO_OUTCOME:
        _draw_connector(out, n, c)
    for card in OUTCOME_CARDS:
        _draw_outcome(out, n, card)


def paint_construction_table(out: list[str], n) -> None:
    _draw_text(out, n, TABLE_CAPTION)
    header_cells = [
        tcell(CONSTR_HEADERS[0], fill=WHITE, bold=True, size=PT(10), align="ctr",
              anchor="b", font=FONT, borders=_border(B=_edge(BLACK), R=_edge(HAIRLINE, 6_350))),
        tcell(CONSTR_HEADERS[1], fill=WHITE, bold=True, size=PT(10), align="ctr",
              anchor="b", font=FONT, borders=_border(B=_edge(BLACK))),
    ]
    body_cells = [
        tcell(CONSTR_BODY[0], fill=WHITE, size=PT(10), color=BLACK, align="ctr",
              anchor="ctr", font=FONT, borders=_border(B=_edge(HAIRLINE, 6_350), R=_edge(HAIRLINE, 6_350))),
        tcell(CONSTR_BODY[1], fill=WHITE, size=PT(10), color=MUTE, align="ctr",
              anchor="ctr", font=FONT, borders=_border(B=_edge(HAIRLINE, 6_350))),
    ]
    out.append(table(
        n(), "ConstructionBoundaryTable", *CONSTR_BOX.emu(),
        col_widths=[IN(CONSTR_COLS[0]), IN(CONSTR_COLS[1])],
        rows=[
            trow(header_cells, h=IN(CONSTR_HEADER_H)),
            trow(body_cells, h=IN(CONSTR_BODY_H)),
        ],
    ))


def paint_chip_footnote(out: list[str], n) -> None:
    _draw_text(out, n, FOOTNOTE)


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_approach_rail(out, n)
    paint_evidence_lanes(out, n)
    paint_confidence_gate(out, n)
    paint_outcome_stack(out, n)
    paint_construction_table(out, n)
    paint_chip_footnote(out, n)
    return "".join(out)


CHROME = Chrome(
    section="DDG-51 Subaward Analysis",
    topic="Methodology",
    title="DDG Hull Linkage Methodology",
    takeaway="Exact hulls are assigned only when contract family and order evidence align",
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
