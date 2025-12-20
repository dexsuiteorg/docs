Bimanual Lift
=============

Task key: ``bimanual_lift``.

``bimanual_lift`` is a two-arm baseline task. Each arm must lift its own cube
to a target height above the spawn position.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Lift both cubes to the goal height and keep them aligned with their goal markers.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_lift",
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

- ``cube_left`` / ``cube_right``: rigid cubes spawned on opposite sides.
- ``goal_left`` / ``goal_right``: fixed, non-colliding spheres above each cube.

Extra Observations
------------------

Bimanual-lift adds (under ``obs["state"]["other"]``):

- ``cube_left_pos``, ``cube_right_pos`` (each shape ``(n_envs, 3)``)
- ``cube_left_quat``, ``cube_right_quat`` (each shape ``(n_envs, 4)``, wxyz)
- ``target_left_pos``, ``target_right_pos`` (each shape ``(n_envs, 3)``)

Termination
-----------

- **Success:** both cubes reach the target height and are close to their targets in XY.
- **Failure:** either TCP leaves the workspace AABB.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 600`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/baselines/bimanual_lift.py``
