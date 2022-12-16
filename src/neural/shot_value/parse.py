import argparse

LEARN = "learn"
LOAD = "load"


def _build_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("num_samples", type=int)
    parser.add_argument("batch_size", type=int)
    parser.add_argument("learning_rate", type=float)
    parser.add_argument("epochs", type=int)
    parser.add_argument("checkpoint_interval", type=int)
    parser.add_argument("output_folder", type=str)


def _build_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("num_samples", type=int)
    parser.add_argument("input_folder", type=str)
    parser.add_argument("--epoch", type=int, default=None)


def _build_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type")
    subparsers.required = True
    _build_learning_subparser(subparsers.add_parser(LEARN))
    _build_loading_subparser(subparsers.add_parser(LOAD))
    return parser


def parse(args=None):
    parser = argparse.ArgumentParser("ShotValueNN")
    _build_parser(parser)
    args = parser.parse_args(args)
    return args
