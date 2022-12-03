from __future__ import annotations
from typing import List, Union, Sequence, Set
import pymunk
from bball.ball import Ball
from bball.player import Player
from bball.game import Game
from bball.team import Team, Teams
from bball.physics_object import PhysicsObject

AddableObject = Union[Player, Ball, Game, Team, Teams]
StoredObject = Union[Player, Ball, Game]


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
        if isinstance(obj, Team):
            return self._add_team(obj)
        if isinstance(obj, Teams):
            return self._add_teams(obj)
        if isinstance(obj, Ball):
            return self._add_ball(obj)
        if isinstance(obj, Game):
            return self._add_game(obj)
        assert False, f"Cannot add object of type {type(obj)} to space"

    def _add_player(self, player: Player) -> Space:
        self._add_physics_object(player._physics)
        self._players.append(player)
        return self

    def _add_team(self, team: Team) -> Space:
        for player in team:
            self._add_player(player)
        return self

    def _add_teams(self, teams: Teams) -> Space:
        for team in teams:
            self._add_team(team)
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
        self._run_strategies(self._games)
        self._step_each(self._players, time_frame)
        self._space.step(time_frame)
        if self._step_one(self._balls, time_frame):
            return
        if self._step_one(self._games, time_frame):
            return

    def _run_strategies(self, games: Sequence[Game]):
        if len(games) == 0:
            return
        for team in games[0].teams:
            if team._strategy is not None:
                team._strategy.drive()

    def _step_each(self, objs: Sequence[StoredObject], time_frame: float):
        for obj in objs:
            obj._step(time_frame)

    def _step_one(self, objs: Sequence[StoredObject], time_frame: float) -> bool:
        if len(objs) == 0:
            return False
        assert len(objs) == 1
        return objs[0]._step(time_frame)
