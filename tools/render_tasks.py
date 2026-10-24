#!/usr/bin/env python
"""One still per task for the docs: the scene at reset, robot and objects, on white with a soft contact shadow.

Same two-pass framing as render_catalog.py (a coarse render measures the content, the final camera keeps the position
and fits lens and shift), then the alpha is faded near the edges so no shadow ends in a line.

    .venv-dexsuite/bin/python tools/render_tasks.py [--only lift stack ...] [--gpu 0]

Reads runs/docs_tasks/<task>/scene.json (tools/export_task_scene.py); writes docs/source/_static/tasks/<task>.webp.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from catalog_data import TASKS  # noqa: E402

DOCS = Path(__file__).resolve().parents[1]
SCENES = Path("/efs/projects/fudi/runs/docs_tasks")
WORK = Path("/efs/projects/fudi/runs/docs_task_renders")
RENDER = Path("/efs/projects/fudi/dexsuite_website/v2/tools/render_replay.py")
BLENDER_PY = "/tmp/hoirfig/bpyenv/bin/python"
OUT = DOCS / "docs/source/_static/tasks"
W, H = 1280, 800
GRAPHITE = {"color": "#2b2d32", "rough": 0.42, "coat": 0.25}
HIDE = ["object:pan_target", "object:drill_tip", "object:mat_collision"]
VIEW = {"default": (-38, 30), "bimanual": (-8, 32)}


def roles_of(scene):
    sc = json.load(open(scene))
    return sorted({m["role"] for m in sc["meshes"] if m["role"] not in ("table", "floor") and m["role"] not in HIDE}), sc


def lights(c):
    x, y, z = c
    return [{"type": "AREA", "energy": 560, "size": 4.0, "loc": [x + 0.5, y - 1.0, z + 3.4], "target": [x, y, z]},
            {"type": "AREA", "energy": 80, "size": 5.0, "loc": [x - 2.0, y + 0.8, z + 2.8], "target": [x, y, z + 0.1]},
            {"type": "AREA", "energy": 220, "size": 1.5, "loc": [x - 0.8, y + 2.0, z + 2.6], "target": [x, y, z + 0.15]}]


def shot(scene, roles, cam, out, res, samples, floor_z, centre, shadow=True):
    s = {"scene": str(scene), "out": str(out), "res": list(res), "samples": samples, "camera": cam,
         "hide_roles": ["floor", "table"], "only_roles": roles, "shadow_catcher": shadow, "floor_z": floor_z,
         "floor_center": [float(centre[0]), float(centre[1])], "overwrite": True, "lights": lights(centre),
         "materials": {"hand": GRAPHITE, "mount": GRAPHITE}}
    Path(out).mkdir(parents=True, exist_ok=True)
    p = Path(out) / "shot.json"
    p.write_text(json.dumps(s, indent=1))
    return p


def render(p, gpu, log):
    with open(log, "w") as f:
        subprocess.run([BLENDER_PY, str(RENDER), str(p)], env=dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu)),
                       stdout=f, stderr=subprocess.STDOUT, check=True)


def soften_shadow(im, k=0.5):
    """Shadow-catcher pixels are semi-transparent near-black; objects are opaque. Lighten only the shadow."""
    px = np.asarray(im, np.float32)
    shadow = (px[..., 3] < 250) & (px[..., :3].max(-1) < 40)
    px[..., 3] = np.where(shadow, px[..., 3] * k, px[..., 3])
    return Image.fromarray(px.astype(np.uint8), "RGBA")


def edge_fade(im, band=0.07):
    a = np.asarray(im.getchannel("A"), np.float32)
    h, w = a.shape
    sm = lambda x: x * x * (3 - 2 * x)  # noqa: E731
    fx = sm(np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / (band * w), 0, 1))
    fy = sm(np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / (band * h), 0, 1))
    im.putalpha(Image.fromarray((a * fy[:, None] * fx[None, :]).astype(np.uint8)))
    return im


HERO = Path("/efs/projects/fudi/dexsuite_website/v2/work/frames/hero_scene/f0000.png")


def from_hero():
    """Spray Graffiti paints its stencil onto the paper texture at runtime, which a static export does not carry.
    Use the project page's fixed-camera replay frame instead (hand, can and the stencil on the sheet)."""
    im = Image.open(HERO).convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox())
    k = min(W * 0.8 / im.width, H * 0.86 / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
    OUT.mkdir(parents=True, exist_ok=True)
    out.save(OUT / "spray_graffiti.webp", "WEBP", quality=88, alpha_quality=92, method=5)


def one(task, gpu):
    if task["key"] == "spray_graffiti":
        return from_hero()
    scene = SCENES / task["key"] / "scene.json"
    roles, sc = roles_of(scene)
    focus = [r for r in roles if r.startswith("object") or r == "hand"]          # frame the task, not the whole robot
    pts = np.array([np.array(m["frames"][0])[:3, 3] for m in sc["meshes"] if m["role"] in focus])
    c = (pts.min(0) + pts.max(0)) / 2
    ext = float(np.linalg.norm(pts.max(0) - pts.min(0)))
    floor_z = sc.get("table_z") if sc.get("table_z") is not None else float(pts[:, 2].min())
    az, el = VIEW["bimanual" if task["group"] == "bimanual" else "default"]
    a, e = math.radians(az), math.radians(el)
    d = np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)])
    cam = {"loc": (c + d * max(0.8, 2.2 * ext)).round(4).tolist(), "target": c.round(4).tolist(), "lens": 28}
    w = WORK / task["key"]
    render(shot(scene, focus, cam, w / "p1", (W // 4, H // 4), 6, floor_z, c, shadow=False), gpu, w / "p1.log")
    im = Image.open(next((w / "p1").glob("f*.png")))
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()        # objects and hand, no shadow
    u0, v0, u1, v1 = bb[0] / im.width, bb[1] / im.height, bb[2] / im.width, bb[3] / im.height
    m = min(0.72 / (u1 - u0), 0.72 / (v1 - v0))                                    # leave room for the arm and shadow
    du, dv = (u0 + u1) / 2 - 0.5, ((v0 + v1) / 2 - 0.5) * H / W                    # shift is in units of the width
    cam2 = dict(cam, lens=round(cam["lens"] * m, 3), shift_x=round(m * du, 4), shift_y=round(-m * dv, 4))
    render(shot(scene, roles, cam2, w / "p2", (W, H), 128, floor_z, c), gpu, w / "p2.log")
    OUT.mkdir(parents=True, exist_ok=True)
    fin = edge_fade(soften_shadow(Image.open(next((w / "p2").glob("f*.png"))).convert("RGBA")))
    fin.save(OUT / f"{task['key']}.webp", "WEBP", quality=88, alpha_quality=92, method=5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--gpu", default="0")
    a = ap.parse_args()
    for t in TASKS:
        if a.only and t["key"] not in a.only:
            continue
        if not (SCENES / t["key"] / "scene.json").exists():
            print("no scene", t["key"], flush=True)
            continue
        try:
            one(t, a.gpu)
            print("ok", t["key"], flush=True)
        except Exception as ex:
            print("FAILED", t["key"], ex, flush=True)


if __name__ == "__main__":
    main()
