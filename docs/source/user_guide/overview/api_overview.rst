.. include:: ../_shared_nav.rst

API Overview
====================

This page gives you the shape of Dexsuite: how to construct an environment, what
``reset()`` / ``step()`` return, how actions are structured (single-arm and bimanual),
and how cameras, controllers, teleoperation, and learning stacks plug in. More details 
will reveal as walking through the subsequent sections.

.. contents::
   :local:
   :depth: 2


One-Minute Quickstart
---------------------

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
