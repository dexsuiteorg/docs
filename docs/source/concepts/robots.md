# Robots

<p class="ds-lede">A robot is built from parts at <code>ds.make</code> time. Tasks never refer to a particular robot, so
the same task runs with a two-finger gripper on a UR5e or a 22-joint hand on a floating wrist.</p>

```{raw} html
:file: ../_static/diagrams/robot.svg
```

## Four kinds

Modular arm + end-effector
: An arm (`franka`, `ur5`, `gen3`, ...) and any end-effector with an adapter for it. The adapter places an optional
  mount piece and the end-effector on the arm's last link. Most tasks use this.

Integrated robot
: A robot model that includes its own gripper: `franka_with_gripper`, `aloha_tactile`, `gen3_lite`, `so_100`,
  `trossen_vx300s`, `trossen_wx250s`. It is one body in the simulator. DexSuite still exposes the gripper joints
  separately, so the observation and the action look the same as for a modular robot.

Floating wrist
: `manipulator="floating"` is a virtual 6-DoF gantry (x, y, z, roll, pitch, yaw) without geometry. It carries a Sharpa
  or Allegro hand alone, for tasks where the arm is not the point.

Two arms
: `RobotOptions(type_of_robot="bimanual", left=..., right=...)`, or a pair of keys in the direct form. Each side is
  one of the kinds above, and the [layout](workspaces.md#two-arms) decides where they stand.

```python
ds.make("lift", manipulator="ur5", gripper="leap")                          # modular
ds.make("lift", manipulator="trossen_vx300s")                               # integrated
ds.make("spray_graffiti", manipulator="floating", gripper="sharpa_fardexbot")  # floating wrist
ds.make("bimanual_reach", manipulator=("ur5", "ur5"), gripper="robotiq")     # two arms
```

## How a modular robot is put together

1. The arm is loaded from its model file and fixed at its base pose.
2. The adapter for this arm and end-effector is read from `dexsuite/models/manipulators/<arm>/<arm>_adapters.yaml`.
   It gives the mount piece (invisible, a cylinder, a box or a mesh) and the pose of the end-effector on the arm's
   last link.
3. The end-effector is loaded and welded to the mount, which is welded to the arm.
4. Joint gains, limits and the home pose come from the arm and end-effector model classes.

If the adapter file has no entry for the pair, `ds.make` raises `ValueError: Adapter missing` and lists the
end-effectors that do fit. The [compatibility table](../robots/compatibility.md) shows every pair.

## Home pose and gains

Every arm defines `home_q`, the joint configuration it starts each episode in, and every end-effector defines its open
configuration. Position gains (`kp`, `kv`) and force limits live on the model classes in `dexsuite/models/`. The
[catalog](../robots/arms.md) lists each robot's degrees of freedom and model source.

## The TCP

Each end-effector defines a tool centre point (`tcp_pose`) relative to its root link, for example 16 cm out from the
Robotiq base. `obs["state"]["gripper"]["tcp_pos"]` reports it, and the pose controllers move it.

## Adding robots

New arms and end-effectors are registered with a decorator and a small model class.
[Add an arm](../how-to/new-arm.md) and [Add an end-effector](../how-to/new-end-effector.md) show both.
