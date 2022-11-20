import math
import pygame
from simulation.render_params import RenderParams
from simulation.simulation_params import SimulationParams
from simulation.screen_params import ScreenParams
from simulation.types import TimePerFrame, SpeedScale
from simulation.game_interface import GameInterface


def step(simulation_params: SimulationParams, max_allowable_step: float):
    time_per_frame = simulation_params.time_per_frame
    substeps = math.ceil(max(1, time_per_frame / max_allowable_step))
    for _ in range(substeps):
        simulation_params.space.step(time_per_frame / substeps)


def draw(render_params: RenderParams, simulation_params: SimulationParams):
    render_params.screen.fill(pygame.Color("white"))
    simulation_params.space.debug_draw(render_params.draw_options)
    render_params.clock.tick(render_params.fps)
    pygame.display.flip()


def caption_fps(render_params: RenderParams):
    pygame.display.set_caption(f"fps: {str(render_params.clock.get_fps())}")


class Simulator:
    render_params: RenderParams
    simulation_params: SimulationParams
    game: GameInterface
    running: bool = True

    @classmethod
    def max_allowable_step(cls) -> TimePerFrame:
        return 0.01

    def __init__(
        self,
        screen_params: ScreenParams,
        game: GameInterface,
        simulation_speed_scale: SpeedScale,
    ):
        self.render_params = RenderParams(screen_params)
        self.simulation_params = SimulationParams(
            screen_params.fps, simulation_speed_scale
        )
        self.game = game

    def run(self) -> None:
        self.start()
        while self.running:
            self.loop()

    def process_actions(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def start(self) -> None:
        self.game.initialize(self.simulation_params.space)

    def loop(self) -> None:
        self.process_actions()
        self.game.update(self.simulation_params.space)
        step(self.simulation_params, self.max_allowable_step())
        draw(self.render_params, self.simulation_params)
        caption_fps(self.render_params)
