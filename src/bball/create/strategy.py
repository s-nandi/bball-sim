from typing import Optional
from bball.strategy import (
    CompositeStrategy,
    RunToBasketAndShoot,
    StandBetweenBasket,
    SpacePassShoot,
)


def create_strategy(shooting_distance: float = 5.0):
    return CompositeStrategy(
        RunToBasketAndShoot(shooting_distance),
        StandBetweenBasket(),
    )


def created_spaced_strategy(
    shooting_distance: float = 5.0,
    spacing_distance: Optional[float] = None,
    make_passes: bool = False,
):
    if spacing_distance is None:
        spacing_distance = shooting_distance
    return CompositeStrategy(
        SpacePassShoot(shooting_distance, spacing_distance, make_passes),
        StandBetweenBasket(),
    )
