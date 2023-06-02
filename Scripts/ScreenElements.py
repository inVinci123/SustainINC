import pygame
import math

import Scripts.AssetManager as am
import Scripts.AudioManager as audio

class Button:
    def __init__(self, pos, size, on_click, inactive_colour = 0x6A6A6A, normal_colour = 0xFBFBFB, hover_colour = 0xC3C3C3, click_colour = 0x999999) -> None:
        self.unscaled_pos = pos
        self.unscaled_size = size
        self.scale = 1
        self.scaled_pos = self.unscaled_pos
        self.scaled_size = self.unscaled_size

        self.on_click = on_click

        self.inactive_colour = inactive_colour
        self.normal_colour = normal_colour
        self.hover_colour = hover_colour
        self.click_colour = click_colour

        self.rect = pygame.Rect(self.scaled_pos, self.scaled_size)

        self.game_screen_dimensions = (0, 0)

        self.hover, self.click, self.click_complete = False, False, False
        return None
    
    def check(self) -> None:
        mouse = pygame.mouse.get_pos()
        r_click = pygame.mouse.get_pressed()[0]

        # evaluate the actual mouse position would be if black bars are present
        w_s = pygame.display.get_window_size()
        relative_origin = ((w_s[0]-self.game_screen_dimensions[0])/2, (w_s[1]-self.game_screen_dimensions[1])/2)
        mouse = (mouse[0]-relative_origin[0], mouse[1]-relative_origin[1])
        
        self.hover = self.rect.collidepoint(mouse)
        if not self.click:
            self.click = self.hover and r_click
        else:
            if not r_click:
                if self.hover:
                    self.click_complete = True
                    self.click = False
                else:
                    self.click = False
        return None
    
    def update_scale(self, scale) -> None:
        self.scale = scale
        self.scaled_pos = scale*self.unscaled_pos[0], scale*self.unscaled_pos[1]
        self.scaled_size = scale*self.unscaled_size[0], scale*self.unscaled_size[1]
        self.rect = pygame.Rect(self.scaled_pos, self.scaled_size)
        return None
    
    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        if check: 
            self.check()
            colour = self.click_colour if self.click else (self.hover_colour if self.hover else self.normal_colour)
            if self.click_complete:
                audio.play_sound("click")
                self.on_click()
                self.click_complete = False
        else:
            self.click = False
            colour = self.inactive_colour

        self.game_screen_dimensions = screen.get_size()
        pygame.draw.rect(screen, colour, self.rect)
        return None

class SpriteButton(Button):
    def __init__(self, pos, on_click, inactive_image: pygame.Surface, normal_image: pygame.Surface, hover_image, click_image) -> None:
        self.pos = pos

        self.inactive_image = inactive_image
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.click_image = click_image

        self.rect = self.normal_image.get_rect()
        self.rect.topleft = pos
        self.size = self.rect.size

        self.on_click = on_click

        self.hover, self.click, self.click_complete = False, False, False
        return None

    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        if check: 
            self.check()
            image = self.click_image if self.click else (self.hover_image if self.hover else self.normal_image)
            if self.click_complete:
                self.on_click()
                self.click_complete = False
        else:
            self.click = False
            image = self.inactive_image
        screen.blit(image, self.pos)
        return None
    
class TextButton(Button):
    def __init__(self, pos, size, on_click, text: str = "Hello World!", inactive_colour=6974058, normal_colour=16514043, hover_colour=12829635, click_colour=10066329, text_colour=1710618) -> None:
        super().__init__(pos, size, on_click, inactive_colour, normal_colour, hover_colour, click_colour)
        self.str = text
        self.text_colour = text_colour
        self.inactive = False
        try:
            self.text = Text(text, (self.scaled_pos[0]+self.scale*10, self.scaled_pos[1]+self.scale*10), (self.scaled_size[0]-self.scale*20, self.scaled_size[1]-self.scale*20), am.normal_font[18], self.text_colour)
        except AttributeError:
            pass
        return None
    
    def update_scale(self, scale) -> None:
        super().update_scale(scale)
        self.text = Text(self.str, (self.scaled_pos[0]+self.scale*10, self.scaled_pos[1]+self.scale*10), (self.scaled_size[0]-self.scale*20, self.scaled_size[1]-self.scale*20), am.normal_font[18], self.text_colour)
        return None
    
    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        super().draw(screen, check and not self.inactive)
        self.text.draw(screen)
        return None

class CenteredTextButton(Button):
    def __init__(self, pos, size, on_click, text: str = "Hello World!", scale = 1, inactive_colour=6974058, normal_colour=16514043, hover_colour=12829635, click_colour=10066329, text_colour=1710618) -> None:
        super().__init__(pos, size, on_click, inactive_colour, normal_colour, hover_colour, click_colour)
        self.str = text
        self.scale = scale
        self.text_colour = text_colour
        self.inactive = False
        try:
            self.text_surf = am.normal_font[24].render(self.str, True, self.text_colour)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_size[0] - self.text_rect.width/2, self.scaled_size[1] - self.text_rect.height/2)
        except AttributeError:
            pass
        return None
    
    def update_scale(self, scale) -> None:
        super().update_scale(scale)
        self.text_surf = am.normal_font[24].render(self.str, True, self.text_colour)
        self.text_rect = self.text_surf.get_rect()
        self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2 - self.text_rect.height/2)
        return None
    
    def draw(self, screen: pygame.Surface, check: bool = True) -> None:
        super().draw(screen, check and not self.inactive)
        screen.blit(self.text_surf, self.text_pos)
        return None

class Text:
    def __init__(self, text: str, scaled_pos: tuple[float, float], text_box_size: tuple[float, float], font: pygame.font.Font, colour = 0x1A1A1A) -> None:
        self.text = text
        self.pos = scaled_pos
        self.size = text_box_size
        self.font = font
        self.colour = colour
        self.game_screen_size = (1280, 720)
        self.scale = 1
        self.text_surf = self.generate_text_surf()
        return None
    
    def generate_text_surf(self) -> pygame.Surface:
        avg_length, height = self.font.render("a", True, self.colour).get_rect().size
        cpl = int((self.size[0]-5*self.scale)/avg_length)
        split_string = self.text.split("\n")
        lines = []
        a = pygame.Surface(self.size, pygame.SRCALPHA) # transparent background surface
        for s in split_string:
            n = math.ceil(len(s)/cpl)

            for i in range(n):
                line = s[i*cpl:(i+1)*cpl]
                if line[-1] in " ,-.!/": # end of the line is empty
                    b = self.font.render(s[i*cpl:(i+1)*cpl].strip(), True, self.colour)
                else:
                    try:
                        if s[(i+1)*cpl] == ' ': # if the beginning of the next line is empty
                            b = self.font.render(s[i*cpl:(i+1)*cpl].strip(), True, self.colour)
                        else:
                            b = self.font.render(s[i*cpl:(i+1)*cpl].strip() + "-", True, self.colour) # a dash to signify next line is a continuation
                    except IndexError: # Index out of range, i.e. this is the last line
                        b = self.font.render(s[i*cpl:(i+1)*cpl].strip(), True, self.colour)                        
                lines.append(b)
        
        for i, b in enumerate(lines):
            a.blit(b, (0, i*height))
        return a

    def draw(self, game_screen: pygame.Surface):
        if game_screen.get_size() != self.game_screen_size:
            # Quick optimisation to only update the text surface when the game screen has changed
            self.game_screen_size = game_screen.get_size()
            self.scale = min(self.game_screen_size[0]/1280, self.game_screen_size[1]/720)
            self.text_surf = self.generate_text_surf()
        game_screen.blit(self.text_surf, self.pos)


class InteractionPrompt:
    def __init__(self, text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.") -> None:
        self.scale: float = 1
        self.unscaled_pos = (140, 500)
        self.unscaled_size = (1000, 140)
        self.scaled_pos = self.unscaled_pos
        self.scaled_size = self.unscaled_size

        self.transparent_surf = pygame.Surface(self.scaled_size)
        self.transparent_surf.fill(0X2A2A2A)
        self.transparent_surf.set_alpha(100)

        self.text = text
        text_box_pos = ((self.unscaled_pos[0]+10)*self.scale, (self.unscaled_pos[1]+10)*self.scale)
        text_box_size = ((self.unscaled_size[0]-20)*self.scale, (self.unscaled_size[1]-20)*self.scale)
        try:
            self.text_box: Text = Text(self.text, text_box_pos, text_box_size, am.normal_font[18])
        except AttributeError:
            pass
        return None
    
    def update_scale(self, scale: float) -> None:
        self.scale = scale
        self.scaled_pos = (self.unscaled_pos[0]*scale, self.unscaled_pos[1]*scale)
        self.scaled_size = (self.unscaled_size[0]*scale, self.unscaled_size[1]*scale)

        text_box_pos = ((self.unscaled_pos[0]+10)*scale, (self.unscaled_pos[1]+10)*scale)
        text_box_size = ((self.unscaled_size[0]-20)*scale, (self.unscaled_size[1]-20)*scale)
        self.text_box = Text(self.text, text_box_pos, text_box_size, am.normal_font[18], 0xFAFAFAFF)
        self.transparent_surf = pygame.Surface(self.scaled_size)
        self.transparent_surf.fill(0x000000)
        self.transparent_surf.set_alpha(180)
        return None
    
    def draw(self, screen, check=True) -> None:
        screen.blit(self.transparent_surf, self.scaled_pos)
        self.text_box.draw(screen)
        return None
    

class Options:
    def __init__(self, opts: list[tuple[str, object]] = []) -> None:
        if len(opts) == 0:
            self.options = [
                TextButton((140, 650), (300, 38), lambda: print("Option 1 clicked!"), "Option 1", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1),
                TextButton((490, 650), (300, 38), lambda: print("Option 2 clicked!"), "Option 2", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1),
                TextButton((840, 650), (300, 38), lambda: print("Option 3 clicked!"), "Option 3", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1)
            ]
        elif len(opts) <= 3:
            self.options: list[Button] = []
            for i, o in enumerate(opts):
                self.options.append(TextButton((140 + i*350, 650), (300, 38), o[1], o[0], 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1))
        return None
    
    def update_scale(self, scale) -> None:
        for o in self.options:
            o.update_scale(scale)
        return None
    
    def draw(self, screen, check=True) -> None:
        for o in self.options:
            o.draw(screen, check)
        return None


class OptionsPrompt(InteractionPrompt):
    def __init__(self, text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", options: Options = Options()) -> None:
        super().__init__(text)
        self.opts = options
    
    def update_scale(self, scale: float) -> None:
        super().update_scale(scale)
        self.opts.update_scale(scale)
        return None
    
    def draw(self, screen, check=True) -> None:
        super().draw(screen)
        self.opts.draw(screen, check)
        return None
    
class InputField:
    def __init__(self, unscaled_pos, unscaled_size, scale=1, chr_limit=11) -> None:
        self.scale = scale
        self.game_screen_dimensions = (1280*scale, 720*scale)

        self.unscaled_pos = unscaled_pos
        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale

        self.unscaled_size = unscaled_size
        self.scaled_size = self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale

        self.underline_pos = self.scaled_pos[0], self.scaled_pos[1]+0.95*self.scaled_size[1]
        self.underline_size = self.scaled_size[0], 0.05*self.scaled_size[1]

        self.character_limit = chr_limit
        self.allowed_characters="ACBDEFGHIJKLMNOPQRSTUVWXYZacbdefghijklmnopqrstuvwxyz_.,?<>\"':;][]{ }\\|-+=`~!@#$%^&*()"

        self.is_active: bool = False
        self.hover: bool = False
        self.click: bool = False

        self.str = "Name: "
        self.name_str = ""
        self.timer = 0.5

        self.col: int = 0xFAFAFA
        self.underline_rect = pygame.Rect(self.underline_pos, self.underline_size)
        
        self.running_time: float = 0
        self.cursor_blink_rate: float = 0.45
        self.cursor_cool_time: float = self.cursor_blink_rate
        
        try:
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        
        except AttributeError:
            pass
        return None
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.scaled_pos, self.scaled_size)
    
    def check(self) -> None:
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
                    self.is_active = True
                else:
                    self.click = False
        
        if r_click and not self.hover:
            self.is_active = False
        return None
    
    def draw(self, screen: pygame.Surface, deltatime=0.1) -> None:
        self.running_time += deltatime
        self.cursor_cool_time -= deltatime
        if self.cursor_cool_time <= -self.cursor_blink_rate: self.cursor_cool_time = self.cursor_blink_rate
        
        self.check()
        if self.is_active:
            if self.col == 0xFF0000 and self.timer > 0:
                self.timer -= deltatime
            else:
                self.col = 0x690000 if len(self.name_str) > self.character_limit else 0xFAFAFA
        else:
            if self.click:
                self.col = 0xFAFAFA
            elif self.hover:
                self.col = 0x9A9A9A
            else:
                self.col = 0x696969
            
        pygame.draw.rect(screen, self.col, self.underline_rect)

        if self.is_active and self.cursor_cool_time > 0:
            self.text_surf = am.normal_font[30].render(self.str+self.name_str+"|", True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/20, self.scaled_pos[1] + self.scaled_size[1]/2)
        else:
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/20, self.scaled_pos[1] + self.scaled_size[1]/2)

        screen.blit(self.text_surf, self.text_pos)
        return None
    
    def add_letter(self, letter) -> None:
        if len(self.name_str) > self.character_limit:
            self.col = 0xFF0000
            self.timer = 0.5
        else:
            self.name_str += letter
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        return None
    
    def backspace(self, clear: bool=False) -> None:
        if len(self.name_str) == 0:
            self.col = 0xFF0000
            self.timer = 0.5
        else:
            
            self.name_str = "" if clear else self.name_str[:-1]
            self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
            self.text_rect = self.text_surf.get_rect()
            self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        return None
    
    def update_text(self, events: list[pygame.event.Event], keys_pressed=[]) -> None:
        if not self.is_active:
            return None
        try:
            ctrl = keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]
        except IndexError:
            ctrl = False
        for e in events:
            try:
                if e.type == pygame.KEYDOWN:
                    if e.unicode in self.allowed_characters:
                        self.add_letter(e.unicode)
                    elif e.key == pygame.K_BACKSPACE:
                        self.backspace(ctrl)
            except AttributeError:
                pass
        return None
    
    def update_scale(self, scale) -> None:
        self.scale = scale
        self.game_screen_dimensions = (1280*scale, 720*scale)

        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale
        self.scaled_size = self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale

        self.underline_pos = self.scaled_pos[0], self.scaled_pos[1]+0.95*self.scaled_size[1]
        self.underline_size = self.scaled_size[0], 0.05*self.scaled_size[1]

        self.underline_rect = pygame.Rect(self.underline_pos, self.underline_size)

        self.text_surf = am.normal_font[30].render(self.str+self.name_str, True, 0xFFFFFFFF)
        self.text_rect = self.text_surf.get_rect()
        self.text_pos = (self.scaled_pos[0] + self.scaled_size[0]/2 - self.text_rect.width/2, self.scaled_pos[1] + self.scaled_size[1]/2)
        return None