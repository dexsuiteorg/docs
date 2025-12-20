Pick And Place
==============

Task key: ``pick_place``.

``pick_place`` is a single-arm baseline task. A cube and a goal marker are
spawned and the agent must pick the cube and place it near the goal.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Pick the cube and place it at the goal marker.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "pick_place",
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

- ``cube``: a rigid cube spawned near the workspace center.
- ``goal``: a fixed, non-colliding sphere spawned in a reachable quadrant.

Extra Observations
------------------

Pick-and-place adds (under ``obs["state"]["other"]``):

- ``cube_pos`` (shape ``(n_envs, 3)``)
- ``cube_quat`` (shape ``(n_envs, 4)``, wxyz convention)
- ``goal_pos`` (shape ``(n_envs, 3)``)

Termination
-----------

- **Success:** cube center is within 3 cm of the goal marker.
- **Failure:** TCP leaves the workspace AABB.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 200`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/baselines/pick_place.py``
