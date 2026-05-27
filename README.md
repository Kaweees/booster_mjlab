# k1_mjlab

```sh
uv run k1_list_envs
```

```sh
just tensorboard
```

```sh
just run k1_train Mjlab-Velocity-Rough-Booster-K1 --env.scene.num-envs 4096 --video True --video-length 200 --video-interval 500 --agent.logger tensorboard
```

```sh
just run k1_train Mjlab-Velocity-Flat-Booster-K1 --env.scene.num-envs 4096 --video True ---video-length 200 --video-interval 500 --agent.logger tensorboard
```

```sh
just run k1_record Mjlab-Velocity-Rough-Booster-K1 --checkpoint-file logs/rsl_rl/k1_velocity/[timestamp]/model_1950.pt --num-envs 12 --num-steps 1000
```

```sh
just run k1_play Mjlab-Velocity-Rough-Booster-K1 --checkpoint-file [path-to-checkpoint] --video True --video-length 200

just run k1_play Mjlab-Velocity-Flat-Booster-K1 --checkpoint-file [path-to-checkpoint] --video True --video-length 200
```

  ### Available Tasks
  
  | Task ID | Robot | Description | Preview |
  | --- | --- | --- | --- |
  | `Mjlab-Velocity-Rough-Booster-K1` | Booster T1 | Velocity tracking on rough terrain | <img alt="Velocity tracking on rough terrain preview" src="assets/gifs/velocity_rough_booster_teaser.gif" width="200"> |
  | `Mjlab-Velocity-Flat-Booster-K1` | Booster T1 | Velocity tracking on flat terrain | <img alt="Velocity tracking on flat terrain preview" src="assets/gifs/velocity_flat_booster_teaser.gif" width="200"> |
