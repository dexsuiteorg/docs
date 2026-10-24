# Observations

<p class="ds-lede">An observation is a nested dict of tensors: the robot's state, the task's state, and one entry per
camera.</p>

```{raw} html
:file: ../_static/diagrams/obs.svg
```

## State

```python
obs["state"]["manipulator"]   # the arm
obs["state"]["gripper"]       # the end-effector
obs["state"]["other"]         # the task, and the last actions
```

| Key | Meaning |
|---|---|
| `manipulator.qpos`, `qvel`, `qtorque` | arm joint positions, velocities, torques |
| `manipulator.eef_pos`, `eef_quat` | pose of the arm's last link in the world |
| `gripper.qpos`, `qvel`, `qtorque` | end-effector joint state |
| `gripper.tcp_pos`, `tcp_quat` | tool centre point in the world |
| `other.*` | what the task adds, for example `cube_pos`, `goal_pos`; listed on each task page |
| `other.action`, `other.last_action` | the action just applied and the one before |

Positions are in metres in the world frame, and quaternions are `(w, x, y, z)`. For two arms, the robot part is split
by side:

```python
obs["state"]["left"]["manipulator"]["qpos"]
obs["state"]["right"]["gripper"]["tcp_pos"]
obs["state"]["other"]                   # shared task state
```

```{note}
For integrated robots, `manipulator.qpos` holds every joint of the robot, gripper included, and `gripper.qpos` holds
the gripper joints alone.
```

## Cameras

```python
obs["cameras"]["front"]["rgb"]      # (224, 224, 3) uint8
obs["cameras"]["wrist"]["depth"]    # (224, 224) float32, when depth is on
```

Static cameras sit at a fixed pose in the world. Dynamic cameras ride on the end-effector. By default there is one of
each, `front` and `wrist`.

| Modality | Shape | Type |
|---|---|---|
| `rgb` (always on) | `(H, W, 3)` | `uint8` |
| `depth` | `(H, W)` | `float32`, metres |
| `segmentation` | `(H, W)` | `int64` |
| `normal` | `(H, W, 3)` | `float32` |

With `n_envs > 1`, every image gets a leading batch dimension.

### Presets

Static presets from `dexsuite/config/cameras.yaml`: `front`, `overhead`, `right_side`, `left_side`,
`right_angled_front`, `left_angled_front`, `right_angled_back`, `left_angled_back`, plus `safe_front` and
`window_front` for the safe and window tasks. The dynamic preset `wrist_cam` places a camera on the end-effector, with
per-end-effector offsets in the same file. In the direct form, `"wrist"` means `wrist_cam` and every other name is a
static preset.

```python
env = ds.make("lift", manipulator="franka", gripper="robotiq",
              cameras=["front", "overhead", "wrist"], modalities=["rgb", "depth"])
```

For two arms, `wrist` becomes `left_wrist` and `right_wrist`. Use a `left_` or `right_` prefix to put a camera on one
side only.

### Custom cameras

```python
cams = ds.CamerasOptions(
    static={"side": ds.StaticCamOptions(pos=(0.5, -1.0, 0.6), lookat=(0.5, 0.0, 0.1), fov=50, res=(320, 240))},
    dynamic={"wrist": ds.DynamicCamOptions(pos_offset=(0.0, 0.05, 0.02), fov=70)},
    modalities=("rgb", "depth"),
)
env = ds.make("lift", manipulator="franka", gripper="robotiq", cameras=cams)
```

```{important}
`res` is `(width, height)`. Dynamic cameras attach to the end-effector's root link. `near` and `far` set the clipping
planes (0.1 and 20 m by default).
```

`camera_gui=True` opens a window per camera, and `camera_gui={"wrist": True}` opens one for a single camera.
[Add a camera](../how-to/new-camera.md) shows how to add a preset to `cameras.yaml`.

(tactile)=
## Tactile pads

Two end-effectors carry simulated tactile pads: the UMI tactile gripper (`franka_umi_tacticle`) and the tactile ALOHA
(`aloha_tactile`). Each finger has a flat pad with the layout of the FlexiTac sensor, a grid of 12 by 32 taxels at
2 mm spacing. Every taxel turns its penetration into nearby objects into a normal and a friction force.

Pads are on whenever the model has them. The readings are under `obs["state"]["gripper"]["tactile"]`:

```python
tac = obs["state"]["gripper"]["tactile"]
tac["left_elastomer"]["force_grid"]     # (12, 32) normal force per taxel
tac["left_elastomer"]["force_norm"]     # (1,) total force on the pad
tac["left_elastomer"]["contact"]        # (1,) any contact
tac["left_elastomer"]["points"]         # (P, 4) taxel positions and normalized force
```

| Key per pad | Meaning |
|---|---|
| `contact` | 1 when the pad touches something |
| `force`, `force_norm` | total contact force (3) and its magnitude |
| `pos`, `quat` | pad pose in the world |
| `points_raw` | `(P, 4)`: taxel position and normal force |
| `points` | the same, force normalized |
| `force_grid`, `force_grid_norm` | the force as a `rows x cols` image |

[Tactile pads](../how-to/tactile.md) shows how to add pads to another end-effector.
