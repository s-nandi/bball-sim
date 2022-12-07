from dataclasses import dataclass
from bball import Player, Space, Ball, BallMode
from bball.utils import close_to, approx
from bball.create import (
    create_initialized_player,
    create_space,
    create_ball,
    create_linear_shot_probability,
    create_player_attributes,
)


@dataclass
class ShootingTest:
    space: Space
    ball: Ball
    shooter: Player


def setup_shooting_test(shot_distance, shot_velocity) -> ShootingTest:
    shooter = create_initialized_player(
        attributes=create_player_attributes(shot_velocity=shot_velocity)
    )
    ball = create_ball()
    space = create_space().add(shooter, ball)
    ball.jump_ball_won_by(shooter)
    assert shooter.has_ball
    shooter.shoot_at((shot_distance, 0))
    space.step(0)
    return ShootingTest(space, ball, shooter)


def test_possession_ends_after_shooting():
    test = setup_shooting_test(1, 2)
    test.space.step(1)
    assert not test.shooter.has_ball


def test_ball_position_mid_shot():
    shot_distance = 4
    test = setup_shooting_test(shot_distance, shot_velocity=1)
    for time_since_shot in range(shot_distance + 1):
        assert close_to(test.ball.position, (time_since_shot, 0))
        test.space.step(1)
    assert test.ball.mode == BallMode.REACHEDSHOT


def test_shot_probability():
    max_shot_distance = 10
    shot_probability = create_linear_shot_probability(
        max_shot_distance=max_shot_distance
    )
    assert approx(shot_probability(0), 1.0)
    assert approx(shot_probability(max_shot_distance), 0.0)
    assert approx(shot_probability(max_shot_distance / 2), 0.5)
    assert approx(shot_probability(7), 3 / 10)
    assert approx(shot_probability(3), 7 / 10)
