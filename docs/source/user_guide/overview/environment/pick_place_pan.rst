Pick Place Pan
==============

Task key: ``pick_place_pan``.

``pick_place_pan`` is a single-arm rigid-object task. A frying pan starts on a
hot plate and must be placed onto a kitchen mat.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Pick the pan from the hot plate and place it on the mat.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "pick_place_pan",
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

- ``hot_plate``: fixed hot plate (visual).
- ``kitchen_mat``: fixed mat (visual) + ``mat_collision`` box (collision).
- ``pan``: rigid pan to place.
- ``pan_target``: marker linked to the pan (used as a reference point).

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

- **Success:** pan rests on the mat inside an inner XY region and within a Z tolerance, while the TCP is clear for several frames.
- **Failure:** pan leaves the workspace AABB, or a fast drop is detected while the TCP is far.
- **Truncation:** episode reaches the horizon.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 500`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/rigid/pick_place_pan.py``
