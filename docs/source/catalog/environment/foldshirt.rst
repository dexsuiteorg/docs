Fold Shirt
==========

Task key: ``foldshirt``.

``foldshirt`` is a single-arm cloth task that spawns a T-shirt mesh as a
deformable object.

.. image:: ../../_static/placeholder_env.svg
   :width: 420

Status
------

This task has not yet been migrated to the current options-first ``BaseEnv`` API
and is not runnable via ``ds.make`` in the current codebase.

Goal
----

- Fold the cloth shirt.

Task Entities
-------------

- ``tshirt``: cloth mesh entity.

Extra Observations
------------------

This task currently does not add extra observations beyond robot state.

Termination
-----------

This file does not currently implement reward or success conditions.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 10``
- ``HORIZON = 150`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/fold_shirt.py``
