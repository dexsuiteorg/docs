.. include:: ../_shared_nav.rst
Controllers
====================
Dexsuite offers a selection of controllers.

Base Controller
--------------------
The base controller class defines the common interface and provides helper methods for
interacting with simulation entities, handling batched environments, and
managing control commands.
    
.. py:class:: Controller(entity, model, broadcast_single_to_batch: bool = False, home_q_broadcast: bool = True)

    :ivar entity: The simulation entity that this controller will operate on.
    :vartype entity: Any
    :ivar model: The robot component model associated with the entity.
    :vartype model: Any
    :ivar dofs_idx: A list of the specific degree-of-freedom indices to control.
    :vartype dofs_idx: list[int]
    :ivar broadcast_single_to_batch: If True, allow 1D actions to be broadcast
        to all environments in a batched simulation.
    :vartype broadcast_single_to_batch: bool
    :ivar home_q_broadcast: If True, allow a 1D home configuration to be
        broadcast to all environments in a batched simulation.
    :vartype home_q_broadcast: bool
    :ivar n_envs: The number of parallel environments.
    :vartype n_envs: int
    :ivar kp: Proportional gains for the controller.
    :vartype kp: Optional[torch.Tensor]
    :ivar kv: Derivative gains for the controller.
    :vartype kv: Optional[torch.Tensor]
    :ivar force_range: The force/torque limits for the actuators.
    :vartype force_range: Optional[torch.Tensor]

    .. py:attribute:: dof
        :property:

        Return the number of controlled degrees of freedom.

        :rtype: int

    .. py:method:: post_build()

        Perform post-build setup, such as installing runtime gains.

        This method is typically called after the simulation world has been fully built.

        :rtype: None

    .. py:method:: install_runtime_gains()

        Set the PD gains and force limits on the simulation entity.

        This uses the values from the :attr:`kp`, :attr:`kv`, and :attr:`force_range` attributes.

        :rtype: None

    .. py:method:: set_home_position()

        Set the entity's joints to the model's home position.

        It respects the :attr:`dofs_idx` and handles batched environments based on :attr:`home_q_broadcast`.

        :raises ValueError: If the sliced home position length doesn't match the controller's DoF count, or if batched-mode requirements for ``home_q`` are not met.
        :rtype: None

    .. py:method:: action_space()

        Define the action space for the controller.

        This is an abstract method and must be implemented by subclasses.

    .. py:method:: step(action)

        Apply a control action.

        The action is passed to the abstract :meth:`_apply_cmd` method.

        :param action: The action to apply, typically a :class:`torch.Tensor`.
        :type action: Any
        :rtype: None

Other controllers inherent from the base controller are listed below. All controllers except IK pose have an option (default: ``False``) to normalize the
output for machine learning applications.

Other Controllers
--------------------
- Joint Position
- Joint Velocity
- Joint Torque
- Inverse Kinematics (IK) Pose
- Operational Space Control (OSC) Pose
- Operational Space Control (OSC) Pose Absolute