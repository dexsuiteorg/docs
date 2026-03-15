Spready Butter
==============

Task key: ``spready_butter``.

``spready_butter`` is a single-arm deformable-object task intended to spread an
MPM butter block using a knife prop.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Status
------

This task has not yet been migrated to the current options-first ``BaseEnv`` API
and is not runnable via ``ds.make`` in the current codebase.

Goal
----

- Spread the butter over the toast.

Task Entities
-------------

- ``toast``: fixed toast mesh.
- ``butter``: MPM deformable block.
- ``knife``: rigid knife mesh.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

The current file returns a zero reward and never reports success.

Simulation Settings
-------------------

- ``SIM_DT = 0.005``
- ``SUBSTEPS = 20``
- ``HORIZON = 2000000`` control steps

Notes
-----

- The task key is spelled ``spready_butter`` in the current registry.

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/spread_butter.py``
