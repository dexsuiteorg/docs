---
myst:
  html_meta:
    description: "Bimanual Rack Mug: Put the mug into the dish rack with two arms."
---

# Bimanual Rack Mug

<span class="ds-chip blue">bimanual</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Put the mug into the dish rack with two arms.</p>

<img class="ds-render" src="../_static/tasks/bimanual_pick_place_mug.webp" alt="Bimanual Rack Mug at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>bimanual_pick_place_mug</code></dd>
<dt>Horizon</dt><dd>40,000 control steps (2000 s at 20 Hz)</dd>
<dt>Objects</dt><dd>mug, dish rack</dd>
<dt>Success</dt><dd>Mug within the rack footprint and height, nearly at rest.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Shown with</dt><dd>two Franka arms with left and right Allegro hands</dd>
<dt>Action size</dt><dd>44 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/bimanual/rigid/bimanual_pick_place_mug.py</code></dd>
</dl>

## Order of interactions

1. Grasp the mug
2. Place it in the rack

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `mug_angular_vel` | (3,) |
| `mug_linear_vel` | (3,) |
| `mug_pos` | (3,) |
| `mug_quat` | (4,) |
| `rack_pos` | (3,) |
| `rack_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make(
    "bimanual_pick_place_mug",
    manipulator=("franka", "franka"),
    gripper=("allegro_left", "allegro_right"),
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
