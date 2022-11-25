from __future__ import annotations
from typing import List, Union
import pymunk
from bball_server.player import Player
from bball_server.physics_object import PhysicsObject

AddableObject = Union[pymunk.Body, pymunk.Shape, pymunk.Constraint]


class Space:
    _space: pymunk.Space
    _players: List[Player]

    def __init__(self):
        self._space = pymunk.Space()
        self._players = []

    def add(self, obj: AddableObject) -> Space:
        self._space.add(obj)
        return self

    def add_player(self, player: Player) -> Space:
        self._add_physics_object(player._physics)
        self._players.append(player)
        return self

    def _add_physics_object(self, physics_object: PhysicsObject) -> Space:
        self._space.add(physics_object._body)
        return self

    def step(self, steps: int) -> Space:
        for _ in range(steps):
            for player in self._players:
                player._step()
            self._space.step(1)
        return self
