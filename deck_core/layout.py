"""deck_core.layout - mechanical layout constants for the build.

Units (IN, PT, EMU_PER_INCH), the canvas size, margins, and the BODY content box.
That is all. No palette, no type hierarchy, no inset presets - visible styling
lives in the slide modules (hex literals, explicit PT() sizes, explicit insets);
study the exemplars, not a token catalog. These constants are load-bearing
geometry the packager and house chrome need, kept verbatim from the locked
template so chrome stays byte-stable.
"""
from __future__ import annotations

# 16:9 widescreen, EMU (914_400 EMU per inch).
SLIDE_W = 12_192_000
SLIDE_H = 6_858_000

EMU_PER_INCH = 914_400


def IN(inches: float) -> int:
    """Inches -> EMU (rounded), e.g. text_box(.., IN(1.5), IN(0.3), ..). Raw EMU
    ints still work; a round-trip through a 3-decimal inch value is visually exact
    (sub-0.05 px) but not byte-exact, so locked chrome geometry stays verbatim EMU."""
    return round(inches * EMU_PER_INCH)


def PT(points: float) -> int:
    """Points -> 1/100 pt, the unit run(size=..) / OOXML sz use: PT(10) == 1000,
    PT(8.5) == 850."""
    return round(points * 100)


# Symmetric left/right margin used by every content slide.
LEFT_MARGIN = 453_079
RIGHT_MARGIN = LEFT_MARGIN
USABLE_W = SLIDE_W - LEFT_MARGIN - RIGHT_MARGIN          # 11_285_842

# Chrome/content column width - rounded to the source pptx grid and kept verbatim
# so chrome (breadcrumb / title / sources) stays byte-aligned with the template.
CONTENT_W = 11_282_362

# -- The authoritative body box ---------------------------------------------
# Place every body shape inside BODY so slides stay flush and clear of chrome.
BODY_X  = LEFT_MARGIN       # 453_079
BODY_Y  = 1_371_600         # 1.5in - below a 2-line title
BODY_CX = CONTENT_W         # 11_282_362
BODY_CY = 4_498_400         # -> bottom 5_870_000
BODY    = (BODY_X, BODY_Y, BODY_CX, BODY_CY)
BODY_R  = BODY_X + BODY_CX  # 11_735_441  right edge
BODY_B  = BODY_Y + BODY_CY  #  5_870_000  bottom edge

# House font. Authors may also just write FONT = "Arial" locally in a module.
DEFAULT_FONT = "Arial"
