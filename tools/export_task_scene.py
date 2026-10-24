#!/usr/bin/env python
"""Export a task at reset (robot + every task object) for the docs renders.

    CUDA_VISIBLE_DEVICES=0 .venv-dexsuite/bin/python tools/export_task_scene.py --task lift --robot franka:allegro --out DIR
    ... --robot floating:sharpa_fardexbot      (hand-only tasks)
    ... --robot bimanual:franka:allegro_left:allegro_right   (two arms, side-by-side layout)

Writes DIR/scene.json + DIR/meshes/*.glb in the format the website renderer reads (render_replay.py): one frame,
roles arm / hand / mount / object:<attribute> / prop:<asset> / table / floor.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/efs/projects/fudi/simulation/Dexsuite")
os.environ.setdefault("PYOPENGL_PLATFORM", "egl")


def quat_to_R(q):  # wxyz
    w, x, y, z = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def T_of(pos, quat):
    T = np.eye(4)
    T[:3, :3] = quat_to_R(np.asarray(quat, float).reshape(-1)[:4])
    T[:3, 3] = np.asarray(pos, float).reshape(-1)[:3]
    return T


def to_np(x):
    return x.detach().cpu().numpy() if hasattr(x, "detach") else np.asarray(x)


def make_env(task, robot, seed):
    import dexsuite as ds
    cams = ds.CamerasOptions(static={}, dynamic={}, modalities=("rgb",))
    sim = ds.SimOptions(n_envs=1)
    parts = robot.split(":")
    if parts[0] == "bimanual":                       # bimanual:<arm>:<left gripper>:<right gripper>
        arm, gl, gr = parts[1], parts[2], parts[3] if len(parts) > 3 else parts[2]
        robot = ds.RobotOptions(type_of_robot="bimanual", left=ds.ArmOptions(manipulator=arm, gripper=gl),
                                right=ds.ArmOptions(manipulator=arm, gripper=gr))
        env = ds.make(task, robot=robot, sim=sim, cameras=cams, render_mode=None)
    else:
        arm, grip = parts[0], (None if parts[1] == "none" else parts[1])
        env = ds.make(task, robot=ds.RobotOptions(single=ds.ArmOptions(manipulator=arm, gripper=grip)),
                      sim=sim, cameras=cams, render_mode=None)
    env.reset(seed=seed)
    return env


def robot_parts(robot):
    """(entity uid -> role) for every arm / hand entity of a single or bimanual robot."""
    out = {}
    for side in (robot, getattr(robot, "single", None), getattr(robot, "left", None), getattr(robot, "right", None)):
        if side is None:
            continue
        a, h = getattr(side, "arm_ent", None), getattr(side, "hand_ent", None)
        if a is not None:
            out.setdefault(a.uid, "arm")
        if h is not None and h is not a:
            out.setdefault(h.uid, "hand")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--robot", default="franka:allegro")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    (out / "meshes").mkdir(parents=True, exist_ok=True)
    env = make_env(a.task, a.robot, a.seed)
    u = env.unwrapped
    parts = robot_parts(env.robot)
    attr_of = {}
    for name in dir(u):
        if name.startswith("_"):
            continue
        try:
            v = getattr(u, name)
        except Exception:
            continue
        if hasattr(v, "links") and hasattr(v, "uid"):
            attr_of.setdefault(v.uid, name)
    canvas = getattr(u, "canvas", None)
    if canvas is not None and getattr(canvas, "entity", None) is not None:
        attr_of[canvas.entity.uid] = "paper"

    def role(e):
        if e.uid in parts:
            return parts[e.uid]
        nm = getattr(e, "name", "") or ""
        if "plane" in nm.lower():
            return "floor"
        if "table" in nm.lower() or "vention" in nm.lower():
            return "table"
        if e.uid in attr_of:
            return "object:" + attr_of[e.uid]
        fname = str(getattr(getattr(e, "morph", None), "file", "") or "")
        return "prop:" + (Path(fname).stem if fname else (nm or "entity"))

    meshes = []
    for e in env.scene.entities:
        if not hasattr(e, "links"):
            continue
        r = role(e)
        if r == "floor":
            continue
        for link in e.links:
            for k, vg in enumerate(link.vgeoms):
                tm = vg.vmesh.trimesh.copy()
                nm = f"{r.replace(':', '_')}__{link.name}__{k}".replace("/", "_").replace(" ", "_")
                path = out / "meshes" / f"{len(meshes):03d}_{nm}.glb"
                try:
                    tm.export(path)
                except Exception:
                    tm.visual = tm.visual.to_color()
                    tm.export(path)
                col = None
                try:
                    c = getattr(vg.surface, "color", None)
                    col = None if c is None else [float(x) for x in np.asarray(c).reshape(-1)[:3]]
                except Exception:
                    pass
                Tl = T_of(to_np(link.get_pos()).reshape(-1)[:3], to_np(link.get_quat()).reshape(-1)[:4])
                Tg = Tl @ T_of(to_np(vg.init_pos), to_np(vg.init_quat))
                meshes.append({"name": nm, "glb": str(path.relative_to(out)), "role": r, "link": link.name,
                               "entity": getattr(e, "name", ""), "color": col, "frames": [np.round(Tg, 6).tolist()]})
    pts = np.array([np.array(m["frames"][0])[:3, 3] for m in meshes if m["role"] != "table"])
    table_z = None
    tz = [np.array(m["frames"][0])[2, 3] for m in meshes if m["role"] == "table"]
    if tz:
        table_z = float(max(tz))
    (out / "scene.json").write_text(json.dumps({"task": a.task, "robot": a.robot, "frames": [0], "fps": 20,
                                                "bounds": [pts.min(0).tolist(), pts.max(0).tolist()],
                                                "table_z": table_z, "meshes": meshes}))
    roles = sorted({m["role"] for m in meshes})
    print(f"ok {a.task} {a.robot}: {len(meshes)} meshes, roles {roles}", flush=True)
    env.close()


if __name__ == "__main__":
    main()
