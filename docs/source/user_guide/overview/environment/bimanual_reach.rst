Bimanual Reach
==============

Task key: ``bimanual_reach``.

``bimanual_reach`` is a two-arm baseline task. Each arm has its own target
sphere and the agent must move both TCPs to their targets.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Move both TCPs to their respective targets.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_reach",
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

- ``target_sphere_left``: fixed target marker for the left arm.
- ``target_sphere_right``: fixed target marker for the right arm.

Extra Observations
------------------

Bimanual-reach adds (under ``obs["state"]["other"]``):

- ``target_left_pos``, ``target_right_pos`` (each shape ``(n_envs, 3)``)
- ``target_left_quat``, ``target_right_quat`` (each shape ``(n_envs, 4)``, wxyz)

Termination
-----------

- **Success:** both TCPs are within 3 cm of their targets.
- **Failure:** either TCP leaves the workspace AABB.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 300`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/baselines/bimanual_reach.py``
