import argparse

LEARN = "learn"
LOAD = "load"

sb3_learn_args = "learn 10000000 100000 output/basic_offense"
sb3_load_args = "load 10 output/basic_offense --visualize"
sb3_noviz_load_args = "load 80 output/basic_offense"


def _build_sb3_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("epochs", type=int)
    parser.add_argument("checkpoint_interval", type=int)
    parser.add_argument("output_path", type=str)


def _build_sb3_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("episodes", type=int)
    parser.add_argument("input_path", type=str)
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--epoch", type=int, default=None)


def _build_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type", required=True)
    _build_sb3_learning_subparser(subparsers.add_parser(LEARN))
    _build_sb3_loading_subparser(subparsers.add_parser(LOAD))


def parse(args=None):
    parser = argparse.ArgumentParser("Reinforcement Learning")
    _build_parser(parser)
    return parser.parse_args(args)
