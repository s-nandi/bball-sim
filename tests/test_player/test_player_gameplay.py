import math
from dataclasses import dataclass
from bball_server import Player, PassingServer, Space
from ..utils import (
    create_space,
    DEFAULT_PLAYER_ATTRIBUTES,
    create_initialized_player,
)


def check_pass_completes_after(space, passer, receiver, expected_time: int):
    for _ in range(expected_time):
        assert passer.has_ball
        assert not receiver.has_ball
        space.step(1)
    assert not passer.has_ball
    assert receiver.has_ball


@dataclass
class PassingTest:
    space: Space
    passer: Player
    receiver: Player


def setup_passing_test(pass_distance, pass_velocity) -> PassingTest:
    passer = create_initialized_player(DEFAULT_PLAYER_ATTRIBUTES, (0, 0), 0)
    receiver = create_initialized_player(position=(pass_distance, 0))
    space = create_space().add(passer).add(receiver)
    passer.give_ball()
    assert passer.has_ball
    assert not receiver.has_ball
    space.add(PassingServer(passer, receiver, pass_velocity=pass_velocity))
    return PassingTest(space, passer, receiver)


def test_standstill_pass():
    pass_distance = 3
    pass_velocity = 1
    test = setup_passing_test(pass_distance, pass_velocity)
    time_to_complete = pass_distance
    check_pass_completes_after(test.space, test.passer, test.receiver, time_to_complete)


def test_handoff():
    pass_distance = 0
    pass_velocity = 0.01
    test = setup_passing_test(pass_distance, pass_velocity)
    test.space.step(10**-6)
    assert not test.passer.has_ball
    assert test.receiver.has_ball


def test_step_passing_server_after_completion():
    pass_distance = 1
    pass_velocity = 1
    test = setup_passing_test(pass_distance, pass_velocity)
    time_to_complete = pass_distance
    check_pass_completes_after(test.space, test.passer, test.receiver, time_to_complete)
    extra_steps = 3
    for _ in range(extra_steps):
        test.space.step(1)


def test_pass_from_moving_passer():
    pass_distance = 3
    pass_velocity = 1
    test = setup_passing_test(pass_distance, pass_velocity)
    time_to_complete = pass_distance
    test.passer.accelerate(1)
    check_pass_completes_after(test.space, test.passer, test.receiver, time_to_complete)


def test_pass_to_moving_receiver():
    pass_distance = 3
    pass_velocity = 2
    test = setup_passing_test(pass_distance, pass_velocity)
    test.receiver.accelerate(1)
    acceleration = test.receiver._attributes.max_acceleration
    # pass_distance + time_to_complete * acceleration == pass_velocity * time_to_complete
    # => time_to_complete = pass_distance / (pass_velocity - accelerate)
    time_to_complete = math.ceil(pass_distance / (pass_velocity - acceleration))
    check_pass_completes_after(test.space, test.passer, test.receiver, time_to_complete)
