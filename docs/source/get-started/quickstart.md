# Quickstart

<p class="ds-lede">One call builds a task, a robot, its cameras and the simulator. The rest is the usual reset and step loop.</p>

## Make an environment

```python
import dexsuite as ds

env = ds.make(
    "lift",                     # the task
    manipulator="franka",       # the arm
    gripper="allegro",          # the end-effector
    render_mode="human",        # open the viewer; leave out on a headless machine
)
obs, info = env.reset(seed=0)
```

The task key, the arm and the end-effector are independent: `"lift"` runs just as well with
`manipulator="ur5", gripper="robotiq"`. The [task catalog](../tasks/index.md) and the [robot catalog](../robots/index.md)
list every key.

## Step it

```python
for _ in range(300):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

`step` returns PyTorch tensors. With the default single environment, observation tensors have no batch dimension
(`tcp_pos` is `(3,)`) and `terminated` and `truncated` have shape `(1,)`. With `n_envs > 1`, every tensor has a
leading `(n_envs,)` dimension.

```{note}
An environment that finishes an episode is reset inside `step`, and the observation you get back is already the first
one of the next episode. You do not need to call `reset` yourself when `terminated` or `truncated` is set.
```

`info` tells you why an episode ended:

```python
info["success"]       # the task's success check fired
info["failure"]       # the task's failure check fired
info["episode"]       # {"step": ..., "horizon": ...}
```

## The action

The action is one flat vector: the arm part first, then the end-effector part.

```python
env.action_space            # Box(-1.0, 1.0, (22,), float32) for the Franka with the Allegro hand
```

With the default controllers, the first 6 values move the hand: a position change and a rotation change, both in
[-1, 1]. The remaining 16 values are the Allegro joint targets, mapped from [-1, 1] to the joint limits. Other
controllers and the layout for two arms are on [Actions and controllers](../concepts/actions.md).

## The observation

```python
obs["state"]["manipulator"]   # qpos, qvel, qtorque, eef_pos, eef_quat
obs["state"]["gripper"]       # qpos, qvel, qtorque, tcp_pos, tcp_quat
obs["state"]["other"]         # task values (object poses, goals) and the last action
obs["cameras"]["front"]["rgb"]   # uint8 image, 224 x 224 x 3
obs["cameras"]["wrist"]["rgb"]   # the camera on the end-effector
```

Quaternions are `(w, x, y, z)`. Each task page lists what it adds under `obs["state"]["other"]`, and
[Observations](../concepts/observations.md) covers depth, segmentation and tactile pads.

## Drive it yourself

The interactive builder asks for a task and a robot, then lets you teleoperate the result. From the repository root:

```bash
python -m scripts.interactive_builder --input keyboard
```

| Keys | Moves the hand |
|---|---|
| ↑ ↓ | forward, back |
| ← → | left, right |
| U J | up, down |
| B M, N H, G V | roll, pitch, yaw |
| P O | close, open the end-effector |
| R | reset |

A SpaceMouse or a Vive tracker works the same way, see [Builders](builders.md) and [Teleoperation](../teleop/index.md).

## Many environments at once

`n_envs` builds several copies of the same scene in one simulator. Every tensor then gets a leading batch dimension.

```python
env = ds.make("lift", manipulator="franka", gripper="robotiq", n_envs=64)
obs, info = env.reset(seed=0)
obs["state"]["gripper"]["tcp_pos"].shape     # (64, 3)
```

[Parallel environments](../concepts/parallel.md) explains batching and partial resets.
