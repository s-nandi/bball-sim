def valid_max_acceleration(acceleration: float) -> bool:
    return acceleration >= 0


def valid_max_velocity(velocity: float) -> bool:
    return velocity > 0


def valid_max_turn_degrees(turn_degrees: float) -> bool:
    return 0 <= turn_degrees


def valid_multiplier(strength: float) -> bool:
    return -1 <= strength <= 1


def valid_positive_multiplier(strength: float) -> bool:
    return 0 <= strength <= 1


def valid_angle_degrees(angle_degrees: float) -> bool:
    return -180 <= angle_degrees < 180


def valid_pass_velocity(pass_velocity: float) -> bool:
    return pass_velocity > 0


def valid_shot_velocity(shot_velocity: float) -> bool:
    return shot_velocity > 0


def valid_probability(probability: float) -> bool:
    return 0.0 <= probability <= 1.0


def valid_shot_value(value: float) -> bool:
    return value >= 0.0
