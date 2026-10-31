---
myst:
  html_meta:
    description: "Bimanual Make Coffee: Place the mug on the tray of a fixed coffee machine with two arms."
---

# Bimanual Make Coffee

<span class="ds-chip blue">bimanual</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Place the mug on the tray of a fixed coffee machine with two arms.</p>

<img class="ds-render" src="../_static/tasks/bimanual_make_coffee.webp" alt="Bimanual Make Coffee at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>bimanual_make_coffee</code></dd>
<dt>Horizon</dt><dd>1,000 control steps (50 s at 20 Hz)</dd>
<dt>Objects</dt><dd>mug, coffee machine</dd>
<dt>Success</dt><dd>No success check yet: the episode runs to the horizon.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Shown with</dt><dd>two Franka arms with left and right Allegro hands</dd>
<dt>Action size</dt><dd>44 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/bimanual/rigid/bimanual_make_coffee.py</code></dd>
</dl>

## Order of interactions

1. Grasp the mug
2. Set it on the tray

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `machine_pos` | (3,) |
| `machine_quat` | (4,) |
| `mug_pos` | (3,) |
| `mug_quat` | (4,) |
| `mug_target_pos` | (3,) |
| `mug_target_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make(
    "bimanual_make_coffee",
    manipulator=("franka", "franka"),
    gripper=("allegro_left", "allegro_right"),
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
