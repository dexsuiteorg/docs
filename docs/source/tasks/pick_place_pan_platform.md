---
myst:
  html_meta:
    description: "Move Pan to Platform: Move the pan from the hot plate onto a mat raised on a 10 cm platform."
---

# Move Pan to Platform

<span class="ds-chip blue">single arm</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Move the pan from the hot plate onto a mat raised on a 10 cm platform.</p>

<img class="ds-render" src="../_static/tasks/pick_place_pan_platform.webp" alt="Move Pan to Platform at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>pick_place_pan_platform</code></dd>
<dt>Horizon</dt><dd>500 control steps (25 s at 20 Hz)</dd>
<dt>Objects</dt><dd>pan, hot plate, platform, raised mat</dd>
<dt>Success</dt><dd>Pan inside the mat footprint, its base within 2 cm of the mat top.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/pick_place_pan_platform.py</code></dd>
</dl>

## Order of interactions

1. Grasp the handle
2. Lift the pan
3. Set it on the raised mat

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `mat_inner_hi` | (2,) |
| `mat_inner_lo` | (2,) |
| `mat_top_z` | (1,) |
| `pan_aabb_hi` | (3,) |
| `pan_aabb_lo` | (3,) |
| `pan_ang` | (3,) |
| `pan_pos` | (3,) |
| `pan_quat` | (4,) |
| `pan_vel` | (3,) |

## Run it

```python
import dexsuite as ds

env = ds.make("pick_place_pan_platform", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
