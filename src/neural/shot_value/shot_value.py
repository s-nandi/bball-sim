from pathlib import Path
from neural.shot_value import parse, model


def learn(args):
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)
    model.train(
        args.num_samples,
        args.batch_size,
        args.learning_rate,
        args.epochs,
        args.checkpoint_interval,
        Path(args.output_folder),
    )


def load(args):
    model.test(args.num_samples, Path(args.input_folder), args.epoch)


fast_learn_args = "learn 3000 500 0.8 100 25 output/test"
slow_learn_args = "learn 3000 500 0.8 100000 10000 output/test"
load_args = "load 2000 output/test"


def main(args=None):
    args = parse.parse(args)

    table = {parse.LEARN: learn, parse.LOAD: load}
    table[args.type](args)
