---
myst:
  html_meta:
    description: "Bimanual Stack Mid-Air: Each arm lifts a cube and the two cubes are stacked in the air."
---

# Bimanual Stack Mid-Air

<span class="ds-chip blue">bimanual</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Each arm lifts a cube and the two cubes are stacked in the air.</p>

<img class="ds-render" src="../_static/tasks/bimanual_stack_mid_air.webp" alt="Bimanual Stack Mid-Air at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>bimanual_stack_mid_air</code></dd>
<dt>Horizon</dt><dd>400 control steps (20 s at 20 Hz)</dd>
<dt>Objects</dt><dd>6 cm cube, 5 cm cube</dd>
<dt>Success</dt><dd>B on A within 2 cm in xy and 1 cm in z, both above 8 cm.</dd>
<dt>Failure</dt><dd>A cube leaves the workspace.</dd>
<dt>Shown with</dt><dd>two Franka arms with left and right Allegro hands</dd>
<dt>Action size</dt><dd>44 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/bimanual/rigid/bimanual_stack_mid_air.py</code></dd>
</dl>

## Order of interactions

1. Both arms lift their cube
2. Stack B on A in the air

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `cube_a_pos` | (3,) |
| `cube_a_quat` | (4,) |
| `cube_b_pos` | (3,) |
| `cube_b_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make(
    "bimanual_stack_mid_air",
    manipulator=("franka", "franka"),
    gripper=("allegro_left", "allegro_right"),
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
