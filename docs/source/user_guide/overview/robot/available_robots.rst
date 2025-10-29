.. include:: ../../_shared_nav.rst

Available Robots
================

This page lists the robots, manipulators, and grippers available by default in DexSuite.


.. list-table:: Default Robots
   :widths: 20 40 30 30
   :header-rows: 1

   * - Name
     - World
     - Description
     - DOF
   * - Gripper1
     - .. image:: ../../../source/_static/image1.jpg
          :width: 150
     - Simple parallel gripper that opens and closes.
     - 1
   * - Manipulator1
     - .. image:: ../../../source/_static/image1.jpg
          :width: 150
     - Robotic arm.
     - 6


.. list-table:: Default Modular Manipulators (Arms)
   :widths: 20 40 40 10
   :header-rows: 1

   * - Name (Key)
     - World
     - Description
     - DOF
   * - ``franka``
     - .. image:: ../../../source/_static/image1.jpg
     - Franka Emika Panda research arm (manipulator only).
     - 7
   * - ``franka_fr3``
     - .. image:: ../../../source/_static/image1.jpg
     - Franka Emika FR3 research arm (manipulator only).
     - 7
   * - ``gen3``
     - .. image:: ../../../source/_static/image1.jpg
     - Kinova Gen3 research arm (manipulator only).
     - 7
   * - ``gen3_lite``
     - .. image:: ../../../source/_static/image1.jpg
     - Kinova Gen3 Lite manipulator with integrated gripper.
     - 10
   * - ``kuka``
     - .. image:: ../../../source/_static/image1.jpg
     - Kuka LBR iiwa 14 arm (manipulator only).
     - 7
   * - ``link6``
     - .. image:: ../../../source/_static/image1.jpg
     - Link6 FR3 research arm (manipulator only).
     - 6
   * - ``so_100``
     - .. image:: ../../../source/_static/image1.jpg
     - SO Arm 100 with rotary single-jaw gripper.
     - 6
   * - ``trossen_vx250s``
     - .. image:: ../../../source/_static/image1.jpg
     - Trossen WX250S manipulator with integrated gripper.
     - 8
   * - ``trossen_vx300s``
     - .. image:: ../../../source/_static/image1.jpg
     - Trossen VX300S manipulator with integrated gripper.
     - 8
   * - ``ur10``
     - .. image:: ../../../source/_static/image1.jpg
     - Universal Robots UR-10e arm only (manipulator only).
     - 6
   * - ``ur5``
     - .. image:: ../../../source/_static/image1.jpg
     - Universal Robots UR-5e arm (manipulator only).
     - 6

.. list-table:: Default Modular Grippers
   :widths: 20 40 40 10
   :header-rows: 1

   * - Name (Key)
     - World
     - Description
     - DOF
   * - ``ability``
     - .. image:: ../../../source/_static/image1.jpg
     - Ability right hand gripper.
     - 6
   * - ``allegro``
     - .. image:: ../../../source/_static/image1.jpg
     - Allegro dexterous hand gripper.
     - 16
   * - ``barrett``
     - .. image:: ../../../source/_static/image1.jpg
     - Barette hand gripper.
     - 8
   * - ``dclaw``
     - .. image:: ../../../source/_static/image1.jpg
     - D claw gripper.
     - 9
   * - ``inspire``
     - .. image:: ../../../source/_static/image1.jpg
     - Inspire right hand gripper.
     - 6
   * - ``leap``
     - .. image:: ../../../source/_static/image1.jpg
     - Leap dexterous right hand gripper.
     - 16
   * - ``robotiq``
     - .. image:: ../../../source/_static/image1.jpg
     - Robotiq 2F-85 parallel gripper.
     - 1
   * - ``schunk``
     - .. image:: ../../../source/_static/image1.jpg
     - Schunk SVH right hand gripper.
     - 9
   * - ``shadow``
     - .. image:: ../../../source/_static/image1.jpg
     - Shadow right hand gripper.
     - 20
   * - ``umi``
     - .. image:: ../../../source/_static/image1.jpg
     - Umi gripper.
     - 1

.. .. list-table:: Default Integrated Robots (Arm + Gripper)
..    :widths: 20 40 40
..    :header-rows: 1

..    * - Name (Key)
..      - Description
..      - DOF
..    * - ``franka_with_gripper``
..      - Franka Emika Panda arm with its native 2-finger gripper.
..      - 7 (Arm) + 1 (Gripper)
