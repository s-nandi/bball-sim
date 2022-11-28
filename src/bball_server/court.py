from typing import Tuple


from bball_server.player import Player


class Court:
    _dimensions: Tuple[float, float]

    def __init__(self, dimensions: Tuple[float, float]):
        self._dimensions = dimensions

    def is_inbounds(self, player: Player) -> bool:
        position = player.position
        inbounds = True
        for dimension in range(2):
            inbounds &= 1 <= position[dimension] <= self._dimensions[dimension]
        return inbounds
