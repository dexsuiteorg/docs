Cut Butter
==========

Task key: ``cut_butter``.

``cut_butter`` is a single-arm deformable-object task that uses an MPM butter
block and knife props.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Status
------

This task has not yet been migrated to the current options-first ``BaseEnv`` API
and is not runnable via ``ds.make`` in the current codebase.

Goal
----

- Cut the butter block using the knife.

Task Entities
-------------

- ``board``: cutting board mesh.
- ``butter``: MPM deformable block.
- ``knife``: rigid knife mesh.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

Success/reward logic is not implemented yet; episodes typically end by horizon
truncation once the task is migrated.

Simulation Settings
-------------------

- ``SIM_DT = 0.005``
- ``SUBSTEPS = 20``
- ``HORIZON = 2000000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/cut_butter.py``
