import argparse

LEARN = "learn"
LOAD = "load"

learn_args = "learn 1000000 0.1 0.7 0.00001 0.001 output/qlearn.txt"
load_args = "load 5 50 output/qlearn.txt --visualize"
noviz_load_args = "load 1000 100000 output/qlearn.txt"


def _build_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("steps", type=int)
    parser.add_argument("learning_rate", type=float)
    parser.add_argument("discount_factor", type=float)
    parser.add_argument("epsilon_decay", type=float)
    parser.add_argument("min_epsilon", type=float)
    parser.add_argument("output_path", type=str)


def _build_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("episodes", type=int)
    parser.add_argument("max_steps", type=int)
    parser.add_argument("input_path", type=str)
    parser.add_argument("--visualize", action="store_true")


def _build_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type", required=True)
    _build_learning_subparser(subparsers.add_parser(LEARN))
    _build_loading_subparser(subparsers.add_parser(LOAD))


def parse(args=None):
    parser = argparse.ArgumentParser("Q-Learning")
    _build_parser(parser)
    return parser.parse_args(args)
