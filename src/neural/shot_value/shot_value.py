import torch
from torch import nn
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt
from experiment.initiate import canonical_game
from neural.datasets import PlayerDataset
from neural.loops import test_loop, train_loop
from neural.shot_value.plot import plot_model, plot_loss


class Model(nn.Module):
    input_factors = 5
    hidden_nodes = 8
    output_factors = 1

    def __init__(self):
        super(Model, self).__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(self.input_factors, self.hidden_nodes),
            nn.ReLU(),
            nn.Linear(self.hidden_nodes, self.output_factors),
        )

    def forward(self, x):
        x = self.flatten(x)
        x = self.layers(x)
        return x


def main():
    verbose = True

    n = 500
    game = canonical_game(1)
    dataset = PlayerDataset(n, game)

    batch_size = 250
    learning_rate = 0.3
    epochs = 500

    model = Model()
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    losses = []
    for t in range(epochs):
        if verbose:
            print(f"Epoch {t+1}\n-------------------------------")
        train_loop(dataloader, model, loss_fn, optimizer, verbose)
        loss = test_loop(dataloader, model, loss_fn, verbose)
        losses.append(loss)
    if verbose:
        print("Done!")

    plot_model(dataloader, model)
    plt.show()
    plot_loss(losses)
    plt.show()


if __name__ == "__main__":
    main()
