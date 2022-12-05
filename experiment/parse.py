import argparse

SIMULATE = "simulate"
LEARN = "learn"

DURATION_SHORT = "-d"
DURATION_LONG = "--duration"
DISPLAY_SCALE_SHORT = "-s"
DISPLAY_SCALE_LONG = "--display-scale"


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("Runner")
    subparsers = parser.add_subparsers(dest="type")
    simulation_parser = subparsers.add_parser(SIMULATE)
    simulation_parser.add_argument("fps", type=int)
    simulation_parser.add_argument("speed_scale", type=float)
    simulation_parser.add_argument(DURATION_SHORT, DURATION_LONG, type=float)
    simulation_parser.add_argument(DISPLAY_SCALE_SHORT, DISPLAY_SCALE_LONG, type=float)
    return parser


def _parse_args(parser: argparse.ArgumentParser, args=None):
    args = parser.parse_args(args)
    headless_str = f"{DURATION_SHORT} / {DURATION_LONG} (headless)"
    visualize_str = f"{DISPLAY_SCALE_SHORT} / {DISPLAY_SCALE_LONG} (headless)"
    all_options_str = f"{headless_str} and {visualize_str}"
    if args.duration is not None and args.display_scale is not None:
        error_msg = f"{SIMULATE} cannot be used with more than one of {all_options_str}"
        parser.error(error_msg)
    if args.duration is None and args.display_scale is None:
        error_msg = f"{SIMULATE} requires exactly one of {all_options_str}"
        parser.error(error_msg)
    return args


def parse(args=None):
    parser = _create_parser()
    return _parse_args(parser, args)
