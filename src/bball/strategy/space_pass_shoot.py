from __future__ import annotations
from random import choices, random
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
from bball.behavior import RunPastPosition
from bball.utils import (
    position_of,
    sum_of,
    DEFAULT_EPS,
    clamp,
    polar_to_cartesian,
    in_range,
)
from bball.strategy.strategy_interface import StrategyInterface

if TYPE_CHECKING:
    from bball.player import Player


@dataclass
class SpacePassShoot(StrategyInterface):
    spacing_distance: float
    shot_quality_threshold: float
    pass_probability: float
    dive_to_basket: bool
    _behaviors: List[RunPastPosition] = field(init=False)
    _shot_quality_metric: List[float] = field(init=False)

    def _target_position_and_distance_for(self, player: Player, player_index: int):
        target_hoop = self._game.target_hoop(player)
        position = position_of(target_hoop)
        if player == self._game.ball.last_belonged_to and self.dive_to_basket:
            return (position, DEFAULT_EPS)

        team_size = len(self._team)
        assert team_size > 0
        half_court = self._game.target_half_court(player)

        angle = (player_index) * (180.0 / (team_size - 1)) - 90
        offset = polar_to_cartesian(angle, self.spacing_distance)
        offset_position = sum_of(position, offset)

        target_coefficients = half_court.position_to_multiplier(offset_position)
        clamped_coefficients = (
            clamp(target_coefficients[0], 0, 1),
            clamp(target_coefficients[1], 0, 1),
        )
        return (half_court.multiplier_to_position(clamped_coefficients), DEFAULT_EPS)

    def _shot_clock_coeff(self) -> float:
        total_shot_clock = self._game.settings.shot_clock_duration
        if total_shot_clock == float("inf"):
            return 1.0
        proportion = self._game.shot_clock / total_shot_clock
        shot_clock_coeff = proportion**2
        assert in_range(shot_clock_coeff, 0.0, 1.0)
        return shot_clock_coeff

    def _shot_quality_for(self, player: Player):
        target_hoop = self._game.target_hoop(player)
        expected_value = target_hoop.expected_value_of_shot_by(player)
        return expected_value

    def update(self):
        self._behaviors = [
            RunPastPosition(*self._target_position_and_distance_for(player, index))
            for index, player in enumerate(self._team)
        ]
        self._shot_quality_metric = [
            self._shot_quality_for(player) for player in self._team
        ]

    def _after_team_set(self):
        self.update()

    def _drive(self):
        self.update()
        for behavior, player in zip(self._behaviors, self._team):
            target_hoop = self._game.target_hoop(player)
            if player.has_ball:
                coeff = self._shot_clock_coeff()
                shot_quality = self._shot_quality_for(player)
                threshold = self.shot_quality_threshold * coeff
                good_shot = shot_quality > threshold
                low_time = self._game.shot_clock < 1.0
                if good_shot or low_time:
                    player.shoot_at(target_hoop.position)
                    return
                if random() < self.pass_probability:

                    receiver = choices(self._team, self._shot_quality_metric)[0]
                    if receiver != player:
                        player.pass_to(receiver)
                        return
            behavior.drive(player, self._time_frame)
