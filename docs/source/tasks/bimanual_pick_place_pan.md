---
myst:
  html_meta:
    description: "Bimanual Move Pan: Move a frying pan from a burner on the hot plate onto the kitchen mat with two arms."
---

# Bimanual Move Pan

<span class="ds-chip blue">bimanual</span><span class="ds-chip">rigid</span>

<p class="ds-lede">Move a frying pan from a burner on the hot plate onto the kitchen mat with two arms.</p>

<img class="ds-render" src="../_static/tasks/bimanual_pick_place_pan.webp" alt="Bimanual Move Pan at reset, rendered in Blender">

## At a glance

<dl class="ds-spec">
<dt>Task key</dt><dd><code>bimanual_pick_place_pan</code></dd>
<dt>Horizon</dt><dd>700 control steps (35 s at 20 Hz)</dd>
<dt>Objects</dt><dd>frying pan, hot plate, kitchen mat</dd>
<dt>Success</dt><dd>No success check yet: the episode runs to the horizon.</dd>
<dt>Failure</dt><dd>None.</dd>
<dt>Shown with</dt><dd>two Franka arms with left and right Allegro hands</dd>
<dt>Action size</dt><dd>44 with the robot shown</dd>
<dt>Source</dt><dd><code>dexsuite/environments/bimanual/rigid/bimanual_pick_place_pan.py</code></dd>
</dl>

## Order of interactions

1. Grasp the pan
2. Carry it onto the mat

These are the stages the [failure analysis](../data/benchmark.md#where-policies-fail) scores, in order.


## Run it

```python
import dexsuite as ds

env = ds.make(
    "bimanual_pick_place_pan",
    manipulator=("franka", "franka"),
    gripper=("allegro_left", "allegro_right"),
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```
