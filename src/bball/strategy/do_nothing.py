from bball.strategy.strategy_interface import StrategyInterface


class DoNothing(StrategyInterface):
    def _after_team_set(self):
        pass

    def _drive(self):
        pass
