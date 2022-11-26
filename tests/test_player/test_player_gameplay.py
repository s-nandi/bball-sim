from tests.utils import (
    create_space,
    DEFAULT_PLAYER_ATTRIBUTES,
    create_initialized_player,
)
from bball_server import PassingServer


def test_pass():
    passing_server = PassingServer()
    pass_distance = 3
    player_1 = create_initialized_player(DEFAULT_PLAYER_ATTRIBUTES, (0, 0), 0)
    player_2 = create_initialized_player(
        DEFAULT_PLAYER_ATTRIBUTES, (pass_distance, 0), 180
    )
    space = create_space().add(passing_server).add(player_1).add(player_2)

    player_1.give_ball()
    assert player_1.has_ball
    assert not player_2.has_ball

    expected_pass_completion_time = pass_distance
    passing_server.pass_between(player_1, player_2, pass_velocity=1)
    for _ in range(expected_pass_completion_time):
        assert player_1.has_ball
        assert not player_2.has_ball
        space.step(1)
    assert not player_1.has_ball
    assert player_2.has_ball
