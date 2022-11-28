def valid_max_acceleration(acceleration: float) -> bool:
    return acceleration >= 0


def valid_max_turn_degrees(turn_degrees: float) -> bool:
    return 0 <= turn_degrees <= 180


def valid_multiplier(strength: float) -> bool:
    return -1 <= strength <= 1


def valid_angle_degrees(angle_degrees: float) -> bool:
    return -180 <= angle_degrees <= 180


def valid_pass_velocity(pass_velocity: float) -> bool:
    return pass_velocity > 0


def valid_shot_velocity(shot_velocity: float) -> bool:
    return shot_velocity > 0
