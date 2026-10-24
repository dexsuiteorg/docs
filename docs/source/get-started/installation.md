# Installation

<p class="ds-lede">DexSuite is a Python package on top of the Genesis simulator. Install it from source so every robot
and object asset comes with it.</p>

## Requirements

<dl class="ds-spec">
<dt>Python</dt><dd>3.10 or newer</dd>
<dt>Simulator</dt><dd>Genesis <code>genesis-world==0.4.3</code>, installed as a dependency</dd>
<dt>GPU</dt><dd>A CUDA GPU. Without one, Genesis falls back to the CPU, which is fine for a quick check but slow.</dd>
<dt>Display</dt><dd>Only for the interactive viewer. Headless machines render cameras through EGL.</dd>
</dl>

## Install from source

```bash
git clone https://github.com/dexsuiteorg/dexsuite.git
cd dexsuite
python -m venv .venv && source .venv/bin/activate      # or conda, or uv venv
pip install -e .
pip install quadprog                                     # QP solver used by the default arm controller
```

`pip install -e .` installs the core dependencies: PyTorch, Genesis, Mink (inverse kinematics), Gymnasium, NumPy,
PyYAML, cattrs and pynput.

```{important}
The default arm controller, `osc_pose`, solves its inverse kinematics with `quadprog`. Mink does not install a QP
solver on its own, so add `quadprog` as above, otherwise the first `step` fails with a missing-solver error.
```

## Optional extras

Install only what you use.

| Extra | Installs | Needed for |
|---|---|---|
| `pip install -e ".[spacemouse]"` | `evdev` (Linux) or `hidapi` | [SpaceMouse](../teleop/devices.md#spacemouse) |
| `pip install -e ".[vive]"` | `openvr` | [Vive trackers and controllers](../teleop/devices.md#vive) over SteamVR |
| `pip install -e ".[manus]"` | `websockets` | [Manus glove](../teleop/devices.md#manus-glove) through GeoRT |
| `pip install -e ".[devices]"` | all of the above | every teleoperation device |
| `pip install -e ".[datasets]"` | `h5py` | HDF5 export for robomimic |
| `pip install lerobot` | LeRobot | recording demonstrations and loading the datasets |
| `pip install pyzmq` | ZeroMQ | Vive poses streamed from another machine |

## Check the install

```python
import dexsuite as ds

env = ds.make("reach", manipulator="franka", gripper="robotiq")
obs, info = env.reset(seed=0)
print(env.action_space.shape)          # (7,): 6 for the arm, 1 for the gripper
print(list(obs["state"]["gripper"]))   # ['qpos', 'qvel', 'qtorque', 'tcp_pos', 'tcp_quat']
```

The first `ds.make` in a process initializes Genesis and compiles its kernels, which takes a little while. Later calls
reuse it.

## Headless machines

Cameras render offscreen through EGL. Set the platform before importing DexSuite:

```bash
export PYOPENGL_PLATFORM=egl
python my_script.py
```

Keep `render_mode=None` (the default) on a headless machine. `render_mode="human"` opens the Genesis viewer and needs
a display.

## Choosing the device

DexSuite runs on CUDA when PyTorch sees a GPU and on the CPU otherwise. To pick explicitly, call `ds.set_device`
before the first `ds.make`:

```python
import dexsuite as ds

ds.set_device("cuda:1")
```

## Troubleshooting

`ValueError: Missing required 'manipulator' argument`
: `ds.make` needs a robot. Pass `manipulator=` and, for modular arms, `gripper=`, or a full `robot=ds.RobotOptions(...)`.

`ValueError: Modular manipulator 'FrankaArm' requires a gripper`
: Modular arms are built with an end-effector. Add `gripper="robotiq"` or any other [end-effector](../robots/end-effectors.md).

`RuntimeError` about the precision
: Genesis is initialized once per process. `precision` (`"32"` or `"64"`) cannot change after the first `ds.make`.

The viewer does not open
: Check that a display is available, or render cameras offscreen with `render_mode=None`.
