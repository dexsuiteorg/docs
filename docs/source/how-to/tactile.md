# Tactile pads

<p class="ds-lede">Any end-effector link with a flat contact face can carry a tactile pad: a grid of taxels that turns
penetration into nearby objects into normal and friction forces.</p>

## Turn them on

Pads are declared on the model class. This is the UMI gripper:

```python
@register_gripper("umi")
class FrankaUmiTacticle(GripperModel):
    ...
    tactile: bool = True
    tactile_links: tuple[str, str] = ("left_elastomer", "right_elastomer")
    tactile_grid_size: tuple[int, int, int] = (12, 1, 32)     # rows, depth, columns
    tactile_point_distance: float = 0.002                       # taxel spacing, metres
```

| Field | Meaning |
|---|---|
| `tactile` | enables the pads for this model |
| `tactile_links` | the links that carry a pad, one pad per link |
| `tactile_grid_size` | taxels per pad as `(rows, depth, columns)`; 12 x 32 matches the FlexiTac sensor |
| `tactile_point_distance` | spacing between taxels |

Integrated robots use the same fields with a `builtin_` prefix (`builtin_tactile_links`, ...), as `aloha_tactile` does.
The pads are built with the robot; there is no switch in `ds.make`.

## Read them

```python
env = ds.make("pick_place", manipulator="franka", gripper="umi")
obs, info = env.reset(seed=0)
pad = obs["state"]["gripper"]["tactile"]["left_elastomer"]
pad["force_grid"]       # (12, 32) normal force per taxel
pad["force_norm"]       # total force on the pad
pad["contact"]          # 1 when touching
```

The full list of fields is on [Observations](../concepts/observations.md#tactile-pads). The LeRobot logger records them
like any other observation, which is how the scripted UMI datasets carry tactile readings.

## Watch them

`scripts/franka_umi_tactile.py` drives the UMI gripper from the keyboard and plots the pads live:

```bash
python scripts/franka_umi_tactile.py --task pick_place_pan --plot
```
