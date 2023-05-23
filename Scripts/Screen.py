import pygame
from Scripts.ScreenElements import Text, TextButton, CenteredTextButton
import Scripts.AssetManager as am

class Screen:
    def __init__(self, scale) -> None:
        self.scale = scale
        self.unscaled_dimensions = (1280, 720)
        self.scaled_dimensions = (self.unscaled_dimensions[0]*self.scale, self.unscaled_dimensions[1]*self.scale)
        self.bg_colour = 0x29292929
        self.screen_elements = []
        return None
    
    def update_scale(self, scale) -> None:
        self.scale = scale
        self.scaled_dimensions = (self.unscaled_dimensions[0]*self.scale, self.unscaled_dimensions[1]*self.scale)
        return None

    def draw(self, screen) -> None:
        for element in self.screen_elements:
            element.draw(screen) # ...
        return None

class PauseScreen(Screen):
    def __init__(self, scale, close_pause_menu) -> None:
        super().__init__(scale)
        self.close_pause_menu = close_pause_menu
        self.screen_elements = [ # add screen elements fsalkjdl resume button, save and quit (a list for the butons only)
            CenteredTextButton((540, 300), (200, 50), self.close_pause_menu, "Resume")
        ]
        for element in self.screen_elements: # correct their positions before continuing
            element.update_scale(scale)
        # bg translucent surface
        self.shadow_surf = pygame.Surface(self.scaled_dimensions)
        self.shadow_surf.set_alpha(200)
        self.shadow_surf.fill(self.bg_colour)

        # title of the screen
        self.pause_screen_text = am.normal_font[50].render("Pause Screen", True, 0xFAFAFAFA)
        self.pst_rect = self.pause_screen_text.get_rect()
        
        # Details on the top right
        # how long the game has been running for
        self.running_time_text = am.normal_font[16].render("Running time: ", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()

        # rate of change of global warming (aim to get this down to zero)
        self.carbon_contribution_text = am.normal_font[16].render("Delta Delta temp: ", True, 0xFAFAFAFA)
        self.cct_rect = self.carbon_contribution_text.get_rect()
        return None
    
    def update_scale(self, scale) -> None:
        super().update_scale(scale)
        self.pause_screen_text = am.normal_font[50].render("Pause Screen", True, 0xFAFAFAFA)
        self.pst_rect = self.pause_screen_text.get_rect()

        # how long the game has been running for
        self.running_time_text = am.normal_font[16].render("Running time: ", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()
        # rate of change of global warming (aim to get this down to zero)
        self.carbon_contribution_text = am.normal_font[16].render("Delta Delta temp: ", True, 0xFAFAFAFA)
        self.cct_rect = self.carbon_contribution_text.get_rect()

        self.shadow_surf = pygame.Surface(self.scaled_dimensions)
        self.shadow_surf.set_alpha(100)
        self.shadow_surf.fill(self.bg_colour)
        for element in self.screen_elements: # correct their positions before continuing
            element.update_scale(scale)
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.shadow_surf, (0, 0))
        screen.blit(self.pause_screen_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.pst_rect.size[0]/2, 100*self.scale))
        screen.blit(self.running_time_text, (self.scaled_dimensions[0] - self.rtt_rect.size[0] - 20 * self.scale, 20*self.scale))
        screen.blit(self.carbon_contribution_text, (self.scaled_dimensions[0] - self.cct_rect.size[0] - 20 * self.scale, 30*self.scale + self.rtt_rect.size[1]))
        return super().draw(screen)
    
    def update_data(self, running_time: float, delta_delta_temp: float) -> None:
        self.running_time_text = am.normal_font[16].render(f"Running time: {running_time}s", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()

        self.carbon_contribution_text = am.normal_font[16].render(f"Delta Delta temp: {str(delta_delta_temp)[:6]}", True, 0xFAFAFAFA) # unrounded value
        self.cct_rect = self.carbon_contribution_text.get_rect()
        return None