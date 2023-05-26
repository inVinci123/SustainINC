import pygame

class Camera:
    """ Not a literal camera, just a structure to manage the player perspective of the scene """
    def __init__(self, game_scale, unscaled_player_pos=(0,0)) -> None:
        self.game_scale = game_scale

        self.unscaled_cam_pos = (unscaled_player_pos[0]-640+32, unscaled_player_pos[1]-360+32)#unscaled_player_pos
        self.cam_pos = (self.unscaled_cam_pos[0]*game_scale, self.unscaled_cam_pos[1]*game_scale) # set this to the TOPLEFT of the screen, callibrate everything else accordingly

        self.movebox_lim: tuple[float, float] = (320*game_scale, 180*game_scale)
        self.unscaled_movebox_pos = (0, 0)
        self.movebox_pos = (0, 0)
        return None
    

    def update_movebox(self, x:float=0, y:float=0) -> None:
        self.unscaled_movebox_pos = self.unscaled_movebox_pos[0]+x, self.unscaled_movebox_pos[1]+y
        self.movebox_pos = self.unscaled_movebox_pos[0]*self.game_scale, self.unscaled_movebox_pos[1]*self.game_scale
        
        x_off, y_off = 0, 0
        if abs(self.movebox_pos[0]) > abs(self.movebox_lim[0]):
            dir = self.movebox_pos[0]/abs(self.movebox_pos[0])
            x_off = dir*(abs(self.movebox_pos[0])-self.movebox_lim[0])
            self.movebox_pos = dir*self.movebox_lim[0], self.movebox_pos[1]
        if abs(self.movebox_pos[1]) > abs(self.movebox_lim[1]):
            dir = self.movebox_pos[1]/abs(self.movebox_pos[1])
            y_off = dir*(abs(self.movebox_pos[1])-self.movebox_lim[1])
            self.movebox_pos = self.movebox_pos[0], dir*self.movebox_lim[1]
        self.unscaled_movebox_pos = self.movebox_pos[0]/self.game_scale, self.movebox_pos[1]/self.game_scale
        self.update_cam_pos(x_off/self.game_scale, y_off/self.game_scale)
        return None


    def update_cam_pos(self, x:float=0, y:float=0, game_scale = None) -> None:
        if not game_scale:
            game_scale = self.game_scale
        self.unscaled_cam_pos = self.unscaled_cam_pos[0]+x, self.unscaled_cam_pos[1]+y
        self.cam_pos = (self.unscaled_cam_pos[0]*game_scale, self.unscaled_cam_pos[1]*game_scale)
        return None
    

    def rescale(self, game_scale):
        self.game_scale = game_scale
        self.update_cam_pos()
        self.movebox_lim = (320*game_scale, 180*game_scale)
        self.update_movebox(0, 0)