from pathlib import Path
from neural.rl import parse, qlearn, dqn, sb3


def main(args=None):
    args = parse.parse(args)
    if args.algo == parse.QLEARNING:
        if args.type == parse.LEARN:
            qlearn.learn(
                args.steps,
                args.learning_rate,
                args.discount_factor,
                args.epsilon_decay,
                args.min_epsilon,
                Path(args.output_path),
            )
        else:
            assert args.type == parse.LOAD
            qlearn.load(
                args.episodes, args.max_steps, args.visualize, Path(args.input_path)
            )
    elif args.algo == parse.SB3:
        if args.type == parse.LEARN:
            sb3.learn(args.epochs, args.checkpoint_interval, Path(args.output_path))
        else:
            assert args.type == parse.LOAD
            sb3.load(args.episodes, args.visualize, Path(args.input_path), args.epoch)
    else:
        assert args.algo == parse.DQN
        if args.type == parse.LEARN:
            dqn.learn(Path(args.output_path))
        else:
            assert args.type == parse.LOAD
            dqn.load(Path(args.input_path))
