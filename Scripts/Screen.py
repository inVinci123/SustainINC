import pygame
from Scripts.ScreenElements import Text, TextButton, CenteredTextButton, InputField
import Scripts.AssetManager as am
import Scripts.AudioManager as audio

class Screen:
    """ Base class for Screens """
    def __init__(self, scale) -> None:
        self.scale = scale

        # dimensions (occupying the whole screen)
        self.unscaled_dimensions = (1280, 720)
        self.scaled_dimensions = (self.unscaled_dimensions[0]*self.scale, self.unscaled_dimensions[1]*self.scale)

        self.bg_colour = 0x09090909 # dark bg
        self.screen_elements = [] # what to draw on the screen
        return None
    
    def update_scale(self, scale) -> None:
        """ adjust the dimensions of the screen according to the new scale """
        self.scale = scale
        self.scaled_dimensions = (self.unscaled_dimensions[0]*self.scale, self.unscaled_dimensions[1]*self.scale)
        return None

    def draw(self, screen) -> None:
        """ draw the screen elements """
        for element in self.screen_elements:
            element.draw(screen)
        return None


class PauseScreen(Screen):
    """ Pause Screen with Audio options, Resume and Quit """
    def __init__(self, scale, close_pause_menu, quit_game) -> None:
        super().__init__(scale)
        self.close_pause_menu = close_pause_menu # function to close the pause menu
        self.quit = quit_game # function to quit the game
        self.screen_elements = [
            CenteredTextButton((490, 200), (300, 80), self.close_pause_menu, "Resume"),
            CenteredTextButton((490, 300), (300, 80), self.music_off, "Music: On") if audio.bgmusic else CenteredTextButton((490, 300), (300, 80), self.music_on, "Music: Off"),
            CenteredTextButton((490, 400), (300, 80), self.sfx_off, "SFX: On") if audio.sfx else CenteredTextButton((490, 400), (300, 80), self.sfx_on, "SFX: Off"),
            CenteredTextButton((490, 500), (300, 80), self.quit, "Quit")
        ]
        for element in self.screen_elements: # correct their positions before rendering them
            element.update_scale(scale)

        # bg translucent surface
        self.shadow_surf = pygame.Surface(self.scaled_dimensions)
        self.shadow_surf.set_alpha(200)
        self.shadow_surf.fill(self.bg_colour)

        # title of the screen
        self.pause_screen_text = am.normal_font[64].render("Pause Screen", True, 0xFAFAFAFA)
        self.pst_rect = self.pause_screen_text.get_rect()
        
        # (the details on the top right)
        # how long the game has been running for
        self.running_time_text = am.normal_font[16].render("Running time: ", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()

        # rate of change of global warming (aim to get this down to zero)
        self.carbon_contribution_text = am.normal_font[16].render("dTemp/dtime: ", True, 0xFAFAFAFA)
        self.cct_rect = self.carbon_contribution_text.get_rect()
        return None

    def music_off(self) -> None:
        """ Turn the background music off and edit the options accordingly """
        audio.bgmusic = False
        pygame.mixer.music.pause()
        self.screen_elements[1] = CenteredTextButton((490, 300), (300, 80), self.music_on, "Music: Off")
        self.update_scale(self.scale)
        return None

    def music_on(self) -> None:
        """ Turn the background music on and edit the options accordingly """
        audio.bgmusic = True
        pygame.mixer.music.unpause()
        self.screen_elements[1] = CenteredTextButton((490, 300), (300, 80), self.music_off, "Music: On")
        self.update_scale(self.scale)
        return None

    def sfx_off(self) -> None:
        """ Turn the Sound Effects off and edit the options accordingly """
        audio.sfx = False
        self.screen_elements[2] = CenteredTextButton((490, 400), (300, 80), self.sfx_on, "SFX: Off")
        self.update_scale(self.scale)
        return None

    def sfx_on(self) -> None:
        """ Turn the Sound Effects on and edit the options accordingly """
        audio.sfx = True
        self.screen_elements[2] = CenteredTextButton((490, 400), (300, 80), self.sfx_off, "SFX: On")
        self.update_scale(self.scale)
        return None

    def update_scale(self, scale) -> None:
        """ adjust everything to the new scale """
        super().update_scale(scale)
        self.pause_screen_text = am.normal_font[64].render("Pause Screen", True, 0xFAFAFAFA)
        self.pst_rect = self.pause_screen_text.get_rect()

        # how long the game has been running for
        self.running_time_text = am.normal_font[16].render("Running time: ", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()
        
        # rate of change of global warming (aim to get this down to zero)
        self.carbon_contribution_text = am.normal_font[16].render("dTemp/dtime: ", True, 0xFAFAFAFA)
        self.cct_rect = self.carbon_contribution_text.get_rect()

        # translucent background surface
        self.shadow_surf = pygame.Surface(self.scaled_dimensions)
        self.shadow_surf.set_alpha(200)
        self.shadow_surf.fill(self.bg_colour)

        for element in self.screen_elements: # update the screen elements
            element.update_scale(scale)
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        """ draw the pause menu screen """
        screen.blit(self.shadow_surf, (0, 0))
        screen.blit(self.pause_screen_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.pst_rect.size[0]/2, 100*self.scale))
        screen.blit(self.running_time_text, (self.scaled_dimensions[0] - self.rtt_rect.size[0] - 20 * self.scale, 20*self.scale))
        screen.blit(self.carbon_contribution_text, (self.scaled_dimensions[0] - self.cct_rect.size[0] - 20 * self.scale, 30*self.scale + self.rtt_rect.size[1]))
        return super().draw(screen)

    def update_ps_audio_values(self) -> None:
        """ re-render screen elements for the Music and SFX options according to their true values (disparity can be generated due to the start menu) """
        self.screen_elements = [
            CenteredTextButton((490, 200), (300, 80), self.close_pause_menu, "Resume"),
            CenteredTextButton((490, 300), (300, 80), self.music_off, "Music: On") if audio.bgmusic else CenteredTextButton((490, 300), (300, 80), self.music_on, "Music: Off"),
            CenteredTextButton((490, 400), (300, 80), self.sfx_off, "SFX: On") if audio.sfx else CenteredTextButton((490, 400), (300, 80), self.sfx_on, "SFX: Off"),
            CenteredTextButton((490, 500), (300, 80), self.quit, "Quit")
        ]
        for element in self.screen_elements: # correct their positions before continuing
            element.update_scale(self.scale)
        return None
    
    def update_data(self, running_time: float, delta_delta_temp: float) -> None:
        """ Update the running time and carbon contribution text """
        # how long the game has been running for
        self.running_time_text = am.normal_font[16].render(f"Running time: {running_time}s", True, 0xFAFAFAFA)
        self.rtt_rect = self.running_time_text.get_rect()
        # rate of change of global warming (aim to get this down to zero)
        self.carbon_contribution_text = am.normal_font[16].render(f"dTemp/dtime: {str(delta_delta_temp)[:6]}", True, 0xFAFAFAFA) # unrounded value
        self.cct_rect = self.carbon_contribution_text.get_rect()
        return None
    
    
class StartScreen(Screen):
    """ Start Screen, with a player name field, options, and quit game"""
    def __init__(self, scale, start_game, quit_game) -> None:
        super().__init__(scale)
        # start and quit functions
        self.start_game = start_game
        self.quit = quit_game

        # bg and the opaque-ish surface
        self.bg = am.gallet_city
        self.opq_surf = pygame.Surface((1280*scale, 720*scale))
        self.opq_surf.fill(0x121212)
        self.opq_surf.set_alpha(150)

        # options
        self.options: bool = False
        self.opt_elements = [
            CenteredTextButton((440, 250), (400, 100), self.music_off, "Music: On"),
            CenteredTextButton((440, 400), (400, 100), self.sfx_off, "SFX: On"),
            CenteredTextButton((440, 550), (400, 100), self.close_options, "<- Back")
        ]

        # title text
        self.sustain_text = am.normal_font[100].render("SUSTAIN INC", True, 0xFAFAFAFA)
        self.st_rect = self.sustain_text.get_rect()
        
        # start menu screen elements
        self.screen_elements = [
            InputField((440, 150), (400, 100)),
            CenteredTextButton((440, 300), (400, 100), lambda: self.start_game(self.screen_elements[0].name_str if self.screen_elements[0].name_str.strip() != "" else "Player"), "Start Game"),
            CenteredTextButton((440, 450), (400, 100), self.open_options, "Options"),
            CenteredTextButton((440, 600), (400, 100), self.quit, "Quit")
        ]
        self.update_scale(scale) # update everything to scale just in case
        return None
    
    def music_off(self) -> None:
        """ Turn the background music off and edit the options accordingly """
        audio.bgmusic = False
        pygame.mixer.music.pause()
        self.opt_elements[0] = CenteredTextButton((440, 250), (400, 100), self.music_on, "Music: Off")
        self.update_scale(self.scale)
        return None

    def music_on(self) -> None:
        """ Turn the background music on and edit the options accordingly """
        audio.bgmusic = True
        pygame.mixer.music.unpause()
        self.opt_elements[0] = CenteredTextButton((440, 250), (400, 100), self.music_off, "Music: On")
        self.update_scale(self.scale)
        return None

    def sfx_off(self) -> None:
        """ Turn the sound effects off and edit the options accordingly """
        audio.sfx = False
        self.opt_elements[1] = CenteredTextButton((440, 400), (400, 100), self.sfx_on, "SFX: Off")
        self.update_scale(self.scale)
        return None

    def sfx_on(self) -> None:
        """ Turn the sound effects on and edit the options accordingly """
        audio.sfx = True
        self.opt_elements[1] = CenteredTextButton((440, 400), (400, 100), self.sfx_off, "SFX: On")
        self.update_scale(self.scale)
        return None
    
    def open_options(self) -> None:
        """ switch to rendering the option buttons instead """
        self.sustain_text = am.normal_font[100].render("OPTIONS", True, 0xFAFAFAFA)
        self.st_rect = self.sustain_text.get_rect()
        self.options = True
        return None
    
    def close_options(self) -> None:
        """ switch to rendering the main start menu instead """
        self.sustain_text = am.normal_font[100].render("SUSTAIN INC", True, 0xFAFAFAFA)
        self.st_rect = self.sustain_text.get_rect()
        self.options = False
        return None

    def process_inputs(self, events: list[pygame.event.Event], keys_pressed=[]) -> None:
        """ update the player name field with the input data """
        self.screen_elements[0].update_text(events, keys_pressed)
        return None
    
    def draw(self, screen, deltatime=1) -> None:
        """ draw the bg, screen elements and title """
        # bg
        screen.blit(self.bg, (-1000*self.scale, -4200*self.scale))
        screen.blit(self.opq_surf, (0, 0))
        if self.options:
            # draw the options (sustain text should say "Options")
            screen.blit(self.sustain_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.st_rect.size[0]/2, 100*self.scale))
            for opt in self.opt_elements:
                opt.draw(screen)
        else:
            # draw the start menu elements
            screen.blit(self.sustain_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.st_rect.size[0]/2, 50*self.scale))
            for element in self.screen_elements:
                if type(element) == InputField:
                    element.draw(screen, deltatime)
                else:
                    element.draw(screen)
        return None

    def update_scale(self, scale) -> None:
        """ adjust everything according to the new scale """
        super().update_scale(scale)
        # update the bg and bg surface
        self.bg = pygame.transform.scale(am.gallet_city, (5120*self.scale, 5120*self.scale))
        self.opq_surf = pygame.Surface((1280*scale, 720*scale))
        self.opq_surf.fill(0x121212)
        self.opq_surf.set_alpha(150)

        # title text
        self.sustain_text = am.normal_font[100].render("SUSTAIN INC", True, 0xFAFAFAFA) if not self.options else am.normal_font[100].render("OPTIONS", True, 0xFAFAFAFA)
        self.st_rect = self.sustain_text.get_rect()

        # screen elements and options
        for element in self.screen_elements+self.opt_elements:
            element.update_scale(scale)
        return None


class EndScreen(Screen):
    """ End Game Screen showing an end message and the option to quit """
    def __init__(self, scale, quit_game, score=0) -> None:
        super().__init__(scale)
        # bg opaque-ish surface 
        self.opq_surf = pygame.Surface((1280*scale, 720*scale))
        self.opq_surf.fill(0x121212)
        self.opq_surf.set_alpha(200)
        
        self.score = score
        self.quit_game = quit_game # quit game function

        if score == 0: # if the player lost the game
            self.game_outcome_text = am.normal_font[100].render("You lost :c", True, 0xFAFAFAFA)
            self.go_rect = self.game_outcome_text.get_rect()
            self.consolation_text = am.normal_font[50].render("But you don't have to in real life!", True, 0xFAFAFAFA)
            self.ct_rect = self.consolation_text.get_rect()
        else: # if the player won the game
            self.game_outcome_text = am.normal_font[100].render(f"You did it", True, 0xFAFAFAFA)
            self.go_rect = self.game_outcome_text.get_rect()
            self.score_text = am.normal_font[100].render(f"Score:{int(score)}", True, 0xFAFAFAFA)
            self.score_rect = self.score_text.get_rect()
            self.consolation_text = am.normal_font[50].render("Let's do it in real life too!", True, 0xFAFAFAFA)
            self.ct_rect = self.consolation_text.get_rect()        

        # quit button in the screen elements
        self.screen_elements = [
            CenteredTextButton((490, 500), (300, 80), self.quit_game, "Quit")
        ]
        for element in self.screen_elements:
            element.update_scale(scale)

        return None

    def update_data(*args) -> None: # need this to pass it for a pause screen (the end screen is actually just rendered as a different type of pause screen)
        return None
    
    def update_ps_audio_values(*args) -> None: # also need this to pass it for a pause screen
        return None
    
    def draw(self, screen) -> None:
        """ draw the end screen """
        # draw the opaque-ish surface
        screen.blit(self.opq_surf, (0, 0))
        if self.score == 0: # if end game is a losing scenario, don't show the score and draw things differently
            screen.blit(self.game_outcome_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.go_rect.size[0]/2, 100*self.scale))
            screen.blit(self.consolation_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.ct_rect.size[0]/2, 250*self.scale))
        else: # else show everything and draw things normally
            screen.blit(self.game_outcome_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.go_rect.size[0]/2, 100*self.scale))
            screen.blit(self.score_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.score_rect.size[0]/2, 220*self.scale))
            screen.blit(self.consolation_text, ((self.unscaled_dimensions[0]/2)*self.scale - self.ct_rect.size[0]/2, 350*self.scale))
        return super().draw(screen)

    def update_scale(self, scale) -> None:
        """ adjust everything according to the new scale """
        super().update_scale(scale)
        # update the opaque-ish surface
        self.opq_surf = pygame.Surface((1280*scale, 720*scale))
        self.opq_surf.fill(0x121212)
        self.opq_surf.set_alpha(200)

        # title texts
        if self.score == 0: # if the player lost
            self.game_outcome_text = am.normal_font[64].render("You lost :c", True, 0xFAFAFAFA)
            self.go_rect = self.game_outcome_text.get_rect()
            self.consolation_text = am.normal_font[50].render("But you don't have to in real life!", True, 0xFAFAFAFA)
            self.ct_rect = self.consolation_text.get_rect()
        else: # if the player won
            self.game_outcome_text = am.normal_font[100].render(f"You did it!", True, 0xFAFAFAFA)
            self.go_rect = self.game_outcome_text.get_rect()
            self.score_text = am.normal_font[100].render(f"Score:{int(self.score)}", True, 0xFAFAFAFA)
            self.score_rect = self.score_text.get_rect()
            self.consolation_text = am.normal_font[50].render("Let's do it real life too!", True, 0xFAFAFAFA)
            self.ct_rect = self.consolation_text.get_rect()   

        # screen elements
        for element in self.screen_elements:
            element.update_scale(scale)
        return None