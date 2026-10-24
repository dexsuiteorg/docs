# Scripted collection

<p class="ds-lede">Scripted experts plan a motion for each task and record it with the same logger as teleoperation.
They produced the scripted tier of the dataset for the UMI gripper.</p>

```bash
python -m scripts.automated_data_collection.lift_automated --episodes 200 --dataset-root collected_dataset
```

There is one script per Track 1 task: `reach_automated`, `lift_automated`, `push_automated`, `pick_place_automated`
and `stack_automated`. Each plans way-points around the objects, interpolates them into a smooth trajectory and drives
the hand with the `osc_pose_abs_quat` controller. The action has 9 values: the wrist position change, the change of
orientation as a quaternion `(w, x, y, z)`, and two gripper values.

## Main options

| Option | Default | Meaning |
|---|---|---|
| `--manipulator`, `--gripper` | `franka`, `franka_umi_tacticle` | robot |
| `--episodes` | 10 | successful episodes to collect |
| `--max-attempts` | | stop after this many tries |
| `--max-steps` | 800 | step limit per episode |
| `--control-hz` | 20 | control rate |
| `--cameras` | `front,wrist,right_side` | cameras to record, or `none` |
| `--dataset-root` | | output folder |
| `--save-all` | off | also keep failed episodes |
| `--no-record`, `--dry-run` | off | run without writing a dataset |
| `--viewer`, `--visualize-tcp` | off | watch it |
| `--video-out`, `--video-camera`, `--video-every` | | save preview videos |
| `--arm-mode` | | `open_loop`, `closed_loop` or `smooth` way-point following |
| `--grasp-retries` | | how often to retry a missed grasp |

Only successful episodes are saved unless `--save-all` is given. The scripts need `roboticstoolbox-python` for the
trajectory interpolation.

## Benchmarking the experts

```bash
python -m scripts.automated_data_collection.benchmark_baselines --tasks reach,lift,pick_place,push,stack --episodes 5
```

reports how often each scripted expert succeeds, which is a quick check after changing a task.
