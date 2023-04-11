import pygame

class Character:
    def __init__(self, idle_anim: list[pygame.Surface]) -> None:
        self.idle = idle_anim
        self.anim_index = 0
        return None

    
    def draw(self, screen: pygame.Surface) -> None:
        return None
