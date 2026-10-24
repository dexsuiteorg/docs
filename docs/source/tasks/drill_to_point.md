---
myst:
  html_meta:
    description: "Drill to Point: Pick up the drill and bring its tip to the target on the wall, aligned with it."
---

# Drill to Point

<span class="ds-chip blue">Track 2 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Pick up the drill and bring its tip to the target on the wall, aligned with it.</p>

<img class="ds-render" src="../_static/tasks/drill_to_point.webp" alt="Drill to Point at reset, rendered in Blender">

<figure><video class="ds-video" src="../_static/clips/drill_allegro.mp4" poster="../_static/clips/drill_allegro.jpg" muted loop playsinline preload="none"></video><figcaption>A recorded demonstration from the dataset, replayed and rendered in Blender.</figcaption></figure>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>drill_to_point</code></dd>
<dt>Horizon</dt><dd>300 control steps (15 s at 20 Hz)</dd>
<dt>Objects</dt><dd>drill, wall with target</dd>
<dt>Success</dt><dd>Tip within 3 cm of the target, pitch and yaw within 20°.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Randomized at reset</dt><dd>Target ±5 cm in x and z; drill yaw ±10°.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/drill_to_point.py</code></dd>
</dl>

## Order of interactions

1. Grasp the drill
2. Lift it
3. Align the tip with the target

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `drill_pos` | (3,) |
| `drill_quat` | (4,) |
| `drill_tip_pos` | (3,) |
| `drill_tip_quat` | (4,) |
| `target_pos` | (3,) |
| `target_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make("drill_to_point", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Allegro hand |
|---|---|
| BC-G (state) | 1 ± 1 |
| BC-GMM (state) | 5 ± 2 |
| BC-T (state) | 47 ± 8 |
| Diffusion (state) | **50** ± 2 |
| ACT (image) | **43** ± 3 |
| Diffusion (image) | 32 ± 4 |
