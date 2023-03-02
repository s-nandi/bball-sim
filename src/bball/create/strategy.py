from bball.strategy import (
    CompositeStrategy,
    RunToBasketAndShoot,
    StandBetweenBasket,
    SpacePassShoot,
)


def create_strategy(shooting_distance: float = 5.0, defensive_tightness=0.5):
    return CompositeStrategy(
        RunToBasketAndShoot(shooting_distance),
        StandBetweenBasket(defensive_tightness),
    )


def created_spaced_strategy(
    spacing_distance: float = 5.0,
    shot_quality_threshold: float = 1.0,
    pass_probability: float = 0.5,
    dive_to_basket: bool = False,
    defensive_tightness: float = 0.5,
):
    return CompositeStrategy(
        SpacePassShoot(
            spacing_distance, shot_quality_threshold, pass_probability, dive_to_basket
        ),
        StandBetweenBasket(defensive_tightness),
    )
