---
myst:
  html_meta:
    description: "Close Window and Spray: Slide the window shut, then spray the glass with the trigger bottle."
---

# Close Window and Spray

<span class="ds-chip blue">single arm</span><span class="ds-chip">articulated + paint</span>

<p class="ds-lede">Slide the window shut, then spray the glass with the trigger bottle.</p>

<img class="ds-render" src="../_static/tasks/close_window_spray.webp" alt="Close Window and Spray at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>close_window_spray</code></dd>
<dt>Horizon</dt><dd>900 control steps (45 s at 20 Hz)</dd>
<dt>Objects</dt><dd>sash window, spray bottle (trigger)</dd>
<dt>Success</dt><dd>Sash closed and at least 20 spray steps on the pane from 15 to 35 cm away.</dd>
<dt>Failure</dt><dd>The bottle falls below the table.</dd>
<dt>Shown with</dt><dd>the Sharpa hand on a floating wrist</dd>
<dt>Action size</dt><dd>28 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/close_window_spray.py</code></dd>
</dl>

## Order of interactions

1. Close the sash
2. Grasp the bottle
3. Spray the pane

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `bottle_pos` | (3,) |
| `bottle_quat` | (4,) |
| `bottle_vel` | (3,) |
| `circle_complete` | (1,) |
| `circle_sector_coverage` | (1,) |
| `circle_spray_steps` | (1,) |
| `latch_q` | (1,) |
| `nozzle_dir` | (3,) |
| `nozzle_pos` | (3,) |
| `paint_debug_spheres` | (1,) |
| `pane_center` | (3,) |
| `pane_coverage` | (1,) |
| `pane_normal` | (3,) |
| `pane_spray_complete` | (1,) |
| `pane_spray_steps` | (1,) |
| `pull_frac` | (1,) |
| `sash_closed` | (1,) |
| `sash_frac` | (1,) |
| `sash_pos` | (3,) |
| `sash_q` | (1,) |
| `spray_active` | (1,) |
| `trigger_q` | (1,) |

## Run it

```python
import dexsuite as ds

env = ds.make("close_window_spray", manipulator="floating", gripper="sharpa")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

```{important}
Not in the pip package yet. This task runs from the `fudi` branch of the repository:
`git clone -b fudi https://github.com/anashoussaini/Dexsuite.git`, then `pip install -e .` in the clone.
```

```{note}
Runs with n_envs=1.
```

```{note}
Finger friction is tuned for the Sharpa hand.
```
