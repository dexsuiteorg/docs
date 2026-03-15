Available Robots
================

This page lists the manipulators and grippers available by default in DexSuite.

Use these keys with ``ds.make(...)``:

* ``manipulator="<key>"`` selects a manipulator model.
* ``gripper="<key>"`` selects a gripper model (for modular manipulators).

.. list-table:: Manipulators (arm-only, modular)
   :widths: 18 32 40 10
   :header-rows: 1

   * - Name (Key)
     - Image
     - Notes
     - DoF
   * - ``franka``
     - .. image:: ../_static/franka_fr3_right45.png
          :width: 240
     - Franka Emika Panda arm (requires a separate gripper).
     - 7
   * - ``franka_fr3``
     - .. image:: ../_static/franka_fr3_right45.png
          :width: 240
     - Franka Emika FR3 arm (requires a separate gripper).
     - 7
   * - ``gen3``
     - .. image:: ../_static/gen3_right45.png
          :width: 240
     - Kinova Gen3 arm (requires a separate gripper).
     - 7
   * - ``kuka``
     - .. image:: ../_static/kuka_right45.png
          :width: 240
     - Kuka LBR iiwa 14 arm (requires a separate gripper).
     - 7
   * - ``link6``
     - .. image:: ../_static/placeholder_robot.svg
          :width: 240
     - Link6 arm (requires a separate gripper).
     - 6
   * - ``ur10``
     - .. image:: ../_static/ur10_right45.png
          :width: 240
     - Universal Robots UR10e arm (requires a separate gripper).
     - 6
   * - ``ur5``
     - .. image:: ../_static/ur10_right45.png
          :width: 240
     - Universal Robots UR5e arm (requires a separate gripper).
     - 6


.. list-table:: Manipulators (integrated gripper)
   :widths: 18 32 40 10
   :header-rows: 1

   * - Name (Key)
     - Image
     - Notes
     - DoF
   * - ``franka_with_gripper``
     - .. image:: ../_static/placeholder_robot.svg
          :width: 240
     - Franka Panda with built-in parallel gripper.
     - 9
   * - ``gen3_lite``
     - .. image:: ../_static/gen3_lite_right45.png
          :width: 240
     - Kinova Gen3 Lite with built-in gripper.
     - 7
   * - ``so_100``
     - .. image:: ../_static/so_100_right45.png
          :width: 240
     - SO Arm 100 with rotary single-jaw gripper.
     - 6
   * - ``trossen_wx250s``
     - .. image:: ../_static/trossen_wx250s_right45.png
          :width: 240
     - Trossen WX250S with built-in gripper.
     - 7
   * - ``trossen_vx300s``
     - .. image:: ../_static/trossen_vx300s_right45.png
          :width: 240
     - Trossen VX300S with built-in gripper.
     - 7

.. list-table:: Default Modular Grippers
   :widths: 18 32 40 10
   :header-rows: 1

   * - Name (Key)
     - Image
     - Notes
     - DoF
   * - ``ability``
     - .. image:: ../_static/ability_right45.png
          :width: 240
     - Ability hand gripper.
     - 6
   * - ``allegro``
     - .. image:: ../_static/allegro_right45.png
          :width: 240
     - Allegro hand gripper (right by default).
     - 16
   * - ``barrett``
     - .. image:: ../_static/barrett_right45.png
          :width: 240
     - Barrett hand gripper.
     - 8
   * - ``dclaw``
     - .. image:: ../_static/dclaw_right45.png
          :width: 240
     - D claw gripper.
     - 9
   * - ``inspire``
     - .. image:: ../_static/inspire_right45.png
          :width: 240
     - Inspire right hand gripper.
     - 6
   * - ``leap``
     - .. image:: ../_static/leap_right45.png
          :width: 240
     - Leap hand gripper (right by default).
     - 16
   * - ``robotiq``
     - .. image:: ../_static/robotiq_right45.png
          :width: 240
     - Robotiq 2F-85 parallel gripper.
     - 1
   * - ``schunk``
     - .. image:: ../_static/schunk_right45.png
          :width: 240
     - Schunk SVH right hand gripper.
     - 9
   * - ``shadow``
     - .. image:: ../_static/shadow_right45.png
          :width: 240
     - Shadow Hand gripper (right by default).
     - 24
   * - ``umi``
     - .. image:: ../_static/umi_right45.png
          :width: 240
     - Umi gripper.
     - 1

Handed Variants
---------------

Some grippers provide explicit left/right keys:

* ``allegro_left`` / ``allegro_right``
* ``leap_left`` / ``leap_right``
* ``shadow_left`` / ``shadow_right``
