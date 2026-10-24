---
myst:
  html_meta:
    description: "Push: Push the cube along the table to a goal 20 cm to its side, without lifting it."
---

# Push

<span class="ds-chip blue">Track 1 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Push the cube along the table to a goal 20 cm to its side, without lifting it.</p>

<img class="ds-render" src="../_static/tasks/push.webp" alt="Push at reset, rendered in Blender">

<div class="ds-duo"><figure><video class="ds-video" src="../_static/clips/t1_push_grip.mp4" poster="../_static/clips/t1_push_grip.jpg" muted loop playsinline preload="none"></video><figcaption>UMI gripper, recorded human demonstration</figcaption></figure><figure><video class="ds-video" src="../_static/clips/t1_push_hand.mp4" poster="../_static/clips/t1_push_hand.jpg" muted loop playsinline preload="none"></video><figcaption>Allegro hand, recorded human demonstration</figcaption></figure></div>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>push</code></dd>
<dt>Horizon</dt><dd>200 control steps (10 s at 20 Hz)</dd>
<dt>Objects</dt><dd>5 cm cube, goal marker</dd>
<dt>Success</dt><dd>Cube within 3 cm of the goal.</dd>
<dt>Failure</dt><dd>TCP leaves the workspace, or the cube is lifted above 5.5 cm.</dd>
<dt>Randomized at reset</dt><dd>Cube within ±10 cm; the goal is 20 cm from it along −y.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/baselines/push.py</code></dd>
</dl>

## Order of interactions

1. Contact the cube
2. Push it to the goal

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `cube_pos` | (3,) |
| `cube_quat` | (4,) |
| `goal_pos` | (3,) |

## Run it

```python
import dexsuite as ds

env = ds.make("push", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Parallel-jaw gripper | Allegro hand |
|---|---|---|
| BC-G (state) | 27 ± 6 | 46 ± 7 |
| BC-GMM (state) | 23 ± 6 | 47 ± 5 |
| BC-T (state) | 48 ± 4 | 60 ± 7 |
| Diffusion (state) | **63** ± 2 | **68** ± 5 |
| ACT (image) | **50** ± 2 | **66** ± 6 |
| Diffusion (image) | 33 ± 6 | 62 ± 3 |
