.. include:: ../_shared_nav.rst

Run a Simple Demo
=================

This demo launches a **Franka + Robotiq** setup that automatically stacks one cube on another and then exits.

Run
---

.. code-block:: bash

   # from the repository root (contains the "dexsuite/" folder)
   python dexsuite/examples/simple_stack_demo.py

   # or
   python -m dexsuite.examples.simple_stack_demo

Expected result
---------------

- A window opens with the Franka arm and two cubes.
- The agent stacks the top cube onto the base cube.
- On success, the program terminates and prints:

.. code-block:: text

   ✅ Dexsuite is good to go!

Next
----

Try :doc:`Keyboard Teleoperation <../getting_started/keyboard_teleoperation>` to control an environment manually.
