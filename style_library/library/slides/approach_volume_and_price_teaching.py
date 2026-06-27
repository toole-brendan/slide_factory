"""Teaching exemplar: Approach (2/2) — volume and price build-up.

ROLE
  market_sizing_flow / two_track_volume_price_build

USE WHEN
  A slide must teach how volume inputs and price inputs roll up into an
  annual, mix-weighted $/TEU estimate.

TEACHES
  - two parallel calculation tracks: Volume and Price
  - operator glyph choreography using =, +, ×, and ÷ as visual math
  - green formula boxes versus gray/outline input boxes
  - dashed repeat frames for cargo-type / route repetition
  - Preliminary callouts as method caveats, not flow nodes

TEXT-FIT PRECEDENT
  formula_nodes:
    geometry: 2.6in wide x 0.35in high
    type: Arial 10pt centered, usually one formula label
    copy_when: a calculation node names a variable rather than a finding

  repeat_frames:
    geometry: large dashed boxes behind repeated formula groups
    type: no-fill frame plus one italic caption
    copy_when: the same calculation repeats across cargo types, routes, programs, or platforms

SOURCE NOTE
  Teaching rewrite of source-faithful `approach_volume_and_price.py`. The
  formula diagram is now expressed through typed records for operators,
  nodes, tracks, legends, callouts, and connector routes.

FIDELITY NOTE
  Coordinates, colors, table headers, callout geometry, and paint order are
  preserved. The teaching layer makes the two-track grammar copyable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.authoring import (
    IN,
    PT,
    BLACK,
    WHITE,
    DK,
    PRELIM,
    BLUE_3,
    BLUE_5,
    GRAY_1,
    FONT,
    slide,
    run,
    paragraph,
    line_break,
    text_box,
    connector,
    table,
    trow,
    tpara,
    trun,
    rcell,
    edge,
    breadcrumb,
    title_placeholder,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []

GREEN_FORMULA = "2E7D32"
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
class FormulaNode:
    role: str
    label: str
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str


@dataclass(frozen=True)
class OperatorGlyph:
    role: str
    box: Box
    prst: str
    rot: int = 0
    line_color: str | None = WHITE


@dataclass(frozen=True)
class TrackLabel:
    label: str
    box: Box


@dataclass(frozen=True)
class LegendEntry:
    """A color-key chip in the top legend row. Its visible caption is the
    adjacent TrackLabel (Price ($) / Volume (#) / Proportions (%)); in the
    source the chip itself carries no text."""
    swatch: Box
    fill: str | None
    line_color: str | None


@dataclass(frozen=True)
class CalloutSpec:
    name: str
    box: Box
    text: str
    geom_adj: dict[str, str]
    align: str | None = None


@dataclass(frozen=True)
class ConnectorSpec:
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


def _plain(label: str, *, size: int = PT(10), color: str = BLACK, bold: bool = False, italic: bool = False, align: str | None = "ctr") -> str:
    return paragraph([run(label, size=size, color=color, bold=bold or None, italic=italic or None, font=FONT)], align=align, line_spacing=100000)


def _draw_node(out: list[str], n, node: FormulaNode) -> None:
    out.append(text_box(n(), "FormulaNode", *node.box.emu(), [_plain(node.label, color=node.text_color)], fill=node.fill, line_color=node.line_color, anchor="ctr"))


def _draw_operator(out: list[str], n, glyph: OperatorGlyph) -> None:
    out.append(text_box(n(), "OperatorGlyph", *glyph.box.emu(), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=glyph.line_color, prst=glyph.prst, anchor="ctr", rot=glyph.rot))


def _draw_connector(out: list[str], n, spec: ConnectorSpec) -> None:
    out.append(connector(n(), spec.name, *spec.box.emu(), color=spec.color, width=spec.width, arrow=spec.arrow, prst=spec.prst, dashed=spec.dashed, flip_h=spec.flip_h, flip_v=spec.flip_v, rot=spec.rot, adj=spec.adj))


TEACHING_METADATA = {
    "role": "market_sizing_flow / two_track_volume_price_build",
    "use_when": "Volume and price formulas roll up into a weighted-average $/TEU estimate.",
    "teaches": (
        "parallel volume and price tracks",
        "operator glyphs as math syntax",
        "green formula boxes vs gray/outline inputs",
        "repeat frames and Preliminary caveats",
    ),
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("formula_nodes", Box(0.495, 1.883, 12.300, 4.830), "Arial 10pt; compact formula labels", "copy for calculation diagrams"),
    TextFitZone("track_labels", Box(0.486, 1.163, 3.393, 0.236), "Arial 8pt, no-wrap", "copy for track-axis labels"),
    TextFitZone("callouts", Box(3.127, 2.481, 9.854, 3.959), "Arial 8pt italic", "copy for method caveats outside nodes"),
)

COPY_RULES: tuple[str, ...] = (
    "Use operators as syntax; do not over-label arrows when the formula is clear.",
    "Use dashed frames only to mark repeated method logic, not as generic emphasis.",
    "Keep assumptions in Preliminary callouts so formula nodes remain variable-like.",
)

FLOW_GRAMMAR = {
    "volume_track": "voyages × capacity × utilization = annual container volume",
    "price_track": "rates × TEU/FEU mix + surcharges = total weighted-average container price",
    "repetition": "repeat across cargo types, routes, and vessels",
}

VOLUME_AND_MIX_INPUTS: tuple[FormulaNode, ...] = (
    FormulaNode('volume_input', 'Annual voyage count (#)', Box(0.495, 2.566, 2.6, 0.35), GRAY_1, BLACK, BLACK),
    FormulaNode('volume_input', 'Vessel capacity (#)', Box(0.495, 3.249, 2.6, 0.35), GRAY_1, BLACK, BLACK),
    FormulaNode('volume_input', 'Vessel utilization (%)', Box(0.495, 4.615, 2.6, 0.35), None, BLACK, BLACK),
    FormulaNode('volume_input', 'Annual container volume (#) ', Box(0.495, 5.297, 2.6, 0.35), GRAY_1, BLACK, BLACK),
    FormulaNode('mix_input', 'FEU proportion of cargo type (%)', Box(7.314, 2.566, 2.6, 0.35), None, BLACK, BLACK),
    FormulaNode('mix_input', 'TEU proportion of cargo type (%)', Box(3.914, 2.566, 2.6, 0.35), None, BLACK, BLACK),
    FormulaNode('mix_input', 'Cargo type proportion of total volume (%)', Box(5.614, 4.615, 2.6, 0.35), None, BLACK, BLACK),
    FormulaNode('volume_input', 'Annual vessel capacity (#)', Box(0.495, 3.932, 2.6, 0.35), GRAY_1, BLACK, BLACK),
    FormulaNode('volume_input', 'Annual voyage count (#)', Box(0.495, 5.98, 2.6, 0.35), GRAY_1, BLACK, BLACK),
    FormulaNode('volume_input', 'Avg. container volume per voyage (#)', Box(0.495, 6.663, 2.6, 0.35), GRAY_1, BLACK, BLACK),
)

PRICE_FORMULAS: tuple[FormulaNode, ...] = (
    FormulaNode("price_formula", 'Fuel surcharge ($ / TEU)', Box(10.195, 3.932, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Avg. TEU basic ocean rate within cargo type ($ / TEU)', Box(3.914, 1.883, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Avg. FEU container rate within cargo type, normalized to TEU ($ / TEU)', Box(7.314, 1.883, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Wharfage / Other Fees ($ / TEU)', Box(10.195, 4.615, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Mix-weighted FEU basic ocean rate, normalized to TEU ($ / TEU)', Box(7.314, 3.249, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Surcharge (%)', Box(8.762, 5.297, 1.228, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Volume-weighted avg. basic ocean rate ($ / TEU)', Box(5.614, 5.297, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", 'Ancillary charges ($ / TEU)', Box(5.614, 5.98, 2.6, 0.35), GREEN_FORMULA, BLACK, WHITE),
)

SPECIAL_FORMULA_BOXES: tuple[FormulaNode, ...] = (
    FormulaNode("price_formula", "Mix-weighted avg. basic ocean rate ($ / TEU)", Box(5.614, 3.932, 2.600, 0.350), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", "Terminal Handling / Stevedoring ($ / TEU)", Box(10.195, 5.297, 2.600, 0.350), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("final_output", "Total weighted avg. container price ($ / TEU)", Box(3.914, 6.663, 6.000, 0.350), GREEN_FORMULA, BLACK, WHITE),
    FormulaNode("price_formula", "Mix-weighted TEU basic ocean rate ($ / TEU)", Box(3.914, 3.249, 2.600, 0.350), GREEN_FORMULA, BLACK, WHITE),
)

TRACK_LABELS: tuple[TrackLabel, ...] = (
    TrackLabel('Volume (#)', Box(1.727, 1.163, 0.752, 0.236)),
    TrackLabel('Price ($)', Box(0.709, 1.163, 0.626, 0.236)),
    TrackLabel('Proportions (%)', Box(2.895, 1.163, 0.984, 0.236)),
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(Box(0.486, 1.163, 0.231, 0.234), '2E7D32', BLACK),  # keys Price ($) track (green calc boxes)
    LegendEntry(Box(1.504, 1.163, 0.231, 0.234), GRAY_1, BLACK),    # keys Volume (#) track (gray inputs)
    LegendEntry(Box(2.671, 1.163, 0.231, 0.234), None, BLACK),      # keys Proportions (%) track (outline boxes)
)

CALCULATION_OPERATORS: tuple[OperatorGlyph, ...] = (
    OperatorGlyph("equals", Box(1.645, 4.981, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("equals", Box(5.064, 2.933, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("equals", Box(8.464, 2.933, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("equals", Box(6.764, 4.981, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("equals", Box(6.764, 6.347, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("equals", Box(1.645, 3.615, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("equals", Box(1.645, 6.347, 0.3, 0.3), "mathEqual", 0, NO_BORDER),
    OperatorGlyph("plus", Box(6.764, 3.26, 0.3, 0.3), "mathPlus", 5400000, WHITE),
    OperatorGlyph("plus", Box(11.345, 4.298, 0.3, 0.3), "mathPlus", 5400000, WHITE),
    OperatorGlyph("plus", Box(11.345, 4.981, 0.3, 0.3), "mathPlus", 5400000, WHITE),
    OperatorGlyph("plus", Box(6.764, 5.664, 0.3, 0.3), "mathPlus", 5400000, WHITE),
    OperatorGlyph("multiply", Box(1.645, 2.933, 0.3, 0.3), "mathMultiply", 0, WHITE),
    OperatorGlyph("multiply", Box(8.464, 2.25, 0.3, 0.3), "mathMultiply", 0, WHITE),
    OperatorGlyph("multiply", Box(5.064, 2.25, 0.3, 0.3), "mathMultiply", 0, WHITE),
    OperatorGlyph("multiply", Box(8.338, 5.322, 0.3, 0.3), "mathMultiply", 0, WHITE),
    OperatorGlyph("multiply", Box(6.764, 4.298, 0.3, 0.3), "mathMultiply", 0, WHITE),
    OperatorGlyph("multiply", Box(1.645, 4.298, 0.3, 0.3), "mathMultiply", 0, WHITE),
)

FLOW_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("Connector: Elbow 52", Box(7.597, 2.915, 0.333, 1.700), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("Connector: Elbow 92", Box(5.897, 2.915, 0.333, 1.700), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("Connector: Elbow 97", Box(9.989, 4.107, 0.206, 1.365), BLACK, 12700, True, "bentConnector3", flip_v=True),
    ConnectorSpec("Connector: Elbow 136", Box(9.601, 4.260, 0.508, 3.282), BLACK, 12700, True, "bentConnector2", rot=5400000),
    ConnectorSpec("Straight Arrow Connector 143", Box(1.795, 2.233, 0.000, 0.333), BLACK, 12700, True),
    ConnectorSpec("Connector: Elbow 169", Box(0.495, 2.741, 0.014, 3.414), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=10800000, adj={"adj1": "val 1800000"}),
)

CALLOUTS: tuple[CalloutSpec, ...] = (
    CalloutSpec("Speech Bubble: Rectangle 105", Box(10.164, 2.481, 2.632, 0.738), "Finding mix-weighted rate required as TEU generally have higher basic ocean and terminal handling / stevedoring charges vs. normalized FEU", {"adj1": "val -59942", "adj2": "val 53401"}),
    CalloutSpec("Speech Bubble: Rectangle 139", Box(11.645, 5.814, 1.336, 0.626), "Also weighted by TEU/FEU mix and cargo composition ", {"adj1": "val 5870", "adj2": "val -74249"}, "ctr"),
    CalloutSpec("Speech Bubble: Rectangle 158", Box(3.127, 5.092, 1.521, 1.238), "Matson does not publish utilization metrics; thus, utilization is solved for using published & forecast annual and quarterly container volume, westbound / eastbound cargo proportions, and cargo type proportions", {"adj1": "val -55587", "adj2": "val -66064"}),
)


def _formula_table(sp_id: int, name: str, x: float, y: float, w: float, label: str) -> str:
    return table(sp_id, name, IN(x), IN(y), IN(w), IN(0.300), col_widths=[IN(w)], rows=[
        trow([rcell([tpara([trun(label, size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], l_ins=37785, r_ins=37785, T=edge(WHITE), B=edge(DK))], h=IN(0.300)),
    ])


def _draw_callout(out: list[str], n, spec: CalloutSpec) -> None:
    out.append(text_box(n(), spec.name, *spec.box.emu(), [paragraph([run(spec.text, size=PT(8), italic=True, color=BLACK, font=FONT)], align=spec.align, line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj=spec.geom_adj, anchor="ctr"))


def paint_chrome(out: list[str], n) -> None:
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Approach (2/2)", "To find annual volume and price per unit of cargo ($ / TEU)."))


def paint_operator_glyphs_and_early_price_node(out: list[str], n) -> None:
    for glyph in [g for g in CALCULATION_OPERATORS if g.role == "equals"]:
        _draw_operator(out, n, glyph)
    _draw_connector(out, n, FLOW_CONNECTORS[0])
    # Preserve the source two-line treatment for the first mix-weighted output.
    out.append(text_box(n(), "MixWeightedBasicOceanRate", IN(5.614), IN(3.932), IN(2.600), IN(0.350), [paragraph([run("Mix-weighted avg. basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=GREEN_FORMULA, line_color=BLACK, anchor="ctr"))
    for glyph in [g for g in CALCULATION_OPERATORS if g.role == "plus"]:
        _draw_operator(out, n, glyph)


def paint_input_nodes_and_headers(out: list[str], n) -> None:
    for node in VOLUME_AND_MIX_INPUTS:
        _draw_node(out, n, node)
    out.append(text_box(n(), "VesselInput", IN(0.495), IN(1.883), IN(2.600), IN(0.350), [_plain("Vessel (e.g., Maunawili)", color=WHITE, italic=True)], fill=BLACK, line_color=BLACK, anchor="ctr"))
    out.append(_formula_table(n(), "VolumeHeader", 0.495, 1.464, 3.100, "Total Container Volume "))
    out.append(_formula_table(n(), "PriceHeader", 3.795, 1.464, 9.000, "Container Price"))


def paint_price_formulas(out: list[str], n) -> None:
    for glyph in [g for g in CALCULATION_OPERATORS if g.role == "multiply"]:
        _draw_operator(out, n, glyph)
    for node in PRICE_FORMULAS:
        _draw_node(out, n, node)
    # Preserve two-line source nodes where line breaks make the formula legible.
    out.append(text_box(n(), "TerminalHandling", IN(10.195), IN(5.297), IN(2.600), IN(0.350), [paragraph([run("Terminal Handling / Stevedoring", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=GREEN_FORMULA, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "FinalWeightedPrice", IN(3.914), IN(6.663), IN(6.000), IN(0.350), [paragraph([run("Total weighted avg. container price", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=GREEN_FORMULA, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "MixWeightedTEU", IN(3.914), IN(3.249), IN(2.600), IN(0.350), [paragraph([run("Mix-weighted TEU basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=GREEN_FORMULA, line_color=BLACK, anchor="ctr"))


def paint_repeat_logic_and_callouts(out: list[str], n) -> None:
    _draw_connector(out, n, FLOW_CONNECTORS[1])
    _draw_connector(out, n, FLOW_CONNECTORS[2])
    out.append(text_box(n(), "RepeatCargoTypesFrame", IN(3.795), IN(1.828), IN(6.194), IN(3.174), [paragraph([], line_spacing=100000), paragraph([run("Repeat across ", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), line_break(), run("cargo types", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b"))
    _draw_callout(out, n, CALLOUTS[0])
    _draw_connector(out, n, FLOW_CONNECTORS[3])
    _draw_callout(out, n, CALLOUTS[1])
    _draw_connector(out, n, FLOW_CONNECTORS[4])
    _draw_callout(out, n, CALLOUTS[2])
    out.append(text_box(n(), "DivisionGlyph", IN(1.645), IN(5.664), IN(0.300), IN(0.300), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=NO_BORDER, prst="mathDivide", anchor="ctr"))
    _draw_connector(out, n, FLOW_CONNECTORS[5])
    out.append(text_box(n(), "RepeatRoutes", IN(7.593), IN(1.164), IN(5.473), IN(0.234), [_plain("Repeat across all routes and vessels", color=WHITE)], fill=BLUE_5, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "RepeatCargo", IN(7.593), IN(1.478), IN(5.473), IN(0.234), [_plain("To find volume and price for dry cargo TEUs, refrigerated TEUs, and automobiles", color=WHITE)], fill=BLUE_3, line_color=BLACK, anchor="ctr"))


def paint_track_labels_and_legend(out: list[str], n) -> None:
    # Top legend row, interleaved: [chip] Price ($)  [chip] Volume (#)  [chip] Proportions (%).
    # The track labels ARE the chip captions; the chips themselves carry no text.
    for label in TRACK_LABELS:
        out.append(text_box(n(), "TrackLabel", *label.box.emu(), [paragraph([run(label.label, size=PT(8), color=DK, font=FONT)], line_spacing=100000)], fill=None, line_color=NO_BORDER, wrap="none"))
    for entry in LEGEND_ENTRIES:
        out.append(text_box(n(), "LegendSwatch", *entry.swatch.emu(), [paragraph([], align="ctr", line_spacing=100000)], fill=entry.fill, line_color=entry.line_color, line_width=3175, anchor="ctr"))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_chrome(out, n)
    paint_operator_glyphs_and_early_price_node(out, n)
    paint_input_nodes_and_headers(out, n)
    paint_price_formulas(out, n)
    paint_repeat_logic_and_callouts(out, n)
    paint_track_labels_and_legend(out, n)
    return "".join(out)


def render() -> str:
    return slide(_body())
