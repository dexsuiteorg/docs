Controllers
===========

Controllers map an action tensor to simulator commands for a robot.

You pick controller *keys* (strings) for the arm and the gripper:

* Flat API: ``arm_control="<key>"`` and ``gripper_control="<key>"``
* Component API: pass ``ControllerOptions(name="<key>", config={...})``

Quickstart
----------

.. code-block:: python

   import dexsuite as ds

   env = ds.make(
       "lift",
       manipulator="franka",
       gripper="robotiq",
       arm_control="osc_pose",
       gripper_control="joint_position",
   )

Normalization (``normalized``)
------------------------------

Most controllers support a ``normalized`` flag.

* If ``normalized=True`` (default), actions are expected in ``[-1, 1]`` and are
  mapped into physical units using the controller config (for example
  ``lin_scale`` or ``v_max``).
* If ``normalized=False``, actions are interpreted directly in physical units
  (for example meters/radians, rad/s, or N*m depending on the controller).
* ``clip`` controls whether inputs are clamped to the allowed range.

Default Controller Config
-------------------------

Defaults live in ``dexsuite/config/env_configs/controllers.yaml``. DexSuite
loads these when you construct ``RobotOptions`` (and when you use the flat API).

Controller Reference
--------------------

.. list-table::
   :widths: 16 14 40 30
   :header-rows: 1

   * - Key
     - Action dim
     - What it commands
     - Config keys
   * - ``joint_position``
     - ``dof``
     - Joint position targets. Normalized maps ``[-1,1]`` to joint limits.
     - ``normalized``, ``clip``
   * - ``joint_velocity``
     - ``dof``
     - Joint velocity targets. Normalized uses ``v = a * v_max``.
     - ``normalized``, ``clip``, ``v_max``
   * - ``joint_torque``
     - ``dof``
     - Joint torque/force commands. Normalized uses ``tau = a * tau_max``.
     - ``normalized``, ``clip``, ``tau_max``
   * - ``osc_pose``
     - ``6``
     - End-effector delta pose (XYZ + RPY) solved by IK each step.
     - ``normalized``, ``clip``, ``lin_scale``, ``ang_scale``
   * - ``osc_pose_abs``
     - ``6``
     - End-effector pose offset from a captured origin pose (XYZ + RPY).
     - ``normalized``, ``clip``, ``lin_range``, ``ang_range``, ``ik_max_iters`` (opt), ``ik_damping`` (opt)
   * - ``osc_pose_abs_quat``
     - ``7``
     - End-effector pose offset from origin (XYZ + delta quaternion, wxyz).
     - ``normalized``, ``clip``, ``lin_range``, ``ik_max_iters`` (opt), ``ik_damping`` (opt)
   * - ``ik_pose``
     - ``6``
     - Absolute end-effector target pose (XYZ + RPY) solved by IK each step.
     - ``normalized``, ``clip`` (opt), ``ik_max_iters``, ``ik_damping``, ``ik_max_step`` (opt), ``ik_init``

Notes
-----

* Joint controllers (``joint_*``) have ``dof`` actions, where ``dof`` is the
  number of controlled joints for that arm/gripper.
* ``osc_pose_abs`` and ``osc_pose_abs_quat`` capture an origin pose on first use.
  If you want a fresh origin, recreate the env (or add a helper to recapture).
