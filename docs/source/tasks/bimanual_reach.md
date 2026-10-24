---
myst:
  html_meta:
    description: "Bimanual Reach: Each hand reaches its own target."
---

# Bimanual Reach

<span class="ds-chip blue">bimanual</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Each hand reaches its own target.</p>

<img class="ds-render" src="../_static/tasks/bimanual_reach.webp" alt="Bimanual Reach at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>bimanual_reach</code></dd>
<dt>Horizon</dt><dd>200 control steps (10 s at 20 Hz)</dd>
<dt>Objects</dt><dd>two target spheres</dd>
<dt>Success</dt><dd>Both TCPs within 3 cm of their targets.</dd>
<dt>Failure</dt><dd>A TCP leaves its workspace.</dd>
<dt>Shown with</dt><dd>two Franka arms with left and right Allegro hands</dd>
<dt>Action size</dt><dd>44 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/bimanual/baselines/bimanual_reach.py</code></dd>
</dl>

## Order of interactions

1. Both hands reach their targets

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `target_left_pos` | (3,) |
| `target_left_quat` | (4,) |
| `target_right_pos` | (3,) |
| `target_right_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make(
    "bimanual_reach",
    manipulator=("franka", "franka"),
    gripper=("allegro_left", "allegro_right"),
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
