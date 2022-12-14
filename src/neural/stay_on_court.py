from torch import nn
from neural.datasets import PlayerDataset


class Model(nn.Module):
    input_factors = 5
    hidden_nodes = 10
    output_factors = 2

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


def create_model():
    pass


def main():
    dataset = PlayerDataset(3)
    print(dataset[0][0], dataset[0][1])
    model = create_model()


if __name__ == "__main__":
    main()
