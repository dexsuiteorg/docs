.. _environment:

Environments
====================
DexSuite environments follow a simple rule: one task equals one Python class.
Each task inherits from :class:`dexsuite.environments.base_env.BaseEnv` and only
implements what is specific to that task.

.. image:: ../../_static/placeholder_env.svg
   :width: 520

Base Environment vs Task
------------------------

**BaseEnv** provides the shared simulation plumbing:

- Creates a Genesis scene and builds physics.
- Builds the arena and robot from options.
- Sets up cameras (optional).
- Creates `action_space` and `observation_space`.
- Handles batched simulation (`n_envs`) and seeding.

**Task classes** implement the task logic by overriding a small set of hook
methods:

- ``_setup_scene``: add task entities to the scene.
- ``_on_episode_start``: reset and randomize the episode.
- ``_get_extra_obs``: add task-specific observation tensors.
- ``_compute_reward``: compute the reward.
- ``_is_success`` and ``_is_failure``: define episode termination.
- ``_step`` (optional): per-control-step updates before stepping physics.

Creating environments
---------------------

Tasks are registered by key and created via :func:`dexsuite.make`:

.. code-block:: python

   import dexsuite as ds

   env = ds.make("lift", manipulator="franka", gripper="robotiq", render_mode="human")
   obs, info = env.reset()
   obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
   env.close()

Workspaces
----------

DexSuite uses a **workspace AABB** (axis-aligned bounding box) to define a safe
region for sampling objects and detecting out-of-bounds behavior.

- Each manipulator has a default workspace in ``Dexsuite/dexsuite/config/workspaces.yaml``.
- The workspace is defined in the manipulator base frame.
- The base pose (from layout options) is applied to transform that AABB into the world frame.
- For bimanual robots, DexSuite computes left, right, overlap, and union AABBs and uses the union as ``env.world_aabb``.

Many tasks sample initial object poses from the workspace AABB, and many tasks
use it as a failure condition (TCP outside workspace).

Layout
------

The robot base pose (single) or base poses (bimanual) come from layout options.
This matters for where the robot appears in the scene and where its workspace
lands in world coordinates.

See :doc:`Workspace Layout <workspace_layout>` for how layout presets work.

.. toctree::
   :maxdepth: 1
   :hidden:

   environment/available_envs
   environment/lift
   environment/reach
   environment/push
   environment/pick_place
   environment/stack
   environment/make_coffee
   environment/pick_place_mug
   environment/pick_place_pan
   environment/drill_to_point
   environment/cable_routing
   environment/cut_butter
   environment/rotatedice
   environment/foldshirt
   environment/pour_water
   environment/spready_butter
   environment/mpm_sponge_drop
   environment/bimanual_reach
   environment/bimanual_lift
   environment/bimanual_push
   environment/bimanual_pick_place
   environment/bimanual_stack
   environment/bimanual_make_coffee
   environment/bimanual_pick_place_mug
   environment/bimanual_pick_place_pan
   environment/bimanual_pick_place_pot
   environment/bimanual_fold_glasses
   environment/bimanual_drill_to_point
