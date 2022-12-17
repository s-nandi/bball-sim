from typing import Optional
from pathlib import Path
from tqdm import tqdm
import torch
from torch import nn
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt
from experiment.initiate import canonical_game
from neural.save import save_model, model_file_name, suffix_for
from neural.loops import test_loop, train_loop
from neural.shot_value.datasets import PlayerDataset
from neural.shot_value.plot import plot_model, plot_loss

num_players = 1
game_template = canonical_game


class Model(nn.Module):
    input_factors = 5
    hidden_nodes = 50
    output_factors = 1

    def __init__(self):
        super(Model, self).__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(self.input_factors, self.hidden_nodes),
            nn.LeakyReLU(),
            nn.Linear(self.hidden_nodes, self.hidden_nodes),
            nn.LeakyReLU(),
            nn.Linear(self.hidden_nodes, self.output_factors),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.flatten(x)
        x = self.layers(x)
        return x


def train(
    num_samples,
    batch_size,
    learning_rate,
    epochs,
    checkpoint_interval,
    output_folder: Path,
):
    verbose = False

    game = game_template(num_players)
    train_dataset = PlayerDataset(num_samples, game)
    test_dataset = PlayerDataset(num_samples, game)
    assert len(train_dataset) == num_samples
    assert len(test_dataset) == num_samples

    model = Model()
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    losses = []
    for epoch in tqdm(range(epochs)):
        is_checkpoint_epoch = verbose or epoch % checkpoint_interval == 0
        if is_checkpoint_epoch:
            tqdm.write(f"Epoch {epoch+1}\n-------------------------------")
        train_loop(train_dataloader, model, loss_fn, optimizer, is_checkpoint_epoch)
        loss = test_loop(test_dataloader, model, loss_fn, is_checkpoint_epoch)
        losses.append(loss)
        if is_checkpoint_epoch:
            save_model(model, output_folder, epoch)

    for name, dataloader in zip(
        ["train", "test"],
        [train_dataloader, test_dataloader],
    ):
        test_model(name, dataloader, model, loss_fn, output_folder)

    plot_loss(losses)
    plt.savefig(output_folder.joinpath("loss.png"))
    plt.clf()
    save_model(model, output_folder)
    save_model(model, output_folder, epochs)


def test_model(name, dataloader, model, loss_fn, output_folder):
    loss = test_loop(dataloader, model, loss_fn, False)
    print(f"{name} loss:", loss)

    plot_model([dataloader], model)
    plt.savefig(output_folder.joinpath(f"{name}_predictions.png"))
    plt.clf()


def _load(input_folder: Path, epoch: Optional[int]):
    file_name = model_file_name(epoch)
    path = input_folder.joinpath(file_name)
    model = Model()
    loss_fn = nn.MSELoss()
    model.load_state_dict(torch.load(path))
    return model, loss_fn


def test(num_samples, input_folder: Path, epoch: Optional[int]):
    game = game_template(num_players)
    model, loss_fn = _load(input_folder, epoch)
    dataset = PlayerDataset(num_samples, game)
    dataloader = DataLoader(dataset, 1)
    test_model(f"post{suffix_for(epoch)}", dataloader, model, loss_fn, input_folder)
