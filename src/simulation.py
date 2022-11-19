import dataclasses
import math
from typing import Callable
import pygame
import pymunk
import pymunk.pygame_util

ScreenDimension = int
Fps = int
TimePerFrame = float
SpeedScale = float


@dataclasses.dataclass
class ScreenParams:
    width: ScreenDimension
    height: ScreenDimension
    fps: Fps


@dataclasses.dataclass
class RenderParams:
    screen: pygame.Surface
    fps: Fps
    clock: pygame.time.Clock
    draw_options: pymunk.pygame_util.DrawOptions

    def __init__(self, screen_params: ScreenParams):
        self.screen = pygame.display.set_mode(
            (screen_params.width, screen_params.height)
        )  # type: ignore
        self.fps = screen_params.fps
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)


@dataclasses.dataclass
class SimulationParams:
    space: pymunk.Space
    time_per_frame: TimePerFrame

    def __init__(
        self,
        fps: Fps,
        speed_scale: SpeedScale = 1.0,
    ):
        self.space = pymunk.Space()
        pymunk.pygame_util.positive_y_is_up = True
        self.time_per_frame = speed_scale / fps


@dataclasses.dataclass
class Simulator:
    render_params: RenderParams
    simulation_params: SimulationParams
    update: Callable[[SimulationParams], None]
    running: bool = True

    @classmethod
    def max_allowable_step(cls) -> TimePerFrame:
        return 0.01

    def __init__(
        self,
        screen_params: ScreenParams,
        initialize: Callable[[pymunk.Space], None],
        update: Callable[[SimulationParams], None],
        simulation_speed_scale: SpeedScale,
    ):
        self.render_params = RenderParams(screen_params)
        self.simulation_params = SimulationParams(
            screen_params.fps, simulation_speed_scale
        )
        self.update = update

        initialize(self.simulation_params.space)

    def run(self) -> None:
        while self.running:
            self.loop()

    def process_actions(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def loop(self) -> None:
        self.process_actions()
        self.update(self.simulation_params)
        self.step(self.simulation_params)
        self.draw(self.render_params, self.simulation_params)
        self.caption_fps(self.render_params)

    @classmethod
    def step(cls, simulation_params: SimulationParams):
        time_per_frame = simulation_params.time_per_frame
        substeps = math.ceil(max(1, time_per_frame / cls.max_allowable_step()))
        for _ in range(substeps):
            simulation_params.space.step(time_per_frame / substeps)

    @staticmethod
    def draw(render_params: RenderParams, simulation_params: SimulationParams):
        render_params.screen.fill(pygame.Color("white"))
        simulation_params.space.debug_draw(render_params.draw_options)
        render_params.clock.tick(render_params.fps)
        pygame.display.flip()

    @staticmethod
    def caption_fps(render_params: RenderParams):
        pygame.display.set_caption(f"fps: {str(render_params.clock.get_fps())}")
