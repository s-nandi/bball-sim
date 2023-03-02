from tqdm import tqdm
import torch
from torch.nn import Module
from torch.utils.data import DataLoader


def train_loop(
    dataloader: DataLoader, model: Module, loss_fn, optimizer, verbose=False
):
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
                tqdm.write(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test_loop(dataloader: DataLoader, model: Module, loss_fn, verbose=False) -> float:
    num_batches = len(dataloader)
    test_loss, mse = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            mse += (pred - y).square().type(torch.float).mean().item()

    test_loss /= num_batches
    if verbose:
        tqdm.write(f"Test Error: \n MSE: {(mse):>8f}, Avg loss: {test_loss:>8f} \n")
    return test_loss
