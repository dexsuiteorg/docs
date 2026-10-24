# Parallel environments

<p class="ds-lede">With <code>n_envs</code>, Genesis simulates many copies of the scene at once on the GPU. Every
tensor gets a leading batch dimension and every copy keeps its own episode.</p>

```python
import torch
import dexsuite as ds

env = ds.make("lift", manipulator="franka", gripper="robotiq", n_envs=256, cameras=None)
obs, info = env.reset(seed=0)

action = torch.zeros(256, env.action_space.shape[0])
obs, reward, terminated, truncated, info = env.step(action)
reward.shape                           # (256,)
obs["state"]["gripper"]["tcp_pos"].shape   # (256, 3)
```

The copies are laid out 3 m apart, so they never touch. A single action of shape `(D,)` is broadcast to every copy.

## Episodes per copy

Each copy counts its own steps. When a copy succeeds, fails or reaches the horizon, it is reset inside `step` and the
others keep going. `info["needs_reset"]` marks the copies that were reset on this step.

To reset some copies yourself:

```python
env.reset_env_idx([0, 5, 9], seed=1)
```

## What does not batch

A few tasks run with one copy only, because their scene holds a single texture or a stateful mechanism: Spray
Graffiti, Close Window and Spray, Open Safe and Stow in Safe. Their task pages say so.

## Speed

- Cameras are the expensive part. Use `cameras=None` for state-based training.
- `performance_mode=True` turns on Genesis performance mode. It is set once per process.
- `control_hz` trades control resolution for speed: fewer, longer steps cost less.
