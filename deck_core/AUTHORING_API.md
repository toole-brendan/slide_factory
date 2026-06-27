# Authoring API — quick reference

Everything a slide module needs comes from **one** import surface:

```python
from deck_core.authoring import (
    slide, text_box, table, trow, cell, rcell, edge, bd,
    IN, PT, BLACK, BLUE_3, GRAY_3, FONT, BODY, BODY_12PT,
    graphic_frame, styled_chart,
)
```

`deck_core.authoring` re-exports the names below from the engine's internal
modules (`primitives`, `style`, `charts`, `chart_key`, `table_kit`). You never
need to import those modules directly. A module file is one slide: it defines
`LAYOUT`, optional `CHARTS`/`IMAGES`, and a `render()` that returns `slide(...)`.

**Not on this surface** (import directly only if you truly need it):
`deck_core.lib.build_pptx` (the packager — the pipeline calls it, not slide
bodies), `deck_core.ooxml` (namespace plumbing), `deck_core.slide_probe` (the
read-only geometry inspector), and `deck_core.text_metrics` (a rough overflow
*smoke alarm*, **not** a fit guide — judge text fit from the exemplar modules).

---

## Slide & chrome
| name | what it does |
|---|---|
| `slide(body, ...)` | wrap a list of shape XML into a complete `<p:sld>` |
| `cover_layout(...)` / `section_divider_layout(...)` | full-bleed cover / section-divider bodies |
| `breadcrumb(...)` | top-left section breadcrumb chrome |
| `title_placeholder(...)` | slide title |
| `prelim_chip(...)` | the "Preliminary" chip |
| `sources_line(...)` | bottom sources/footnote line |

## Text
| name | what it does |
|---|---|
| `text_box(sp_id, name, x, y, cx, cy, paras, ...)` | a free text box |
| `paragraph(runs, align=, ...)` / `run(text, size=, color=, font=, ...)` | paragraph / styled run |
| `line_break()` | soft line break within a paragraph |
| `esc(s)` | XML-escape a string for raw OOXML |

## Shapes & connectors
| name | what it does |
|---|---|
| `custom_geometry(...)` | arbitrary path shape |
| `picture(...)` | image (wired via the module's `IMAGES`) |
| `connector(...)` | straight/elbow connector line |

## Tables & the table kit
| name | what it does |
|---|---|
| `table(sp_id, name, x, y, cx, cy, *, col_widths, rows)` | the table frame |
| `trow(cells, h=)` | one table row |
| `tcell(text, ...)` / `tcell_rich(paras, ...)` | low-level cells (engine primitives) |
| `tpara(...)` / `trun(...)` / `tbreak()` | table paragraph / run / break |
| **`cell(text, *, …, L=edge(...), B=edge(...))`** | single-run cell + borders/insets (kit) |
| **`rcell(paras, *, …, **edges)`** | multi-paragraph cell + borders/insets (kit) |
| **`edge(color, w=12700)`** | one border edge |
| **`bd(L=, R=, T=, B=)`** | border map from only the sides drawn |

Borders pass as keyword edges: `cell("12%", align="r", L=edge(GRAY_3), B=edge(BLACK))`.
Insets default to `45720` EMU (0.05in); pass `l_ins=`/`r_ins=`/`t_ins=`/`b_ins=` to override.
Helpers whose defaults are slide-specific stay **local** to the modules that use
them — the run helper `r()` (per-slide size), the matrix one-run helper `tx()`, and
the empty-matrix-cell `mt()` (its `end_size` differs by slide).

## Charts
| name | what it does |
|---|---|
| `styled_chart(...)` | data-over-template: rewrite a source chart's data cache from a Python dict, keep its style |
| `graphic_frame(...)` | the frame that hosts a chart part |
| `editable_bundled_chart(...)` | verbatim-bundled source chart with its workbook reattached |
| `column_chart` / `bar_chart` / `line_chart` / `waterfall_chart` / `marimekko_chart` | native chart factories |
| `THINKCELL_BARS` | house static think-cell bar style (pair with `chart_key`) |
| `chart_key(...)` / `chart_legend(...)` | manual swatch+label legends |

**Which chart?** mimic a pristine source chart → `styled_chart`; new basic chart →
`column_chart`/`bar_chart`/`line_chart`; house static think-cell look →
`THINKCELL_BARS` + `chart_key`; exact copied source chart → `editable_bundled_chart`.

## Tokens (`style`)
- **Units:** `IN(inches)`, `PT(points)` → EMU. `EMU_PER_INCH`.
- **Canvas / BODY:** `SLIDE_W`, `SLIDE_H`, `LEFT_MARGIN`, `RIGHT_MARGIN`, `USABLE_W`,
  `CONTENT_W`, `BODY` (and `BODY_X/Y/CX/CY/R/B`).
- **Palette:** `BLACK`, `WHITE`, `BODY_TEXT`, `DK`, `BREADCRUMB`, `PRELIM`;
  `BLUE_1..5`, `GRAY_1..5` (general use); `CHART_ACCENT_1..6` (**charts only**).
  Paired text: `BLUE_SCALE`/`BLUE_TEXT`, `GRAY_SCALE`/`GRAY_TEXT`; helpers
  `blue_pair(i)`, `gray_pair(i)`, `chart_accent_pair(i)`, `chart_accent_seq(n)`.
- **Type scale:** `FONT`; `SOURCES_8PT`, `FINEPRINT_8_5PT`, `LABEL_9PT`,
  `DENSE_BODY_10PT`, `CHART_TITLE_10PT`, `MESSAGE_11PT`, `BODY_12PT`, `CAP_12PT`,
  `EXHIBIT_HEADER_13PT`, `VALUE_14PT`, `BADGE_16PT`, `RIBBON_KPI_18PT`,
  `ANSWER_KPI_24PT`, `HERO_32PT`; `LNSPC_BODY`, `LNSPC_SINGLE`.
- **Insets:** `INSETS_NONE`, `INSETS_DEFAULT`, `INSETS_CARD`, `INSETS_CHIP`,
  `INSETS_LABEL`, `INSETS_MICRO_CAP`, `INSETS_BADGE`, `INSETS_EVIDENCE`,
  `INSETS_MESSAGE`, `INSETS_RIBBON_CAP`, `INSETS_ANSWER_CARD`; `PAD_X/Y(_LG)`.
- **Chrome sizes/ids:** `SZ_*` (breadcrumb/title/subtitle/cover/divider) and
  `SP_ID_BREADCRUMB/TITLE/PRELIM/SOURCES`.
