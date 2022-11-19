# bball-sim

## Dependencies
* Python 3
    * Pygame
    * Pymunk
    * Pylint
    * Pytest
    * Black

## Setup
Run 
```
python -m pip install pygame pymunk pylint mypy pytest black
```

## Linting
Run `python -m pylint src tests && python -m mypy src tests`

## Formatting
Run `python -m black src tests`

## Testing
Run `python -m pytest src tests`