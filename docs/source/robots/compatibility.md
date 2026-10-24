# Compatibility

<p class="ds-lede">Which end-effector mounts on which arm. A pair is available when the arm's adapter file has an entry
for the end-effector.</p>

✓ available, ⚠ available but the adapter mounts it at the wrong angle today, empty: no adapter.

| Arm | `robotiq` | `franka_umi_tacticle` | `barrett` | `dclaw` | `inspire` | `ability` | `schunk` | `allegro` | `leap` | `sharpa` | `shadow` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `franka` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `franka_fr3` |  |  |  |  |  |  |  |  |  |  |  |
| `gen3` | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |  | ✓ |
| `kuka` | ⚠ |  | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ |  |  | ⚠ |
| `sawyer` | ⚠ |  | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ |  |  | ⚠ |
| `ur5` | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |  |
| `ur10` | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |  | ✓ |
| `lite6` | ⚠ |  | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ |  |  | ⚠ |
| `link6` | ⚠ |  | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ |  |  | ⚠ |
| `z1` | ⚠ |  | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ |  |  | ⚠ |
| `floating` |  |  |  |  |  |  |  | ✓ |  | ✓ |  |

Adapters live next to each arm in `dexsuite/models/manipulators/<arm>/<arm>_adapters.yaml`. Each entry places an
optional mount piece and the end-effector relative to the arm's last link; [Add an end-effector](../how-to/new-end-effector.md)
shows the format. Asking for a pair without an entry raises `ValueError: Adapter missing`.

Integrated robots (`franka_with_gripper`, `aloha_tactile`, `gen3_lite`, `so_100`, `trossen_vx300s`,
`trossen_wx250s`) always use their own gripper.
