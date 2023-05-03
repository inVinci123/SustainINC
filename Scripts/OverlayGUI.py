import pygame
from Scripts.ScreenElements import InteractionPrompt

class OverlayGUI:
    prompt = InteractionPrompt()
    show_prompt: bool = True
    def draw(self, screen) -> None:
        if self.show_prompt:
            self.prompt.draw(screen)
        self.show_prompt = False
    
    def update_scale(self, scale) -> None:
        self.prompt.update_scale(scale)

gui: OverlayGUI