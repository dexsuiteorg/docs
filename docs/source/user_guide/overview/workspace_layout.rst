Workspace Layout
====================

Workspace layout answers two questions:

1) Where is the robot base placed in the world?
2) Given that base pose, what region of space is considered "in-bounds" for the robot?

.. image:: ../../_static/placeholder_robot.svg
   :width: 520

Robot base placement
--------------------

DexSuite places robots using :class:`dexsuite.options.LayoutOptions`.

Single-arm
~~~~~~~~~~

Single-arm robots use one base pose (``PoseOptions``). If you do not pass an
explicit pose, the default is the origin.

Bimanual
~~~~~~~~

Bimanual robots have a left and right base pose. DexSuite uses named layout
presets to keep these placements consistent across tasks.

Presets live under ``Dexsuite/dexsuite/config/presets/``. For example, the
default preset file defines:

- ``side_by_side``
- ``face_to_face``
- ``right_angle``

Workspaces and AABBs
--------------------

Each manipulator has a default workspace AABB in
``Dexsuite/dexsuite/config/workspaces.yaml``. This AABB is defined in the
manipulator base frame.

At runtime, DexSuite transforms this AABB into the world frame using the robot
base pose and exposes:

- ``env.world_aabb``: union workspace used by most tasks.
- ``env.get_workspace_aabbs()``: dict with keys ``union``, ``left``, ``right``, and ``overlap``.

These AABBs are commonly used for:

- Sampling initial object poses.
- Clamping targets into reachable space.
- Detecting out-of-bounds TCP behavior.

Visualizing the workspace
-------------------------

You can visualize workspace corners by enabling ``visualize_aabb`` on your robot
options. This draws small markers at the eight AABB corners during environment
construction.

Examples
--------

Pick a bimanual preset (flat API)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_reach",
       manipulator=("franka", "franka"),
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       layout="face_to_face",
       render_mode="human",
   )

Set explicit base poses (component API)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dexsuite as ds
   from dexsuite.options import CamerasOptions, LayoutOptions, PoseOptions, RobotOptions, SimOptions

   robot = RobotOptions(
       type_of_robot="bimanual",
       layout=LayoutOptions(
           left=PoseOptions(pos=(0.0, 0.35, 0.0), yaw_rad=0.0),
           right=PoseOptions(pos=(0.0, -0.35, 0.0), yaw_rad=0.0),
       ),
   )

   env = ds.make(
       "bimanual_reach",
       robot=robot,
       sim=SimOptions(n_envs=1, control_hz=20),
       cameras=CamerasOptions(modalities=("rgb",)),
       render_mode="human",
   )

Override a workspace AABB (component API)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dexsuite as ds
   from dexsuite.options import AABBOptions, ArmOptions, RobotOptions

   robot = RobotOptions(
       type_of_robot="single",
       single=ArmOptions(
           manipulator="franka",
           workspace=AABBOptions(min=(0.2, -0.3, 0.0), max=(0.6, 0.3, 0.6)),
       ),
       visualize_aabb=True,
   )

   env = ds.make("reach", robot=robot, render_mode="human")
