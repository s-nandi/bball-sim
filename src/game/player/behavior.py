from typing import List, Tuple
import pymunk
from game.court import Court
from game.player import Player
from game.types import Team, convert_to_vec2d
from game.player.movement import move_towards, move_in_direction, MovementStyle

TEAMS: Tuple[Team, Team] = (0, 1)


def other_team(team: Team) -> Team:
    return 1 if team == 0 else 1


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


def own_rim_position(team: Team, court: Court) -> pymunk.Vec2d:
    res = (
        court.dimensions.right_rim_position
        if team == 1
        else court.dimensions.left_rim_position
    )
    return convert_to_vec2d(res)


def determine_team_with_ball(players: List[Player]) -> Team:
    for player in players:
        if player.has_ball:
            return player.team
    assert False


# Movement Utils


def run_to_basket(
    player: Player,
    court: Court,
    distance_threshold: float,
    movement_style: MovementStyle,
):
    other_basket = target_rim_position(player.team, court)
    move_towards(player, other_basket, distance_threshold, movement_style)


def block_player(
    defender: Player, attacker: Player, defending_spot: pymunk.Vec2d, tightness: float
) -> None:
    assert 0 <= tightness <= 1
    attacker_position: pymunk.Vec2d = attacker.body.position
    midpoint = tightness * attacker_position + (1 - tightness) * defending_spot
    move_towards(defender, midpoint, 1, MovementStyle.STEADY)


# Strategies


def direct_collision(players: List[Player], _court: Court) -> None:
    for player in players:
        if player.team == 0:
            move_in_direction(player, pymunk.Vec2d(1, 0), float("inf"))
        else:
            move_in_direction(player, pymunk.Vec2d(-1, 0), float("inf"))


def everyone_runs_to_basket(
    players: List[Player], court: Court, distance_threshold: float
) -> None:
    for player in players:
        run_to_basket(player, court, distance_threshold, MovementStyle.HIGHVARIANCE)


def get_close_to_basket_or_block(
    players: List[Player],
    court: Court,
    distance_threshold: float,
    defensive_tightness: float,
) -> None:
    players_by_team = split_by_team(players)
    team_with_ball = determine_team_with_ball(players)
    team_without_ball = other_team(team_with_ball)
    offensive_team = players_by_team[team_with_ball]
    defensive_team = players_by_team[team_without_ball]
    everyone_runs_to_basket(offensive_team, court, distance_threshold)

    defender_basket = own_rim_position(team_without_ball, court)
    for defender, attacker in zip(defensive_team, offensive_team):
        block_player(defender, attacker, defender_basket, defensive_tightness)
