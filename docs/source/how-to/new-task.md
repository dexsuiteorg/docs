# Add a task

<p class="ds-lede">A task is one class. It adds its objects to the scene, places them at every reset, reports their
state, and says when the episode succeeds or fails. The robot, the cameras and the loop come from <code>BaseEnv</code>.</p>

This guide builds **Tap Cube**: touch the top of a cube with the tool point, with any arm and end-effector.

## 1. The class

Create `dexsuite/environments/single/rigid/tap_cube.py`:

```python
"""Touch the top of a cube with the tool point."""

from __future__ import annotations

import genesis as gs
import torch

from dexsuite.core.registry import register_env
from dexsuite.environments.base_env import BaseEnv
from dexsuite.utils.randomizers import sample_in_aabb_center_xy_band

SIM_DT = 0.01        # physics step, seconds
SUBSTEPS = 1
HORIZON = 200        # control steps per episode
CUBE = 0.05          # cube edge, metres
TOUCH = 0.02         # success distance, metres


@register_env("tap_cube")
class TapCubeEnv(BaseEnv):
    """Touch the top face of a cube."""

    def __init__(self, *, robot=None, cameras=None, sim=None, render_mode=None, seed=None, **scene_kw):
        super().__init__(robot_options=robot, cameras_options=cameras, sim_options=sim,
                         render_mode=render_mode, seed=seed,
                         sim_dt=SIM_DT, substeps=SUBSTEPS, horizon=HORIZON, **scene_kw)

    def _setup_scene(self) -> None:
        """Add the task's entities. Called once, before the scene is built."""
        self.cube = self.scene.add_entity(
            gs.morphs.Box(size=(CUBE, CUBE, CUBE)),
            material=gs.materials.Rigid(),
            surface=gs.surfaces.Default(color=(0.16, 0.61, 0.89)),
        )

    def _on_episode_start(self, envs_idx) -> None:
        """Place the objects. envs_idx is None for every environment, or the ones being reset."""
        pos = sample_in_aabb_center_xy_band(self.world_aabb, band_xy=(0.10, 0.20), z=CUBE / 2,
                                            env_idx=envs_idx, mode="square")
        self.cube.set_pos(pos, envs_idx=envs_idx)

    def _get_extra_obs(self) -> dict[str, torch.Tensor]:
        """Task state, added under obs["state"]["other"]."""
        top = self.cube.get_pos() + torch.tensor([0.0, 0.0, CUBE / 2], device=self.cube.get_pos().device)
        return {"cube_pos": self.cube.get_pos(), "cube_top": top}

    def _compute_reward(self, obs) -> torch.Tensor:
        d = torch.linalg.norm(obs["state"]["gripper"]["tcp_pos"] - obs["state"]["other"]["cube_top"], dim=-1)
        return -d

    def _is_success(self, obs) -> torch.Tensor:
        d = torch.linalg.norm(obs["state"]["gripper"]["tcp_pos"] - obs["state"]["other"]["cube_top"], dim=-1)
        return d < TOUCH

    def _is_failure(self, obs) -> torch.Tensor:
        return self._is_tcp_outside_workspace(obs)
```

## 2. Run it

```python
import dexsuite as ds

env = ds.make("tap_cube", manipulator="franka", gripper="robotiq", render_mode="human")
obs, info = env.reset(seed=0)
obs["state"]["other"]["cube_top"]
```

Files under `dexsuite/environments/` are imported when `dexsuite` is imported, so the decorator registers the task.
A task defined elsewhere is registered when its module is imported, so import it before `ds.make`.

## The hooks

| Hook | Called | Returns |
|---|---|---|
| `_setup_scene()` | once, before the scene is built | nothing; add entities with `self.scene.add_entity` |
| `_on_episode_start(envs_idx)` | at every reset | nothing; place objects for `envs_idx` |
| `_get_extra_obs()` | every step | dict of tensors with a leading `n_envs` dimension |
| `_compute_reward(obs)` | every step | `(n_envs,)` tensor; zeros if not overridden |
| `_is_success(obs)` | every step | `(n_envs,)` bool tensor |
| `_is_failure(obs)` | every step | `(n_envs,)` bool tensor; never fails if not overridden |
| `_step()` | every control step | optional per-step logic, such as a mechanism |

## Rules that keep a task portable

- **Name `robot`, `cameras` and `sim` in the constructor.** `ds.make` passes only the arguments the constructor
  declares.
- **Sample inside `self.world_aabb`.** It is the arm's workspace box in world coordinates, so the task fits every arm.
  The helpers in `dexsuite.utils.randomizers` sample boxes, discs and non-overlapping sets of objects.
- **Respect `envs_idx`.** With `n_envs > 1`, only the environments being reset should move.
- **Return batched tensors.** Every observation and check has a leading `n_envs` dimension.
- **Use `(w, x, y, z)` quaternions**, as the rest of DexSuite does.
- **Read the robot through the observation**, never through a particular model's link names, so the task works with
  every end-effector.

## Two arms

Two-arm tasks live in `dexsuite/environments/bimanual/`. The robot state is under `obs["state"]["left"]` and
`obs["state"]["right"]`, and `self.get_workspace_aabbs()` gives each side's box. `bimanual_reach.py` is the smallest
example.

## Document it

Add an entry to `tools/catalog_data.py` in the docs repository and run `tools/build_catalog.py`. The task gets a page,
a tile in the catalog and, after `tools/render_tasks.py`, a render.
