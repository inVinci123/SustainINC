import pygame
import Scripts.AssetManager as am


class Character:
    def __init__(self, anim: dict[str, list[pygame.Surface]], pos: tuple[float, float]) -> None:
        self.anim = anim
        self.anim_state = "idle"
        self.unscaled_pos: tuple[float, float] = pos
        self.scale: float = 1
        self.scaled_pos: tuple[float, float] = pos
        return None

    def move(self, x: int = 0, y: int = 0) -> None:
        self.unscaled_pos = self.unscaled_pos[0]+x, self.unscaled_pos[1]+y
        self.scaled_pos = self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale
        return None

    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int=0) -> None:
        relative_pos = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        screen.blit(self.anim["s"][self.anim_state][tick], relative_pos) # type: ignore
        return None

    def update_scale(self, scale: float, new_anim = None) -> None:
        self.scale = scale
        self.move() # to reset the character's scaled position
        if new_anim: self.anim = new_anim
        return None


class Player(Character):
    def __init__(self, pos: tuple[float, float]) -> None: # add an avatar, name argument?
        super().__init__(am.ben_anim, pos)
        self.anim_dir = "s"
        return None
    
    def move(self, x: int = 0, y: int = 0, anim_dir: str = "s") -> None:
        super().move(x, y)
        self.anim_dir = anim_dir
        return None
    
    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int = 0, walking: bool = False) -> None:
        self.anim_state = "walk" if walking else "idle"
        relative_pos = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        screen.blit(self.anim[self.anim_dir][self.anim_state][tick], relative_pos)
        return None

    def update_scale(self, scale: float, new_anim=None) -> None:
        super().update_scale(scale, new_anim)
        self.anim = am.ben_anim # make it compatible with all characters?
    