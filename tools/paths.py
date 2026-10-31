"""Where the docs tools find their inputs.

Every path can be set with an environment variable. The defaults assume one workspace folder (DEXSUITE_WORKSPACE, by
default the folder that holds this docs repository) with the repositories side by side:

    <workspace>/Dexsuite                the DexSuite code                 DEXSUITE_REPO
    <workspace>/dexsuiteorg.github.io   the project page                  DEXSUITE_SITE
    <workspace>/paper                   the paper's LaTeX source          DEXSUITE_PAPER (optional)
    <workspace>/docs_work               scene exports and renders         DEXSUITE_DOCS_WORK
    <workspace>/fonts                   Inter (SIL Open Font License)     DEXSUITE_FONTS

BLENDER_PY is a Python with bpy 5.0.1 for the renders (render_catalog.py, render_tasks.py).
"""
from __future__ import annotations

import os
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("DEXSUITE_WORKSPACE", DOCS.parent))


def _path(var: str, default: str) -> Path:
    return Path(os.environ.get(var, WORKSPACE / default))


DEXSUITE = _path("DEXSUITE_REPO", "Dexsuite")
SITE = _path("DEXSUITE_SITE", "dexsuiteorg.github.io")
PAPER = _path("DEXSUITE_PAPER", "paper")
WORK = _path("DEXSUITE_DOCS_WORK", "docs_work")
FONTS = _path("DEXSUITE_FONTS", "fonts")
BLENDER_PY = os.environ.get("BLENDER_PY", "python")
