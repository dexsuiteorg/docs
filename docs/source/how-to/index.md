# How-to guides

<p class="ds-lede">Extend DexSuite with your own tasks, robots, cameras and sensors. Each guide ends with a working
<code>ds.make</code> call.</p>

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Add a task
:link: new-task
:link-type: doc
One class: the scene, the reset, the observations and the success check.
:::

:::{grid-item-card} Add an arm
:link: new-arm
:link-type: doc
A model class, an adapter file and a workspace box. Integrated arms included.
:::

:::{grid-item-card} Add an end-effector
:link: new-end-effector
:link-type: doc
A gripper or hand model, its tool point, and an adapter entry on each arm.
:::

:::{grid-item-card} Add a camera
:link: new-camera
:link-type: doc
Static presets, wrist-camera offsets per end-effector, and one-off cameras.
:::

:::{grid-item-card} Tactile pads
:link: tactile
:link-type: doc
Turn flat finger links into taxel grids and read them from the observation.
:::
::::

```{toctree}
:hidden:

new-task
new-arm
new-end-effector
new-camera
tactile
```
