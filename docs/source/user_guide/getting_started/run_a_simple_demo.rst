Run a Simple Demo
=================

This demo launches a **Franka + Robotiq** setup in the ``stack`` environment and
steps the simulation for a short rollout. It’s meant as a quick sanity check
that your install + rendering works.

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
- The script steps the environment for a few seconds and prints:

.. code-block:: text

   Dexsuite is good to go!

Next
----

Try :doc:`Keyboard Teleoperation <../getting_started/keyboard_teleoperation>` to control an environment manually.
