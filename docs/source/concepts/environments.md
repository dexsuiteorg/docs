# The environment loop

<p class="ds-lede">Every DexSuite environment is a Gymnasium environment with batched PyTorch tensors. A task fills in
its scene, its observations and its success check; everything else is shared.</p>

## reset

```python
obs, info = env.reset(seed=0)
```

`reset` seeds PyTorch with `seed` when given, resets every environment, places the robot at its home pose and lets
the task randomize its objects. It returns the first observation and an empty `info`. The `options` argument of the
Gymnasium signature is accepted and ignored.

## step

```python
obs, reward, terminated, truncated, info = env.step(action)
```

| Return | Shape | Meaning |
|---|---|---|
| `obs` | dict | the [observation](observations.md) after the step |
| `reward` | `(n_envs,)` | the task's reward, zero for tasks without one |
| `terminated` | `(n_envs,)` bool | success or failure |
| `truncated` | `(n_envs,)` bool | the horizon was reached |
| `info` | dict | `success`, `failure`, `terminated`, `truncated`, `needs_reset`, `episode` |

With a single environment, the observation tensors, `reward` and `info["success"]` have no batch dimension, while
`terminated` and `truncated` keep a dimension of 1. Wrap checks in `bool(...)` or `.any()` to handle both.

The action can be a PyTorch tensor, a NumPy array or a list. A single action of shape `(D,)` is used for every
environment. Each `step` advances the physics by one control period: at 20 Hz with a 10 ms physics step, that is five
physics steps.

## When an episode ends

An episode ends when the task's success check fires, its failure check fires, or the horizon is reached.

- **Success**: the task's goal condition, for example the cube within 3 cm of the goal. It is listed on every task page.
- **Failure**: an unrecoverable state, for example the hand leaving the workspace or the object falling off the table.
  Many tasks have none.
- **Horizon**: a fixed number of control steps per task (100 for Reach, 600 for Stack). It counts from the last reset.

```{important}
Finished environments are reset inside `step`. The `obs` returned alongside `terminated=True` is the first observation
of the next episode, and `info["needs_reset"]` tells you which environments were reset. Calling `env.reset()` yourself
afterwards resets them a second time.
```

## Seeding

`reset(seed=...)` and the constructor's `seed` call `torch.manual_seed`. Object placement uses PyTorch's generator, so
the same seed gives the same sequence of initial states. The robot always starts from the same home pose.

## Rendering

With `render_mode="human"`, the Genesis viewer opens and follows the simulation. To get images, read the cameras from
the observation, or call `env.render("rgb_array")`, which returns every camera's frames. `env.render()` with no
argument means `"human"` and returns `None`.

```python
frames = env.render("rgb_array")
```

## Workspace boxes

`env.get_workspace_aabbs()` returns the box each arm may reach into, in world coordinates. Tasks use it to place
objects and to detect a hand that has left its workspace. See [Workspaces and layouts](workspaces.md).

## Writing a task

A task subclasses `BaseEnv` and fills in a few hooks: the scene, the reset, the extra observations, the reward and the
success and failure checks. [Add a task](../how-to/new-task.md) walks through a complete one.
