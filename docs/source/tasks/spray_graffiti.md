---
myst:
  html_meta:
    description: "Spray Graffiti: Grasp the spray can and press its nozzle to paint the circular stencil on the sheet."
---

# Spray Graffiti

<span class="ds-chip blue">Track 2 benchmark</span><span class="ds-chip">articulated + paint</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Grasp the spray can and press its nozzle to paint the circular stencil on the sheet.</p>

<img class="ds-render" src="../_static/tasks/spray_graffiti.webp" alt="Spray Graffiti at reset, rendered in Blender">

<figure><video class="ds-video" src="../_static/clips/spray_sharpa.mp4" poster="../_static/clips/spray_sharpa.jpg" muted loop playsinline preload="none"></video><figcaption>A recorded demonstration from the dataset, replayed and rendered in Blender.</figcaption></figure>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>spray_graffiti</code></dd>
<dt>Horizon</dt><dd>600 control steps (30 s at 20 Hz)</dd>
<dt>Objects</dt><dd>spray can (sprung nozzle), paper sheet with a stencil</dd>
<dt>Success</dt><dd>At least 60% of the stencil painted with at most 35% of the paint outside it.</dd>
<dt>Failure</dt><dd>The can falls below the table.</dd>
<dt>Randomized at reset</dt><dd>Paper and can each within ±2 by ±3 cm, can yaw ±15°.</dd>
<dt>Shown with</dt><dd>the Sharpa hand on a floating wrist</dd>
<dt>Action size</dt><dd>28 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/spray_graffiti.py</code></dd>
</dl>

## Order of interactions

1. Grasp the can
2. Aim at the stencil
3. Press the nozzle to fill it

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `can_pos` | (3,) |
| `can_quat` | (4,) |
| `can_vel` | (3,) |
| `head_q` | (1,) |
| `nozzle_dir` | (3,) |
| `nozzle_pos` | (3,) |
| `paint_coverage` | (1,) |
| `paint_debug_spheres` | (1,) |
| `paint_outside_frac` | (1,) |
| `paper_pos` | (3,) |
| `paper_quat` | (4,) |
| `press_frac` | (1,) |
| `spray_active` | (1,) |
| `spray_hit_xy` | (2,) |
| `stencil_center_xy` | (2,) |
| `stencil_coverage` | (1,) |
| `stencil_id` | (1,) |
| `stencil_size` | (1,) |

## Run it

```python
import dexsuite as ds

env = ds.make("spray_graffiti", manipulator="floating", gripper="sharpa")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

```{note}
Runs with n_envs=1 (the paint canvas is a single texture).
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Sharpa hand |
|---|---|
| BC-G (state) | 0 ± 0 |
| BC-GMM (state) | 0 ± 0 |
| BC-T (state) | 0 ± 0 |
| Diffusion (state) | 0.7 ± 1 |
| ACT (image) | 0 ± 0 |
| Diffusion (image) | 0.7 ± 1 |
