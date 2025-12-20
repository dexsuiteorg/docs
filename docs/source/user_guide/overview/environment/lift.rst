Lift
====

Task key: ``lift``.

``lift`` is a single-arm baseline task. A cube is spawned inside the robot
workspace and the agent must lift it to a fixed target height.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Lift the cube until it reaches the goal height.
- Keep the cube's XY position close to the goal marker.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       render_mode="human",
   )

   obs, info = env.reset()
   obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

   env.close()

Task Entities
-------------

- ``cube``: a rigid cube that starts on the table.
- ``goal``: a fixed, non-colliding sphere placed above the cube spawn.

Observations
------------

Observations follow the DexSuite convention:

- ``obs["state"]`` is a nested dict of torch tensors (robot state + task state).
- ``obs["cameras"]`` is a dict of rendered camera outputs (if cameras are enabled).

Lift adds (under ``obs["state"]["other"]``):

- ``cube_pos`` (shape ``(n_envs, 3)``)
- ``cube_quat`` (shape ``(n_envs, 4)``, wxyz convention)
- ``target_pos`` (shape ``(n_envs, 3)``)

The base environment also adds:

- ``other["action"]`` and ``other["last_action"]`` (flat action tensors)

Actions
-------

DexSuite uses a single, flat action tensor:

- Single env: shape ``(D,)``
- Batched envs: shape ``(n_envs, D)``

``D`` depends on your robot + controller choices. Use ``env.action_space.shape``
to inspect it.

``env.step(...)`` accepts a torch tensor, a NumPy array, or a Python sequence.
Inputs are converted to a float32 torch tensor on the environment device.

Termination
-----------

- **Success:** cube reaches the target height (within tolerance) and its XY
  position is within 5 cm of the target.
- **Failure:** the tool center point (TCP) leaves the workspace AABB.
- **Truncation:** the episode reaches the horizon.

Simulation Settings
-------------------

The lift baseline uses:

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 600`` control steps

``SimOptions.control_hz`` controls the control frequency; physics steps run at
``SIM_DT`` with ``SUBSTEPS`` substeps per physics step.

Source
------

- ``Dexsuite/dexsuite/environments/single/baselines/lift.py``
