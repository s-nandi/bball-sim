from dataclasses import dataclass
import math
from typing import Tuple
import pygame
from bball import Game, DrawInterface, Color, Point, Corners


def scale_up(point: Point, scale: float):
    return (point[0] * scale, point[1] * scale)


def scale_while_maintaining_resolution(
    max_w: float, max_h: float, target_w_to_h: float
) -> Tuple[float, float]:
    max_scale = min(max_w / target_w_to_h, max_h / 1)
    return (max_scale * target_w_to_h, max_scale)


def resolution_for(game: Game, display_scale=0.5) -> Tuple[float, float]:
    width, height = game.court.dimensions
    pygame.init()
    display_info = pygame.display.Info()
    return scale_while_maintaining_resolution(
        display_info.current_w * display_scale,
        display_info.current_h * display_scale,
        width / height,
    )


def padded_resolution_for(
    game: Game, display_scale=0.5, padding_scale=0.5
) -> Tuple[float, float]:
    resolution = resolution_for(game, display_scale)
    display_info = pygame.display.Info()
    width_slack = display_info.current_w - resolution[0]
    height_slack = display_info.current_h - resolution[1]
    border = min(width_slack, height_slack) * padding_scale
    return (resolution[0] + border, resolution[1] + border)


@dataclass
class Transform:
    _scale_factor: float
    _offset: Tuple[float, float]

    def apply(self, point: Point) -> Point:
        return (
            point[0] * self._scale_factor + self._offset[0],
            point[1] * self._scale_factor + self._offset[1],
        )

    def scale(self, coeff: float) -> float:
        return self._scale_factor * coeff


class Drawer(DrawInterface):
    surface: pygame.surface.Surface
    transform: Transform

    def __init__(
        self,
        resolution: Tuple[float, float],
        scale: float = 1,
        offset: Tuple[float, float] = (0, 0),
    ):
        self.surface = pygame.surface.Surface(resolution)
        self.transform = Transform(scale, offset)

    def _draw_circle(
        self, center: Point, radius: float, color: Color, thickness_or_fill: float
    ):
        center = self.transform.apply(center)
        radius = self.transform.scale(radius)
        pygame.draw.circle(
            self.surface, color, center, radius, math.ceil(thickness_or_fill)
        )

    def draw_circle(self, center: Point, radius: float, color: Color, thickness: float):
        assert thickness > 0
        return self._draw_circle(center, radius, color, thickness)

    def draw_filled_circle(self, center: Point, radius: float, color: Color):
        self._draw_circle(center, radius, color, 0)

    def draw_line(self, point_1: Point, point_2: Point, color: Color, thickness: float):
        assert thickness > 0
        point_1 = self.transform.apply(point_1)
        point_2 = self.transform.apply(point_2)
        pygame.draw.line(self.surface, color, point_1, point_2, math.ceil(thickness))

    def _draw_rectangle(self, corners: Corners, color: Color, thickness_or_fill: float):
        lower_corner = self.transform.apply(corners[0])
        upper_corner = self.transform.apply(corners[1])
        width = upper_corner[0] - lower_corner[0]
        height = upper_corner[1] - lower_corner[1]
        assert width > 0
        assert height > 0
        pygame.draw.rect(
            self.surface,
            color,
            ((lower_corner[0], lower_corner[1]), (width, height)),
            math.ceil(thickness_or_fill),
        )

    def draw_rectangle(self, corners: Corners, color: Color, thickness: float):
        assert thickness > 0
        self._draw_rectangle(corners, color, thickness)

    def draw_filled_rectangle(self, corners: Corners, color: Color):
        return self._draw_rectangle(corners, color, 0)

    def write_text(self, position: Point, color: Color, text: str, font_size: int):
        position = self.transform.apply(position)
        font = pygame.font.SysFont("freesansbold.ttf", font_size)
        img = font.render(text, True, color)
        img_rect = img.get_rect(center=position)
        self.surface.blit(img, img_rect)
