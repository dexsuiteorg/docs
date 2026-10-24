---
myst:
  html_meta:
    description: "Place Fruits: Put the apple and the lemon into the bowl, one after the other."
---

# Place Fruits

<span class="ds-chip blue">Track 2 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Put the apple and the lemon into the bowl, one after the other.</p>

<img class="ds-render" src="../_static/tasks/pick_place_fruit.webp" alt="Place Fruits at reset, rendered in Blender">

<figure><video class="ds-video" src="../_static/clips/fruit_allegro.mp4" poster="../_static/clips/fruit_allegro.jpg" muted loop playsinline preload="none"></video><figcaption>A recorded demonstration from the dataset, replayed and rendered in Blender.</figcaption></figure>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>pick_place_fruit</code></dd>
<dt>Horizon</dt><dd>400 control steps (20 s at 20 Hz)</dd>
<dt>Objects</dt><dd>apple, lemon, bowl</dd>
<dt>Success</dt><dd>Both fruits inside the bowl, at least 1 cm below the rim, hand clear of the bowl.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Randomized at reset</dt><dd>Bowl and fruits each within ±12 cm, fruits 15 to 45 cm apart, yaw ±10°.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/pick_place_fruit.py</code></dd>
</dl>

## Order of interactions

1. Place the apple in the bowl
2. Release
3. Place the lemon

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `apple_ang` | (3,) |
| `apple_pos` | (3,) |
| `apple_quat` | (4,) |
| `apple_vel` | (3,) |
| `bowl_aabb_hi` | (3,) |
| `bowl_aabb_lo` | (3,) |
| `bowl_inner_hi` | (2,) |
| `bowl_inner_lo` | (2,) |
| `bowl_pos` | (3,) |
| `bowl_quat` | (4,) |
| `bowl_top_z` | (1,) |
| `lemon_ang` | (3,) |
| `lemon_pos` | (3,) |
| `lemon_quat` | (4,) |
| `lemon_vel` | (3,) |

## Run it

```python
import dexsuite as ds

env = ds.make("pick_place_fruit", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Allegro hand |
|---|---|
| BC-G (state) | 1 ± 1 |
| BC-GMM (state) | 3 ± 1 |
| BC-T (state) | **9** ± 2 |
| Diffusion (state) | 7 ± 3 |
| ACT (image) | **27** ± 5 |
| Diffusion (image) | 5 ± 1 |
