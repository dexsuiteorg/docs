# Teleoperation

<p class="ds-lede">Drive any robot from a keyboard, a SpaceMouse, a Vive tracker or a Manus glove, and record every
successful episode straight to a LeRobot dataset.</p>

```{raw} html
:file: ../_static/diagrams/teleop.svg
```

A device turns what the operator does into a pose for the hand and a command for the fingers. The arm's pose controller
follows the pose, the end-effector's joint controller takes the finger command, and the logger writes each step.
Because every robot takes the same kind of action, a device set up for one arm works for all of them.

| Device | Drives | Typical controller | Setup |
|---|---|---|---|
| Keyboard | hand pose, gripper open and close | `osc_pose` | none |
| SpaceMouse | hand pose, gripper | `osc_pose` | `pip install "dexsuite[spacemouse]"` |
| Vive tracker or controller | absolute hand pose | `osc_pose_abs_quat` | SteamVR, `pip install "dexsuite[vive]"` |
| Manus glove | finger joints, through GeoRT retargeting | `joint_position` (unnormalized) | Manus SDK, GeoRT, `pip install "dexsuite[manus]"` |

The Vive tracker on the wrist and the Manus glove on the hand together drive an arm and a dexterous hand at once; this
is how the human demonstrations in the [datasets](../data/index.md) were collected.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Devices
:link: devices
:link-type: doc
Each device, how to connect it and what it returns.
:::

:::{grid-item-card} Recording
:link: recording
:link-type: doc
The LeRobot logger, the collection scripts and uploading to Hugging Face.
:::
::::

```{toctree}
:hidden:

devices
recording
```
