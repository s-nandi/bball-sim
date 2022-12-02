import math
from dataclasses import dataclass
import pygame
from bball_server import DrawInterface, Color, Point, Corners
from bball_server.draw import scale_up


@dataclass
class DrawObject(DrawInterface):
    surface: pygame.surface.Surface
    scale: float

    def _draw_circle(
        self, center: Point, radius: float, color: Color, thickness_or_fill: float
    ):
        center = scale_up(center, self.scale)
        pygame.draw.circle(
            self.surface,
            color,
            center,
            radius * self.scale,
            math.ceil(thickness_or_fill),
        )

    def draw_circle(self, center: Point, radius: float, color: Color, thickness: float):
        assert thickness > 0
        return self._draw_circle(center, radius, color, thickness)

    def draw_filled_circle(self, center: Point, radius: float, color: Color):
        self._draw_circle(center, radius, color, 0)

    def draw_line(self, point_1: Point, point_2: Point, color: Color, thickness: float):
        assert thickness > 0
        point_1 = scale_up(point_1, self.scale)
        point_2 = scale_up(point_2, self.scale)
        pygame.draw.line(self.surface, color, point_1, point_2, math.ceil(thickness))

    def _draw_rectangle(self, corners: Corners, color: Color, thickness_or_fill: float):
        x_lo = corners[0][0] * self.scale
        x_hi = corners[1][0] * self.scale
        y_lo = corners[0][1] * self.scale
        y_hi = corners[1][1] * self.scale
        assert x_lo <= x_hi
        assert y_lo <= y_hi
        pygame.draw.rect(
            self.surface,
            color,
            ((x_lo, y_lo), (x_hi - x_lo, y_hi - y_lo)),
            math.ceil(thickness_or_fill),
        )

    def draw_rectangle(self, corners: Corners, color: Color, thickness: float):
        assert thickness > 0
        self._draw_rectangle(corners, color, thickness)

    def draw_filled_rectangle(self, corners: Corners, color: Color):
        return self._draw_rectangle(corners, color, 0)

    def write_text(self, position: Point, color: Color, text: str, font_size: int):
        font = pygame.font.SysFont("freesansbold.ttf", font_size)
        img = font.render(text, True, color)
        self.surface.blit(img, position)
