"""Teaching exemplar: DDG hull-linkage methodology evidence gate.

ROLE
  methodology_flow / hull_linkage_confidence_gate

USE WHEN
  A slide needs to explain a controlled analytical method that assigns exact hulls
  only when independent contract-family evidence and hull-text evidence align.

TEACHES
  - five-card left approach rail copied from the TCV approach family
  - two evidence lanes converging into a central confidence gate via an
    ORTHOGONAL collector manifold (horizontal stubs -> vertical collector ->
    one feed arrow), mirroring the gate's outbound trunk/branch manifold
  - direct order-level hull mentions treated as the strongest evidence signal
  - weaker requirement-text mentions retained as family-level evidence
  - right-hand A/B, C/D, X outcome stack with exception treatment
  - compact construction-hierarchy mini-table distinguishing supported vs.
    unsupported attribution levels

CONNECTOR GRAMMAR
  Every connector is axis-aligned (cx == 0 OR cy == 0): there are no diagonal
  lines. Convergence and divergence are drawn as right-angle manifolds, not as
  point-to-point diagonals. A feed that must change rows turns at a collector or
  trunk, never on a slope. The evidence lanes collect onto a vertical bus at
  COLLECTOR_X and feed the gate with a single horizontal arrow; the gate fans out
  through a vertical trunk at TRUNK_X to the three outcome cards.

TEXT-FIT PRECEDENT
  approach_rail:
    geometry: 2.05in wide x 0.54in high cards
    type: Arial 10pt, left aligned, 100% line spacing
    content: one verb-first method step per card
    copy_when: the slide needs to teach a method beside a flow diagram

  evidence_nodes:
    geometry: 1.43-1.52in wide x 0.42in high nodes on a 2-column grid
    type: Arial 9-10pt centered
    content: short evidence labels, not implementation mechanics
    copy_when: the flow describes evidence layers rather than numeric calculations

  outcome_stack:
    geometry: 2.58in wide x 0.82in high cards
    type: Arial 10-16pt mixed runs
    content: confidence tier plus one assignment outcome
    copy_when: a method needs an executive-readable output taxonomy

SOURCE NOTE
  Authored from the project source-file grammar rather than a converted source
  slide. Primary visual precedents are `tcv_approach_iamd.py` for the left rail,
  filter/gate logic, right-angle route connectors, and right output stack;
  `tcv_approach_usv.py` / `tcv_approach_manned.py` for compact approach cards;
  and `definitions_market_levels.py` for pairing a conceptual diagram with a
  short formal reference table.
"""

from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, run, table, tcell,
    text_box, trow,
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
RULE_GRAY = "808080"
RED = "C00000"
RED_TINT = "FCE4E4"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

NO_BORDER = "none"

# -- Shared horizontal anchors for the orthogonal evidence/outcome manifolds ----
# Right edge shared by the right-hand evidence-node column; the collector bus and
# the gate sit to its right, the outcome trunk to the gate's right. Keeping these
# as named constants is what guarantees the feeds stay axis-aligned.
NODE_R = 6.650          # right edge of the right-hand evidence column
COLLECTOR_X = 6.950     # vertical collector bus between the lanes and the gate
GATE_L = 7.300          # gate left edge
GATE_R = 9.270          # gate right edge
GATE_MID_Y = 3.385      # gate vertical centre (feed in / fan out height)
TRUNK_X = 10.030        # vertical outcome trunk between the gate and the cards
CARD_L = 10.250         # outcome-card left edge
CONTENT_R = 12.834      # shared right edge (== BODY right margin; nothing past it)


@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU only at primitive boundaries."""

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
    line_width: int = 3_175
    align: str | None = "ctr"
    anchor: str = "ctr"
    prst: str = "rect"
    dashed_line: bool = False
    wrap: str = "square"
    l_ins: int | None = None
    t_ins: int | None = None
    r_ins: int | None = None
    b_ins: int | None = None


@dataclass(frozen=True)
class MethodCard:
    label: str
    box: Box


@dataclass(frozen=True)
class EvidenceNode:
    role: str
    label: tuple[str, ...]
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str = BLACK
    line_width: int = 3_175
    font_pt: float = 10
    bold_first: bool = False
    italic_second: bool = False
    dashed_line: bool = False


@dataclass(frozen=True)
class ConnectorSpec:
    name: str
    box: Box
    color: str = BLACK
    width: int = 12_700
    arrow: bool = False
    prst: str = "line"
    dashed: bool = False
    flip_h: bool = False
    flip_v: bool = False
    rot: int = 0
    adj: dict[str, str] | None = None


@dataclass(frozen=True)
class OutcomeCard:
    tier: str
    label: str
    outcome: str
    box: Box
    fill: str | None
    line_color: str
    tier_color: str
    text_color: str
    line_width: int = 12_700
    dashed_line: bool = False


TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_rail", Box(0.700, 1.675, 2.050, 3.310), "Arial 10pt; verb-first labels only", "copy for compact methodology spines"),
    TextFitZone("evidence_nodes", Box(3.000, 1.675, 6.700, 3.230), "Arial 9-10pt centered evidence labels on a 2-col grid", "copy for two-layer evidence-gate diagrams"),
    TextFitZone("outcome_stack", Box(10.250, 1.730, 2.584, 3.200), "A/B dark, C/D pale, X exception tint", "copy for confidence-tier output taxonomies"),
    TextFitZone("hierarchy_note", Box(3.000, 5.550, 9.834, 0.730), "Arial 10pt mini reference table", "copy when a method needs an explicit attribution boundary"),
)

COPY_RULES: tuple[str, ...] = (
    "Keep visible copy at the evidence level: contract family, hull mention, signal, confidence tier.",
    "Treat direct order-level hull mentions as the strongest evidence; use requirement text as weaker family-level signal.",
    "Only A/B exact hull outcomes should read as assigned; C/D stays family-level and X stays visibly outside the roll-up.",
    "Do not introduce parsing syntax, workbook references, or build-process mechanics into the slide body.",
    "Draw convergence and divergence as right-angle manifolds (collector bus / trunk), never as diagonal point-to-point lines.",
)

FLOW_GRAMMAR = {
    "evidence_layers": "PIID contract family + direct hull text",
    "confidence_gate": "assign exact hull only when family and order evidence align",
    "outcomes": "A/B exact hull; C/D family-level; X exception queue",
    "attribution_boundary": "subaward evidence supports hull / SWBS / vendor / timing, not physical module attribution",
}


# ════════════════════════════════════════════════════════════════════════════
# Layout zones and slide content.
# ════════════════════════════════════════════════════════════════════════════
RAIL_HEADER = TextSpec(
    "approach_header",
    "ApproachRailHeader",
    Box(0.522, 1.340, 2.250, 0.250),
    (RunSpec("Methodology steps", PT(10), DK, italic=True),),
    align=None,
)
RAIL_RULE = ConnectorSpec("ApproachRailHeaderRule", Box(0.522, 1.606, 2.250, 0.000), DK, 12_700, False)
RAIL_SPINE = ConnectorSpec("ApproachRailSpine", Box(0.586, 1.824, 0.000, 3.130), RULE_GRAY, 6_350, True)

METHOD_CARDS: tuple[MethodCard, ...] = (
    MethodCard("Define DDG subaward universe", Box(0.700, 1.675, 2.050, 0.540)),
    MethodCard("Map prime contract to candidate hull family", Box(0.700, 2.365, 2.050, 0.540)),
    MethodCard("Read order-level hull mentions", Box(0.700, 3.055, 2.050, 0.540)),
    MethodCard("Compare hull evidence to contract family", Box(0.700, 3.745, 2.050, 0.540)),
    MethodCard("Assign confidence tier and roll up exact matches", Box(0.700, 4.435, 2.050, 0.540)),
)

# Lane panels are light backgrounds; they paint before connectors and nodes.
# Panel A is sized to contain its sub-labels; the gate bridges the two panels.
LANE_PANELS: tuple[TextSpec, ...] = (
    TextSpec("lane_panel", "ContractFamilyLanePanel", Box(3.000, 1.675, 6.620, 1.260), (), GRAY_1, NO_BORDER),
    TextSpec("lane_panel", "HullEvidenceLanePanel", Box(3.000, 3.035, 6.620, 1.870), (), "F7F9FB", NO_BORDER),
)

SECTION_LABELS: tuple[TextSpec, ...] = (
    TextSpec("section_label", "EvidenceSectionHeader", Box(3.000, 1.340, 6.620, 0.250), (RunSpec("Two independent evidence layers", PT(10), DK, italic=True),), align=None),
    TextSpec("section_label", "OutputSectionHeader", Box(10.250, 1.340, 2.584, 0.250), (RunSpec("Confidence outcome", PT(10), DK, italic=True),), align=None),
    TextSpec("section_label", "HierarchySectionHeader", Box(3.000, 5.290, 9.834, 0.250), (RunSpec("Construction hierarchy note", PT(10), DK, italic=True),), align=None),
)

LANE_LABELS: tuple[TextSpec, ...] = (
    TextSpec("lane_label", "LayerAHeader", Box(3.150, 1.820, 0.920, 0.290), (RunSpec("Layer A", PT(9), WHITE, bold=True),), BLUE_4, BLUE_4, align="ctr"),
    TextSpec("lane_label", "LayerATitle", Box(4.120, 1.820, 1.450, 0.290), (RunSpec("Contract family", PT(10), DK, bold=True),), None, NO_BORDER, align=None),
    TextSpec("lane_label", "LayerBHeader", Box(3.150, 3.180, 0.920, 0.290), (RunSpec("Layer B", PT(9), WHITE, bold=True),), BLUE_4, BLUE_4, align="ctr"),
    TextSpec("lane_label", "LayerBTitle", Box(4.120, 3.180, 1.450, 0.290), (RunSpec("Hull evidence", PT(10), DK, bold=True),), None, NO_BORDER, align=None),
)

# Two-column evidence grid: left column right-aligns at 4.820, right column at
# NODE_R (6.650), so every lane connector is the same 0.400in horizontal hop and
# every collector stub is the same 0.300in hop.
EVIDENCE_NODES: tuple[EvidenceNode, ...] = (
    EvidenceNode("contract_family", ("Prime PIID",), Box(3.300, 2.245, 1.520, 0.420), WHITE, DK, BLACK, 6_350, 10, True),
    EvidenceNode("contract_family", ("Candidate hull", "family"), Box(5.220, 2.245, 1.430, 0.420), BLUE_1, DK, BLACK, 6_350, 10, True),
    EvidenceNode("contract_sublabel", ("Single-ship contract",), Box(3.300, 2.690, 1.520, 0.220), None, NO_BORDER, RULE_GRAY, 3_175, 8, False, True),
    EvidenceNode("contract_sublabel", ("MYP hull family",), Box(5.220, 2.690, 1.430, 0.220), None, NO_BORDER, RULE_GRAY, 3_175, 8, False, True),
    EvidenceNode("hull_evidence", ("Order-level", "hull mention"), Box(3.300, 3.630, 1.520, 0.420), WHITE, DK, BLACK, 6_350, 10, True),
    EvidenceNode("hull_evidence", ("Strongest direct", "signal"), Box(5.220, 3.630, 1.430, 0.420), BLUE_2, DK, BLACK, 6_350, 10, True),
    EvidenceNode("hull_evidence_weak", ("Requirement-text", "mention"), Box(3.300, 4.295, 1.520, 0.420), WHITE, RULE_GRAY, BLACK, 3_175, 10, True, dashed_line=True),
    EvidenceNode("hull_evidence_weak", ("Family-level", "signal"), Box(5.220, 4.295, 1.430, 0.420), BLUE_1, RULE_GRAY, BLACK, 3_175, 10, True, dashed_line=True),
)

CONFIDENCE_GATE = EvidenceNode(
    "confidence_gate",
    ("Confidence Gate", "Family + text align", "No forced assignment"),
    Box(GATE_L, 2.760, GATE_R - GATE_L, 1.250),
    BLUE_5,
    DK,
    WHITE,
    12_700,
    10,
    True,
    True,
)

# Inbound collector manifold: each lane hops to the right column, a no-arrow stub
# carries it to the vertical collector bus, and a single arrow feeds the gate at
# its mid-height. The weak (family-level) line stays dashed up to the bus.
EVIDENCE_CONNECTORS: tuple[ConnectorSpec, ...] = (
    # within-lane hops (left column -> right column)
    ConnectorSpec("PrimePIIDToFamily", Box(4.820, 2.455, 0.400, 0.000), BLACK, 9_525, True),
    ConnectorSpec("OrderMentionToSignal", Box(4.820, 3.840, 0.400, 0.000), BLACK, 9_525, True),
    ConnectorSpec("RequirementTextToSignal", Box(4.820, 4.505, 0.400, 0.000), RULE_GRAY, 6_350, True, dashed=True),
    # stubs onto the collector bus (no arrowheads — these are joins)
    ConnectorSpec("FamilyStub", Box(NODE_R, 2.455, COLLECTOR_X - NODE_R, 0.000), BLACK, 9_525, False),
    ConnectorSpec("StrongSignalStub", Box(NODE_R, 3.840, COLLECTOR_X - NODE_R, 0.000), BLACK, 9_525, False),
    ConnectorSpec("FamilySignalStub", Box(NODE_R, 4.505, COLLECTOR_X - NODE_R, 0.000), RULE_GRAY, 6_350, False, dashed=True),
    # the collector bus, and the single feed into the gate
    ConnectorSpec("EvidenceCollectorBus", Box(COLLECTOR_X, 2.455, 0.000, 2.050), BLACK, 9_525, False),
    ConnectorSpec("CollectorToGate", Box(COLLECTOR_X, GATE_MID_Y, GATE_L - COLLECTOR_X, 0.000), BLACK, 9_525, True),
    # outbound trunk manifold: gate -> trunk -> three outcome branches
    ConnectorSpec("GateToOutcomeTrunk", Box(GATE_R, GATE_MID_Y, TRUNK_X - GATE_R, 0.000), BLACK, 9_525, False),
    ConnectorSpec("OutcomeTrunk", Box(TRUNK_X, 2.140, 0.000, 2.380), BLACK, 9_525, False),
    ConnectorSpec("OutcomeBranchAB", Box(TRUNK_X, 2.140, CARD_L - TRUNK_X, 0.000), BLACK, 9_525, True),
    ConnectorSpec("OutcomeBranchCD", Box(TRUNK_X, 3.335, CARD_L - TRUNK_X, 0.000), BLACK, 9_525, True),
    ConnectorSpec("OutcomeBranchX", Box(TRUNK_X, 4.520, CARD_L - TRUNK_X, 0.000), BLACK, 9_525, True),
)

OUTCOME_CARDS: tuple[OutcomeCard, ...] = (
    OutcomeCard("A/B", "Exact hull", "Assigned to hull", Box(CARD_L, 1.730, CONTENT_R - CARD_L, 0.820), BLUE_5, DK, WHITE, WHITE, 12_700),
    OutcomeCard("C/D", "Family-level", "Retained at contract family", Box(CARD_L, 2.925, CONTENT_R - CARD_L, 0.820), BLUE_1, BLUE_3, BLUE_4, BLACK, 6_350),
    OutcomeCard("X", "Exception queue", "Held out of roll-up", Box(CARD_L, 4.110, CONTENT_R - CARD_L, 0.820), RED_TINT, RED, RED, BLACK, 19_050, dashed_line=True),
)

HIERARCHY_TABLE = Box(3.000, 5.550, 9.834, 0.730)


# ════════════════════════════════════════════════════════════════════════════
# Drawing helpers.
# ════════════════════════════════════════════════════════════════════════════
def _shape_ids():
    return iter(range(100, 2000))


def _p(runs: tuple[RunSpec, ...], *, align: str | None = "ctr") -> str:
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
    return paragraph(pieces, align=align, line_spacing=100000)


def _draw_text(out: list[str], n, spec: TextSpec) -> None:
    kwargs = dict(
        fill=spec.fill,
        line_color=spec.line_color,
        line_width=spec.line_width,
        anchor=spec.anchor,
        prst=spec.prst,
        dashed_line=spec.dashed_line,
        wrap=spec.wrap,
    )
    if spec.l_ins is not None:
        kwargs["l_ins"] = spec.l_ins
    if spec.t_ins is not None:
        kwargs["t_ins"] = spec.t_ins
    if spec.r_ins is not None:
        kwargs["r_ins"] = spec.r_ins
    if spec.b_ins is not None:
        kwargs["b_ins"] = spec.b_ins
    out.append(text_box(n(), spec.name, *spec.box.emu(), [_p(spec.runs, align=spec.align)], **kwargs))


def _draw_connector(out: list[str], n, spec: ConnectorSpec) -> None:
    out.append(connector(
        n(),
        spec.name,
        *spec.box.emu(),
        color=spec.color,
        width=spec.width,
        arrow=spec.arrow,
        prst=spec.prst,
        dashed=spec.dashed,
        flip_h=spec.flip_h,
        flip_v=spec.flip_v,
        rot=spec.rot,
        adj=spec.adj,
    ))


def _draw_method_card(out: list[str], n, card: MethodCard) -> None:
    out.append(text_box(
        n(),
        "MethodCard",
        *card.box.emu(),
        [paragraph([run(card.label, size=PT(10), color=BLACK, font=FONT)], align=None, line_spacing=100000)],
        fill=WHITE,
        line_color=GRAY_3,
        line_width=3_175,
        anchor="ctr",
        l_ins=60_960,
        r_ins=45_720,
        t_ins=22_860,
        b_ins=22_860,
    ))


def _node_paragraphs(node: EvidenceNode) -> list[str]:
    paras: list[str] = []
    for i, label in enumerate(node.label):
        paras.append(paragraph(
            [run(
                label,
                size=PT(node.font_pt if i == 0 else max(node.font_pt - 1, 8)),
                color=node.text_color,
                bold=(node.bold_first and i == 0) or None,
                italic=(node.italic_second and i > 0) or None,
                font=FONT,
            )],
            align="ctr",
            line_spacing=100000,
        ))
    return paras


def _draw_evidence_node(out: list[str], n, node: EvidenceNode) -> None:
    out.append(text_box(
        n(),
        "EvidenceNode",
        *node.box.emu(),
        _node_paragraphs(node),
        fill=node.fill,
        line_color=node.line_color,
        line_width=node.line_width,
        anchor="ctr",
        dashed_line=node.dashed_line,
        l_ins=22_860,
        r_ins=22_860,
        t_ins=11_430,
        b_ins=11_430,
    ))


def _draw_outcome_card(out: list[str], n, card: OutcomeCard) -> None:
    paras = [
        paragraph([
            run(f"{card.tier} \u2014 ", size=PT(16), color=card.tier_color, bold=True, font=FONT),
            run(card.label, size=PT(12), color=card.text_color, bold=True, font=FONT),
        ], align="ctr", line_spacing=100000),
        paragraph([run(card.outcome, size=PT(10), color=card.text_color, font=FONT)], align="ctr", line_spacing=100000),
    ]
    out.append(text_box(
        n(),
        "OutcomeCard",
        *card.box.emu(),
        paras,
        fill=card.fill,
        line_color=card.line_color,
        line_width=card.line_width,
        anchor="ctr",
        dashed_line=card.dashed_line,
        l_ins=22_860,
        r_ins=22_860,
        t_ins=22_860,
        b_ins=22_860,
    ))


# ── mini-table kit ──
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text: str, *, fill=None, color=BLACK, bold=False, italic=False, size=PT(10), align="ctr", **edges):
    return tcell(
        text,
        fill=fill,
        color=color,
        bold=bold or None,
        italic=italic or None,
        size=size,
        align=align,
        anchor="ctr",
        font=FONT,
        l_ins=45_720,
        r_ins=45_720,
        t_ins=22_860,
        b_ins=22_860,
        borders=bd(**edges),
    )


def _draw_hierarchy_table(out: list[str], n) -> None:
    half = round(HIERARCHY_TABLE.w / 2, 3)
    out.append(table(
        n(),
        "ConstructionHierarchyMiniTable",
        *HIERARCHY_TABLE.emu(),
        col_widths=[IN(half), IN(HIERARCHY_TABLE.w - half)],
        rows=[
            trow([
                cell("Supported by subaward evidence", fill=DK, color=WHITE, bold=True, size=PT(10), B=edge(WHITE, 6_350), R=edge(WHITE, 6_350)),
                cell("Not supported by subaward evidence", fill=GRAY_2, color=BLACK, bold=True, size=PT(10), B=edge(WHITE, 6_350)),
            ], h=IN(0.315)),
            trow([
                cell("Hull \u00b7 SWBS \u00b7 Vendor \u00b7 Timing", fill=BLUE_1, color=BLACK, size=PT(10), R=edge(WHITE, 6_350)),
                cell("Physical module \u00b7 Grand block \u00b7 Structural unit", fill=RED_TINT, color=BLACK, size=PT(10), L=edge(WHITE, 6_350)),
            ], h=IN(0.415)),
        ],
    ))


# ════════════════════════════════════════════════════════════════════════════
# Paint layers. Connectors are created before nodes so edges sit behind labels.
# ════════════════════════════════════════════════════════════════════════════
def paint_backgrounds_and_headers(out: list[str], n) -> None:
    for panel in LANE_PANELS:
        _draw_text(out, n, panel)
    for label in SECTION_LABELS:
        _draw_text(out, n, label)
    for label in LANE_LABELS:
        _draw_text(out, n, label)
    _draw_text(out, n, RAIL_HEADER)
    _draw_connector(out, n, RAIL_RULE)


def paint_connectors(out: list[str], n) -> None:
    _draw_connector(out, n, RAIL_SPINE)
    for spec in EVIDENCE_CONNECTORS:
        _draw_connector(out, n, spec)


def paint_approach_rail(out: list[str], n) -> None:
    for card in METHOD_CARDS:
        _draw_method_card(out, n, card)


def paint_evidence_gate(out: list[str], n) -> None:
    for node in EVIDENCE_NODES:
        _draw_evidence_node(out, n, node)
    _draw_evidence_node(out, n, CONFIDENCE_GATE)


def paint_outcome_stack(out: list[str], n) -> None:
    for card in OUTCOME_CARDS:
        _draw_outcome_card(out, n, card)


def paint_hierarchy_note(out: list[str], n) -> None:
    _draw_hierarchy_table(out, n)


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_backgrounds_and_headers(out, n)
    paint_connectors(out, n)
    paint_approach_rail(out, n)
    paint_evidence_gate(out, n)
    paint_outcome_stack(out, n)
    paint_hierarchy_note(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Methodology",
    topic="DDG Hull Linkage",
    title="DDG Hull Linkage Methodology",
    takeaway="Exact hulls are assigned only when contract family and order evidence align.",
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
