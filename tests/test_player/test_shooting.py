from dataclasses import dataclass
from bball_server import Player, Space, Ball
from ..utils import create_initialized_player, create_space, create_ball, close_to


@dataclass
class ShootingTest:
    space: Space
    ball: Ball
    shooter: Player


def setup_shooting_test(shot_distance, shot_velocity) -> ShootingTest:
    shooter = create_initialized_player(position=(0, 0))
    ball = create_ball()
    space = create_space().add(shooter, ball)
    ball.give_to(shooter)
    assert shooter.has_ball
    shooter.shoot_at((shot_distance, 0), shot_velocity=shot_velocity)
    return ShootingTest(space, ball, shooter)


def test_posession_ends_after_shooting():
    test = setup_shooting_test(1, 2)
    test.space.step(1)
    assert not test.shooter.has_ball


def test_ball_position_mid_shot():
    shot_distance = 4
    test = setup_shooting_test(shot_distance, shot_velocity=1)
    for time_since_shot in range(shot_distance + 1):
        assert close_to(test.ball.position, (time_since_shot, 0))
        test.space.step(1)
