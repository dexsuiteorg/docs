Add a New Camera
================

DexSuite supports two camera types:

- Static cameras: fixed in the world (good for front or overhead views)
- Dynamic cameras: attached to a robot link (wrist views)

You can add cameras in two ways:

- One-off in Python (no config files changed)
- As a reusable preset in ``Dexsuite/dexsuite/config/env_configs/cameras.yaml``

Option 1: Add a one-off camera in Python
----------------------------------------

This is the easiest way to experiment.

.. code-block:: python

   import dexsuite as ds
   from dexsuite.options import CamerasOptions, StaticCamOptions

   cameras = CamerasOptions(
       static={
           "my_front": StaticCamOptions(
               pos=(1.2, 0.0, 0.6),
               lookat=(0.4, 0.0, 0.2),
               fov=65.0,
               res=(320, 240),
           ),
       },
       dynamic={},
       modalities=("rgb",),
   )

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       cameras=cameras,
       render_mode=None,
   )
   obs, info = env.reset()
   obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
   env.close()

Option 2: Add a static camera preset (cameras.yaml)
---------------------------------------------------

Static camera presets live under the ``static:`` key.

1) Edit:

- ``Dexsuite/dexsuite/config/env_configs/cameras.yaml``

2) Add an entry:

.. code-block:: yaml

   static:
     my_front:
       pos: [1.2, 0.0, 0.6]
       lookat: [0.4, 0.0, 0.2]
       fov: 65
       res: [320, 240]

3) Use it from the flat API:

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       cameras=("my_front", "wrist"),
       modalities=("rgb",),
       render_mode=None,
   )

Dynamic camera presets (wrist cameras)
--------------------------------------

Dynamic presets live under the ``dynamic:`` key. They define:

- ``fov`` and ``res`` for the camera
- A ``default`` block with ``pos_offset`` and optional ``quat_offset``
- An optional ``by`` block to override offsets per gripper (or per manipulator for integrated robots)

Example:

.. code-block:: yaml

   dynamic:
     my_wrist_cam:
       fov: 60
       res: [224, 224]
       default:
         pos_offset: [0.00, 0.10, -0.03]
         quat_offset: [1.00, 0.00, 0.00, 0.00]
       by:
         robotiq:
           pos_offset: [0.00, 0.14, 0.00]

Using a dynamic preset
~~~~~~~~~~~~~~~~~~~~~~

The flat ``cameras=("wrist", ...)`` path always uses the built-in ``wrist_cam`` preset.
To use your own preset, pass a :class:`dexsuite.options.CamerasOptions` object:

.. code-block:: python

   import dexsuite as ds
   from dexsuite.options import CamerasOptions

   cameras = CamerasOptions(
       static={"front": "front"},
       dynamic={"wrist": "my_wrist_cam"},
       modalities=("rgb",),
   )

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       cameras=cameras,
       render_mode=None,
   )

For bimanual robots, a generic dynamic name like ``"wrist"`` is expanded to left and right.
If you need different left and right offsets, pass explicit ``DynamicCamOptions`` objects
with names like ``left_wrist`` and ``right_wrist``.

Notes and troubleshooting
-------------------------

- Static camera positions are in world coordinates.
- Dynamic camera offsets are in the attached link frame (typically the gripper root link).
- If you add a new preset and it is not found, double check YAML indentation and keys.

Related page
------------

- Cameras overview: :doc:`../overview/cameras_sensors`
