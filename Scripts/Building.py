import math
from decimal import Decimal
import pygame

import Scripts.AssetManager as am
import Scripts.OverlayGUI as overlay
from Scripts.ScreenElements import Button, InteractionPrompt, Options, OptionsPrompt

class Building:
    # learn how to make buildings here: https://www.youtube.com/watch?v=jKTOGz3XAcc
    def __init__(self, name: str, pos: tuple[float, float], img_str: str | None = None) -> None:
        self.name = name
        self.unscaled_pos: tuple[float, float] = pos
        self.scale = 1
        self.scaled_pos: tuple[float, float] = pos

        self.unscaled_size: tuple[float, float] = (512, 512) # set it to the size of the building sprite instead
        self.scaled_size: tuple[float, float] = (self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale)
        self.colour = 0x696969

        self.inframe: bool = True
        self.col_rect = pygame.Rect(self.scaled_pos, self.scaled_size)

        self.img = img_str
        if self.img:
            self.image = am.buildings[self.img]
        self.name_tag = am.normal_font[14 if len(name)>12 else 16].render(name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int=0) -> tuple[float, float]:
        rel_pos: tuple[float, float] = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        self.col_rect.topleft = rel_pos # type: ignore
        if self.inframe:
            if not self.img:
                pygame.draw.rect(screen, self.colour ,self.col_rect)
                screen.blit(self.name_tag, (rel_pos[0]+self.col_rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height))
            else:
                screen.blit(self.image, rel_pos)
                screen.blit(self.name_tag, (rel_pos[0]+self.col_rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height))
        return rel_pos

    def update_scale(self, scale) -> None:
        self.scale = scale
        if self.img:
            self.image = am.buildings[self.img]
        self.scaled_pos = self.unscaled_pos[0]*scale, self.unscaled_pos[1]*scale
        self.scaled_size = (self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale)
        self.name_tag = am.normal_font[14 if len(self.name)>12 else 16].render(self.name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        self.col_rect = pygame.Rect(self.scaled_pos, self.scaled_size)
        return None


class SustainINC(Building):
    def __init__(self, gm, flags: dict[str, bool|int|object]) -> None:
        self.gm = gm
        self.flags = flags
        pos = (580, 0)
        super().__init__("SUSTAIN INC.", pos, "SustainINC")

        self.interaction_radius = 400
        self.can_interact: bool = False
        self.uninteracting = False

        self.inframe: bool = True

        self.level = 0
        self.max_level = 30
        self.income = self.income_at_level(self.level)
        self.cost = math.exp(2*self.level)

        self.previous_aslet_level: int = 0

        self.prompts: list[InteractionPrompt] = [OptionsPrompt(f"Upgrade to level {self.level+1}?")]
        self.prompt_index: int = 0
        
        return None
    
    def income_at_level(self, lvl) -> float:
        return ((math.exp((1.5+0.0132*lvl)*lvl) -3*self.level)*(1+self.flags["investmentlevel"]*0.1)) # type: ignore
    
    def check_interact(self, player_pos) -> bool:
        if self.can_interact:
            x, y = player_pos[0]-(self.unscaled_pos[0]+self.unscaled_size[0]/2), player_pos[1]-(self.unscaled_pos[1]+self.unscaled_size[1]/2) # COMPARE IT FROM THE CENTRE!
            if math.sqrt(x**2 + y**2) > self.interaction_radius:
                self.can_interact = False
        else:
            x, y = player_pos[0]-(self.unscaled_pos[0]+self.unscaled_size[0]/2), player_pos[1]-(self.unscaled_pos[1]+self.unscaled_size[1]/2)
            if math.sqrt(x**2 + y**2) <= self.interaction_radius:
                self.can_interact = True
        return self.can_interact
    
    def interact(self) -> bool:
        """" returns whether the interactable building wants to uninteract """
        if self.flags["investmentlevel"] != self.previous_aslet_level: # if aslet was upgraded, reevaluate income
            self.previous_aslet_level = self.flags["investmentlevel"] # type: ignore
            self.income = self.income_at_level(self.level)
            if self.level < self.max_level: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nCurrent Level: {self.level}\nCurrent Income: {overlay.format_value(int(self.income))}/s\nUpgrade to level {self.level+1}? (New income={overlay.format_value(int(self.income_at_level(self.level+1)))}/s)", Options([(f"$ {overlay.format_value(self.cost)}", self.upgrade), ("Cancel", self.uninteract)]))]
            else: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nMax Level ({self.max_level})\nCurrent Income: {overlay.format_value(int(self.income))}/s", Options([("Cancel", self.uninteract)]))]
        
        if self.uninteracting:
            self.uninteracting = False
            return True
        overlay.gui.show_prompt = True
        overlay.gui.prompt = self.prompts[self.prompt_index]
        overlay.gui.update_scale(self.scale)
        return False
    
    def uninteract(self) -> None:
        self.uninteracting = True
        return None
    
    def next_dialogue(self) -> bool:
        return False
    
    def update_scale(self, scale) -> None:
        super().update_scale(scale)
        if self.level < self.max_level: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nCurrent Level: {self.level}\nCurrent Income: {overlay.format_value(int(self.income))}/s\nUpgrade to level {self.level+1}? (New income={overlay.format_value(int(self.income_at_level(self.level+1)))}/s)", Options([(f"$ {overlay.format_value(self.cost)}", self.upgrade), ("Cancel", self.uninteract)]))]
        else: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nMax Level ({self.max_level})\nCurrent Income: {overlay.format_value(int(self.income))}/s", Options([("Cancel", self.uninteract)]))]
        return None
    
    def upgrade(self) -> None:
        if self.level < self.max_level:
            if self.gm.resources < self.cost: return None
            self.level += 1
            self.gm.resources -= self.cost

            self.income = self.income_at_level(self.level)
            self.cost = math.e**(2*self.level)
            if self.level < self.max_level: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nCurrent Level: {self.level}\nCurrent Income: {overlay.format_value(int(self.income))}/s\nUpgrade to level {self.level+1}? (New income={overlay.format_value(int(self.income_at_level(self.level+1)))}/s)", Options([(f"$ {overlay.format_value(self.cost)}", self.upgrade), ("Cancel", self.uninteract)]))]
            else: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nMax Level ({self.max_level})\nCurrent Income: {overlay.format_value(int(self.income))}/s", Options([("Cancel", self.uninteract)]))]
            overlay.gui.push_notification(f"Upgraded Sustain to lvl {self.level}!" , "upgrade")
            if not self.level == self.max_level:
                overlay.gui.add_objective("upgradesustain", f"Upgrade Sustain to Level {self.level+1}")
            else:
                overlay.gui.remove_objective("upgradesustain")
            self.flags["sustainlevel"] = self.level
            # self.uninteract()
        elif self.level == self.max_level:
            self.prompts = [OptionsPrompt(f"Max Level ({self.max_level})", Options([("Cancel", self.uninteract)]))]
        return None
    
    def check_upgrade(self) -> None:
        if self.level == self.max_level:
            return
        if self.cost > self.gm.resources:
            self.prompts[0].opts.options[0].inactive = True # type: ignore
        else:
            self.prompts[0].opts.options[0].inactive = False # type: ignore
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, debug_circle: bool = False) -> None:
        self.colour = 0x424242 if self.can_interact else 0x696969
        rel_pos = super().draw(screen, cam_pos, tick)
        self.check_upgrade()
        if debug_circle:
            pygame.draw.circle(screen, 0xFFFFFF, (rel_pos[0]+self.col_rect.size[0]/2, rel_pos[1]+self.col_rect.size[1]/2), self.interaction_radius*self.scale, 1)
            # pygame.draw.circle(screen, 0xFFFFFF, (rel_pos[0], rel_pos[1]), self.interaction_radius*self.scale, 1)
        return None