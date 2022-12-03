from typing import Tuple
from bball.player import Player
from bball.game import Game, Score
from bball.ball import Ball
from bball.team import Teams
from bball.court import Court, Hoop, ThreePointLine, RectangleThreePointLine
from bball.utils import angle_degrees_to_vector, sum_of
from bball.draw.draw_interface import DrawInterface, Color

BALL_RADIUS = 0.2
PLAYER_RADIUS = 0.9
PLAYER_ORIENTATION_THICKNESS = 5

BLACK = (0, 0, 0)
TEAM_COLORS = [(153, 186, 221), (24, 70, 59)]
BASKETBALL_COLOR = (238, 103, 48)
COURT_LINE_COLOR = (0, 103, 130)
COURT_LINE_THICKNESS = 7
HOOP_COLOR = BLACK
TEXT_COLOR = BLACK


def draw_player(draw_object: DrawInterface, player: Player, color: Color):
    draw_object.draw_filled_circle(player.position, PLAYER_RADIUS, color)
    delta = angle_degrees_to_vector(player.orientation_degrees, PLAYER_RADIUS)
    draw_object.draw_line(
        player.position,
        sum_of(player.position, delta),
        BLACK,
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


def draw_score(draw_object: DrawInterface, score: Score):
    draw_object.write_text((40, 25), TEXT_COLOR, f"{score[0]} - {score[1]}", 30)


def draw_game(draw_object: DrawInterface, game: Game):
    draw_teams(draw_object, game.teams)
    draw_court(draw_object, game.court)
    draw_ball(draw_object, game.ball)
    draw_score(draw_object, game.score)