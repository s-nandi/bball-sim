from bball_server import Game, Team
from bball_server.create import (
    create_game,
    create_initialized_player,
    create_court,
    create_player_attributes,
    create_hoop,
    create_three_point_line,
)
from engine import Engine


def setup_game() -> Game:
    attributes = create_player_attributes(max_acceleration=2.34)
    player_1 = create_initialized_player(position=(4, 4), attributes=attributes)
    player_2 = create_initialized_player(position=(7, 7), attributes=attributes)
    width = 28.65
    height = 15.24
    three_point_line = create_three_point_line(width, height)
    hoop = create_hoop(width, height, 1.6, three_point_line)
    court = create_court(width, height, hoop)
    return create_game(teams=[Team(player_1), Team(player_2)], court=court)


def main():
    game = setup_game()
    engine = Engine(game, lambda _: game.teams[0][0].accelerate(1))
    engine.run()


if __name__ == "__main__":
    main()
