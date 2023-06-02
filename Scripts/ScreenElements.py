import pygame
import math

import Scripts.AssetManager as am
import Scripts.AudioManager as audio

class Button:
    """ Base class for a simple coloured button """
    def __init__(self, pos, size, on_click, inactive_colour = 0x6A6A6A, normal_colour = 0xFBFBFB, hover_colour = 0xC3C3C3, click_colour = 0x999999) -> None:
        # position & size stuff
        self.unscaled_pos = pos
        self.unscaled_size = size
        self.scale = 1
        self.scaled_pos = self.unscaled_pos
        self.scaled_size = self.unscaled_size
        self.rect = pygame.Rect(self.scaled_pos, self.scaled_size)
        self.game_screen_dimensions = (0, 0)

        self.on_click = on_click # function
        
        # diff colours
        self.inactive_colour = inactive_colour
        self.normal_colour = normal_colour
        self.hover_colour = hover_colour
        self.click_colour = click_colour

        # hover/click stuff
        self.hover, self.click, self.click_complete = False, False, False
        return None
    
    def check(self) -> None:
        """ check hover or click """
        # fetch the mouse pos and right_click info
        mouse = pygame.mouse.get_pos()
        r_click = pygame.mouse.get_pressed()[0]

        # evaluate the actual mouse position (mouse position based on the game screen instead of the application window)
        w_s = pygame.display.get_window_size()
        relative_origin = ((w_s[0]-self.game_screen_dimensions[0])/2, (w_s[1]-self.game_screen_dimensions[1])/2)
        mouse = (mouse[0]-relative_origin[0], mouse[1]-relative_origin[1])
        
        self.hover = self.rect.collidepoint(mouse) # check for hover
        if not self.click: # if the mouse hasn't clicked yet
            self.click = self.hover and r_click # set click to true if it is hovering above the rect and r_clicking
        else: # if the mouse already clicked last frame
            if not r_click: # if it unclicked
                if self.hover: # if it is still on the rect, the click is complete
                    self.click_complete = True
                    self.click = False
                else: # if it is no longer on the rect, the click was incomplete and the action has finished
                    self.click = False
        return None
    
    def update_scale(self, scale) -> None:
        """ adjust everything to the new scale """
        self.scale = scale
        self.scaled_pos = scale*self.unscaled_pos[0], scale*self.unscaled_pos[1]
        self.scaled_size = scale*self.unscaled_size[0], scale*self.unscaled_size[1]
        self.rect = pygame.Rect(self.scaled_pos, self.scaled_size)
        return None
    
    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        """ draw the button as a rect """
        if check: # if checking is allowed
            self.check() # check for click/hover
            colour = self.click_colour if self.click else (self.hover_colour if self.hover else self.normal_colour) # set the appropriate colour
            if self.click_complete:
                audio.play_sound("click")
                self.on_click()
                self.click_complete = False
        else: # else render it in active
            self.click = False
            colour = self.inactive_colour

        self.game_screen_dimensions = screen.get_size() # update the game screen dimensions for the mouse checks
        pygame.draw.rect(screen, colour, self.rect)
        return None

    
class TextButton(Button):
    """ Simple Text Button based on the Button class """
    def __init__(self, pos, size, on_click, text: str = "Hello World!", inactive_colour=6974058, normal_colour=16514043, hover_colour=12829635, click_colour=10066329, text_colour=1710618) -> None:
        super().__init__(pos, size, on_click, inactive_colour, normal_colour, hover_colour, click_colour)
        self.str = text # text to render on the button
        self.text_colour = text_colour
        self.inactive = False
        
        try:
            # try creating the text object (won't work if the assets haven't been loaded in yet)
            self.text = Text(text, (self.scaled_pos[0]+self.scale*10, self.scaled_pos[1]+self.scale*10), (self.scaled_size[0]-self.scale*20, self.scaled_size[1]-self.scale*20), am.normal_font[18], self.text_colour)
        except AttributeError:
            pass
        return None
    
    def update_scale(self, scale) -> None:
        """ adjust everything according to the new scale """
        super().update_scale(scale)
        self.text = Text(self.str, (self.scaled_pos[0]+self.scale*10, self.scaled_pos[1]+self.scale*10), (self.scaled_size[0]-self.scale*20, self.scaled_size[1]-self.scale*20), am.normal_font[18], self.text_colour)
        return None
    
    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        """ draw and check for mouse clicks """
        super().draw(screen, check and not self.inactive)
        self.text.draw(screen)
        return None


class CenteredTextButton(Button):
    """ Centered Text Button (uses pygame.font instead of Text) """
    def __init__(self, pos, size, on_click, text: str = "Hello World!", scale = 1, inactive_colour=6974058, normal_colour=16514043, hover_colour=12829635, click_colour=10066329, text_colour=1710618) -> None:
        super().__init__(pos, size, on_click, inactive_colour, normal_colour, hover_colour, click_colour)
        self.str = text
        self.scale = scale
        self.text_colour = text_colour
        self.inactive = False
        try:
            self.text_surf = am.normal_font[24].render(self.str, True, self.text_colour)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_size[0] - self.text_rect.width/2, self.scaled_size[1] - self.text_rect.height/2) # position the rect in the centre of the button
        except AttributeError:
            pass
        return None
    
    def update_scale(self, scale) -> None:
        """ adjust everything according to the new scale  """
        super().update_scale(scale)
        
        # update the text stuff
        self.text_surf = am.normal_font[24].render(self.str, True, self.text_colour)
        self.text_rect = self.text_surf.get_rect()
        self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2 - self.text_rect.height/2)
        return None
    
    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        """ draw the button + text and check for clicks/hover"""
        super().draw(screen, check and not self.inactive)
        screen.blit(self.text_surf, self.text_pos)
        return None


class Text:
    """ Class for multi-line text (mainly used in Interaction/Option Prompts and Notifications/Objectives) """
    def __init__(self, text: str, scaled_pos: tuple[float, float], text_box_size: tuple[float, float], font: pygame.font.Font, colour = 0x1A1A1A) -> None:
        self.text = text # in the form of str
        # dimensions:
        self.scale = 1
        self.pos = scaled_pos
        self.size = text_box_size

        self.font = font
        self.colour = colour

        self.game_screen_size = (1280, 720)
        self.text_surf = self.generate_text_surf()
        return None
    
    def generate_text_surf(self) -> pygame.Surface:
        """ create a surface with the text split up with dashes """
        avg_length, height = self.font.render("a", True, self.colour).get_rect().size
        cpl = int((self.size[0]-5*self.scale)/avg_length) # estimate for how long each line will be in terms of characters
        split_string = self.text.split("\n") # new lines should still be respected
        lines = []
        a = pygame.Surface(self.size, pygame.SRCALPHA) # transparent background surface (to blit the text on)
        for s in split_string:
            n = math.ceil(len(s)/cpl)

            for i in range(n):
                line = s[i*cpl:(i+1)*cpl] # the relevant characters in the line
                if line[-1] in " ,-.!/": # end of the line is empty
                    b = self.font.render(s[i*cpl:(i+1)*cpl].strip(), True, self.colour)
                else:
                    try:
                        if s[(i+1)*cpl] in ' ,-.!/': # if the beginning of the next line isn't continuing this word
                            b = self.font.render(s[i*cpl:(i+1)*cpl].strip(), True, self.colour)
                        else:
                            b = self.font.render(s[i*cpl:(i+1)*cpl].strip() + "-", True, self.colour) # a dash to signify next line is a continuation of this word
                    except IndexError: # Index out of range, i.e. this is the last line
                        b = self.font.render(s[i*cpl:(i+1)*cpl].strip(), True, self.colour)                        
                lines.append(b)
        
        for i, b in enumerate(lines): # add all the lines to the transparent surface a and return that as the text surface
            a.blit(b, (0, i*height))
        return a

    def draw(self, game_screen: pygame.Surface) -> None:
        """ draw the Text on the screen """
        if game_screen.get_size() != self.game_screen_size:
            # Quick optimisation to only update the text surface when the game screen has changed
            self.game_screen_size = game_screen.get_size()
            self.scale = min(self.game_screen_size[0]/1280, self.game_screen_size[1]/720)
            self.text_surf = self.generate_text_surf()
        game_screen.blit(self.text_surf, self.pos) # draw the surface
        return None


class InteractionPrompt:
    """ The on screen prompt for common interactions between the player and NPCS/Building (non option) """
    def __init__(self, text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.") -> None:
        # dimensions
        self.scale: float = 1
        self.unscaled_pos = (140, 500)
        self.unscaled_size = (1000, 140)
        self.scaled_pos = self.unscaled_pos
        self.scaled_size = self.unscaled_size

        # bg transparent surface
        self.transparent_surf = pygame.Surface(self.scaled_size)
        self.transparent_surf.fill(0X2A2A2A)
        self.transparent_surf.set_alpha(100)
        
        # text for the prompt
        self.text = text
        text_box_pos = ((self.unscaled_pos[0]+10)*self.scale, (self.unscaled_pos[1]+10)*self.scale)
        text_box_size = ((self.unscaled_size[0]-20)*self.scale, (self.unscaled_size[1]-20)*self.scale)
        try:
            self.text_box: Text = Text(self.text, text_box_pos, text_box_size, am.normal_font[18])
        except AttributeError:
            pass
        return None
    
    def update_scale(self, scale: float) -> None:
        """ adjust everything according to the new scale """
        # dimensions
        self.scale = scale
        self.scaled_pos = (self.unscaled_pos[0]*scale, self.unscaled_pos[1]*scale)
        self.scaled_size = (self.unscaled_size[0]*scale, self.unscaled_size[1]*scale)

        # callibrated textbox pos and scale
        text_box_pos = ((self.unscaled_pos[0]+10)*scale, (self.unscaled_pos[1]+10)*scale)
        text_box_size = ((self.unscaled_size[0]-20)*scale, (self.unscaled_size[1]-20)*scale)

        # multi-line text surf
        self.text_box = Text(self.text, text_box_pos, text_box_size, am.normal_font[18], 0xFAFAFAFF)
        
        # bg stuff
        self.transparent_surf = pygame.Surface(self.scaled_size)
        self.transparent_surf.fill(0x000000)
        self.transparent_surf.set_alpha(180)
        return None
    
    def draw(self, screen, check=True) -> None:
        """ draw the interaction prompt """
        screen.blit(self.transparent_surf, self.scaled_pos)
        self.text_box.draw(screen)
        return None
    

class Options:
    """ Text Buttons organised in a structure as Options for an Options Prompt """
    def __init__(self, opts: list[tuple[str, object]] = []) -> None:
        if len(opts) == 0:
            self.options = [ # pre gen options
                TextButton((140, 650), (300, 38), lambda: print("Option 1 clicked!"), "Option 1", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1),
                TextButton((490, 650), (300, 38), lambda: print("Option 2 clicked!"), "Option 2", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1),
                TextButton((840, 650), (300, 38), lambda: print("Option 3 clicked!"), "Option 3", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1)
            ]
        elif len(opts) <= 3: # create the options if the list of tuple pairs is provided
            self.options: list[Button] = []
            for i, o in enumerate(opts):
                self.options.append(TextButton((140 + i*350, 650), (300, 38), o[1], o[0], 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1))
        return None
    
    def update_scale(self, scale) -> None:
        """ adjust the options to the new scale """
        for o in self.options:
            o.update_scale(scale)
        return None
    
    def draw(self, screen, check=True) -> None:
        """ draw the options at their positions """
        for o in self.options:
            o.draw(screen, check)
        return None


class OptionsPrompt(InteractionPrompt):
    """ Type of InteractionPrompt with Options """
    def __init__(self, text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", options: Options = Options()) -> None:
        super().__init__(text)
        self.opts = options # add some options
        return None
    
    def update_scale(self, scale: float) -> None:
        """ adjust the sizes of everything, including the options """
        super().update_scale(scale)
        self.opts.update_scale(scale)
        return None
    
    def draw(self, screen, check=True) -> None:
        """ draw everything, including the options """
        super().draw(screen)
        self.opts.draw(screen, check)
        return None
    

class InputField:
    """ Screen Element to input data """
    def __init__(self, unscaled_pos, unscaled_size, scale=1, chr_limit=11) -> None:
        # dimensions and scale
        self.scale = scale
        self.game_screen_dimensions = (1280*scale, 720*scale)
        self.unscaled_pos = unscaled_pos
        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale
        self.unscaled_size = unscaled_size
        self.scaled_size = self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale

        # underline rect
        self.underline_pos = self.scaled_pos[0], self.scaled_pos[1]+0.95*self.scaled_size[1]
        self.underline_size = self.scaled_size[0], 0.05*self.scaled_size[1]

        # input limits
        self.character_limit = chr_limit
        self.allowed_characters="ACBDEFGHIJKLMNOPQRSTUVWXYZacbdefghijklmnopqrstuvwxyz_.,?<>\"':;][]{ }\\|-+=`~!@#$%^&*()"

        # active stuff
        self.is_active: bool = False
        self.hover: bool = False
        self.click: bool = False

        # str prompt
        self.str = "Name: "
        self.name_str = ""

        # timer for how long the under line will stay red
        self.timer = 0.5

        self.col: int = 0xFAFAFA # default colour (editing, no errors)
        self.underline_rect = pygame.Rect(self.underline_pos, self.underline_size)
        
        self.running_time: float = 0
        
        # cursor stuff
        self.cursor_blink_rate: float = 0.45
        self.cursor_cool_time: float = self.cursor_blink_rate
        
        try: # try generating the text surf and stuff (won't work if asset manager hasn't been loaded yet)
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        except AttributeError:
            pass
        return None
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.scaled_pos, self.scaled_size)
    
    def check(self) -> None:
        """ check for hover/click (method described in class Button in ScreenElements.py) """
        mouse = pygame.mouse.get_pos()
        r_click = pygame.mouse.get_pressed()[0]

        # evaluate the actual mouse position would be if black bars are present
        w_s = pygame.display.get_window_size()
        relative_origin = ((w_s[0]-self.game_screen_dimensions[0])/2, (w_s[1]-self.game_screen_dimensions[1])/2)
        mouse = (mouse[0]-relative_origin[0], mouse[1]-relative_origin[1])
        
        self.hover = self.get_rect().collidepoint(mouse)
        if not self.click:
            self.click = self.hover and r_click
        else:
            if not r_click:
                if self.hover:
                    self.click_complete = True
                    self.click = False
                    self.is_active = True # make the field active if clicked on
                else:
                    self.click = False
        
        if r_click and not self.hover:
            self.is_active = False
        return None
    
    def draw(self, screen: pygame.Surface, deltatime=0.1) -> None:
        """ draw the text and underline with appropriate characters and colour """
        self.running_time += deltatime
        self.cursor_cool_time -= deltatime
        if self.cursor_cool_time <= -self.cursor_blink_rate: self.cursor_cool_time = self.cursor_blink_rate # half the time the cursor will be on and off the other half
        
        self.check() # check for hover and click
        if self.is_active:
            if self.col == 0xFF0000 and self.timer > 0: # if the underline is red (warning), subtract the deltatime from the timer
                self.timer -= deltatime
            else:
                self.col = 0x690000 if len(self.name_str) > self.character_limit else 0xFAFAFA # else normal if their is enough space for more characters and red if there's no space for any more characters. 
        else: # if not active, update the colour based on hover or click parameters
            if self.click:
                self.col = 0xFAFAFA
            elif self.hover:
                self.col = 0x9A9A9A
            else:
                self.col = 0x696969
        
        # draw the underline
        pygame.draw.rect(screen, self.col, self.underline_rect)

        if self.is_active and self.cursor_cool_time > 0: # render the cursor half the time (if it is active)
            self.text_surf = am.normal_font[30].render(self.str+self.name_str+"|", True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/20, self.scaled_pos[1] + self.scaled_size[1]/2)
        else: # the other half, don't render the cursor
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/20, self.scaled_pos[1] + self.scaled_size[1]/2)

        screen.blit(self.text_surf, self.text_pos)
        return None
    
    def add_letter(self, letter) -> None:
        """ add a letter to the collection if possible, else make the underline red """
        if len(self.name_str) > self.character_limit: # make the underline red if there is no more space
            self.col = 0xFF0000
            self.timer = 0.5
        else: # else add the letter
            self.name_str += letter
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        return None
    
    def backspace(self, clear: bool=False) -> None:
        """ remove the last letter is possible, else make the underline red """
        if len(self.name_str) == 0: # make the underline red if there is no letters to remove
            self.col = 0xFF0000
            self.timer = 0.5
        else: # else remove the last letter (or clear it)
            self.name_str = "" if clear else self.name_str[:-1]
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        return None
    
    def update_text(self, events: list[pygame.event.Event], keys_pressed=[]) -> None:
        """ process the unicode inputs and see if any letter is to be added/removed """
        if not self.is_active: # don't update anything if the input field isn't active
            return None
        try:
            ctrl = keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL] # check whether ctrl is pressed
        except IndexError:
            ctrl = False
        for e in events:
            try:
                if e.type == pygame.KEYDOWN:
                    if e.unicode in self.allowed_characters: # add the letters to the string if possible
                        self.add_letter(e.unicode)
                    elif e.key == pygame.K_BACKSPACE:
                        self.backspace(ctrl) # remove the latest letter of the string if possible
            except AttributeError:
                pass
        return None
    
    def update_scale(self, scale) -> None:
        """ adjust everything according to the new scale """
        # update the dimensions
        self.scale = scale
        self.game_screen_dimensions = (1280*scale, 720*scale)
        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale
        self.scaled_size = self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale

        # update the underline rect
        self.underline_pos = self.scaled_pos[0], self.scaled_pos[1]+0.95*self.scaled_size[1]
        self.underline_size = self.scaled_size[0], 0.05*self.scaled_size[1]
        self.underline_rect = pygame.Rect(self.underline_pos, self.underline_size)

        # update the text
        self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
        self.text_rect = self.text_surf.get_rect()
        self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        return None