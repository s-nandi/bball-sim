from abc import ABC, abstractmethod
from bball.ball.ball_mode import BallMode


class BallState(ABC):
    def _step(self, _time_frame: float) -> bool:
        return False

    def _reset(self) -> None:
        return

    @staticmethod
    @abstractmethod
    def mode() -> BallMode:
        pass
