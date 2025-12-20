Rotate Dice
===========

Task key: ``rotatedice``.

``rotatedice`` spawns a dice mesh and lets the robot interact with it.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Interact with the dice (reward/success is currently not defined).

Quickstart
----------

Task keys are case-insensitive; the underlying decorator uses ``"rotateDice"``,
but ``ds.make`` normalizes keys to lowercase.

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "rotatedice",
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

- ``dice``: rigid dice mesh.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

Success/reward logic is not implemented yet; episodes end by horizon truncation.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 2``
- ``HORIZON = 40000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/dice_rotate.py``
