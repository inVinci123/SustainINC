import pygame
import Scripts.AssetManager as am

class GalletCity:
    """ Structure to hold the bg city image and easily update it's scale """
    def __init__(self) -> None:
        self.image = am.gallet_city
        self.unscaled_pos = (-2560, -2560) # the image is 512/512 scaled 10x. By rendering it at that position, the centre of the map can be at (0, 0)
        self.scale = 1
        self.scaled_pos = self.unscaled_pos
        return None
    
    def draw(self, screen: pygame.Surface, cam_pos: tuple[float, float]) -> None:
        """ draw the map relative to the camera """
        rel_pos: tuple[float, float] = (self.scaled_pos[0]-cam_pos[0], self.scaled_pos[1]-cam_pos[1])
        screen.blit(self.image, rel_pos)
        return None

    def update_scale(self, scale) -> None:
        """ adjust the scale to the position and the size """
        self.scale = scale
        self.image = am.gallet_city
        self.scaled_pos = (self.unscaled_pos[0]*self.scale, self.unscaled_pos[1]*self.scale)
        return None