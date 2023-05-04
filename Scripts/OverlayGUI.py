import pygame
from decimal import Decimal

from Scripts.ScreenElements import InteractionPrompt, Text
import Scripts.AssetManager as am

class OverlayGUI:
    prompt = InteractionPrompt()
    show_prompt: bool = True
    resources_bg = pygame.Surface((230, 30))
    resources_bg.fill(0x121212)
    resources_bg.set_alpha(180)
    try:
        resources_text = Text("$1234567890", (20, 11), (200, 20), am.normal_font[18], 0xFAFAFAFA)
    except AttributeError:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if self.show_prompt:
            self.prompt.draw(screen)
        
        screen.blit(self.resources_bg, (10, 10))
        try:
            self.resources_text.draw(screen)
        except AttributeError:
            pass
        self.show_prompt = False
        return None

    def update_resources(self, val: float = 0) -> None:
        self.resources_text = Text(f"${int(val) if val <= 1e6 else '%.2E' % Decimal(int(val))}", (20, 16), (200, 20), am.normal_font[18], 0xFAFAFAFA)
        return None
    
    def update_scale(self, scale) -> None:
        self.prompt.update_scale(scale)
        self.resources_bg = pygame.Surface((230*scale, 30*scale))
        self.resources_bg.set_alpha(180)
        self.resources_bg.fill(0x121212)
        return None

gui: OverlayGUI