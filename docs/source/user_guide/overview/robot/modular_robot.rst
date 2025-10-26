.. include:: ../../_shared_nav.rst

Modular Robots
================

.. _modular_robots:

Modular Robots are the most common and flexible robot type. They are defined as a collection of separate components that are "fused" together at runtime. This design allows for maximum reusability, as different grippers can be easily swapped and attached to different manipulators.

A Modular Robot is composed of three distinct parts.

Modular Manipulator
^^^^^^^^^^^^^^^^^^^^^
The arm itself, which does not include a gripper (e.g., a UR-5 or Franka arm).

(Coming Soon)

Gripper
^^^^^^^
The end-effector, defined in its own file (e.g., a Robotiq 2F-85).

(Coming Soon)

Gripper Mount
^^^^^^^^^^^^^^^
A realistic adapter piece (optional) that defines the precise attachment offset between the arm's wrist and the gripper's base. This can be defined as an invisible offset or as a visible shape (like a cylinder).

(Coming Soon)