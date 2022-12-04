from typing import Optional
from bball.ball import Ball
from bball.court import Court
from bball.team import Teams
from bball.game import Game, GameSettings
from bball.create.teams import create_teams
from bball.create.ball import create_ball
from bball.create.court import create_court

# Alias for consistency while still enabling type hinting
create_game_settings = GameSettings  # pylint: disable=invalid-name


def create_game(
    teams: Optional[Teams] = None,
    ball: Optional[Ball] = None,
    court: Optional[Court] = None,
    settings: Optional[GameSettings] = None,
):
    if teams is None:
        teams = create_teams()
    if ball is None:
        ball = create_ball()
    if court is None:
        court = create_court()
    if settings is None:
        settings = create_game_settings()
    return Game(teams, ball, court, settings)
