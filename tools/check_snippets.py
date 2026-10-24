#!/usr/bin/env python
"""Check the claims the concept and how-to pages make, against the real API. Prints one line per check.

    CUDA_VISIBLE_DEVICES=0 PYOPENGL_PLATFORM=egl .venv-dexsuite/bin/python tools/check_snippets.py
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, "/efs/projects/fudi/simulation/Dexsuite")
os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
import torch  # noqa: E402

import dexsuite as ds  # noqa: E402

DOCS = Path(__file__).resolve().parents[1] / "docs/source"
results = []


def check(name):
    def deco(f):
        try:
            out = f()
            results.append(("ok", name, out))
            print("ok  ", name, "|", out, flush=True)
        except Exception as e:  # noqa: BLE001
            results.append(("FAIL", name, repr(e)))
            print("FAIL", name, "|", traceback.format_exc()[-500:], flush=True)
        return f
    return deco


@check("exports")
def _():
    names = ["RobotOptions", "ArmOptions", "ControllerOptions", "SimOptions", "CamerasOptions", "StaticCamOptions",
             "DynamicCamOptions", "LayoutOptions", "PoseOptions", "AABBOptions", "set_device", "get_device", "make"]
    missing = [n for n in names if not hasattr(ds, n)]
    assert not missing, missing
    return "all exported"


@check("single env shapes, reach franka+robotiq (installation page)")
def _():
    env = ds.make("reach", manipulator="franka", gripper="robotiq")
    obs, info = env.reset(seed=0)
    a = env.action_space
    obs2, r, te, tr, info = env.step(a.sample())
    out = dict(action=tuple(a.shape), low=float(a.low.min()), high=float(a.high.max()), grip_keys=list(obs["state"]["gripper"]),
               manip_keys=list(obs["state"]["manipulator"]), tcp=tuple(obs["state"]["gripper"]["tcp_pos"].shape),
               reward=tuple(r.shape), terminated=tuple(te.shape), truncated=tuple(tr.shape), success=tuple(info["success"].shape),
               cams=sorted(obs["cameras"]), rgb=tuple(obs["cameras"]["front"]["rgb"].shape), rgb_dtype=str(obs["cameras"]["front"]["rgb"].dtype),
               ep=info["episode"])
    fr = env.render("rgb_array")
    out["render_rgb_array"] = type(fr).__name__
    out["render_default"] = repr(env.render()) if env.render_mode != "human" else "human"
    out["aabbs"] = sorted(env.get_workspace_aabbs())
    segs = [(s.name, s.start, s.stop, s.ctrl) for s in env.robot._layout.segments]
    out["segments"] = segs
    env.close()
    return out


@check("batched shapes, lift n_envs=4, reset_env_idx")
def _():
    env = ds.make("lift", manipulator="franka", gripper="robotiq", n_envs=4, cameras=None)
    obs, info = env.reset(seed=0)
    act = torch.zeros(4, env.action_space.shape[0])
    obs, r, te, tr, info = env.step(act)
    one = env.step(torch.zeros(env.action_space.shape[0]))
    env.reset_env_idx([0, 2], seed=1)
    out = dict(reward=tuple(r.shape), terminated=tuple(te.shape), tcp=tuple(obs["state"]["gripper"]["tcp_pos"].shape),
               cams=sorted(obs.get("cameras", {})), needs_reset=tuple(info["needs_reset"].shape), broadcast=tuple(one[1].shape))
    env.close()
    return out


@check("allegro action space (quickstart)")
def _():
    env = ds.make("lift", manipulator="franka", gripper="allegro", cameras=None)
    s = repr(env.action_space)
    env.close()
    return s


@check("custom cameras: res=(320,240), depth, segmentation")
def _():
    cams = ds.CamerasOptions(
        static={"side": ds.StaticCamOptions(pos=(0.5, -1.0, 0.6), lookat=(0.5, 0.0, 0.1), fov=50, res=(320, 240))},
        dynamic={"wrist": ds.DynamicCamOptions(pos_offset=(0.0, 0.05, 0.02), fov=70)},
        modalities=("rgb", "depth", "segmentation"))
    env = ds.make("lift", manipulator="franka", gripper="robotiq", cameras=cams)
    obs, _ = env.reset(seed=0)
    c = obs["cameras"]
    out = {k: {m: (tuple(v.shape), str(v.dtype)) for m, v in c[k].items()} for k in c}
    env.close()
    return out


@check("camera names + modalities, direct form")
def _():
    env = ds.make("lift", manipulator="franka", gripper="robotiq", cameras=["front", "overhead", "wrist"], modalities=["rgb", "depth"])
    obs, _ = env.reset(seed=0)
    out = {k: sorted(v) for k, v in obs["cameras"].items()}
    env.close()
    return out


@check("tactile pads, franka_umi_tacticle")
def _():
    env = ds.make("pick_place", manipulator="franka", gripper="franka_umi_tacticle", cameras=None)
    obs, _ = env.reset(seed=0)
    tac = obs["state"]["gripper"]["tactile"]
    pad = tac["left_elastomer"]
    out = dict(top=sorted(tac), pad={k: tuple(v.shape) for k, v in pad.items()})
    env.close()
    return out


@check("controllers via options (actions page)")
def _():
    robot = ds.RobotOptions(single=ds.ArmOptions(
        manipulator="franka", gripper="allegro",
        manipulator_controller=ds.ControllerOptions(name="osc_pose", config={"lin_scale": 0.4, "ang_scale": 0.08}),
        gripper_controller=ds.ControllerOptions(name="joint_position", config={"normalized": False})))
    env = ds.make("lift", robot=robot, cameras=None)
    env.reset(seed=0)
    out = repr(env.action_space)
    env.close()
    return out


@check("workspace override (workspaces page)")
def _():
    arm = ds.ArmOptions(manipulator="franka", gripper="robotiq", workspace=ds.AABBOptions(min=(0.2, -0.4, 0.0), max=(0.6, 0.4, 0.5)))
    env = ds.make("lift", robot=ds.RobotOptions(single=arm), cameras=None)
    env.reset(seed=0)
    out = {k: v for k, v in env.get_workspace_aabbs().items() if v is not None}
    env.close()
    return str(out)[:200]


@check("bimanual face_to_face layout + per-side state")
def _():
    env = ds.make("bimanual_reach", manipulator=("franka", "franka"), gripper="robotiq", layout="face_to_face", cameras=None)
    obs, _ = env.reset(seed=0)
    out = dict(state=sorted(obs["state"]), aabbs=sorted(env.get_workspace_aabbs()), action=tuple(env.action_space.shape))
    env.close()
    return out


@check("bimanual explicit poses (workspaces page)")
def _():
    layout = ds.LayoutOptions(left=ds.PoseOptions(pos=(0.0, 0.4, 0.0), yaw_rad=0.0), right=ds.PoseOptions(pos=(0.0, -0.4, 0.0), yaw_rad=0.0))
    robot = ds.RobotOptions(type_of_robot="bimanual", left=ds.ArmOptions(manipulator="ur5", gripper="robotiq"),
                            right=ds.ArmOptions(manipulator="ur5", gripper="robotiq"), layout=layout)
    env = ds.make("bimanual_reach", robot=robot, cameras=None)
    env.reset(seed=0)
    env.close()
    return "built"


@check("how-to: Tap Cube, exactly as written")
def _():
    md = (DOCS / "how-to/new-task.md").read_text()
    code = re.search(r'Create `dexsuite/environments/single/rigid/tap_cube.py`:\n\n```python\n(.*?)```', md, re.S).group(1)
    d = Path(tempfile.mkdtemp())
    (d / "tap_cube_doc.py").write_text(code)
    sys.path.insert(0, str(d))
    import tap_cube_doc  # noqa: F401  registers "tap_cube"
    env = ds.make("tap_cube", manipulator="franka", gripper="robotiq", cameras=None)
    obs, info = env.reset(seed=0)
    obs, r, te, tr, info = env.step(env.action_space.sample())
    out = dict(cube_top=tuple(obs["state"]["other"]["cube_top"].shape), reward=float(r), success=bool(info["success"]))
    env.close()
    return out


@check("integrated robot and floating wrist (robots page)")
def _():
    e1 = ds.make("lift", manipulator="trossen_vx300s", cameras=None); a1 = tuple(e1.action_space.shape); e1.close()
    e2 = ds.make("lift", manipulator="so_100", cameras=None); a2 = tuple(e2.action_space.shape); e2.close()
    e3 = ds.make("lift", manipulator="ur5", gripper="leap", cameras=None); a3 = tuple(e3.action_space.shape); e3.close()
    return dict(trossen=a1, so_100=a2, ur5_leap=a3)


if __name__ == "__main__":
    print("\nSUMMARY", sum(r[0] == "ok" for r in results), "ok,", sum(r[0] == "FAIL" for r in results), "failed")
