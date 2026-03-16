"""Main game engine: window, clock, screen management."""
import pygame
import sys

from game.theme import SCREEN_W, SCREEN_H, FPS, TITLE, get_fonts


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fonts = get_fonts()
        self.running = True
        self.current_screen = None

        # Start with the main menu
        from game.screens.menu_screen import MenuScreen
        self.set_screen(MenuScreen(self))

    def set_screen(self, screen):
        self.current_screen = screen

    def start_config(self, preset=None):
        from game.screens.config_screen import ConfigScreen
        self.set_screen(ConfigScreen(self, preset))

    def start_simulation(self, config):
        from game.screens.simulation_screen import SimulationScreen
        from game.simulation_bridge import SimulationBridge
        bridge = SimulationBridge()
        bridge.start(config)
        self.set_screen(SimulationScreen(self, config, bridge))

    def show_evaluation(self, evaluation, config):
        from game.screens.evaluation_screen import EvaluationScreen
        self.set_screen(EvaluationScreen(self, evaluation, config))

    def show_menu(self):
        from game.screens.menu_screen import MenuScreen
        self.set_screen(MenuScreen(self))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # cap delta time to avoid spiral of death

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.show_menu()
                if self.current_screen:
                    self.current_screen.handle_event(e)

            if self.current_screen:
                self.current_screen.update(dt)
                self.current_screen.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
