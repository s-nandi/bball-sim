from dataclasses import asdict
import pprint
from experiment import initiate, run, parse
import ga

FPS = 90
SPEED_SCALE = 5.0


def load(args):
    generation_number, game, metadata, parameters_list = ga.load(
        folder=args.input_folder, generation_number=args.generation
    )
    args.generation = generation_number
    args.fps = metadata.fps if args.fps is None else args.fps
    args.duration = metadata.duration if args.duration is None else args.duration
    args.speed_scale *= metadata.speed_scale
    if args.evaluate:

        def comparator(parameters_1, parameters_2):
            return ga.compare(
                game,
                parameters_1,
                parameters_2,
                duration=args.duration,
                fps=args.fps,
                speed_scale=args.speed_scale,
            )

        serializer = ga.parameters.ParametersSerializer(
            args.input_folder
        ).jump_to_generation(args.generation)
        _, evaluation = ga.tournament(comparator, parameters_list)
        pprint.pprint(asdict(evaluation))
        serializer.serialize_evaluation(evaluation)
    elif args.visualize:
        index_1 = args.index_1
        index_2 = args.index_2
        if index_1 is not None and index_2 is None:
            index_2 = index_1
        if index_2 is None and index_1 is not None:
            index_1 = index_2
        if index_1 is None and index_2 is None:
            index_1 = 0
            index_2 = 1
        game.assign_team_strategy(0, parameters_list[index_1].strategy())
        game.assign_team_strategy(1, parameters_list[index_2].strategy())
        simulate(args, game)
    else:
        indices = []
        if args.index_1 is not None:
            indices.append(args.index_1)
        if args.index_2 is not None:
            indices.append(args.index_2)
        if not indices:
            indices = list(range(len(parameters_list)))
        pprint.pprint([asdict(parameters_list[index]) for index in indices])
        pprint.pprint(f"# parameters: {len(parameters_list)}")
        if args.index_1 is not None and args.index_2 is not None:
            delta = ga.compare(
                game,
                parameters_list[args.index_1],
                parameters_list[args.index_2],
                fps=args.fps,
                duration=args.duration,
                speed_scale=args.speed_scale,
            )
            print(f"delta = {delta}")


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
    if args.display_scale is not None:
        run.visualize(
            game,
            fps=args.fps,
            speed_scale=args.speed_scale,
            display_scale=args.display_scale,
        )
    else:
        assert args.duration is not None
        run.headless(
            game, fps=args.fps, speed_scale=args.speed_scale, duration=args.duration
        )


def main():
    args = parse.parse()
    table = {parse.SIMULATE: simulate, parse.LEARN: learn, parse.LOAD: load}
    table[args.type](args)


if __name__ == "__main__":
    main()
