# Tasks

<p class="ds-lede">Every task is one class with its own reset, observations and success check, and runs with any arm and
end-effector that fits it. These are the tasks that build and report success today, rendered at reset.</p>

Pick a task by its key: `ds.make("<key>", manipulator=..., gripper=...)`. Eleven of them form the
[DexSuite benchmark](../data/benchmark.md), and their demonstrations are on
[Hugging Face](https://huggingface.co/dexsuite).

## Benchmark, Track 1

Cross-embodiment: run with the parallel-jaw gripper and the Allegro hand.

<div class="ds-grid wide">
<a class="ds-tile" href="reach.html"><img src="../_static/tasks/reach.webp" alt="Reach" loading="lazy"><div class="ds-tile-text"><b>Reach</b><small><code>reach</code></small></div></a>
<a class="ds-tile" href="lift.html"><img src="../_static/tasks/lift.webp" alt="Lift" loading="lazy"><div class="ds-tile-text"><b>Lift</b><small><code>lift</code></small></div></a>
<a class="ds-tile" href="push.html"><img src="../_static/tasks/push.webp" alt="Push" loading="lazy"><div class="ds-tile-text"><b>Push</b><small><code>push</code></small></div></a>
<a class="ds-tile" href="pick_place.html"><img src="../_static/tasks/pick_place.webp" alt="Pick &amp; Place" loading="lazy"><div class="ds-tile-text"><b>Pick &amp; Place</b><small><code>pick_place</code></small></div></a>
<a class="ds-tile" href="stack.html"><img src="../_static/tasks/stack.webp" alt="Stack" loading="lazy"><div class="ds-tile-text"><b>Stack</b><small><code>stack</code></small></div></a>
</div>

## Benchmark, Track 2

Dexterous capability: hand-only tasks.

<div class="ds-grid wide">
<a class="ds-tile" href="pick_place_mug.html"><img src="../_static/tasks/pick_place_mug.webp" alt="Rack Mug" loading="lazy"><div class="ds-tile-text"><b>Rack Mug</b><small><code>pick_place_mug</code></small></div></a>
<a class="ds-tile" href="pick_place_pan.html"><img src="../_static/tasks/pick_place_pan.webp" alt="Move Pan" loading="lazy"><div class="ds-tile-text"><b>Move Pan</b><small><code>pick_place_pan</code></small></div></a>
<a class="ds-tile" href="drill_to_point.html"><img src="../_static/tasks/drill_to_point.webp" alt="Drill to Point" loading="lazy"><div class="ds-tile-text"><b>Drill to Point</b><small><code>drill_to_point</code></small></div></a>
<a class="ds-tile" href="pick_place_fruit.html"><img src="../_static/tasks/pick_place_fruit.webp" alt="Place Fruits" loading="lazy"><div class="ds-tile-text"><b>Place Fruits</b><small><code>pick_place_fruit</code></small></div></a>
<a class="ds-tile" href="spray_graffiti.html"><img src="../_static/tasks/spray_graffiti.webp" alt="Spray Graffiti" loading="lazy"><div class="ds-tile-text"><b>Spray Graffiti</b><small><code>spray_graffiti</code></small></div></a>
<a class="ds-tile" href="put_bread_toaster.html"><img src="../_static/tasks/put_bread_toaster.webp" alt="Toast Bread" loading="lazy"><div class="ds-tile-text"><b>Toast Bread</b><small><code>put_bread_toaster</code></small></div></a>
</div>

## More single-arm tasks

Further tasks with a success check, outside the benchmark.

<div class="ds-grid wide">
<a class="ds-tile" href="make_coffee.html"><img src="../_static/tasks/make_coffee.webp" alt="Make Coffee" loading="lazy"><div class="ds-tile-text"><b>Make Coffee</b><small><code>make_coffee</code></small></div></a>
<a class="ds-tile" href="tool_hang.html"><img src="../_static/tasks/tool_hang.webp" alt="Tool Hang" loading="lazy"><div class="ds-tile-text"><b>Tool Hang</b><small><code>tool_hang</code></small></div></a>
<a class="ds-tile" href="pick_place_pan_platform.html"><img src="../_static/tasks/pick_place_pan_platform.webp" alt="Move Pan to Platform" loading="lazy"><div class="ds-tile-text"><b>Move Pan to Platform</b><small><code>pick_place_pan_platform</code></small></div></a>
<a class="ds-tile" href="pick_place_duck.html"><img src="../_static/tasks/pick_place_duck.webp" alt="Duck in Bowl" loading="lazy"><div class="ds-tile-text"><b>Duck in Bowl</b><small><code>pick_place_duck</code></small></div></a>
<a class="ds-tile" href="open_safe.html"><img src="../_static/tasks/open_safe.webp" alt="Open Safe" loading="lazy"><div class="ds-tile-text"><b>Open Safe</b><small><code>open_safe</code></small></div></a>
<a class="ds-tile" href="stow_in_safe.html"><img src="../_static/tasks/stow_in_safe.webp" alt="Stow in Safe" loading="lazy"><div class="ds-tile-text"><b>Stow in Safe</b><small><code>stow_in_safe</code></small></div></a>
<a class="ds-tile" href="pliers_in_jewelry_box.html"><img src="../_static/tasks/pliers_in_jewelry_box.webp" alt="Pliers in Jewelry Box" loading="lazy"><div class="ds-tile-text"><b>Pliers in Jewelry Box</b><small><code>pliers_in_jewelry_box</code></small></div></a>
<a class="ds-tile" href="close_window_spray.html"><img src="../_static/tasks/close_window_spray.webp" alt="Close Window and Spray" loading="lazy"><div class="ds-tile-text"><b>Close Window and Spray</b><small><code>close_window_spray</code> · from source</small></div></a>
</div>

## Bimanual tasks

Two arms, side by side by default.

<div class="ds-grid wide">
<a class="ds-tile" href="bimanual_reach.html"><img src="../_static/tasks/bimanual_reach.webp" alt="Bimanual Reach" loading="lazy"><div class="ds-tile-text"><b>Bimanual Reach</b><small><code>bimanual_reach</code></small></div></a>
<a class="ds-tile" href="bimanual_lift.html"><img src="../_static/tasks/bimanual_lift.webp" alt="Bimanual Lift" loading="lazy"><div class="ds-tile-text"><b>Bimanual Lift</b><small><code>bimanual_lift</code></small></div></a>
<a class="ds-tile" href="bimanual_push.html"><img src="../_static/tasks/bimanual_push.webp" alt="Bimanual Push" loading="lazy"><div class="ds-tile-text"><b>Bimanual Push</b><small><code>bimanual_push</code></small></div></a>
<a class="ds-tile" href="bimanual_pick_place.html"><img src="../_static/tasks/bimanual_pick_place.webp" alt="Bimanual Pick &amp; Place" loading="lazy"><div class="ds-tile-text"><b>Bimanual Pick &amp; Place</b><small><code>bimanual_pick_place</code></small></div></a>
<a class="ds-tile" href="bimanual_stack.html"><img src="../_static/tasks/bimanual_stack.webp" alt="Bimanual Stack" loading="lazy"><div class="ds-tile-text"><b>Bimanual Stack</b><small><code>bimanual_stack</code></small></div></a>
<a class="ds-tile" href="bimanual_stack_mid_air.html"><img src="../_static/tasks/bimanual_stack_mid_air.webp" alt="Bimanual Stack Mid-Air" loading="lazy"><div class="ds-tile-text"><b>Bimanual Stack Mid-Air</b><small><code>bimanual_stack_mid_air</code></small></div></a>
<a class="ds-tile" href="bimanual_pick_place_mug.html"><img src="../_static/tasks/bimanual_pick_place_mug.webp" alt="Bimanual Rack Mug" loading="lazy"><div class="ds-tile-text"><b>Bimanual Rack Mug</b><small><code>bimanual_pick_place_mug</code></small></div></a>
<a class="ds-tile" href="bimanual_pick_place_pan.html"><img src="../_static/tasks/bimanual_pick_place_pan.webp" alt="Bimanual Move Pan" loading="lazy"><div class="ds-tile-text"><b>Bimanual Move Pan</b><small><code>bimanual_pick_place_pan</code></small></div></a>
<a class="ds-tile" href="bimanual_pick_place_pot.html"><img src="../_static/tasks/bimanual_pick_place_pot.webp" alt="Bimanual Move Pot" loading="lazy"><div class="ds-tile-text"><b>Bimanual Move Pot</b><small><code>bimanual_pick_place_pot</code></small></div></a>
<a class="ds-tile" href="bimanual_make_coffee.html"><img src="../_static/tasks/bimanual_make_coffee.webp" alt="Bimanual Make Coffee" loading="lazy"><div class="ds-tile-text"><b>Bimanual Make Coffee</b><small><code>bimanual_make_coffee</code></small></div></a>
<a class="ds-tile" href="bimanual_drill_to_point.html"><img src="../_static/tasks/bimanual_drill_to_point.webp" alt="Bimanual Drill to Point" loading="lazy"><div class="ds-tile-text"><b>Bimanual Drill to Point</b><small><code>bimanual_drill_to_point</code></small></div></a>
<a class="ds-tile" href="bimanual_fold_glasses.html"><img src="../_static/tasks/bimanual_fold_glasses.webp" alt="Bimanual Fold Glasses" loading="lazy"><div class="ds-tile-text"><b>Bimanual Fold Glasses</b><small><code>bimanual_fold_glasses</code></small></div></a>
</div>

```{toctree}
:hidden:
:maxdepth: 1

reach
lift
push
pick_place
stack
pick_place_mug
pick_place_pan
drill_to_point
pick_place_fruit
spray_graffiti
put_bread_toaster
make_coffee
tool_hang
pick_place_pan_platform
pick_place_duck
open_safe
stow_in_safe
pliers_in_jewelry_box
close_window_spray
bimanual_reach
bimanual_lift
bimanual_push
bimanual_pick_place
bimanual_stack
bimanual_stack_mid_air
bimanual_pick_place_mug
bimanual_pick_place_pan
bimanual_pick_place_pot
bimanual_make_coffee
bimanual_drill_to_point
bimanual_fold_glasses
```
