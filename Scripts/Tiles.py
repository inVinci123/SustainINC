import pygame

import Scripts.AssetManager as am

class GrassTile:
    def __init__(self, pos: tuple[float, float], size: tuple[float, float] = (0, 0)) -> None:
        self.unscaled_pos: tuple[float, float] = pos
        self.scale: float = 1
        self.scaled_pos: tuple[float, float] = pos

        self.size: tuple[float, float] = size
        self.tile: pygame.Surface = am.grass_tile
    
    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float], tick: int=0) -> None:
        relative_pos = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        screen.blit(self.tile, relative_pos)
        return None

    def update_scale(self, scale: float) -> None:
        self.scale = scale
        self.scaled_pos = (self.unscaled_pos[0]*scale, self.unscaled_pos[1]*scale)
        self.tile = am.grass_tile
        return None