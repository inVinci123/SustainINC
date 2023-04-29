import pygame
import math

class Button:
    def __init__(self, pos, size, on_click, inactive_colour = 0x6A6A6A, normal_colour = 0xFBFBFB, hover_colour = 0xC3C3C3, click_colour = 0x999999) -> None:
        self.pos = pos
        self.size = size
        self.on_click = on_click

        self.inactive_colour = inactive_colour
        self.normal_colour = normal_colour
        self.hover_colour = hover_colour
        self.click_colour = click_colour

        self.rect = pygame.Rect(pos, size)

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
        # to add: text
        return None

class Text:
    def __init__(self, text: str, text_box_size: tuple[float, float], font: pygame.font.Font, colour = 0x1A1A1A) -> None:
        self.text = text
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
            a = pygame.Surface(self.size, pygame.SRCALPHA)
            for i in range(lines):
                b = self.font.render(self.text[i*cpl:(i+1)*cpl], True, self.colour)
                # blitting surfaces over surfaces reduces their quality, might be better to test the real width of each character and then work like that accordingly
                # b = pygame.Surface((self.size[0], rect.height))
                # b.set_colorkey((0, 0, 0))
                # b.blit(text_box, (-i*self.size[0], 0))
                a.blit(b, (0, i*height))

            return a
    
    def draw(self, game_screen):
        game_screen.blit(self.generate_text_surf(), (69, 69))


