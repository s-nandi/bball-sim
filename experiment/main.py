from dataclasses import asdict
import pprint
from experiment import initiate, run, parse
import ga

FPS = 90
SPEED_SCALE = 5.0


def load(args):
    game, parameters_list = ga.load(
        folder=args.input_folder, generation_number=args.generation
    )
    if args.visualize:
        game.assign_team_strategy(0, parameters_list[args.index_1].strategy())
        game.assign_team_strategy(1, parameters_list[args.index_2].strategy())
        simulate(args, game)
    else:
        pprint.pprint([asdict(parameters) for parameters in parameters_list])
        pprint.pprint(f"# parameters: {len(parameters_list)}")


def learn(args):
    ga.learn(
        num_players=args.player_count,
        population_size=args.population_size,
        generation_limit=args.generations,
        output_folder=args.output_folder,
        output_frequency=args.output_frequency,
    )


def simulate(args, game=None):
    if game is None:
        game = initiate.canonical_game(2)
    if args.duration is not None:
        run.headless(
            game, fps=args.fps, speed_scale=args.speed_scale, duration=args.duration
        )
    else:
        assert args.display_scale is not None
        run.visualize(
            game,
            fps=args.fps,
            speed_scale=args.speed_scale,
            display_scale=args.display_scale,
        )


def main():
    args = parse.parse()
    table = {parse.SIMULATE: simulate, parse.LEARN: learn, parse.LOAD: load}
    table[args.type](args)


if __name__ == "__main__":
    main()
