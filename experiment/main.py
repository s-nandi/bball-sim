from experiment import initiate, run, parse

FPS = 90
SPEED_SCALE = 5.0


def simulate(args):
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
    table = {parse.SIMULATE: simulate}
    table[args.type](args)


if __name__ == "__main__":
    main()
