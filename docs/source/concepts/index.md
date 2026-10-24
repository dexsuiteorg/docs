# Concepts

<p class="ds-lede">What <code>ds.make</code> builds, what an environment returns, and how robots, controllers, cameras
and workspaces fit together.</p>

```{raw} html
:file: ../_static/diagrams/make.svg
```

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Making environments
:link: make
:link-type: doc
The two ways to call `ds.make`, every argument, and the option classes behind them.
:::

:::{grid-item-card} The environment loop
:link: environments
:link-type: doc
`reset`, `step`, termination, the horizon, automatic resets, seeding and rendering.
:::

:::{grid-item-card} Robots
:link: robots
:link-type: doc
Modular arms with an end-effector, integrated robots, the floating wrist, and two-arm setups.
:::

:::{grid-item-card} Actions and controllers
:link: actions
:link-type: doc
How the action vector is laid out and what each controller does with its part.
:::

:::{grid-item-card} Observations
:link: observations
:link-type: doc
Robot state, task state, cameras and their modalities, and tactile pads.
:::

:::{grid-item-card} Workspaces and layouts
:link: workspaces
:link-type: doc
Where each arm stands, the box it may reach into, and the presets for two arms.
:::

:::{grid-item-card} Parallel environments
:link: parallel
:link-type: doc
Many copies of a scene in one simulator, batched tensors and partial resets.
:::
::::

```{toctree}
:hidden:

make
environments
robots
actions
observations
workspaces
parallel
```
