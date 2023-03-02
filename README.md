# bball-sim

## Dependencies

- Python 3
  - Pygame
  - Pymunk
  - Pytorch
  - Stable Baselines 3
  - Tqdm
  - Pylint
  - Pytest
  - Black

## Setup

1. Install [pytorch](https://pytorch.org/get-started/locally/)
2. Run
   ```
   python -m pip install pygame pymunk stable-baselines3 pylint mypy pytest black tqdm
   ```

## Linting

Run `python -m pylint src experiment tests && python -m mypy src tests experiment`

## Formatting

Run `python -m black src tests experiment`

## Testing

Run `python -m pytest`

# ML Agent

## Training

Run

```
python -m src.neural.basic_offense learn 10000000000 10000000 output/basic_offense
```

or

```
python -m src.neural.basic_offense learn 10000000000 10000000 output/basic_offense --epoch ${EPOCH}
```

to continue training from a specific epoch

Run

```
tensorboard --logdir output/basic_offense
```

to visualize training progress

## Testing

Run

```
python -m src.neural.basic_offense load 20 output/basic_offense
```

to visualize 20 runs of the latest model or

```
python -m src.neural.basic_offense load 20 output/basic_offense --epoch ${EPOCH}
```

to visualize a specific epoch
