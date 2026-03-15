Available Environments
======================

DexSuite environments are selected by the *task key* you pass to ``ds.make(...)``.

Task keys are case-insensitive (they are normalized with ``.lower()``).

Each task page documents the scene entities, observations, success conditions,
and any task-specific notes.

.. code-block:: python

   import dexsuite as ds

   env = ds.make("lift", manipulator="franka", gripper="robotiq")


Single-Arm Baselines
--------------------

.. list-table::
   :widths: 18 32 50
   :header-rows: 1

   * - Task key
     - Image
     - Description
   * - :doc:`reach <reach>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Reach a target pose.
   * - :doc:`lift <lift>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Lift a cube to a target height.
   * - :doc:`push <push>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Push an object towards a goal region.
   * - :doc:`pick_place <pick_place>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Pick and place an object.
   * - :doc:`stack <stack>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Stack one cube on another.


Single-Arm Rigid Tasks
----------------------

.. list-table::
   :widths: 18 32 50
   :header-rows: 1

   * - Task key
     - Image
     - Description
   * - :doc:`make_coffee <make_coffee>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Place a mug on the coffee machine tray.
   * - :doc:`pick_place_mug <pick_place_mug>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Place a mug into a dish rack.
   * - :doc:`pick_place_pan <pick_place_pan>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Pick and place a pan.
   * - :doc:`drill_to_point <drill_to_point>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Move a drill tip to a target point.


Single-Arm Deformable Tasks
---------------------------

.. list-table::
   :widths: 18 32 50
   :header-rows: 1

   * - Task key
     - Image
     - Description
   * - :doc:`cable_routing <cable_routing>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Route a cable through clip fixtures.
   * - :doc:`cut_butter <cut_butter>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Cut a deformable butter block.
   * - :doc:`pour_water <pour_water>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Pour water from a bottle into a cup.
   * - :doc:`foldshirt <foldshirt>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Fold a cloth shirt.
   * - :doc:`spready_butter <spready_butter>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Spread a deformable butter block with a tool.
   * - :doc:`mpm_sponge_drop <mpm_sponge_drop>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Soft sponge scene.


Single-Arm Misc Tasks
---------------------

.. list-table::
   :widths: 18 32 50
   :header-rows: 1

   * - Task key
     - Image
     - Description
   * - :doc:`rotatedice <rotatedice>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Interact with a dice object.


Bimanual Baselines
------------------

.. list-table::
   :widths: 18 32 50
   :header-rows: 1

   * - Task key
     - Image
     - Description
   * - :doc:`bimanual_reach <bimanual_reach>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Reach a goal with two arms.
   * - :doc:`bimanual_lift <bimanual_lift>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Lift an object with two arms.
   * - :doc:`bimanual_push <bimanual_push>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Push an object with two arms.
   * - :doc:`bimanual_pick_place <bimanual_pick_place>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Bimanual pick-and-place baseline.
   * - :doc:`bimanual_stack <bimanual_stack>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Stack three cubes with two arms.


Bimanual Rigid Tasks
--------------------

.. list-table::
   :widths: 18 32 50
   :header-rows: 1

   * - Task key
     - Image
     - Description
   * - :doc:`bimanual_make_coffee <bimanual_make_coffee>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Place a mug on the coffee machine tray.
   * - :doc:`bimanual_pick_place_mug <bimanual_pick_place_mug>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Pick and place a mug with two arms.
   * - :doc:`bimanual_pick_place_pan <bimanual_pick_place_pan>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Pick and place a pan with two arms.
   * - :doc:`bimanual_drill_to_point <bimanual_drill_to_point>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Move a drill tip to a target point with two arms.
   * - :doc:`bimanual_pick_place_pot <bimanual_pick_place_pot>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Pick and place a pot with two arms.
   * - :doc:`bimanual_fold_glasses <bimanual_fold_glasses>`
     - .. image:: ../../../_static/placeholder_env.svg
          :width: 260
     - Fold glasses.

.. toctree::
   :maxdepth: 1
   :hidden:

   lift
   reach
   push
   pick_place
   stack
   make_coffee
   pick_place_mug
   pick_place_pan
   drill_to_point
   cable_routing
   cut_butter
   rotatedice
   foldshirt
   pour_water
   spready_butter
   mpm_sponge_drop
   bimanual_reach
   bimanual_lift
   bimanual_push
   bimanual_pick_place
   bimanual_stack
   bimanual_make_coffee
   bimanual_pick_place_mug
   bimanual_pick_place_pan
   bimanual_pick_place_pot
   bimanual_fold_glasses
   bimanual_drill_to_point
