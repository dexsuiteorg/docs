#!/usr/bin/env python
"""DexSuite wordmark as SVG outlines (Inter Bold, -0.05em tracking, the website's blue gradient).

    .venv-dexsuite/bin/python tools/make_wordmark.py
writes docs/source/_static/brand/wordmark.svg (navbar logo) and wordmark-white.svg (for dark backgrounds).
"""
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT = Path("/efs/projects/fudi/scripts/analysis/hoir_pipeline_figure/fonts/Inter-Bold.ttf")
OUT = Path(__file__).resolve().parents[1] / "docs/source/_static/brand"
TEXT, TRACK = "DexSuite", -0.05            # tracking in em, as the website h1

f = TTFont(str(FONT))
upm = f["head"].unitsPerEm
cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
asc, desc = f["hhea"].ascent, f["hhea"].descent
pen, bounds = SVGPathPen(gs), BoundsPen(gs)
x = 0
for ch in TEXT:
    g = cmap[ord(ch)]
    for p in (pen, bounds):
        gs[g].draw(TransformPen(p, (1, 0, 0, -1, x, asc)))     # flip y: font units are y-up
    x += hmtx[g][0] + TRACK * upm
x0, y0, x1, y1 = bounds.bounds                                   # the ink box, padded a little
pad = 0.03 * upm
left, w, top, bottom = x0 - pad, x1 - x0 + 2 * pad, y0 - pad, y1 + pad
d = pen.getCommands()
OUT.mkdir(parents=True, exist_ok=True)
for name, fill, defs in (
    ("wordmark.svg", "url(#g)", '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0.18">'
                                '<stop offset="0" stop-color="#1468b8"/><stop offset="0.6" stop-color="#289be4"/>'
                                '<stop offset="1" stop-color="#45b2ee"/></linearGradient></defs>'),
    ("wordmark-white.svg", "#ffffff", ""),
):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left:.0f} {top:.0f} {w:.0f} {bottom - top:.0f}" role="img" aria-label="DexSuite">'
           f'{defs}<path fill="{fill}" d="{d}"/></svg>\n')
    (OUT / name).write_text(svg)
    print(name, len(svg) // 1024, "KB", f"{w:.0f}x{bottom - top:.0f}")
