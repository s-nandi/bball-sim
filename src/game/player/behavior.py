from typing import List, Tuple
import pymunk
from game.court import Court
from game.player import Player
from game.types import Team, convert_to_vec2d, ConvertibleToVec2d

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


def move_in_direction(
    player: Player, p_diff: ConvertibleToVec2d, attempted_acceleration: float
) -> None:
    p_diff = convert_to_vec2d(p_diff)
    if attempted_acceleration < 0:
        attempted_acceleration = -attempted_acceleration
        p_diff = -p_diff

    player.body.angle = p_diff.angle
    acceleration = min(player.attributes.max_acceleration, attempted_acceleration)

    a_new = p_diff.scale_to_length(acceleration)
    player.body.force = a_new * player.body.mass


def distance_under_constant_acceleration(
    v_init: float, a_init: float, time_frame: float
) -> float:
    return v_init * time_frame + 1 / 2 * a_init * time_frame**2


def lowest_acceleration_that_reaches(
    p_delta: float, v_curr: float, a_max: float, time_frame: float
) -> float:
    iters = 20
    a_lo = -a_max
    a_hi = a_max
    for _ in range(iters):
        mid = a_lo + (a_hi - a_lo) / 2
        can_travel = distance_under_constant_acceleration(v_curr, mid, time_frame)
        if p_delta < can_travel:
            a_hi = mid
        else:
            a_lo = mid
    return a_lo


def move_towards(
    player: Player, p_goal: ConvertibleToVec2d, acceptable_distance: float
) -> None:
    p_goal = convert_to_vec2d(p_goal)
    time_frame = 20

    a_max: float = player.attributes.max_acceleration
    p_curr: pymunk.Vec2d = player.body.position
    v_curr: pymunk.Vec2d = player.body.velocity
    a_curr: pymunk.Vec2d = player.body.force / player.body.mass

    p_diff = p_goal - p_curr

    a_next = float("inf")
    if p_diff.length < acceptable_distance:
        stop_movement(player)

    dist_rem = p_diff.length - acceptable_distance
    if dist_rem < distance_under_constant_acceleration(
        v_curr.length, -a_max, time_frame
    ):
        a_next = -a_max
        print("start slowing down ", player.team)
        # a_next = lowest_acceleration_that_reaches(
        #     dist_rem, v_curr.length, a_max, time_frame
        # )

    move_in_direction(player, p_diff, a_next)


def stop_movement(player: Player):
    v_curr: pymunk.Vec2d = player.body.velocity
    time_frame = 2

    print("try stopping movement ", v_curr.length, player.team)

    if v_curr.length <= player.attributes.max_acceleration * 0.1:
        player.body.velocity = pymunk.Vec2d(0, 0)
        player.body.force = pymunk.Vec2d(0, 0)
    else:
        opposite_acceleration = player.body.velocity.length / time_frame
        move_in_direction(player, -player.body.velocity, opposite_acceleration)


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
            move_towards(player, other_basket, distance_threshold)
