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
Run `python -m pylint src experiment tests && python -m mypy src tests experiment`

## Formatting
Run `python -m black src tests experiment`

## Testing
Run `python -m pytest`