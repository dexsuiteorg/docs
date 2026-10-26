# Devices

<p class="ds-lede">Every device returns the same dictionary from <code>get_action()</code>: a pose for the hand, a
gripper command, and the reset and button events.</p>

```python
act = device.get_action()
act["pose"]      # 6 values (keyboard, SpaceMouse) or 7: [x, y, z, qw, qx, qy, qz] (Vive)
act["gripper"]   # open and close command, when the device has one
act["reset"]     # the reset key or button
act["event"], act["meta"]
```

With `normalized=True`, pose values are clipped to [-1, 1], which is what the normalized `osc_pose` controller
expects.

## Keyboard

Needs nothing beyond `pynput`, installed with DexSuite.

```python
from dexsuite.devices import Keyboard

kb = Keyboard(controller="OSCPose", normalized=True, pos_sens=1.0, rot_sens=1.0, gripper=True)
```

| Keys | Action |
|---|---|
| ↑ ↓ | move along x |
| ← → | move along y |
| U J | move along z |
| B M, N H, G V | roll, pitch, yaw |
| P O | gripper |
| R | reset |

For AZERTY keyboards, pass `mapping=MAPPING_AZERTY` from `dexsuite.devices.keyboard`.

(spacemouse)=
## SpaceMouse

```bash
pip install "dexsuite[spacemouse]"     # evdev on Linux, hidapi elsewhere
```

```python
from dexsuite.devices import Spacemouse

sm = Spacemouse(path_or_ids=None, controller="OSCPose", normalized=True, gripper=True, deadzone=0.05)
```

`path_or_ids=None` finds the first SpaceMouse. To pick one, pass its evdev path (`"/dev/input/eventX"`) on Linux or
the HID path from `hid.enumerate()` elsewhere. The six axes move the hand, and the buttons drive the gripper and reset.
On Linux, the user needs read access to the device under `/dev/input`.

(vive)=
## Vive

Vive trackers and controllers give an absolute pose, which suits a hand that should follow the operator's wrist. Use
them with the `osc_pose_abs_quat` controller, unnormalized: the action is `[dx, dy, dz, qw, qx, qy, qz]` relative to
the pose at reset.

### Through SteamVR on the same machine

```bash
pip install "dexsuite[vive]"     # openvr
```

```python
from dexsuite.devices import ViveTracker

tracker = ViveTracker(tracker_id="tracker_1", transport="openvr", gripper=True, reset_key="r")
```

### Streamed from another machine

SteamVR often runs on a Windows or Linux machine next to the base stations, and the simulation runs elsewhere. Publish
the poses over ZeroMQ on the SteamVR machine:

```bash
python -m dexsuite.devices.vive_publisher_steamvr --bind tcp://*:5559 --topic vive.tracker --rate-hz 120
```

and subscribe in the simulation:

```python
from dexsuite.devices import ViveTrackerZMQClient

tracker = ViveTrackerZMQClient(endpoint="tcp://<steamvr-host>:5559", topic="vive.tracker")
```

Install the `vive` extra on both machines, it brings `openvr` and `pyzmq`. Controllers work the same way with `ViveController` and
`python -m dexsuite.devices.vive_controller_zmq_server` (port 5558, topic `vive.controller`); the trigger opens and
closes the gripper.

(manus-glove)=
## Manus glove

The glove drives the fingers of a dexterous hand. The Manus SDK streams the operator's hand, and
[GeoRT](https://github.com/facebookresearch/GeoRT) retargets it to the robot hand's joint angles. DexSuite reads those
joint angles from GeoRT over a WebSocket:

```bash
pip install "dexsuite[manus]"     # websockets
```

```python
from dexsuite.devices.manus_geort import ManusGeort

glove = ManusGeort(url="ws://127.0.0.1:8767", expected_dim=16)    # 16 joints: Allegro
q = glove.get_action()                                            # joint vector in the hand's order
```

GeoRT runs as a separate process. It sends `{"type": "qpos", "qpos": [...]}` messages, and for the 16-joint Allegro
hand DexSuite reorders them from GeoRT's joint order to the Allegro order.

Use the glove with the end-effector's `joint_position` controller, unnormalized, so the joint angles go straight to
the hand. Together with a Vive tracker on the wrist, see the
[Manus collection script](recording.md#manus-glove-and-vive-tracker).
