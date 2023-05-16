import pygame
import os

from Scripts.Tiles import GrassTile
from Scripts.Camera import Camera
from Scripts.Character import Character, Player, NPC
from Scripts.GameCharacters import GraterThunderberg, MelonUsk
from Scripts.Building import Building, SustainINC
import Scripts.AssetManager as am
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt
import Scripts.OverlayGUI as overlay


class GameManager:
    def __init__(self, game_scale: float, debugging: bool = False, player_name: str = "Ben the Brave") -> None:
        am.load_assets(game_scale)

        # a dictionary of "flags" keeping track of whether in game events have occured or not
        # since it's mutable, it will be passed by reference to every NPC
        self.flags: dict[str, bool|int|object] = {
            "firstmeloninteraction": False,
            "sustainlevel": 0,
            "thunderbergreference": False,
            "spendresources": self.spend_resources,
            "getresources": self.get_resources,
            "donatetoun": False,
            "investedinaslet": 0,
            "buffreference": False
        }

        self.debugging: bool = debugging
        self.game_scale = game_scale
        self.ben_anim: dict = am.ben_anim

        # self.test_character = NPC(self.ben_anim, (3*120, 3*120), "Joe Doe 1")#, [InteractionPrompt(
            #"Hello there, I'm John Doe!"), InteractionPrompt("Why you still talking to me, huh?"), OptionsPrompt("Leave or Stay?", Options(["Leave", self.test_character.uninteract]))])
        
        
        # need it to be standalone
        self.sustain = SustainINC(self, self.flags)
        
        self.character_dict: dict[str, NPC] = {
            "Melon Usk": MelonUsk(player_name, self.flags),
            "Grater Thunderberg": GraterThunderberg(player_name, self.flags)
        }
        self.character_list: list[NPC] = [item for _, item in self.character_dict.items()] # class objects are mutable, so this is efficient to do

        self.building_dict: dict[str, Building] = {
            "Test Building": Building("Test Building", (1000, 0)),
            "Sustain INC": self.sustain
        }
        self.building_list: list[Building] = [b for _, b in self.building_dict.items()]

        self.interactables: list[SustainINC | NPC] = self.character_list + [self.sustain]

        for c in self.character_list:
            c.update_scale(game_scale)
        for b in self.building_list:
            b.update_scale(game_scale)

        self.anim_dir = "s"

        self.cam = Camera(game_scale)

        self.movement_enabled: bool = True
        self.walking = False
        self.normal_speed = 280
        self.fast_speed = 2800
        self.speed = 280

        # self.player = Player(((1280/2-32), (720/2-32)))
        self.player = Player((0, 0))
        self.player.update_scale(game_scale)

        self.resources: float = 0

        # no collisions for 2 frames
        self.collision_cooldown: int = 2 
        self.player_interacting: bool = False

        self.grass_tiles: list[GrassTile] = []
        for i in range(-50, 50):  # 4000 blocks of grass as the underlayer
            for j in range(-10, 10):
                g = GrassTile((i*255, j*255))
                self.grass_tiles.append(g)
                g.update_scale(game_scale)

        return None
    
    def spend_resources(self, amount) -> bool:
        if amount < self.resources:
            self.resources -= amount
            return True
        else:
            return False
    
    def get_resources(self) -> float:
        return self.resources

    # better name --> evaluate game? manage game processes?
    def evaluate_game_screen(self, deltatime: float = 1) -> None:
        # change the player position if the player is walking
        if not self.movement_enabled:
            self.walking = False
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

        interacting: bool = False
        for interactable in self.interactables:
            # check if the interactable is in frame
            if type(interactable) == SustainINC:
                check_lims = (700+256, 400+256) # consider the dimensions of the building
            else:
                check_lims = (700, 400)
            if abs(self.cam.unscaled_cam_pos[0]+640-interactable.unscaled_pos[0]) > check_lims[0] or abs(self.cam.unscaled_cam_pos[1]+360-interactable.unscaled_pos[1]) > check_lims[1]:
                interactable.inframe = False
                continue
            else:
                interactable.inframe = True
            # evaluate the player position in a different way for the Building (to consider the centre of the player)
            pos = (self.player.unscaled_pos[0] + 32, self.player.unscaled_pos[1] + 32) if type(interactable) == SustainINC else self.player.unscaled_pos
            if interactable.check_interact(pos):
                self.player.can_interact = True
                interacting = True
                self.player.interaction_character = interactable
        else: # at the end of the loop
            if not interacting:
                self.player.can_interact = False
                self.player.interaction_character = None

        for b in self.building_list: # check if other buildings are in frame too
            if abs(self.cam.unscaled_cam_pos[0]+640-b.unscaled_pos[0]) > 700+256 or abs(self.cam.unscaled_cam_pos[1]+360-b.unscaled_pos[1]) > 400+256: b.inframe = False
            else: b.inframe = True

        for g in self.grass_tiles:
            if abs(self.cam.unscaled_cam_pos[0]+640-g.unscaled_pos[0]) > 900 or abs(self.cam.unscaled_cam_pos[1]+360-g.unscaled_pos[1]) > 620:
                g.inframe = False
            else:
                g.inframe = True

        if self.player_interacting:
            if not self.player.interaction_character == None:
                if self.player.interaction_character.interact():
                        self.player_interacting = False
                        self.movement_enabled = True

        # check for collisions and adjust the player
        x, y = self.check_collisions()
        self.player.move(x, y)
        self.cam.update_movebox(x, y)
        
        overlay.gui.update_resources(self.resources)
        if self.debugging: self.resources += 5*self.sustain.cost*deltatime
        else: self.resources += self.sustain.income*deltatime*(1+self.flags["investedinaslet"]*0.1) # type: ignore
        
        return None

    def check_collisions(self) -> tuple[float, float]:
        if self.collision_cooldown:
            self.collision_cooldown -= 1
            return (0, 0)
        checkrects = [c.collider_rect for c in self.character_list] + [b.col_rect for b in self.building_list]
        index = self.player.collider_rect.collidelist(checkrects)
        if index == -1: return (0, 0)

        col_rect = checkrects[index]

        # check edge collisions
        if self.player.col['l'].colliderect(col_rect):  # left
            return (col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx), 0)
        if self.player.col['r'].colliderect(col_rect):  # right
            return ((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2, 0)
        if self.player.col['t'].colliderect(col_rect):  # top
            return (0, col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))
        if self.player.col['b'].colliderect(col_rect):  # bottom
            return (0, (col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)

        # check corner collisions
        if self.player.col['tl'].colliderect(col_rect):  # top left
            return (col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx), col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))
        if self.player.col['bl'].colliderect(col_rect):  # bottom left
            return (col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx), (col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)
        if self.player.col['br'].colliderect(col_rect):  # bottom right
            return ((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2, (col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)
        if self.player.col['tr'].colliderect(col_rect):  # top right
            return ((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2, col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))

        return (0, 0)

    def resize(self, game_scale) -> None:
        self.game_scale = game_scale
        self.collision_cooldown = 2
        am.load_assets(game_scale)
        os.system("cls")
        ben_anim = am.ben_anim

        # print(f"Old: {self.player.unscaled_pos}")
        for c in self.character_list: # TODO: NEED TO CHANGE THIS TO MAKE IT WORK FOR EVERY INDIVIDUAL CHARACTER
            if c.name == "Grater Thunderberg":
                c.update_scale(game_scale, am.grater_anim)
            else:
                c.update_scale(game_scale, ben_anim)
        
        self.player.update_scale(game_scale, ben_anim)
        
        for b in self.building_list:
            b.update_scale(game_scale)

        for tile in self.grass_tiles:
            tile.update_scale(game_scale)
        self.cam.rescale(game_scale)

        return None
