import pygame
from .button import Button
from .world import World

class Screen:
    def __init__(self, world: World) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._world = world

    def main_menue(self) -> None:
        pygame.display.set_caption("Random Walk")
        font = pygame.font.SysFont("Arial", 48)

        running = True
        while running:
            self._screen.fill("black")

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = font.render("Random Walk", True, "white")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            START_BUTTON = Button(
                text="Start",
                pos=(640, 300),
                font=font,
                screen=self._screen,
            )
            QUIT_BUTTON = Button(
                text="Quit",
                pos=(640, 500),
                font=font,
                screen=self._screen,
            )
            
            self._screen.blit(MENU_TEXT, MENU_RECT)
            
            for button in [START_BUTTON, QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if START_BUTTON.check_for_input(MENU_MOUSE_POS):
                        self.simulation()
                    if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        running = False
            pygame.display.update()
            self._clock.tick(60)
    
    def simulation(self) -> None:
        pygame.display.set_caption("Random Walk - Simulation")
        font = pygame.font.SysFont("Arial", 20)

        world = self._world
        walkers = world._walkers
        nmb_walkers = len(walkers)

        colors = []
        for i in range(nmb_walkers):
            color = pygame.Color(0)
            color.hsva = (i * 360.0 / max(nmb_walkers, 1), 80, 100, 100)
            colors.append(color)

        min_x = max_x = 0.0
        min_y = max_y = 0.0
        paused = False
        running = True

        def update_bounds() -> None:
            nonlocal min_x, max_x, min_y, max_y
            for walker in walkers:
                x, y = walker.position
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key in (pygame.K_SPACE, pygame.K_p):
                        paused = not paused

            if not paused:
                world.step()
                update_bounds()

            screen_w, screen_h = self._screen.get_size()
            world_w = max_x - min_x
            world_h = max_y - min_y
            eps = 1e-6
            scale_w = (screen_w * 0.9) / max(world_w, eps)
            scale_h = (screen_h * 0.9) / max(world_h, eps)
            max_scale = 40.0
            scale = min(scale_w, scale_h, max_scale)
            offset_x = (screen_w - world_w * scale) / 2
            offset_y = (screen_h - world_h * scale) / 2

            def to_screen(x: float, y: float) -> tuple[int, int]:
                sx = offset_x + (x - min_x) * scale
                sy = offset_y + (max_y - y) * scale
                return int(sx), int(sy)

            self._screen.fill("black")

            for i, walker in enumerate(walkers):
                color = colors[i % len(colors)]
                path = walker.chemin
                if len(path) >= 2:
                    points = [to_screen(x, y) for x, y in path]
                    pygame.draw.lines(self._screen, color, False, points, 2)
                x, y = walker.position
                pygame.draw.circle(self._screen, color, to_screen(x, y), 4)

            if paused:
                pause_text = font.render("Pause (space/p to resume)", True, "yellow")
                self._screen.blit(pause_text, (10, 10))
            else:
                info = font.render("Space/P: pause, Esc: quit", True, "gray")
                self._screen.blit(info, (10, 10))

            pygame.display.flip()
            self._clock.tick(24)



