Integrated Robots
=================

.. _integrated_robots:

Integrated robots are manipulators that already include a gripper in the same
URDF/MJCF asset. In DexSuite, these show up as a *manipulator key* that has a
built-in gripper (for example ``franka_with_gripper``).

DexSuite still exposes a separate gripper controller by creating a small
"hand proxy" that points at the gripper joint indices inside the integrated
entity.

.. image:: ../../_static/placeholder_robot.svg
   :width: 420

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "reach",
       manipulator="franka_with_gripper",
       gripper=None,  # integrated gripper
       arm_control="osc_pose",
       gripper_control="joint_position",
       render_mode="human",
   )

   obs, info = env.reset()

Notes
-----

* For integrated manipulators, you typically set ``gripper=None`` (or omit it).
* The total ``DoF`` shown on :doc:`Available Robots <../../catalog/available_robots>` includes
  both the arm and the built-in gripper.
