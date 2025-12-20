Bimanual Pick Place Pot
=======================

Task key: ``bimanual_pick_place_pot``.

``bimanual_pick_place_pot`` is a two-arm rigid-object task. A pot starts on a
hot plate and must be placed onto a kitchen mat.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Move the pot from the hot plate to the mat.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_pick_place_pot",
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

- ``pot``: rigid pot.
- ``hot_plate``: fixed hot plate.
- ``kitchen_mat``: fixed mat (visual) + collision box.
- ``pot_target_left`` / ``pot_target_right``: markers linked to the pot.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

This task is still being finalized. In the current code, reward and
success/failure checks are not enabled, so episodes typically end by horizon
truncation.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 2``
- ``HORIZON = 7000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/rigid/bimanual_pick_place_pot.py``
