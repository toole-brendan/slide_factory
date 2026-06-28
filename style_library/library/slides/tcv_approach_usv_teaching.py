"""Teaching exemplar: Approach to find TCV — USV-specified.

ROLE
  market_sizing_flow / unmanned_usv_tcv

USE WHEN
  A slide needs to explain an unmanned-platform sizing method where platform-
  specified funding rolls directly into Total Funding, TAM, SAM, and Company TCV.

TEACHES
  - five-step approach rail that describes the author's method, not the math itself
  - left-to-right budget build-up with operator glyphs as calculation syntax
  - split between detailed worked chain and right-hand executive summary stack
  - four-state addressability legend kept as reusable scope grammar
  - tight 9pt node labels that stay variable-like rather than sentence-like

TEXT-FIT PRECEDENT
  approach_rail:
    geometry: 2.101in wide x 0.701in high cards
    type: Arial 10pt, left aligned, 100% line spacing
    content: one numbered verb-first method step per card
    copy_when: the slide needs to teach the methodology while the body shows the audit trail

  calculation_nodes:
    geometry: 1.519-2.549in wide x 0.359in high
    type: Arial 9pt, centered
    content: short variables such as Total Funding, TAM, SAM, Company TCV
    copy_when: the flow is a calculation, not a narrative process map

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_approach_usv.py`. The converter-era
  tuple buckets have been promoted into typed semantic records: `StepCard`,
  `FlowNode`, `LegendEntry`, `GlyphSpec`, and `ConnectorSpec`.

FIDELITY NOTE
  Coordinates, colors, logo relationship, and all original visible text are kept
  as source precedents. Paint order is now expressed through named `paint_*`
  layers so future authors can copy the pattern by role.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, picture, run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
GRAY_1 = "F2F2F2"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

CHARTS: list = []

SIZED_IN_ANOTHER_CAMPAIGN = "A6A6A6"
SCOPE_BLUE = "99B9D8"
PALE_SCOPE_BLUE = "CEDDEC"
SURFACE_BLUE = "447BB2"
RULE_GRAY = "808080"
NO_BORDER = "none"


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
    l_ins: int | None = None
    t_ins: int | None = None
    r_ins: int | None = None
    b_ins: int | None = None


@dataclass(frozen=True)
class StepCard:
    step: int
    box: Box
    label: str


@dataclass(frozen=True)
class FlowNode:
    role: str
    label: str
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str
    line_width: int = 3175
    size: int = PT(9)


@dataclass(frozen=True)
class MissionCell:
    role: str
    label: str
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str
    size: int = PT(9)


@dataclass(frozen=True)
class LegendEntry:
    label: str
    swatch: Box
    label_box: Box
    fill: str | None
    line_color: str | None
    label_align: str | None = "ctr"


@dataclass(frozen=True)
class GlyphSpec:
    role: str
    name: str
    box: Box
    prst: str
    rot: int = 0
    fill: str | None = BLACK
    line_color: str | None = BLACK
    line_width: int = 12700
    geom_adj: dict[str, str] | None = None


@dataclass(frozen=True)
class ConnectorSpec:
    role: str
    name: str
    box: Box
    color: str = BLACK
    width: int = 12700
    arrow: bool = False
    prst: str = "line"
    dashed: bool = False
    flip_h: bool = False
    flip_v: bool = False
    rot: int = 0
    adj: dict[str, str] | None = None


def _shape_ids():
    return iter(range(100, 2000))


def _p_from_runs(runs: tuple[RunSpec, ...], *, align: str | None = "ctr") -> str:
    body = []
    for spec in runs:
        if spec.break_before:
            body.append(line_break())
        body.append(run(
            spec.text,
            size=spec.size,
            color=spec.color,
            bold=spec.bold or None,
            italic=spec.italic or None,
            font=FONT,
        ))
    return paragraph(body, align=align, line_spacing=100000)


def _draw_text(out: list[str], n, spec: TextSpec) -> None:
    kwargs = dict(
        fill=spec.fill,
        line_color=spec.line_color,
        line_width=spec.line_width,
        anchor=spec.anchor,
        prst=spec.prst,
        rot=spec.rot,
        geom_adj=spec.geom_adj,
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
    out.append(text_box(n(), spec.name, *spec.box.emu(), [_p_from_runs(spec.runs, align=spec.align)], **kwargs))


def _draw_step(out: list[str], n, step: StepCard) -> None:
    _draw_text(out, n, TextSpec(
        "approach_step",
        "ApproachStep",
        step.box,
        (RunSpec(step.label, PT(10), BLACK),),
        align=None,
        line_color=NO_BORDER,
    ))


def _draw_flow_node(out: list[str], n, node: FlowNode) -> None:
    out.append(text_box(
        n(),
        "FlowNode",
        *node.box.emu(),
        [paragraph([run(node.label, size=node.size, color=node.text_color, font=FONT)], align="ctr", line_spacing=100000)],
        fill=node.fill,
        line_color=node.line_color,
        line_width=node.line_width,
        anchor="ctr",
    ))


def _draw_mission_cell(out: list[str], n, cell: MissionCell) -> None:
    out.append(text_box(
        n(),
        "MissionCell",
        *cell.box.emu(),
        [paragraph([run(cell.label, size=cell.size, color=cell.text_color, font=FONT)], align="ctr", line_spacing=100000)],
        fill=cell.fill,
        line_color=cell.line_color,
        line_width=3175,
        anchor="ctr",
    ))


def _draw_glyph(out: list[str], n, glyph: GlyphSpec) -> None:
    out.append(text_box(
        n(),
        glyph.name,
        *glyph.box.emu(),
        [paragraph([], align="ctr", line_spacing=100000)],
        fill=glyph.fill,
        line_color=glyph.line_color,
        line_width=glyph.line_width,
        prst=glyph.prst,
        rot=glyph.rot,
        geom_adj=glyph.geom_adj,
        anchor="ctr",
    ))


def _draw_connector(out: list[str], n, c: ConnectorSpec) -> None:
    out.append(connector(
        n(),
        c.name,
        *c.box.emu(),
        color=c.color,
        width=c.width,
        arrow=c.arrow,
        prst=c.prst,
        dashed=c.dashed,
        flip_h=c.flip_h,
        flip_v=c.flip_v,
        rot=c.rot,
        adj=c.adj,
    ))


def _draw_legend(out: list[str], n) -> None:
    for entry in ADDRESSABILITY_LEGEND:
        out.append(text_box(
            n(),
            "LegendSwatch",
            *entry.swatch.emu(),
            [paragraph([], align="ctr", line_spacing=100000)],
            fill=entry.fill,
            line_color=entry.line_color,
            line_width=3175,
            anchor="ctr",
        ))
    for entry in ADDRESSABILITY_LEGEND:
        out.append(text_box(
            n(),
            "LegendLabel",
            *entry.label_box.emu(),
            [paragraph([run(entry.label, size=PT(8), color=BLACK, font=FONT)], align=entry.label_align, line_spacing=100000)],
            fill=None,
            line_color=NO_BORDER,
            anchor="ctr",
            wrap="none",
        ))

IMAGES = [{"rId": "rId2", "file": "image8_3071a231.jpeg"}]

TEACHING_METADATA = {
    "role": "market_sizing_flow / unmanned_usv_tcv",
    "use_when": "USV-specified funding rolls into Total Funding, TAM, SAM, and Company TCV.",
    "teaches": (
        "method rail beside calculation body",
        "blue-gradient summary stack",
        "operator glyphs as visual math",
        "four-state addressability legend",
    ),
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_rail", Box(0.426, 1.593, 2.101, 3.756), "Arial 10pt; one method sentence per card", "copy for sizing-method spines"),
    TextFitZone("calculation_nodes", Box(3.003, 1.764, 9.975, 3.415), "Arial 9pt centered variable labels", "copy for TCV build-up nodes"),
    TextFitZone("legend_row", Box(7.764, 1.068, 5.209, 0.200), "8pt no-wrap legend labels", "copy for addressability keys"),
)

COPY_RULES: tuple[str, ...] = (
    "Use the left rail for author logic and the central body for calculation logic.",
    "Keep black boxes as inputs/factors; use the blue ramp only for calculated outputs.",
    "Use the right stack for the executive readout, even when the middle chain is dense.",
)

FLOW_GRAMMAR = {
    "inputs": ("sUSV", "mUSV", "USV Enabling Capabilities"),
    "budget_chain": "OBBBA items + Programs + Projects + Cost Elements = Total Funding",
    "conversion_chain": "Total Funding = TAM; TAM × unmanned adoption = SAM; SAM × share = Company TCV",
}

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(2, Box(0.426, 2.357, 2.101, 0.701), '2. Identify and sum corresponding budget items to find Total Funding'),
    StepCard(3, Box(0.426, 3.121, 2.101, 0.701), '3. Total Funding equals TAM'),
    StepCard(4, Box(0.426, 3.884, 2.101, 0.701), '4. Multiply by unmanned adoption rate to find SAM'),
    StepCard(1, Box(0.426, 1.593, 2.101, 0.701), '1. Identify applicable unmanned platforms'),
    StepCard(5, Box(0.426, 4.648, 2.101, 0.701), '5. Multiply by Saronic market share to find Company TCV'),
)

FOOTNOTE_NOTES: tuple[TextSpec, ...] = (
    TextSpec('footnote_note', 'Label', Box(0.495, 6.642, 12.367, 0.354), (RunSpec('Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)', PT(10), BLACK),), align=None, line_color='none'),
)

CALCULATION_NODES: tuple[FlowNode, ...] = (
    FlowNode('right_summary_stack', 'Total Funding ($)', Box(11.46, 2.528, 1.519, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(9)),
    FlowNode('right_summary_stack', 'TAM ($)', Box(11.46, 3.292, 1.519, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'Total Funding ($)', Box(3.003, 3.292, 2.549, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'TAM ($)', Box(3.003, 4.056, 2.549, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(9)),
    FlowNode('right_summary_stack', 'SAM ($)', Box(11.46, 4.056, 1.519, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(9)),
    FlowNode('right_summary_stack', 'Company TCV ($)', Box(11.46, 4.82, 1.519, 0.359), BLUE_4, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Cost Elements ($)', Box(9.106, 2.528, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'SAM ($)', Box(3.003, 4.819, 2.549, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Saronic market share (%)', Box(8.088, 4.819, 2.548, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'OBBBA items ($)', Box(3.003, 2.528, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'USV Enabling Capabilities', Box(10.429, 1.764, 2.549, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
)

ADDRESSABILITY_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Included in sizing", Box(7.764, 1.068, 0.200, 0.200), Box(7.987, 1.068, 1.068, 0.200), BLACK, BLACK, "ctr"),
    LegendEntry("Sized in another campaign", Box(9.078, 1.068, 0.200, 0.200), Box(9.301, 1.068, 1.448, 0.200), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, None),
    LegendEntry("Future effort", Box(10.773, 1.068, 0.200, 0.200), Box(10.996, 1.068, 0.817, 0.200), GRAY_1, GRAY_1, None),
    LegendEntry("Non-addressable", Box(11.836, 1.068, 0.200, 0.200), Box(12.060, 1.068, 0.913, 0.200), None, GRAY_3, "ctr"),
)

PLATFORM_INPUTS: tuple[TextSpec, ...] = (
    TextSpec("platform_input", "sUSVInput", Box(3.003, 1.764, 2.549, 0.359), (RunSpec("sUSV ", PT(9), WHITE), RunSpec("(incl. Corsair- and Mirage-equivalent platforms)", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("platform_input", "mUSVInput", Box(6.716, 1.764, 2.549, 0.359), (RunSpec("mUSV", PT(9), WHITE),), BLACK, BLACK),
)

BUDGET_AND_CONVERSION_BOXES: tuple[TextSpec, ...] = (
    TextSpec("budget_factor", "Programs", Box(5.037, 2.528, 1.519, 0.359), (RunSpec("Programs ($)", PT(9), WHITE), RunSpec("1", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("conversion_factor", "AdoptionRate", Box(8.088, 4.056, 2.548, 0.359), (RunSpec("Unmanned adoption (%)", PT(9), WHITE), RunSpec("Rate: 100% ", PT(9), WHITE, italic=True, break_before=True)), BLACK, BLACK),
    TextSpec("budget_factor", "Projects", Box(7.072, 2.528, 1.519, 0.359), (RunSpec("Projects ($)", PT(9), WHITE), RunSpec(" 1", PT(9), WHITE)), BLACK, BLACK),
)

SUMMARY_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("summary_arrow", "Connector: Elbow 63", Box(8.045, -0.882, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_arrow", "Connector: Elbow 64", Box(8.045, -0.118, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_arrow", "Connector: Elbow 65", Box(8.045, 0.646, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
)

BRACES: tuple[GlyphSpec, ...] = (
    GlyphSpec("grouping_brace", "Left Brace 69", Box(7.811, -2.673, 0.359, 9.975), "leftBrace", 16200000, None, BLACK, geom_adj={"adj1": "val 8333", "adj2": "val 7206"}),
    GlyphSpec("grouping_brace", "Left Brace 70", Box(7.811, -2.673, 0.359, 9.975), "leftBrace", 16200000, None, BLACK, 3175, {"adj1": "val 8333", "adj2": "val 68631"}),
)

APPROACH_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(0.425, 1.229, 2.101, 0.359), (RunSpec("Approach steps", PT(10), BLACK, italic=True),), line_color=NO_BORDER, align=None)
APPROACH_UNDERLINE = ConnectorSpec("approach_header_rule", "Approach underline", Box(0.426, 1.586, 2.100, 0.002), DK, 12700, flip_h=True)
SCOPE_CHIP = TextSpec("scope_chip", "ScopeChip", Box(9.353, 0.137, 2.200, 0.375), (RunSpec("Unmanned-specified", PT(10), DK, bold=True),), SCOPE_BLUE, DK)


def paint_approach_rail(out: list[str], n) -> None:
    for step in APPROACH_STEPS:
        _draw_step(out, n, step)
    for note in FOOTNOTE_NOTES:
        _draw_text(out, n, note)


def paint_calculation_nodes(out: list[str], n) -> None:
    for node in CALCULATION_NODES:
        _draw_flow_node(out, n, node)


def paint_inputs_and_factors(out: list[str], n) -> None:
    for spec in PLATFORM_INPUTS:
        _draw_text(out, n, spec)
    _draw_text(out, n, BUDGET_AND_CONVERSION_BOXES[0])


def paint_operator_system(out: list[str], n) -> None:
    for y in (2.507, 3.271, 4.035, 4.799):
        _draw_glyph(out, n, GlyphSpec("equals_column", "Equals", Box(10.843, y, 0.400, 0.400), "mathEqual"))
    _draw_glyph(out, n, GlyphSpec("sam_conversion_plus", "Plus Sign 59", Box(6.620, 4.035, 0.400, 0.400), "mathPlus", 2572505))
    _draw_text(out, n, BUDGET_AND_CONVERSION_BOXES[1])
    for c in SUMMARY_CONNECTORS:
        _draw_connector(out, n, c)
    _draw_glyph(out, n, GlyphSpec("tcv_conversion_plus", "Plus Sign 66", Box(6.620, 4.799, 0.400, 0.400), "mathPlus", 2572505))
    for brace in BRACES:
        _draw_glyph(out, n, brace)
    _draw_text(out, n, BUDGET_AND_CONVERSION_BOXES[2])
    for x in (6.614, 8.648, 4.579):
        _draw_glyph(out, n, GlyphSpec("budget_sum_plus", "Plus", Box(x, 2.507, 0.300, 0.300), "mathPlus", 5400000))
    _draw_text(out, n, APPROACH_HEADER)
    _draw_connector(out, n, APPROACH_UNDERLINE)


def paint_legend_scope_and_logo(out: list[str], n) -> None:
    _draw_legend(out, n)
    _draw_text(out, n, SCOPE_CHIP)
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_approach_rail(out, n)
    paint_calculation_nodes(out, n)
    paint_inputs_and_factors(out, n)
    paint_operator_system(out, n)
    paint_legend_scope_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Surface incl. MDA)",
    title="Approach to find TCV",
    takeaway="USV-specified",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
