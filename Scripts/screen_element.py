import pygame

class ScreenElement:
    def __init__(self, pos: tuple, size: tuple) -> None:
        self.rect = pygame.Rect(pos, size)
        pass


    def draw(self, screen: pygame.Surface, check: bool = False, mouse: tuple[int, int] = (0, 0), r_click: bool = False) -> None:
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        return None