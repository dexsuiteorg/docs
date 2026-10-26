# FAQ

## Installing

**Recording fails with `ModuleNotFoundError: lerobot`.**
Install the datasets extra, `pip install "dexsuite[datasets]"`. It pins LeRobot 0.4.4: the logger relies on that version's
dataset layout, and LeRobot 0.6 changed it.

**Saving an episode fails with `TypeError: only 0-dimensional arrays can be converted to Python scalars`.**
NumPy 2.4 refuses what LeRobot 0.4.4 hands to `datasets` when it writes an episode. The datasets extra pins
`numpy<2.4`; reinstall it with `pip install "dexsuite[datasets]"`.

**A prototype task or an object model is missing after `pip install dexsuite`.**
The package ships every robot and the assets of every task. The prototype tasks and the objects no task uses yet come
with the repository: [install from source](../get-started/installation.md#install-from-source) with `pip install -e .`.

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
