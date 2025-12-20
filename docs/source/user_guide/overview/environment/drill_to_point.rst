Drill To Point
==============

Task key: ``drill_to_point``.

``drill_to_point`` is a single-arm rigid-object task. A power drill and a wall
are spawned and the agent must bring the drill tip to a target point on the
wall.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Bring the drill tip close to the target point on the wall.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "drill_to_point",
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

- ``drill``: rigid power drill.
- ``drill_tip``: marker linked to the drill tip.
- ``wooden_wall``: rigid wall block.
- ``target``: marker linked to the wall.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

The success/failure logic for this task is still being finalized; by default,
episodes typically end by horizon truncation.

Notes
-----

- The repository currently contains multiple implementations registered under the same key; import order determines which one wins in the registry.

Simulation Settings
-------------------

The two in-tree variants use different horizons:

- ``HORIZON = 300`` (rigid variant)
- ``HORIZON = 30000`` (alternate variant)

Source
------

- ``Dexsuite/dexsuite/environments/single/rigid/drill_to_point.py``
- ``Dexsuite/dexsuite/environments/single/prototypes/drill_to_point.py``
