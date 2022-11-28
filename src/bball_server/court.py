from typing import Tuple


from bball_server.player import Player


class Court:
    _width: float
    _height: float

    def __init__(self, dimensions: Tuple[float, float]):
        self._width = dimensions[0]
        self._height = dimensions[1]

    def is_inbounds(self, player: Player) -> bool:
        position = player.position
        x_in_bounds = 1 <= position[0] <= self._width
        y_in_bounds = 1 <= position[1] <= self._height
        return x_in_bounds and y_in_bounds
