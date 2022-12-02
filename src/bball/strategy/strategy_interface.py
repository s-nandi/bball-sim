from abc import ABC, abstractmethod
from bball.game import Game
from bball.team import Team


class StrategyInterface(ABC):
    def __init__(self, _team: Team, _time_frame: float, *_args):
        pass

    @abstractmethod
    def drive(self, game: Game):
        pass
