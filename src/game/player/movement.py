from enum import Enum, auto
import pymunk
from game.player import Player
from game.types import convert_to_vec2d, ConvertibleToVec2d

EPS = 10**-6


def face_towards(player: Player, point: ConvertibleToVec2d):
    point = convert_to_vec2d(point)
    direction = point - player.body.position
    player.body.angle = direction.angle


def move_in_direction(
    player: Player, p_diff: ConvertibleToVec2d, attempted_acceleration: float
) -> None:
    p_diff = convert_to_vec2d(p_diff)
    if p_diff.length < EPS:
        return

    if attempted_acceleration < 0:
        attempted_acceleration = -attempted_acceleration
        p_diff = -p_diff

    acceleration = min(player.attributes.max_acceleration, attempted_acceleration)
    a_new = (
        p_diff.scale_to_length(acceleration)
        if p_diff.length > EPS
        else pymunk.Vec2d(0, 0)
    )
    applied_force = a_new * player.body.mass
    player.body.force = applied_force
    # player.body.apply_impulse_at_world_point(applied_force, player.body.position)
    player.previous_accel = a_new


def stop_movement(player: Player):
    v_curr: pymunk.Vec2d = player.body.velocity
    opposite_acceleration = min(player.attributes.max_acceleration, v_curr.length)
    move_in_direction(player, -player.body.velocity, opposite_acceleration)


def distance_under_constant_acceleration(
    v_init: float, a_init: float, time_frame: float
) -> float:
    return v_init * time_frame + a_init * time_frame * (time_frame - 1) / 2


def constant_acceleration_for_reaching(
    dist: float, v_curr: float, a_max: float, time_frame: float
) -> float:
    def dist_exact_calc(a_next):
        return distance_under_constant_acceleration(v_curr, a_next, time_frame)

    max_iters = 50
    a_lo = -a_max
    a_hi = a_max
    for _ in range(max_iters):
        a_next = (a_lo + a_hi) / 2
        dist_exact = dist_exact_calc(a_next)
        if dist > dist_exact:
            a_lo = a_next
        else:
            a_hi = a_next
    return a_hi


def highest_acceleration_without_overshoot(
    dist: float, v_curr: float, a_max: float, time_frame: float
) -> float:
    def dist_at_least_calc(a_next):
        v_next = v_curr + a_next
        return v_curr + distance_under_constant_acceleration(
            v_next, -a_max, time_frame - 1
        )

    max_iters = 50
    a_lo = -a_max
    a_hi = a_max
    for _ in range(max_iters):
        a_next = (a_lo + a_hi) / 2
        dist_at_least = dist_at_least_calc(a_next)
        if dist < dist_at_least:
            a_hi = a_next
        else:
            a_lo = a_next
    return a_lo


def time_steps_needed(p_delta: float, v_curr: float, a_max: float) -> float:
    assert a_max > 0
    max_steps = 1000
    feasible_covered = 0.0
    for steps in range(1, max_steps + 1):
        v_curr += a_max
        feasible_covered += v_curr
        if feasible_covered >= p_delta:
            return steps
    assert False


class MovementStyle(Enum):
    STEADY = auto()
    HIGHVARIANCE = auto()


def determine_acceleration(
    dist: float, v_curr: float, a_max: float, style: MovementStyle
):
    time_feas = time_steps_needed(dist, v_curr, a_max)
    if style == MovementStyle.HIGHVARIANCE:
        acc = highest_acceleration_without_overshoot(dist, v_curr, a_max, time_feas)
    elif style == MovementStyle.STEADY:
        acc = constant_acceleration_for_reaching(dist, v_curr, a_max, time_feas)
    else:
        assert False
    return acc


def move_towards(
    player: Player,
    p_goal: ConvertibleToVec2d,
    acceptable_distance: float,
    style: MovementStyle,
) -> None:
    p_goal = convert_to_vec2d(p_goal)

    p_diff: pymunk.Vec2d = p_goal - player.body.position
    dist_needed: float = p_diff.length - acceptable_distance
    if dist_needed < EPS:
        stop_movement(player)
    else:
        a_max: float = player.attributes.max_acceleration
        v_curr: float = player.body.velocity.length
        a_next = determine_acceleration(dist_needed, v_curr, a_max, style)
        move_in_direction(player, p_diff, a_next)
    face_towards(player, p_goal)
