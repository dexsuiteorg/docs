Cable Routing
=============

Task key: ``cable_routing``.

``cable_routing`` is a single-arm deformable-object task focused on routing a
cable across fixtures.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Status
------

This task has not yet been migrated to the current options-first ``BaseEnv`` API
and is not runnable via ``ds.make`` in the current codebase.

Goal
----

- Route the cable across the clip fixtures on the board.

Task Entities
-------------

- ``board``: fixed peg board mesh (visual) + ``board_col`` (collision box).
- ``clip_neg`` / ``clip_mid`` / ``clip_pos``: fixed clips.
- ``cable``: cable entity.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

Success/reward logic is not implemented yet; episodes typically end by horizon
truncation once the task is migrated.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 1``
- ``HORIZON = 2000000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/cable_routing.py``
