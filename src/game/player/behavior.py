from typing import List
import pymunk
from game.game import Game
from game.player.shooting import player_shoots
from game.court import Court
from game.player import Player
from game.team import other_team, split_by_team
from game.player.movement import move_towards, MovementStyle
from game.types import ConvertibleToVec2d, convert_to_vec2d


# Movement Utils


def run_to_basket(
    player: Player,
    court: Court,
    distance_threshold: float,
    movement_style: MovementStyle,
):
    other_basket = court.target_rim_position(player.team)
    move_towards(player, other_basket, distance_threshold, movement_style)


def block_player(
    defender: Player,
    attacker: Player,
    defending_spot: ConvertibleToVec2d,
    tightness: float,
) -> None:
    assert 0 <= tightness <= 1
    defending_spot = convert_to_vec2d(defending_spot)
    attacker_position: pymunk.Vec2d = attacker.body.position
    midpoint = tightness * attacker_position + (1 - tightness) * defending_spot
    move_towards(defender, midpoint, 1, MovementStyle.STEADY)


def shoot_if_close(game: Game, attacker: Player, distance_threshold: float) -> None:
    target = game.court.target_rim_position(attacker.team)
    distance_to_target = attacker.body.position.get_distance(target)
    if distance_to_target <= distance_threshold:
        player_shoots(game, attacker)


# Strategies


def everyone_runs_to_basket(
    _game: Game, players: List[Player], court: Court, distance_threshold: float
) -> None:
    for player in players:
        run_to_basket(player, court, distance_threshold, MovementStyle.HIGHVARIANCE)


def get_close_to_basket_or_block(
    game: Game,
    players: List[Player],
    court: Court,
    shooting_distance_threshold: float,
    defensive_tightness: float,
) -> None:
    team_with_ball = game.team_with_ball
    team_without_ball = other_team(team_with_ball)

    players_by_team = split_by_team(players)
    offensive_team = players_by_team[team_with_ball]
    defensive_team = players_by_team[team_without_ball]

    everyone_runs_to_basket(game, offensive_team, court, shooting_distance_threshold)
    for player in offensive_team:
        if player.has_ball:
            shoot_if_close(game, player, shooting_distance_threshold)

    defender_basket = court.own_rim_position(team_without_ball)
    for defender, attacker in zip(defensive_team, offensive_team):
        block_player(defender, attacker, defender_basket, defensive_tightness)
