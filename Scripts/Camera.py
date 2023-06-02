import pygame

class Camera:
    """ Not an actual scene camera, just a structure to manage what everything else should be rendered relative to. """
    def __init__(self, game_scale, unscaled_player_pos=(0,0)) -> None:
        self.game_scale = game_scale

        # set the position such that the player is exactly at the centre of the screen
        self.unscaled_cam_pos = (unscaled_player_pos[0]-640+32, unscaled_player_pos[1]-360+32)
        self.cam_pos = (self.unscaled_cam_pos[0]*game_scale, self.unscaled_cam_pos[1]*game_scale) # scaled and set to the TOP-LEFT of the screen

        self.movebox_lim: tuple[float, float] = (180*game_scale, 180*game_scale) # a square box where the player can move aroud without scene scrolling
        
        # positions of the player in the movebox
        self.unscaled_movebox_pos = (0, 0)
        self.movebox_pos = (0, 0)
        return None
    
    def update_movebox(self, x:float=0, y:float=0) -> None:
        """ update the player's position in the movebox and check if scene scrolling is necessary """
        # update the player's position in the movebox accordingly
        self.unscaled_movebox_pos = self.unscaled_movebox_pos[0]+x, self.unscaled_movebox_pos[1]+y
        self.movebox_pos = self.unscaled_movebox_pos[0]*self.game_scale, self.unscaled_movebox_pos[1]*self.game_scale
        
        x_off, y_off = 0, 0
        # check if horizontal pos exceeds the limits
        if abs(self.movebox_pos[0]) > abs(self.movebox_lim[0]):
            # generate an offset accordingly in the horizontal direction
            dir = self.movebox_pos[0]/abs(self.movebox_pos[0])
            x_off = dir*(abs(self.movebox_pos[0])-self.movebox_lim[0])
            self.movebox_pos = dir*self.movebox_lim[0], self.movebox_pos[1] # put the player back on the edge of the move box
        # check if vertical pos exceeds the limits
        if abs(self.movebox_pos[1]) > abs(self.movebox_lim[1]):
            # generate an offset accordingly in the vertical direction
            dir = self.movebox_pos[1]/abs(self.movebox_pos[1])
            y_off = dir*(abs(self.movebox_pos[1])-self.movebox_lim[1])
            self.movebox_pos = self.movebox_pos[0], dir*self.movebox_lim[1] # put the player back on the edge of the move box
        
        # update the unscaled movebox position too (based on the scaled changes that occured above)
        self.unscaled_movebox_pos = self.movebox_pos[0]/self.game_scale, self.movebox_pos[1]/self.game_scale
        self.update_cam_pos(x_off/self.game_scale, y_off/self.game_scale) # with the offsets generated (adjusted to the scale), move the camera (everything else is rendered relative to the camera so this will effectively scroll the scene)
        return None

    def update_cam_pos(self, x:float=0, y:float=0, game_scale = None) -> None:
        """ Update the position of the "camera". Everything else is rendered relative to this, so it effectively scrolls the screen. """
        if not game_scale: # check if the scale has been updated (no longer required)
            game_scale = self.game_scale
        # update the unscaled and scaled camera positions accordingly
        self.unscaled_cam_pos = self.unscaled_cam_pos[0]+x, self.unscaled_cam_pos[1]+y
        self.cam_pos = (self.unscaled_cam_pos[0]*game_scale, self.unscaled_cam_pos[1]*game_scale)
        return None
    
    def rescale(self, game_scale) -> None:
        """ Update the game scale for the camera. """
        self.game_scale = game_scale
        self.update_cam_pos() # adjust the camera according to the new scale
        self.movebox_lim = (180*game_scale, 180*game_scale) # rescale the move box limits
        self.update_movebox(0, 0) # adjust the player's position in the movebox to the new scale
        return None