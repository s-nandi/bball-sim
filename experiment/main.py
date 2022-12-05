from experiment import initiate, run
from bball import Game
from bball.create import created_spaced_strategy, create_strategy

simulation_parameters = {"fps": 90, "speed_scale": 5.0}


def visualize_game(game: Game):
    run.visualize(game, display_scale=0.3, **simulation_parameters)


def compare_strategies(game: Game):
    run.headless(game, duration=10, **simulation_parameters)
    return game.scoreboard


def main():
    do_visualize = False
    game = initiate.canonical_game(2)
    game.assign_team_strategy(0, created_spaced_strategy(4, 3.0, 1.0, True, 0.5))
    game.assign_team_strategy(1, create_strategy(10, 0.5))

    if do_visualize:
        visualize_game(game)
    else:
        print(compare_strategies(game))


if __name__ == "__main__":
    main()
