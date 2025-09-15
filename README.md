# Mitigating Metropolitan Carbon Emissions with Eco-driving at Scale

Code for 'Mitigating Metropolitan Carbon Emissions with Eco-driving at Scale' published at Transportation Research Part C: Emerging Technologies (TR-C) 2025.

## Installation
1. Install SUMO (ideally 1.12, but 1.13 seems to work as well) according to your OS, and make sure that the env var SUMO_HOME is set.
2. Create a conda env or venv with python 3.7
3. Install dependencies `pip install -r requirements.txt`

## Run Instructions (local)
`<dir>` is where all the training artifacts will be stored and/or the checkpoints will be retrieved (to evaluate or restart the training). Will be created if it doesn't exist.

If you haven't set the `WANDB_API_KEY` env var (see below), set `WANDB_MODE` to `offline`.

### Examples
From the root of the repo and the correct venv:

`python code/main.py --dir <exp_dir>`

`python code/main.py --dir <exp_dir> --kwargs <python dict with arguments to override the config in main.py>`

Example:
`python code/main.py --dir wd/best_agent_based --kwargs "{'n_steps':30, 'run_mode':'full_eval'}" `

## Getting started

### Config
The default config is stored in `containers/config.py` along with documentation for each field.
Important fields:

- `run_mode`, can be set to 'train',  'single_eval'
(i.e. runs a single episode, useful for visualisation or a quick check) or 'full_eval'
(i.e. evaluates all the possible environments as specified)
- `task_context` a `TaskContext` object which specifies which environments are used
  - When training/single_eval an env is chosen uniformly at random, in full eval each possible env configuration will be run
  - Can either be a `NetGetTaskContext`, i.e. a synthetic dataset (good for training), or a `PathTaskContext` i.e. a real world dataset
  - see `containers/task_context` for more details.
- `n_steps` how many eval steps in training mode or different random seeds to use in eval mode
- `moves_emissions_models` uses specified MOVES surrogates for emissions modelling, none by default. Can be multiple condition to evaluate many scenarios at once (multiple weather for example).
Not recommended for training

### TaskContexts

Used to specify environments.

Typical example for training:
```python
task = NetGenTaskContext(
    base_id=[11],
    penetration_rate=[0.2],
    single_approach=True,
    inflow=ContinuousSelector(200, 400, 4),
    lane_length=ContinuousSelector(100, 600, 4),
    speed_limit=ContinuousSelector(6.5, 30, 4),
    green_phase=ContinuousSelector(30, 45, 3),
    red_phase=ContinuousSelector(30, 45, 4),
    offset=ContinuousSelector(0, 1, 5),
)
```

Example for evaluating on a synthetic dataset:
```python
task = NetGenTaskContext(
    base_id=[11],
    penetration_rate=[0.2],
    single_approach=False,
    inflow=ContinuousSelector(200, 400, 3),
    lane_length=ContinuousSelector(100, 600, 4),
    speed_limit=[10, 13, 20, 30],
    green_phase=35,
    red_phase=35,
    offset=0,
)
```

Example for evaluating on the dataset contained in the repo, one approach at a time:
```python
task = PathTaskContext(
    dir=Path('dataset'),
    single_approach=True,
    penetration_rate=0.2
)
```
### Datasets

The dataset used in the paper is available [here](https://drive.google.com/drive/folders/1y3W83MPfnt9mSFGbg8L9TLHTXElXvcHs). If you are using this dataset, please consider citing the following paper.

```
bibtex
@article{intersectionzoo2025,
  title   = {IntersectionZoo: Eco-driving for Benchmarking Multi-Agent Contextual Reinforcement Learning, },
  author  = {V. Jayawardana, B. Freydt, A. Qu, C. Hickert, Z. Yan, C. Wu},
  journal = {International Conference on Learning Representations (ICLR)},
  year    = {2025},
}
```

### Citing

If you are using this codebase, please consider citing the following paper.

```bibtex
@article{jayawardana2025mitigating,
  title   = {Mitigating Metropolitan Carbon Emissions with Eco-driving at Scale},
  author  = {V. Jayawardana, B. Freydt, A. Qu, C. Hickert, E. Sanchez, C. Tang, M. Tylor, B. Leonard, C. Wu},
  journal = {Transportation Research Part C: Emerging Technologies},
  year    = {2025},
  publisher = {Elsevier}
}
```

###  Troubleshooting

#### If you get `OSError: AF_UNIX path length cannot exceed 107 bytes:`
This might happen for batch jobs on Supercloud.

#### Solution

The best way to solve it is to (okay you usually should NEVER do that) modify line 183 of `.conda/envs/no-stop/lib/python3.7/site-packages/ray/node.py`
(the local installation of ray !) into this : `date_str = datetime.datetime.today().strftime("%H%M%S%f")`.

Basically this changes the name of ray sessions into a shorter name.

#### Anyhting else

Please open a Github issue. 
