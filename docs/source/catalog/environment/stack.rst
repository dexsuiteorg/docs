Stack
=====

Task key: ``stack``.

``stack`` is a single-arm baseline task. Three cubes are spawned and the agent
must stack them into a tower: A (red) at the bottom, B (blue) in the middle,
and C (green) on top.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Stack the three cubes into a stable tower (A, then B, then C).

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "stack",
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

- ``cube_a``: bottom cube (red).
- ``cube_b``: middle cube (blue).
- ``cube_c``: top cube (green).

Extra Observations
------------------

Stack adds (under ``obs["state"]["other"]``):

- ``cube_a_pos``, ``cube_b_pos``, ``cube_c_pos`` (each shape ``(n_envs, 3)``)
- ``cube_a_quat``, ``cube_b_quat``, ``cube_c_quat`` (each shape ``(n_envs, 4)``, wxyz)

Termination
-----------

- **Success:** cube B is placed on cube A, and cube C is placed on cube B (within tolerances).
- **Failure:** none beyond horizon truncation.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 600`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/baselines/stack.py``
