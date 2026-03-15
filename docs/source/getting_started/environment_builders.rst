Environment Builders
====================

DexSuite can be configured in a lot of ways (task, robot, controllers, layout, cameras).
The two builders below help you generate a correct configuration quickly.

.. image:: ../_static/placeholder_env.svg
   :width: 720

HTML builder (fastest way to get code)
--------------------------------------

DexSuite includes a small, self-contained HTML tool:

- ``Dexsuite/env_builder.html``

Open it in a browser, pick your task and options, then copy the generated Python snippet
into your script or notebook.

.. image:: ../_static/placeholder_env.svg
   :width: 720

What it generates
~~~~~~~~~~~~~~~~~

The HTML builder is focused on generating a good ``ds.make(...)`` call:

- Task key
- Single vs bimanual robot
- Manipulator and gripper
- Arm and gripper controllers
- Layout preset (for bimanual)
- Cameras and modalities

It also shows a workspace AABB for the selected manipulator so you can sanity check
that the robot and table setup make sense for the task.

Interactive builder (terminal UI + reusable JSON spec)
------------------------------------------------------

If you want a guided setup that can also launch a small runner, use the interactive builder:

.. code-block:: bash

   python -m dexsuite.interactive_builder

By default it:

- Launches a terminal UI (or a simpler prompt UI if curses is unavailable)
- Writes a JSON spec to ``dexsuite_builder_spec.json``
- Optionally runs the environment after building

.. image:: ../_static/placeholder_env.svg
   :width: 720

Common workflows
~~~~~~~~~~~~~~~~

Build a spec and do not run anything yet:

.. code-block:: bash

   python -m dexsuite.interactive_builder --no-run --output dexsuite_builder_spec.json

Run later from an existing spec:

.. code-block:: bash

   python -m dexsuite.interactive_builder run --config dexsuite_builder_spec.json --input keyboard

Pick a UI explicitly:

.. code-block:: bash

   python -m dexsuite.interactive_builder --ui tui
   python -m dexsuite.interactive_builder --ui simple

Supported input devices for the runner are:

- ``keyboard``
- ``spacemouse``
- ``vive_controller``
- ``vive_tracker``
- ``none``

Next steps
----------

- Cameras: :doc:`../core_concepts/cameras_sensors`
- API overview: :doc:`../core_concepts/api_overview`
