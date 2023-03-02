from pathlib import Path
from neural.movement import parse, sb3


def main(args=None):
    args = parse.parse(args)
    if args.type == parse.LEARN:
        sb3.learn(args.epochs, args.checkpoint_interval, Path(args.output_path))
    else:
        assert args.type == parse.LOAD
        sb3.load(args.episodes, args.visualize, Path(args.input_path), args.epoch)
