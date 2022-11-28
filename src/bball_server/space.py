from __future__ import annotations
from typing import List, Union, Iterable, Set
import pymunk
from bball_server.ball import Ball
from bball_server.player import Player
from bball_server.game import Game
from bball_server.physics_object import PhysicsObject

AddableObject = Union[Player, Ball, Game]


class Space:
    _space: pymunk.Space
    _players: List[Player]
    _balls: List[Ball]
    _games: List[Game]
    _ids: Set[int]

    def __init__(self):
        self._space = pymunk.Space()
        self._players = []
        self._balls = []
        self._games = []
        self._ids = set()

    def add(self, *objs: AddableObject) -> Space:
        for obj in objs:
            self._add_single_object(obj)
        return self

    def _add_single_object(self, obj: AddableObject) -> Space:
        if id(obj) in self._ids:
            return self
        self._ids.add(id(obj))
        if isinstance(obj, Player):
            return self._add_player(obj)
        if isinstance(obj, Ball):
            return self._add_ball(obj)
        if isinstance(obj, Game):
            return self._add_game(obj)
        assert False, f"Cannot add object of type {type(obj)} to space"

    def _add_player(self, player: Player) -> Space:
        self._add_physics_object(player._physics)
        self._players.append(player)
        return self

    def _add_physics_object(self, physics_object: PhysicsObject) -> Space:
        self._space.add(physics_object._body)
        return self

    def _add_ball(self, ball: Ball) -> Space:
        assert len(self._balls) == 0
        self._balls.append(ball)
        return self

    def _add_game(self, game: Game) -> Space:
        assert len(self._games) == 0
        self._games.append(game)
        for team in game.teams:
            for player in team:
                self.add(player)
        self.add(game.ball)
        return self

    def step(self, time_frame: float) -> Space:
        substeps_per_unit_time = 1
        time_per_substep = time_frame / substeps_per_unit_time
        for _ in range(substeps_per_unit_time):
            self._substep(time_per_substep)
        for player in self._players:
            player._reset()
        return self

    def _substep(self, time_frame: float):
        self._step_each(self._players, time_frame)
        self._space.step(time_frame)
        self._step_each(self._balls, time_frame)
        self._step_each(self._games, time_frame)

    def _step_each(self, objs: Iterable[AddableObject], time_frame: float):
        for obj in objs:
            obj._step(time_frame)
