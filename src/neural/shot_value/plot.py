import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from bball.utils import divide_by
from bball.draw.draw_functions import HOOP_RADIUS

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
    color_2 = (0, 1, 1)
    colors = [color_fader(color_1, color_2, value) for value in values]
    return colors


def create_subplots(num_horiz, num_vert, game):
    dimensions = game.court.dimensions
    fig, axs = plt.subplots(
        num_horiz,
        num_vert,
        figsize=(dimensions[0] / num_horiz, dimensions[1] / num_vert),
    )
    return fig, axs


def normalized_hoop_circle(game):
    court = game.court
    bigger_dimension = max(court.dimensions)
    base_player = game.teams[0][0]
    target_hoop = game.target_hoop(base_player)
    position = divide_by(target_hoop.position, bigger_dimension)
    radius = HOOP_RADIUS / max(game.court.dimensions)
    return position, radius


def draw_hoop(ax: plt.Axes, game):
    position, radius = normalized_hoop_circle(game)
    color = (0, 0, 0)
    circle = plt.Circle(position, radius, color=color, alpha=0.2)
    ax.add_patch(circle)


def plot_model(dataloaders, model):
    if not dataloaders:
        return

    game = dataloaders[0].dataset.game
    _, axes = create_subplots(len(dataloaders), 2, game)
    if len(np.array(axes).shape) == 1:
        axes = [axes]
    for axs, dataloader in zip(axes, dataloaders):
        xs = []
        ys = []
        evaluations = []
        expecteds = []

        ax_1, ax_2 = axs
        ax_1.set_title("Expected")
        ax_2.set_title("Output")
        for data, expected in dataloader:
            batch_size = data.shape[0]
            assert data.shape == (batch_size, 1, 5)
            positions = data.squeeze(1)[:, 0:2]

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
        output_colors = to_colors(evaluations, max_value)
        for ax, colors in zip(axs, [expected_colors, output_colors]):
            ax.scatter(xs, ys, c=colors)
            draw_hoop(ax, game)


def plot_loss(losses):
    plt.plot(losses)
    plt.xlabel("Epoch")
    plt.ylim([0, max(plt.ylim())])
    plt.ylabel("Loss")
    plt.title("Training progress")
