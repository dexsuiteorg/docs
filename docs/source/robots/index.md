# Robots

<p class="ds-lede">A robot in DexSuite is an arm and an end-effector, chosen by name when the environment is made.
Modular arms take any end-effector with an adapter for them, integrated robots come with their own gripper, and the
floating wrist carries a hand on its own.</p>

```python
# a modular arm with a hand
env = ds.make("lift", manipulator="ur5", gripper="allegro")

# an integrated robot, with its built-in gripper
env = ds.make("lift", manipulator="so_100")

# a hand on its own, on the floating wrist
env = ds.make("put_bread_toaster", manipulator="floating", gripper="sharpa_fardexbot")
```

How the parts are joined is described in [Robots](../concepts/robots.md). Which pairs are available is in the
[compatibility table](compatibility.md).

## Arms

<div class="ds-grid">
<a class="ds-tile" href="arms.html#franka"><img src="../_static/catalog/arm_franka.webp" alt="Franka Panda" loading="lazy"><div class="ds-tile-text"><b>Franka Panda</b><small>7 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#gen3"><img src="../_static/catalog/arm_gen3.webp" alt="Kinova Gen3" loading="lazy"><div class="ds-tile-text"><b>Kinova Gen3</b><small>7 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#kuka"><img src="../_static/catalog/arm_kuka.webp" alt="KUKA LBR iiwa 14" loading="lazy"><div class="ds-tile-text"><b>KUKA LBR iiwa 14</b><small>7 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#sawyer"><img src="../_static/catalog/arm_sawyer.webp" alt="Rethink Sawyer" loading="lazy"><div class="ds-tile-text"><b>Rethink Sawyer</b><small>7 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#ur5"><img src="../_static/catalog/arm_ur5.webp" alt="UR5e" loading="lazy"><div class="ds-tile-text"><b>UR5e</b><small>6 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#ur10"><img src="../_static/catalog/arm_ur10.webp" alt="UR10e" loading="lazy"><div class="ds-tile-text"><b>UR10e</b><small>6 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#lite6"><img src="../_static/catalog/arm_lite6.webp" alt="UFactory Lite 6" loading="lazy"><div class="ds-tile-text"><b>UFactory Lite 6</b><small>6 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#link6"><img src="../_static/catalog/arm_link6.webp" alt="Link6" loading="lazy"><div class="ds-tile-text"><b>Link6</b><small>6 DoF arm</small></div></a>
<a class="ds-tile" href="arms.html#z1"><img src="../_static/catalog/arm_z1.webp" alt="Unitree Z1" loading="lazy"><div class="ds-tile-text"><b>Unitree Z1</b><small>6 DoF arm</small></div></a>
</div>

## Integrated robots

<div class="ds-grid">
<a class="ds-tile" href="arms.html#franka_with_gripper"><img src="../_static/catalog/robot_franka_with_gripper.webp" alt="Franka Panda with Franka Hand" loading="lazy"><div class="ds-tile-text"><b>Franka Panda with Franka Hand</b><small>7 + 2 DoF</small></div></a>
<a class="ds-tile" href="arms.html#aloha_tactile"><img src="../_static/catalog/robot_aloha_tactile.webp" alt="ALOHA (tactile)" loading="lazy"><div class="ds-tile-text"><b>ALOHA (tactile)</b><small>6 + 2 DoF</small></div></a>
<a class="ds-tile" href="arms.html#gen3_lite"><img src="../_static/catalog/robot_gen3_lite.webp" alt="Kinova Gen3 Lite" loading="lazy"><div class="ds-tile-text"><b>Kinova Gen3 Lite</b><small>6 + 1 DoF</small></div></a>
<a class="ds-tile" href="arms.html#so_100"><img src="../_static/catalog/robot_so_100.webp" alt="SO-100" loading="lazy"><div class="ds-tile-text"><b>SO-100</b><small>5 + 1 DoF</small></div></a>
<a class="ds-tile" href="arms.html#trossen_vx300s"><img src="../_static/catalog/robot_trossen_vx300s.webp" alt="Trossen ViperX 300 S" loading="lazy"><div class="ds-tile-text"><b>Trossen ViperX 300 S</b><small>6 + 1 DoF</small></div></a>
<a class="ds-tile" href="arms.html#trossen_wx250s"><img src="../_static/catalog/robot_trossen_wx250s.webp" alt="Trossen WidowX 250 S" loading="lazy"><div class="ds-tile-text"><b>Trossen WidowX 250 S</b><small>6 + 1 DoF</small></div></a>
</div>

## End-effectors

<div class="ds-grid">
<a class="ds-tile" href="end-effectors.html#robotiq"><img src="../_static/catalog/ee_robotiq.webp" alt="Robotiq 2F-85" loading="lazy"><div class="ds-tile-text"><b>Robotiq 2F-85</b><small>Parallel-jaw gripper, 1 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#umi"><img src="../_static/catalog/ee_umi.webp" alt="UMI gripper" loading="lazy"><div class="ds-tile-text"><b>UMI gripper</b><small>Parallel-jaw gripper, 1 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#franka_umi_tacticle"><img src="../_static/catalog/ee_franka_umi_tacticle.webp" alt="UMI tactile gripper" loading="lazy"><div class="ds-tile-text"><b>UMI tactile gripper</b><small>Parallel-jaw gripper with tactile pads, 2 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#barrett"><img src="../_static/catalog/ee_barrett.webp" alt="BarrettHand" loading="lazy"><div class="ds-tile-text"><b>BarrettHand</b><small>Three-finger hand, 8 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#dclaw"><img src="../_static/catalog/ee_dclaw.webp" alt="D&#x27;Claw" loading="lazy"><div class="ds-tile-text"><b>D&#x27;Claw</b><small>Three-finger hand, 9 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#inspire"><img src="../_static/catalog/ee_inspire.webp" alt="Inspire Hand" loading="lazy"><div class="ds-tile-text"><b>Inspire Hand</b><small>Five-finger hand, 6 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#ability"><img src="../_static/catalog/ee_ability.webp" alt="Ability Hand" loading="lazy"><div class="ds-tile-text"><b>Ability Hand</b><small>Five-finger hand, 6 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#schunk"><img src="../_static/catalog/ee_schunk.webp" alt="Schunk SVH" loading="lazy"><div class="ds-tile-text"><b>Schunk SVH</b><small>Five-finger hand, 9 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#allegro"><img src="../_static/catalog/ee_allegro.webp" alt="Allegro Hand" loading="lazy"><div class="ds-tile-text"><b>Allegro Hand</b><small>Four-finger hand, 16 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#leap"><img src="../_static/catalog/ee_leap.webp" alt="LEAP Hand" loading="lazy"><div class="ds-tile-text"><b>LEAP Hand</b><small>Four-finger hand, 16 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#sharpa"><img src="../_static/catalog/ee_sharpa.webp" alt="Sharpa Wave" loading="lazy"><div class="ds-tile-text"><b>Sharpa Wave</b><small>Five-finger hand, 22 DoF</small></div></a>
<a class="ds-tile" href="end-effectors.html#shadow"><img src="../_static/catalog/ee_shadow.webp" alt="Shadow Hand" loading="lazy"><div class="ds-tile-text"><b>Shadow Hand</b><small>Five-finger hand, 24 DoF</small></div></a>
</div>

```{toctree}
:hidden:
:maxdepth: 1

arms
end-effectors
compatibility
```
