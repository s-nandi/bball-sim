from dataclasses import dataclass
from bball.player import Player
from bball.utils import Point, distance_between
from bball.ball.state import BallState
from bball.ball.ball_mode import BallMode


@dataclass
class ShotParameters:
    shooter: Player
    target: Point
    location: Point
    probability: float


@dataclass
class ReachedShot(BallState):
    shooter: Player
    target: Point
    location: Point

    def parameters(self):
        distance = distance_between(self.location, self.target)
        shot_probability = self.shooter._attributes.skill.shot_probability
        return ShotParameters(
            self.shooter,
            self.target,
            self.location,
            shot_probability.probability(distance),
        )

    @staticmethod
    def mode() -> BallMode:
        return BallMode.REACHEDSHOT
