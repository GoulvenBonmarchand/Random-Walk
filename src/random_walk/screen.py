import pygame
from button import Button

class Screen:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))

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
                text=font.render("Start", True, "white"),
                pos=(640, 300),
                font=font,
                screen=self._screen,
            )
            SETTINGS_BUTTON = Button(
                text=font.render("Settings", True, "white"),
                pos=(640, 400),
                font=font,
                screen=self._screen,
            )
            QUIT_BUTTON = Button(
                text=font.render("Quit", True, "white"),
                pos=(640, 500),
                font=font,
                screen=self._screen,
            )
            
            self._screen.blit(MENU_TEXT, MENU_RECT)
            
            for button in [START_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if START_BUTTON.check_for_input(MENU_MOUSE_POS):
                        self.start()
                    if SETTINGS_BUTTON.check_for_input(MENU_MOUSE_POS):
                        self.setting()
                    if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        running = False



