import pygame
from Scripts.ScreenElements import Text, TextButton, CenteredTextButton
import Scripts.AssetManager as am
import Scripts.AudioManager as audio

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
            element.draw(screen)
        return None

class PauseScreen(Screen):
    def __init__(self, scale, close_pause_menu, quit_game) -> None:
        super().__init__(scale)
        self.close_pause_menu = close_pause_menu
        self.quit = quit_game
        self.screen_elements = [ # add screen elements fsalkjdl resume button, save and quit (a list for the butons only)
            CenteredTextButton((540, 300), (200, 50), self.close_pause_menu, "Resume"),
            CenteredTextButton((540, 400), (200, 50), self.music_off, "Music: On") if audio.bgmusic else CenteredTextButton((540, 400), (200, 50), self.music_on, "Music: Off"),
            CenteredTextButton((540, 500), (200, 50), self.sfx_off, "SFX: On") if audio.sfx else CenteredTextButton((540, 500), (200, 50), self.sfx_on, "SFX: Off"),
            CenteredTextButton((540, 600), (200, 50), self.quit, "Quit")
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

    def music_off(self) -> None:
        audio.bgmusic = False
        pygame.mixer.music.pause()
        self.screen_elements[1] = CenteredTextButton((540, 400), (200, 50), self.music_on, "Music: Off")
        self.update_scale(self.scale)
        return None

    def music_on(self) -> None:
        audio.bgmusic = True
        pygame.mixer.music.unpause()
        self.screen_elements[1] = CenteredTextButton((540, 400), (200, 50), self.music_off, "Music: On")
        self.update_scale(self.scale)
        return None

    def sfx_off(self) -> None:
        audio.sfx = False
        self.screen_elements[2] = CenteredTextButton((540, 500), (200, 50), self.sfx_on, "SFX: Off")
        self.update_scale(self.scale)
        return None

    def sfx_on(self) -> None:
        audio.sfx = True
        self.screen_elements[2] = CenteredTextButton((540, 500), (200, 50), self.sfx_off, "SFX: On")
        self.update_scale(self.scale)
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

    def update_ps_audio_values(self) -> None:
        self.screen_elements = [ # add screen elements fsalkjdl resume button, save and quit (a list for the butons only)
            CenteredTextButton((540, 300), (200, 50), self.close_pause_menu, "Resume"),
            CenteredTextButton((540, 400), (200, 50), self.music_off, "Music: On") if audio.bgmusic else CenteredTextButton((540, 400), (200, 50), self.music_on, "Music: Off"),
            CenteredTextButton((540, 500), (200, 50), self.sfx_off, "SFX: On") if audio.sfx else CenteredTextButton((540, 500), (200, 50), self.sfx_on, "SFX: Off"),
            CenteredTextButton((540, 600), (200, 50), self.quit, "Quit")
        ]
        for element in self.screen_elements: # correct their positions before continuing
            element.update_scale(self.scale)
        return None
    
    def update_data(self, running_time: float, delta_delta_temp: float) -> None:

        self.running_time_text = am.normal_font[16].render(f"Running time: {running_time}s", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()

        self.carbon_contribution_text = am.normal_font[16].render(f"Delta Delta temp: {str(delta_delta_temp)[:6]}", True, 0xFAFAFAFA) # unrounded value
        self.cct_rect = self.carbon_contribution_text.get_rect()
        return None
    
class StartScreen(Screen):
    def __init__(self, scale, start_game, quit_game) -> None:
        super().__init__(scale)
        self.start_game = start_game
        self.quit = quit_game

        self.bg = am.gallet_city
        self.opq_surf = pygame.Surface((1280*scale, 720*scale))
        self.opq_surf.fill(0x121212)
        self.opq_surf.set_alpha(150)

        self.options: bool = False

        self.opt_elements = [
            CenteredTextButton((540, 300), (200, 50), self.music_off, "Music: On"),
            CenteredTextButton((540, 400), (200, 50), self.sfx_off, "SFX: On"),
            CenteredTextButton((540, 500), (200, 50), self.close_options, "<- Back")
        ]

        self.sustain_text = am.normal_font[64].render("SUSTAIN INC", True, 0xFAFAFAFA)
        self.st_rect = self.sustain_text.get_rect()
        
        self.screen_elements = [ # add screen elements fsalkjdl resume button, save and quit (a list for the butons only)
            CenteredTextButton((540, 300), (200, 50), self.start_game, "Start Game"),
            CenteredTextButton((540, 400), (200, 50), self.open_options, "Options"),
            CenteredTextButton((540, 500), (200, 50), self.quit, "Quit")
        ]
        self.update_scale(scale)
    
    def music_off(self) -> None:
        audio.bgmusic = False
        pygame.mixer.music.pause()
        self.opt_elements[0] = CenteredTextButton((540, 300), (200, 50), self.music_on, "Music: Off")
        self.update_scale(self.scale)
        return None

    def music_on(self) -> None:
        audio.bgmusic = True
        pygame.mixer.music.unpause()
        self.opt_elements[0] = CenteredTextButton((540, 300), (200, 50), self.music_off, "Music: On")
        self.update_scale(self.scale)
        return None

    def sfx_off(self) -> None:
        audio.sfx = False
        self.opt_elements[1] = CenteredTextButton((540, 400), (200, 50), self.sfx_on, "SFX: Off")
        self.update_scale(self.scale)
        return None

    def sfx_on(self) -> None:
        audio.sfx = True
        self.opt_elements[1] = CenteredTextButton((540, 400), (200, 50), self.sfx_off, "SFX: On")
        self.update_scale(self.scale)
        return None
    
    def open_options(self) -> None:
        print("trynna open options...")
        self.options = True
        return None
    
    def close_options(self) -> None:
        print("trynna close options...")
        self.options = False
        return None

    def process_inputs(self, keys_pressed) -> None:

        return None
    
    def draw(self, screen) -> None:
        screen.blit(self.bg, (-1000*self.scale, -4200*self.scale))
        screen.blit(self.opq_surf, (0, 0))
        screen.blit(self.sustain_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.st_rect.size[0]/2, 100*self.scale))
        if self.options:
            for opt in self.opt_elements:
                opt.draw(screen)
        else:
            for element in self.screen_elements:
                element.draw(screen)

    def update_scale(self, scale) -> None:
        super().update_scale(scale)
        self.opq_surf = pygame.Surface((1280*scale, 720*scale))
        self.opq_surf.fill(0x121212)
        self.opq_surf.set_alpha(150)

        self.sustain_text = am.normal_font[64].render("SUSTAIN INC", True, 0xFAFAFAFA)
        self.st_rect = self.sustain_text.get_rect()

        self.bg = pygame.transform.scale(am.gallet_city, (5120*self.scale, 5120*self.scale))

        for element in self.screen_elements+self.opt_elements: # correct their positions before continuing
            element.update_scale(scale)
        return None