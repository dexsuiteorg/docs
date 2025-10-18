.. include:: ../_shared_nav.rst

API Overview
====================


# API Overview

The Dexsuite API is designed for users from different technical background. 
It handles a sprectrum of: one made very intuitively so that most parameters are handled by the program, 
and one made for experts, so that they can customize their own environment settings. 

Notes: Let's call it a spectrum rather than two modes 


This page gives you the shape of Dexsuite: how to construct an environment, what
``reset()`` / ``step()`` return, how actions are structured (single-arm and bimanual),
and how cameras, controllers, teleoperation, and learning stacks plug in. More details 
will reveal as walking through the subsequent sections.

.. contents::
   :local:
   :depth: 2


One-Minute Quickstart
---------------------

.. rubric:: Explanation

This mode allows you to use Dexsuite without worrying about the whole range of options that needs to be set. The basic API will be sufficient for the majority of users and applications, and is great if you are a beginner with the API.

.. rubric:: How to use

To run the basic API, just run :code:`ds.make(<<options>>)`, where options can be the following parameters:

-   :code:`args`
-   (other parameters, if any)

The :code:`make()` function will automatically convert the arguments into presets, and will build the environment based on that.

.. rubric:: Example

.. code-block:: python

    import dexsuite as ds

    # --- Minimal environment creation ---
    env = ds.make("reach", manipulator="franka_with_gripper", arm_control="osc_pose")

    obs = env.reset()
    for t in range(200):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
    env.close()



.. code-block:: python

    import torch
    import dexsuite as ds

    # 1) Build an environment (task/robot/controller are determined here)
    env = ds.make(
        "stack",                       # task name: e.g. "stack", "pick_place_mug", "bimanual_reach"
        manipulator="franka",          # robot arm key
        gripper="robotiq",             # gripper key
        arm_control="osc_pose",        # arm controller key
        gripper_control="joint_position",
        render_mode="human",           # "human" | "rgb_array" | None
    )

    # 2) Gymnasium-style rollout (Just sanity check; does not teleoperate)
    obs, info = env.reset()
    for _ in range(500):
        arm_cmd  = torch.zeros(6)       # controller-specific; here: [dx, dy, dz, droll, dpitch, dyaw]
        grip_cmd = torch.tensor([-1.0]) # open (-1), close (+1)
        obs, reward, terminated, truncated, info = env.step((arm_cmd, grip_cmd))
        if terminated or truncated:
            break

    # 3) Rendering
    env.render(mode="human")            
    env.close()

.. tip::

   For **live control**, see :ref:`Teleoperation & Datasets <api_overview_teleop>` for details.


Core Concepts
-------------

**Factory & Registry**

``ds.make(task_name, **kwargs)`` constructs a complete simulation scene. Tasks
(e.g., ``"stack"``, ``"pick_place_mug"``, ``"bimanual_reach"``), robots,
grippers, and controllers are looked up by string keys, keeping scripts short and
portable.

**Gymnasium-like API**

- ``reset() -> (obs, info)``
- ``step(action) -> (obs, reward, terminated, truncated, info)``
- ``render(mode="human" | "rgb_array", camera=...)``
- ``close()``

**Episode Endings**

``terminated`` becomes true on task-defined success or failure; ``truncated``
becomes true on time/out-of-horizon. ``info["success"]`` is provided.


structure
---------

We will now go over the general structure behind the Dexsuite API, how each component interacts with each other, and how they work together.

.. figure:: architecture
    :alt: Diagram of the Dexsuite API architecture.

.. container::

    .. rubric:: Simulation

    The simulation part contains all general information about the environment that you want to create. Here you can define the control frequency, the horizon, the simulation speed, and the number of parallel environments.

    *What it contains*

    -   Options
    -   Args

.. container::

    .. rubric:: Robot

    Robot is probably the most complex part of the system. It describes the grippers and manipulators you want to use for your simulation, their initial position and orientation, their controllers, and their axis aligned boundary box. You also have the choice to have either a single arm setting, or a bimanual setting with two arms.

    *What it contains*

    -   Options
    -   Args

.. container::

    .. rubric:: Camera

    The camera contains everything related to the points of view that you want to have on your simulation. It can be both static cameras, or dynamic cameras, i.e. cameras mounted on your robot. You also have the option to choose which output format you want for your cameras. It can be regular RGB, or it can be depth, segmentation or normal.

    *What it contains*

    -   Options
    -   Args

Observations
------------

Observations are a nested dictionary designed to be predictable and ML-friendly.

Top-level layout:

- ``obs["state"]`` – numeric tensors only; stable keys for robots/grippers plus
  task-specific entries under ``"other"``.
  - *Single-arm example:* ``state["manipulator"]["eef_pose"]``,
    ``state["gripper"]["tcp_pose"]``, ``state["other"][...]``.
  - *Bimanual example:* ``state["left"][...]``, ``state["right"][...]``,
    plus ``state["other"][...]``.
- ``obs["cameras"]`` *(optional)* – a dict of per-camera modalities, e.g.
  ``{"front": {"rgb": HxWx3 uint8, "depth": HxWx1}}`` if enabled.

The observation space mirrors this structure via nested ``gymnasium.spaces.Dict``.


Actions & Spaces
----------------

Actions are a tuple ``(arm_cmd, gripper_cmd)`` (single arm) or a left/right
composite (bimanual). Commands are normalized for interchangeability:

- **Arm command** – a 6-D (or controller-specific) vector in ``[-1, 1]``.
- **Gripper command** – 1-D (or k-D) open/close in ``[-1, 1]``.

Inspect dimensions programmatically:

.. code-block:: python

    act_space = env.action_space
    obs_space = env.observation_space  # nested Dict matching obs["state"] / ["cameras"]

    # Example (single arm):
    arm_dim   = act_space["manipulator"].shape[0]
    grip_dim  = act_space["gripper"].shape[0]


Controllers
-----------

Controllers translate normalized commands into low-level actuation:

- **Arm** (e.g., ``"osc_pose"``, ``"joint_position"``): maps 6-D pose deltas or
  joint targets to torques/positions internally.
- **Gripper** (e.g., ``"joint_position"``): maps a scalar or vector open/close
  to the hand’s DOFs.

All controllers observe the same normalization convention (``[-1, 1]``) so
teleoperation, scripted agents, and RL policies can share code.

Basic API
---------
.. rubric:: Explanation

This mode allows you to use Dexsuite without worrying about the whole range of options that needs to be set. The basic API will be sufficient for the majority of users and applications, and is great if you are a beginner with the API.

.. rubric:: How to use

To run the basic API, just run :code:`ds.make(<<options>>)`, where options can be the following parameters:

-   :code:`args`
-   (other parameters, if any)

The :code:`make()` function will automatically convert the arguments into presets, and will build the environment based on that.

.. rubric:: Example

.. code-block:: python

    import dexsuite as ds

    # --- Minimal environment creation ---
    env = ds.make("reach", manipulator="franka_with_gripper", arm_control="osc_pose")

    obs = env.reset()
    for t in range(200):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
    env.close()

Advanced API
------------

.. rubric:: Explanation

In the custom API settings, you can select manually a variety of parameters for your environment, bringing Dexsuite to its full potential. It is useful for all cases that the default environments does not satisfy, whether it is about the number of parallel environments, the robot's controller type, or the rendering mode of the camera.

.. rubric:: How to use

Instead of passing arguments into :code:`ds.make()`, we pass three dataclasses containing all information about the environment we want to produce. The three dataclasses are:

-   :code:`SimOptions`: Contains general settings about the simulation
-   :code:`RobotOptions`: Contains information about the robot(s) we are using
-   :code:`CameraOptions`: Contains information about the static and dynamic cameras used to get observations

.. rubric:: Examples

.. code-block:: python

    from dexsuite.options import RobotOptions, SimOptions, CamOptions
    import dexsuite as ds

    # --- Define robot configuration ---
    robot_opt = RobotOptions(
        manipulator="franka_with_gripper",
        arm_control="osc_pose",
        gripper_control="joint_position",
        physics="mujoco",
        control_hz=100,
    )

    # --- Define simulation parameters ---
    sim_opt = SimOptions(
        render=True,
        control_hz=100,
        gravity=(0, 0, -9.81),
        headless=False,
    )

    # --- Define cameras ---
    cameras_opt = CamOptions(
        static={
            "front": {"pos": (1.2, 0, 0.5), "lookat": (0, 0, 0)},
            "side": {"pos": (0, 0.7, 0.5), "lookat": (0, 0, 0)},
        },
        resolution=(640, 480),
        depth=True,
    )

    # --- Build the environment ---
    env = ds.make(
        robot=robot_opt,
        sim=sim_opt,
        cameras=cameras_opt,
    )

    obs = env.reset()


Cameras & Rendering
-------------------

Dexsuite mounts named cameras into the scene (e.g., ``"front"``, ``"left"``).
You can:

- open an interactive viewer with ``env.render("human")``,
- fetch frames as arrays with ``env.render("rgb_array", camera="front")``, or
- include camera images in ``obs["cameras"]`` when enabled at construction.

Camera intrinsics/extrinsics and modalities (RGB/Depth/etc.) are configured in
the repository and attached at build time. See the *Cameras and Sensors* page.

.. _api_overview_teleop:

Teleoperation & Datasets
------------------------

Dexsuite includes ready-to-use teleoperation recorders (e.g., keyboard,
SpaceMouse). Recorded episodes are written to HDF5 with the full state tree (and
optionally RGB). A conversion script exports to **robomimic** format for
imitation learning (flattened keys and ``next_obs`` layout).

Typical workflow:

1. Teleoperate several successful demonstrations.

   .. code-block:: bash

      python dataset_teleop.py --task stack --manipulator franka --gripper robotiq

2. Convert to robomimic HDF5.

   .. code-block:: bash

      python convert_robomimic_dataset.py \
        --in path/to/raw_dexsuite.hdf5 \
        --out datasets/stack_robomimic.hdf5 \
        --include_images

3. Train a behavior-cloning policy and evaluate it back in Dexsuite.


Learning Stack Integrations
---------------------------

- **Imitation Learning (robomimic):** Use the provided converter and environment
  wrappers to train BC/sequence models. Choose low-dim state, RGB, or both.
- **Reinforcement Learning:** Dexsuite follows Gymnasium, so PPO/SAC/etc. work
  out of the box—just match your policy head to the action dimensions reported
  by ``env.action_space``.

Next
----

- :doc:`Environments </user_guide/overview/environments>`
