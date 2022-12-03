import math
import pytest
from bball import Team, BallMode
from bball.strategy import RunToBasketAndShoot, StandBetweenBasket
from bball.utils import distance_between
from bball.create import (
    create_initialized_player,
    create_space,
    create_game,
    create_court,
    create_guaranteed_shot_probability,
    create_player_attributes,
    create_strategy,
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
    strategy = RunToBasketAndShoot(threshold).for_team_index_in_game(0, game)
    target_hoop = game.target_hoop(player)
    did_shoot = False
    for _ in range(steps):
        is_close_enough = (
            distance_between(player.position, target_hoop.position) <= threshold
        )
        strategy.drive(time_frame)
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
    strategy = StandBetweenBasket().for_team_index_in_game(1, game)
    target_hoop = game.target_hoop(player_1)
    for _ in range(width - initial_padding - 1):
        assert player_1.position[0] <= target_hoop.position[0]
        assert player_1.position[0] <= player_2.position[0] <= target_hoop.position[0]
        strategy.drive(time_frame)
        space.step(time_frame)


def test_scoring_with_composite_strategy():
    duration = 50
    time_frame = 0.2
    attributes = create_player_attributes(
        shot_probability=create_guaranteed_shot_probability()
    )
    player_1 = create_initialized_player(position=(4, 4), attributes=attributes)
    player_2 = create_initialized_player(position=(7, 7), attributes=attributes)
    court = create_court()
    game = create_game(teams=[Team(player_1), Team(player_2)], court=court)
    space = create_space().add(game)
    for team_index in range(2):
        game.assign_team_strategy(team_index, create_strategy(time_frame))
    num_steps = math.ceil(duration / time_frame)
    for _ in range(num_steps):
        space.step(time_frame)
    assert game.score[0] > 0 and game.score[1] > 0


def test_stay_relatively_on_court_with_composite_strategy():
    duration = 300
    time_frame = 0.2
    attributes = create_player_attributes(
        shot_probability=create_guaranteed_shot_probability(), max_acceleration=2.5
    )
    player_1 = create_initialized_player(position=(4, 4), attributes=attributes)
    player_2 = create_initialized_player(position=(7, 7), attributes=attributes)
    court = create_court(28, 15)
    game = create_game(teams=[Team(player_1), Team(player_2)], court=court)
    space = create_space().add(game)
    game.assign_team_strategy(0, create_strategy(5))
    game.assign_team_strategy(1, create_strategy(3))
    num_steps = math.ceil(duration / time_frame)

    def assert_relatively_on_court(player, threshold: float):
        position_x = player.position[0]
        position_y = player.position[1]
        width = court.width
        height = court.height
        assert position_x >= -threshold
        assert position_x <= width + threshold
        assert position_y >= -threshold
        assert position_y <= height + threshold

    threshold = 1
    for _ in range(num_steps):
        assert_relatively_on_court(player_1, threshold)
        assert_relatively_on_court(player_2, threshold)
        space.step(time_frame)
