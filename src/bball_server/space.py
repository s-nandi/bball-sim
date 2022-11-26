from __future__ import annotations
from typing import List, Union
import pymunk
from bball_server.player import Player
from bball_server.passing_server import PassingServer
from bball_server.physics_object import PhysicsObject

AddableObject = Union[Player, PassingServer]


class Space:
    _space: pymunk.Space
    _players: List[Player]
    _passing_servers: List[PassingServer]

    def __init__(self):
        self._space = pymunk.Space()
        self._players = []
        self._passing_servers = []

    def add(self, obj: AddableObject) -> Space:
        if isinstance(obj, Player):
            return self._add_player(obj)
        if isinstance(obj, PassingServer):
            return self._add_passing_server(obj)
        else:
            assert False, f"Cannot add object of type {type(obj)} to space"

    def _add_player(self, player: Player) -> Space:
        self._add_physics_object(player._physics)
        self._players.append(player)
        return self

    def _add_physics_object(self, physics_object: PhysicsObject) -> Space:
        self._space.add(physics_object._body)
        return self

    def _add_passing_server(self, passing_server: PassingServer) -> Space:
        self._passing_servers.append(passing_server)
        return self

    def step(self, time_frame: float) -> Space:
        substeps_per_unit_time = 1
        time_per_substep = time_frame / substeps_per_unit_time
        for _ in range(substeps_per_unit_time):
            for player in self._players:
                player._step(time_per_substep)
            for passing_server in self._passing_servers:
                passing_server._step(time_per_substep)
            self._space.step(time_per_substep)
        for player in self._players:
            player._reset()
        return self
