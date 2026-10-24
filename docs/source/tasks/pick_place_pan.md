---
myst:
  html_meta:
    description: "Move Pan: Lift the pan off the hot plate and set it down on the mat."
---

# Move Pan

<span class="ds-chip blue">Track 2 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Lift the pan off the hot plate and set it down on the mat.</p>

<img class="ds-render" src="../_static/tasks/pick_place_pan.webp" alt="Move Pan at reset, rendered in Blender">

<figure><video class="ds-video" src="../_static/clips/pan_allegro.mp4" poster="../_static/clips/pan_allegro.jpg" muted loop playsinline preload="none"></video><figcaption>A recorded demonstration from the dataset, replayed and rendered in Blender.</figcaption></figure>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>pick_place_pan</code></dd>
<dt>Horizon</dt><dd>500 control steps (25 s at 20 Hz)</dd>
<dt>Objects</dt><dd>pan, hot plate, mat</dd>
<dt>Success</dt><dd>Pan inside the mat footprint (4 cm margin), its base within 2 cm of the mat top.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Randomized at reset</dt><dd>Pan on one of the four burners, yaw ±20°. The hot plate and mat stay fixed.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/pick_place_pan.py</code></dd>
</dl>

## Order of interactions

1. Grasp the handle
2. Lift the pan
3. Carry it
4. Set it on the mat

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

env = ds.make("pick_place_pan", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Allegro hand |
|---|---|
| BC-G (state) | 5 ± 5 |
| BC-GMM (state) | 13 ± 6 |
| BC-T (state) | 68 ± 16 |
| Diffusion (state) | **69** ± 6 |
| ACT (image) | **89** ± 3 |
| Diffusion (image) | 72 ± 14 |
