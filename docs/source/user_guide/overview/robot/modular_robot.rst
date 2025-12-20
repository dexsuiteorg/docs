Modular Robots
==============

.. _modular_robots:

Modular robots are built from two separate models:

* a manipulator (arm)
* a gripper (hand)

DexSuite mounts the gripper onto the manipulator at build time using an adapter
definition (a fixed pose offset).

.. image:: ../../../_static/placeholder_robot.svg
   :width: 420

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       render_mode="human",
   )

   obs, info = env.reset()

What happens under the hood
---------------------------

* DexSuite loads the manipulator model (for example ``franka``).
* DexSuite loads the gripper model (for example ``robotiq``).
* DexSuite looks up an adapter for that manipulator+gripper pair.
* The two simulation entities are linked together with a fixed mount.

If an adapter is missing, DexSuite raises a clear error listing which grippers
are available for that manipulator.
