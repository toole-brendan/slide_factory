"""Table-cell convenience kit - the small helpers that recur across slide modules.

These separate cell *content* (text, fills, spans) from cell *mechanics* (borders,
insets, anchors). They are thin wrappers over the engine's ``tcell`` / ``tcell_rich``
/ ``tpara`` primitives and emit byte-identical OOXML to writing those primitives by
hand - centralized here so authors share one vocabulary instead of re-deriving it
per slide.

  edge(color, w)            one cell-border edge dict
  bd(L=, R=, T=, B=)        border map from only the sides drawn (omitted = no-fill)
  cell(text, ...)           single-run text cell (borders via L/R/T/B=edge(...))
  rcell(paras, ...)         multi-paragraph rich cell

Borders are passed as keyword edges, e.g. ``cell("x", L=edge(GRAY_3), B=edge(BLACK))``;
``**edges`` flows through ``bd(...)`` into the primitive's ``borders=``. Insets default
to the engine's 45720 EMU (0.05in); pass ``l_ins=`` etc. for non-default padding.

Note: helpers whose defaults vary slide-to-slide stay LOCAL to the modules that use
them - they are not one-size-fits-all: the run helper ``r()`` (per-slide size), the
matrix one-run helper ``tx()``, and the empty-matrix-cell ``mt()`` (whose ``end_size``
differs by slide - some pin <a:endParaRPr> to 1pt, some don't).
"""
from __future__ import annotations

from deck_core.primitives import tcell, tcell_rich
from deck_core.style import PT, BLACK, FONT


def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell with span/anchor/insets defaulted to the engine defaults (size=PT(10) -
    the dense-table norm); borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...).
    Pass l_ins/r_ins explicitly for non-default padding (e.g. 41564); omit for the 45720 default."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))
