import pymunk


def zero_gravity(body, _gravity, damping, d_time):
    pymunk.Body.update_velocity(body, (0, 0), damping, d_time)
