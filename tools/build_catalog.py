#!/usr/bin/env python
"""Generate the task and robot catalog pages from tools/catalog_data.py.

    python3 tools/build_catalog.py

Writes docs/source/tasks/{index,<key>}.md and docs/source/robots/{index,arms,end-effectors,compatibility}.md.
Benchmark results are read from the paper's Table II source (PAPER_TABLE) when it is available, so the numbers on
the task pages are the published ones; without it the result tables are left out.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from catalog_data import ADAPTERS, ARMS, END_EFFECTORS, FLOATING, IN_PROGRESS, INTEGRATED, TASKS  # noqa: E402

SRC = Path(__file__).resolve().parents[1] / "docs/source"
FACTS = Path(__file__).parent / "task_facts.json"          # tools/check_tasks.py: what each snippet really returns
PAPER_TABLE = Path("/efs/projects/fudi/test_stuff/paper_ol/Dexsuite/imitation_results.tex")
GROUPS = {"track1": ("Benchmark, Track 1", "Cross-embodiment: run with the parallel-jaw gripper and the Allegro hand."),
          "track2": ("Benchmark, Track 2", "Dexterous capability: hand-only tasks."),
          "single": ("More single-arm tasks", "Further tasks with a success check, outside the benchmark."),
          "bimanual": ("Bimanual tasks", "Two arms, side by side by default.")}
PHYS = {"rigid": "rigid", "articulated": "articulated", "articulated + paint": "articulated + paint"}
esc = lambda s: html.escape(s, quote=True)  # noqa: E731


# ---------------------------------------------------------------------------------------------- benchmark results
def table_ii():
    """{task name: {embodiment: [(model, mean, std, bold)]}} from Table II, or {} if the paper is not here."""
    if not PAPER_TABLE.exists():
        return {}
    tex = PAPER_TABLE.read_text()
    out = {}
    blocks = re.findall(r"\\begin\{tabular\*\}.*?\\end\{tabular\*\}", tex, re.S)
    embs = [["Parallel-jaw gripper"] * 5 + ["Allegro hand"] * 3, ["Allegro hand"] * 6 + ["Sharpa hand"] * 2]
    for bi, block in enumerate(blocks):
        lines = [l.strip() for l in block.splitlines()]
        head = next(l for l in lines if l.startswith("\\textbf{Model"))
        tasks = [re.sub(r"\\textbf\{(.*?)\}", r"\1", t).replace("\\&", "&").strip() for t in re.split(r"(?<!\\)&", head.rstrip("\\"))[1:]]
        for l in lines:
            m = re.match(r"((?:BC-G|BC-GMM|BC-T|Diffusion|ACT) \((?:state|image)\))", l)
            if not m:
                continue
            for j, c in enumerate(l.rstrip("\\").split("&")[1:]):
                v = float(re.search(r"\$\s*(?:\\bm\{)?(\d+(?:\.\d+)?)", c).group(1))
                sd = float(re.search(r"\\pm\\,\s*(\d+(?:\.\d+)?)", c).group(1))
                out.setdefault(tasks[j], {}).setdefault(embs[bi][j], []).append((m.group(1), v, sd, "\\bm{" in c))
    return out


def results_md(name, res):
    if name not in res:
        return ""
    embs = list(res[name])
    models = [m for m, *_ in res[name][embs[0]]]
    fmt = lambda v: f"{v:g}"  # noqa: E731
    rows = []
    for k, mdl in enumerate(models):
        cells = []
        for e in embs:
            _, v, sd, b = res[name][e][k]
            cells.append(f"**{fmt(v)}** ± {fmt(sd)}" if b else f"{fmt(v)} ± {fmt(sd)}")
        rows.append(f"| {mdl} | " + " | ".join(cells) + " |")
    head = "| Baseline | " + " | ".join(embs) + " |\n|---|" + "---|" * len(embs)
    return ("\n## Baseline results\n\nSuccess rate (%) from the DexSuite benchmark: mean ± standard deviation over three "
            "evaluation seeds with 50 episodes each. Bold is the best result within each input type. See "
            "[the benchmark](../data/benchmark.md) for the protocol.\n\n" + head + "\n" + "\n".join(rows) + "\n")


# ---------------------------------------------------------------------------------------------- task pages
def make_call(t):
    r = t["robot"].split(":")
    if r[0] == "bimanual":
        return f'env = ds.make(\n    "{t["key"]}",\n    manipulator=("{r[1]}", "{r[1]}"),\n    gripper=("{r[2]}", "{r[3]}"),\n)'
    return f'env = ds.make("{t["key"]}", manipulator="{r[0]}", gripper="{r[1]}")'


def robot_text(t):
    r = t["robot"].split(":")
    if r[0] == "bimanual":
        return f"two Franka arms with left and right Allegro hands"
    if r[0] == "floating":
        return "the Sharpa hand on a floating wrist"
    ee = next((e["name"] for e in END_EFFECTORS if e["key"] == r[1]), r[1])
    return f"a Franka with the {ee}"


def chips(t):
    g = {"track1": "Track 1 benchmark", "track2": "Track 2 benchmark", "single": "single arm", "bimanual": "bimanual"}[t["group"]]
    out = [f'<span class="ds-chip blue">{g}</span>', f'<span class="ds-chip">{esc(PHYS.get(t["physics"], t["physics"]))}</span>']
    if t["group"] in ("track1", "track2"):
        out.append('<span class="ds-chip">dataset on Hugging Face</span>')
    return "".join(out)


def clip_html(t):
    clips = t.get("clips", ())
    if not clips:
        return ""
    if len(clips) == 2:
        cap = ("UMI gripper" if t["key"] != "reach" else "Robotiq 2F-85", "Allegro hand")
        speed = ", 2× speed" if t["key"] == "stack" else ""
        figs = "".join(f'<figure><video class="ds-video" src="../_static/clips/{c}.mp4" poster="../_static/clips/{c}.jpg" '
                       f'muted loop playsinline preload="none"></video><figcaption>{cap[i]}, recorded human demonstration{speed}'
                       f'</figcaption></figure>' for i, c in enumerate(clips))
        return f'\n<div class="ds-duo">{figs}</div>\n'
    c = clips[0]
    return (f'\n<figure><video class="ds-video" src="../_static/clips/{c}.mp4" poster="../_static/clips/{c}.jpg" '
            f'muted loop playsinline preload="none"></video><figcaption>A recorded demonstration from the dataset, '
            f'replayed and rendered in Blender.</figcaption></figure>\n')


def obs_md(t):
    import json
    facts = json.loads(FACTS.read_text()).get(t["key"], {}) if FACTS.exists() else {}
    other = facts.get("other")
    if not other:
        return ""
    shape = lambda v: "(" + ", ".join(str(x) for x in v) + ("," if len(v) == 1 else "") + ")" if v is not None else "scalar"  # noqa: E731
    rows = "\n".join(f"| `{k}` | {shape(v)} |" for k, v in other.items())
    return (f"\n## Observations\n\nWhat the task adds under `obs[\"state\"][\"other\"]`, next to the robot state and "
            f"the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.\n\n| Key | Shape |\n|---|---|\n{rows}\n")


def task_page(t, res):
    import json
    facts = json.loads(FACTS.read_text()).get(t["key"], {}) if FACTS.exists() else {}
    spec = [("Task key", f"<code>{t['key']}</code>"), ("Horizon", f"{t['horizon']:,} control steps ({t['horizon'] / 20:g} s at 20 Hz)"),
            ("Objects", esc(", ".join(t["objects"]))), ("Success", esc(t["success"])), ("Failure", esc(t["failure"]))]
    if t.get("random"):
        spec.append(("Randomized at reset", esc(t["random"])))
    spec.append(("Shown with", esc(robot_text(t))))
    if facts.get("action_dim"):
        spec.append(("Action size", f"{facts['action_dim']} with the robot shown"))
    spec.append(("Source", f"<code>{t['file']}</code>"))
    dl = "\n".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in spec)
    order = "\n".join(f"{i}. {s}" for i, s in enumerate(t["order"], 1))
    notes = "".join(f"\n```{{note}}\n{n}\n```\n" for n in t.get("notes", []))
    return f"""---
myst:
  html_meta:
    description: "{esc(t['name'])}: {esc(t['goal'])}"
---

# {t['name']}

{chips(t)}

<p class="ds-lede">{esc(t['goal'])}</p>

<img class="ds-render" src="../_static/tasks/{t['key']}.webp" alt="{esc(t['name'])} at reset, rendered in Blender">
{clip_html(t)}
## At a glance

<dl class="ds-spec">
{dl}
</dl>

## Order of interactions

{order}

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.

{obs_md(t)}
## Run it

```python
import dexsuite as ds

{make_call(t)}
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
{notes}{results_md(t['name'], res) if t['group'] in ('track1', 'track2') else ''}"""


def tile(t):
    return (f'<a class="ds-tile" href="{t["key"]}.html"><img src="../_static/tasks/{t["key"]}.webp" alt="{esc(t["name"])}" loading="lazy">'
            f'<div class="ds-tile-text"><b>{esc(t["name"])}</b><small><code>{t["key"]}</code></small></div></a>')


def tasks_index():
    parts = ["""# Tasks

<p class="ds-lede">Every task is one class with its own reset, observations and success check, and runs with any arm and
end-effector that fits it. These are the tasks that build and report success today, rendered at reset.</p>

Pick a task by its key: `ds.make("<key>", manipulator=..., gripper=...)`. Eleven of them form the
[DexSuite benchmark](../data/benchmark.md), and their demonstrations are on
[Hugging Face](https://huggingface.co/dexsuite).
"""]
    for g, (title, sub) in GROUPS.items():
        ts = [t for t in TASKS if t["group"] == g]
        parts.append(f'\n## {title}\n\n{sub}\n\n<div class="ds-grid wide">\n' + "\n".join(tile(t) for t in ts) + "\n</div>\n")
    rows = "\n".join(f"| `{k}` | {d} | {why} |" for k, d, why in IN_PROGRESS)
    parts.append(f"""
## In progress

These tasks are registered but cannot be used from `ds.make` yet. They are listed so nobody is surprised by them.

| Key | What it is | What is missing |
|---|---|---|
{rows}

```{{toctree}}
:hidden:
:maxdepth: 1

""" + "\n".join(t["key"] for t in TASKS) + "\n```\n")
    return "".join(parts)


# ---------------------------------------------------------------------------------------------- robot pages
def robot_tile(img, name, sub, href):
    return (f'<a class="ds-tile" href="{href}"><img src="../_static/catalog/{img}.webp" alt="{esc(name)}" loading="lazy">'
            f'<div class="ds-tile-text"><b>{esc(name)}</b><small>{esc(sub)}</small></div></a>')


def robots_index():
    arms = "\n".join(robot_tile(f"arm_{a['key']}", a["name"], f"{a['dof']} DoF arm", f"arms.html#{a['key']}") for a in ARMS if a["key"] != "franka_fr3")
    integ = "\n".join(robot_tile(f"robot_{r['key']}", r["name"], f"{r['dof']} DoF", f"arms.html#{r['key']}") for r in INTEGRATED)
    ees = "\n".join(robot_tile(f"ee_{e['key']}", e["name"], f"{e['kind']}, {e['dof']} DoF", f"end-effectors.html#{e['key']}") for e in END_EFFECTORS)
    return f"""# Robots

<p class="ds-lede">A robot in DexSuite is an arm and an end-effector, chosen by name when the environment is made.
Modular arms take any end-effector with an adapter for them, integrated robots come with their own gripper, and the
floating wrist carries a hand on its own.</p>

```python
# a modular arm with a hand
env = ds.make("lift", manipulator="ur5", gripper="allegro")

# an integrated robot, with its built-in gripper
env = ds.make("lift", manipulator="so_100")

# a hand on its own, on the floating wrist
env = ds.make("put_bread_toaster", manipulator="floating", gripper="sharpa_fardexbot")
```

How the parts are joined is described in [Robots](../concepts/robots.md). Which pairs are available is in the
[compatibility table](compatibility.md).

## Arms

<div class="ds-grid">
{arms}
</div>

## Integrated robots

<div class="ds-grid">
{integ}
</div>

## End-effectors

<div class="ds-grid">
{ees}
</div>

```{{toctree}}
:hidden:
:maxdepth: 1

arms
end-effectors
compatibility
```
"""


def arms_page():
    parts = ["""# Arms

<p class="ds-lede">Ten modular arms, six integrated robots and a floating wrist. Every arm has a workspace box in
<code>dexsuite/config/workspaces.yaml</code> and starts each episode at a fixed home pose.</p>

## Modular arms
"""]
    for a in ARMS:
        ees = ADAPTERS.get(a["key"], [])
        mounts = ", ".join(f"`{k}`" for k in ees) if ees else "none yet"
        img = (f'<img class="ds-render" style="max-width:360px" src="../_static/catalog/arm_{a["key"]}.webp" alt="{esc(a["name"])}">'
               if a["key"] != "franka_fr3" else "")
        note = ""
        if a.get("note"):
            note = f"\n```{{warning}}\n{a['note']}\n```\n"
        elif a.get("mount_issue"):
            note = ("\n```{warning}\nThe adapters for this arm currently mount end-effectors at the wrong angle. "
                    "Use the Franka, Gen3, UR5e or UR10e until the adapter files are fixed.\n```\n")
        parts.append(f"""
({a['key']})=
### {a['name']}

{img}

<dl class="ds-spec">
<dt>Key</dt><dd><code>{a['key']}</code></dd>
<dt>Maker</dt><dd>{esc(a['maker'])}</dd>
<dt>Degrees of freedom</dt><dd>{a['dof']}</dd>
<dt>Model</dt><dd><code>{a['asset']}</code>, license {esc(a['license'])}</dd>
<dt>End-effectors</dt><dd>{mounts}</dd>
</dl>
{note}""")
    parts.append("\n## Integrated robots\n\nThese come with their own gripper, so `gripper` is not passed. The gripper "
                 "joints appear in `obs[\"state\"][\"gripper\"]` like any other end-effector.\n")
    for r in INTEGRATED:
        tac = "\n<dt>Tactile</dt><dd>pads on both fingers, see <a href=\"../concepts/observations.html#tactile-pads\">tactile</a></dd>" if r.get("tactile") else ""
        parts.append(f"""
({r['key']})=
### {r['name']}

<img class="ds-render" style="max-width:360px" src="../_static/catalog/robot_{r['key']}.webp" alt="{esc(r['name'])}">

<dl class="ds-spec">
<dt>Key</dt><dd><code>{r['key']}</code></dd>
<dt>Degrees of freedom</dt><dd>{r['dof']} (arm + gripper)</dd>
<dt>Gripper</dt><dd>{esc(r['gripper'])}</dd>{tac}
</dl>
""")
    f = FLOATING
    parts.append(f"""
## Floating wrist

({f['key']})=
### {f['name']}

{f['text']}

<dl class="ds-spec">
<dt>Key</dt><dd><code>{f['key']}</code></dd>
<dt>Degrees of freedom</dt><dd>{f['dof']}</dd>
<dt>End-effectors</dt><dd>{", ".join(f"<code>{k}</code>" for k in f['mounts'])}</dd>
</dl>
""")
    return "".join(parts)


def ee_page():
    parts = ["""# End-effectors

<p class="ds-lede">Twelve end-effectors, from parallel-jaw grippers to a 24-joint hand. Every one is controlled per
joint, so the gripper part of the action has one entry per actuated degree of freedom.</p>
"""]
    for e in END_EFFECTORS:
        arms = [a for a, ks in ADAPTERS.items() if e["key"] in ks]
        var = f"\n<dt>Variants</dt><dd>{', '.join(f'<code>{v}</code>' for v in e['variants'])}</dd>" if e.get("variants") else ""
        tac = "\n<dt>Tactile</dt><dd>pads on both fingers</dd>" if e.get("tactile") else ""
        parts.append(f"""
({e['key']})=
## {e['name']}

<img class="ds-render" style="max-width:340px" src="../_static/catalog/ee_{e['key']}.webp" alt="{esc(e['name'])}">

<dl class="ds-spec">
<dt>Key</dt><dd><code>{e['key']}</code></dd>
<dt>Type</dt><dd>{esc(e['kind'])}</dd>
<dt>Actuated DoF</dt><dd>{e['dof']}</dd>
<dt>Fingers</dt><dd>{e['fingers']}</dd>{var}{tac}
<dt>Mounts on</dt><dd>{", ".join(f"<code>{a}</code>" for a in arms)}</dd>
<dt>Model license</dt><dd>{esc(e['license'])}</dd>
</dl>
""")
    return "".join(parts)


def compat_page():
    cols = [e["key"] for e in END_EFFECTORS]
    head = "| Arm | " + " | ".join(f"`{c}`" for c in cols) + " |\n|---|" + "---|" * len(cols)
    rows = []
    issue = {a["key"] for a in ARMS if a.get("mount_issue")}
    for a in [x["key"] for x in ARMS] + ["floating"]:
        ks = ADAPTERS.get(a, [])
        mark = lambda c: ("⚠" if a in issue else "✓") if c in ks else ""  # noqa: E731
        rows.append(f"| `{a}` | " + " | ".join(mark(c) for c in cols) + " |")
    return f"""# Compatibility

<p class="ds-lede">Which end-effector mounts on which arm. A pair is available when the arm's adapter file has an entry
for the end-effector.</p>

✓ available, ⚠ available but the adapter mounts it at the wrong angle today, empty: no adapter.

{head}
{chr(10).join(rows)}

Adapters live next to each arm in `dexsuite/models/manipulators/<arm>/<arm>_adapters.yaml`. Each entry places an
optional mount piece and the end-effector relative to the arm's last link; [Add an end-effector](../how-to/new-end-effector.md)
shows the format. Asking for a pair without an entry raises `ValueError: Adapter missing`.

Integrated robots (`franka_with_gripper`, `aloha_tactile`, `gen3_lite`, `so_100`, `trossen_vx300s`,
`trossen_wx250s`) always use their own gripper.
"""


MANIFEST = Path("/efs/projects/fudi/dexsuite_website/static/data_viewer/manifest.json")
TIERS = ["Human teleoperation", "Scripted expert", "Machine-generated"]


def datasets_partial():
    """Benchmark datasets by task and embodiment, linked to Hugging Face (from the data viewer manifest)."""
    import json
    sets = json.load(open(MANIFEST))["sets"]
    name = {t["key"]: t["name"] for t in TASKS}
    rows, seen = [], []
    for s in sets:
        k = (s["task"], s["embodiment"])
        if k not in seen:
            seen.append(k)
    for task, emb in seen:
        cells = []
        for tier in TIERS:
            m = [x for x in sets if (x["task"], x["embodiment"], x["tier"]) == (task, emb, tier)]
            if not m:
                cells.append("")
            elif m[0].get("hf"):
                cells.append(f"[`{m[0]['hf'].split('/')[1]}`](https://huggingface.co/datasets/{m[0]['hf']})")
            else:
                cells.append("coming soon")
        rows.append(f"| [{name.get(task, task)}](../tasks/{task}.md) | {emb} | " + " | ".join(cells) + " |")
    return "| Task | Embodiment | Human teleoperation | Scripted expert | Machine-generated |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n"


def results_partial(res):
    """Table II as one markdown table: one row per task-embodiment pair, one column per baseline."""
    if not res:
        return "The results table is generated from the paper source, which was not available for this build.\n"
    order = [(t["name"], e) for t in TASKS if t["group"] in ("track1", "track2") for e in res.get(t["name"], {})]
    models = [m for m, *_ in next(iter(next(iter(res.values())).values()))]
    fmt = lambda v: f"{v:g}"  # noqa: E731
    head = "| Task | Embodiment | " + " | ".join(m.replace(" (", "<br>(") for m in models) + " |\n|---|---|" + "---|" * len(models)
    rows = []
    for nm, e in order:
        cells = [f"**{fmt(v)}** ± {fmt(sd)}" if b else f"{fmt(v)} ± {fmt(sd)}" for _, v, sd, b in res[nm][e]]
        rows.append(f"| {nm} | {e} | " + " | ".join(cells) + " |")
    return head + "\n" + "\n".join(rows) + "\n"


def main():
    res = table_ii()
    (SRC / "data/_partials").mkdir(parents=True, exist_ok=True)
    (SRC / "data/_partials/datasets.md").write_text(datasets_partial())
    (SRC / "data/_partials/results.md").write_text(results_partial(res))
    (SRC / "tasks").mkdir(parents=True, exist_ok=True)
    (SRC / "robots").mkdir(parents=True, exist_ok=True)
    (SRC / "tasks/index.md").write_text(tasks_index())
    for t in TASKS:
        (SRC / f"tasks/{t['key']}.md").write_text(task_page(t, res))
    (SRC / "robots/index.md").write_text(robots_index())
    (SRC / "robots/arms.md").write_text(arms_page())
    (SRC / "robots/end-effectors.md").write_text(ee_page())
    (SRC / "robots/compatibility.md").write_text(compat_page())
    print(f"{len(TASKS)} task pages, robots pages; benchmark results for {len(res)} tasks")


if __name__ == "__main__":
    main()
