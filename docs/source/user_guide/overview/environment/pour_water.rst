Pour Water
==========

Task key: ``pour_water``.

``pour_water`` is a single-arm fluid task intended to pour water from a bottle
into a cup using SPH simulation.

.. image:: ../../../_static/placeholder_env.svg
   :width: 420

Status
------

This task has not yet been migrated to the current options-first ``BaseEnv`` API
and is not runnable via ``ds.make`` in the current codebase.

Goal
----

- Pour water from the bottle into the cup.

Extra Observations
------------------

The current implementation exposes (under ``obs["state"]["other"]``):

- ``bottle_pos`` (shape ``(n_envs, 3)``)
- ``cup_pos`` (shape ``(n_envs, 3)``)

Termination
-----------

The current file returns a zero reward and never reports success.

Simulation Settings
-------------------

- ``SIM_DT = 0.01``
- ``SUBSTEPS = 20``
- ``HORIZON = 40000`` control steps

Source
------

- ``Dexsuite/dexsuite/environments/single/prototypes/pour_water.py``
