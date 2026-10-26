# Installation

<p class="ds-lede">DexSuite is a Python package on top of the Genesis simulator. One <code>pip install</code> brings
every robot, every hand and the assets of every task.</p>

## Requirements

<dl class="ds-spec">
<dt>Python</dt><dd>3.10 or newer</dd>
<dt>Simulator</dt><dd>Genesis <code>genesis-world==0.4.3</code>, installed as a dependency</dd>
<dt>GPU</dt><dd>A CUDA GPU. Without one, Genesis falls back to the CPU, which is fine for a quick check but slow.</dd>
<dt>Display</dt><dd>Only for the interactive viewer. Headless machines render cameras throu## Install

```bash
python -m venv .venv && source .venv/bin/activate      # or conda, or uv venv
pip install dexsuite
```

This installs the core dependencies: PyTorch, Genesis, Mink with the `quadprog` solver (inverse kinematics for the
default arm controller), Gymnasium, NumPy, PyYAML, cattrs and pynput. The package carries every arm, hand and integrated
robot and the models of every task, about 90 MB.

## Install from source

To change the code, or for the prototype tasks and the full object library (the objects no task uses yet), install
the repository in editable mode:

```bash
git clone https://github.com/anashoussaini/Dexsuite.git
cd Dexsuite
pip install -e .
```

An editable install reads the models in place from the clone.

them in place.
```

## Optional extras

Install only what you use, or everything with `pip install "dexsuite[all]"`. From a clone, the same extras
install with `pip install -e ".[datasets]"` and so on.

| Extra | Installs | Needed for |
|---|---|---|
| `pip install "dexsuite[datasets]"` | LeRobot 0.4.4, `h5py` | [recording demonstrations](../teleop/recording.md), loading the datasets, HDF5 export for robomimic |
| `pip install "dexsuite[spacemouse]"` | `evdev` (Linux) or `hidapi` | [SpaceMouse](../teleop/devices.md#spacemouse) |
| `pip install "dexsuite[vive]"` | `openvr`, `pyzmq` | [Vive trackers and controllers](../teleop/devices.md#vive), over SteamVR or streamed from another machine |
| `pip install "dexsuite[manus]"` | `websockets` | [Manus glove](../teleop/devices.md#manus-glove) through GeoRT |
| `pip install "dexsuite[devices]"` | every device above | every teleoperation device |
| `pip install "dexsuite[all]"` | `datasets` and `devices` | everything |

## Check the install

```python
import dexsuite as ds

env = ds.make("reach", manipulator="franka", gripper="robotiq")
obs, info = env.reset(seed=0)
print(env.action_space.shape)          # (7,): 6 for the arm, 1 for the gripper
print(list(obs["state"]["gripper"]))   # ['qpos', 'qvel', 'qtorque', 'tcp_pos', 'tcp_quat']
```

The first `ds.make` on a machine compiles the Genesis kernels, which takes about a minute. They are cached, so later
runs start in seconds.

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
