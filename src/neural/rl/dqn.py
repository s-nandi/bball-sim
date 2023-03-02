from collections import namedtuple, deque
import random
from pathlib import Path
import torch
from torch import nn
from neural.rl import frozen

Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))

# https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html#replay-memory
class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class Model(nn.Module):
    input_factors = frozen.observation_size
    hidden_nodes = 50
    output_factors = frozen.action_size

    def __init__(self):
        super(Model, self).__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(self.input_factors, self.hidden_nodes),
            nn.LeakyReLU(),
            nn.Linear(self.hidden_nodes, self.hidden_nodes),
            nn.LeakyReLU(),
            nn.Linear(self.hidden_nodes, self.output_factors),
        )

    def forward(self, x):
        x = self.flatten(x)
        x = self.layers(x)
        return x


def learn(output_folder: Path):
    batch_size = 100
    discount_factor = 0.99
    min_eps = 0.05
    eps_decay = 10**-6
    update_rate = 0.005
    learning_rate = 10**-4

    policy_net = Model()
    target_net = Model()
    target_net.load_state_dict(policy_net.state_dict())

    optimizer = torch.optim.AdamW(
        policy_net.parameters(), lr=learning_rate, amsgrad=True
    )
    memory = ReplayMemory(10000)

    print("learn dqn")
    env = frozen.makegymnasium()


def load(input_folder: Path):
    print("load dqn")
    env = frozen.makegymnasium()
