# Add an arm

<p class="ds-lede">An arm is a model file, a small class that names its links and home pose, an adapter file for the
end-effectors it carries, and a workspace box.</p>

## 1. The files

```
dexsuite/models/manipulators/my_arm/
├── __init__.py
├── my_arm.py              # the model class
├── my_arm_adapters.yaml   # one entry per end-effector
└── assets/
    └── my_arm.xml         # MJCF or URDF, with its meshes and license
```

## 2. The model class

```python
import torch

from dexsuite.core.components import ModularManipulatorModel
from dexsuite.core.registry import register_manipulator
from dexsuite.utils.models_utils import package_asset_path


@register_manipulator("my_arm")
class MyArm(ModularManipulatorModel):
    """Six-joint arm without a hand."""

    model_path: str = package_asset_path(__package__, "my_arm.xml")
    dof: int = 6
    root_link: str = "base_link"        # fixed to the world at the base pose
    end_link: str = "flange"            # where end-effectors attach
    home_q: torch.Tensor = torch.tensor([0.0, -1.57, 1.57, -1.57, -1.57, 0.0])
```

The base class also takes `kp`, `kv`, `force_range`, `q_lo`, `q_hi` and `control_dofs_index` when the model file's
values are not what you want.

## 3. The adapters

`my_arm_adapters.yaml` has one entry per end-effector key. Each entry places a mount piece on `end_link` and the
end-effector on the mount, positions in metres and quaternions `(w, x, y, z)`:

```yaml
robotiq:
  mount_type : cylinder            # invisible, cylinder, box or mesh
  mount_pos  : [0.0, 0.0, 0.0]
  mount_quat : [1.0, 0.0, 0.0, 0.0]
  geometry   :
    radius : 0.035
    height : 0.01
  gripper_pos  : [0.0, 0.0, 0.005]
  gripper_quat : [1.0, 0.0, 0.0, 0.0]
```

The end-effector's approach axis has to line up with the flange's outward axis. Check every entry in the viewer before
relying on it: a wrong `mount_quat` builds without error and only shows as a hand pointing the wrong way.

## 4. The workspace box

Add the arm to `dexsuite/config/workspaces.yaml`, in its base frame:

```yaml
my_arm:
  min: [0.15, -0.45, -0.1]
  max: [0.60, 0.45, 0.55]
```

Tasks place objects inside this box, so it should be the region the arm reaches comfortably.

## 5. Optional

- **Two-arm layouts**: `dexsuite/config/layouts/my_arm.yaml`, otherwise `defaults.yaml` is used.
- **Wrist camera**: an entry under `wrist_cam.overrides.my_arm` in `dexsuite/config/cameras.yaml`.

## Try it

```python
env = ds.make("reach", manipulator="my_arm", gripper="robotiq", render_mode="human")
env.reset(seed=0)
```

## Integrated arms

An arm with its own gripper derives from `IntegratedManipulatorModel` instead and declares the gripper part:

```python
@register_manipulator("my_arm_with_gripper")
class MyArmWithGripper(IntegratedManipulatorModel):
    model_path = package_asset_path(__package__, "my_arm_with_gripper.xml")
    dof = 7                                  # arm + gripper joints
    control_dofs_index = [0, 1, 2, 3, 4, 5]  # the arm joints
    root_link = "base_link"
    end_link = "gripper_link"
    home_q = torch.tensor([0.0, -1.57, 1.57, -1.57, -1.57, 0.0])
    builtin_gripper_dof = 1
    builtin_gripper_control_dofs_index = [6]
    builtin_gripper_root_link = "gripper_link"
    builtin_gripper_q_lo = torch.tensor([0.0])
    builtin_gripper_q_hi = torch.tensor([0.04])
    builtin_gripper_home_q = torch.tensor([0.04])
    builtin_gripper_tcp_pose = torch.tensor([0.0, 0.0, 0.10, 0.0, 0.0, 0.0])
```

Integrated arms need no adapter file. `so_100.py` and `gen3_lite.py` are compact examples.
