from typing import Tuple
from bball_server import Court, Hoop
from .utils import create_initialized_player, create_court, require_exception


def is_position_inbounds(court: Court, position: Tuple[float, float]) -> bool:
    player = create_initialized_player(position=position)
    return court.is_inbounds(player)


def test_court_bounds():
    width = 40
    height = 20
    court = create_court(width, height)
    assert is_position_inbounds(court, (width, height))
    assert is_position_inbounds(court, (1, height))
    assert is_position_inbounds(court, (width, 1))
    assert is_position_inbounds(court, (1, 1))
    assert not is_position_inbounds(court, (width + 1, 1))
    assert not is_position_inbounds(court, (1, height + 1))


def test_invalid_hoop_position():
    width = 10
    height = 1

    def invalid_court_1():
        return Court(dimensions=(width, height), hoops=(Hoop(10, 1), Hoop(10, 0)))

    def invalid_court_2():
        return Court(dimensions=(width, height), hoops=(Hoop(1, 2), Hoop(10, 1)))

    def valid_court():
        return Court(dimensions=(width, height), hoops=(Hoop(1, 1), Hoop(10, 1)))

    require_exception(invalid_court_1, AssertionError)
    require_exception(invalid_court_2, AssertionError)
    valid_court()
