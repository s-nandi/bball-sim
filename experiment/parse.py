from typing import Optional
import argparse

SIMULATE = "simulate"
LEARN = "learn"
LOAD = "load"

DURATION_SHORT = "-d"
DURATION_LONG = "--duration"
DISPLAY_SCALE_SHORT = "-k"
DISPLAY_SCALE_LONG = "--display-scale"
SPEED_SHORT = "-s"
SPEED_LONG = "--speed"
SPEED_DEST = "speed_scale"


def _build_simulation_parser(parser: argparse.ArgumentParser):
    parser.add_argument("fps", type=int)
    parser.add_argument(DURATION_SHORT, DURATION_LONG, type=float)
    parser.add_argument(
        SPEED_SHORT, SPEED_LONG, dest=SPEED_DEST, type=float, default=1.0
    )
    parser.add_argument(DISPLAY_SCALE_SHORT, DISPLAY_SCALE_LONG, type=float)


def _build_learning_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("player_count", type=int)
    parser.add_argument("population_size", type=int)
    parser.add_argument("output_folder", type=str)
    parser.add_argument("--output_frequency", type=int, default=10)
    parser.add_argument("--generations", type=int)


def _build_loading_subparser(parser: argparse.ArgumentParser):
    parser.add_argument("input_folder", type=str)
    parser.add_argument("-g", "--generation", type=int)
    parser.add_argument("-v", "--visualize", action="store_true")
    parser.add_argument("-fps", "--fps", type=int)
    parser.add_argument(DURATION_SHORT, DURATION_LONG, type=float)
    parser.add_argument(
        SPEED_SHORT, SPEED_LONG, dest=SPEED_DEST, type=float, default=1.0
    )
    parser.add_argument(DISPLAY_SCALE_SHORT, DISPLAY_SCALE_LONG, type=float)
    parser.add_argument("-i1", "--index_1", type=int)
    parser.add_argument("-i2", "--index_2", type=int)
    parser.add_argument("-e", "--evaluate", action="store_true")


def _build_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="type")
    subparsers.required = True
    _build_simulation_parser(subparsers.add_parser(SIMULATE))
    _build_learning_subparser(subparsers.add_parser(LEARN))
    _build_loading_subparser(subparsers.add_parser(LOAD))
    return parser


def _validate_simulation_args(args) -> Optional[str]:
    headless_str = f"{DURATION_SHORT} / {DURATION_LONG} (headless)"
    visualize_str = f"{DISPLAY_SCALE_SHORT} / {DISPLAY_SCALE_LONG} (headless)"
    all_options_str = f"{headless_str} and {visualize_str}"
    if args.duration is not None and args.display_scale is not None:
        error_msg = f"{SIMULATE} cannot be used with more than one of {all_options_str}"
        return error_msg
    if args.duration is None and args.display_scale is None:
        error_msg = f"{SIMULATE} requires exactly one of {all_options_str}"
        return error_msg
    return None


def _validate_args(args) -> Optional[str]:
    if args.type == SIMULATE:
        return _validate_simulation_args(args)
    if args.type == LOAD and args.visualize:
        return _validate_simulation_args(args)
    return None


def parse(args=None):
    parser = argparse.ArgumentParser("Runner")
    _build_parser(parser)
    args = parser.parse_args(args)
    error = _validate_args(args)
    if error is not None:
        parser.error(error)
    return args
