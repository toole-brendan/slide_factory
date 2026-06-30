"""Small local helpers for the DDG-51 distributed-shipbuilding target slides.

The helpers intentionally wrap only the public deck_core.authoring surface so the
new modules stay native-editable and do not create a second styling system.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from deck_core.authoring import (
    Chrome, IN, PT, Sources, body_slide, connector, paragraph, run, text_box,
)

FONT = "Arial"
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BREADCRUMB = "44505C"
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
BLUE_5 = "263746"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
GRAY_4 = "808080"
PALE_ORANGE = "FCE4D6"
ORANGE = "FB6B3C"
GREEN = "548235"
YELLOW = "FFF2CC"

TIGHT = dict(l_ins=45_720, t_ins=27_432, r_ins=45_720, b_ins=27_432)
MED = dict(l_ins=60_960, t_ins=45_720, r_ins=60_960, b_ins=45_720)
ZERO = dict(l_ins=0, t_ins=0, r_ins=0, b_ins=0)


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


class ShapeIds:
    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        out = self._next
        self._next += 1
        return out


def _b(value: bool) -> bool | None:
    return True if value else None


def p(text: str, *, size: float = 10, bold: bool = False, italic: bool = False,
      color: str = BLACK, align: str = "l", space_after: int = 0,
      bullet: bool = False, bullet_char: str | None = None, level: int = 0,
      mar_l: int | None = None, indent: int | None = None):
    return paragraph(
        [run(text, size=PT(size), bold=_b(bold), italic=_b(italic), color=color, font=FONT)],
        align=align,
        space_after=space_after,
        bullet=bullet,
        bullet_char=bullet_char,
        level=level,
        mar_l=mar_l,
        indent=indent,
    )


def blank(size: float = 3):
    return paragraph([], end_size=PT(size))


def paras(lines: str | Sequence[str], *, size: float = 10, bold: bool = False,
          italic: bool = False, color: str = BLACK, align: str = "l"):
    if isinstance(lines, str):
        lines = lines.splitlines() or [""]
    return [p(line, size=size, bold=bold, italic=italic, color=color, align=align) for line in lines]


def rich(parts: Sequence[tuple[str, bool, bool, str | None, float | None]], *,
         align: str = "l", space_after: int = 0):
    runs = [
        run(text, size=PT(size or 10), bold=_b(bold), italic=_b(italic),
            color=color or BLACK, font=FONT)
        for text, bold, italic, color, size in parts
    ]
    return paragraph(runs, align=align, space_after=space_after)


def bullet(text: str, *, size: float = 9, color: str = BLACK, level: int = 0):
    return p(text, size=size, color=color, bullet=True,
             bullet_char=("-" if level else "•"), level=level)


def shape(ids: ShapeIds, name: str, box: Box, paragraphs: Sequence[str], *,
          fill: str | None = None, line_color: str | None = "none",
          line_width: int = 12_700, dashed_line: bool = False,
          anchor: str = "t", prst: str = "rect", text_color: str | None = None,
          insets: dict | None = None, fill_alpha: int | None = None):
    # text_color is accepted for call-site readability; actual color lives inside the paragraphs.
    _ = text_color
    pad = insets or MED
    kwargs = dict(fill=fill, line_color=line_color,
                  line_width=line_width, dashed_line=dashed_line, anchor=anchor,
                  prst=prst, **pad)
    if fill_alpha is not None:
        kwargs["fill_alpha"] = fill_alpha
    return text_box(ids.next(), name, *box.emu(), list(paragraphs), **kwargs)


def label(ids: ShapeIds, name: str, box: Box, text: str, *, size: float = 9,
          color: str = BLACK, bold: bool = False, italic: bool = False,
          align: str = "ctr", fill: str | None = None,
          line_color: str | None = "none"):
    return shape(ids, name, box, [p(text, size=size, color=color, bold=bold,
                                   italic=italic, align=align)],
                 fill=fill, line_color=line_color, anchor="ctr", insets=TIGHT)


def card(ids: ShapeIds, name: str, box: Box, kicker: str, headline: str,
         body: str, *, fill: str = WHITE, accent: str = BLUE_4,
         headline_size: float = 16):
    return shape(
        ids, name, box,
        [
            p(kicker.upper(), size=7.5, bold=True, color=accent),
            p(headline, size=headline_size, bold=True, color=BLACK),
            p(body, size=8.5, color=BLACK),
        ],
        fill=fill, line_color=accent, line_width=12_700, insets=MED,
    )


def metric_chip(ids: ShapeIds, name: str, box: Box, value: str, label_text: str,
                *, fill: str = BLUE_1, accent: str = BLUE_4):
    return shape(
        ids, name, box,
        [p(value, size=17, bold=True, color=accent, align="ctr"),
         p(label_text, size=8, color=BLACK, align="ctr")],
        fill=fill, line_color="none", anchor="ctr", insets=TIGHT,
    )


def hline(ids: ShapeIds, name: str, x: float, y: float, w: float, *,
          color: str = DK, width: int = 12_700, dashed: bool = False):
    return connector(ids.next(), name, IN(x), IN(y), IN(w), 0,
                     color=color, width=width, dashed=dashed)


def arrow(ids: ShapeIds, name: str, x: float, y: float, w: float, *,
          color: str = DK, width: int = 12_700, dashed: bool = False):
    return connector(ids.next(), name, IN(x), IN(y), IN(w), 0,
                     color=color, width=width, dashed=dashed, arrow="head")


def vline(ids: ShapeIds, name: str, x: float, y: float, h: float, *,
          color: str = DK, width: int = 12_700, dashed: bool = False):
    return connector(ids.next(), name, IN(x), IN(y), 0, IN(h),
                     color=color, width=width, dashed=dashed)
