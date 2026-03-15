Reach
=====

Task key: ``reach``.

``reach`` is a single-arm baseline task. A fixed, non-colliding sphere is
spawned as a target, and the agent must move the tool center point (TCP) to the
target position.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Move the TCP to the target sphere.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "reach",
       manipulator="franka",
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

- ``target_sphere``: a fixed, non-colliding sphere (visual marker).

Extra Observations
------------------

Reach adds (under ``obs["state"]["other"]``):

- ``target_pos`` (shape ``(n_envs, 3)``)
- ``target_quat`` (shape ``(n_envs, 4)``, wxyz convention)

Termination
-----------

- **Success:** TCP is within 3 cm of the target.
- **Failure:** none beyond horizon truncation.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 100`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/baselines/reach.py``
