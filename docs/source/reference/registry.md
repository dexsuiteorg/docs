# Registry

<p class="ds-lede">Every name <code>ds.make</code> understands, read from the registration decorators in the source.
The <a href="../tasks/index.html">task catalog</a> documents the tasks that are ready to use.</p>

Tasks (33)
: `bimanual_drill_to_point`, `bimanual_fold_glasses`, `bimanual_lift`, `bimanual_make_coffee`, `bimanual_pick_place`, `bimanual_pick_place_mug`, `bimanual_pick_place_pan`, `bimanual_pick_place_pot`, `bimanual_push`, `bimanual_reach`, `bimanual_stack`, `bimanual_stack_mid_air`, `cable_routing`, `cut_butter`, `drill_to_point`, `foldshirt`, `lift`, `make_coffee`, `mpm_sponge_drop`, `open_jar`, `pick_place`, `pick_place_fruit`, `pick_place_mug`, `pick_place_pan`, `pour_water`, `push`, `put_bread_toaster`, `reach`, `rotateDice`, `spray_graffiti`, `spready_butter`, `stack`, `tool_hang`

Arms and robots (17)
: `aloha_tactile`, `floating`, `franka`, `franka_fr3`, `franka_with_gripper`, `gen3`, `gen3_lite`, `kuka`, `link6`, `lite6`, `sawyer`, `so_100`, `trossen_vx300s`, `trossen_wx250s`, `ur10`, `ur5`, `z1`

End-effectors (19)
: `ability`, `allegro`, `allegro_left`, `allegro_right`, `barrett`, `dclaw`, `franka_umi_tacticle`, `inspire`, `leap`, `leap_left`, `leap_right`, `robotiq`, `schunk`, `shadow`, `shadow_left`, `shadow_right`, `sharpa`, `sharpa_left`, `sharpa_right`

Controllers (7)
: `ik_pose`, `joint_position`, `joint_torque`, `joint_velocity`, `osc_pose`, `osc_pose_abs`, `osc_pose_abs_quat`

Names are case-insensitive. Registration happens when `dexsuite` is imported, which walks `dexsuite.models` and
`dexsuite.environments`. Code outside the package registers its classes when it is imported.

```python
from dexsuite.core.registry import register_env, register_manipulator, register_gripper
```
