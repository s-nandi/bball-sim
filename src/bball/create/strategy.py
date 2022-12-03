from bball.strategy import CompositeStrategy, RunToBasketAndShoot, StandBetweenBasket


def create_strategy(time_frame: float, offensive_distance_threshold: float = 5.0):
    return CompositeStrategy(
        RunToBasketAndShoot(time_frame, offensive_distance_threshold),
        StandBetweenBasket(time_frame),
    )
