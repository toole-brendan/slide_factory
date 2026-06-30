"""Teaching exemplar: DDG Hull Linkage Methodology, v4 diagram at the method footprint.

ROLE
  method_slide / evidence_gate_allocation (v4 diagram, method-footprint variant)

USE WHEN
  The v4 hull-linkage methodology diagram is wanted, but laid out on the geometry
  of ``ddg51_hull_linkage_method`` instead of the original v4 footprint.

WHAT THIS IS
  The shapes and styles are taken from ``ddg_hull_linkage_methodology_v4``: the
  plain numbered approach rail, the two evidence lanes (black source nodes -> blue
  evidence nodes -> grey sub-chips), the Confidence Gate fed by orthogonal
  bentConnector3 elbows, and the A/B · C/D · X outcome stack. Two elements are
  pulled from ``ddg51_hull_linkage_method``: the gate uses that module's compact
  gate variation (darker BLUE_5 fill, 1.25in-high box, three-line "Confidence
  Gate / Family + text align / No forced assignment" label), so v4's separate
  dashed gate-rule note is dropped and the gate fans out through a vertical
  outcome trunk; and the bottom band carries a stretched-out, vertically-short
  rebuild of that module's "Downstream result views" table. The geometry is
  retargeted:

    - rail sits at the method rail anchors (header 0.522in, steps 0.700in);
    - the gate (method compact size, 1.97in x 1.25in) is centred in the gap
      between the evidence nodes (right 7.10in) and the outcome cards (left
      10.25in), i.e. left 7.69in / right 9.66in with 0.59in clear each side;
    - the outcome cards move to the method card column (left 10.25in, width
      2.584in, height 0.82in) at the method card heights;
    - the result-views table is stretched to the method full-width bottom band
      (3.00in -> 12.834in).

FIDELITY NOTE
  This is a drop-in slide module: it declares LAYOUT, CHARTS, _body(), and
  render(), and returns a complete slide XML string through body_slide(). No
  parsing syntax, workbook internals, or build-process mechanics appear in copy;
  every connector is axis-aligned (a horizontal line or a bentConnector3 elbow),
  never a diagonal; the gate is a rectangle, never a hexagon.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, run,
    table, tcell, text_box, trow,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_4 = "3D5972"
BLUE_5 = "263746"           # method-module Confidence Gate fill (darker than BLUE_4)
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_TX = "595959"           # muted caption / subcaption text
RULE = "BFBFBF"              # thin within-table row divider
RED = "C00000"
FONT = "Arial"
NO_BORDER = "none"

LAYOUT = "slideLayout4"

CHARTS: list = []
IMAGES: list = []


# ════════════════════════════════════════════════════════════════════════════
# Method-footprint anchors (from ddg51_hull_linkage_method). Keeping these as
# named constants is what guarantees the gate column and card column line up.
# ════════════════════════════════════════════════════════════════════════════
EVID_L = 3.000          # diagram left edge (== method body content left)
NODE_R = 7.100          # right edge of the evidence-node column (gate's left neighbour)
GATE_L = 7.690          # gate left edge — centred in the NODE_R -> CARD_L gap
GATE_R = 9.660          # gate right edge (= GATE_L + method gate width 1.97)
GATE_MID_Y = 3.385      # gate vertical centre (single feed in / single fan out)
TRUNK_X = 10.030        # vertical outcome trunk between the gate and the cards
CARD_L = 10.250         # outcome-card left edge (method card column)
CONTENT_R = 12.834      # shared right edge (== BODY right margin; nothing past it)


# ════════════════════════════════════════════════════════════════════════════
# Semantic geometry / data records (v4 grammar).
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


COPY_RULES: tuple[str, ...] = (
    "Keep visible copy at the evidence level; never expose parsing or workbook mechanics.",
    "Assign an exact hull only when the contract-family signal and a direct order-level signal agree.",
    "Let colour intensity carry the confidence tier: dark = assigned, pale = inferred, red = held out.",
    "Treat order-level hull fields as the strongest signal and requirement text as a weaker, family-level signal.",
    "State the attribution boundary explicitly: subaward evidence places hull / SWBS / vendor / timing, not physical module / block.",
    "Route every cross-row connector as an orthogonal bentConnector3 or a pure horizontal line; the gate is a rectangle.",
)

FLOW_GRAMMAR = {
    "layer_a": "Prime PIID -> candidate hull family (single-ship contract or MYP hull family)",
    "layer_b": "subaward order text -> order-level hull mention (strong) + requirement-text mention (weak)",
    "gate": "two independent layers weighed; no forced assignment",
    "outcomes": "A/B exact hull | C/D family-level | X exception queue",
}


# ════════════════════════════════════════════════════════════════════════════
# Paint helpers (v4).
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
    # Font treatment mirrors the evidence nodes (_draw_node): a plain PT10 primary
    # line over a PT8 italic secondary line — not a bold grade.
    runs = (
        RunSpec(card.grade, PT(10), card.text_color),
        RunSpec(card.result, PT(8), card.text_color, italic=True, break_before=True),
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
# Zone 1 — Left approach rail (v4 plain numbered steps) at the method rail
# anchors: header flush at 0.522in, steps flush at 0.700in / 2.050in wide.
# ════════════════════════════════════════════════════════════════════════════
RAIL_HDR_X = 0.522
RAIL_HDR_W = 2.250
RAIL_X = 0.700
RAIL_W = 2.050

RAIL_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(RAIL_HDR_X, 1.340, RAIL_HDR_W, 0.250), (RunSpec("Approach steps", PT(10), BLACK, italic=True),), align=None)
RAIL_UNDERLINE = ConnectorSpec("approach_header_rule", "ApproachUnderline", Box(RAIL_HDR_X, 1.606, RAIL_HDR_W, 0.002), DK, 12700, arrow=False, prst="line", flip_h=True)

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(1, Box(RAIL_X, 1.675, RAIL_W, 0.540), "Define DDG subaward universe"),
    StepCard(2, Box(RAIL_X, 2.365, RAIL_W, 0.540), "Map prime contract to candidate hull family"),
    StepCard(3, Box(RAIL_X, 3.055, RAIL_W, 0.540), "Read order-level hull mentions"),
    StepCard(4, Box(RAIL_X, 3.745, RAIL_W, 0.540), "Compare hull evidence to contract family"),
    StepCard(5, Box(RAIL_X, 4.435, RAIL_W, 0.540), "Assign confidence tier and roll up exact matches"),
)


# ════════════════════════════════════════════════════════════════════════════
# Zone 2 — Centre evidence diagram (v4 shapes), compressed so the gate sits
# centred in the gap between the evidence nodes and the outcome cards. Anchors:
#   source col   x=3.00 w=1.85  (right 4.85)
#   evidence col x=5.15 w=1.95  (right 7.10 == NODE_R)
#   gate         x=7.69 w=1.97  (right 9.66)  — 0.59in clear on each side
# ════════════════════════════════════════════════════════════════════════════
DIAGRAM_HEADER = TextSpec("diagram_header", "EvidenceHeader", Box(EVID_L, 1.340, 3.000, 0.250), (RunSpec("Evidence evaluation", PT(10), BLACK, italic=True),), align=None)
DIAGRAM_UNDERLINE = ConnectorSpec("diagram_header_rule", "EvidenceUnderline", Box(EVID_L, 1.606, 3.000, 0.002), DK, 12700, arrow=False, prst="line", flip_h=True)

LANE_A_LABEL = TextSpec("lane_label", "LayerALabel", Box(EVID_L, 1.960, 2.100, 0.300), (RunSpec("Layer A — Contract family", PT(10), DK, italic=True),), align=None)
LANE_B_LABEL = TextSpec("lane_label", "LayerBLabel", Box(EVID_L, 3.520, 2.100, 0.300), (RunSpec("Layer B — Hull evidence", PT(10), DK, italic=True),), align=None)

LANE_A_NODES: tuple[FlowNode, ...] = (
    FlowNode("source_node", Box(3.00, 2.30, 1.85, 0.42), BLACK, BLACK, WHITE, "Prime PIID"),
    FlowNode("evidence_node", Box(5.15, 2.30, 1.95, 0.42), BLUE_2, BLUE_4, BLACK, "Candidate hull family"),
)

LANE_A_SUBCHIPS: tuple[FlowNode, ...] = (
    FlowNode("subchip", Box(5.15, 2.82, 0.95, 0.34), GRAY_1, GRAY_2, BLACK, "Single-ship contract", size=PT(8)),
    FlowNode("subchip", Box(6.15, 2.82, 0.95, 0.34), GRAY_1, GRAY_2, BLACK, "MYP hull family", size=PT(8)),
)

LANE_B_NODES: tuple[FlowNode, ...] = (
    FlowNode("source_node", Box(3.00, 4.04, 1.85, 0.52), BLACK, BLACK, WHITE, "Subaward order text"),
    FlowNode("evidence_node", Box(5.15, 3.74, 1.95, 0.52), BLUE_2, BLUE_4, BLACK, "Order-level hull mention", "Strongest direct signal"),
    FlowNode("evidence_node", Box(5.15, 4.34, 1.95, 0.52), BLUE_1, BLUE_4, BLACK, "Requirement-text mention", "Family-level signal"),
)

# Confidence gate — the method module's gate variation verbatim: darker BLUE_5
# fill, the three-line "Confidence Gate / Family + text align / No forced
# assignment" label (bold first line over italic rule lines), AND the method
# module's compact gate box (1.25in high, centred on GATE_MID_Y). The gate now
# carries the "no forced assignment" rule itself, so v4's separate dashed
# gate-rule note is dropped.
CONFIDENCE_GATE = TextSpec(
    "confidence_gate", "ConfidenceGate", Box(GATE_L, 2.760, GATE_R - GATE_L, 1.250),
    (
        RunSpec("Confidence Gate", PT(10), WHITE, bold=True),
        RunSpec("Family + text align", PT(9), WHITE, italic=True, break_before=True),
        RunSpec("No forced assignment", PT(9), WHITE, italic=True, break_before=True),
    ),
    fill=BLUE_5, line_color=DK, line_width=12700, align="ctr", anchor="ctr", prst="rect",
)

# Lane-A internal arrow: same row -> pure horizontal "line" (not diagonal).
LANE_A_ARROW = ConnectorSpec("lane_a_flow", "LaneAArrow", Box(4.85, 2.51, 0.30, 0.000), prst="line")

# Lane-B split: crooked elbow connectors (bentConnector3), no diagonal.
LANE_B_SPLIT: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("lane_b_flow", "LaneBToOrderLevel", Box(4.85, 4.00, 0.30, 0.30), prst="bentConnector3", flip_v=True),
    ConnectorSpec("lane_b_flow", "LaneBToRequirement", Box(4.85, 4.30, 0.30, 0.30), prst="bentConnector3"),
)

# Both lanes converge into the compact gate (left edge x=7.69) via crooked elbows,
# each entering within the gate's 2.76in -> 4.01in span.
CONVERGE: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("converge", "FamilyToGate", Box(NODE_R, 2.51, GATE_L - NODE_R, 0.59), prst="bentConnector3"),
    ConnectorSpec("converge", "OrderLevelToGate", Box(NODE_R, 3.65, GATE_L - NODE_R, 0.35), prst="bentConnector3", flip_v=True),
    ConnectorSpec("converge", "RequirementToGate", Box(NODE_R, 3.85, GATE_L - NODE_R, 0.75), prst="bentConnector3", flip_v=True),
)


# ════════════════════════════════════════════════════════════════════════════
# Zone 3 — Right outcome stack (v4 colour-intensity tiers), left-anchored at the
# method card column (x=10.25). Each card is sized to match the "Order-level hull
# mention" evidence node (1.95in x 0.52in); card centres stay on the trunk
# branch heights (2.14 / 3.335 / 4.52), so y = centre - 0.26in.
# ════════════════════════════════════════════════════════════════════════════
OUTCOME_W = 1.95   # match the evidence-node width
OUTCOME_H = 0.52   # match the evidence-node height

OUTCOME_CARDS: tuple[OutcomeCard, ...] = (
    OutcomeCard("outcome_assigned", Box(CARD_L, 1.880, OUTCOME_W, OUTCOME_H), DK, DK, WHITE, "A / B — Exact hull", "Assigned to hull"),
    OutcomeCard("outcome_family", Box(CARD_L, 3.075, OUTCOME_W, OUTCOME_H), BLUE_1, BLUE_4, BLACK, "C / D — Family-level", "Retained at contract family"),
    OutcomeCard("outcome_exception", Box(CARD_L, 4.260, OUTCOME_W, OUTCOME_H), WHITE, RED, RED, "X — Exception queue", "Held out of roll-up", dashed=True, line_width=19050),
)

# Gate -> outcomes: the compact gate fans out through one feed into a vertical
# trunk (x=10.03) that branches to the three cards at their vertical centres
# (2.14 / 3.335 / 4.52). The exception branch is red.
GATE_TO_OUTCOME: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("gate_trunk", "GateToOutcomeTrunk", Box(GATE_R, GATE_MID_Y, TRUNK_X - GATE_R, 0.000), prst="line", arrow=False),
    ConnectorSpec("gate_trunk", "OutcomeTrunk", Box(TRUNK_X, 2.140, 0.000, 2.380), prst="line", arrow=False),
    ConnectorSpec("gate_branch", "OutcomeBranchAB", Box(TRUNK_X, 2.140, CARD_L - TRUNK_X, 0.000), prst="line"),
    ConnectorSpec("gate_branch", "OutcomeBranchCD", Box(TRUNK_X, 3.335, CARD_L - TRUNK_X, 0.000), prst="line"),
    ConnectorSpec("gate_branch", "OutcomeBranchX", Box(TRUNK_X, 4.520, CARD_L - TRUNK_X, 0.000), prst="line", color=RED),
)


# ════════════════════════════════════════════════════════════════════════════
# Bottom — downstream result views: a stretched-out, vertically-short rebuild of
# the "Downstream result views" table from ``ddg_subaward_hull_linkage_results``,
# on the method full-width bottom band (3.00in -> 12.834in).
# ════════════════════════════════════════════════════════════════════════════
RESULT_VIEWS_HEADER = TextSpec(
    "grid_caption", "ResultViewsCaption", Box(EVID_L, 5.250, 4.400, 0.210),
    (RunSpec("Downstream result views", PT(10), DK, italic=True),),
    align=None,
)
RESULT_VIEWS_SUBHEADER = TextSpec(
    "grid_subcaption", "ResultViewsSubcaption", Box(7.400, 5.250, CONTENT_R - 7.400, 0.210),
    (RunSpec("Built from the linked subaward rows", PT(8.5), GRAY_TX, italic=True),),
    align="r",
)

RESULT_VIEWS_BOX = Box(EVID_L, 5.510, CONTENT_R - EVID_L, 1.020)
RESULT_VIEWS_COLS = (3.050, 3.680, CONTENT_R - EVID_L - 3.050 - 3.680)
RESULT_VIEWS_HEADERS = ("Result view", "What enters", "What it supports")
RESULT_VIEWS_ROWS = (
    ("Exact-hull spend summary", "A/B rows only", "Hull-level spend readout"),
    ("Vendor × Hull exposure", "1,193 rows · 281 vendors · 24 hulls", "Supplier exposure by assigned hull"),
    ("Vendor × Hull × SWBS", "1,296 rows · HII-Ingalls only", "Functional-system view by hull"),
    ("Exception queue", "63 rows", "Human review; excluded from hull roll-ups"),
)

FOOTNOTE = TextSpec(
    "footnote", "OutcomeFootnote", Box(0.495, 6.660, 12.340, 0.300),
    (RunSpec("Note: A and B populate an assigned hull; C and D are inferred at the contract family; X is multi-hull or conflicting and is held out of the roll-up.", PT(9), BLACK),),
    align=None,
)


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


def paint_outcome_stack(out: list[str], n) -> None:
    for c in GATE_TO_OUTCOME:
        _draw_connector(out, n, c)
    for card in OUTCOME_CARDS:
        _draw_outcome(out, n, card)


def _rv_cell(text, *, bold=False, **edges):
    return tcell(
        text, bold=bold or None, size=PT(9), color=BLACK, align="l", anchor="ctr",
        font=FONT, l_ins=45_720, r_ins=45_720, t_ins=18_000, b_ins=18_000,
        borders=_border(**edges),
    )


def paint_result_views(out: list[str], n) -> None:
    _draw_text(out, n, RESULT_VIEWS_HEADER)
    _draw_text(out, n, RESULT_VIEWS_SUBHEADER)
    rows = [trow(
        [_rv_cell(h, bold=True, B=_edge(DK)) for h in RESULT_VIEWS_HEADERS],
        h=IN(0.220),
    )]
    last = len(RESULT_VIEWS_ROWS) - 1
    for i, (rv, we, ws) in enumerate(RESULT_VIEWS_ROWS):
        rule = {} if i == last else {"B": _edge(RULE, 6_350)}
        rows.append(trow([
            _rv_cell(rv, bold=True, **rule),
            _rv_cell(we, **rule),
            _rv_cell(ws, **rule),
        ], h=IN(0.200)))
    out.append(table(
        n(), "ResultViewsTable", *RESULT_VIEWS_BOX.emu(),
        col_widths=[IN(w) for w in RESULT_VIEWS_COLS],
        rows=rows,
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
    paint_result_views(out, n)
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
