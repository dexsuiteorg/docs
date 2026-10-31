#!/usr/bin/env python
"""Run every task page's snippet for real and record what it returns.

For each documented task: ds.make with the documented robot (exactly the call on the page), reset(seed=0), one step
with a random action. Records the action size, the task's extra observation keys and shapes, and the camera names.
build_catalog.py reads the result into the task pages; a task that fails here fails the docs build check.

    CUDA_VISIBLE_DEVICES=0 PYOPENGL_PLATFORM=egl .venv-dexsuite/bin/python tools/check_tasks.py [keys...]
writes tools/task_facts.json (merged with existing entries).
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import DEXSUITE  # noqa: E402

sys.path.insert(0, str(DEXSUITE))
os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
from catalog_data import TASKS  # noqa: E402

OUT = Path(__file__).parent / "task_facts.json"


def shape(x):
    return list(x.shape) if hasattr(x, "shape") else None


def run(t):
    import dexsuite as ds
    r = t["robot"].split(":")
    if r[0] == "bimanual":
        env = ds.make(t["key"], manipulator=(r[1], r[1]), gripper=(r[2], r[3]))
    else:
        env = ds.make(t["key"], manipulator=r[0], gripper=r[1])
    obs, info = env.reset(seed=0)
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    other = {k: shape(v) for k, v in obs["state"]["other"].items() if k not in ("action", "last_action")}
    cams = {k: sorted(v) for k, v in obs.get("cameras", {}).items()}
    fact = {"action_dim": int(env.action_space.shape[0]), "other": other, "cameras": cams,
            "info": sorted(k for k in info), "reward_shape": shape(reward)}
    env.close()
    return fact


def main():
    keys = sys.argv[1:]
    facts = json.loads(OUT.read_text()) if OUT.exists() else {}
    for t in TASKS:
        if keys and t["key"] not in keys:
            continue
        try:
            facts[t["key"]] = run(t)
            print("ok", t["key"], facts[t["key"]]["action_dim"], list(facts[t["key"]]["other"]), flush=True)
        except Exception:
            facts[t["key"]] = {"error": traceback.format_exc()[-600:]}
            print("FAILED", t["key"], traceback.format_exc()[-300:], flush=True)
        OUT.write_text(json.dumps(facts, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
