from typing import Tuple, Callable
import pygame
from bball_server import Game, Space
from bball_server.draw import draw_game
from draw_object import DrawObject


def scale_while_maintaining_resolution(
    max_w: float, max_h: float, target_w_to_h: float
) -> Tuple[float, float]:
    max_scale = min(max_w / target_w_to_h, max_h / 1)
    max_scale = 1000
    return (max_scale * target_w_to_h, max_scale)


DISPLAY_SCALE = 0.5
FRAME_RATE = 30


class Engine:
    game: Game
    space: Space
    screen: pygame.surface.Surface
    draw_object: DrawObject
    clock: pygame.time.Clock

    def __init__(self, game: Game, callback: Callable[[Game], None]):
        self.game = game
        self.space = Space().add(game)
        self.callback = callback

        court = game.court
        pygame.init()
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            scale_while_maintaining_resolution(
                display_info.current_w * DISPLAY_SCALE,
                display_info.current_h * DISPLAY_SCALE,
                court.width / court.height,
            )
        )
        self.draw_object = DrawObject(
            self.screen, self.screen.get_width() / court.width
        )
        self.clock = pygame.time.Clock()

    def run(self):
        while self.loop():
            self.simulate()
            self.draw()
        pygame.quit()

    def loop(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def simulate(self):
        self.callback(self.game)
        self.space.step(1 / FRAME_RATE)
        self.clock.tick(FRAME_RATE)

    def draw(self):
        self.screen.fill((255, 255, 255))
        draw_game(self.draw_object, self.game)
        pygame.display.set_caption(str(round(self.clock.get_fps(), 2)))
        pygame.display.flip()
