Configuration System
====================

DexSuite environments are built from a small set of options blocks:

- Simulation options (:class:`dexsuite.options.SimOptions`)
- Robot options (:class:`dexsuite.options.RobotOptions`)
- Camera options (:class:`dexsuite.options.CamerasOptions`)
- Layout options (:class:`dexsuite.options.LayoutOptions`)

This page explains what each option means, where defaults come from, and how
``ds.make`` combines everything.

.. image:: ../_static/placeholder_env.svg
   :width: 720

The spectrum (easy to advanced)
-------------------------------

Most users start simple and add control only when needed.

1) Pure defaults (fastest)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dexsuite as ds
   env = ds.make("lift")

2) Flat API (strings and tuples)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this when you are still exploring tasks and controllers.

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       control_hz=20,
       n_envs=1,
       cameras=("front", "wrist"),
       modalities=("rgb",),
       render_mode="human",
   )

3) Component API (dataclasses)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this when you want full control and reproducibility.

.. code-block:: python

   import dexsuite as ds
   from dexsuite.options import CamerasOptions, RobotOptions, SimOptions

   env = ds.make(
       "lift",
       robot=RobotOptions(type_of_robot="single"),
       sim=SimOptions(control_hz=50, n_envs=8),
       cameras=CamerasOptions(modalities=("rgb",)),
       render_mode=None,
   )

If you want help generating configs, use the builders:

- :doc:`../getting_started/environment_builders`

Where defaults come from
------------------------

DexSuite uses YAML files for defaults and presets:

- Robot defaults: ``Dexsuite/dexsuite/config/env_configs/robots.yaml``
- Arm defaults: ``Dexsuite/dexsuite/config/env_configs/arms.yaml``
- Controller defaults: ``Dexsuite/dexsuite/config/env_configs/controllers.yaml``
- Camera presets: ``Dexsuite/dexsuite/config/env_configs/cameras.yaml``
- Workspaces (AABBs): ``Dexsuite/dexsuite/config/workspaces.yaml``
- Layout presets: ``Dexsuite/dexsuite/config/presets/*.yaml`` (fallback: ``defaults.yaml``)

You can override any of these values in a single ``ds.make`` call without editing YAML.

How ds.make combines options (important rules)
----------------------------------------------

DexSuite supports both configuration styles, but it enforces a few rules so the
result is not ambiguous.

Strict keyword surface
~~~~~~~~~~~~~~~~~~~~~~

``ds.make`` raises an error on unknown keyword arguments. This is on purpose.

Exclusivity
~~~~~~~~~~~

Do not mix:

- ``robot=RobotOptions(...)`` with flat robot keys like ``manipulator=...`` or ``arm_control=...``
- ``sim=SimOptions(...)`` with flat sim keys like ``control_hz=...`` or ``n_envs=...``

You can still mix component and flat in a controlled way, for example:

- Use flat robot keys but pass ``cameras=CamerasOptions(...)`` for custom cameras.

Precedence
~~~~~~~~~~

When you pass a dataclass (for example ``robot=RobotOptions(...)``), DexSuite
uses it as-is. When you use flat keys, DexSuite builds the dataclass for you
using YAML defaults and the values you provided.

SimOptions (simulation block)
-----------------------------

SimOptions controls global simulation settings for a built environment.

Fields
~~~~~~

- ``control_hz``: how often one action is applied (how often you call ``env.step`` per second)
- ``n_envs``: number of parallel environments inside one scene
- ``performance_mode``: a flag intended to enable faster Genesis settings

What control_hz actually does
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each environment has its own physics timestep (``SIM_DT``) and substeps.
DexSuite converts your requested control rate to a number of physics steps:

- ``control_dt = 1 / control_hz``
- ``n_phys_per_ctrl = round(control_dt / SIM_DT)``

So one call to ``env.step(action)`` advances physics by ``n_phys_per_ctrl`` steps.

Parallel environments (n_envs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you set ``n_envs > 1``:

- Actions are batched and observations are batched.
- ``terminated`` and ``truncated`` are tensors of shape ``(n_envs,)``.
- Camera outputs also become batched (see :doc:`cameras_sensors`).

RobotOptions (robot block)
--------------------------

RobotOptions describes what robot is in the scene and how it is controlled.

Single vs bimanual
~~~~~~~~~~~~~~~~~~

The top-level field is:

- ``type_of_robot="single"`` or ``type_of_robot="bimanual"``

Then:

- Single: configure ``robot.single`` (an :class:`dexsuite.options.ArmOptions`)
- Bimanual: configure ``robot.left`` and ``robot.right`` (two ArmOptions)

ArmOptions (per-arm settings)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each arm has:

- ``manipulator``: the arm model name (for example ``"franka"``)
- ``gripper``: the gripper model name (for modular arms), or ``None`` for integrated arms
- ``manipulator_controller``: a :class:`dexsuite.options.ControllerOptions`
- ``gripper_controller``: a ControllerOptions (or ``None`` if you want no gripper control)
- ``workspace``: an optional AABB override (see below)

Controllers
~~~~~~~~~~~

Controller defaults are loaded from:

- ``Dexsuite/dexsuite/config/env_configs/controllers.yaml``

Flat API picks controller names with:

- ``arm_control="<key>"``
- ``gripper_control="<key>"``

Component API can override controller parameters explicitly:

.. code-block:: python

   from dexsuite.options import ArmOptions, ControllerOptions, RobotOptions

   robot = RobotOptions(
       type_of_robot="single",
       single=ArmOptions(
           manipulator="franka",
           gripper="robotiq",
           manipulator_controller=ControllerOptions(
               name="osc_pose",
               config={"normalized": True, "lin_scale": 0.05, "ang_scale": 0.10},
           ),
       ),
   )

Workspaces (AABB)
~~~~~~~~~~~~~~~~~

Each manipulator has a default workspace AABB in:

- ``Dexsuite/dexsuite/config/workspaces.yaml``

DexSuite uses this AABB for:

- Sampling object initial poses
- Failure checks (for example TCP outside workspace)

You can override an arm workspace in the component API:

.. code-block:: python

   from dexsuite.options import AABBOptions, ArmOptions, RobotOptions

   robot = RobotOptions(
       type_of_robot="single",
       single=ArmOptions(
           manipulator="franka",
           gripper="robotiq",
           workspace=AABBOptions(min=(0.20, -0.30, 0.00), max=(0.60, 0.30, 0.50)),
       ),
   )

Visual debugging flags
~~~~~~~~~~~~~~~~~~~~~~

RobotOptions also includes:

- ``visualize_tcp``: draw a tool center point marker
- ``visualize_aabb``: draw the workspace AABB corners

LayoutOptions (where robots are placed)
---------------------------------------

LayoutOptions controls base poses (robot placement in the world).

Single-arm placement
~~~~~~~~~~~~~~~~~~~~

Single-arm robots do not use layout presets. If you want to move the base, set:

- ``robot.layout.single = PoseOptions(...)``

Bimanual presets
~~~~~~~~~~~~~~~~

Bimanual robots typically use a preset string like ``"side_by_side"`` or
``"right_angle"``:

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_reach",
       manipulator=("franka", "franka"),
       gripper="robotiq",
       layout="side_by_side",
   )

Presets are resolved per manipulator model from:

- ``Dexsuite/dexsuite/config/presets/<model>.yaml``
- fallback: ``Dexsuite/dexsuite/config/presets/defaults.yaml``

CameraOptions (camera block)
----------------------------

Camera configuration is split into:

- Static cameras: fixed in the world
- Dynamic cameras: attached to robot links (wrist cameras)

See :doc:`cameras_sensors` for modality shapes and examples.

Fields
~~~~~~

The main fields are:

- ``static``: mapping of camera name to preset string or StaticCamOptions
- ``dynamic``: mapping of camera name to preset string or DynamicCamOptions
- ``modalities``: tuple like ``("rgb", "depth")``

Static camera presets
~~~~~~~~~~~~~~~~~~~~~

Static presets are defined in:

- ``Dexsuite/dexsuite/config/env_configs/cameras.yaml`` under ``static:``

Flat API example:

.. code-block:: python

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       cameras=("front", "overhead"),
       modalities=("rgb",),
   )

Dynamic wrist camera preset
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The flat camera name ``"wrist"`` is special:

- Single-arm: creates ``"wrist"``
- Bimanual: creates ``"left_wrist"`` and ``"right_wrist"``

Offsets are selected from:

- ``Dexsuite/dexsuite/config/env_configs/cameras.yaml`` under ``dynamic: wrist_cam``

The selection tries to match your gripper (or manipulator for integrated robots),
otherwise it falls back to ``default``.

Disabling cameras
~~~~~~~~~~~~~~~~~

Pass ``cameras=None`` to disable all rendering and return an empty
``obs["cameras"]`` dict.
