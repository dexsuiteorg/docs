Bimanual Make Coffee
====================

Task key: ``bimanual_make_coffee``.

``bimanual_make_coffee`` is a two-arm rigid-object task. A coffee machine and a
mug are spawned, and the agent must place the mug onto the machine tray.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Place the mug in the tray region of the coffee machine.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_make_coffee",
       manipulator=("franka", "franka"),
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
       render_mode="human",
   )

   obs, info = env.reset()
   obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

   env.close()

Task Entities
-------------

- ``machine``: a fixed coffee machine.
- ``mug``: a rigid mug to place.
- ``mug_target``: a marker linked to the mug (used as a handle-side reference).

Extra Observations
------------------

Bimanual make-coffee adds (under ``obs["state"]["other"]``):

- ``machine_pos`` (shape ``(n_envs, 3)``)
- ``mug_pos`` (shape ``(n_envs, 3)``)

Termination
-----------

This task is still being finalized. In the current code, reward and
success/failure checks are not enabled, so episodes typically end by horizon
truncation.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 1000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/rigid/bimanual_make_coffee.py``
