import pygame

from Scripts.Tiles import GrassTile
from Scripts.Camera import Camera
from Scripts.Character import Player, NPC
import Scripts.AssetManager as am


class GameManager:
    def __init__(self, game_scale: float, debugging: bool = False) -> None:

        am.load_assets(game_scale)

        self.debugging: bool = debugging
        self.game_scale = game_scale
        self.ben_anim: dict = am.ben_anim
        self.test_character = NPC(self.ben_anim, (5*120, 3*120), "Joe Doe")
        self.test_character.update_scale(game_scale)

        self.anim_dir = "s"

        self.cam = Camera(game_scale)

        self.movement_enabled: bool = True
        self.walking = False
        self.speed = 200
        self.player = Player((1280/2*game_scale + 32, 720/2*game_scale))
        self.player.update_scale(game_scale)

        self.last_move: tuple[float, float] = (0, 0)

        self.grass_tiles: list[GrassTile] = []
        for i in range(-100, 100): # I'm crazy enough to render 4000 blocks for testing
            for j in range(-10, 10):
                g = GrassTile((i*255, j*255))
                self.grass_tiles.append(g)
                g.update_scale(game_scale)
        
        return None
    
    def evaluate_game_screen(self, deltatime: float = 1) -> None: # better name --> evaluate game? manage game processes?
        # change the player position if the player is walking
        if self.walking:
            if self.anim_dir == "w":
                self.player.move(0, -self.speed*deltatime, self.anim_dir)
                self.last_move = (0, -self.speed*deltatime)
                self.cam.update_movebox(0, -self.speed*deltatime)
            if self.anim_dir == "s":
                self.player.move(0, self.speed*deltatime, self.anim_dir)
                self.last_move = (0, self.speed*deltatime)
                self.cam.update_movebox(0, self.speed*deltatime)
            if self.anim_dir == "a":
                self.player.move(-self.speed*deltatime, 0, self.anim_dir)
                self.last_move = (-self.speed*deltatime, 0)
                self.cam.update_movebox(-self.speed*deltatime, 0)
            if self.anim_dir == "d":
                self.player.move(self.speed*deltatime, 0, self.anim_dir)
                self.last_move = (self.speed*deltatime, 0)
                self.cam.update_movebox(self.speed*deltatime, 0)
        self.test_character.check_interact(self.player.unscaled_pos)
        
        # check for collisions
        if self.check_collisions():
            self.player.move(-self.last_move[0]*1.2, -self.last_move[1]*1.2)
            self.cam.update_movebox(-self.last_move[0]*1.2, -self.last_move[1]*1.2)
        return None
    

    def check_collisions(self) -> bool:
        # when you get multiple things to check, use player.rect.collidelist/collidedict
        # ISSUE: the rect for some reason are drawn on the top left of the screen?
        if self.player.collider_rect.colliderect(self.test_character.collider_rect):
            return True
        # check if the player is colliding, if so invert the velocity and multiply it by 1.5 to ensure the player cannot force their way in. return ok if all is ok else return not ok :)
        return False

    def resize(self, game_scale) -> None:
        self.game_scale = game_scale
        am.load_assets(game_scale)
        ben_anim = am.ben_anim
        
        self.test_character.update_scale(game_scale, ben_anim)
        self.player.update_scale(game_scale, ben_anim)
        for tile in self.grass_tiles:
            tile.update_scale(game_scale)
        self.cam.rescale(game_scale)

        return None