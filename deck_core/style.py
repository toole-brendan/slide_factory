"""deck_core.style - design tokens for the PowerPoint build pipeline.

Single source of truth for everything style-y: canvas, margins, the BODY
content box, palette (with paired text colors), the type scale, inset presets,
and the locked-chrome geometry. Slide modules import the names they need from
here instead of inlining a private copy.

Pure data plus two tiny helpers (blue_pair / gray_pair); no dependency on the
rest of deck_core, so importing it is cheap and safe.

Sections:
    1. Layout      - canvas, margins, the BODY box
    2. Palette     - type colors + blue/gray ramps + paired text colors
    3. Typography  - FONT, line spacing, point-size-bearing body scale plus
                     locked chrome sizes (1/100 pt)
    4. Insets      - PAD_* / INSETS_* presets for text_box()
    5. Chrome      - breadcrumb / title / Prelim chip / sources geometry + ids

This module is the machine-readable style system - tokens kept verbatim from the
locked template, so chrome stays byte-stable.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Layout
# ---------------------------------------------------------------------------

# 16:9 widescreen, EMU (914_400 EMU per inch).
SLIDE_W = 12_192_000
SLIDE_H = 6_858_000

EMU_PER_INCH = 914_400


def IN(inches: float) -> int:
    """Inches -> EMU (rounded). Lets a slide module express geometry in inches and
    have the build convert to EMU for the OOXML, e.g. text_box(.., IN(1.5), IN(0.3), ..).
    Backward-compatible: raw EMU ints still work. Round-trip through a 3-decimal inch
    value is visually exact (sub-0.05 px) but not byte-exact, so the locked chrome
    geometry below stays in verbatim EMU."""
    return round(inches * EMU_PER_INCH)


def PT(points: float) -> int:
    """Points -> 1/100 pt, the unit run(size=..) / OOXML sz use, e.g. PT(10) == 1000,
    PT(8.5) == 850. Exact for the usual half-point sizes. Lets a module write font
    sizes as points (PT(10)) instead of the 1/100-pt integer (1000)."""
    return round(points * 100)

# Symmetric left/right margin used by every content slide.
LEFT_MARGIN = 453_079
RIGHT_MARGIN = LEFT_MARGIN
USABLE_W = SLIDE_W - LEFT_MARGIN - RIGHT_MARGIN          # 11_285_842

# Chrome/content column width. Slightly narrower than USABLE_W - rounded to
# the source pptx grid and preserved verbatim so chrome stays byte-aligned
# with the locked template (breadcrumb / title / sources all use this).
CONTENT_W = 11_282_362

# -- The authoritative body box ---------------------------------------------
# Place every body shape inside BODY so slides stay flush and clear of chrome.
# x flush with breadcrumb/title (right edge BODY_R). y clears a 2-line title
# (Arial 20pt, noAutofit). Bottom stops ~0.07in above the Sources box.
BODY_X  = LEFT_MARGIN       # 453_079
BODY_Y  = 1_371_600         # 1.5in - below a 2-line title
BODY_CX = CONTENT_W         # 11_282_362
BODY_CY = 4_498_400         # -> bottom 5_870_000
BODY    = (BODY_X, BODY_Y, BODY_CX, BODY_CY)
BODY_R  = BODY_X + BODY_CX  # 11_735_441  right edge
BODY_B  = BODY_Y + BODY_CY  #  5_870_000  bottom edge


# ---------------------------------------------------------------------------
# 2. Palette
# ---------------------------------------------------------------------------
# Two roles, kept distinct:
#   Type (text): BLACK default body/exhibit text; WHITE on dark fills; the
#     locked-chrome DK / BREADCRUMB tokens are reserved for chrome only.
#   Fill (optional): a step from the BLUE_*/GRAY_* ramps, white, dark, or none.

# Type colors.
#
# Two roles, kept deliberately separate so a body-text cleanup can't disturb the
# locked chrome:
#   - BLACK is the default BODY/EXHIBIT text color (000000) and the border /
#     Preliminary-chip-text color.
#   - DK / BREADCRUMB are LOCKED CHROME / legacy tokens; the chrome builders in
#     primitives.py (_chrome_run, title_placeholder, sources_line, the divider
#     page number) still use them, so their hex values must not change.
BLACK      = "000000"   # default body/exhibit text + 1pt/1.5pt borders + draft-chip text
WHITE      = "FFFFFF"   # text on a dark fill (BLUE_3/4/5, GRAY_5)
BODY_TEXT  = BLACK      # semantic alias for body/exhibit text

DK         = "162029"   # do not change: locked chrome (title/sources) + legacy slide code
BREADCRUMB = "44505C"   # do not change: breadcrumb text only

# Draft signal.
PRELIM = "FFFFCC"      # draft-yellow fill (Preliminary chip, draft slots)

# Blue ramp (lightest -> darkest); text flips to WHITE at BLUE_3.
BLUE_1 = "E2E9EF"; BLUE_2 = "B6C8D8"; BLUE_3 = "6E91B1"; BLUE_4 = "3D5972"; BLUE_5 = "263746"
# Gray ramp (lightest -> darkest); text flips to WHITE at GRAY_5.
GRAY_1 = "F2F2F2"; GRAY_2 = "D9D9D9"; GRAY_3 = "BFBFBF"; GRAY_4 = "7F7F7F"; GRAY_5 = "646464"

# Chart accent palette — CHARTS ONLY. Do NOT use these for shapes, tables,
# text, chrome, or any non-chart fill; the deck's general palette is the BLUE_*
# / GRAY_* ramps above. These six are the theme accent1..6 hexes (from
# infra/template theme1.xml <a:clrScheme>, the Saronic gray-blue ramp) — the
# literal values a plain `schemeClr accentN` resolves to — exposed only so
# native charts can mirror the static think-cell exhibits (which fill with
# accentN) while staying native srgbClr. Order is the theme's, NOT brightness:
# by luma accent6 > accent5 > accent4 > accent1 > accent3 > accent2.
CHART_ACCENT_1 = "79838F"; CHART_ACCENT_2 = "1D4D68"; CHART_ACCENT_3 = "486D82"
CHART_ACCENT_4 = "89A2B0"; CHART_ACCENT_5 = "AFC2CC"; CHART_ACCENT_6 = "D8E3EB"

# Paired text colors: BLACK on light fills, WHITE once the fill goes dark (blue
# flips at the third step, gray at the darkest): default body text is BLACK,
# WHITE only on dark fills.
BLUE_SCALE = (BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5)
BLUE_TEXT  = (BLACK,  BLACK,  WHITE,  WHITE,  WHITE)
GRAY_SCALE = (GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5)
GRAY_TEXT  = (BLACK,  BLACK,  BLACK,  BLACK,  WHITE)
# Chart accent pairing (theme order) — CHARTS ONLY, see CHART_ACCENT_* above.
# Label text flips to WHITE on the dark accents (1/2/3, luma < 0.55) and stays
# BLACK on the light ones (4/5/6).
CHART_ACCENT_SCALE = (CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
                      CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6)
CHART_ACCENT_TEXT  = (WHITE, WHITE, WHITE, BLACK, BLACK, BLACK)


def blue_pair(i: int) -> tuple[str, str]:
    """(fill, text_color) for blue ramp index 0..4 (lightest -> darkest), so
    text contrast can't drift. e.g. fill, txt = blue_pair(2) -> mid blue,
    white text."""
    return BLUE_SCALE[i], BLUE_TEXT[i]


def gray_pair(i: int) -> tuple[str, str]:
    """(fill, text_color) for gray ramp index 0..4 (lightest -> darkest)."""
    return GRAY_SCALE[i], GRAY_TEXT[i]


def chart_accent_pair(i: int) -> tuple[str, str]:
    """(fill, text_color) for CHART accent index 0..5 (accent1..accent6), so a
    label drawn on a chart accent swatch picks readable text automatically.
    CHARTS ONLY — see CHART_ACCENT_* above."""
    return CHART_ACCENT_SCALE[i], CHART_ACCENT_TEXT[i]


def chart_accent_seq(n: int) -> list[str]:
    """Chart-segment/column fills for an n-series chart (house rule): a 1-v-1
    (n==2) chart uses gray accent1 + blue accent2; otherwise step through the
    blue accents (accent2 onward), extending with the full ramp if n>5. CHARTS
    ONLY — see CHART_ACCENT_* above."""
    if n == 2:
        return [CHART_ACCENT_1, CHART_ACCENT_2]
    blues = list(CHART_ACCENT_SCALE[1:])           # accent2..accent6
    return (blues + list(CHART_ACCENT_SCALE))[:n]  # full ramp as overflow if n>5


# ---------------------------------------------------------------------------
# 3. Typography
# ---------------------------------------------------------------------------

FONT = "Arial"   # Arial everywhere

# Default line spacing for body paragraphs. PPTX <a:spcPct val="N"/> is
# N/1000 of single - 115_000 => 115%.
LNSPC_BODY = 115_000
# Single (100%) line spacing — the right density for TABLE cells (dense tabular
# data), as opposed to the 115% body default. Table builders default to this.
LNSPC_SINGLE = 100_000

# PPTX <a:rPr sz="..."> is in hundredths of a point: 800 == 8pt, 1200 == 12pt.
#
# These are DEFAULTS, not a cage. If a slide needs a size not listed here, use
# the raw numeric size directly with a nearby comment, e.g.
#     size=1150  # 11.5pt, tight axis label
# Keep bold=True / italic=True explicit in run() calls. ALL CAPS is text
# content, not a hidden style.

# -- Body-slide authoring scale ---------------------------------------------
# Names carry their point size so the hierarchy is visible in slide code.

SOURCES_8PT          = 800
# 8pt | sources footer and true footnote/caveat text; regular or italic.
# Also acceptable for very small axis ticks when space is constrained.

FINEPRINT_8_5PT      = 850
# 8.5pt | dense sublines, unit notes, chip bodies, second lines inside cards;
# often italic for qualifiers or regular for compact evidence.

LABEL_9PT            = 900
# 9pt | row labels, column labels, bar labels, segment labels, map-box bodies;
# often bold for structure, italic for explanatory labels.

CONNECTOR_NOTE_8_5PT = 850
# 8.5pt | short annotation along/beside a connector in a tree, flow chart,
# system map, or bus diagram; usually italic, no fill, no border.

DENSE_BODY_10PT      = 1000
# 10pt | compact body text inside dense cards, rails, ledgers, callouts,
# chart-side explanations, narrow shapes; regular unless the phrase is a label.

CHART_TITLE_10PT     = 1000
# 10pt | chart or exhibit title; Arial italic, no fill, no border. Use bold
# only if it is the main exhibit header, not a quiet chart caption.

MESSAGE_11PT         = 1100
# 11pt | short message strip, readout body, concise finding sentence,
# unit-conversion value, or boundary-ribbon body.

BODY_12PT            = 1200
# 12pt | default body text when the shape has room; regular. Use
# DENSE_BODY_10PT instead for consulting-style dense exhibits.

CAP_12PT             = 1200
# 12pt | card cap, strip cap, section cap, in-shape header; bold, often
# ALL CAPS, usually centered in dark cap shapes.

EXHIBIT_HEADER_13PT  = 1300
# 13pt | primary visual header inside a large exhibit card; bold. Use
# sparingly when a visual block needs its own local title.

VALUE_14PT           = 1400
# 14pt | compact numeric value inside a bar, chip, or small KPI cell; bold.

BADGE_16PT           = 1600
# 16pt | program badge, row identity, major gate title, or compact anchor; bold.

RIBBON_KPI_18PT      = 1800
# 18pt | boundary-ribbon KPI or short high-emphasis strip value; bold.

ANSWER_KPI_24PT      = 2400
# 24pt | answer-card KPI value; bold.

HERO_32PT            = 3200
# 32pt | one true hero headline on a content slide; bold. Use 40pt only as a
# slide-local exception for cover-like pages.

# -- Locked chrome / distinctive slides -------------------------------------
# Unchanged. Set by the chrome builders in deck_core.primitives (breadcrumb /
# title_placeholder / prelim_chip / sources_line) and the cover/divider
# layouts. Body slides should not need these directly.
SZ_BREADCRUMB       = 1000    # 10pt  breadcrumb
SZ_PRELIM           = 1200    # 12pt  Preliminary chip
SZ_SOURCES          = 800     # 8pt   sources footer
SZ_SLIDE_TITLE      = 2000    # 20pt  content-slide title ("Topic | Finding.")
SZ_SUBTITLE         = 2000    # 20pt  cover / divider subtitle (italic)
SZ_COVER_TITLE      = 2800    # 28pt
SZ_COVER_SUBTITLE   = 2000    # 20pt
SZ_DIVIDER_TITLE    = 2800    # 28pt
SZ_DIVIDER_SUBTITLE = 2000    # 20pt


# ---------------------------------------------------------------------------
# 4. Insets
# ---------------------------------------------------------------------------
# Text inset presets for text_box(insets=...) - (l, t, r, b) in EMU.

PAD_X = 91_440        # 0.10in left/right (standard)
PAD_Y = 63_500        # 0.07in top/bottom (standard)
PAD_X_LG = 114_300    # 0.125in left/right (roomier card)
PAD_Y_LG = 76_200     # 0.083in top/bottom (roomier card)

INSETS_NONE    = (0, 0, 0, 0)
INSETS_DEFAULT = (91_440, 45_720, 91_440, 45_720)
INSETS_CARD    = (PAD_X_LG, PAD_Y_LG, PAD_X_LG, PAD_Y_LG)
INSETS_CHIP    = (45_720, 9_144, 45_720, 9_144)

# Padding-by-role presets (l, t, r, b) - padding is part of the hierarchy; don't
# use one inset for every shape.
INSETS_LABEL       = INSETS_NONE                          # no-fill labels / ticks / captions
INSETS_MICRO_CAP   = (60_000, 35_000, 60_000, 35_000)     # tiny cap / small badge
INSETS_BADGE       = (120_000, 30_000, 120_000, 30_000)   # program / row-identity badge
INSETS_EVIDENCE    = (140_000, 70_000, 140_000, 70_000)   # evidence chip
INSETS_MESSAGE     = (200_000, 70_000, 200_000, 70_000)   # explanatory message panel
INSETS_RIBBON_CAP  = (140_000, 50_000, 140_000, 50_000)   # boundary-ribbon cap
INSETS_ANSWER_CARD = (200_000, 110_000, 200_000, 110_000) # focal answer card


# ---------------------------------------------------------------------------
# 5. Chrome - locked geometry + shape ids
# ---------------------------------------------------------------------------
# Values are EMU, verbatim from the locked template. Don't move these; set
# their TEXT per slide (see the chrome builders in deck_core.primitives).

# Breadcrumb (bound to slideLayout4 body placeholder idx=10).
BREADCRUMB_X, BREADCRUMB_Y, BREADCRUMB_CX, BREADCRUMB_CY = LEFT_MARGIN, 263_452, CONTENT_W, 153_888
# Title (bound to the layout title placeholder).
TITLE_X, TITLE_Y, TITLE_CX, TITLE_CY = LEFT_MARGIN, 554_500, CONTENT_W, 640_080
# Preliminary chip (top-right, flush to the content right edge).
PRELIM_X, PRELIM_Y, PRELIM_CX, PRELIM_CY = 10_267_829, 111_556, 1_467_612, 290_000
# Sources footer (bottom strip).
SOURCES_X, SOURCES_Y, SOURCES_CX, SOURCES_CY = LEFT_MARGIN, 5_930_000, CONTENT_W, 540_000

# Shape ids the chrome occupies (keep body shapes at 10+; 9999 is Sources).
SP_ID_BREADCRUMB = 2
SP_ID_TITLE      = 3
SP_ID_PRELIM     = 4
SP_ID_SOURCES    = 9999
