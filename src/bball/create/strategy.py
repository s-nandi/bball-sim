from bball.team import Team
from bball.strategy import CompositeStrategy, RunToBasketAndShoot, StandBetweenBasket


def create_strategy(
    team: Team, time_frame: float, offensive_distance_threshold: float = 5.0
):
    return CompositeStrategy(
        team,
        time_frame,
        RunToBasketAndShoot,
        dict(distance_threshold=offensive_distance_threshold),
        StandBetweenBasket,
        None,
    )
