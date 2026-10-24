# Workspaces and layouts

<p class="ds-lede">Each arm stands at a base pose and reaches into a box in front of it. Tasks place their objects
inside that box, so the same task fits a small SO-100 and a long UR10e.</p>

## The workspace box

Every arm has an axis-aligned box in its own base frame, in `dexsuite/config/workspaces.yaml`:

```yaml
franka:
  min: [0.15, -0.5, -0.1]
  max: [0.65, 0.5, 0.6]
```

At build time the box is moved to the world with the arm's base pose (position and yaw) and stored on the environment.
Tasks sample object positions inside it, and many use it as a failure check: an episode fails when the hand leaves the
box.

```python
boxes = env.get_workspace_aabbs()
boxes["union"]           # the box for one arm, or the union of both
boxes["left"], boxes["right"], boxes["overlap"]   # for two arms
```

To change it for one run, pass your own box:

```python
arm = ds.ArmOptions(manipulator="franka", gripper="robotiq",
                    workspace=ds.AABBOptions(min=(0.2, -0.4, 0.0), max=(0.6, 0.4, 0.5)))
env = ds.make("lift", robot=ds.RobotOptions(single=arm))
```

(two-arms)=
## Two arms

A layout preset places the two bases. The presets are read from `dexsuite/config/layouts/<arm>.yaml`, with
`defaults.yaml` as the fallback.

| Preset | Left base | Right base |
|---|---|---|
| `side_by_side` (default) | y = +0.35 | y = −0.35 |
| `face_to_face` | (0.3, +0.7), facing −90° | (0.3, −0.7), facing +90° |
| `right_angle` | (0.2, +0.6), facing −45° | (0.2, −0.6), facing +45° |

```python
env = ds.make("bimanual_reach", manipulator=("franka", "franka"), gripper="robotiq", layout="face_to_face")
```

For full control, give each side a pose:

```python
layout = ds.LayoutOptions(left=ds.PoseOptions(pos=(0.0, 0.4, 0.0), yaw_rad=0.0),
                          right=ds.PoseOptions(pos=(0.0, -0.4, 0.0), yaw_rad=0.0))
robot = ds.RobotOptions(type_of_robot="bimanual",
                        left=ds.ArmOptions(manipulator="ur5", gripper="robotiq"),
                        right=ds.ArmOptions(manipulator="ur5", gripper="robotiq"),
                        layout=layout)
env = ds.make("bimanual_reach", robot=robot)
```

A pose takes a position and either a yaw angle or a full quaternion `(w, x, y, z)`. One arm always stands at the
origin; presets are for two arms only.

## Seeing them

`RobotOptions(visualize_aabb=True)` draws the workspace boxes in the viewer, and `visualize_tcp=True` marks the tool
centre point.
