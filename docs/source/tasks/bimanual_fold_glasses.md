---
myst:
  html_meta:
    description: "Bimanual Fold Glasses: Fold a pair of articulated glasses resting on a tray with two arms."
---

# Bimanual Fold Glasses

<span class="ds-chip blue">bimanual</span><span class="ds-chip">articulated</span>

<p class="ds-lede">Fold a pair of articulated glasses resting on a tray with two arms.</p>

<img class="ds-render" src="../_static/tasks/bimanual_fold_glasses.webp" alt="Bimanual Fold Glasses at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>bimanual_fold_glasses</code></dd>
<dt>Horizon</dt><dd>40,000 control steps (2000 s at 20 Hz)</dd>
<dt>Objects</dt><dd>glasses (two hinges), tray</dd>
<dt>Success</dt><dd>No success check yet: the episode runs to the horizon.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Shown with</dt><dd>two Franka arms with left and right Allegro hands</dd>
<dt>Action size</dt><dd>44 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/bimanual/rigid/bimanual_fold_glasses.py</code></dd>
</dl>

## Order of interactions

1. Fold one temple
2. Fold the other

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `glasses_pos` | (3,) |
| `hinge_angles` | (2,) |
| `tray_top_z` | (1,) |

## Run it

```python
import dexsuite as ds

env = ds.make(
    "bimanual_fold_glasses",
    manipulator=("franka", "franka"),
    gripper=("allegro_left", "allegro_right"),
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
