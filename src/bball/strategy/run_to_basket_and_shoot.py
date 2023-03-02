from dataclasses import dataclass, field
from bball.team import other_team_index
from bball.strategy.strategy_interface import StrategyInterface
from bball.strategy.run_to_target_and_shoot import RunToTargetAndShoot


@dataclass
class RunToBasketAndShoot(StrategyInterface):
    distance_threshold: float
    _strategy: RunToTargetAndShoot = field(init=False)

    def _after_team_set(self):
        target_hoop = self._game.court.hoop(other_team_index(self._team_index))
        self._strategy = RunToTargetAndShoot(target_hoop, self.distance_threshold)
        self._strategy.for_team_index_in_game(self._team_index, self._game)

    def _drive(self):
        self._strategy.drive(self._time_frame)
