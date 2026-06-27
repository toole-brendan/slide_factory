"""Think-cell-style chart color key — a manual legend for native charts that drop
the native legend (the think-cell look; see THINKCELL_BARS in deck_core.charts).
Emits one horizontal row of [swatch + label] entries: a small filled rect in the
chart accent color + a quiet 8.5pt label, packed left-to-right from `x`. Each
label's width is estimated via the deck's Arial char-width model so the row stays
tight regardless of label length.

Pair the swatch fills with deck_core.style.chart_accent_seq(n). The key's
geometry/placement is the caller's — typically a thin band where the dropped
native legend used to sit (shrink the chart graphic_frame by the band height).
"""
from __future__ import annotations

from deck_core.primitives import run, paragraph, text_box
from deck_core.style import BLACK, FONT, FINEPRINT_8_5PT, BODY_12PT, INSETS_NONE

# Arial average glyph advance / font size, in EMU — the deck's text-width model
# (formerly deck_core.text_metrics.avg_char_width_emu, inlined here as its last user).
_EMU_PER_POINT = 12_700
_AVG_CHAR_WIDTH_RATIO = 0.50


def _avg_char_width_emu(size_pt: float) -> float:
    """Approximate average Arial glyph advance at `size_pt`, in EMU."""
    return size_pt * _AVG_CHAR_WIDTH_RATIO * _EMU_PER_POINT

_SWATCH = 96_000          # ~0.105in filled square (matches the chart's 8pt scale)
_GAP_SW_LABEL = 50_000    # swatch -> its own label
_GAP_ENTRY = 200_000      # one entry's label -> the next swatch
_LABEL_PAD = 44_000       # slack added to each estimated label width
# Capital-heavy short labels run wider than the 0.50 avg-char model predicts, so
# pad the *spacing* estimate; labels themselves use wrap="none" and never wrap.
_WIDTH_SAFETY = 1.25


def chart_key(sp_id: int, x: int, y: int, h: int, entries,
              *, label_size: int = FINEPRINT_8_5PT) -> str:
    """Horizontal color key. `entries` is a list of (label, fill_hex). Returns
    concatenated <p:sp> XML: per entry a no-border filled-rect swatch + a
    vertically-centered label. Lays out from `x`; `h` is the band height the
    swatches/labels center within. `sp_id` is the first shape id; each entry
    consumes two ids (swatch, label)."""
    char_w = _avg_char_width_emu(label_size / 100.0) * _WIDTH_SAFETY
    parts: list[str] = []
    cx = x
    sid = sp_id
    for label, fill in entries:
        sw_y = y + (h - _SWATCH) // 2
        parts.append(text_box(
            sid, "ChartKeySwatch", cx, sw_y, _SWATCH, _SWATCH,
            [paragraph([])],
            fill=fill, line_color=None, anchor="ctr", insets=INSETS_NONE))
        sid += 1
        lx = cx + _SWATCH + _GAP_SW_LABEL
        lw = int(len(label) * char_w) + _LABEL_PAD
        parts.append(text_box(
            sid, "ChartKeyLabel", lx, y, lw, h,
            [paragraph([run(label, size=label_size, color=BLACK, font=FONT)])],
            fill=None, line_color=None, anchor="ctr", wrap="none",
            insets=INSETS_NONE))
        sid += 1
        cx = lx + lw + _GAP_ENTRY
    return "".join(parts)


# Reference (think-cell) legend geometry: a rectangular swatch + a 12pt label per
# entry, laid out left-to-right and centered on a target x. Larger and heavier
# than chart_key() (the quiet 8.5pt side-key) — use it where the source places a
# full legend centered above or below the plot.
_LEG_SW_W = 179_388          # swatch width  (matches the reference swatch rect)
_LEG_SW_H = 133_350          # swatch height
_LEG_GAP_SW_LABEL = 60_000   # swatch -> its own label
_LEG_GAP_ENTRY = 200_000     # one entry's label -> the next swatch


def chart_legend(sp_id: int, entries, *, cy: int,
                 x_center: int | None = None, x: int | None = None,
                 label_size: int = BODY_12PT) -> str:
    """Horizontal legend matching the think-cell reference: a rectangular swatch +
    a 12pt label per entry, the whole row vertically centered on `cy`. Provide
    either `x_center` (center the row on that x — typically the body mid-x) or `x`
    (pin the row's left edge). `entries` is a list of (label, fill_hex); each
    consumes two shape ids (swatch, label)."""
    char_w = _avg_char_width_emu(label_size / 100.0) * _WIDTH_SAFETY
    label_w = [int(len(label) * char_w) + _LABEL_PAD for label, _ in entries]
    if x is None:
        total = sum(_LEG_SW_W + _LEG_GAP_SW_LABEL + lw for lw in label_w) \
            + _LEG_GAP_ENTRY * (len(entries) - 1)
        x = (x_center or 0) - total // 2
    parts: list[str] = []
    cx = x
    sid = sp_id
    sw_y = cy - _LEG_SW_H // 2
    for (label, fill), lw in zip(entries, label_w):
        parts.append(text_box(
            sid, "LegendSwatch", cx, sw_y, _LEG_SW_W, _LEG_SW_H,
            [paragraph([])],
            fill=fill, line_color=None, anchor="ctr", insets=INSETS_NONE))
        lx = cx + _LEG_SW_W + _LEG_GAP_SW_LABEL
        parts.append(text_box(
            sid + 1, "LegendLabel", lx, cy - _LEG_SW_H, lw, _LEG_SW_H * 2,
            [paragraph([run(label, size=label_size, color=BLACK, font=FONT)])],
            fill=None, line_color=None, anchor="ctr", wrap="none",
            insets=INSETS_NONE))
        cx = lx + lw + _LEG_GAP_ENTRY
        sid += 2
    return "".join(parts)
