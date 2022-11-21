from typing import List, Tuple, Iterable
import math
import pymunk
import pymunk.pygame_util
import pygame
from game.dimensions import CourtDimensions
from game.types import Color


def transform_points(
    transform: pymunk.Transform, vertices: Iterable[Tuple[float, float]]
) -> List[Tuple[float, float]]:
    return [transform @ vertex for vertex in vertices]


def draw_polygon(
    screen: pygame.Surface,
    polygon: List[Tuple[float, float]],
    *,
    radius: float,
    outline_color: Color,
    fill_color: Color,
    scale: float,
) -> None:
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    transform = pymunk.Transform.scaling(scale)
    xformed_polygon = transform_points(transform, polygon)
    radius *= scale
    draw_options.draw_polygon(xformed_polygon, radius, outline_color, fill_color)


def draw_segment(
    screen: pygame.Surface,
    endpoints: Tuple[Tuple[float, float], Tuple[float, float]],
    *,
    radius: float,
    outline_color: Color,
    scale: float,
) -> None:
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    transform = pymunk.Transform.scaling(scale)
    xformed_endpoints = transform_points(transform, endpoints)
    xformed_radius = radius * scale
    draw_options.draw_fat_segment(
        xformed_endpoints[0],
        xformed_endpoints[1],
        xformed_radius,
        outline_color,
        outline_color,
    )


def chord_endpoints(
    center, radius, starting_angle, total_angle, subdivisions
) -> List[Tuple[float, float]]:
    endpoints = []
    current_angle = starting_angle
    for _ in range(subdivisions + 1):
        point = center + pymunk.Vec2d(radius, 0).rotated(current_angle)
        endpoints.append(point)
        current_angle += total_angle / subdivisions
    return endpoints


def draw_circle_arc(
    screen: pygame.Surface,
    center: Tuple[float, float],
    *,
    radius: float,
    starting_angle: float,
    total_angle: float,
    thickness: float,
    outline_color: Color,
    subdivisions: int,
    scale: float,
) -> None:

    endpoints = chord_endpoints(
        center, radius, starting_angle, total_angle, subdivisions
    )
    assert len(endpoints) == subdivisions + 1
    for i, endpoint in enumerate(endpoints[1:], start=1):
        endpoint_2 = endpoints[i - 1]
        draw_segment(
            screen,
            (endpoint, endpoint_2),
            radius=thickness,
            outline_color=outline_color,
            scale=scale,
        )


def draw_court_markings(
    dimensions: CourtDimensions, screen: pygame.Surface, scale: float
) -> None:
    three_point_line_dimensions = dimensions.three_point_line

    top_y = dimensions.y_max - three_point_line_dimensions.distance_from_top_edge
    bottom_y = dimensions.y_min + three_point_line_dimensions.distance_from_top_edge
    left_x = dimensions.x_min
    right_x = dimensions.x_min + three_point_line_dimensions.corner_length

    line_color = Color(0, 103, 130, 255)
    line_thickness = three_point_line_dimensions.line_thickness

    opposite = (
        three_point_line_dimensions.corner_length
        - dimensions.rim.distance_from_left_edge
    )
    adjacent = (
        dimensions.height / 2 - three_point_line_dimensions.distance_from_top_edge
    )
    amt_radians_less_than_semicircle = math.atan2(opposite, adjacent)

    def draw_left_three_point_line():
        draw_segment(
            screen,
            ((left_x, top_y), (right_x, top_y)),
            radius=line_thickness,
            outline_color=line_color,
            scale=scale,
        )
        draw_segment(
            screen,
            ((left_x, bottom_y), (right_x, bottom_y)),
            radius=line_thickness,
            outline_color=line_color,
            scale=scale,
        )
        draw_circle_arc(
            screen,
            dimensions.left_rim_position,
            starting_angle=amt_radians_less_than_semicircle - math.pi / 2,
            total_angle=math.pi - 2 * amt_radians_less_than_semicircle,
            thickness=line_thickness,
            radius=three_point_line_dimensions.outer_radius,
            outline_color=line_color,
            subdivisions=30,
            scale=scale,
        )

    def draw_right_three_point_line():
        draw_segment(
            screen,
            ((dimensions.width - left_x, top_y), (dimensions.width - right_x, top_y)),
            radius=line_thickness,
            outline_color=line_color,
            scale=scale,
        )
        draw_segment(
            screen,
            (
                (dimensions.width - left_x, bottom_y),
                (dimensions.width - right_x, bottom_y),
            ),
            radius=line_thickness,
            outline_color=line_color,
            scale=scale,
        )
        draw_circle_arc(
            screen,
            dimensions.right_rim_position,
            starting_angle=amt_radians_less_than_semicircle + math.pi / 2,
            total_angle=math.pi - 2 * amt_radians_less_than_semicircle,
            thickness=line_thickness,
            radius=three_point_line_dimensions.outer_radius,
            outline_color=line_color,
            subdivisions=30,
            scale=scale,
        )

    def draw_half_court_line():
        draw_segment(
            screen,
            (
                (dimensions.x_mid, dimensions.y_max),
                (dimensions.x_mid, dimensions.y_min),
            ),
            radius=line_thickness,
            outline_color=line_color,
            scale=scale,
        )

    draw_left_three_point_line()
    draw_right_three_point_line()
    draw_half_court_line()
