from bball_server.game import Game, Teams, Court, Ball, Score
from bball_server.draw_interface import DrawInterface


def draw_teams(draw_object: DrawInterface, teams: Teams):
    pass


def draw_court(draw_object: DrawInterface, court: Court):
    pass


def draw_ball(draw_object: DrawInterface, ball: Ball):
    pass


def draw_score(draw_object: DrawInterface, score: Score):
    pass


def draw_game(draw_object: DrawInterface, game: Game):
    draw_teams(draw_object, game.teams)
    draw_court(draw_object, game.court)
    draw_ball(draw_object, game.ball)
    draw_score(draw_object, game.score)
