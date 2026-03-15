Bimanual Robots
===============

.. _bimanual_robots:

Bimanual robots are a configuration of two single-arm robots operating in the
same scene. Each side can be either modular or integrated, and the two robot
bases are placed using a layout preset.

.. image:: ../../_static/placeholder_robot.svg
   :width: 420

Quickstart (flat API)
---------------------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_reach",
       manipulator=("franka", "franka"),
       gripper=("robotiq", "robotiq"),
       layout="side_by_side",
       arm_control="osc_pose",
       gripper_control="joint_position",
       render_mode="human",
   )

   obs, info = env.reset()

Layouts
-------

Common layout presets:

* ``side_by_side``
* ``face_to_face``
* ``right_angle``

If you need full control over base poses, use ``RobotOptions`` with explicit
``PoseOptions``.
