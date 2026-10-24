---
myst:
  html_meta:
    description: "Stack: Build a tower of three cubes: B on A, then C on B."
---

# Stack

<span class="ds-chip blue">Track 1 benchmark</span><span class="ds-chip">rigid</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Build a tower of three cubes: B on A, then C on B.</p>

<img class="ds-render" src="../_static/tasks/stack.webp" alt="Stack at reset, rendered in Blender">

<div class="ds-duo"><figure><video class="ds-video" src="../_static/clips/t1_stack_grip.mp4" poster="../_static/clips/t1_stack_grip.jpg" muted loop playsinline preload="none"></video><figcaption>UMI gripper, recorded human demonstration, 2× speed</figcaption></figure><figure><video class="ds-video" src="../_static/clips/t1_stack_hand.mp4" poster="../_static/clips/t1_stack_hand.jpg" muted loop playsinline preload="none"></video><figcaption>Allegro hand, recorded human demonstration, 2× speed</figcaption></figure></div>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>stack</code></dd>
<dt>Horizon</dt><dd>600 control steps (30 s at 20 Hz)</dd>
<dt>Objects</dt><dd>cube A (red, bottom), cube B (blue), cube C (green, top)</dd>
<dt>Success</dt><dd>Each cube within 2 cm of the one below in xy and stacked within 1 cm in z, in order.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Randomized at reset</dt><dd>Three cubes spread over 25 by 40 cm, 15 to 45 cm apart.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/baselines/stack.py</code></dd>
</dl>

## Order of interactions

1. Place cube B on cube A
2. Place cube C on cube B

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `cube_a_pos` | (3,) |
| `cube_a_quat` | (4,) |
| `cube_b_pos` | (3,) |
| `cube_b_quat` | (4,) |
| `cube_c_pos` | (3,) |
| `cube_c_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make("stack", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Parallel-jaw gripper | Allegro hand |
|---|---|---|
| BC-G (state) | 0 ± 0 | 0 ± 0 |
| BC-GMM (state) | 0 ± 0 | 0 ± 0 |
| BC-T (state) | 2 ± 0 | 1 ± 1 |
| Diffusion (state) | **16** ± 2 | **9** ± 5 |
| ACT (image) | 1 ± 1 | 0 ± 0 |
| Diffusion (image) | 2 ± 0 | 1 ± 1 |
