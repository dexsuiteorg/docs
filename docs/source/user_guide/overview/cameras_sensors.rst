Cameras and Sensors
===================

DexSuite can render camera observations directly from the simulator.

You can use cameras for:

- Training vision policies (RGB, depth, segmentation, normals)
- Debugging (save images, inspect viewpoints)
- Teleoperation (wrist cameras are often the easiest view)

.. image:: ../../_static/placeholder_env.svg
   :width: 720

Where cameras show up in observations
----------------------------------------

The environment observation has two top-level keys:

- ``obs["state"]``: robot + task state (torch tensors)
- ``obs["cameras"]``: camera outputs (torch tensors)

Camera outputs are nested by camera name, then by modality:

.. code-block:: python

   front_rgb = obs["cameras"]["front"]["rgb"]

If you disable cameras (``cameras=None``), then ``obs["cameras"]`` is an empty dict.

Quickstart (flat API)
---------------------

Enable a front static camera and a wrist camera:

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       cameras=("front", "wrist"),
       modalities=("rgb", "depth"),
       render_mode=None,
   )

   obs, info = env.reset()
   obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

   rgb = obs["cameras"]["front"]["rgb"]
   depth = obs["cameras"]["front"]["depth"]

   env.close()

Default behavior
~~~~~~~~~~~~~~~~

If you do not pass ``cameras=...`` to ``ds.make``, DexSuite enables:

- ``("front", "wrist")`` cameras
- ``("rgb",)`` modality

Disable all cameras by passing ``cameras=None``.

Camera names and presets
------------------------

Static camera presets live in:

- ``Dexsuite/dexsuite/config/env_configs/cameras.yaml`` under ``static:``

The commonly used ones are:

- ``front``
- ``overhead``
- ``left_side`` and ``right_side``
- ``left_angled_front`` and ``right_angled_front``
- ``left_angled_back`` and ``right_angled_back``

Dynamic cameras
~~~~~~~~~~~~~~~

The flat API supports a built-in dynamic wrist camera name:

- ``wrist``: a camera attached to the gripper root link

For bimanual robots, ``wrist`` expands to:

- ``left_wrist``
- ``right_wrist``

The offsets for the wrist camera come from:

- ``Dexsuite/dexsuite/config/env_configs/cameras.yaml`` under ``dynamic: wrist_cam``

DexSuite picks the best available offsets for your gripper (or for integrated manipulators).

Modalities
----------

Modalities are selected with ``modalities=(...)``.

Supported modalities:

- ``rgb`` (required)
- ``depth``
- ``segmentation``
- ``normal``

Shapes and dtypes
-----------------

DexSuite returns the raw Genesis camera outputs as torch tensors.

Let:

- ``B = n_envs``
- ``H, W`` be the camera image height and width

Shapes:

- Single env (``B=1``):
  - ``rgb`` and ``normal``: ``(H, W, 3)``
  - ``depth`` and ``segmentation``: ``(H, W)``
- Batched (``B>1``):
  - ``rgb`` and ``normal``: ``(B, H, W, 3)``
  - ``depth`` and ``segmentation``: ``(B, H, W)``

Dtypes:

- ``rgb``: ``uint8`` in ``[0, 255]``
- ``depth``: ``float32`` in meters (non-negative)
- ``segmentation``: integer IDs (``int32``)
- ``normal``: ``float32`` in ``[-1, 1]``

Custom cameras (component API)
------------------------------

Use the component API when you want full control over camera placement and resolution.

Static camera example:

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

Dynamic camera example (custom wrist offset):

.. code-block:: python

   import dexsuite as ds
   from dexsuite.options import CamerasOptions, DynamicCamOptions

   cameras = CamerasOptions(
       static={},
       dynamic={
           "wrist": DynamicCamOptions(
               pos_offset=(0.00, 0.10, -0.03),
               quat_offset=(1.0, 0.0, 0.0, 0.0),
               res=(224, 224),
           ),
       },
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

Performance tips
----------------

Camera rendering is often the largest cost in the simulation loop.

Common ways to keep things fast:

- Disable cameras during pure state-based training: pass ``cameras=None``.
- Keep resolutions small (for example 224x224) when running large ``n_envs``.
- Prefer fewer cameras over many cameras when you are running in parallel.

Related pages
-------------

- Environment builders (configure cameras interactively): :doc:`../getting_started/environment_builders`
- Teleoperation overview: :doc:`teleoperation`
