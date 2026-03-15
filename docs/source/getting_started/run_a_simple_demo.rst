Run a Simple Demo
=================

The simple demo launches a Franka arm with a Robotiq gripper in the ``stack`` task
and steps the simulation through a short rollout. It is the fastest way to confirm
that your installation, GPU driver, and Genesis renderer are all working correctly.

Run
---

From the repository root (the directory that contains the ``dexsuite/`` folder):

.. code-block:: bash

   python dexsuite/examples/simple_stack_demo.py

   # Alternatively, as a module
   python -m dexsuite.examples.simple_stack_demo

Expected Output
---------------

A viewer window opens showing the Franka arm and two cubes on a table. The script
steps the environment for several seconds and then prints:

.. code-block:: text

   Dexsuite is good to go!

The window closes automatically when the script finishes.

Command-Line Options
--------------------

The demo accepts arguments to change the robot, task, and rendering behavior.

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Argument
     - Default
     - Description
   * - ``--task``
     - ``stack``
     - Task key to load. See the :doc:`../catalog/index` for all available tasks.
   * - ``--manipulator``
     - ``franka``
     - Manipulator arm to use.
   * - ``--gripper``
     - ``robotiq``
     - Gripper to attach.
   * - ``--arm-control``
     - ``osc_pose``
     - Arm controller mode.
   * - ``--gripper-control``
     - ``joint_position``
     - Gripper controller mode.
   * - ``--steps``
     - ``300``
     - Number of simulation steps to run.
   * - ``--render-mode``
     - ``human``
     - Rendering mode. Use ``human`` for a viewer window.
   * - ``--seed``
     - ``0``
     - Random seed for environment initialization.

Example with a different robot:

.. code-block:: bash

   python dexsuite/examples/simple_stack_demo.py \
     --task pick_place \
     --manipulator gen3 \
     --gripper robotiq \
     --steps 500

Troubleshooting
---------------

**No window appears, or the script exits immediately**

Confirm that your GPU driver and OpenGL configuration are correct. Refer to the
GPU verification steps in :doc:`installation`.

**Genesis initialization error**

This typically indicates a renderer or driver problem. Run ``nvidia-smi`` and
``glxinfo | grep "OpenGL renderer"`` to verify the GPU is active.

Next Steps
----------

Proceed to :doc:`keyboard_teleoperation` to take direct control of an environment
using your keyboard.
