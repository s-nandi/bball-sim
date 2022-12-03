from bball.strategy import CompositeStrategy, RunToBasketAndShoot, StandBetweenBasket


def create_strategy(offensive_distance_threshold: float = 5.0):
    return CompositeStrategy(
        RunToBasketAndShoot(offensive_distance_threshold),
        StandBetweenBasket(),
    )
