"""Teaching exemplar: two-stage market-sizing approach (TAM + SAM).

ROLE
  methodology_flow / two_stage_market_sizing

USE WHEN
  A methodology/approach slide must explain a two-track sizing method in one
  glance: a budget-down TAM pipeline beside a transaction-up SAM pipeline, over a
  shared scope-and-dollar-basis foundation.

TEACHES
  - two parallel vertical pipelines as the whole slide (left = formula, right = flow)
  - distinct connective grammar per column: preset math glyphs (mathMultiply /
    mathEqual) on the calculation column; down-arrows on the process column
  - BLUE_1 -> BLUE_2 -> BLUE_4 depth ramp, with the output box as the dark focal
    node (white text, 1.5pt focal border)
  - a single unboxed foundation line that carries shared scope + dollar basis once
  - a compact chip row that keeps the three program coefficients quotable

TEXT-FIT PRECEDENT
  pipeline_box:
    geometry: 5.90in wide x 0.53-0.58in high
    type: Arial 10pt bold lead line + 9pt detail line, centered, 100% line spacing
    content: one verb/noun lead + one short qualifying clause
    copy_when: a step must read as a labelled stage, not a sentence

  stage_header:
    geometry: 5.90in wide x 0.46in high, DK underline beneath
    type: Arial 13pt (name bold) + 10pt italic muted subtitle
    content: "{ACRONYM}: {what it produces}" over "({direction})"

  coefficient_chip:
    geometry: 1.86in wide x 0.34in high, BLUE_2 fill
    type: Arial 9pt bold, centered
    content: one "{Program} ~NN%" pill; keep to a single 3-chip row

SOURCE NOTE
  Original teaching module (no source-faithful predecessor). Built on the public
  deck_core.authoring surface only: text_box / connector for shapes, run /
  paragraph for text, Chrome / body_slide for house furniture. Geometry mirrors
  the two-column proportions of overview.py and the rail/flow idiom of
  tcv_approach_usv.py.

FIDELITY NOTE
  Visible styling (hex colors, PT sizes, insets) is intentionally local to this
  module, as in the other teaching rewrites. The breadcrumb, title, takeaway, and
  source line are placeholders an author edits in the CHROME record below.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, paragraph, run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
MUTED = "44505C"
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: a small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "methodology_flow / two_stage_market_sizing",
    "use_when": (
        "Use for an approach slide that contrasts a budget-down TAM with a "
        "transaction-up SAM as two parallel pipelines."
    ),
    "teaches": [
        "two parallel vertical pipelines",
        "preset math glyphs on the formula column, arrows on the process column",
        "BLUE_1->BLUE_2->BLUE_4 depth ramp with a dark focal output box",
        "single unboxed shared foundation line",
        "quotable coefficient chip row",
    ],
}

TEXT_FIT = {
    "pipeline_box": {"box_in": (5.90, 0.55), "font_pt": "10 lead / 9 detail",
                     "content": "one bold lead line + one short detail clause"},
    "stage_header": {"box_in": (5.90, 0.46), "font_pt": "13 name / 10 italic subtitle",
                     "content": "acronym + what it produces, over a direction tag"},
    "coefficient_chip": {"box_in": (1.86, 0.34), "font_pt": 9,
                         "content": "one '{Program} ~NN%' pill in a single 3-chip row"},
}

COPY_RULES = (
    "Keep the left column a formula (mathMultiply / mathEqual glyphs) and the right column a flow (arrows).",
    "Make only the two output boxes dark (BLUE_4) + white text + 1.5pt border.",
    "Keep each box to a lead line plus one clause; push detail to the appendix.",
    "Use the foundation line for anything shared by BOTH stages; never duplicate it per column.",
)


# ════════════════════════════════════════════════════════════════════════════
# Small semantic geometry/content records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU at the primitive boundary."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class Step:
    """One pipeline box: a bold lead line + one detail clause, on a ramp fill."""

    box: Box
    lead: str
    detail: str
    fill: str
    text_color: str
    focal: bool = False


@dataclass(frozen=True)
class Chip:
    box: Box
    label: str


class ShapeIds:
    """Tiny deterministic id allocator for body shapes."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ── Column geometry (mirrors overview.py's two-column proportions) ───────────
LEFT_X = 0.495
RIGHT_X = 6.935
COL_W = 5.90
LEFT_C = LEFT_X + COL_W / 2          # 3.445 — left column centre line
RIGHT_C = RIGHT_X + COL_W / 2        # 9.885 — right column centre line


# ── Foundation line: shared scope + dollar basis, stated once (unboxed) ──────
FOUNDATION = Box(0.495, 1.46, 12.34, 0.40)
FOUNDATION_TEXT = ("Both pipelines cover outsourced new-construction on DDG-51, "
                   "Virginia, and Columbia, stated in constant FY2026 dollars.")


# ── Stage headers (name + direction tag) + underline rules ───────────────────
@dataclass(frozen=True)
class Header:
    box: Box
    name: str
    rest: str
    tag: str
    underline_y: float


LEFT_HEADER = Header(Box(LEFT_X, 2.12, COL_W, 0.46),
                     "TAM", ": addressable outsourced scope", "(budget-down)", 2.60)
RIGHT_HEADER = Header(Box(RIGHT_X, 2.12, COL_W, 0.46),
                      "SAM", ": observed supplier network", "(transaction-up)", 2.60)


# ── Left pipeline: a vertical formula (base x coefficient = TAM) ─────────────
LEFT_STEPS = (
    Step(Box(LEFT_X, 2.74, COL_W, 0.55),
         "SCN Basic Construction base", "by program and fiscal year (excludes GFE)",
         BLUE_1, BLACK),
    Step(Box(LEFT_X, 3.695, COL_W, 0.55),
         "Outsourced share",
         "% of Basic Construction performed outside the prime and co-prime yards",
         BLUE_2, BLACK),
    Step(Box(LEFT_X, 4.65, COL_W, 0.55),
         "Addressable outsourced market (TAM)", "$ by program and fiscal year",
         BLUE_4, WHITE, focal=True),
)

# Preset math glyphs sit in the gaps between the left boxes (multiply, then equals),
# drawn as filled <a:prstGeom> shapes the same way tcv_approach_usv.py draws its
# mathPlus / mathEqual operators (not text characters).
LEFT_OPERATORS = (
    ("mathMultiply", Box(LEFT_C - 0.16, 3.3425, 0.32, 0.32)),   # after the base
    ("mathEqual", Box(LEFT_C - 0.16, 4.2975, 0.32, 0.32)),      # before the TAM box
)

# Coefficient chips + caption under the TAM output box.
COEFF_CAPTION = Box(LEFT_X, 5.38, COL_W, 0.16)
COEFF_CAPTION_TEXT = "Applied outsourced share of Basic Construction, by program"
COEFF_CHIPS = (
    Chip(Box(LEFT_X, 5.58, 1.86, 0.34), "Virginia ~34%"),
    Chip(Box(LEFT_X + 2.02, 5.58, 1.86, 0.34), "Columbia ~22%"),
    Chip(Box(LEFT_X + 4.04, 5.58, 1.86, 0.34), "DDG-51 ~25%"),
)


# ── Right pipeline: a vertical process (subawards -> mapped supplier network) ─
RIGHT_STEPS = (
    Step(Box(RIGHT_X, 2.74, COL_W, 0.52),
         "First-tier subawards", "under in-scope hull-builder prime contracts",
         BLUE_1, BLACK),
    Step(Box(RIGHT_X, 3.627, COL_W, 0.52),
         "Roll up to supplier", "one row per UEI \u00d7 Program",
         BLUE_2, BLACK),
    Step(Box(RIGHT_X, 4.514, COL_W, 0.52),
         "Classify each supplier", "into archetypes",
         BLUE_3, WHITE),
    Step(Box(RIGHT_X, 5.401, COL_W, 0.52),
         "Observed supplier map (SAM)",
         "spend, concentration & continuity \u2192 where to play",
         BLUE_4, WHITE, focal=True),
)


# ════════════════════════════════════════════════════════════════════════════
# Paint helpers. Document order is PowerPoint paint order (later = on top).
# ════════════════════════════════════════════════════════════════════════════
def _r(text, *, size, color=DK, bold=False, italic=False):
    return run(text, size=size, color=color, bold=bold or None,
               italic=italic or None, font=FONT)


def paint_foundation(out, ids):
    out.append(text_box(ids.next(), "FoundationLine", *FOUNDATION.emu(),
                        [paragraph([_r(FOUNDATION_TEXT, size=PT(11), color=DK)],
                                   align="l", line_spacing=100_000)],
                        fill=None, line_color="none", anchor="ctr",
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0))


def paint_headers(out, ids):
    for hdr in (LEFT_HEADER, RIGHT_HEADER):
        paras = [
            paragraph([_r(hdr.name, size=PT(13), bold=True), _r(hdr.rest, size=PT(13))],
                      align="l", line_spacing=100_000),
            paragraph([_r(hdr.tag, size=PT(10), color=MUTED, italic=True)],
                      align="l", line_spacing=100_000),
        ]
        out.append(text_box(ids.next(), "StageHeader", *hdr.box.emu(), paras,
                            fill=None, line_color="none", anchor="t",
                            l_ins=0, t_ins=0, r_ins=0, b_ins=0))
        out.append(connector(ids.next(), "HeaderRule",
                             IN(hdr.box.x), IN(hdr.underline_y), IN(hdr.box.w), 0,
                             color=DK, width=12700))


def _paint_step(out, ids, step: Step):
    paras = [
        paragraph([_r(step.lead, size=PT(10), color=step.text_color, bold=True)],
                  align="ctr", line_spacing=100_000),
        paragraph([_r(step.detail, size=PT(9), color=step.text_color)],
                  align="ctr", line_spacing=100_000),
    ]
    out.append(text_box(ids.next(), "PipelineBox", *step.box.emu(), paras,
                        fill=step.fill, line_color=DK,
                        line_width=19050 if step.focal else 12700,
                        anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))


def _paint_down_arrow(out, ids, cx_in, y_top_in, y_bot_in):
    out.append(connector(ids.next(), "FlowArrow",
                         IN(cx_in), IN(y_top_in), 0, IN(y_bot_in - y_top_in),
                         color=DK, width=15875, arrow=True))


def paint_left_pipeline(out, ids):
    # Preset math glyphs first (filled DK <a:prstGeom> shapes), boxes on top.
    for prst, box in LEFT_OPERATORS:
        out.append(text_box(ids.next(), "Operator", *box.emu(),
                            [paragraph([], align="ctr", line_spacing=100_000)],
                            fill=DK, line_color="none", prst=prst, anchor="ctr",
                            l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for step in LEFT_STEPS:
        _paint_step(out, ids, step)


def paint_left_coefficients(out, ids):
    out.append(text_box(ids.next(), "CoeffCaption", *COEFF_CAPTION.emu(),
                        [paragraph([_r(COEFF_CAPTION_TEXT, size=PT(8), color=MUTED, italic=True)],
                                   align="l", line_spacing=100_000)],
                        fill=None, line_color="none", anchor="ctr",
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for chip in COEFF_CHIPS:
        out.append(text_box(ids.next(), "CoeffChip", *chip.box.emu(),
                            [paragraph([_r(chip.label, size=PT(9), color=DK, bold=True)],
                                       align="ctr", line_spacing=100_000)],
                            fill=BLUE_2, line_color=DK, line_width=12700, anchor="ctr",
                            l_ins=18288, t_ins=9144, r_ins=18288, b_ins=9144))


def paint_right_pipeline(out, ids):
    arrows = [
        (RIGHT_STEPS[0].box.y + RIGHT_STEPS[0].box.h, RIGHT_STEPS[1].box.y),
        (RIGHT_STEPS[1].box.y + RIGHT_STEPS[1].box.h, RIGHT_STEPS[2].box.y),
        (RIGHT_STEPS[2].box.y + RIGHT_STEPS[2].box.h, RIGHT_STEPS[3].box.y),
    ]
    for y_top, y_bot in arrows:
        _paint_down_arrow(out, ids, RIGHT_C, y_top, y_bot)
    for step in RIGHT_STEPS:
        _paint_step(out, ids, step)


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds()
    paint_foundation(out, ids)
    paint_headers(out, ids)
    paint_left_pipeline(out, ids)
    paint_left_coefficients(out, ids)
    paint_right_pipeline(out, ids)
    return "".join(out)


# ── House chrome (placeholders — edit the breadcrumb/title/takeaway/source) ──
CHROME = Chrome(
    section="Market Sizing",
    topic="Distributed Shipbuilding",
    title="Approach",
    takeaway=("The market is sized two ways: a budget-down TAM of addressable "
              "outsourced work and a transaction-up SAM of the observed supplier "
              "network."),
    preliminary=True,
)


def render() -> str:
    return body_slide(CHROME, _body())
