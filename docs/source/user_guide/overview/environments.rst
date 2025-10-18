.. include:: ../_shared_nav.rst
Environments
====================
Dexsuite offers a variety of pre-built environments to facilitate simulation and testing. These environments include different tasks and setups for both singular and bimanual operations.
In **Dexsuite**, an **environment** is where everything happens: It is where the simulation is running, where observations are retrieved, and where action steps are applied. In this overview, we will walk you through the different methods to create an environment.

There are three main functions that are related to the environment:

-   :code:`make()`: Creates the environment based on the input options
-   :code:`get_obs()`: Retrieves the observations from the environment. It can contain the robot's positions, the cameras' output and/or the environment's data
-   :code:`step()`: Sends an action to the environment for the robot to execute

For :code:`get_obs()` and :code:`step()`


Singular
--------------------
(coming soon.)

Bimanual
--------------------
(coming soon.)