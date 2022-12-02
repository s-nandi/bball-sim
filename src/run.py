from bball.initiate import two_uniform_players
from runner import run_game


def main():
    run_game(two_uniform_players(), fps=30)


if __name__ == "__main__":
    main()
