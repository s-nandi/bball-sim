import itertools
import functools
import logging
from typing import List
from game import Game, Player, generate_players, Court, behavior
from game.dimensions import CourtDimensions, RimDimensions, ThreePointLineDimensions
from visualizer import Visualizer, ScreenParams

# Canonical
# mass_generator = itertools.cycle([81.19, 98.3]),  # kg
# size_generator = itertools.repeat(0.94),  # m
# max_speed_generator = itertools.cycle([2.096618, 1.627226]),  # m / s
# max_acceleration_generator = itertools.cycle([2.34, 2.5]),  # m / s ^ 2
# sideline_thickness = 0.05  # m
# width = 28.65  # m
# height = 15.24  # m
# rim_radius = 0.4572  # m
# rim_distance_from_left_edge = 1.6002  # m
# three_point_line_distance_from_top_edge = 1.019  # m
# three_point_line_corner_length = 3.006725  # m
# three_point_line_outer_radius = 6.75  # m
# three_point_line_line_thickness = 0.025  # m


def create_players() -> List[Player]:
    players = generate_players(
        mass_generator=itertools.cycle([81.19, 98.3]),  # kg
        size_generator=itertools.repeat(0.94),  # m
        max_speed_generator=itertools.cycle([2.096618, 1.627226]),  # m / s
        max_acceleration_generator=itertools.cycle([2.34, 2.5]),  # m / s ^ 2
        position_generator=[(3.5, 7.62), (28.65 - 3.5, 7.62)],
        teams_generator=itertools.cycle([0, 1]),
    )
    return list(players)


def create_court() -> Court:
    sideline_thickness = 0.05  # m
    width = 28.65  # m
    height = 15.24  # m
    rim_radius = 0.4572  # m
    rim_distance_from_left_edge = 1.6002  # m
    three_point_line_distance_from_top_edge = 1.019  # m
    three_point_line_corner_length = 3.006725  # m
    three_point_line_outer_radius = 6.75  # m
    three_point_line_line_thickness = 0.025  # m

    padded_width = width + sideline_thickness * 2
    padded_height = height + sideline_thickness * 2
    damping = 0.5
    return Court(
        CourtDimensions(
            width=padded_width,
            height=padded_height,
            boundary_thickness=sideline_thickness,
            rim=RimDimensions(rim_radius, rim_distance_from_left_edge),
            three_point_line=ThreePointLineDimensions(
                three_point_line_distance_from_top_edge,
                three_point_line_corner_length,
                three_point_line_outer_radius,
                three_point_line_line_thickness,
            ),
        ),
        damping=damping,
    )


def setup_simulation() -> Visualizer:
    game = Game(
        create_players(),
        create_court(),
        functools.partial(behavior.get_close_to_basket, 10.0),
    )
    screen_params = ScreenParams(
        width=game.court.dimensions.width,
        height=game.court.dimensions.height,
        fps=90,
    )
    simulation = Visualizer(
        screen_params,
        game,
        simulation_speed_scale=2.0,
    )
    return simulation


def configure_logger() -> None:
    logging.basicConfig(filename="output/run.log", level=logging.DEBUG)


def main() -> None:
    configure_logger()
    simulation = setup_simulation()
    simulation.run()


if __name__ == "__main__":
    main()
