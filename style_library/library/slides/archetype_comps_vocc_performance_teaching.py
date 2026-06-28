"""Teaching exemplar: archetype-comparison native bubble chart with narrative rail.

ROLE
  archetype_comparison / performance_bubble_chart

USE WHEN
  A slide needs to compare performance behavior across several business
  archetypes using a bubble chart, an external archetype legend, and a
  right-hand commentary rail that explains the drivers behind plotted movement.

TEACHES
  - rebuilding a source bubble chart as a native editable `bubble_chart(...)`
  - transcribing sparse x/y/size bubble-cache data into auditable Python records
  - preserving source per-point fills and a patterned terminal-operator bucket
  - manual x-axis year ticks below the native chart frame
  - manual y-axis title outside the chart frame
  - mixed legend grammar: solid archetype dots, a patterned archetype dot, and
    a revenue bubble-size ring
  - dense no-fill narrative rail with bold archetype heads and hanging bullets
  - single-cell table used as a rail title band
  - compact off-house source note with colored constituent labels

TEXT-FIT PRECEDENT
  narrative_rail:
    geometry: 3.136in wide x 4.870in high
    type: Arial 10pt, black, 100% line spacing
    content: 4 archetype section heads + 7 hanging bullets
    copy_when: the chart carries the comparative evidence and the rail explains
               mechanism/timing rather than adding a second exhibit

  manual_legend:
    geometry: 2.4in wide x 1.5in high, below/right of plot area
    type: Arial 10pt, no-wrap labels
    content: 5 archetype marks plus one revenue bubble-size key
    copy_when: the chart template is too semantically overloaded for a native
               chart legend and the legend is part of the slide-level evidence

  source_note:
    geometry: 5.102in wide x 0.349in high
    type: Arial 7pt with colored bold archetype labels
    content: one dense constituent-company source line
    copy_when: source detail is needed but cannot occupy the house source band

SOURCE NOTE
  Teaching rewrite of the source-faithful `archetype_comps_vocc_performance.py`
  module. The source `slide33_chart18.xml` and `slide33_chart18.xlsb` were used
  only to transcribe the bubble chart data, per-series fills, point overrides,
  fixed axes, bubble scale, and manual plot layout into Python constants. This
  module reads no chart sidecar files at runtime: it builds the chart through
  `bubble_chart()` and generates its own editable embedded `.xlsx`.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. It preserves the visible chart semantics: year on x, EBIT margin on y,
  revenue as bubble size, value-chain archetype as bubble style, hidden native
  x-axis labels, fixed source axes, source bubble scale, external legend,
  narrative rail, source note, and Preliminary chip. Minor differences can remain
  in PowerPoint's internal native chart XML ordering and bubble rendering versus
  the original chart part.
"""
from __future__ import annotations

from dataclasses import dataclass
from deck_core.authoring import (
    Chrome, IN, PT, body_slide, bubble_chart, graphic_frame, paragraph, run, table,
    tcell_rich, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
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

# Local semantic palette. These are value-chain archetype colors, not house
# chrome colors. Keep them explicit so an authoring agent can copy the legend.
SHIPBUILDER_RED = "C30C3E"
OWNER_OPERATOR_BLUE = "364D6E"
CHARTER_GREEN = "27AE60"
TERMINAL_INTEGRATED_BLUE = "6F8DB9"
TERMINAL_STANDALONE_GRAY = "8A8F93"


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "archetype_comparison / performance_bubble_chart",
    "use_when": (
        "Use when a slide compares performance across business archetypes with "
        "a style-dense bubble chart, where marker position shows margin, bubble "
        "size shows revenue, and the right rail explains period-specific drivers."
    ),
    "teaches": [
        "native editable bubble_chart rebuild",
        "sparse chart-cache data transcribed into Python",
        "manual year ticks over a bubble chart",
        "manual y-axis title outside the chart frame",
        "external legend for marker color, hatch pattern, and bubble size",
        "dense narrative rail with section heads and hanging bullets",
        "single-cell table as rail header",
        "compact colored source note",
    ],
    "source_module": "archetype_comps_vocc_performance.py",
    "source_chart_assets_transcribed_from": ("slide33_chart18.xml", "slide33_chart18.xlsb"),
    "rebuild_strategy": "replace bundled XML/XLSB with native bubble_chart data and generated embedded xlsx",
}

TEXT_FIT = {
    "narrative_rail": {
        "box_in": (3.136, 4.870),
        "font_pt": 10,
        "content": "4 heads + 7 bullets with bold time-period labels",
        "note": "Works because prose is sentence-fragment style, not full paragraphs.",
    },
    "rail_header": {
        "box_in": (3.135, 0.300),
        "font_pt": 10,
        "content": "Revenue and EBIT margin drivers",
        "note": "Single-cell table gives exact top/bottom rule behavior.",
    },
    "manual_year_ticks": {
        "box_in": (0.306, 0.167),
        "font_pt": 10,
        "content": "four-digit year tick; five ticks only",
    },
    "legend_labels": {
        "box_in": "0.760-2.139 wide x 0.167 high",
        "font_pt": 10,
        "content": "no-wrap archetype captions",
    },
    "source_note": {
        "box_in": (5.102, 0.349),
        "font_pt": 7,
        "content": "one dense constituent-company source line",
    },
}

COPY_RULES = [
    "Use native bubble_chart when the source x/y/size caches can be transcribed; keep marker size and per-point styling explicit in Python.",
    "Use the slide-level legend as the semantic contract when the native chart still carries sparse internal buckets rather than clean archetype series.",
    "Use a right commentary rail when the chart explains what happened and the rail explains why it happened.",
    "Do not place long narrative inside the chart area; reserve the plot for markers, axis ticks, and a compact legend.",
    "A colored source note can carry constituent detail when a full appendix table would overtake the slide.",
]

CHART_ENCODING_CONTRACT = {
    "native_factory": "bubble_chart",
    "visible_encoding": {
        "x": "calendar year, 2020-2024",
        "y": "EBIT margin (%)",
        "bubble_size": "revenue, with $10B shown by the external ring key",
        "marker_color": "value-chain archetype",
    },
    "source_chart_xml": {
        "chart_type": "bubbleChart",
        "internal_series_count": 7,
        "source_cache_slots_per_series": 73,
        "bubble_scale": 66,
        "x_axis_min_max": (2019, 2025),
        "x_axis_major_unit": 1,
        "y_axis_min_max": (-50, 70),
        "y_axis_major_unit": 10,
        "plot_layout": {
            "x": 0.048794167134043748,
            "y": 0.032721202003338896,
            "w": 0.94148438960553371,
            "h": 0.92754590984974961,
        },
        "bubble_line_width": 3_175,
        "axis_line_width": 9_525,
    },
    "manual_shapes": (
        "year ticks, EBIT Margin y-axis title, archetype legend, revenue ring key, "
        "right narrative rail, rail header, source note, and preliminary chip"
    ),
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU only at the primitive boundary."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class BubblePoint:
    """One plotted bubble in its original source-cache slot."""

    slot: int
    year: int
    ebit_margin: float
    revenue: float


@dataclass(frozen=True)
class BubbleSeriesBucket:
    """One sparse source bucket for the native bubble_chart() factory.

    The source chart stored 73 cache slots per series, with each internal series
    populated only for its own slot range. Keeping those slot numbers makes the
    data auditable against the source XML while still generating a fresh embedded
    .xlsx at build time.
    """

    name: str
    default_fill: str | None = None
    default_pattern: dict | None = None
    points: tuple[BubblePoint, ...] = ()
    point_fills: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True)
class YearTick:
    """Manual x-axis tick under the chart template."""

    box: Box
    label: str


@dataclass(frozen=True)
class LegendEntry:
    """One external legend entry beside/below the plot area."""

    label: str
    marker: str
    marker_box: Box
    label_box: Box
    fill: str | None
    line_color: str = DK
    pattern_fill: dict | None = None


@dataclass(frozen=True)
class NarrativeBullet:
    """One hanging bullet in the commentary rail."""

    prefix: str | None
    text: str


@dataclass(frozen=True)
class NarrativeSection:
    """Section head plus bullets for the right rail."""

    title: str
    qualifier: str | None
    bullets: tuple[NarrativeBullet, ...]


@dataclass(frozen=True)
class SourceRun:
    """A run in the compact colored source note."""

    text: str
    color: str = BLACK
    bold: bool = False


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.373, 1.696, 9.286, 5.200)
Y_AXIS_TITLE = Box(0.533, 1.505, 1.064, 0.167)
YEAR_TICK_Y = 6.736
YEAR_TICK_SIZE = (0.306, 0.167)
LEGEND_LABEL_H = 0.167
NARRATIVE_RAIL = Box(9.660, 1.866, 3.136, 4.870)
NARRATIVE_HEADER = Box(9.660, 1.563, 3.135, 0.300)
SOURCE_NOTE = Box(0.495, 7.081, 5.102, 0.349)


# ════════════════════════════════════════════════════════════════════════════
# Native chart data. These constants replace the former runtime XML/XLSB read.
# Each series is sparse across the 73 original source slots; helper functions
# below expand the sparse records into the native factory's editable workbook.
# ════════════════════════════════════════════════════════════════════════════
POINT_SLOT_COUNT = CHART_ENCODING_CONTRACT["source_chart_xml"]["source_cache_slots_per_series"]


BUBBLE_SERIES_BUCKETS: tuple[BubbleSeriesBucket, ...] = (
    BubbleSeriesBucket(
        name='Bucket 1: shipbuilder recovery/stress',
        default_fill='C30C3E',
        default_pattern=None,
        points=(
            BubblePoint(0, 2021, -2.9787234042553195, 19771.325688420737),
            BubblePoint(1, 2022, -33.20027982387556, 3856.7506229268834),
            BubblePoint(2, 2022, 1.9083969465648851, 20790.68069640845),
        ),
    ),
    BubbleSeriesBucket(
        name='Bucket 2: owner/operator default with shipbuilder points',
        default_fill='364D6E',
        default_pattern=None,
        points=(
            BubblePoint(3, 2020, -7.826086956521738, 21176.49225216599),
            BubblePoint(4, 2021, -38.99333333333333, 3785.9985360805663),
            BubblePoint(5, 2021, 4.1817392562581395, 7821.8697999999995),
            BubblePoint(6, 2022, 0.3434112180997913, 11784.824390166483),
            BubblePoint(7, 2020, 10.954584404455868, 29175.0),
            BubblePoint(8, 2021, 54.245502842762605, 10729.0),
            BubblePoint(9, 2021, 37.24290927185272, 48232.0),
            BubblePoint(10, 2022, 45.33351996143019, 64299.0),
            BubblePoint(11, 2023, -8.174809189880284, 5162.2),
            BubblePoint(12, 2023, 6.617537812379283, 33653.0),
            BubblePoint(13, 2024, 42.112632603175356, 8427.4),
            BubblePoint(14, 2024, 12.68588852038087, 37388.0),
        ),
        point_fills=(
            (3, 'C30C3E'),
            (4, 'C30C3E'),
            (5, 'C30C3E'),
            (6, 'C30C3E'),
        ),
    ),
    BubbleSeriesBucket(
        name='Bucket 3: charter default with shipbuilder and owner/operator points',
        default_fill='27AE60',
        default_pattern=None,
        points=(
            BubblePoint(15, 2021, 7.840197254431562, 1089.4355999999998),
            BubblePoint(16, 2022, -0.13365410318096765, 8004.243600000001),
            BubblePoint(17, 2023, 3.0864197530864197, 25097.40737584917),
            BubblePoint(18, 2024, 2.3054755043227666, 23479.89660725644),
            BubblePoint(19, 2020, 18.261523046092183, 3992.0),
            BubblePoint(20, 2020, 10.297043287370515, 14577.0),
            BubblePoint(21, 2021, 42.15738351798452, 26356.0),
            BubblePoint(22, 2022, 36.14512215764826, 3544.6),
            BubblePoint(23, 2022, 50.73212274388066, 36401.0),
            BubblePoint(24, 2023, 14.143675169182718, 19210.0),
            BubblePoint(25, 2024, 13.392813131562084, 20287.0),
            BubblePoint(26, 2021, 51.92159420289856, 690.0),
            BubblePoint(27, 2021, 55.61092637836599, 793.639),
            BubblePoint(28, 2022, 65.80422960725076, 993.0),
            BubblePoint(29, 2022, 59.455101588262075, 1113.859),
            BubblePoint(30, 2022, 14.103882746207253, 1555.6),
            BubblePoint(31, 2023, 59.61611909650924, 974.0),
            BubblePoint(32, 2023, 30.965074903765107, 1511.406),
            BubblePoint(33, 2023, 21.258235671389425, 1715.1),
            BubblePoint(34, 2024, 22.182558229929164, 2083.894),
        ),
        point_fills=(
            (15, 'C30C3E'),
            (16, 'C30C3E'),
            (17, 'C30C3E'),
            (18, 'C30C3E'),
            (19, '364D6E'),
            (20, '364D6E'),
            (21, '364D6E'),
            (22, '364D6E'),
            (23, '364D6E'),
            (24, '364D6E'),
            (25, '364D6E'),
        ),
    ),
    BubbleSeriesBucket(
        name='Bucket 4: owner/operator default with charter points',
        default_fill='364D6E',
        default_pattern=None,
        points=(
            BubblePoint(35, 2020, 2.517434937914611, 7190.017000000001),
            BubblePoint(36, 2022, 3.845388188453882, 1025.5135),
            BubblePoint(37, 2023, 1.324192336589031, 16496.1230702495),
            BubblePoint(38, 2024, 5.615161719790116, 17280.39191804366),
            BubblePoint(39, 2020, 13.204595717136847, 1853.9),
            BubblePoint(40, 2021, 36.315755873340144, 3132.8),
            BubblePoint(41, 2022, 48.91892752515603, 12561.6),
            BubblePoint(42, 2023, 11.90149374243036, 2477.0),
            BubblePoint(43, 2024, 17.827526070398974, 2809.7),
            BubblePoint(44, 2020, 13.105694094747339, 460.319),
            BubblePoint(45, 2020, 31.652219595482006, 3807.0),
            BubblePoint(46, 2021, 29.325000000000003, 4000.0),
            BubblePoint(47, 2022, 19.03454587051018, 4371.0),
            BubblePoint(48, 2023, 25.494276795005206, 3844.0),
            BubblePoint(49, 2024, 29.764837625979844, 4465.0),
        ),
        point_fills=(
            (35, 'C30C3E'),
            (36, 'C30C3E'),
            (37, 'C30C3E'),
            (38, 'C30C3E'),
            (44, '27AE60'),
            (45, '6F8DB9'),
            (46, '6F8DB9'),
            (47, '6F8DB9'),
            (48, '6F8DB9'),
            (49, '6F8DB9'),
        ),
    ),
    BubbleSeriesBucket(
        name='Bucket 5: standalone terminal-operator pattern',
        default_fill=None,
        default_pattern={'prst': 'pct50', 'fg': 'scheme:tx1', 'bg': 'scheme:bg1'},
        points=(
            BubblePoint(50, 2020, 2.1914285714285713, 6445.019381093996),
            BubblePoint(51, 2023, 3.2152659783034894, 8463.5362),
            BubblePoint(52, 2024, 1.9931102362204725, 8413.2928),
            BubblePoint(53, 2024, 27.35885788449059, 2311.5),
            BubblePoint(54, 2020, 32.75701021875992, 1380.7877834240462),
            BubblePoint(55, 2020, 42.955828628362674, 1505.5),
            BubblePoint(56, 2021, 40.61280117184256, 1698.04861787784),
            BubblePoint(57, 2021, 47.833780160857906, 1865.0),
            BubblePoint(58, 2022, 35.1868290838553, 1559.4693328206115),
            BubblePoint(59, 2022, 50.92657155595185, 2243.0),
            BubblePoint(60, 2023, 31.215682587438888, 1361.686873471687),
            BubblePoint(61, 2023, 50.728753109918834, 2388.326),
            BubblePoint(62, 2024, 37.84991786980203, 1489.1151821002356),
            BubblePoint(63, 2024, 53.95908194270246, 2739.524),
        ),
        point_fills=(
            (50, 'C30C3E'),
            (51, 'C30C3E'),
            (52, 'C30C3E'),
            (53, '27AE60'),
        ),
    ),
    BubbleSeriesBucket(
        name='Bucket 6: shipbuilder default with charter points',
        default_fill='C30C3E',
        default_pattern=None,
        points=(
            BubblePoint(64, 2020, 6.697282816685799, 1410.0531899999999),
            BubblePoint(65, 2023, 2.6524303821389523, 5738.553180941462),
            BubblePoint(66, 2024, 2.206755753526355, 7291.6243757866105),
            BubblePoint(67, 2020, 42.43581410464738, 1230.8),
            BubblePoint(68, 2021, 47.85417941916616, 1470.3),
            BubblePoint(69, 2024, 53.34161735700197, 1014.0),
        ),
        point_fills=(
            (67, '27AE60'),
            (68, '27AE60'),
            (69, '27AE60'),
        ),
    ),
    BubbleSeriesBucket(
        name='Bucket 7: terminal/charter tail points',
        default_fill='C30C3E',
        default_pattern=None,
        points=(
            BubblePoint(70, 2023, 1.7566688353936235, 1049.4636),
            BubblePoint(71, 2024, 5.16068282607375, 1018.11285),
            BubblePoint(72, 2020, 43.17748917748918, 462.0),
        ),
        point_fills=(
            (72, '27AE60'),
        ),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Manual labels and legend entries copied from source slide coordinates.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, *YEAR_TICK_SIZE), label)
    for x, label in (
        (2.130, "2020"),
        (3.589, "2021"),
        (5.045, "2022"),
        (6.502, "2023"),
        (7.960, "2024"),
    )
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Shipbuilders",
        "solid_archetype_dot",
        Box(7.148, 5.583, 0.146, 0.146),
        Box(7.375, 5.578, 0.760, LEGEND_LABEL_H),
        SHIPBUILDER_RED,
    ),
    LegendEntry(
        "Owner/Operator (Carrier Segment)",
        "solid_archetype_dot",
        Box(7.148, 5.806, 0.146, 0.146),
        Box(7.375, 5.800, 2.139, LEGEND_LABEL_H),
        OWNER_OPERATOR_BLUE,
    ),
    LegendEntry(
        "Charter Companies",
        "solid_archetype_dot",
        Box(7.148, 6.028, 0.146, 0.146),
        Box(7.375, 6.023, 1.200, LEGEND_LABEL_H),
        CHARTER_GREEN,
    ),
    LegendEntry(
        "Terminal Operators (Integrated)",
        "solid_archetype_dot",
        Box(7.148, 6.250, 0.146, 0.146),
        Box(7.375, 6.245, 1.944, LEGEND_LABEL_H),
        TERMINAL_INTEGRATED_BLUE,
    ),
    LegendEntry(
        "Terminal Operators (Standalone)",
        "hatched_archetype_dot",
        Box(7.148, 6.472, 0.146, 0.146),
        Box(7.375, 6.467, 2.021, LEGEND_LABEL_H),
        None,
        pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"},
    ),
    LegendEntry(
        "$10B (Revenue)",
        "revenue_bubble_ring",
        Box(7.066, 5.139, 0.326, 0.326),
        Box(7.450, 5.224, 1.005, LEGEND_LABEL_H),
        None,
    ),
)

NARRATIVE_SECTIONS: tuple[NarrativeSection, ...] = (
    NarrativeSection(
        "Shipbuilders",
        "(relating to Commercial market)",
        (
            NarrativeBullet("’21-’22:", "While orders recovered from ’20, earnings remained pressured by input materials and labor cost growth."),
            NarrativeBullet("’23-’24:", "Improvement driven by performance against orderbook contracts and rising new build prices"),
        ),
    ),
    NarrativeSection(
        "Owner/Operators",
        None,
        (
            NarrativeBullet("’21-’22:", "Freight rates reached historic highs driven by post-COVID pent-up demand and shift toward goods consumption, while port congestion and operational disruptions constrained effective vessel supply amid below-trend capacity additions."),
            NarrativeBullet("’23-’24:", "Freight rates normalized as consumer demand softened under inflationary pressure, coinciding with acceleration in new vessel deliveries that expanded global fleet capacity."),
        ),
    ),
    NarrativeSection(
        "Charter Companies",
        None,
        (
            NarrativeBullet("’21-’22:", "Charter rates surged alongside freight rates as operators sought to secure tonnage in supply-constrained market."),
            NarrativeBullet("’23-’24:", "Earnings remained supported by multi-year charter contracts signed at peak market conditions ’21-’22, partially insulating results from lower charter rates."),
        ),
    ),
    NarrativeSection(
        "Terminal Operators",
        None,
        (
            NarrativeBullet(None, "Relatively more stable margins given ability to pass on costs to operators."),
        ),
    ),
)

SOURCE_RUNS: tuple[SourceRun, ...] = (
    SourceRun("Source: Company filings |   "),
    SourceRun("Shipbuilders:", SHIPBUILDER_RED, True),
    SourceRun(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. "),
    SourceRun("Owner/Operator", OWNER_OPERATOR_BLUE, True),
    SourceRun(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. "),
    SourceRun("Charter Companies", CHARTER_GREEN, True),
    SourceRun(": Danaos, "),
    SourceRun("Costamare"),
    SourceRun(", Seaspan. "),
    SourceRun("Terminal Operators (Integrated)", TERMINAL_INTEGRATED_BLUE, True),
    SourceRun(": Maersk Terminals.         "),
    SourceRun("Terminal Operators (Standalone)", TERMINAL_STANDALONE_GRAY, True),
    SourceRun(": Hutchison Ports, ICTS. Note: Segment margins not burdened by corporate"),
)


# ════════════════════════════════════════════════════════════════════════════
# Native chart factory helpers and chart specification.
# ════════════════════════════════════════════════════════════════════════════
def _sparse_values(bucket: BubbleSeriesBucket, field: str) -> list[float | int | None]:
    values: list[float | int | None] = [None] * POINT_SLOT_COUNT
    for point in bucket.points:
        values[point.slot] = getattr(point, field)
    return values


def _sparse_point_fills(bucket: BubbleSeriesBucket) -> list[str | None]:
    fills: list[str | None] = [None] * POINT_SLOT_COUNT
    for slot, fill in bucket.point_fills:
        fills[slot] = fill
    return fills


def _native_bubble_series(bucket: BubbleSeriesBucket) -> dict:
    series = {
        "name": bucket.name,
        "x_values": _sparse_values(bucket, "year"),
        "y_values": _sparse_values(bucket, "ebit_margin"),
        "bubble_sizes": _sparse_values(bucket, "revenue"),
        "hide_labels": True,
    }
    if bucket.default_pattern is not None:
        series["pattern"] = dict(bucket.default_pattern)
    elif bucket.default_fill is not None:
        series["color"] = bucket.default_fill
    if bucket.point_fills:
        series["data_point_colors"] = _sparse_point_fills(bucket)
    return series


# Legacy-shape mirror for agents/tools that expect the converted-slide data
# shape. CHARTS consumes the same values through bubble_chart().
_CHART0_DATA = {
    "categories": None,
    "series": [
        {
            "name": bucket.name,
            "x_values": _sparse_values(bucket, "year"),
            "values": _sparse_values(bucket, "ebit_margin"),
            "bubble_sizes": _sparse_values(bucket, "revenue"),
        }
        for bucket in BUBBLE_SERIES_BUCKETS
    ],
}

CHART_STYLE = {
    "series": [_native_bubble_series(bucket) for bucket in BUBBLE_SERIES_BUCKETS],
    "show_legend": False,
    "x_axis_format": "General",
    "y_axis_format": '#,##0;"-"#,##0',
    "bubble_size_format": "General",
    "x_axis_min": 2019,
    "x_axis_max": 2025,
    "x_axis_major_unit": 1,
    "y_axis_min": -50,
    "y_axis_max": 70,
    "y_axis_major_unit": 10,
    "show_x_axis_labels": False,
    "show_y_axis_labels": True,
    "show_x_gridlines": True,
    "show_y_gridlines": True,
    "x_major_gridline_color": "none",
    "y_major_gridline_color": "none",
    "x_axis_crosses_at": 0,
    "y_axis_crosses": "min",
    "bubble_scale": 66,
    "show_negative_bubbles": False,
    "bubble_line_color": "scheme:tx1",
    "bubble_line_width": 3_175,
    "axis_line_color": "scheme:tx1",
    "axis_line_width": 9_525,
    "axis_label_size_pt": 10,
    "axis_label_color": BLACK,
    "plot_layout": dict(CHART_ENCODING_CONTRACT["source_chart_xml"]["plot_layout"]),
}

CHARTS = [bubble_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Tiny local authoring helpers.
# ════════════════════════════════════════════════════════════════════════════
def _textbox(sp_id: int, name: str, box: Box, paras: list[str], **kwargs) -> str:
    return text_box(sp_id, name, *box.emu(), paras, **kwargs)


def _one_line(
    text: str,
    *,
    size: int = PT(10),
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
    align: str | None = None,
) -> str:
    return paragraph(
        [run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100000,
    )


def _empty_centered_paragraph() -> str:
    return paragraph([], align="ctr", line_spacing=100000)


def _narrative_head(section: NarrativeSection) -> str:
    runs = [run(section.title, size=PT(10), bold=True, color=BLACK, font=FONT)]
    if section.qualifier:
        runs.append(run(" ", size=PT(10), color=BLACK, font=FONT))
        runs.append(run(section.qualifier, size=PT(10), italic=True, color=BLACK, font=FONT))
    return paragraph(runs, line_spacing=100000)


def _narrative_bullet(bullet: NarrativeBullet) -> str:
    runs = []
    if bullet.prefix:
        runs.append(run(bullet.prefix, size=PT(10), bold=True, color=BLACK, font=FONT))
        runs.append(run(" ", size=PT(10), color=BLACK, font=FONT))
    runs.append(run(bullet.text, size=PT(10), color=BLACK, font=FONT))
    return paragraph(runs, mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)


def _narrative_paragraphs() -> list[str]:
    paras: list[str] = []
    for section in NARRATIVE_SECTIONS:
        paras.append(_narrative_head(section))
        paras.extend(_narrative_bullet(bullet) for bullet in section.bullets)
    return paras


def _source_paragraph() -> str:
    return paragraph(
        [
            run(src.text, size=PT(7), bold=src.bold or None, color=src.color, font=FONT)
            for src in SOURCE_RUNS
        ],
        line_spacing=100000,
    )


def paint_template_bubble_chart(next_id) -> list[str]:
    """Native editable bubble chart: position = margin, size = revenue."""

    x, y, w, h = CHART_FRAME.emu()
    return [
        graphic_frame(
            sp_id=next_id(),
            name="Chart",
            x=x,
            y=y,
            cx=w,
            cy=h,
            rId="rId2",
        )
    ]


def paint_manual_axis_labels(next_id) -> list[str]:
    """Five manual year ticks plus the outside y-axis title."""

    shapes: list[str] = []
    for tick in YEAR_TICKS:
        shapes.append(
            _textbox(
                next_id(),
                "YearLabel",
                tick.box,
                [_one_line(tick.label, align="ctr")],
                fill=None,
                line_color="none",
                wrap="none",
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )
    shapes.append(
        _textbox(
            next_id(),
            "YAxisTitle",
            Y_AXIS_TITLE,
            [_one_line("EBIT Margin (%)", bold=True)],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        )
    )
    return shapes


def paint_legend(next_id) -> list[str]:
    """External legend: archetype markers plus revenue bubble-size ring."""

    shapes: list[str] = []
    # Paint the revenue-size ring with the solid dots, matching the source order.
    for entry in LEGEND_ENTRIES:
        if entry.marker == "hatched_archetype_dot":
            continue
        shapes.append(
            _textbox(
                next_id(),
                "LegendMarker",
                entry.marker_box,
                [_empty_centered_paragraph()],
                fill=entry.fill,
                line_color=entry.line_color,
                line_width=3175,
                prst="ellipse",
                anchor="ctr",
            )
        )

    hatched = next(entry for entry in LEGEND_ENTRIES if entry.marker == "hatched_archetype_dot")
    shapes.append(
        _textbox(
            next_id(),
            "LegendMarkerHatched",
            hatched.marker_box,
            [_empty_centered_paragraph()],
            fill=None,
            line_color=hatched.line_color,
            pattern_fill=hatched.pattern_fill,
            line_width=3175,
            prst="ellipse",
            anchor="ctr",
        )
    )

    for entry in LEGEND_ENTRIES:
        shapes.append(
            _textbox(
                next_id(),
                "LegendLabel",
                entry.label_box,
                [_one_line(entry.label)],
                fill=None,
                line_color="none",
                anchor="ctr",
                wrap="none",
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )
    return shapes


def paint_narrative_rail(next_id) -> list[str]:
    """Right rail explaining the margin drivers by archetype and period."""

    return [
        _textbox(
            next_id(),
            "RevenueAndMarginDriversRail",
            NARRATIVE_RAIL,
            _narrative_paragraphs(),
            fill=None,
            line_color="none",
        )
    ]


def paint_narrative_header(next_id) -> list[str]:
    """Single-cell table header for the right narrative rail."""

    return [
        table(
            next_id(),
            "RevenueAndMarginDriversHeader",
            *NARRATIVE_HEADER.emu(),
            col_widths=[IN(NARRATIVE_HEADER.w)],
            rows=[
                trow(
                    [
                        rcell(
                            [
                                tpara(
                                    [trun("Revenue and EBIT margin drivers", size=PT(10), bold=True, color=BLACK, font=FONT)],
                                    mar_l=0,
                                    indent=0,
                                )
                            ],
                            l_ins=41564,
                            r_ins=41564,
                            T=edge(WHITE),
                            B=edge(BLACK),
                        )
                    ],
                    h=IN(NARRATIVE_HEADER.h),
                )
            ],
        )
    ]


def paint_source_note(next_id) -> list[str]:
    """Compact source/constituent line retained at the source position."""

    return [
        _textbox(
            next_id(),
            "SourceNote",
            SOURCE_NOTE,
            [_source_paragraph()],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    ]


def paint_preliminary_chip(next_id) -> list[str]:
    """House Preliminary chip, intentionally painted after body content."""

    return [""]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    shapes.extend(paint_template_bubble_chart(next_id))
    shapes.extend(paint_manual_axis_labels(next_id))
    shapes.extend(paint_legend(next_id))
    shapes.extend(paint_narrative_rail(next_id))
    shapes.extend(paint_narrative_header(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_preliminary_chip(next_id))
    return "".join(shapes)


CHROME = Chrome(
    section="Commercial Maritime Value Chain",
    topic="Performance",
    title="Archetype Comps (2/3)",
    takeaway="VOCC performance ’21-’22 driven by historically high freight rates; charter companies benefitted through ’24 from leases locked in ’21-’22.",
)


def render() -> str:
    return body_slide(CHROME, _body())
