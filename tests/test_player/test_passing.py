import math
from dataclasses import dataclass
from bball_server import Player, Space, Ball, BallMode
from bball_server.utils import close_to
from ..utils import create_space, create_ball, create_initialized_player


@dataclass
class PassingTest:
    space: Space
    ball: Ball
    passer: Player
    receiver: Player


def check_pass_completes_after(test: PassingTest, expected_time: int):
    space = test.space
    ball = test.ball
    for _ in range(expected_time):
        assert ball.mode == BallMode.MIDPASS
        space.step(1)
    assert ball.mode == BallMode.RECEIVEDPASS


def setup_passing_test(pass_distance, pass_velocity) -> PassingTest:
    passer = create_initialized_player(position=(0, 0))
    receiver = create_initialized_player(position=(pass_distance, 0))
    ball = create_ball()
    space = create_space().add(passer, receiver, ball)
    ball.jump_ball_won_by(passer)
    assert passer.has_ball
    assert not receiver.has_ball
    passer.pass_to(receiver, pass_velocity=pass_velocity)
    space.step(0)
    return PassingTest(space, ball, passer, receiver)


def calculate_time_to_complete(
    pass_distance: float, pass_velocity: float, receiver_speed: float
) -> float:
    # pass_distance + time_to_complete * receiver_speed == pass_velocity * time_to_complete
    # => time_to_complete = pass_distance / (pass_velocity - receiver_speed)
    return math.ceil(pass_distance / (pass_velocity - receiver_speed))


def test_standstill_pass():
    pass_distance = 1
    pass_velocity = 1
    test = setup_passing_test(pass_distance, pass_velocity)
    time_to_complete = pass_distance
    check_pass_completes_after(test, time_to_complete)


def test_handoff():
    pass_distance = 0
    pass_velocity = 0.01
    test = setup_passing_test(pass_distance, pass_velocity)
    assert test.ball.mode == BallMode.RECEIVEDPASS


def test_step_passing_server_after_completion():
    pass_distance = 1
    pass_velocity = 1
    test = setup_passing_test(pass_distance, pass_velocity)
    time_to_complete = pass_distance
    check_pass_completes_after(test, time_to_complete)
    extra_steps = 3
    for _ in range(extra_steps):
        test.space.step(1)


def test_pass_from_moving_passer():
    pass_distance = 3
    pass_velocity = 1
    test = setup_passing_test(pass_distance, pass_velocity)
    time_to_complete = pass_distance
    test.passer.accelerate(1)
    check_pass_completes_after(test, time_to_complete)


def test_pass_to_moving_receiver():
    pass_distance = 3
    pass_velocity = 2
    test = setup_passing_test(pass_distance, pass_velocity)
    test.receiver.accelerate(1)
    receiver_speed = test.receiver._attributes.physical.max_acceleration
    time_to_complete = calculate_time_to_complete(
        pass_distance, pass_velocity, receiver_speed
    )
    check_pass_completes_after(test, time_to_complete)


def test_ball_position_mid_pass_with_both_players_moving():
    pass_distance = 4
    pass_velocity = 2
    test = setup_passing_test(pass_distance, pass_velocity)
    test.passer.turn(1).accelerate(1)
    test.receiver.accelerate(1)
    receiver_speed = test.receiver._attributes.physical.max_acceleration
    time_to_complete = calculate_time_to_complete(
        pass_distance, pass_velocity, receiver_speed
    )
    for time_since_pass in range(time_to_complete):
        assert close_to(test.ball.position, (time_since_pass * pass_velocity, 0))
        test.space.step(1)
