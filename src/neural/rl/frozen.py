import gymnasium

size = 4
observation_size = size**2
action_size = 4

import gym
from gym import spaces


class Frozen(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, env: gymnasium.Env):
        super(Frozen, self).__init__()
        self.env = env
        self.render_mode = self.env.render_mode
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(env.action_space.n)
        # Example for using image as input:
        self.observation_space = spaces.Discrete(env.observation_space.n)

    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(action)
        return observation, reward, terminated or truncated, info

    def reset(self):
        observation, _ = self.env.reset()  # reward, done, info can't be included
        return observation

    def render(self):
        return self.env.render()

    def close(self):
        return self.env.close()


def validate(env):
    assert env.observation_space.n == observation_size
    assert env.action_space.n == action_size


def makegymnasium(render_mode=None):
    env = gymnasium.make("FrozenLake-v1", render_mode=render_mode, is_slippery=True)
    validate(env)
    return env


def makegym():
    env = gym.make("FrozenLake-v1", is_slippery=True)
    validate(env)
    return env
