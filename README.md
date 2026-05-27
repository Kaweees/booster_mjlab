# k1_mjlab

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

Before attempting to build this project, make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Just](https://just.systems/man/en/installation.html) installed on your machine.

### Installation

To get a local copy of the project up and running on your machine, follow these simple steps:

1. Clone the project repository

   ```sh
   git clone https://github.com/Kaweees/booster_mjlab.git
   ```

2. Install the project dependencies

   ```sh
   just install
   ```

3. Train the policy

    ```sh
    clear && just run k1_train Mjlab-Velocity-Rough-Booster-K1 --env.scene.num-envs 4096 --video True --video-length 200 --video-interval 500 --agent.logger tensorboard
    ```

4. Play the trained model

   ```sh
   clear && just run k1_play Mjlab-Velocity-Rough-Booster-K1 --checkpoint-file [path-to-checkpoint] --num-envs 64 --viewer viser --video True --video-length 200
   ```

### Available Tasks

| Task ID | Robot | Description | Preview |
| --- | --- | --- | --- |
| `Mjlab-Velocity-Flat-Booster-K1` | Booster K1 | Velocity tracking on flat terrain | <img alt="Velocity tracking on flat terrain preview" src="assets/gifs/velocity_flat_booster_teaser.gif" width="200"> |
| `Mjlab-Velocity-Rough-Booster-K1` | Booster K1 | Velocity tracking on rough terrain | <img alt="Velocity tracking on rough terrain preview" src="assets/gifs/velocity_rough_booster_teaser.gif" width="200"> |
