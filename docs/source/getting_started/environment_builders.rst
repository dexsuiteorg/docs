Environment Builders
====================

DexSuite exposes a large configuration space: task, robot, controllers, layout,
cameras, and sensor modalities. The two builders below help you produce a valid
``ds.make(...)`` call quickly, without needing to memorize every parameter.

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Builder
     - Best For
   * - HTML Builder
     - Instant code generation in a browser, no terminal needed.
   * - Interactive Builder
     - Guided terminal setup with a reusable JSON spec and optional live runner.

HTML Builder
------------

The HTML builder is a single, self-contained file that runs entirely in the browser:

.. code-block:: text

   dexsuite/env_builder.html

Open the file in any browser, configure your environment using the dropdown menus,
and copy the generated ``ds.make(...)`` snippet into your script or notebook.

What It Generates
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Parameter
     - Description
   * - Task key
     - The string identifier passed to ``ds.make()``.
   * - Robot configuration
     - Single-arm or bimanual, manipulator model, and gripper model.
   * - Controllers
     - Arm controller mode and gripper controller mode.
   * - Layout preset
     - Workspace layout for bimanual configurations.
   * - Cameras and modalities
     - Camera names and observation types (RGB, depth, segmentation).
   * - Workspace AABB
     - Axis-aligned bounding box for the selected manipulator, displayed as a reference.

Interactive Builder
-------------------

The interactive builder provides a guided terminal interface and produces a reusable
JSON configuration file. It can also launch a live runner after configuration is complete.

.. code-block:: bash

   python -m dexsuite.interactive_builder

By default, the builder:

- Launches a full terminal UI (TUI). If ``curses`` is unavailable, it falls back to a simpler prompt-based UI.
- Writes the completed configuration to ``dexsuite_builder_spec.json``.
- Offers to run the environment immediately using the chosen input device.

Common Workflows
~~~~~~~~~~~~~~~~

Generate a spec file without launching the environment:

.. code-block:: bash

   python -m dexsuite.interactive_builder --no-run --output dexsuite_builder_spec.json

Run an environment from an existing spec file:

.. code-block:: bash

   python -m dexsuite.interactive_builder run \
     --config dexsuite_builder_spec.json \
     --input keyboard

Select a UI mode explicitly:

.. code-block:: bash

   # Full terminal UI
   python -m dexsuite.interactive_builder --ui tui

   # Simple prompt UI (for environments without curses support)
   python -m dexsuite.interactive_builder --ui simple

Supported Input Devices for the Runner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Next Steps
----------

- :doc:`../core_concepts/api_overview` covers the full ``ds.make()`` API and all available parameters.
- :doc:`../core_concepts/cameras_sensors` explains how to configure cameras and sensor modalities.
