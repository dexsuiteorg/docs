Bimanual Push
=============

Task key: ``bimanual_push``.

``bimanual_push`` is a two-arm baseline task. Each arm must push its own cube
to a nearby goal marker on the table plane.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Push both cubes to their goal markers while keeping them on the table.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_push",
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
- ``goal_left`` / ``goal_right``: fixed goal markers near each cube.

Extra Observations
------------------

Bimanual-push adds (under ``obs["state"]["other"]``):

- ``cube_left_pos``, ``cube_right_pos`` (each shape ``(n_envs, 3)``)
- ``cube_left_quat``, ``cube_right_quat`` (each shape ``(n_envs, 4)``, wxyz)
- ``goal_left_pos``, ``goal_right_pos`` (each shape ``(n_envs, 3)``)

Termination
-----------

- **Success:** both cubes are within 3 cm of their goals.
- **Failure:** either TCP leaves the workspace AABB, or either cube is lifted above a small threshold.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 450`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/baselines/bimanual_push.py``
