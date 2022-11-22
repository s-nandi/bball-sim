from typing import List, Tuple
import pymunk
from game.court import Court
from game.player import Player
from game.types import Team, convert_to_vec2d
from game.player.movement import move_towards, move_in_direction, MovementStyle

TEAMS: Tuple[Team, Team] = (0, 1)


def split_by_team(players: List[Player]) -> Tuple[List[Player], List[Player]]:
    res: Tuple[List[Player], List[Player]] = ([], [])
    for team in TEAMS:
        for player in players:
            if player.team == team:
                res[team].append(player)
    return res


def target_rim_position(team: Team, court: Court) -> pymunk.Vec2d:
    res = (
        court.dimensions.right_rim_position
        if team == 0
        else court.dimensions.left_rim_position
    )
    return convert_to_vec2d(res)


def direct_collision(players: List[Player], _court: Court) -> None:
    for player in players:
        if player.team == 0:
            move_in_direction(player, pymunk.Vec2d(1, 0), float("inf"))
        else:
            move_in_direction(player, pymunk.Vec2d(-1, 0), float("inf"))


def get_close_to_basket(
    distance_threshold, players: List[Player], court: Court
) -> None:
    players_by_team = split_by_team(players)
    for team, team_players in zip(TEAMS, players_by_team):
        other_basket = target_rim_position(team, court)
        for player in team_players:
            style = MovementStyle.HIGHVARIANCE
            move_towards(player, other_basket, distance_threshold, style)
