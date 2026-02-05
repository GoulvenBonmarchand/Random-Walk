import pygame

class Screen:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))

    def main_menue(self) -> None:
        pygame.display.set_caption("Random Walk")
        font = pygame.font.SysFont("Arial", 48)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self._screen.fill("black")

            MENUE_MOUSE_POS = pygame.mouse.get_pos()

            MENUE_TEXT = font.render("Random Walk", True, "white")

            MENUE_RECT = MENUE_TEXT.get_rect(center=(640, 100))
            
            pygame.display.update()

