Run a Simple Demo
=================

The keyboard demo starts a single-arm robot under the ``osc_pose`` controller and
maps keyboard keys to 6-DOF end-effector deltas. No additional hardware is required.

Run
---

From the repository root:

.. code-block:: bash

   python dexsuite/examples/keyboard_demo.py

   # Alternatively, as a module
   python -m dexsuite.examples.keyboard_demo

Quit with :kbd:`Ctrl` + :kbd:`C`.

Key Bindings
------------

QWERTY (Default)
~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Keys
     - Axis
     - Action
   * - :kbd:`↑` / :kbd:`↓`
     - X
     - Translate end-effector forward / backward
   * - :kbd:`←` / :kbd:`→`
     - Y
     - Translate end-effector left / right
   * - :kbd:`u` / :kbd:`j`
     - Z
     - Translate end-effector up / down
   * - :kbd:`b` / :kbd:`m`
     - Roll
     - Rotate around X-axis
   * - :kbd:`n` / :kbd:`h`
     - Pitch
     - Rotate around Y-axis
   * - :kbd:`g` / :kbd:`v`
     - Yaw
     - Rotate around Z-axis
   * - :kbd:`o` / :kbd:`p`
     - Gripper
     - Open / Close
   * - :kbd:`r`
     - (reset)
     - Reset the episode

.. AZERTY
.. ~~~~~~

.. Pass ``--layout azerty`` to use an AZERTY-friendly mapping:

.. .. code-block:: bash

..    python dexsuite/examples/keyboard_demo.py --layout azerty

.. .. list-table::
..    :widths: 25 25 50
..    :header-rows: 1

..    * - Keys
..      - Axis
..      - Action
..    * - :kbd:`z` / :kbd:`s`
..      - X
..      - Translate end-effector forward / backward
..    * - :kbd:`q` / :kbd:`d`
..      - Y
..      - Translate end-effector left / right
..    * - :kbd:`e` / :kbd:`a`
..      - Z
..      - Translate end-effector up / down
..    * - :kbd:`h` / :kbd:`k`
..      - Roll
..      - Rotate around X-axis
..    * - :kbd:`j` / :kbd:`u`
..      - Pitch
..      - Rotate around Y-axis
..    * - :kbd:`y` / :kbd:`i`
..      - Yaw
..      - Rotate around Z-axis
..    * - :kbd:`o` / :kbd:`p`
..      - Gripper
..      - Open / Close
..    * - :kbd:`r`
..      - (reset)
..      - Reset the episode

Command-Line Options
--------------------

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Argument
     - Default
     - Description
   * - ``--task``
     - ``lift``
     - Task key to load.
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
   * - ``--layout``
     - ``qwerty``
     - Keyboard layout. Accepted values: ``qwerty``, ``azerty``.
   * - ``--pos-sens``
     - ``1.0``
     - Position sensitivity multiplier.
   * - ``--rot-sens``
     - ``1.0``
     - Rotation sensitivity multiplier.
   * - ``--render-mode``
     - ``human``
     - Rendering mode.
   * - ``--control-hz``
     - ``None``
     - Control loop frequency in Hz. ``None`` runs as fast as possible.

Example with a different task and increased sensitivity:

.. code-block:: bash

   python dexsuite/examples/keyboard_demo.py \
     --task pick_place \
     --manipulator gen3 \
     --gripper robotiq \
     --pos-sens 1.5 \
     --rot-sens 1.2



Troubleshooting
---------------

**No window appears, or the script exits immediately**

If you are on GPU, confirm that your GPU driver and OpenGL configuration are correct. Refer to the
GPU verification steps in :doc:`installation`.

**Genesis initialization error**

This typically indicates a renderer or driver problem. Run ``nvidia-smi`` and
``glxinfo | grep "OpenGL renderer"`` to verify the GPU is active.

Next Steps
----------

Proceed to :doc:`environment_builders` to learn how to configure arbitrary robot
and task combinations without writing boilerplate code.
