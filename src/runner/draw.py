import math
from typing import Tuple
import pygame
from bball_server import Game, DrawInterface, Color, Point, Corners


def scale_up(point: Point, scale: float):
    return (point[0] * scale, point[1] * scale)


def scale_while_maintaining_resolution(
    max_w: float, max_h: float, target_w_to_h: float
) -> Tuple[float, float]:
    max_scale = min(max_w / target_w_to_h, max_h / 1)
    return (max_scale * target_w_to_h, max_scale)


def max_resolution_for(game: Game, display_scale=0.5):
    width, height = game.court.dimensions
    pygame.init()
    display_info = pygame.display.Info()
    return scale_while_maintaining_resolution(
        display_info.current_w * display_scale,
        display_info.current_h * display_scale,
        width / height,
    )


class Drawer(DrawInterface):
    surface: pygame.surface.Surface
    scale: float

    def __init__(self, surface: pygame.surface.Surface, scale: float):
        self.surface = surface
        self.scale = scale

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
