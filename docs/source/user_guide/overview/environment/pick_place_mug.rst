Pick Place Mug
==============

Task key: ``pick_place_mug``.

``pick_place_mug`` is a single-arm rigid-object task. A dish rack and a mug are
spawned, and the agent must place the mug into the rack.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Goal
----

- Place the mug into the dish rack.

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "pick_place_mug",
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

- ``rack``: dish rack.
- ``mug``: rigid mug.

Extra Observations
------------------

Pick-place-mug adds (under ``obs["state"]["other"]``):

- ``rack_pos`` (shape ``(n_envs, 3)``)
- ``mug_pos`` (shape ``(n_envs, 3)``)

Termination
-----------

In the current code, reward and success/failure checks are not enabled, so
episodes typically end by horizon truncation.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 2``
- ``HORIZON = 400`` control steps

Notes
-----

- The repository contains a legacy implementation registered under the same key; import order determines which one wins in the registry.

Source
------

- ``Dexsuite/dexsuite/environments/single/rigid/pick_place_mug.py``
- ``Dexsuite/dexsuite/environments/single/prototypes/pick_and_place_mug.py``
