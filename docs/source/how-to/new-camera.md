# Add a camera

<p class="ds-lede">Cameras are either presets in <code>dexsuite/config/cameras.yaml</code>, used by name, or option
objects passed for one run.</p>

## A static preset

Add an entry under `static:`. Position and target are in world coordinates, `res` is `[width, height]`:

```yaml
static:
  bench_left:
    pos: [0.6, 0.9, 0.7]
    lookat: [0.45, 0.0, 0.1]
    fov: 50
    res: [320, 240]
```

and use it by name:

```python
env = ds.make("lift", manipulator="franka", gripper="robotiq", cameras=["bench_left", "wrist"])
obs["cameras"]["bench_left"]["rgb"].shape     # (240, 320, 3)
```

## Wrist cameras

The dynamic preset `wrist_cam` rides on the end-effector's root link. Its pose comes from `default`, unless an entry
in `overrides` matches the end-effector key (checked first) or the arm key:

```yaml
dynamic:
  wrist_cam:
    fov: 60
    res: [224, 224]
    default:
      pos_offset: [0.0, 0.14, 0.0]
      quat_offset: [0.3466, -0.938, 0.0, 0.0]
    overrides:
      robotiq:
        pos_offset: [0.0, 0.14, 0.0]
        quat_offset: [0.3466, -0.938, 0.0, 0.0]
```

An override can also change `fov`, `res`, `near` and `far`, as the Sharpa entry does to match the real D405 camera.

## For one run

```python
cams = ds.CamerasOptions(
    static={"front": "front", "close": ds.StaticCamOptions(pos=(0.8, -0.3, 0.4), lookat=(0.45, 0.0, 0.05), fov=40)},
    dynamic={"wrist": "wrist_cam"},
    modalities=("rgb", "depth", "segmentation"),
)
env = ds.make("lift", manipulator="franka", gripper="robotiq", cameras=cams)
```

A string value refers to a preset, an options object defines the camera in place. See
[Observations](../concepts/observations.md#cameras) for the modalities and shapes.
