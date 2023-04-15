import pygame

class Camera:
    """ Not a literal camera, just a structure to manage the player perspective of the scene """
    def __init__(self, game_scale) -> None:
        self.game_scale = game_scale

        self.unscaled_cam_pos = (0, 0)
        self.cam_pos = (self.unscaled_cam_pos[0]*game_scale, self.unscaled_cam_pos[1]*game_scale) # set this to the centre of the screen, callibrate everything else accordingly

        self.move_box_lim: tuple[float, float] = (128*game_scale, 72*game_scale)
        self.move_box_pos = (0, 0)
        return None
    

    def update_move_box(self, x:float=0, y:float=0) -> None:
        self.move_box_pos = self.move_box_pos[0]+(x*self.game_scale), self.move_box_pos[1]+(y*self.game_scale)
        
        x_off, y_off = 0, 0
        if abs(self.move_box_pos[0]) > abs(self.move_box_lim[0]):
            dir = self.move_box_pos[0]/abs(self.move_box_pos[0])
            x_off = dir*(abs(self.move_box_pos[0])-self.move_box_lim[0])
            self.move_box_pos = dir*self.move_box_lim[0], self.move_box_pos[1]
        if abs(self.move_box_pos[1]) > abs(self.move_box_lim[1]):
            dir = self.move_box_pos[1]/abs(self.move_box_pos[1])
            y_off = dir*(abs(self.move_box_pos[1])-self.move_box_lim[1])
            self.move_box_pos = self.move_box_pos[0], dir*self.move_box_lim[1]
        print("x_off", x_off, "y_off", y_off)
        self.update_cam_pos(x_off, y_off)
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
        self.move_box_lim = (128*game_scale, 72*game_scale)
        self.move_box_pos = self.move_box_pos[0]*game_scale, self.move_box_pos[1]*game_scale