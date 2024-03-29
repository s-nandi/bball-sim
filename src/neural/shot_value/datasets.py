from copy import deepcopy
from random import uniform
import torch
from torch.utils.data import Dataset
from bball import Game, Player, Court, Hoop
from bball.utils import divide_by


def create_player_on_court(base_player: Player, court: Court) -> Player:
    player = deepcopy(base_player)
    position = tuple((uniform(0, court.dimensions[i]) for i in range(2)))
    random_angle = uniform(0, 360)
    max_velocity = player.physical_attributes.max_acceleration * 3
    velocity_magnitude = uniform(0, max_velocity)
    return player.place_at(position, random_angle).with_velocity(velocity_magnitude)


def to_tensor(player: Player, court: Court):
    bigger_dimension = max(court.dimensions)
    position = divide_by(player.position, bigger_dimension)
    velocity = divide_by(player.velocity, bigger_dimension)
    orientation = player.orientation_degrees / 360
    return torch.Tensor((*position, *velocity, orientation))


def evaluate_state(player: Player, hoop: Hoop):
    shot_value = hoop.expected_value_of_shot_by(player) / 3
    assert 0 <= shot_value <= 1
    return shot_value


def generate_data(game: Game):
    base_player = game.teams[0][0]
    target_hoop = game.target_hoop(base_player)
    random_player = create_player_on_court(base_player, game.court)
    player_tensor = to_tensor(random_player, game.court)
    fitness_value = evaluate_state(random_player, target_hoop)

    fitness = torch.Tensor(1)
    fitness.fill_(fitness_value)
    assert player_tensor.shape == (5,)
    assert fitness.shape == (1,)
    return player_tensor, fitness


def generate_data_n(n: int, game: Game):
    vecs = []
    fitnesses = []
    for _ in range(n):
        vec, fitness = generate_data(game)
        vecs.append(vec)
        fitnesses.append(fitness)
    return vecs, fitnesses


class PlayerDataset(Dataset):
    def __init__(self, n: int, game: Game, transform=None, target_transform=None):
        game = deepcopy(game)
        self.points, self.labels = generate_data_n(n, game)
        self.game = game
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        point = self.points[idx].unsqueeze(0)
        label = self.labels[idx]
        if self.transform:
            point = self.transform(point)
        if self.target_transform:
            label = self.target_transform(label)
        return point, label
