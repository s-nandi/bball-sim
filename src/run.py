import itertools
import logging
from typing import List
from game import Game, Player, generate_players, Court
from game.dimensions import CourtDimensions, RimDimensions, ThreePointLineDimensions
from visualizer import Visualizer, ScreenParams


def configure_logger() -> None:
    logging.basicConfig(filename="output/run.log", level=logging.DEBUG)


def create_players() -> List[Player]:
    players = generate_players(
        mass_generator=itertools.cycle([81.19, 98.3]),  # kg
        size_generator=itertools.repeat(0.94),  # m
        max_speed_generator=itertools.cycle([2.096618, 1.627226]),  # m / s
        max_acceleration_generator=itertools.cycle([2.34, 2.5]),  # m / s ^ 2
        position_generator=[(2, 5), (3.5, 6.5)],
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
        )
    )


def setup_simulation() -> Visualizer:
    game = Game(create_players(), create_court())
    screen_params = ScreenParams(
        width=game.court.dimensions.width,
        height=game.court.dimensions.height,
        fps=30,
    )
    simulation = Visualizer(
        screen_params,
        game,
        simulation_speed_scale=1.0,
    )
    return simulation


def main() -> None:
    configure_logger()
    simulation = setup_simulation()
    simulation.run()


if __name__ == "__main__":
    main()
