import argparse

LEARN = "learn"
LOAD = "load"
QLEARNING = "q"
DQN = "dqn"
SB3 = "sb3"

q_learn_args = "q learn 1000000 0.1 0.7 0.00001 0.001 output/qlearn/q.txt"
q_load_args = "q load 5 50 output/qlearn/q.txt --visualize"
q_noviz_load_args = "q load 1000 100000 output/qlearn/q.txt"

sb3_learn_args = "python -m neural.rl sb3 learn 100000 10000 output/sb3"
sb3_load_args = "sb3 load 1 output/sb3 --epoch 100000 --visualize"
sb3_noviz_load_args = "python -m neural.rl sb3 load 100 output/sb3"


def _build_qlearning_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("steps", type=int)
    parser.add_argument("learning_rate", type=float)
    parser.add_argument("discount_factor", type=float)
    parser.add_argument("epsilon_decay", type=float)
    parser.add_argument("min_epsilon", type=float)
    parser.add_argument("output_path", type=str)


def _build_qlearning_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("episodes", type=int)
    parser.add_argument("max_steps", type=int)
    parser.add_argument("input_path", type=str)
    parser.add_argument("--visualize", action="store_true")


def _build_qlearning_subparser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type", required=True)
    _build_qlearning_learning_subparser(subparsers.add_parser(LEARN))
    _build_qlearning_loading_subparser(subparsers.add_parser(LOAD))


def _build_dqn_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("output_path", type=str)


def _build_dqn_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("input_path", type=str)


def _build_dqn_subparser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type", required=True)
    _build_dqn_learning_subparser(subparsers.add_parser(LEARN))
    _build_dqn_loading_subparser(subparsers.add_parser(LOAD))


def _build_sb3_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("epochs", type=int)
    parser.add_argument("checkpoint_interval", type=int)
    parser.add_argument("output_path", type=str)


def _build_sb3_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("episodes", type=int)
    parser.add_argument("input_path", type=str)
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--epoch", type=int, default=None)


def _build_sb3_subparser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type", required=True)
    _build_sb3_learning_subparser(subparsers.add_parser(LEARN))
    _build_sb3_loading_subparser(subparsers.add_parser(LOAD))


def _build_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="algo", required=True)
    _build_qlearning_subparser(subparsers.add_parser(QLEARNING))
    _build_dqn_subparser(subparsers.add_parser(DQN))
    _build_sb3_subparser(subparsers.add_parser(SB3))


def parse(args=None):
    parser = argparse.ArgumentParser("Reinforcement Learning")
    _build_parser(parser)
    return parser.parse_args(args)
