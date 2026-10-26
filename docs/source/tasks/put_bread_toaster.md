---
myst:
  html_meta:
    description: "Toast Bread: Stand the slice of bread in a toaster slot and push the lever down."
---

# Toast Bread

<span class="ds-chip blue">Track 2 benchmark</span><span class="ds-chip">articulated</span><span class="ds-chip">dataset on Hugging Face</span>

<p class="ds-lede">Stand the slice of bread in a toaster slot and push the lever down.</p>

<img class="ds-render" src="../_static/tasks/put_bread_toaster.webp" alt="Toast Bread at reset, rendered in Blender">

<figure><video class="ds-video" src="../_static/clips/toast_sharpa.mp4" poster="../_static/clips/toast_sharpa.jpg" muted loop playsinline preload="none"></video><figcaption>A recorded demonstration from the dataset, replayed and rendered in Blender.</figcaption></figure>

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>put_bread_toaster</code></dd>
<dt>Horizon</dt><dd>600 control steps (30 s at 20 Hz)</dd>
<dt>Objects</dt><dd>toaster (lever, dial), slice of bread</dd>
<dt>Success</dt><dd>Toast upright at least 3 cm into a slot, lever at least 80% down, toast at rest.</dd>
<dt>Failure</dt><dd>The toast falls below the table.</dd>
<dt>Randomized at reset</dt><dd>Toaster within ±2 cm and yaw ±8°, toast within ±3 by ±4 cm at any yaw.</dd>
<dt>Shown with</dt><dd>the Sharpa hand on a floating wrist</dd>
<dt>Action size</dt><dd>28 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/put_bread_toaster.py</code></dd>
</dl>

## Order of interactions

1. Grasp the toast
2. Insert it into a slot
3. Press the lever

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `dial_q` | (1,) |
| `lever_frac` | (1,) |
| `lever_q` | (1,) |
| `toast_aabb_hi` | (3,) |
| `toast_aabb_lo` | (3,) |
| `toast_ang` | (3,) |
| `toast_in_slot` | (1,) |
| `toast_in_toaster_frame` | (3,) |
| `toast_pos` | (3,) |
| `toast_quat` | (4,) |
| `toast_vel` | (3,) |
| `toaster_pos` | (3,) |
| `toaster_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make("put_bread_toaster", manipulator="floating", gripper="sharpa")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

```{note}
The slot geometry is chosen with the DEXSUITE_TOASTER_SLOT environment variable (default wide_b).
```

## Baseline results

Success rate (%) from the DexSuite benchmark: mean ± standard deviation over three evaluation seeds with 50 episodes each. Bold is the best result within each input type. See [the benchmark](../data/benchmark.md) for the protocol.

| Baseline | Sharpa hand |
|---|---|
| BC-G (state) | 0 ± 0 |
| BC-GMM (state) | 0 ± 0 |
| BC-T (state) | 0 ± 0 |
| Diffusion (state) | 0 ± 0 |
| ACT (image) | 0 ± 0 |
| Diffusion (image) | 0 ± 0 |
