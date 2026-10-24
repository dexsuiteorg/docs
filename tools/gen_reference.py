#!/usr/bin/env python
"""Generate the options reference and the registry from the DexSuite source (read with ast, nothing is imported).

    python3 tools/gen_reference.py [path/to/Dexsuite]

Writes docs/source/reference/options.md and docs/source/reference/registry.md. Re-run after the options change.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "/efs/projects/fudi/simulation/Dexsuite")
PKG = REPO / "dexsuite"
OUT = Path(__file__).resolve().parents[1] / "docs/source/reference"
CLASSES = [("sim.py", "SimOptions"), ("robot.py", "RobotOptions"), ("robot.py", "ArmOptions"), ("robot.py", "ControllerOptions"),
           ("robot.py", "AABBOptions"), ("layout.py", "LayoutOptions"), ("layout.py", "PoseOptions"),
           ("camera.py", "CamerasOptions"), ("camera.py", "StaticCamOptions"), ("camera.py", "DynamicCamOptions")]
READABLE = {"_default_manipulator_controller": 'ControllerOptions("osc_pose")',
            "_default_gripper_controller": 'ControllerOptions("joint_position")',
            "_DEFAULT_MANIPULATOR": '"franka"', "_DEFAULT_GRIPPER": '"robotiq"'}
HIDDEN = {"umi"}   # registered, but not a documented robot: the UMI gripper is franka_umi_tacticle
MISSING = {("SimOptions", "n_envs"): "Number of parallel copies of the scene.",
           ("LayoutOptions", "params"): "Reserved, not used yet."}


def attrs_from_doc(doc):
    out, cur = {}, None
    m = re.search(r"Attributes:\n(.*?)(\n\s*\n|\Z)", doc or "", re.S)
    if not m:
        return out
    for line in m.group(1).splitlines():
        mm = re.match(r"\s{4,8}(\w+)(?: \([^)]*\))?:\s*(.*)", line)
        if mm and len(line) - len(line.lstrip()) <= 8:
            cur = mm.group(1)
            out[cur] = mm.group(2).strip()
        elif cur and line.strip():
            out[cur] += " " + line.strip()
    return out


CONSTS: dict[str, str] = {}


def module_consts(tree):
    """Module-level NAME = value, so defaults like _DEFAULT_ROBOT_TYPE show their value."""
    out = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            out[n.targets[0].id] = ast.unparse(n.value)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.value is not None:
            out[n.target.id] = ast.unparse(n.value)
    return out


def default_of(node):
    if node is None:
        return "required"
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "field":
        for kw in node.keywords:
            if kw.arg == "default_factory":
                v = ast.unparse(kw.value)
                if isinstance(kw.value, ast.Lambda):
                    v = ast.unparse(kw.value.body)
                return READABLE.get(v, v + "()" if not v.endswith(")") else v)
            if kw.arg == "default":
                return ast.unparse(kw.value)
    v = ast.unparse(node)
    return READABLE.get(v, CONSTS.get(v, v))


def summary(doc):
    return " ".join((doc or "").strip().split("\n\n")[0].split())


def options_md():
    parts = ["""# Options

<p class="ds-lede">Every option class that <code>ds.make</code> accepts, field by field, generated from
<code>dexsuite/options/</code>. Import them from <code>dexsuite</code>.</p>

```python
import dexsuite as ds

ds.make("lift", robot=ds.RobotOptions(...), cameras=ds.CamerasOptions(...), sim=ds.SimOptions(...))
```
"""]
    for fname, cname in CLASSES:
        tree = ast.parse((PKG / "options" / fname).read_text())
        CONSTS.clear()
        CONSTS.update(module_consts(tree))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cname)
        doc = ast.get_docstring(cls)
        docs = attrs_from_doc(doc)
        rows = []
        for n in cls.body:
            if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and not n.target.id.startswith("_"):
                name = n.target.id
                typ = ast.unparse(n.annotation).replace("|", "\\|")
                d = docs.get(name) or MISSING.get((cname, name), "")
                dflt = default_of(n.value).replace("|", "\\|")
                rows.append(f"| `{name}` | `{typ}` | `{dflt}` | {d} |")
        parts.append(f"\n({cname.lower()})=\n## {cname}\n\n{summary(doc)}\n\n| Field | Type | Default | Meaning |\n|---|---|---|---|\n"
                     + "\n".join(rows) + "\n")
    return "".join(parts)


def registry_md():
    def names(sub, deco):
        out = set()
        for p in (PKG / sub).rglob("*.py"):
            out |= set(re.findall(rf'{deco}\("([A-Za-z0-9_]+)"', p.read_text(errors="ignore")))
        return sorted(out, key=str.lower)
    envs, arms, ees = names("environments", "register_env"), names("models/manipulators", "register_manipulator"), names("models/grippers", "register_gripper")
    ees = [e for e in ees if e not in HIDDEN]
    ctrls = sorted(p.stem for p in (PKG / "controllers").glob("*.py") if not p.stem.startswith("_") and p.stem not in ("base", "base_controller", "pose_backend", "validation", "utils"))
    fmt = lambda xs: ", ".join(f"`{x}`" for x in xs)  # noqa: E731
    return f"""# Registry

<p class="ds-lede">Every name <code>ds.make</code> understands, read from the registration decorators in the source.
The <a href="../tasks/index.html">task catalog</a> documents the tasks that are ready to use.</p>

Tasks ({len(envs)})
: {fmt(envs)}

Arms and robots ({len(arms)})
: {fmt(arms)}

End-effectors ({len(ees)})
: {fmt(ees)}

Controllers ({len(ctrls)})
: {fmt(ctrls)}

Names are case-insensitive. Registration happens when `dexsuite` is imported, which walks `dexsuite.models` and
`dexsuite.environments`. Code outside the package registers its classes when it is imported.

```python
from dexsuite.core.registry import register_env, register_manipulator, register_gripper
```
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "options.md").write_text(options_md())
    (OUT / "registry.md").write_text(registry_md())
    print("reference: options.md, registry.md")


if __name__ == "__main__":
    main()
