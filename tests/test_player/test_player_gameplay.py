from tests.utils import (
    create_space,
    DEFAULT_PLAYER_ATTRIBUTES,
    create_initialized_player,
)
from bball_server import PassingServer


def test_pass():
    passing_server = PassingServer()
    player_1 = create_initialized_player(DEFAULT_PLAYER_ATTRIBUTES, (0, 0), 0)
    player_2 = create_initialized_player(DEFAULT_PLAYER_ATTRIBUTES, (3, 3), 180)
    space = create_space().add(passing_server).add(player_1).add(player_2)

    player_1.give_ball()
    assert player_1.has_ball
    assert not player_2.has_ball

    pass_completion_time = 3
    passing_server.pass_between(player_1, player_2, complete_in=pass_completion_time)
    for _ in range(pass_completion_time):
        assert player_1.has_ball
        assert not player_2.has_ball
        space.step(1)
    assert not player_1.has_ball
    assert player_2.has_ball
