from experiment import initiate, compare, visualize
from bball import Game


def visualize_game(game: Game):
    visualize.visualize(game, fps=90.0, speed_scale=5.0, display_scale=0.3)


def compare_strategies(game: Game):
    comparison = compare.compare(game, duration=300.0, time_frame=1 / 90)
    return comparison


def main():
    game = initiate.multiple_players(2)

    # visualize_game(game)
    print(compare_strategies(game))


if __name__ == "__main__":
    main()
