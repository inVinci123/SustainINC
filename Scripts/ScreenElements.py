import pygame
import math

import Scripts.AssetManager as am

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

        self.hover, self.click, self.click_complete = False, False, False
        return None
    
    def check(self) -> None:
        mouse = pygame.mouse.get_pos()
        r_click = pygame.mouse.get_pressed()[0]
        
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
                self.on_click()
                self.click_complete = False
        else:
            self.click = False
            colour = self.inactive_colour
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
        super().draw(screen, check)
        self.text.draw(screen)
        return None


class Text:
    def __init__(self, text: str, pos: tuple[float, float], text_box_size: tuple[float, float], font: pygame.font.Font, colour = 0x1A1A1A) -> None:
        self.text = text
        self.pos = pos
        self.size = text_box_size
        self.font = font
        self.colour = colour

        self.text_surf = self.generate_text_surf()
        return None
    
    def generate_text_surf(self) -> pygame.Surface:
        text_box = self.font.render(self.text, True, self.colour)
        avg_length, height = self.font.render("a", True, self.colour).get_rect().size
        cpl = int(self.size[0]/avg_length)
        lines = math.ceil(len(self.text)/cpl)
        if lines == 1:
            return text_box
        else:
            a = pygame.Surface(self.size, pygame.SRCALPHA) # transparent background surface
            for i in range(lines):
                b = self.font.render(self.text[i*cpl:(i+1)*cpl], True, self.colour)
                # blitting surfaces over surfaces reduces their quality, might be better to test the real width of each character and then work like that accordingly
                # b = pygame.Surface((self.size[0], rect.height))
                # b.set_colorkey((0, 0, 0))
                # b.blit(text_box, (-i*self.size[0], 0))
                a.blit(b, (0, i*height))
            return a
    
    def draw(self, game_screen):
        game_screen.blit(self.generate_text_surf(), self.pos)


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
    
    def draw(self, screen) -> None:
        screen.blit(self.transparent_surf, self.scaled_pos)
        self.text_box.draw(screen)
        return None
    
class OptionsPrompt(InteractionPrompt):
    def __init__(self, text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", options: list[Button] = []) -> None:
        super().__init__(text)
        if len(options) == 0:
            self.options = [
                TextButton((140, 650), (300, 38), lambda: print("Option 1 clicked!"), "Option 1", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1),
                TextButton((490, 650), (300, 38), lambda: print("Option 2 clicked!"), "Option 2", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1),
                TextButton((840, 650), (300, 38), lambda: print("Option 3 clicked!"), "Option 3", 0x020202, 0x2A2A2A, 0x1A1A1A, 0x080808, 0xF1F1F1F1)
            ]
        else:
            self.options = options
    
    def update_scale(self, scale: float) -> None:
        super().update_scale(scale)
        for opt in self.options:
            opt.update_scale(scale)
        return None
    
    def draw(self, screen) -> None:
        super().draw(screen)
        for opt in self.options:
            opt.draw(screen, True)
        return None