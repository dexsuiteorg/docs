.. include:: ../_shared_nav.rst
Environments
====================
In DexSuite, environments are structured around two core concepts: the **Base Environment** and the **Task**. The **Base Environment** (`BaseEnv`) takes care of setting up the simulator, robot, cameras, batching, and device management—essentially handling all the underlying infrastructure that makes the simulation run smoothly. On the other hand, the **Task** defines the specific logic that makes each environment unique, including how the scene is populated, how episodes begin, how observations and rewards are computed, and when the task succeeds or fails.

DexSuite follows a straightforward, direct workflow that keeps environment creation simple and intuitive, yet powerful. This approach is centered on **Direct Inheritance**, where each task is implemented as a single class inheriting from `BaseEnv`. This single child class fully encapsulates the environment logic—populating scenes, randomizing episodes, computing rewards, and determining episode outcomes—without needing separate managers or configuration classes.

This design offers transparency, giving you clear visibility into how your task behaves, with no hidden layers. It's particularly advantageous when optimizing performance or implementing detailed logic that's difficult to split into separate modules.

* **The BaseEnv Foundation**:
  `BaseEnv` is the parent class that handles all the foundational elements. It sets up the simulator scene, arena, robot, optional cameras, device selection, and batching. It also manages seeding, defines workspace boundaries, validates actions, and constructs observation/action spaces from a prototype observation. You do not need to re-implement any of this infrastructure yourself.

* **The Task Implementation**:
  Your child class is responsible exclusively for task-specific logic. This involves clearly defined "hook" methods: `_setup_scene` for creating entities in the scene, `_on_episode_start` for episode randomization, `_get_extra_obs` for custom observations beyond robot state, `_compute_reward` for scoring progress, and `_is_success`/`_is_failure` to determine when the task is complete.
