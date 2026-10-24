# Making environments

<p class="ds-lede"><code>ds.make(task, **kwargs)</code> looks up the task, builds the robot, the cameras and the
simulator from the arguments, and returns the environment.</p>

```{raw} html
:file: ../_static/diagrams/make.svg
```

There are two ways to describe what to build. Use the direct form for one arm and default cameras, and the options form
when you need two arms, custom cameras or a non-default layout. The two cannot be mixed for the same part: passing both
`robot=` and `manipulator=` raises an error.

## Direct form

```python
import dexsuite as ds

env = ds.make(
    "pick_place",
    manipulator="ur5",
    gripper="robotiq",
    arm_control="osc_pose",
    gripper_control="joint_position",
    cameras=["front", "wrist"],
    modalities=["rgb", "depth"],
    control_hz=20,
    n_envs=1,
)
```

For two arms, give each side as a pair, left first:

```python
env = ds.make("bimanual_lift", manipulator=("franka", "franka"), gripper=("allegro_left", "allegro_right"))
```

A single `gripper` string is used for both sides.

## Options form

```python
robot = ds.RobotOptions(
    single=ds.ArmOptions(
        manipulator="ur5",
        gripper="robotiq",
        manipulator_controller=ds.ControllerOptions(name="osc_pose", config={"lin_scale": 0.5}),
    )
)
cameras = ds.CamerasOptions(
    static={"front": "front", "top": ds.StaticCamOptions(pos=(1.2, 0.0, 1.0), lookat=(0.4, 0.0, 0.0))},
    dynamic={"wrist": "wrist_cam"},
    modalities=("rgb", "depth"),
)
sim = ds.SimOptions(control_hz=20, n_envs=4)

env = ds.make("pick_place", robot=robot, cameras=cameras, sim=sim)
```

The option classes are documented field by field in the [reference](../reference/options.md).

## Arguments

| Argument | Type | Meaning |
|---|---|---|
| `task` | `str` | Task key, case-insensitive. An unknown key raises `ValueError` with the list of tasks. |
| `manipulator` | `str` or pair | Arm key. Required unless `robot=` is given. |
| `gripper` | `str`, `None` or pair | End-effector key. Required for modular arms, left out for integrated robots. |
| `arm_control` | `str` | Arm controller, default `osc_pose`. See [controllers](actions.md#controllers). |
| `gripper_control` | `str` | End-effector controller, default `joint_position`. |
| `robot` | `RobotOptions` | Full robot description, replaces the four arguments above. |
| `layout` | `str` or `LayoutOptions` | Placement of two arms: `side_by_side`, `face_to_face` or `right_angle`. |
| `cameras` | names, `CamerasOptions` or `None` | Camera names (`"front"`, `"wrist"`, any preset), full options, or `None` for no cameras. |
| `modalities` | names | `rgb` (always on), `depth`, `segmentation`, `normal`. Only with camera names. |
| `camera_gui` | `bool` or dict | Open a window per camera, or per named camera. |
| `control_hz` | `int` | Control rate, default 20. |
| `n_envs` | `int` | Number of parallel copies, default 1. |
| `performance_mode` | `bool` | Genesis performance mode. |
| `sim` | `SimOptions` | Full simulator options, replaces the three above and adds `physics_substeps` and `precision`. |
| `render_mode` | `"human"`, `"rgb_array"` or `None` | `"human"` opens the viewer. |

Any other keyword raises `TypeError`, so a typo never passes silently.

## Defaults

| Part | Default |
|---|---|
| Robot | one arm. In the options form, `ArmOptions()` is a Franka with a Robotiq 2F-85. |
| Arm controller | `osc_pose` |
| End-effector controller | `joint_position` |
| Cameras | a static `front` camera and a `wrist` camera on the end-effector, RGB, 224 x 224 |
| Simulator | 20 Hz control, one environment, 32-bit precision |
| Layout for two arms | `side_by_side` |

```{note}
In the direct form, a missing `gripper` means no end-effector, which only integrated robots accept. Name the
end-effector for modular arms.
```

## Genesis is initialized once

The first `ds.make` in a process starts Genesis with the backend (GPU when available), the precision and the
performance mode of that call. Later calls reuse it: a different `precision` raises `RuntimeError`, and a different
`performance_mode` has no effect. Start a new process to change them.

## Task-specific settings

`ds.make` only passes the arguments above. Settings that belong to one task, like the toaster slot geometry, are read
from environment variables and listed on the task page.
