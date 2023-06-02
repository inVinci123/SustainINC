import math
import pygame

import Scripts.AssetManager as am
import Scripts.AudioManager as audio
import Scripts.OverlayGUI as overlay
from Scripts.ScreenElements import Button, InteractionPrompt, Options, OptionsPrompt

class Collider:
    """ base class for all physical colliders in the game (mostly used as a standalone non abstract class) """
    def __init__(self, unscaled_pos: tuple[float, float], unscaled_size: tuple[float, float] = (512, 512)) -> None:
        # init the positions and sizes
        self.unscaled_pos: tuple[float, float] = unscaled_pos
        self.scale = 1
        self.scaled_pos: tuple[float, float] = unscaled_pos
        self.unscaled_size: tuple[float, float] = unscaled_size
        self.scaled_size: tuple[float, float] = (self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale)

        self.inframe: bool = True
        self.col_rect = pygame.Rect(self.scaled_pos, self.scaled_size) # colliding rectangle
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], debugging=False) -> tuple[float, float]:
        """ update the collider rectangle relative to the camera, draw stuff if required """
        rel_pos: tuple[float, float] = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        self.col_rect.topleft = rel_pos # type: ignore
        if debugging:
            pygame.draw.rect(screen, 0xFFFFFF, self.col_rect, 1)
        return rel_pos

    def update_scale(self, scale) -> None:
        """ adjust everything to the new scale """
        self.scale = scale
        self.scaled_pos = self.unscaled_pos[0]*scale, self.unscaled_pos[1]*scale
        self.scaled_size = (self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale)
        self.col_rect = pygame.Rect(self.scaled_pos, self.scaled_size)
        return None
    

class Building(Collider):
    """ Type of Collider (not used, basically depreciated, but left as a stepping stone between Collider and Sustain INC) """
    def __init__(self, name: str, pos: tuple[float, float], img_str: str | None = None) -> None:
        self.name = name # name of the building
        # position and size stuff
        self.unscaled_pos: tuple[float, float] = pos
        self.scale = 1
        self.scaled_pos: tuple[float, float] = pos

        self.unscaled_size: tuple[float, float] = (512, 512) # set it to the size of the building sprite instead
        self.scaled_size: tuple[float, float] = (self.unscaled_size[0]*self.scale, self.unscaled_size[1]*self.scale)
        self.colour = 0x696969 # temp col of the building when testing it

        
        self.inframe: bool = True
        self.col_rect = pygame.Rect(self.scaled_pos, self.scaled_size)

        # if the building has an image, save it
        self.img = img_str
        if self.img:
            self.image = am.buildings[self.img]

        # name tag of the building
        self.name_tag = am.normal_font[14 if len(name)>12 else 16].render(name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int=0) -> tuple[float, float]:
        """ draw the building and update it's position """
        # get the position relative to where the camera is
        rel_pos: tuple[float, float] = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        self.col_rect.topleft = rel_pos # type: ignore
        if self.inframe: # only draw if it's in frame
            if not self.img:
                # draw the collider if there's no image
                pygame.draw.rect(screen, self.colour ,self.col_rect)
                screen.blit(self.name_tag, (rel_pos[0]+self.col_rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height))
            else:
                # else draw the image
                screen.blit(self.image, rel_pos)
                screen.blit(self.name_tag, (rel_pos[0]+self.col_rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height))
        return rel_pos

    def update_scale(self, scale) -> None:
        """ adjust everything to the new scale """
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
    """ Interactable Element + Building. Generates income & cost functions for levelling. """
    def __init__(self, gm, flags: dict[str, bool|int|object]) -> None:
        # a reference to the game manager is necessary
        self.gm = gm
        self.flags = flags # game flags (mutable dict containing information about whether certain game events have happened or not)
        pos = (-1040, 1760) # position of sustain on the map
        super().__init__("SUSTAIN INC.", pos, "SustainINC") # init the Building constructor

        # interaction stuff
        self.interaction_radius = 400
        self.can_interact: bool = False
        self.uninteracting = False

        self.inframe: bool = True

        # building level system + income/cost functions
        self.level = 0
        self.max_level = 30
        self.income = self.income_at_level(self.level)
        self.cost = math.exp(2*self.level) # exponential growth -> cost gets increasingly greater than the income

        self.previous_aslet_level: int = 0 # to check whether aslet has been upgraded (which increases the player income)

        self.prompts: list[InteractionPrompt] = [OptionsPrompt(f"Upgrade to level {self.level+1}?")] # interaction prompts
        self.prompt_index: int = 0 # which prompt is it on (unneccesary but maintained for consistency with other interactables)
        return None
    
    def income_at_level(self, lvl) -> float:
        """ return the income at the given level """
        return ((math.exp((1.5+0.0132*lvl)*lvl) -3*self.level)*(1+self.flags["investmentlevel"]*0.1)) # type: ignore
    
    def check_interact(self, player_pos) -> bool:
        """ check if the player is within the interaction range of the building """
        if self.can_interact: # if player can already interact, check whether it can no longer interact
            x, y = player_pos[0]-(self.unscaled_pos[0]+self.unscaled_size[0]/2), player_pos[1]-(self.unscaled_pos[1]+self.unscaled_size[1]/2) # COMPARE IT FROM THE CENTRE!
            if math.sqrt(x**2 + y**2) > self.interaction_radius:
                self.can_interact = False
        else: # else check if the player can interact
            x, y = player_pos[0]-(self.unscaled_pos[0]+self.unscaled_size[0]/2), player_pos[1]-(self.unscaled_pos[1]+self.unscaled_size[1]/2)
            if math.sqrt(x**2 + y**2) <= self.interaction_radius:
                self.can_interact = True
        return self.can_interact
    
    def interact(self) -> bool:
        """ provides the interaction prompt to the overlay gui and returns whether the interactable building wants to uninteract """
        if self.flags["investmentlevel"] != self.previous_aslet_level: # if aslet was upgraded, re evaluate income
            self.previous_aslet_level = self.flags["investmentlevel"] # type: ignore
            self.income = self.income_at_level(self.level)
            if self.level < self.max_level: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nCurrent Level: {self.level}\nCurrent Income: {overlay.format_value(int(self.income))}/s\nUpgrade to level {self.level+1}? (New income={overlay.format_value(int(self.income_at_level(self.level+1)))}/s)", Options([(f"$ {overlay.format_value(self.cost)}", self.upgrade), ("Cancel", self.uninteract)]))]
            else: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nMax Level ({self.max_level})\nCurrent Income: {overlay.format_value(int(self.income))}/s", Options([("Cancel", self.uninteract)]))]
        
        if self.uninteracting: # if the player wants to uninteract, stop interacting
            self.uninteracting = False
            return True
        
        # update the overlay gui with the prompt
        overlay.gui.show_prompt = True
        overlay.gui.prompt = self.prompts[self.prompt_index]
        overlay.gui.update_scale(self.scale)
        return False
    
    def uninteract(self) -> None:
        """ stop interacting with the building """
        self.uninteracting = True
        return None
    
    def next_dialogue(self) -> bool:
        """ for other interactables, this goes to the next prompt index, but since there's only one prompt, it doubles up as uninteract """
        return False
    
    def update_scale(self, scale) -> None:
        """ adjust everything to the new scale """
        super().update_scale(scale)
        if self.level < self.max_level: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nCurrent Level: {self.level}\nCurrent Income: {overlay.format_value(int(self.income))}/s\nUpgrade to level {self.level+1}? (New income={overlay.format_value(int(self.income_at_level(self.level+1)))}/s)", Options([(f"$ {overlay.format_value(self.cost)}", self.upgrade), ("Cancel", self.uninteract)]))]
        else: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nMax Level ({self.max_level})\nCurrent Income: {overlay.format_value(int(self.income))}/s", Options([("Cancel", self.uninteract)]))]
        return None
    
    def upgrade(self) -> None:
        """ upgrade sustain if possible """
        if self.level < self.max_level:
            if self.gm.resources < self.cost: return None # safety check: if there isn't enough money, don't do anything
            self.level += 1
            self.flags["carboncontribution"] -= min(14, 0.75*self.level) # type: ignore # since Sustain INC is an actual sustainiblity consulting business, it helps reduce the carbon foot print (capped at 14 per level though)
            self.gm.resources -= self.cost

            audio.play_sound("upgrade")

            # update the income and cost functions
            self.income = self.income_at_level(self.level)
            self.cost = math.e**(2*self.level)

            # update the upgrade prompts
            if self.level < self.max_level: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nCurrent Level: {self.level}\nCurrent Income: {overlay.format_value(int(self.income))}/s\nUpgrade to level {self.level+1}? (New income={overlay.format_value(int(self.income_at_level(self.level+1)))}/s)", Options([(f"$ {overlay.format_value(self.cost)}", self.upgrade), ("Cancel", self.uninteract)]))]
            else: self.prompts = [OptionsPrompt(f"SUSTAIN, INC\nMax Level ({self.max_level})\nCurrent Income: {overlay.format_value(int(self.income))}/s", Options([("Cancel", self.uninteract)]))]
            
            overlay.gui.push_notification(f"Upgraded Sustain to lvl {self.level}!" , "upgrade")
            
            # add an objective to upgrade sustain to the next level (unless it's on max level)
            if not self.level == self.max_level:
                overlay.gui.add_objective("upgradesustain", f"Upgrade Sustain to Level {self.level+1}")
            else:
                overlay.gui.remove_objective("upgradesustain")
            
            # update the global list of flags
            self.flags["sustainlevel"] = self.level

            # remind the player to meet melon usk again once they upgrade to level 5
            if self.level >= 5 and not self.flags["secondmeloninteraction"]:
                overlay.gui.add_objective("meetuskagain", "Go to Melon Usk")
                
        elif self.level == self.max_level: # change the upgrade prompt to a max level prompt instead
            self.prompts = [OptionsPrompt(f"Max Level ({self.max_level})", Options([("Cancel", self.uninteract)]))]
        return None
    
    def check_upgrade(self) -> None:
        """ check if an upgrade is possible, if not, deactivate the upgrade button """
        if self.level == self.max_level:
            return None
        if self.cost > self.gm.resources:
            self.prompts[0].opts.options[0].inactive = True # type: ignore
        else:
            self.prompts[0].opts.options[0].inactive = False # type: ignore
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, debug_circle: bool = False) -> None:
        """ draw and keep updating the building details """
        rel_pos: tuple[float, float] = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        self.col_rect.topleft = rel_pos # type: ignore
        if self.inframe:
            if debug_circle: # debugging only - show the interaction radius
                pygame.draw.circle(screen, 0xFFFFFF, (rel_pos[0]+self.col_rect.size[0]/2, rel_pos[1]+self.col_rect.size[1]/2), self.interaction_radius*self.scale, 1)
            if self.can_interact:
                screen.blit(self.image, rel_pos) # draw another image on top if interaction is possible
            screen.blit(self.name_tag, (rel_pos[0]+self.col_rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height))
        self.check_upgrade()
        return None