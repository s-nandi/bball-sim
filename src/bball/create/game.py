from typing import Union, List
from bball.ball import Ball
from bball.court import Court
from bball.team import Team, Teams
from bball.game import Game, GameSettings
from bball.create.aliases import create_ball, create_game_settings
from bball.create.court import create_court


def _normalized_teams(teams: List[Team]) -> Teams:
    assert len(teams) <= 2
    while len(teams) <= 2:
        teams.append(Team())
    return Teams(teams[0], teams[1])


def create_game(
    teams: List[Team],
    ball: Union[Ball, None] = None,
    court: Union[Court, None] = None,
    settings: Union[GameSettings, None] = None,
):
    if ball is None:
        ball = create_ball()
    if court is None:
        court = create_court()
    if settings is None:
        settings = create_game_settings()
    return Game(_normalized_teams(teams), ball, court, settings)
