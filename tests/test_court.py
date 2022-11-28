from typing import Tuple
from bball_server import Court
from .utils import create_uninitialized_player


def is_position_inbounds(court: Court, position: Tuple[float, float]) -> bool:
    player = create_uninitialized_player()
    player.place_at(position, 0)
    return court.is_inbounds(player)


def test_court_bounds():
    width = 20
    length = 40
    court = Court(dimensions=(width, length))
    assert is_position_inbounds(court, (width, length))
    assert is_position_inbounds(court, (1, length))
    assert is_position_inbounds(court, (width, 1))
    assert is_position_inbounds(court, (1, 1))
    assert not is_position_inbounds(court, (width + 1, 1))
    assert not is_position_inbounds(court, (1, length + 1))
