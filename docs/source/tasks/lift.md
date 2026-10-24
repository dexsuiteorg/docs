---
myst:
  html_meta:
    description: "Lift: Grasp a 5 cm cube and lift it to the goal marker above its start."
---

# Lift

<span class="ds-chip blue">Track 1 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Grasp a 5 cm cube and lift it to the goal marker above its start.</p>

<img class="ds-render" src="../_static/tasks/lift.webp" alt="Lift at reset, rendered in Blender">

<div class="ds-duo"><figure><video class="ds-video" src="../_static/clips/t1_lift_grip.mp4" poster="../_static/clips/t1_lift_grip.jpg" muted loop playsinline preload="none"></video><figcaption>UMI gripper, recorded human demonstration</figcaption></figure><figure><video class="ds-video" src="../_static/clips/t1_lift_hand.mp4" poster="../_static/clips/t1_lift_hand.jpg" muted loop playsinline preload="none"></video><figcaption>Allegro hand, recorded human demonstration</figcaption></figure></div>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>lift</code></dd>
<dt>Horizon</dt><dd>600 control steps (30 s at 20 Hz)</dd>
<dt>Objects</dt><dd>5 cm cube, goal marker</dd>
<dt>Success</dt><dd>Cube raised to at least 0.215 m (within 1 cm of the goal) and within 5 cm of its start in xy.</dd>
<dt>Failure</dt><dd>TCP leaves the workspace.</dd>
<dt>Randomized at reset</dt><dd>Cube within ±10 by ±25 cm; the goal sits 22.5 cm above it.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/baselines/lift.py</code></dd>
</dl>

## Order of interactions

1. Grasp the cube
2. Raise it to the goal

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `cube_pos` | (3,) |
| `cube_quat` | (4,) |
| `target_pos` | (3,) |

## Run it

```python
import dexsuite as ds

env = ds.make("lift", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Parallel-jaw gripper | Allegro hand |
|---|---|---|
| BC-G (state) | 31 ± 5 | 21 ± 2 |
| BC-GMM (state) | 32 ± 5 | 43 ± 8 |
| BC-T (state) | 57 ± 8 | 47 ± 6 |
| Diffusion (state) | **72** ± 3 | **65** ± 8 |
| ACT (image) | **73** ± 6 | 45 ± 5 |
| Diffusion (image) | 54 ± 8 | **58** ± 12 |
