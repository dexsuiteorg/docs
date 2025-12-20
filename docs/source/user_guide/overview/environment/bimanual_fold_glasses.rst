Bimanual Fold Glasses
=====================

Task key: ``bimanual_fold_glasses``.

``bimanual_fold_glasses`` is a two-arm rigid-object task. A pair of glasses
rests on a tray and the agent must fold the hinges.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Fold the glasses hinges into the folded range.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "bimanual_fold_glasses",
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

- ``tray``: fixed tray mesh.
- ``glasses``: glasses URDF with hinge joints.

Extra Observations
------------------

Bimanual fold-glasses adds (under ``obs["state"]["other"]``):

- ``tray_top_z`` (shape ``(1,)`` in the current implementation)
- ``hinge_angles`` (shape ``(2,)`` in the current implementation)
- ``glasses_pos`` (shape ``(n_envs, 3)``)

Termination
-----------

This task is still being finalized. In the current code, reward and
success/failure checks are not enabled, so episodes typically end by horizon
truncation.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 2``
- ``HORIZON = 40000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/bimanual/rigid/bimanual_fold_glasses.py``
