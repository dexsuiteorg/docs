# FAQ

## Installing

**The first `step` fails because no QP solver is available.**
The default arm controller solves its inverse kinematics with `quadprog`, which Mink does not install. Run
`pip install quadprog`.

**Recording fails with `ModuleNotFoundError: lerobot`.**
`pip install lerobot`. The logger and the datasets use it, but `pip install -e .` does not pull it in.

**Some robots are missing after `pip install dexsuite`.**
Install from source with `pip install -e .`. The source checkout carries every robot and object asset.

## Making environments

**`ds.make("lift")` raises "Missing required 'manipulator' argument".**
A task needs a robot. Pass `manipulator=` and, for modular arms, `gripper=`.

**`ValueError: Adapter missing`.**
The arm has no adapter for that end-effector. The [compatibility table](../robots/compatibility.md) lists the pairs.

**A keyword I passed is rejected with `TypeError`.**
`ds.make` accepts a fixed set of arguments, listed in [Making environments](../concepts/make.md#arguments), so that
typos fail early.

**Changing `precision` raises `RuntimeError`.**
Genesis is initialized once per process. Start a new process for a different precision or performance mode.

## Running

**My episodes reset twice.**
`step` resets finished environments itself. Do not call `env.reset()` again after `terminated` or `truncated`.

**`env.render()` returns `None`.**
Without an argument it means `"human"`. Call `env.render("rgb_array")` for images, or read `obs["cameras"]`.

**The images are the wrong way round.**
Camera `res` is `(width, height)`; the image arrays are `(height, width, 3)`.

**The viewer does not open on a server.**
It needs a display. Use `render_mode=None` and `PYOPENGL_PLATFORM=egl` to render cameras offscreen.

**A task refuses `n_envs > 1`.**
Spray Graffiti, Close Window and Spray, Open Safe and Stow in Safe run one copy at a time; their pages say so.

## Speed

**How do I train faster?**
Turn cameras off (`cameras=None`) for state-based learning, raise `n_envs`, and keep `performance_mode=True`. Cameras
dominate the cost.
