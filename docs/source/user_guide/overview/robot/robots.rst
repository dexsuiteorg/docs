.. include:: ../../_shared_nav.rst
Robots
====================
A robot is represented in the simulator by a URDF or MJCF description file. A significant design challenge is that these robot descriptions come in two common forms: some provide the manipulator (arm) and end-effector (gripper) in separate files, while others provide them as a single, combined file.

To handle both of these cases cleanly, ``dexsuite`` provides two distinct robot abstractions: **Modular Robots** and **Integrated Robots**. This design allows the framework to correctly apply controllers and manage the robot's kinematics, regardless of how its source files are structured.

Modular Robots
^^^^^^^^^^^^^^^^

Modular Robots are the most common and flexible robot type. They are defined as a collection of separate components that are "fused" together at runtime. This design allows for maximum reusability, as different grippers can be easily swapped and attached to different manipulators.

A Modular Robot is composed of three distinct parts:

* **Modular Manipulator:** The arm itself, which does not include a gripper (e.g., a UR-5 or Franka arm).

* **Gripper:** The end-effector, defined in its own file (e.g., a Robotiq 2F-85).

* **Gripper Mount (Optional):** A realistic adapter piece that defines the precise attachment offset between the arm's wrist and the gripper's base. This can be defined as an invisible offset or as a visible shape (like a cylinder).

Integrated Robots
^^^^^^^^^^^^^^^^^^^

Integrated Robots are defined by a single URDF or MJCF file that already contains both the manipulator and its built-in gripper (e.g., the Franka Emika "Panda" arm with its native gripper).

While these robots appear simpler, they introduce a significant control challenge. The control system must be able to differentiate between the "arm" joints, which are typically driven by Inverse Kinematics (IK) using a pose controller, and the "gripper" joints, which are driven by a joint position controller.

To solve this, each integrated robot must define a **gripper proxy**. This proxy manually specifies which joint indices in the robot's file belong to the gripper. This allows the framework to "wrap" the correct joints with the correct controller, enabling simultaneous arm and gripper control. This setup is handled within the ``IntegratedRobot`` class but requires a specific joint map for each new integrated robot added to the framework.
