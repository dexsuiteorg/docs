.. include:: ../../_shared_nav.rst

Available Robots
================

This page lists the robots, manipulators, and grippers available by default in DexSuite.

.. list-table:: Default Modular Manipulators (Arms)
   :widths: 20 40 40
   :header-rows: 1

   * - Name (Key)
     - Description
     - DOF
   * - ``franka``
     - Franka Emika Panda research arm (manipulator only).
     - 7
   * - ``ur5``
     - Universal Robots UR-5 arm (manipulator only).
     - 6

.. list-table:: Default Modular Grippers
   :widths: 20 40 40
   :header-rows: 1

   * - Name (Key)
     - Description
     - DOF
   * - ``robotiq``
     - Robotiq 2F-85 parallel gripper.
     - 1
   * - ``gripper1``
     - A simple parallel gripper that opens and closes.
     - 1

.. list-table:: Default Integrated Robots (Arm + Gripper)
   :widths: 20 40 40
   :header-rows: 1

   * - Name (Key)
     - Description
     - DOF
   * - ``franka_with_gripper``
     - Franka Emika Panda arm with its native 2-finger gripper.
     - 7 (Arm) + 1 (Gripper)