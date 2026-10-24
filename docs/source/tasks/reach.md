---
myst:
  html_meta:
    description: "Reach: Move the hand to a target point sampled in front of the robot."
---

# Reach

<span class="ds-chip blue">Track 1 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Move the hand to a target point sampled in front of the robot.</p>

<img class="ds-render" src="../_static/tasks/reach.webp" alt="Reach at reset, rendered in Blender">

<div class="ds-duo"><figure><video class="ds-video" src="../_static/clips/t1_reach_grip.mp4" poster="../_static/clips/t1_reach_grip.jpg" muted loop playsinline preload="none"></video><figcaption>Robotiq 2F-85, recorded human demonstration</figcaption></figure><figure><video class="ds-video" src="../_static/clips/t1_reach_hand.mp4" poster="../_static/clips/t1_reach_hand.jpg" muted loop playsinline preload="none"></video><figcaption>Allegro hand, recorded human demonstration</figcaption></figure></div>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>reach</code></dd>
<dt>Horizon</dt><dd>100 control steps (5 s at 20 Hz)</dd>
<dt>Objects</dt><dd>target sphere (no collision)</dd>
<dt>Success</dt><dd>TCP within 3 cm of the target.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Randomized at reset</dt><dd>Target in an ellipsoid with half axes of 15, 20 and 10 cm around the workspace centre.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/baselines/reach.py</code></dd>
</dl>

## Order of interactions

1. Move the hand to the target

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `target_pos` | (3,) |
| `target_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make("reach", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Parallel-jaw gripper | Allegro hand |
|---|---|---|
| BC-G (state) | 78 ± 5 | 82 ± 9 |
| BC-GMM (state) | 76 ± 2 | 75 ± 4 |
| BC-T (state) | 90 ± 2 | 88 ± 2 |
| Diffusion (state) | **100** ± 0 | **97** ± 1 |
| ACT (image) | 76 ± 6 | **73** ± 1 |
| Diffusion (image) | **80** ± 6 | 61 ± 2 |
