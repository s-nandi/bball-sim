from utils import (
    create_space,
    create_player_attributes,
    DEFAULT_PLAYER_ATTRIBUTES,
    create_initialized_player,
    create_uninitialized_player,
    close_to,
    require_exception,
)
from bball_server import PassingServer


def test_invalid_moves():
    def test_turn(value):
        player = create_initialized_player()
        player.turn(value)

    def test_acceleration(value):
        player = create_initialized_player()
        player.accelerate(value)

    require_exception(lambda: test_turn(2), AssertionError)
    require_exception(lambda: test_turn(-1.01), AssertionError)
    require_exception(lambda: test_acceleration(1.01), AssertionError)
    require_exception(lambda: test_acceleration(-2), AssertionError)


def test_turn_after_accelerate():
    def turn_after_accelerate():
        player = create_initialized_player()
        player.accelerate(1).turn(1)

    def accelerate_after_turn():
        player = create_initialized_player()
        player.turn(1).accelerate(1)

    require_exception(turn_after_accelerate, AssertionError)
    accelerate_after_turn()


def test_double_initialization():
    def initialize_position_twice():
        player = create_uninitialized_player()
        player.initial_position(0, 3).initial_position(3, 0)

    def initialize_orientation_twice():
        player = create_uninitialized_player()
        player.initial_orientation(0).initial_orientation(90)

    require_exception(initialize_orientation_twice, AssertionError)
    require_exception(initialize_position_twice, AssertionError)


def test_place():
    def orientation_before_position():
        player = create_uninitialized_player()
        player.initial_orientation(0).initial_position(-100.0, 23)
        assert close_to(player.position, (-100.0, 23))

    def position_before_orientation():
        player = create_uninitialized_player()
        player.initial_position(-100.0, 23).initial_orientation(0)
        assert close_to(player.position, (-100.0, 23))

    orientation_before_position()
    position_before_orientation()


def test_if_displaced():
    player = create_initialized_player()
    space = create_space().add_player(player)

    original_position = player.position
    player.turn(1).accelerate(1)
    print("actual", player._physics._body.position)
    assert close_to(player.position, original_position)
    space.step(1)
    print("actual", player._physics._body.position)
    assert not close_to(player._physics._body.position, original_position)


def test_accelerate_simple():
    player = create_initialized_player(create_player_attributes())
    space = create_space().add_player(player)
    player.accelerate(1)
    space.step(1)
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))


def test_skip_accelerate():
    player = create_initialized_player(
        create_player_attributes(max_acceleration=2.0, velocity_decay=0)
    )
    space = create_space().add_player(player)

    player.turn(1).accelerate(0.5)
    space.step(1)

    body = player._physics._body
    print(player, body.force, len(body.space.bodies), body.mass)

    assert close_to(player.position, (0, 1))
    assert close_to(player.velocity, (0, 1))
    space.step(1)
    assert close_to(player.position, (0, 2))
    assert close_to(player.velocity, (0, 1))


def test_accelerate_twice():
    player = create_initialized_player(
        create_player_attributes(max_acceleration=2.0, velocity_decay=0)
    )
    space = create_space().add_player(player)

    player.turn(1).accelerate(0.5)
    space.step(1)
    assert close_to(player.position, (0, 1))
    assert close_to(player.velocity, (0, 1))
    player.accelerate(0.5)
    space.step(1)
    assert close_to(player.position, (0, 3))
    assert close_to(player.velocity, (0, 2))


def test_max_velocity_decay():
    player = create_initialized_player(
        create_player_attributes(max_acceleration=1.0, velocity_decay=1.0)
    )
    space = create_space().add_player(player)

    player.accelerate(1)
    space.step(1)
    assert close_to(player.position, (1, 0))
    player.accelerate(1)
    space.step(1)
    assert close_to(player.position, (2, 0))


def test_velocity_after_turning():
    player = create_initialized_player()
    space = create_space().add_player(player)

    player.accelerate(1)
    space.step(1)
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (0, 1))
    assert close_to(player.position, (1, 1))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (-1, 0))
    assert close_to(player.position, (0, 1))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (0, -1))
    assert close_to(player.position, (0, 0))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))


def test_pass():
    passing_server = PassingServer()
    player_1 = create_initialized_player(DEFAULT_PLAYER_ATTRIBUTES, (0, 0), 0)
    player_2 = create_initialized_player(DEFAULT_PLAYER_ATTRIBUTES, (3, 3), 180)
    player_1.give_ball()
    assert player_1.has_ball
    assert not player_2.has_ball

    pass_completion_time = 3
    passing_server.pass_between(player_1, player_2, complete_in=pass_completion_time)
    for _ in range(pass_completion_time):
        assert player_1.has_ball
        assert not player_2.has_ball
        passing_server.step()
    assert not player_1.has_ball
    assert player_2.has_ball
