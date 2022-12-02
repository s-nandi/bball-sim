from abc import ABC, abstractmethod
from typing import Tuple
from bball_server.utils import Point

Color = Tuple[int, int, int]
Corners = Tuple[Point, Point]


class DrawInterface(ABC):
    @abstractmethod
    def draw_circle(self, center: Point, radius: float, color: Color, fill: bool):
        pass

    @abstractmethod
    def draw_line(self, point_1: Point, point_2: Point, color: Color):
        pass

    @abstractmethod
    def draw_rectangle(self, corners: Corners, color: Color, fill: bool):
        pass

    @abstractmethod
    def write_text(self, position: Point, color: Color, text: str, font_size: int):
        pass
