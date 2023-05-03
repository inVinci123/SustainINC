import pygame, os

from Scripts.Tiles import GrassTile
from Scripts.Camera import Camera
from Scripts.Character import Player, NPC
import Scripts.AssetManager as am
from Scripts.ScreenElements import InteractionPrompt, OptionsPrompt


class GameManager:
    def __init__(self, game_scale: float, debugging: bool = False) -> None:
        am.load_assets(game_scale)

        self.debugging: bool = debugging
        self.game_scale = game_scale
        self.ben_anim: dict = am.ben_anim
        self.test_character = NPC(self.ben_anim, (3*120, 3*120), "Joe Doe 1", [InteractionPrompt("Hello there, I'm John Doe!"), InteractionPrompt("Why you still talking to me, huh?"), OptionsPrompt("Leave or Stay?")])
        self.test_character.update_scale(game_scale)
        self.test_character2 = NPC(self.ben_anim, (3*120, 5*120), "Joe Doe 2")
        self.test_character2.update_scale(game_scale)
        self.test_character3 = NPC(self.ben_anim, (7*120, 6*120), "Joe Doe 3")
        self.test_character3.update_scale(game_scale)

        self.anim_dir = "s"

        self.cam = Camera(game_scale)

        self.movement_enabled: bool = True
        self.walking = False
        self.normal_speed = 280
        self.fast_speed = 2800
        self.speed = 280

        self.player = Player((1280/2*game_scale + 32, 720/2*game_scale))
        self.player.update_scale(game_scale)

        self.collision_cooldown: bool = False # to ensure that no collisions occur right after scaling
        self.player_interacting: bool = False

        self.grass_tiles: list[GrassTile] = []
        for i in range(-100, 100): # 4000 blocks for testing
            for j in range(-10, 10):
                g = GrassTile((i*255, j*255))
                self.grass_tiles.append(g)
                g.update_scale(game_scale)
        
        return None
    
    def evaluate_game_screen(self, deltatime: float = 1) -> None: # better name --> evaluate game? manage game processes?
        # change the player position if the player is walking
        if not self.movement_enabled: self.walking = False
        if self.walking:
            if self.anim_dir == "w":
                self.player.move(0, -self.speed*deltatime, self.anim_dir)
                self.cam.update_movebox(0, -self.speed*deltatime)
            if self.anim_dir == "s":
                self.player.move(0, self.speed*deltatime, self.anim_dir)
                self.cam.update_movebox(0, self.speed*deltatime)
            if self.anim_dir == "a":
                self.player.move(-self.speed*deltatime, 0, self.anim_dir)
                self.cam.update_movebox(-self.speed*deltatime, 0)
            if self.anim_dir == "d":
                self.player.move(self.speed*deltatime, 0, self.anim_dir)
                self.cam.update_movebox(self.speed*deltatime, 0)

        if self.test_character.check_interact(self.player.unscaled_pos):
            self.player.can_interact = True
            self.player.interaction_character = self.test_character
        elif self.test_character2.check_interact(self.player.unscaled_pos):
            self.player.can_interact = True
            self.player.interaction_character = self.test_character2
        elif self.test_character3.check_interact(self.player.unscaled_pos):
            self.player.can_interact = True
            self.player.interaction_character = self.test_character3
        else:
            self.player.can_interact = False
            self.player.interaction_character = None
        
        if self.player_interacting:
            if self.player.interaction_character == None:
                print("oogabooga")
            else:
                # print(type(self.player.interaction_character))
                self.player.interaction_character.interact() # type: ignore

        # check for collisions
        x, y = self.check_collisions()
        self.player.move(x, y)
        self.cam.update_movebox(x, y)
        if not (x, y) == (0, 0): print("colliding")
        return None

    def check_collisions(self) -> tuple[float, float]:
        if self.collision_cooldown:
            self.collision_cooldown = False
            return (0, 0)
        checkrects = [self.test_character.collider_rect, self.test_character2.collider_rect, self.test_character3.collider_rect] # make it a class wide list
        index = self.player.collider_rect.collidelist(checkrects)
        if index == -1:
            return (0, 0)
        
        col_rect = checkrects[index]
        # check edge collisions
        if self.player.col['l'].colliderect(col_rect): # left
            return (col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx), 0)
        if self.player.col['r'].colliderect(col_rect): # right
            return ((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2, 0)
        if self.player.col['t'].colliderect(col_rect): # top
            return (0, col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))
        if self.player.col['b'].colliderect(col_rect): # bottom
            return (0, (col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)

        # check corner collisions
        if self.player.col['tl'].colliderect(col_rect): # top left
            return (col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx), col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))
        if self.player.col['bl'].colliderect(col_rect): # bottom left
            return (col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx), (col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)
        if self.player.col['br'].colliderect(col_rect): # bottom right
            return ((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2, (col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)
        if self.player.col['tr'].colliderect(col_rect): # top right
            return ((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2, col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))

        return (0, 0)


    def resize(self, game_scale) -> None:
        self.game_scale = game_scale
        self.collision_cooldown = True
        am.load_assets(game_scale)
        os.system("cls")
        ben_anim = am.ben_anim
        
        print(f"Old: {self.player.unscaled_pos}")
        self.test_character.update_scale(game_scale, ben_anim)
        self.test_character2.update_scale(game_scale, ben_anim)
        self.test_character3.update_scale(game_scale, ben_anim)
        self.player.update_scale(game_scale, ben_anim)
        for tile in self.grass_tiles:
            tile.update_scale(game_scale)
        self.cam.rescale(game_scale)

        return None