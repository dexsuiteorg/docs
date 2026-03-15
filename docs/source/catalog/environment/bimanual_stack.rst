Bimanual Stack
==============

Task key: ``bimanual_stack``.

``bimanual_stack`` is a two-arm baseline stacking task. Three cubes are spawned
in the shared workspace and the goal is to stack them in order.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Stack three cubes: A (bottom), B (middle), C (top).

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_stack",
       manipulator=("franka", "franka"),
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

- ``cube_a`` / ``cube_b`` / ``cube_c``: rigid cubes to be stacked.

Extra Observations
------------------

Bimanual-stack adds (under ``obs["state"]["other"]``):

- ``cube_a_pos``, ``cube_b_pos``, ``cube_c_pos`` (each shape ``(n_envs, 3)``)
- ``cube_a_quat``, ``cube_b_quat``, ``cube_c_quat`` (each shape ``(n_envs, 4)``, wxyz)

Termination
-----------

- **Success:** cubes are vertically stacked with small XY and Z tolerances.
- **Failure:** any cube leaves the workspace AABB, or either TCP leaves the workspace AABB.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 800`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/baselines/bimanual_stack.py``
