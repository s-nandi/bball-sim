import torch


def suffix_for(epoch):
    return f"_{epoch}" if epoch is not None else ""


def model_file_name(epoch):
    return f"model{suffix_for(epoch)}.pt"


def save_model(model, output_folder, epoch=None):
    output_file = output_folder.joinpath(model_file_name(epoch))
    torch.save(model.state_dict(), output_file)
