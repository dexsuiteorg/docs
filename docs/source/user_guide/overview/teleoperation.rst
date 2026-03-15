Teleoperation
====================

Teleoperation means you drive the robot in real time with an input device and DexSuite
turns that input into an action for ``env.step(action)``.

This is useful for:

- Debugging controllers and action conventions
- Exploring tasks before training
- Collecting demonstrations (if you want to build an imitation dataset)

.. image:: ../../assets/teleoperation_devices.png
   :width: 720

Two ways to teleoperate
-----------------------

1) Example scripts
~~~~~~~~~~~~~~~~~~

Start with keyboard teleop:

- :doc:`../getting_started/keyboard_teleoperation`

2) Interactive builder runner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The interactive builder can launch a small runner after it writes a JSON spec.

Build a spec and run immediately (default behavior):

.. code-block:: bash

   python -m dexsuite.interactive_builder --input keyboard

Run later from an existing spec:

.. code-block:: bash

   python -m dexsuite.interactive_builder run --config dexsuite_builder_spec.json --input keyboard

Supported input devices
-----------------------

The runner supports these input names:

- ``keyboard`` (requires ``pynput``)
- ``spacemouse`` (requires OS access to the device, and extra deps)
- ``vive_controller`` (requires ``openvr``)
- ``vive_tracker`` (requires ``openvr``)
- ``none`` (sends zero actions)

.. image:: ../../assets/retargeting.png
   :width: 720

Controller compatibility
------------------------

The runner checks that your controller matches what the device produces:

- ``keyboard`` and ``spacemouse`` currently support only 6D pose arm actions.
- ``vive_controller`` and ``vive_tracker`` currently support only 7D pose arm actions.
- Teleop input is currently implemented for single-arm robots only.

If you pick an incompatible controller, DexSuite will raise a clear error instead
of running with a wrong action size.

Where the device code lives
---------------------------

- Input devices: ``Dexsuite/dexsuite/devices/``
- Builder runner loop: ``Dexsuite/dexsuite/interactive_builder/runner.py``
- Builder CLI entry point: ``python -m dexsuite.interactive_builder``
