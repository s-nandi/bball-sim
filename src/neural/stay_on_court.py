import torch
from torch import nn
from torch.utils.data import DataLoader
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from neural.datasets import PlayerDataset, game
from bball import Court

torch.manual_seed(3)


class Model(nn.Module):
    input_factors = 5
    hidden_nodes = 10
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


def train_loop(dataloader, model, loss_fn, optimizer, verbose=False):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            if verbose:
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn, verbose=False):
    num_batches = len(dataloader)
    test_loss, mse = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            mse += (pred - y).square().type(torch.float).mean().item()

    test_loss /= num_batches
    if verbose:
        print(f"Test Error: \n MSE: {(mse):>8f}, Avg loss: {test_loss:>8f} \n")
    return test_loss


# https://stackoverflow.com/a/50784012
def color_fader(c1, c2, mix=0):
    c1 = np.array(colors.to_rgb(c1))
    c2 = np.array(colors.to_rgb(c2))
    return colors.to_hex((1 - mix) * c1 + mix * c2)


def to_colors(values, max_value=None):
    if max_value is None:
        max_value = max(values)

    # assert min(values) >= 0
    assert max(values) <= max_value

    values = [max(0, value) / max_value for value in values]
    color_1 = (1, 0, 0)
    color_2 = (0, 0, 1)
    colors = [color_fader(color_1, color_2, value) for value in values]
    return colors


def create_subplots(num_horiz, num_vert):
    dimensions = game.court.dimensions
    fig, axs = plt.subplots(
        num_horiz,
        num_vert,
        figsize=(dimensions[0] / num_horiz, dimensions[1] / num_vert),
    )
    return fig, axs


def draw_hoop(ax, court: Court):
    pass


def plot_model(dataloader, model):
    xs = []
    ys = []
    evaluations = []
    expecteds = []

    fig, axs = create_subplots(1, 2)
    ax_1, ax_2 = axs
    for data, expected in dataloader:
        batch_size = data.shape[0]

        assert data.shape == (batch_size, 1, 5)
        positions = data.squeeze()[:, 0:2]

        assert expected.shape == (batch_size, 1)

        outputs = model(data)
        assert outputs.shape == (batch_size, 1)

        for position, output, expected in zip(positions, outputs, expected):
            xs.append(position[0].item())
            ys.append(position[1].item())
            expecteds.append(expected.item())
            evaluations.append(output.item())
    max_value = max(max(expecteds), max(evaluations))
    expected_colors = to_colors(expecteds, max_value)
    model_colors = to_colors(evaluations, max_value)
    ax_1.scatter(xs, ys, c=model_colors)
    ax_2.scatter(xs, ys, c=expected_colors)


def plot_loss(losses):
    plt.plot(losses)
    plt.xlabel("Epoch")
    plt.ylim([-1, max(plt.ylim())])
    plt.ylabel("Loss")
    plt.title("Keras training progress")


def main():
    verbose = True

    n = 100
    dataset = PlayerDataset(n)

    batch_size = 50
    learning_rate = 0.05
    epochs = 100

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
    # plot_loss(losses)
    # plt.show()


if __name__ == "__main__":
    main()
