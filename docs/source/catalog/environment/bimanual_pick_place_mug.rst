Bimanual Pick Place Mug
=======================

Task key: ``bimanual_pick_place_mug``.

``bimanual_pick_place_mug`` is a two-arm rigid-object task. A dish rack and a
mug are spawned, and the agent must place the mug into the rack.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Place the mug into the dish rack.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_pick_place_mug",
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

- ``rack``: dish rack.
- ``mug``: rigid mug.

Extra Observations
------------------

Bimanual pick-place-mug adds (under ``obs["state"]["other"]``):

- ``rack_pos``, ``mug_pos`` (each shape ``(n_envs, 3)``)
- ``rack_quat``, ``mug_quat`` (each shape ``(n_envs, 4)``, wxyz)
- ``mug_linear_vel``, ``mug_angular_vel`` (each shape ``(n_envs, 3)``)

Termination
-----------

- **Success:** mug is near the rack in XY, within a Z tolerance, and has low linear/angular velocity.
- **Failure:** none beyond horizon truncation.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 2``
- ``HORIZON = 40000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/rigid/bimanual_pick_place_mug.py``
