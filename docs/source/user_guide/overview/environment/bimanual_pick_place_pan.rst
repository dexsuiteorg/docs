Bimanual Pick Place Pan
=======================

Task key: ``bimanual_pick_place_pan``.

``bimanual_pick_place_pan`` is a two-arm rigid-object task. A frying pan starts
on a hot plate and must be placed onto a kitchen mat.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Move the pan from the hot plate to the mat.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_pick_place_pan",
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

- ``hot_plate``: fixed hot plate (visual).
- ``kitchen_mat``: fixed mat (visual) + collision box.
- ``pan``: rigid pan to place.

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
- ``SUBSTEPS = 1``
- ``HORIZON = 700`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/rigid/bimanual_pick_place_pan.py``
