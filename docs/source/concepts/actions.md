# Actions and controllers

<p class="ds-lede">The action is one flat vector. Each part of the robot owns a slice of it, and each slice goes
through that part's controller.</p>

```{raw} html
:file: ../_static/diagrams/action.svg
```

## Layout

| Robot | Layout |
|---|---|
| One arm | `[arm | end-effector]` |
| Two arms | `[left arm | left end-effector | right arm | right end-effector]` |
| Integrated robot | `[arm | built-in gripper]` |
| Floating wrist | `[wrist pose | hand]` |

The arm slice has the controller's size (6 for `osc_pose`), and the end-effector slice has one value per actuated joint
(1 for the Robotiq 2F-85, 16 for the Allegro hand, 22 for the Sharpa hand). `env.action_space` is the concatenated box.

To see the exact slices of a robot:

```python
for seg in env.robot._layout.segments:
    print(seg.name, seg.start, seg.stop, seg.ctrl)
```

The same layout is saved with every recorded dataset in `meta/action_layout.json`.

## Controllers

Choose them with `arm_control=` and `gripper_control=` in the direct form, or `ControllerOptions(name=..., config=...)`
in the options form. Defaults come from `dexsuite/config/controllers.yaml`, and any key you pass overrides them.

| Controller | Size | Input |
|---|---|---|
| `osc_pose` | 6 | Change of hand pose per step: `[dx, dy, dz, droll, dpitch, dyaw]` in [-1, 1], scaled by `lin_scale` (0.7) and `ang_scale` (0.12). The default for arms. |
| `osc_pose_abs` | 6 | Hand pose offset from the pose at reset, in [-1, 1], scaled by `lin_range` and `ang_range`. |
| `osc_pose_abs_quat` | 7 | Hand pose offset `[dx, dy, dz, qw, qx, qy, qz]` from the pose at reset, unnormalized. Used for teleoperation. |
| `ik_pose` | 6 | Absolute hand pose `[x, y, z, roll, pitch, yaw]`, solved by inverse kinematics each step. |
| `joint_position` | DoF | Joint targets. Normalized: [-1, 1] maps to the joint limits. The default for end-effectors. |
| `joint_velocity` | DoF | Joint velocities, scaled by `v_max`. |
| `joint_torque` | DoF | Joint torques, scaled by `tau_max`. |

End-effectors take joint controllers only. The pose controllers solve differential inverse kinematics with
[Mink](https://github.com/kevinzakka/mink) (a QP solved by `quadprog`); `backend="genesis_internal"` switches to the
Genesis solver.

```python
robot = ds.RobotOptions(single=ds.ArmOptions(
    manipulator="franka",
    gripper="allegro",
    manipulator_controller=ds.ControllerOptions(name="osc_pose", config={"lin_scale": 0.4, "ang_scale": 0.08}),
    gripper_controller=ds.ControllerOptions(name="joint_position", config={"normalized": False}),
))
env = ds.make("lift", robot=robot)
```

With `normalized: False`, joint targets are given in radians (or metres for prismatic joints) instead of [-1, 1].

## Control rate

`control_hz` (default 20) sets how often a new action is applied. The pose controllers' solver step (`mink_dt`, or
`ik_dt` for `ik_pose`) is set to one control period unless you pass it. Physics runs at the task's own step size
underneath, several physics steps per control step.
