# Add an end-effector

<p class="ds-lede">An end-effector is a model file, a class with its joint range and tool point, and one adapter entry on
every arm that should carry it.</p>

## 1. The model class

Put the class and its model file under `dexsuite/models/grippers/my_hand/`:

```python
import torch

from dexsuite.core.components import GripperModel
from dexsuite.core.registry import register_gripper
from dexsuite.utils.models_utils import package_asset_path


@register_gripper("my_hand")
class MyHand(GripperModel):
    """Four-finger hand."""

    model_path: str = package_asset_path(__package__, "my_hand.xml")
    dof: int = 12
    root_link: str = "palm"
    tcp_pose = torch.tensor([0.0, 0.0, 0.12, 0.0, 0.0, 0.0])   # [x, y, z, roll, pitch, yaw] from root_link
    open_q = torch.zeros(12)
    closed_q = torch.full((12,), 1.2)
    home_q = open_q.clone()
```

| Field | Meaning |
|---|---|
| `dof` | actuated joints, the size of the end-effector's action |
| `root_link` | the link welded to the arm's mount; dynamic cameras attach here |
| `tcp_pose` | the tool point, reported as `tcp_pos` and moved by the pose controllers |
| `open_q`, `closed_q`, `home_q` | reference configurations |
| `q_lo`, `q_hi`, `kp`, `kv`, `force_range` | optional overrides of the model file |

For left and right versions, stack the decorators on the right hand (`@register_gripper("my_hand")` and
`@register_gripper("my_hand_right")`) and register the mirrored model as `my_hand_left`.

## 2. Mount it

Add an entry for `my_hand` to the adapter file of each arm that should carry it, for example
`dexsuite/models/manipulators/franka/franka_adapters.yaml` (format in [Add an arm](new-arm.md#3-the-adapters)).
Without an entry, `ds.make` raises `ValueError: Adapter missing`.

## 3. Optional: a wrist camera

Wrist cameras sit relative to the end-effector's root link. Add an offset under `wrist_cam.overrides` in
`dexsuite/config/cameras.yaml`:

```yaml
dynamic:
  wrist_cam:
    overrides:
      my_hand:
        pos_offset: [0.0, 0.0, -0.18]
        quat_offset: [-0.183, -0.683, 0.683, 0.183]
```

## Try it

```python
env = ds.make("lift", manipulator="franka", gripper="my_hand", render_mode="human")
env.reset(seed=0)
env.action_space.shape        # (6 + 12,)
```
