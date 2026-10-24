---
myst:
  html_meta:
    description: "Tool Hang: Assemble the hook frame on its stand and hang the wrench on the hook."
---

# Tool Hang

<span class="ds-chip blue">single arm</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Assemble the hook frame on its stand and hang the wrench on the hook.</p>

<img class="ds-render" src="../_static/tasks/tool_hang.webp" alt="Tool Hang at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>tool_hang</code></dd>
<dt>Horizon</dt><dd>1,000 control steps (50 s at 20 Hz)</dd>
<dt>Objects</dt><dd>hook frame, stand, ratcheting wrench</dd>
<dt>Success</dt><dd>Frame assembled and the wrench hole threaded on the hook.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Shown with</dt><dd>a Franka with the Allegro Hand</dd>
<dt>Action size</dt><dd>22 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/tool_hang.py</code></dd>
</dl>

## Order of interactions

1. Insert the frame into the stand
2. Grasp the wrench
3. Hang it on the hook

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `hook_frame_pos` | (3,) |
| `hook_frame_quat` | (4,) |
| `stand_pos` | (3,) |
| `stand_quat` | (4,) |
| `wrench_pos` | (3,) |
| `wrench_quat` | (4,) |

## Run it

```python
import dexsuite as ds

env = ds.make("tool_hang", manipulator="franka", gripper="allegro")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
