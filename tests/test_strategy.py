import pytest
from bball import Team, BallMode
from bball.strategy import EveryoneRunToBasketStrategy, StandBetweenBasket
from bball.utils import distance_between
from bball.create import (
    create_initialized_player,
    create_space,
    create_game,
    create_court,
)


def test_run_to_basket_strategy():
    player = create_initialized_player()
    game = create_game(teams=[Team(player)])
    space = create_space().add(player)
    ball = game.ball
    ball.jump_ball_won_by(player)

    time_frame = 1
    steps = 20
    threshold = 5
    strategy = EveryoneRunToBasketStrategy(
        team=game.teams[0], distance_threshold=threshold, time_frame=time_frame
    )
    target_hoop = game.target_hoop(player)
    did_shoot = False
    for _ in range(steps):
        is_close_enough = (
            distance_between(player.position, target_hoop.position) <= threshold
        )
        strategy.drive(game)
        space.step(time_frame)
        if ball.mode in [BallMode.MIDSHOT, BallMode.REACHEDSHOT]:
            did_shoot = True
        if is_close_enough:
            assert did_shoot
    assert did_shoot


@pytest.mark.parametrize("attacker_accel", [0.1, 0.5, 0.8, 0.9, 1.0])
def test_stand_between_player_and_basket(attacker_accel):
    width = 20
    height = 10
    initial_padding = 3
    player_1 = create_initialized_player(position=(0, height / 2))
    player_2 = create_initialized_player(position=(initial_padding, height / 2))
    court = create_court(width, height)
    game = create_game(teams=[Team(player_1), Team(player_2)], court=court)
    space = create_space().add(game)
    ball = game.ball
    ball.jump_ball_won_by(player_1)
    player_1.accelerate(attacker_accel)
    time_frame = 0.1
    strategy = StandBetweenBasket(team=game.teams[1], time_frame=time_frame)
    target_hoop = game.target_hoop(player_1)
    for _ in range(width - initial_padding - 1):
        assert player_1.position[0] <= target_hoop.position[0]
        assert player_1.position[0] <= player_2.position[0] <= target_hoop.position[0]
        strategy.drive(game)
        space.step(time_frame)
