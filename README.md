# bball-sim

## Dependencies
* Python 3
    * Pygame
    * Pymunk
    * Pytorch
    * Stable Baselines 3
    * Tqdm
    * Pylint
    * Pytest
    * Black

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