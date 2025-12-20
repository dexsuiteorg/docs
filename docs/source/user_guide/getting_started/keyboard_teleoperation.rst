Keyboard Teleoperation
======================

Try out a simple teleoperation setup with just your keyboard. This demo uses a
single-arm robot with the ``osc_pose`` controller (6D delta pose).

Run Script
----------
.. code-block:: bash

   # from the repository root (contains the "dexsuite/" folder)
   python dexsuite/examples/keyboard_demo.py

   # or
   python -m dexsuite.examples.keyboard_demo

Quit the demo with :kbd:`Ctrl` + :kbd:`C`.

Key bindings (QWERTY default)
-----------------------------

The demo uses the following mapping by default:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Keys
     - Action
   * - :kbd:`↑` / :kbd:`↓`
     - Translate ``+dx`` / ``-dx``
   * - :kbd:`←` / :kbd:`→`
     - Translate ``+dy`` / ``-dy``
   * - :kbd:`u` / :kbd:`j`
     - Translate ``+dz`` / ``-dz``
   * - :kbd:`b` / :kbd:`m`
     - Rotate ``+droll`` / ``-droll``
   * - :kbd:`n` / :kbd:`h`
     - Rotate ``+dpitch`` / ``-dpitch``
   * - :kbd:`g` / :kbd:`v`
     - Rotate ``+dyaw`` / ``-dyaw``
   * - :kbd:`o` / :kbd:`p`
     - Gripper open / close
   * - :kbd:`r`
     - Reset the episode

AZERTY mapping
--------------

Use ``--layout azerty`` to switch to an AZERTY-friendly mapping:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Keys
     - Action
   * - :kbd:`z` / :kbd:`s`
     - Translate ``+dx`` / ``-dx``
   * - :kbd:`q` / :kbd:`d`
     - Translate ``+dy`` / ``-dy``
   * - :kbd:`e` / :kbd:`a`
     - Translate ``+dz`` / ``-dz``
   * - :kbd:`h` / :kbd:`k`
     - Rotate ``+droll`` / ``-droll``
   * - :kbd:`j` / :kbd:`u`
     - Rotate ``+dpitch`` / ``-dpitch``
   * - :kbd:`y` / :kbd:`i`
     - Rotate ``+dyaw`` / ``-dyaw``
   * - :kbd:`o` / :kbd:`p`
     - Gripper open / close
   * - :kbd:`r`
     - Reset the episode
