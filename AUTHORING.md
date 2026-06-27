# Authoring a slide module

A slide module is a plain Python file in `style_library/library/slides/`. The build
(`cd style_library && python3 build_deck.py`) imports it, calls `render()`, and packages
the result. **Learn the patterns by reading the exemplar modules**, not from a token catalog —
visible styling (hex colors, `PT()` sizes, insets) lives in the modules on purpose.

## The contract
A module may define:

| name | required | meaning |
|------|----------|---------|
| `render() -> str` | **yes** | returns the complete `<p:sld>` body |
| `LAYOUT` | no | `"slideLayout4"` (default) / `"slideLayout3"` / … |
| `CHARTS` | no | list of chart dicts from the native factories |
| `IMAGES` | no | list of `{"rId": "rIdN", "file": "<name in ppt/media>"}` |

Register the module in `style_library/library/slides/__init__.py` (import it, and add it to
`SLIDE_RENDERS` in render order).

## The one import surface
Everything an author needs comes from `deck_core.authoring`:

```python
from deck_core.authoring import (
    # units / layout
    IN, PT, BODY,
    # slide + house chrome
    slide, body_slide, Chrome, Sources,
    breadcrumb, slide_title, preliminary_chip, source_note,
    layout_title, layout_placeholder,
    # text / shapes
    run, line_break, paragraph, text_box, custom_geometry, picture, connector,
    # tables (low-level; define edge/bd/cell/rcell locally if you want them)
    table, trow, tcell, tcell_rich, tpara, trun, tbreak,
    # charts
    graphic_frame, column_chart, bar_chart, combo_chart, bubble_chart,
)
```

Colors are hex literals (`fill="CEDDEC"`), defined locally where they carry meaning
(`TAM_FILL = "B6C8D8"`). There is no shared palette, type hierarchy, or inset vocabulary —
copy a proven exemplar instead. Off the surface: `deck_core._build` (the packager, the
pipeline calls it), `deck_core.ooxml` (namespaces), `tools/slide_probe.py` (a dev inspector).
