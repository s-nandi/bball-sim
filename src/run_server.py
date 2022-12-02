from bball_server import Team, DrawInterface, Color, Point, Corners, draw_game
from bball_server.create import create_game, create_initialized_player


class DrawObject(DrawInterface):
    def draw_circle(self, center: Point, radius: float, color: Color, fill: bool):
        pass

    def draw_line(self, point_1: Point, point_2: Point, color: Color):
        pass

    def draw_rectangle(self, corners: Corners, color: Color, fill: bool):
        pass


if __name__ == "__main__":
    player_1 = create_initialized_player(position=(0, 0))
    player_2 = create_initialized_player(position=(5, 0))
    game = create_game(teams=[Team(player_1), Team(player_2)])
    draw_object = DrawObject()
    draw_game(draw_object, game)
