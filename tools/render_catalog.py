#!/usr/bin/env python
"""Catalog renders for the docs: every arm on its own, every end-effector on its own, the integrated robots whole.

Two passes per asset. A quick wide render measures where the robot lands in the frame, then the final render uses
the same camera position with the lens and sensor shift fitted so every asset fills the frame the same way.
Transparent backgrounds, no floor shadow, the project page's studio lights and graphite hands.

    .venv-dexsuite/bin/python tools/render_catalog.py [--only arm_franka ee_allegro ...] [--gpu 0]

Reads the Genesis exports of the website pipeline (dexsuite_website/v2/work/robots/<arm>__<grip>/scene.json), or the
docs' own re-exports in runs/docs_catalog/exports when one exists (arms whose home pose or mount changed since),
renders with dexsuite_website/v2/tools/render_replay.py (Blender Cycles), and writes
docs/source/_static/catalog/<name>.webp (900 px, transparent).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

DOCS = Path(__file__).resolve().parents[1]
SITE = Path("/efs/projects/fudi/dexsuite_website/v2")
ROBOTS = [Path("/efs/projects/fudi/runs/docs_catalog/exports"), SITE / "work/robots"]   # first match wins
RENDER = SITE / "tools/render_replay.py"
BLENDER_PY = "/tmp/hoirfig/bpyenv/bin/python"
OUT = DOCS / "docs/source/_static/catalog"
WORK = Path("/efs/projects/fudi/runs/docs_catalog")
GRAPHITE = {"color": "#2b2d32", "rough": 0.42, "coat": 0.25}
LIGHTS = [  # same as the project page robot stills
    {"type": "AREA", "energy": 520, "size": 3.5, "loc": [0.9, -1.3, 3.4], "target": [0.3, 0, 0.3]},
    {"type": "AREA", "energy": 110, "size": 4.0, "loc": [-2.2, 0.6, 1.6], "target": [0.3, 0, 0.4]},
    {"type": "AREA", "energy": 300, "size": 1.2, "loc": [-0.6, 2.2, 2.0], "target": [0.3, 0, 0.45]},
]
ARM_VIEW, EE_VIEW = (-40, 18), (-32, 12)          # azimuth, elevation in degrees

# name: (export dir, roles to keep, view)
ASSETS = {f"arm_{a}": (f"{a}__robotiq", ["arm"], ARM_VIEW)
          for a in ("franka", "franka_fr3", "gen3", "kuka", "link6", "lite6", "sawyer", "ur5", "ur10", "z1")}
ASSETS.update({f"robot_{r}": (f"{r}__none", ["arm", "hand", "mount"], ARM_VIEW)
               for r in ("aloha_tactile", "gen3_lite", "so_100", "trossen_vx300s", "trossen_wx250s", "franka_with_gripper")})
ASSETS.update({f"ee_{g}": (f"franka__{g}", ["hand"], EE_VIEW)
               for g in ("robotiq", "franka_umi_tacticle", "barrett", "dclaw", "inspire", "ability", "schunk",
                         "allegro", "leap", "sharpa", "shadow")})


def centre(scene, roles):
    sc = json.load(open(scene))
    p = np.array([np.array(m["frames"][0])[:3, 3] for m in sc["meshes"] if m["role"] in roles])
    return (p.min(0) + p.max(0)) / 2, float(np.linalg.norm(p.max(0) - p.min(0)))


def shot(scene, roles, cam, out, res, samples):
    s = {"scene": str(scene), "out": str(out), "res": [res, res], "samples": samples, "camera": cam,
         "hide_roles": ["floor", "table"], "only_roles": roles, "shadow_catcher": False, "overwrite": True,
         "lights": LIGHTS, "materials": {"hand": GRAPHITE, "mount": GRAPHITE}}
    p = Path(out) / "shot.json"
    Path(out).mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(s, indent=1))
    return p


def render(p, gpu, log):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu))
    with open(log, "w") as f:
        subprocess.run([BLENDER_PY, str(RENDER), str(p)], env=env, stdout=f, stderr=subprocess.STDOUT, check=True)


def one(name, gpu):
    exp, roles, (az, el) = ASSETS[name]
    scene = next(d / exp / "scene.json" for d in ROBOTS if (d / exp / "scene.json").exists())
    c, ext = centre(scene, roles)
    a, e = math.radians(az), math.radians(el)
    d = np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)])
    loc = c + d * max(0.6, 2.4 * ext)
    cam = {"loc": loc.round(4).tolist(), "target": c.round(4).tolist(), "lens": 30}
    w = WORK / name
    # pass 1: wide and coarse, to find the ink box
    render(shot(scene, roles, cam, w / "p1", 384, 6), gpu, w / "p1.log")
    im = Image.open(next((w / "p1").glob("f*.png")))
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb is None:
        raise RuntimeError(f"{name}: nothing rendered")
    W = im.width
    u0, v0, u1, v1 = (x / W for x in bb)
    cu, cv, half = (u0 + u1) / 2, (v0 + v1) / 2, max(u1 - u0, v1 - v0) / 2
    m = 0.86 / (2 * half)                                    # magnification: the asset fills 86 % of the frame
    cam2 = dict(cam, lens=round(cam["lens"] * m, 3), shift_x=round(m * (cu - 0.5), 4), shift_y=round(-m * (cv - 0.5), 4))
    # pass 2: final
    render(shot(scene, roles, cam2, w / "p2", 1200, 128), gpu, w / "p2.log")
    OUT.mkdir(parents=True, exist_ok=True)
    fin = Image.open(next((w / "p2").glob("f*.png"))).convert("RGBA").resize((900, 900), Image.LANCZOS)
    fin.save(OUT / f"{name}.webp", "WEBP", quality=90, alpha_quality=95, method=5)
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--gpu", default="0")
    a = ap.parse_args()
    names = a.only or list(ASSETS)
    for n in names:
        try:
            print("ok", one(n, a.gpu), flush=True)
        except Exception as ex:  # keep going, report at the end
            print("FAILED", n, ex, flush=True)


if __name__ == "__main__":
    main()
