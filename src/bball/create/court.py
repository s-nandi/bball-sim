from typing import Optional
from bball.court import Court, Hoop, ThreePointLine, RectangleThreePointLine

DEFAULT_WIDTH_RATIO = 1 / 4
DEFAULT_HEIGHT_RATIO = 1 / 5


def create_three_point_line(
    width: float,
    height: float,
    width_ratio: float = DEFAULT_WIDTH_RATIO,
    height_ratio: float = DEFAULT_HEIGHT_RATIO,
) -> RectangleThreePointLine:
    """
    Returns a rectangular three point line for the left side of the court
    that spans from 0 to width * width_ratio along the x-axis, and from
    height_ratio * height to (1 - height_ratio) * height along the y-axis
    """
    assert width_ratio < 0.5, "Entire width of court is in 3-point range"
    assert height_ratio < 0.5, "Entire height of court is in 3-point range"
    distance_from_left = width * width_ratio
    distance_from_bottom = height * height_ratio
    line = RectangleThreePointLine(
        0, distance_from_left, distance_from_bottom, height - distance_from_bottom
    )
    return line


def create_hoop(
    width: float,
    height: float,
    offset_from_left: float = 0.0,
    three_point_line: Optional[ThreePointLine] = None,
):
    if three_point_line is None:
        three_point_line = create_three_point_line(width, height)
    return Hoop(offset_from_left, height / 2, three_point_line)


def create_court(
    width: float = 12,
    height: float = 5,
    hoop: Optional[Hoop] = None,
) -> Court:
    if hoop is None:
        hoop = create_hoop(width, height)
    return Court(dimensions=(width, height), hoops=(hoop, hoop.other_hoop(width)))
