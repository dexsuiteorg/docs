Bimanual Pick And Place
=======================

Task key: ``bimanual_pick_place``.

``bimanual_pick_place`` is a two-arm baseline task. Each arm must pick its own
cube and place it near a corresponding goal marker.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Pick and place both cubes to their respective goal markers.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_pick_place",
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

- ``cube_left`` / ``cube_right``: rigid cubes to place.
- ``goal_left`` / ``goal_right``: fixed goal markers for each cube.

Extra Observations
------------------

Bimanual pick-and-place adds (under ``obs["state"]["other"]``):

- ``cube_left_pos``, ``cube_right_pos`` (each shape ``(n_envs, 3)``)
- ``cube_left_quat``, ``cube_right_quat`` (each shape ``(n_envs, 4)``, wxyz)
- ``goal_left_pos``, ``goal_right_pos`` (each shape ``(n_envs, 3)``)

Termination
-----------

- **Success:** both cubes are within 3 cm of their respective goals.
- **Failure:** either TCP leaves the workspace AABB.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 200`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/baselines/bimanual_pick_place.py``
