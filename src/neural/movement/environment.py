from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
import numpy as np
import gym
from gym import spaces
from experiment.initiate import canonical_game
from bball import BallMode
from bball.create import create_space
from bball.utils import interpolation_coefficient, vector_length
from stable_baselines3.common.env_checker import check_env

import pygame
from runner.draw import resolution_for, padded_resolution_for, Drawer
from runner.setup import step_space, BACKGROUND_COLOR, time_frame_for
from engine import Engine
from bball.draw import draw_game

if TYPE_CHECKING:
    from bball import Player, Court

game_template = canonical_game
num_players = 1
fps = 60
speed_scale = 3.0
time_frame = time_frame_for(fps, speed_scale)
display_scale = 0.5

action_shape = (2,)
observation_shape = (5,)
observation_dtype = np.float32


def _validate_observation(observation: np.array):
    assert observation.shape == observation_shape
    assert observation.dtype == observation_dtype


@dataclass
class PlayerState:
    position_x: float
    position_y: float
    orientation: float
    velocity_x: float
    velocity_y: float

    @staticmethod
    def from_observation(
        observation: np.array, player: Player, court: Court
    ) -> PlayerState:
        _validate_observation(observation)
        max_velocity = player.physical_attributes.max_velocity

        coeffs = [coeff.item() for coeff in observation]
        coeffs = [(coeff + 1) / 2 for coeff in coeffs]
        position_x, position_y, orientation, velocity_x, velocity_y = coeffs
        position_x *= court.width
        position_y *= court.height
        orientation *= 360
        velocity_x *= max_velocity
        velocity_y *= max_velocity
        return PlayerState(position_x, position_y, orientation, velocity_x, velocity_y)

    def to_observation(self: PlayerState, player: Player, court: Court, checked=False):
        max_velocity = player.physical_attributes.max_velocity

        position_x = interpolation_coefficient(self.position_x, 0, court.width)
        position_y = interpolation_coefficient(self.position_y, 0, court.height)
        orientation = interpolation_coefficient(self.orientation, -180, 180)
        vel_x = interpolation_coefficient(self.velocity_x, -max_velocity, max_velocity)
        vel_y = interpolation_coefficient(self.velocity_y, -max_velocity, max_velocity)
        coeffs = [position_x, position_y, orientation, vel_x, vel_y]
        if checked:
            assert all([0 <= val <= 1 for val in coeffs]), coeffs
        coeffs = [2 * val - 1 for val in coeffs]
        observation = np.array(coeffs, dtype=np.float32)

        _validate_observation(observation)
        return observation

    @staticmethod
    def from_player(player: Player) -> PlayerState:
        return PlayerState(
            player.position[0],
            player.position[1],
            player.orientation_degrees,
            player.velocity[0],
            player.velocity[1],
        )


class Environment(gym.Env):
    def __init__(self, visualize=False):
        super(Environment, self).__init__()

        self.game = game_template(num_players)
        self.space = create_space(self.game)
        self.width, self.height = self.game.court.dimensions

        self.action_space = spaces.Box(
            low=-np.ones(action_shape, dtype=np.float32),
            high=np.ones(action_shape, dtype=np.float32),
        )
        self.observation_space = spaces.Box(
            low=-np.ones(observation_shape, dtype=np.float32),
            high=np.ones(observation_shape, dtype=np.float32),
        )
        self.total_reward = 0.0

        self.visualize = visualize
        if self.visualize:
            pygame.init()
            resolution = resolution_for(self.game, display_scale)
            padded_resolution = padded_resolution_for(
                self.game, display_scale, display_scale
            )
            scale = resolution[0] / self.game.court.dimensions[0]
            padding = (padded_resolution[0] - resolution[0]) / 2

            self.drawer = Drawer(padded_resolution, scale, (padding, padding))
            self.engine = Engine(padded_resolution, fps)
            self.surface = self.engine.surface
            self.clock = self.engine.clock
            self.render_settings = self.engine.render_settings

    def step(self, action):
        turn_degrees, acceleration = action
        turn_degrees = turn_degrees.item()
        acceleration = acceleration.item()
        self.player.turn(turn_degrees).accelerate(acceleration)
        step_space(self.space, time_frame)

        if self._is_out_of_bounds():
            reward = -(10**3)
        else:
            shot_value_multiplier = 1 + self._standstill_bonus() + self._noturn_bonus()
            reward = (
                shot_value_multiplier * self._shot_value()
                - 0.05
                - 0.05 * abs(turn_degrees)
                - 0.05 * abs(acceleration)
            )
        self.total_reward += reward

        observation = self._get_observation()
        done = self._is_out_of_bounds() or self._lost_possession()
        info = {}
        return observation, reward, done, info

    def reset(self):
        self.total_reward = 0.0
        self.court = self.game.court
        self.player = self.game.teams[0][0]
        self.target_hoop = self.game.target_hoop(self.player)

        while self.game.ball.mode != BallMode.HELD:
            self.space.step(0.0)

        if not self.player.has_ball:
            self.game.ball.turnover()

        state = PlayerState.from_observation(
            self.observation_space.sample(), self.player, self.court
        )

        def place_at_random_state():
            self.player.place_at(
                (state.position_x, state.position_y), state.orientation
            )

        place_at_random_state()
        while self.game.ball.mode != BallMode.HELD:
            self.space.step(0.0)
            place_at_random_state()

        observation = self._get_observation()
        return observation

    def _shot_value(self):
        return self.target_hoop.expected_value_of_shot_by(self.player)

    def _standstill_bonus(self):
        current_speed = vector_length(self.player.velocity)
        scale = current_speed / self.player.physical_attributes.max_velocity
        if scale > 1:
            return 0
        else:
            assert scale > -(10**-6)
            return 1 - scale

    def _noturn_bonus(self):
        return 0

    def _get_observation(self):
        is_in_bounds = not self._is_out_of_bounds()
        return PlayerState.from_player(self.player).to_observation(
            self.player, self.court, is_in_bounds
        )

    def _is_out_of_bounds(self):
        return not self.court.is_inbounds(self.player)

    def _lost_possession(self):
        return not self.player.has_ball

    def render(self):
        try:
            if not self.engine.should_loop():
                self.visualize = False
                pygame.quit()
        except pygame.error:
            self.visualize = False

        if self.visualize:
            self.surface.fill((255, 255, 255))

            self.drawer.surface.fill(BACKGROUND_COLOR)
            draw_game(self.drawer, self.game)

            target_rectangle = self.engine.surface.get_rect()
            source_rectangle = self.drawer.surface.get_rect(
                center=target_rectangle.center
            )
            self.engine.surface.blit(self.drawer.surface, source_rectangle)

            self.clock.tick(self.render_settings.frame_rate)
            pygame.display.set_caption(str(round(self.clock.get_fps(), 2)))
            pygame.display.flip()

    def close(self):
        if self.visualize:
            pygame.quit()


def makegym():
    return Environment()


def makegymnasium():
    return Environment()


check_env(Environment())
