# Session log & handoff — `slide_factory` git init + GitHub, the full teaching-module rename sweep, the native `bubble_chart`/`combo_chart` engine factories, and full `_src` retirement

**Date:** 2026-06-27 (a later session the same day as `2026-06-27_teaching_module_curation_v2_*`)
**Project:** `/Users/brendantoole/projects3/slide_factory/` — standalone, pure-stdlib OOXML PowerPoint authoring workspace.
**Build:** `cd style_library && python3 build_deck.py` → `library.pptx`. Pure Python 3.9 stdlib, no deps, no CLI tools.
**Remote:** now a git repo — **https://github.com/toole-brendan/slide_factory**, branch `main`, HEAD at the end of this session = `cd4a319` (plus the note-removal + this log on top).
**Status at handoff:** builds green — **40 slides, 22 charts, 23 embeddings**. Every registered module is now a `*_teaching*` variant; **every chart module is self-contained** (generates its own editable `.xlsx`, reads no `_src`); **all 44 `_src` chart files (22 pairs) are orphaned**.

Big picture: this session took the curated corpus and (1) put it under **git + GitHub**, (2) finished migrating **all 40 registered modules** to hand-authored `*_teaching` / `*_teaching_factory_{chart,table}` variants (deleting every old non-teaching module), (3) drove the **chart-construction convergence** to completion — first by converting most `styled_chart`/`_src` charts to native factories module-by-module, then by adding the two missing chart varieties (**`bubble_chart`, `combo_chart`**) to the engine via a deep-research agent and converting the last four `_src`-backed modules to use them. Net result: zero `_src` reads anywhere in the live deck.

---

## 0. Git initialization + GitHub (commit `66341b8` …)

The repo did not exist at session start (`git init` had been declined historically). Set it up against the user's fresh empty GitHub repo:

- `git init -b main`; **local** identity set to `Brendan Toole <toole.brendan@gmail.com>` (the global git email was a machine hostname — kept it out of a public repo). `gh` was already authed as `toole-brendan` over https → `gh auth setup-git`, remote `origin`, pushed.
- **`.gitignore`**: `.DS_Store`, `__pycache__/`, `*.py[cod]`, MS Office lock files (`~$*` — a `~$library.pptx` PowerPoint lock had snuck into staging), and initially `style_library/library.pptx`.
- **`library.pptx` is tracked** (user asked to add it; un-ignored in `a89032a`) so the built deck is viewable from GitHub. Rebuild with `cd style_library && python3 build_deck.py`.
- Initial commit = 168 files (engine, style library, template, `infra/`, `_src/`, both prior logs).
- `production_outlook_separate.py` was deleted-on-disk-but-still-tracked at init; committed the deletion (`f86dd7f`) — it was already unregistered dead code.

**Verification habit established this session:** after every change, `git push` then assert `local HEAD == git ls-remote origin main`.

---

## 1. The full teaching-module rename sweep (commits `482707f` → `f352ed1`, plus engine work below)

The transcript's "teaching rewrite" workstream, carried to completion. The user delivered hand-authored replacement modules from `~/Downloads` in batches; each was swapped in under a consistent **convention**:

> **"swap out" = put the new module in, DELETE the old one (`git rm`), repoint the registry — don't leave old files hanging around in the repo.**

Mechanics per swap:
- New module keeps its full `*_teaching*` filename; the old non-teaching module is `git rm`-ed.
- `style_library/library/slides/__init__.py` is repointed in **both** places — the `from . import (...)` block **and** the `SLIDE_RENDERS` tuple list. (Imports are order-independent; only `SLIDE_RENDERS` order sets slide order.)
- Same-named overwrites (e.g. a revised `*_teaching.py`) need **no** registry change.
- Rebuild → verify the affected slide(s) in the `.pptx` (chart parts / table counts / first text runs) → commit → push.

**Pre-flight checklist run on every incoming module** (a script/grep, not by eye):
1. defines `render()` and carries `LAYOUT` / `CHARTS` / (`IMAGES`);
2. **actual** asset reads (`.read_text`/`.read_bytes`/`_asset_path`/`open(`) vs. mere comment/metadata mentions of `slideNN_chartMM` — the modules name their source assets in `"source_chart_assets"` provenance dicts and `ValueError` validation strings, which are **not** reads;
3. required `_src`/image assets exist on disk;
4. **Python-3.9 safety** (see §2).

Modules converted (final render slot in parens): overview(22), key_terms_glossary(23), key_findings ×3 (24–26), archetype_comps newbuild/vocc/shipbuilder, status_quo_outlook oceangoing/offshore_1/offshore_2, ships_act volume/plus/captive, assumptions 1/2 (32/33), approach_unit_economics(34), freight_charges(35), coordination_archetypes(36), key_inputs(37), comparison_vs_ddgs(38), production_outlook colocated/separate (39/40), plus the earlier-promoted front exemplars. **End state: all 40 registered modules are `*_teaching*`; no non-teaching module remains** (verified `git ls-files` after each batch).

---

## 2. GOTCHA — Python 3.9 and runtime PEP 604 unions (fixed in `482707f`)

The build runs on **Python 3.9.6**. `coordination_archetypes_teaching_factory_table.py` shipped with a **module-level** `CellContent = str | RichCellContent` — a runtime `X | Y` union, which 3.9 rejects (`TypeError: unsupported operand type(s) for |: 'type' and 'types.GenericAlias'`). `from __future__ import annotations` only defers unions in **annotation position** (function signatures, dataclass fields stay lazy strings); a bare module-level alias assignment is evaluated eagerly. Fix: `from typing import Union` + `CellContent = Union[str, RichCellContent]`.

**This is now a standing pre-flight check:** `grep -nE "^[A-Za-z_][A-Za-z0-9_]* *=.*\|"` on every incoming module. All later modules were clean.

---

## 3. Chart-construction convergence — module-by-module (commits `2baf1d8`, `da01aa2`, and the chart swaps)

Three chart-construction routes existed in the corpus:
- **Native engine factory** (the target): `column_chart`/`bar_chart`(`**CHART_STYLE`) → builds the chart part **and** a fresh editable `.xlsx` from a declarative Python spec; reads nothing.
- **Local helper**: the module defines its **own** chart-builder (e.g. `def stacked_area_chart(...)`) using the engine's low-level `_build_embed_xlsx` + raw chart XML, because the engine lacks that chart type. Self-contained, but the factory logic is copied into the module rather than shared. **Only** `ships_act_volume`(29) and `ships_act_plus_volume`(30) use this (both for stacked-area).
- **`_src`-backed** (`styled_chart` / `editable_bundled_chart`): reads `_src/slideNN_chartMM.{xml,xlsb}` at import. The non-target route.

Early in the session several chart modules were swapped in still using the `_src` route, then the user supplied self-contained re-exports that were swapped over them: `status_quo_outlook_oceangoing` (styled→native `column_chart(stacked)`, renamed off the `_factory_chart` suffix to plain `_teaching`) and `ships_act_volume` (styled→local `stacked_area_chart`). A couple of "(1)" re-downloads were caught as **byte-identical no-ops** via `diff` before wasting a swap.

### The `_src` audit (ground truth, not grep)
To answer "which `_src` files are actually used," monkey-patched `pathlib.Path.read_text`/`read_bytes`/`open` to record any path under `_src/`, then imported the registry and ran every `render()`. At that point: **44 `_src` files = 22 pairs; only 4 pairs (8 files) were read** — by exactly four modules still on the `_src` route:

| `_src` pair | Reader | Route |
|---|---|---|
| `slide32_chart17` | `archetype_comps_newbuild_prices_teaching` | `editable_bundled_chart` |
| `slide33_chart18` | `archetype_comps_vocc_performance_teaching` | `editable_bundled_chart` |
| `slide45_chart27` | `status_quo_outlook_offshore_1_teaching` | `styled_chart` |
| `slide46_chart28` | `status_quo_outlook_offshore_2_teaching` | `styled_chart` |

(Also confirmed 40 modules on disk == 40 registered, so no unregistered "stray" readers skew the audit.) These four were the **only** remaining `_src` dependents — and their charts were types the engine had no native factory for.

---

## 4. The deep-research agent hand-off — engine additions, two sessions (package outside the repo)

The four `_src` charts were inspected from their source XML: `slide32_chart17` / `slide33_chart18` = **bubble charts**; `slide45_chart27` = **stacked bar**; `slide46_chart28` = **stacked bar + line combo**. The engine (`deck_core/charts.py`) exposed `column_chart, bar_chart, line_chart, waterfall_chart, marimekko_chart` — **no `bubble_chart`, no combo**. So a native conversion required engine work first.

Built a self-contained package the user could hand to an external agent — **`/Users/brendantoole/projects3/slide_factory_chart_conversion/`** (deliberately **outside** the repo, so it never shows as a repo change):
```
PROMPT_1_engine.txt   PROMPT_2_modules.txt
defective_modules/    the 4 _src-backed modules (the targets)
reference_modules/    8 self-contained exemplars (incl. ships_act_*_factory_chart, production_outlook_separate, oceangoing, shipbuilder_margins)
source_chart_assets/  slide32/33/45/46 .xml + .xlsb (8 files)
engine/               deck_core: charts.py, primitives.py, style.py, ooxml.py, authoring.py, table_kit.py, chart_key.py, AUTHORING_API.md
```
Two-session plan (the user runs them sequentially in separate agent sessions): **Session 1** = add `bubble_chart` + stacked-bar+line combo natively to the engine, additive only, 3.9-safe, re-export through `authoring.py`, return full drop-in `deck_core` files + usage spec. **Session 2** (fresh session, with the updated engine already in place) = rewrite the 4 modules to call the new factories, transcribing exact values/colors/axes from the source XML so they render identically. File-location convention in the prompts: the session's **focus is "attached"** (source assets for S1; defective modules for S2), everything else lives in the project's **"source" directory**. After S1 landed, the package's `engine/` was refreshed to the post-S1 files so S2 would see the real new signatures.

---

## 5. Engine update — native `bubble_chart` + `combo_chart` (commit `0f7fab7`, **output-neutral**)

Session-1 output (`Downloads/authoring.py`, `Downloads/charts.py`) swapped into `deck_core/`. What changed:
- **`charts.py`** (85K→118K): added `combo_chart(*, mode="stacked", **kwargs)` and `bubble_chart(...)` plus ~18 private helpers (`_build_bubble_series`, `_bubble_axis_xml`, `_chart_*` shared XML emitters, etc.). **No existing `def` removed or renamed.**
- **`authoring.py`**: re-exports `bubble_chart`, `combo_chart` (both land in `__all__`, which is derived from imports).

**Output-neutrality proof (the project's standard method):** snapshotted all 62 rendered slide+chart XML parts from the pre-swap `library.pptx` to scratch, swapped the engine, rebuilt, and SHA-256-diffed every part → **0 of 62 changed**. An additive engine change must leave every existing slide byte-identical; it did. New factories confirmed callable via `deck_core.authoring` and present in `__all__`; both 3.9-clean. (Agent added bubble + combo only — **not** `stacked_area_chart`, so the two local-helper modules in §3 still carry their own.)

---

## 6. Converting the last four modules to native factories (commit `9e256c2`) + promotion to front (`cd4a319`)

Session-2 output swapped in (same module names → no registry change):
- `archetype_comps_newbuild_prices_teaching`, `archetype_comps_vocc_performance_teaching` → **`bubble_chart(**CHART_STYLE)`** → render `<c:bubbleChart>`, 7 series each, fresh `.xlsx`.
- `status_quo_outlook_offshore_1_teaching` → **`column_chart(**CHART_STYLE)`** → stacked `<c:barChart>`, 2 series.
- `status_quo_outlook_offshore_2_teaching` → **`combo_chart(**CHART_STYLE)`** → one part with both `<c:barChart>`(stacked) + `<c:lineChart>`(standard), 3 series.

All four now read **no** `_src`. Re-ran the read-trace audit: **USED `_src` files = NONE; 44 of 44 orphaned.** Build still 40 slides / 22 charts.

Then promoted all four to the **first four render slots** (the three already-front ones kept their order; `offshore_1` moved up to slot 4). Final front order: 1 `vocc_performance`(bubble) · 2 `offshore_2`(combo) · 3 `newbuild_prices`(bubble) · 4 `offshore_1`(stacked bar). The user then asked to **remove the leftover `# NOTE:` breadcrumb** at `offshore_1`'s former position (no note at all there) — done (this commit, on top of `cd4a319`).

---

## 7. Current state & what's open

- **18 chart-bearing modules → 22 chart parts**, all self-contained. Chart routes now: native factory (most), local `stacked_area_chart` helper (only slides 29–30), `_src` (**none**).
- **All 44 `_src` files (22 pairs) are orphaned** — nothing reads them. They split into: (a) provenance-traceable (named in a now-native module's comments/validation), and (b) referenced nowhere at all (`slide19_chart3`, `slide25_chart5`, `slide53_chart32`). **User explicitly chose NOT to delete any yet** — audit-only. Safe-to-delete candidates when ready: bucket (b) first; bucket (a) optionally keep as provenance or move to `_src/_archive/`.
- **Open / deferred:**
  - Retire/archive the orphaned `_src/` files (user's call; nothing references them).
  - Optionally add **`stacked_area_chart`** to the engine (session-1 scope creep that wasn't done), then simplify `ships_act_volume`(29) + `ships_act_plus_volume`(30) to drop their local helpers → would make **every** chart module call a shared engine factory (full DRY uniformity).
  - The `slide_factory_chart_conversion/` package (outside the repo) still has the two prompts; `PROMPT_1` is now spent (engine done) — only `PROMPT_2` would be reused, and only if more `_src` modules appear.

**Verification methodology to reuse** (unchanged and load-bearing): per-slide/chart **byte-diff against a pre-change snapshot** for output-neutral engine/refactor work; a **monkey-patched read-trace** (`pathlib.Path.read_text/read_bytes/open`) over a full `render()` pass for ground-truth asset-usage audits; and the **3.9 module-level-union grep** + **actual-read vs. comment-mention grep** as standing module pre-flight checks. After any change: rebuild, verify the affected `.pptx` parts, commit, push, and assert `local HEAD == origin/main`.
