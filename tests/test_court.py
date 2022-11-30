from typing import Tuple
from bball_server import Court, Hoop, Player, Space
from .utils import (
    create_initialized_player,
    create_court,
    create_three_point_line,
    require_exception,
    create_hoop,
    create_space,
)


def is_position_inbounds(court: Court, position: Tuple[float, float]) -> bool:
    player = create_initialized_player(position=position)
    return court.is_inbounds(player)


def is_position_beyond_line(hoop: Hoop, position: Tuple[float, float]) -> bool:
    player = create_initialized_player(position=position)
    return hoop.is_beyond_three_point_line(player.position)


def check_is_off_court_after(
    court: Court, player: Player, space: Space, expected_time: int
):
    for _ in range(expected_time):
        assert court.is_inbounds(player)
        space.step(1)
    assert not court.is_inbounds(player)


def test_court_bounds():
    width = 40
    height = 20
    court = create_court(width, height)
    assert is_position_inbounds(court, (width, height))
    assert is_position_inbounds(court, (0, height))
    assert is_position_inbounds(court, (width, 0))
    assert is_position_inbounds(court, (0, 0))
    assert not is_position_inbounds(court, (width + 0.01, 0))
    assert not is_position_inbounds(court, (0, height + 0.01))
    assert not is_position_inbounds(court, (-0.01, 0))
    assert not is_position_inbounds(court, (0, -0.01))


def test_move_off_court_horizontal():
    width = 5
    height = 1

    def test_with_starting_position(position, expected_time):
        court = create_court(width, height)
        player = create_initialized_player(position=position)
        space = create_space().add(player)
        player.accelerate(1)
        check_is_off_court_after(court, player, space, expected_time)

    test_with_starting_position((0.5, 0.5), width)
    test_with_starting_position((0, 0.5), width + 1)


def test_move_off_court_vertical():
    width = 5
    height = 1

    def test_with_starting_position(position, expected_time):
        court = create_court(width, height)
        player = create_initialized_player(position=position)
        space = create_space().add(player)
        player.turn(1).accelerate(1)
        check_is_off_court_after(court, player, space, expected_time)

    test_with_starting_position((0.5, 0.5), height)
    test_with_starting_position((0.5, 0), height + 1)


def test_invalid_hoop_position():
    width = 10
    height = 1

    line = create_three_point_line(width, height)

    def invalid_court_1():
        return Court((width, height), (Hoop(10, 1, line), Hoop(10, -0.001, line)))

    def invalid_court_2():
        return Court((width, height), (Hoop(1, 1.01, line), Hoop(10, 1, line)))

    def valid_court():
        return Court((width, height), (Hoop(1, 1, line), Hoop(10, 1, line)))

    require_exception(invalid_court_1, AssertionError)
    require_exception(invalid_court_2, AssertionError)
    valid_court()


def test_left_three_point_line():
    width = 8
    height = 5
    distance_from_left = 2
    distance_from_bottom = 1

    ##########################
    #  5 | . . . . . . . . . #
    #  4 | 3 3 3 . . . 3 3 3 #
    #  3 | 3 3 3 . . . 3 3 3 #
    # .5 |   H           H   #
    #  2 | 3 3 3 . . . 3 3 3 #
    #  1 | 3 3 3 . . . 3 3 3 #
    #  0 | . . . . . . . . . #
    #    / - - - - - - - - - #
    #      0 1 2 3 4 5 6 7 8 #
    ##########################

    left_hoop = create_hoop(
        width,
        height,
        three_point_line=create_three_point_line(
            width, height, distance_from_left / width, distance_from_bottom / height
        ),
    )
    beyond_line_positions = [
        (0, 4.01),
        (0, 0.99),
        (2, 4.01),
        (2, 0.99),
        (2.01, 1),
        (2.01, 2.5),
        (2.01, 3.5),
        (2.01, 4),
    ]
    within_line_positions = [
        (0, 1),
        (0, 4),
        (1, 1),
        (1, 2.5),
        (1, 4),
        (1.2, 1.01),
        (1.2, 3.99),
        (2, 1),
        (2, 4),
    ]
    for position in beyond_line_positions:
        assert is_position_beyond_line(left_hoop, position)
    for position in within_line_positions:
        assert not is_position_beyond_line(left_hoop, position)

    def reflect(position: Tuple[float, float]) -> Tuple[float, float]:
        return (width - position[0], position[1])

    right_hoop = left_hoop.other_hoop(width)
    for position in beyond_line_positions:
        assert is_position_beyond_line(right_hoop, reflect(position))
    for position in within_line_positions:
        assert not is_position_beyond_line(right_hoop, reflect(position))
