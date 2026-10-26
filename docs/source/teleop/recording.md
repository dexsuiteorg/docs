# Recording

<p class="ds-lede">The LeRobot logger writes each step of an environment to a LeRobot dataset: every observation,
the action, the outcome, and the robot's action layout, so a dataset can be replayed on the same robot later.</p>

```bash
pip install "dexsuite[datasets]"      # LeRobot 0.4.4, the version the logger and the datasets are written with
```

## The logger

```python
import dexsuite as ds
from dexsuite.utils.lerobot_logger import LeRobotLogger

env = ds.make("lift", manipulator="franka", gripper="allegro")
log = LeRobotLogger("lift", env, root_dir="collected_dataset")

obs, info = env.reset(seed=0)
while True:
    action = ...                                      # from a device or a policy
    nxt, reward, terminated, truncated, info = env.step(action)
    log.add_step_pre(obs, action, reward, terminated, truncated, info)
    obs = nxt
    if terminated.any() or truncated.any():
        if info["success"].any():
            log.save_episode()                        # keep it
        else:
            log.clear_buffer()                        # drop it
        break
log.close()
```

`add_step_pre` records the observation from before the action, together with that action and what followed.
`save_episode` writes the buffered episode, `clear_buffer` throws it away, including its video frames.

## What is stored

Every leaf of the observation becomes a feature, flattened with dots:

| Feature | Content |
|---|---|
| `obs.state.manipulator.qpos`, ... | robot state, one feature per key |
| `obs.state.other.cube_pos`, ... | task state |
| `obs.cameras.front.rgb`, ... | camera images, stored as video |
| `action` | the action vector |
| `reward`, `terminated`, `truncated`, `success`, `failure` | the step's outcome |
| `task` | the task key |

The frame rate is the control rate. Two files go into `meta/`:

- `action_layout.json`: the action slices (name, start, stop, width, controller type), see
  [Actions](../concepts/actions.md).
- `env_config.json`: the simulator, robot and camera options the dataset was recorded with.

By default a dataset lands in `collected_dataset/<task>/<task>_<yymmdd_HHMMSS>`, with the LeRobot repo id
`lerobot/dexsuite_<task>_<arm>_<end-effector>`. Opening an existing folder with the same features and frame rate
appends to it.

## Collection scripts

The scripts in `scripts/data_collection/` set up a task, a robot and a device, and save successful episodes. Run them
from the repository root.

### SpaceMouse

```bash
python -m scripts.data_collection.spacemouse_datacollection
```

Lift with a Franka and an Allegro hand, `osc_pose` for the arm and `joint_position` for the hand, front, wrist and side
cameras. Edit the top of the script to change the task or the robot.

(manus-glove-and-vive-tracker)=
### Manus glove and Vive tracker

The setup used for the human demonstrations: a Vive tracker on the operator's wrist drives the hand pose, and the
Manus glove, through GeoRT, drives the fingers.

```bash
python scripts/data_collection/manus_datacollection.py \
    --task pick_place_pan --manipulator franka --end-effector allegro \
    --vive-backend steamvr --tracker-endpoint tcp://<steamvr-host>:5559 \
    --manus-url ws://127.0.0.1:8767 --dataset-root collected_dataset
```

| Option | Default | Meaning |
|---|---|---|
| `--task` | `pick_place_pan` | task key |
| `--manipulator`, `--end-effector` | `floating`, `allegro` | robot |
| `--vive-backend` | `steamvr` | where the tracker poses come from |
| `--tracker-endpoint`, `--tracker-topic`, `--tracker-id`, `--tracker-side` | | ZeroMQ source of the tracker |
| `--manus-url` | `ws://127.0.0.1:8767` | GeoRT WebSocket |
| `--success-only` / `--no-success-only` | on | save only successful episodes |
| `--dataset-root` | `collected_dataset` | output folder |
| `--haptics` | off | buzz the glove when the Allegro fingertips touch something |

Keys while recording: `r` recalibrates the tracker to the current hand pose, `d` drops the episode and resets. The
arm uses `osc_pose_abs_quat` and the hand unnormalized `joint_position`, with front and wrist cameras in RGB and depth.
`manus_bimanual_datacollection.py` is the two-arm version (two trackers, two gloves).

## Upload to Hugging Face

```bash
python -m scripts.data_collection.push_to_hub --path collected_dataset/lift/lift_241023_101500 --owner <hf-user> --private
```

The repository name comes from the dataset's `meta/env_config.json`. `--push-videos/--no-push-videos` controls the
camera videos and `--upload-large-folder` uses the resumable uploader for big datasets.
