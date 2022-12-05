from experiment import initiate, compare, visualize
from bball import Game
from bball.create import created_spaced_strategy, create_strategy


def visualize_game(game: Game):
    visualize.visualize(game, fps=90, speed_scale=5.0, display_scale=0.3)


def compare_strategies(game: Game):
    comparison = compare.compare(game, duration=300.0, time_frame=1 / 90)
    return comparison


def main():
    do_visualize = 0
    game = initiate.canonical_game(2)
    game.assign_team_strategy(0, created_spaced_strategy(4, 3.0, 1.0, True, 0.5))
    game.assign_team_strategy(1, create_strategy(10, 0.5))

    if do_visualize:
        visualize_game(game)
    else:
        print(compare_strategies(game))


if __name__ == "__main__":
    main()
