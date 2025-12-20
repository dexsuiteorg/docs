MPM Sponge Drop
===============

Task key: ``mpm_sponge_drop``.

``mpm_sponge_drop`` is a minimal single-arm deformable-object scene that drops a
soft sponge mesh.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Status
------

This task has not yet been migrated to the current options-first ``BaseEnv`` API
and is not runnable via ``ds.make`` in the current codebase.

Goal
----

- Interact with a deformable sponge.

Task Entities
-------------

- ``sponge``: deformable sponge mesh.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

The current file returns a zero reward and never reports success.

Simulation Settings
-------------------

- ``SIM_DT = 0.005``
- ``SUBSTEPS = 10``
- ``HORIZON = 5000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/sponge.py``
