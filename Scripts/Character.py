import pygame
import Scripts.AssetManager as am
from Scripts.Building import SustainINC
import Scripts.OverlayGUI as overlay
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt

class Character():
    """ Base class for all the Characters in the game (NPCs & Player) """
    def __init__(self, anim: dict[str, dict[str, list[pygame.Surface]]], pos: tuple[float, float]) -> None:
        self.is_player: bool = False

        self.name: str = ""
        # anim stuff
        self.anim = anim # animation dictionary
        self.anim_state = "idle"
        self.anim_dir = "s" # can be one of wasd

        # pos stuff
        self.unscaled_pos: tuple[float, float] = pos
        self.scale: float = 1
        self.scaled_pos: tuple[float, float] = pos
        self.rect = self.anim[self.anim_dir][self.anim_state][0].get_rect()
        
        # the main colliding rect
        self.collider_rect = pygame.Rect((0, 0), (0.45*self.rect.width, 0.9*self.rect.height))
        self.inframe: bool = True
        return None

    def move(self, x: float = 0, y: float = 0) -> None:
        """ move the character (only used for player) """
        self.unscaled_pos = self.unscaled_pos[0]+x, self.unscaled_pos[1]+y
        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int=0) -> tuple[float, float]:
        """ Update the character's position and draw it if it's in frame """
        relative_pos = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        self.rect.topleft = relative_pos # type: ignore
        self.collider_rect.center = self.rect.center
        if self.inframe:
            screen.blit(self.anim[self.anim_dir][self.anim_state][tick], relative_pos)
        return relative_pos

    def update_scale(self, scale: float, new_anim = None) -> None:
        """ adjust the character according to the new scale """
        self.scale = scale
        self.move() # to reset the character's scaled position
        if new_anim: self.anim = new_anim # update it's animation if provided
        # update the collider and normal rects
        self.rect = self.anim[self.anim_dir][self.anim_state][0].get_rect()
        self.collider_rect = pygame.Rect((0, 0), (0.45*self.rect.width, 0.9*self.rect.height))
        return None


class Player(Character):
    """ Modified character to contain the player colliders and rendering"""
    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(am.ben_anim, pos)
        # interaction stuff
        self.can_interact: bool = False
        self.is_player = True
        self.interaction_character: NPC | SustainINC | None

        # a collider for each edge and corner (for the 8 collider system, elaborated in GameManager.py, process_collisions)
        self.col = {
            "tl": pygame.Rect(self.collider_rect.topleft, (8*self.scale, 8*self.scale)), # top
            "l": pygame.Rect((self.collider_rect.left, self.collider_rect.centery-12*self.scale), (8*self.scale, 24*self.scale)), # top left
            "bl": pygame.Rect((self.collider_rect.left, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)), # bottom left
            "b": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.bottom-8*self.scale), (16*self.scale, 8*self.scale)), # bottom
            "br": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)), # bottom right
            "r": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.centery-12*self.scale), (8*self.scale, 24*self.scale)), # right
            "tr": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.top), (8*self.scale, 8*self.scale)), # top right
            "t": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.top), (16*self.scale, 8*self.scale)) # top
        }
        return None
    
    def move(self, x: float = 0, y: float = 0, anim_dir: str = "x") -> None:
        """ move the player and update it's animation direction """
        super().move(x, y)
        if anim_dir != "x":
            self.anim_dir = anim_dir
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, walking: bool = False) -> None:
        """ draw the player and update the colliders with any change in positions """
        self.anim_state = "walk" if walking else "idle" # set the correct animation state before the base rendering takes place
        super().draw(screen, cam_pos, tick)
        self.col = { # update the 8 colliders based on the updated default collider 
            "tl": pygame.Rect(self.collider_rect.topleft, (8*self.scale, 8*self.scale)),
            "l": pygame.Rect((self.collider_rect.left, self.collider_rect.centery-12*self.scale), (8*self.scale, 24*self.scale)),
            "bl": pygame.Rect((self.collider_rect.left, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "b": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.bottom-8*self.scale), (16*self.scale, 8*self.scale)),
            "br": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "r": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.centery-12*self.scale), (8*self.scale, 24*self.scale)),
            "tr": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.top), (8*self.scale, 8*self.scale)),
            "t": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.top), (16*self.scale, 8*self.scale))
        }
        return None

    def update_scale(self, scale: float, new_anim=None) -> None:
        """ adjust the colliders and animations according to the new scale """
        super().update_scale(scale, new_anim)
        self.col = {
            "tl": pygame.Rect(self.collider_rect.topleft, (8*self.scale, 8*self.scale)),
            "l": pygame.Rect((self.collider_rect.left, self.collider_rect.centery-12*self.scale), (8*self.scale, 24*self.scale)),
            "bl": pygame.Rect((self.collider_rect.left, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "b": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.bottom-8*self.scale), (16*self.scale, 8*self.scale)),
            "br": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "r": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.centery-12*self.scale), (8*self.scale, 24*self.scale)),
            "tr": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.top), (8*self.scale, 8*self.scale)),
            "t": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.top), (16*self.scale, 8*self.scale))
        }
        self.anim = am.ben_anim
        return None


class NPC(Character):
    """ Base class for the Non Playable Characters. All the NPCs in GameCharacters.py inherity from this class. """
    def __init__(self, anim: dict[str, dict[str, list[pygame.Surface]]], pos: tuple[float, float], name: str = "John Doe", prompts: list[list[InteractionPrompt]] = []) -> None:
        super().__init__(anim, pos)

        # name and name tag variables
        self.name = name
        self.name_tag = am.normal_font[14 if len(name)>12 else 16].render(name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        
        # interaction variables
        self.interaction_radius = 120
        self.can_interact = False
        self.uninteracting = False
        
        # interaction prompt variables
        self.prompt_index: int = 0 # current prompt in the sequence
        self.level: int = 0 # which sequence of prompts to show
        if prompts == []: # default prompt
            self.prompts: list[list[InteractionPrompt]] = [[InteractionPrompt(f"{self.name}: Hello there! ..."), OptionsPrompt("What will you do?", Options([("Leave", self.uninteract)]))]]
        else:
            self.prompts = prompts
        return None
    
    def check_interact(self, player_pos) -> bool:
        """ check if the player is within interaction range """
        if self.can_interact: # if already can interact, check if they are no longer able to interact
            x, y = player_pos[0]-self.unscaled_pos[0], player_pos[1]-self.unscaled_pos[1]
            if x**2 + y**2 > self.interaction_radius**2:
                self.can_interact = False
            self.anim_dir = "a" if x < 0 else "d"
        else: # if they can't interact, check if they can intereact
            x, y = player_pos[0]-self.unscaled_pos[0], player_pos[1]-self.unscaled_pos[1]
            if x**2 + y**2 <= self.interaction_radius**2:
                self.can_interact = True
        return self.can_interact
    
    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, debug_circle: bool = False) -> None:
        """ draw the NPC and evaluate their position """
        rel_pos = super().draw(screen, cam_pos, tick)
        screen.blit(self.name_tag, (rel_pos[0]+self.rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height))
        if debug_circle: pygame.draw.circle(screen, 0xFFFFFF, (rel_pos[0]+self.rect.size[0]/2, rel_pos[1]+self.rect.size[1]/2), self.interaction_radius*self.scale, 1)
        return None
    
    def interact(self) -> bool:
        """ returns False if the interaction is continued else True """
        if self.uninteracting:
            self.uninteracting = False
            return True
        # if the interaction is continued, show the current overlay prompt
        overlay.gui.show_prompt = True
        overlay.gui.prompt = self.prompts[self.level][self.prompt_index]
        overlay.gui.update_scale(self.scale)
        return False
    
    def uninteract(self) -> None:
        """ stop interacting """
        self.uninteracting = True
        self.prompt_index = 0
        return None
    
    def next_dialogue(self, num=1) -> bool:
        """ move to the next dialogue if possible, else uninteract """
        self.prompt_index += num
        if self.prompt_index >= len(self.prompts[self.level]):
            self.prompt_index = 0
            self.uninteract()
            return False
        else:
            return True

    def update_scale(self, scale: float, new_anim=None) -> None:
        """ adjust the NPC according to the new scale """
        super().update_scale(scale, new_anim) # update the animation and collliders
        # update the name tag
        self.name_tag = am.normal_font[14 if len(self.name)>12 else 16].render(self.name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        return None
