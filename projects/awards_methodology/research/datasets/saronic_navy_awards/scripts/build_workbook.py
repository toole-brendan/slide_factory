"""Build the Saronic USV awards-evidence mini-workbook.

Run:
    python build_workbook.py

Resolves the repo root (for workbook_core) and this dir (for the `workbook`
package) onto sys.path, renders the five tabs, and writes the xlsx next to the
extracted/ pulls.
"""
from __future__ import annotations

import pathlib
import sys


def _bootstrap_path() -> pathlib.Path:
    here = pathlib.Path(__file__).resolve().parent          # .../research/contracts
    root = here
    while root != root.parent and not (root / "workbook_core").is_dir():
        root = root.parent
    for p in (str(root), str(here)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return root


def build() -> int:
    _bootstrap_path()
    from workbook_core.lib import package_workbook
    from workbook.paths import OUT
    from workbook.sheets import SHEETS

    return package_workbook(
        OUT, SHEETS,
        title="Saronic USV Awards Evidence",
        creator="Saronic market intelligence",
        app_name="Saronic awards workbook",
        normalize_dashes=True,
    )


if __name__ == "__main__":
    sys.exit(build())
