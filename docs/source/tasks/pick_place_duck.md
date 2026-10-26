---
myst:
  html_meta:
    description: "Duck in Bowl: Pinch the rubber duck by the head and drop it into the bowl."
---

# Duck in Bowl

<span class="ds-chip blue">single arm</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Pinch the rubber duck by the head and drop it into the bowl.</p>

<img class="ds-render" src="../_static/tasks/pick_place_duck.webp" alt="Duck in Bowl at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>pick_place_duck</code></dd>
<dt>Horizon</dt><dd>500 control steps (25 s at 20 Hz)</dd>
<dt>Objects</dt><dd>rubber duck, bowl</dd>
<dt>Success</dt><dd>Duck in the bowl, at rest and not touching the hand for 5 steps.</dd>
<dt>Failure</dt><dd>The duck falls below the table.</dd>
<dt>Shown with</dt><dd>the Sharpa hand on a floating wrist</dd>
<dt>Action size</dt><dd>28 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/single/rigid/pick_place_duck.py</code></dd>
</dl>

## Order of interactions

1. Pinch the duck
2. Carry it
3. Release it into the bowl

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Observations

What the task adds under `obs["state"]["other"]`, next to the robot state and the last two actions. Shapes are for one environment; with `n_envs > 1` each gets a leading batch dimension.

| Key | Shape |
|---|---|
| `bowl_floor_z` | (1,) |
| `bowl_inner_hi` | (2,) |
| `bowl_inner_lo` | (2,) |
| `bowl_inner_radius` | (1,) |
| `bowl_pos` | (3,) |
| `bowl_rim_z` | (1,) |
| `duck_aabb_hi` | (3,) |
| `duck_aabb_lo` | (3,) |
| `duck_ang` | (3,) |
| `duck_hand_contact` | (1,) |
| `duck_head_pos` | (3,) |
| `duck_in_bowl` | (1,) |
| `duck_pos` | (3,) |
| `duck_quat` | (4,) |
| `duck_rest_ticks` | (1,) |
| `duck_vel` | (3,) |

## Run it

```python
import dexsuite as ds

env = ds.make("pick_place_duck", manipulator="floating", gripper="sharpa_fardexbot")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

```{important}
Not in the pip package yet. This task runs from the `fudi` branch of the repository:
`git clone -b fudi https://github.com/anashoussaini/Dexsuite.git`, then `pip install -e .` in the clone.
```

```{note}
The spawn area is sized for a floating hand.
```
