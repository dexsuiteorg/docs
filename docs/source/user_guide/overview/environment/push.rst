Push
====

Task key: ``push``.

``push`` is a single-arm baseline task. A cube is spawned on the table along
with a goal marker, and the agent must push the cube into the goal region.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Push the cube to the goal marker while keeping it on the table.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "push",
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
- ``goal``: a fixed, non-colliding sphere placed near the cube.

Extra Observations
------------------

Push adds (under ``obs["state"]["other"]``):

- ``cube_pos`` (shape ``(n_envs, 3)``)
- ``cube_quat`` (shape ``(n_envs, 4)``, wxyz convention)
- ``goal_pos`` (shape ``(n_envs, 3)``)

Termination
-----------

- **Success:** cube center is within 3 cm of the goal marker.
- **Failure:** TCP leaves the workspace AABB, or the cube is lifted above a small threshold.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 200`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/baselines/push.py``
