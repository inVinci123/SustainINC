import pygame
import Scripts.AssetManager as am
from Scripts.Building import SustainINC
import Scripts.OverlayGUI as overlay
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt

class Character():
    def __init__(self, anim: dict[str, dict[str, list[pygame.Surface]]], pos: tuple[float, float]) -> None:
        self.anim = anim
        self.anim_state = "idle"
        self.anim_dir = "s"
        self.unscaled_pos: tuple[float, float] = pos
        self.scale: float = 1
        self.scaled_pos: tuple[float, float] = pos
        self.rect = self.anim[self.anim_dir][self.anim_state][0].get_rect()
        self.collider_rect = pygame.Rect((0, 0), (0.45*self.rect.width, 0.9*self.rect.height))
        return None

    def move(self, x: float = 0, y: float = 0) -> None:
        self.unscaled_pos = self.unscaled_pos[0]+x, self.unscaled_pos[1]+y
        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int=0) -> tuple[float, float]:
        relative_pos = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        self.rect.topleft = relative_pos # type: ignore
        self.collider_rect.center = self.rect.center
        screen.blit(self.anim[self.anim_dir][self.anim_state][tick], relative_pos)
        return relative_pos

    def update_scale(self, scale: float, new_anim = None) -> None:
        self.scale = scale
        self.move() # to reset the character's scaled position
        if new_anim: self.anim = new_anim
        self.rect = self.anim[self.anim_dir][self.anim_state][0].get_rect()
        self.collider_rect = pygame.Rect((0, 0), (0.45*self.rect.width, 0.9*self.rect.height))
        return None


class Player(Character):
    def __init__(self, pos: tuple[float, float]) -> None: # add an avatar, name argument?
        super().__init__(am.ben_anim, pos)
        self.can_interact: bool = False
        self.interaction_character: NPC | SustainINC | None

        self.col = {
            "tl": pygame.Rect(self.collider_rect.topleft, (8*self.scale, 8*self.scale)),
            "l": pygame.Rect((self.collider_rect.left, self.collider_rect.centery-24*self.scale), (8*self.scale, 48*self.scale)),
            "bl": pygame.Rect((self.collider_rect.left, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "b": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.bottom-8*self.scale), (16*self.scale, 8*self.scale)),
            "br": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "r": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.centery-24*self.scale), (8*self.scale, 48*self.scale)),
            "tr": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.top), (8*self.scale, 8*self.scale)),
            "t": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.top), (16*self.scale, 8*self.scale))
        }
        return None
    

    def move(self, x: float = 0, y: float = 0, anim_dir: str = "x") -> None:
        super().move(x, y)
        if anim_dir != "x":
            self.anim_dir = anim_dir
        return None
    

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, walking: bool = False) -> None:
        self.anim_state = "walk" if walking else "idle"
        super().draw(screen, cam_pos, tick)
        self.col = {
            "tl": pygame.Rect(self.collider_rect.topleft, (8*self.scale, 8*self.scale)),
            "l": pygame.Rect((self.collider_rect.left, self.collider_rect.centery-24*self.scale), (8*self.scale, 48*self.scale)),
            "bl": pygame.Rect((self.collider_rect.left, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "b": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.bottom-8*self.scale), (16*self.scale, 8*self.scale)),
            "br": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "r": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.centery-24*self.scale), (8*self.scale, 48*self.scale)),
            "tr": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.top), (8*self.scale, 8*self.scale)),
            "t": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.top), (16*self.scale, 8*self.scale))
        }
        return None

    def update_scale(self, scale: float, new_anim=None) -> None:
        super().update_scale(scale, new_anim)
        self.col = {
            "tl": pygame.Rect(self.collider_rect.topleft, (8*self.scale, 8*self.scale)),
            "l": pygame.Rect((self.collider_rect.left, self.collider_rect.centery-24*self.scale), (8*self.scale, 48*self.scale)),
            "bl": pygame.Rect((self.collider_rect.left, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "b": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.bottom-8*self.scale), (16*self.scale, 8*self.scale)),
            "br": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.bottom-8*self.scale), (8*self.scale, 8*self.scale)),
            "r": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.centery-24*self.scale), (8*self.scale, 48*self.scale)),
            "tr": pygame.Rect((self.collider_rect.right-8*self.scale, self.collider_rect.top), (8*self.scale, 8*self.scale)),
            "t": pygame.Rect((self.collider_rect.centerx-8*self.scale, self.collider_rect.top), (16*self.scale, 8*self.scale))
        }
        self.anim = am.ben_anim # make it compatible with all characters?


class NPC(Character):
    def __init__(self, anim: dict[str, dict[str, list[pygame.Surface]]], pos: tuple[float, float], name: str = "John Doe", prompts: list[list[InteractionPrompt]] = []) -> None:
        super().__init__(anim, pos)
        self.name = name
        self.name_tag = am.normal_font[14 if len(name)>12 else 16].render(name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        
        self.interaction_radius = 120
        self.can_interact = False
        self.uninteracting = False
        
        self.prompt_index: int = 0
        self.level: int = 0 # which sequence of prompts to show
        if prompts == []:
            self.prompts: list[list[InteractionPrompt]] = [[InteractionPrompt(f"{self.name}: Hello there! ..."), OptionsPrompt("What will you do?", Options([("Leave", self.uninteract)]))]]
        else:
            self.prompts = prompts
    
    def check_interact(self, player_pos) -> bool:
        if self.can_interact:
            # interaction prompt
            x, y = player_pos[0]-self.unscaled_pos[0], player_pos[1]-self.unscaled_pos[1]
            if x**2 + y**2 > self.interaction_radius**2:
                self.can_interact = False
            if abs(x) > abs(y):
                self.anim_dir = "a" if x < 0 else "d"
            else:
                self.anim_dir = "w" if y < 0 else "s"
        else:
            x, y = player_pos[0]-self.unscaled_pos[0], player_pos[1]-self.unscaled_pos[1]
            if x**2 + y**2 <= self.interaction_radius**2:
                self.can_interact = True
                print(f"{self.name} says: Hi bud!")
        return self.can_interact
    
    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, debug_circle: bool = False) -> None:
        rel_pos = super().draw(screen, cam_pos, tick)
        screen.blit(self.name_tag, (rel_pos[0]+self.rect.width/2-self.name_tag_rect.width/2, rel_pos[1]-self.name_tag_rect.height/2))
        if debug_circle: pygame.draw.circle(screen, 0xFFFFFF, (rel_pos[0]+self.rect.size[0]/2, rel_pos[1]+self.rect.size[1]/2), self.interaction_radius*self.scale, 1)
        return None
    
    def interact(self) -> bool:
        """ returns whether the interactable character wants to uninteract """
        overlay.gui.show_prompt = True
        overlay.gui.prompt = self.prompts[self.level][self.prompt_index]
        overlay.gui.update_scale(self.scale)
        if self.uninteracting:
            self.uninteracting = False
            return True
        return False
    
    def uninteract(self) -> None:
        self.uninteracting = True
        self.prompt_index = 0
        return None
    
    def next_dialogue(self) -> bool:
        self.prompt_index += 1
        if self.prompt_index >= len(self.prompts[self.level]):
            self.prompt_index = 0
            self.uninteract()
            return False
        else:
            return True

    def update_scale(self, scale: float, new_anim=None) -> None:
        super().update_scale(scale, new_anim)
        self.name_tag = am.normal_font[14 if len(self.name)>12 else 16].render(self.name, True, 0xFFFFFFFF)
        self.name_tag_rect = self.name_tag.get_rect()
        return None