# Training

<p class="ds-lede">The baselines are trained with robomimic on the HDF5 export of a dataset and evaluated in DexSuite.
The scripts live in <code>scripts/imitation_learning/robomimic/</code>.</p>

## 1. Download and convert

```bash
python -m scripts.imitation_learning.robomimic.download_dataset --repo dexsuite/lift_franka_allegro --out ./datasets --robomimic
```

`--robomimic` converts the dataset after downloading. To convert one you already have:

```bash
python -m scripts.imitation_learning.robomimic.lerobot_to_hdf5 --repo dexsuite/lift_franka_allegro --out datasets/lift_allegro
```

| Option | Default | Meaning |
|---|---|---|
| `--split` | `train` | dataset split |
| `--no-images` | off | skip camera frames, for state-based training |
| `--video-backend` | `auto` | `pyav`, `video_reader` or `decord` |
| `--compression` | `none` | `gzip` to shrink the file, `--compression-opts` sets the level |
| `--read-workers`, `--block-size` | 8, 128 | decoding parallelism |

The HDF5 file follows robomimic's layout, `data/demo_k/{actions, rewards, dones, states, obs, next_obs}`, plus the
action split per component under `action/` and an `action_config.json` next to it.

## 2. Make a config

```bash
python -m scripts.imitation_learning.robomimic.make_config_from_dataset \
    --base <robomimic base config.json> --dataset-root datasets/lift_allegro --obs-profile lowdim --out lift_allegro.json
```

`--obs-profile lowdim` uses the robot and task state, `cameras` adds the images. The observation and action keys are
read from the dataset, so the config always matches it.

## 3. Train

```bash
python -m scripts.imitation_learning.robomimic.train --config lift_allegro.json
```

Training rolls the policy out in DexSuite during training and saves checkpoints with their success rate in the file
name, which is step 2 of the [protocol](benchmark.md#protocol).

```{note}
The rollouts use a DexSuite environment wrapper for robomimic (`robomimic.envs.env_dexsuite`), so install a robomimic
build that includes it.
```

## 4. Evaluate

```bash
python -m scripts.imitation_learning.robomimic.eval --agent <checkpoint.pth> --n-rollouts 50 --seed 0
```

Run it for three seeds and report the mean and the standard deviation, as in the [benchmark](benchmark.md).

| Option | Default | Meaning |
|---|---|---|
| `--n-rollouts` | 50 | episodes |
| `--horizon` | 400 | step limit |
| `--seed` | 0 | evaluation seed |
| `--video-path`, `--video-skip` | | save a video, every n-th frame |
| `--render` | off | open the viewer |

## Reinforcement learning

`scripts/reinforcement_learning/` has PPO and TD3 examples with skrl on Reach, using many parallel environments
(`--n_envs 64`).
