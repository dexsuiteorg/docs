---
myst:
  html_meta:
    description: "Pick &amp; Place: Pick up the cube and place it on a goal in the far quadrant of the table."
---

# Pick & Place

<span class="ds-chip blue">Track 1 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Pick up the cube and place it on a goal in the far quadrant of the table.</p>

<img class="ds-render" src="../_static/tasks/pick_place.webp" alt="Pick &amp; Place at reset, rendered in Blender">

<div class="ds-duo"><figure><video class="ds-video" src="../_static/clips/t1_pickplace_grip.mp4" poster="../_static/clips/t1_pickplace_grip.jpg" muted loop playsinline preload="none"></video><figcaption>UMI gripper, recorded human demonstration</figcaption></figure><figure><video class="ds-video" src="../_static/clips/t1_pickplace_hand.mp4" poster="../_static/clips/t1_pickplace_hand.jpg" muted loop playsinline preload="none"></video><figcaption>Allegro hand, recorded human demonstration</figcaption></figure></div>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>pick_place</code></dd>
<dt>Horizon</dt><dd>200 control steps (10 s at 20 Hz)</dd>
<dt>Objects</dt><dd>5 cm cube, goal marker</dd>
<dt>Success</dt><dd>Cube within 3 cm of the goal.</dd>
<dt>Failure</dt><dd>TCP leaves the workspace.</dd>
<dt>Randomized at reset</dt><dd>Cube within 5 cm of the centre; goal within 5 cm of a point in the far quadrant.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/baselines/pick_place.py</code></dd>
</dl>

## Order of interactions

1. Grasp the cube
2. Carry it
3. Place it at the goal

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

env = ds.make("pick_place", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Parallel-jaw gripper | Allegro hand |
|---|---|---|
| BC-G (state) | 49 ± 14 | 15 ± 4 |
| BC-GMM (state) | 24 ± 6 | 35 ± 5 |
| BC-T (state) | 64 ± 0 | **76** ± 5 |
| Diffusion (state) | **65** ± 5 | 67 ± 3 |
| ACT (image) | **66** ± 4 | **60** ± 7 |
| Diffusion (image) | 45 ± 4 | 52 ± 11 |
