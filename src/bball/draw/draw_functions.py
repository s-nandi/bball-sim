from typing import Tuple
from bball.player import Player
from bball.game import Game, Scoreboard
from bball.ball import Ball
from bball.team import Teams
from bball.court import Court, Hoop, ThreePointLine, RectangleThreePointLine
from bball.utils import angle_degrees_to_vector, sum_of, multiply_by
from bball.draw.draw_interface import DrawInterface, Color

BALL_RADIUS = 0.5
DEFAULT_PLAYER_RADIUS = 0.9
PLAYER_ORIENTATION_THICKNESS = 5

BLACK = (0, 0, 0)
PLAYER_MOVEMENT_COLOR = (200, 0, 0)
TEAM_COLORS = [(153, 186, 221), (24, 70, 59)]
BASKETBALL_COLOR = (238, 103, 48)
COURT_LINE_COLOR = (0, 103, 130)
COURT_LINE_THICKNESS = 7
HOOP_COLOR = BLACK
TEXT_COLOR = BLACK


def draw_player(draw_object: DrawInterface, player: Player, color: Color):
    radius = player.physical_attributes.size
    if radius == 0:
        radius = DEFAULT_PLAYER_RADIUS
    draw_object.draw_filled_circle(player.position, radius, color)
    delta = angle_degrees_to_vector(player.orientation_degrees, radius)
    draw_object.draw_line(
        player.position,
        sum_of(player.position, delta),
        BLACK,
        PLAYER_ORIENTATION_THICKNESS,
    )
    acceleration_arrow = multiply_by(
        player.acceleration, radius / player.physical_attributes.max_acceleration
    )
    draw_object.draw_line(
        player.position,
        sum_of(player.position, acceleration_arrow),
        PLAYER_MOVEMENT_COLOR,
        PLAYER_ORIENTATION_THICKNESS,
    )


def draw_teams(draw_object: DrawInterface, teams: Teams):
    for index, team in enumerate(teams):
        color = TEAM_COLORS[index]
        for player in team:
            draw_player(draw_object, player, color)


def draw_rectangular_three_point_line(
    draw_object: DrawInterface, line: RectangleThreePointLine
):
    corners = (line.x_lo, line.y_lo), (line.x_hi, line.y_hi)
    draw_object.draw_rectangle(corners, COURT_LINE_COLOR, COURT_LINE_THICKNESS)


def draw_three_point_line(draw_object: DrawInterface, line: ThreePointLine):
    if isinstance(line, RectangleThreePointLine):
        draw_rectangular_three_point_line(draw_object, line)
        return
    assert False


def draw_hoop(draw_object: DrawInterface, hoop: Hoop):
    draw_object.draw_circle(
        hoop.position, 2 * BALL_RADIUS, HOOP_COLOR, COURT_LINE_THICKNESS
    )


def draw_court_boundary(draw_object: DrawInterface, dimension: Tuple[float, float]):
    width, height = dimension
    corners = (0, 0), (width, height)
    draw_object.draw_rectangle(corners, COURT_LINE_COLOR, COURT_LINE_THICKNESS)


def draw_half_court_line(draw_object: DrawInterface, dimension: Tuple[float, float]):
    width, height = dimension
    draw_object.draw_line(
        (width / 2, 0), (width / 2, height), COURT_LINE_COLOR, COURT_LINE_THICKNESS
    )


def draw_court(draw_object: DrawInterface, court: Court):
    draw_half_court_line(draw_object, court._dimensions)
    draw_court_boundary(draw_object, court._dimensions)
    for hoop in court._hoops:
        draw_hoop(draw_object, hoop)
        draw_three_point_line(draw_object, hoop.three_point_line)


def draw_ball(draw_object: DrawInterface, ball: Ball):
    draw_object.draw_filled_circle(ball.position, BALL_RADIUS, BASKETBALL_COLOR)


def format_float(val: float):
    return str(round(val, 2))


def draw_score(
    draw_object: DrawInterface,
    scoreboard: Scoreboard,
    dimensions: Tuple[float, float],
):
    score = scoreboard.score
    possessions = scoreboard.possessions

    font_size = 80
    padding_for_font_size = 0.001 * font_size
    offset_1 = (dimensions[0] / 2, dimensions[1] * (1 + padding_for_font_size))
    score_0 = format_float(score[0])
    score_1 = format_float(score[1])
    score_string = f"{score_0}  -  {score_1}"
    draw_object.write_text(offset_1, TEXT_COLOR, score_string, font_size)
    possessions_string = f"({possessions[0]} - {possessions[1]})"
    offset_2 = (dimensions[0] / 2, dimensions[1] * (1 + 3 * padding_for_font_size))
    draw_object.write_text(offset_2, TEXT_COLOR, possessions_string, font_size)


def draw_shot_clock(
    draw_object: DrawInterface,
    shot_clock: float,
    dimensions: Tuple[float, float],
):
    if shot_clock == float("inf"):
        return
    font_size = 30
    padding_for_font_size = 0.001 * font_size
    offset = (dimensions[0] / 2, -dimensions[1] * padding_for_font_size)
    shot_clock_string = f"{int(shot_clock)}s"
    draw_object.write_text(offset, TEXT_COLOR, shot_clock_string, font_size)


def draw_game(draw_object: DrawInterface, game: Game):
    draw_teams(draw_object, game.teams)
    draw_court(draw_object, game.court)
    draw_ball(draw_object, game.ball)
    draw_score(
        draw_object,
        game.scoreboard,
        game.court.dimensions,
    )
    draw_shot_clock(draw_object, game.shot_clock, game.court.dimensions)
