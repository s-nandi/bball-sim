from utils import (
    create_initialized_player,
    create_uninitialized_player,
    close_to,
    require_exception,
)


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
    original_position = player.position
    player.turn(1).accelerate(1)
    assert close_to(player.position, original_position)
    player.step()
    assert not close_to(player.position, original_position)


def test_skip_accelerate():
    player = create_initialized_player(max_acceleration=2.0, velocity_decay=0)
    player.turn(1).accelerate(0.5)
    player.step()
    assert close_to(player.position, (0, 1))
    assert close_to(player.velocity, (0, 1))
    player.step()
    assert close_to(player.position, (0, 2))
    assert close_to(player.velocity, (0, 1))


def test_accelerate_twice():
    player = create_initialized_player(max_acceleration=2.0, velocity_decay=0)
    player.turn(1).accelerate(0.5)
    player.step()
    assert close_to(player.position, (0, 1))
    assert close_to(player.velocity, (0, 1))
    player.accelerate(0.5)
    player.step()
    assert close_to(player.position, (0, 3))
    assert close_to(player.velocity, (0, 2))


def test_max_velocity_decay():
    player = create_initialized_player(max_acceleration=1, velocity_decay=1.0)
    player.accelerate(1)
    player.step()
    assert close_to(player.position, (1, 0))
    player.accelerate(1)
    player.step()
    assert close_to(player.position, (2, 0))


def test_velocity_after_turning():
    player = create_initialized_player()
    player.accelerate(1)
    player.step()
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))
    player.turn(1)
    player.step()
    assert close_to(player.velocity, (0, 1))
    assert close_to(player.position, (1, 1))
    player.turn(1)
    player.step()
    assert close_to(player.velocity, (-1, 0))
    assert close_to(player.position, (0, 1))
    player.turn(1)
    player.step()
    assert close_to(player.velocity, (0, -1))
    assert close_to(player.position, (0, 0))
    player.turn(1)
    player.step()
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))
