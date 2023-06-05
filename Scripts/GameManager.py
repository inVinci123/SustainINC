import pygame
import os

from Scripts.Camera import Camera
from Scripts.Character import Character, Player, NPC
from Scripts.GameCharacters import SaharaEmployee, BuffJesos, GraterThunderberg, MelonUsk, MrDani, MrFeast, MrGutters, inV
from Scripts.Building import Building, Collider, SustainINC
import Scripts.AssetManager as am
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt
import Scripts.OverlayGUI as overlay


class GameManager:
    """ Manages the game processes, records in-game events, handles game evaluation, etc. """
    def __init__(self, game_scale) -> None:
        """ load the assets before the game is started """
        am.load_assets(game_scale)
        return None
    
    def post_init(self, game_scale: float, debugging: bool = False, player_name: str = "Player", end_game= lambda *kwargs: None) -> None:
        """ post constructor executed from main.py when the game actually starts """
        am.load_assets(game_scale)

        # a dictionary of global variables/flags keeping track of whether in game events have occurred or not
        # since it's mutable, it will be passed by reference to every NPC
        self.flags: dict[str, bool|int|object] = {
            "firstmeloninteraction": False,
            "secondmeloninteraction": False,
            "sustainlevel": 0,
            "thunderbergreference": False,
            "spendresources": self.spend_resources,
            "getresources": self.get_resources,
            "donatetoun": False,
            "investmentlevel": 0,
            "buffreference": False,
            "globaltemperatureunlocked": False,
            "unlockglobaltemperature": self.unlock_global_temperature,
            "danireference": False,
            "daniconvinced": False,
            "spaceyacquired": False,
            "saharaacquired": False,
            "finishgame": self.finish_game,
            "carboncontribution": 500,
            "hascar": False
        }

        self.end_game = end_game # function to end the game

        self.debugging: bool = debugging
        self.game_scale = game_scale
        
        # building kept as a standalone mutable object
        self.sustain = SustainINC(self, self.flags)
        
        self.character_dict: dict[str, NPC] = { # dictionary for the non playable characters
            "Melon Usk": MelonUsk(player_name, self.flags),
            "Grater Thunderberg": GraterThunderberg(player_name, self.flags),
            "Mr Gutters": MrGutters(player_name, self.flags),
            "Mr Dani": MrDani(player_name, self.flags),
            "Sahara Employee #1": SaharaEmployee(player_name, self.flags, (1700, 2150)),
            "Sahara Employee #2": SaharaEmployee(player_name, self.flags, (2200, 2150)),
            "Buff Jesos": BuffJesos(player_name, self.flags),
            "Mr Feast": MrFeast(player_name, self.flags),
            "inV": inV(player_name, self.flags)
        }
        self.character_list: list[NPC] = [item for _, item in self.character_dict.items()] # class objects are mutable, so this is efficient to do and helps iterate over things faster

        self.building_dict: dict[str, Building] = { # a dictionary for all the buildings (made with the intention to expand the number of buildings in the game)
            "Sustain INC": self.sustain
        }
        self.building_list: list[Building] = [b for _, b in self.building_dict.items()]

        self.colliders: list[Collider] = [] # colliders laid over the bg city

        for col in am.colliders: # load the colliders from the asset manager
            a = Collider((col["xpos"], col["ypos"]), (col["xsiz"], col["ysiz"]))
            self.colliders.append(a)
            a.update_scale(self.game_scale)
        
        self.extra_colliders = [ # Extra colliders used until the Player talks to Melon Usk
            Collider((-520, 2280), (80, 250)),
            Collider((0, 2300), (120, 250))
        ]
        for c in self.extra_colliders:
            c.update_scale(self.game_scale)

        self.interactables: list[SustainINC | NPC] = self.character_list + [self.sustain] # combined list to check to check for interactions

        # update the characters and buildings with the game scale just in case
        for c in self.character_list:
            c.update_scale(game_scale)
        for b in self.building_list:
            b.update_scale(game_scale)

        # player movement variables
        self.anim_dir = "s"
        self.move_dir: tuple[int, int] = (0, 0)
        self.movement_enabled: bool = True
        self.walking = False
        self.normal_speed = 280
        self.fast_speed = 2800 if debugging else 600
        self.speed = 280

        self.cam = Camera(game_scale, (-365, 2330))

        # create the player itself
        self.player = Player((-365, 2330))
        self.player.name = player_name
        self.player.update_scale(game_scale)

        # the stuff on the top left
        self.resources: float = 0
        self.global_temp: float = 0

        # collision cooldown to pause collisions for 2 frames after the scale is updated (done to avoid a bug)
        self.collision_cooldown: int = 2
        self.player_interacting: bool = False
        
        self.collided_last_frame: bool = False # whether the player collided last frame
        
        overlay.gui.show_hint = True # show the hint about what to do first (TALK TO MELON USK)
        return None
    
    def spend_resources(self, amount) -> bool:
        """ for the player to spend resources """
        if amount < self.resources:
            self.resources -= amount
            return True
        else:
            return False
    
    def get_resources(self) -> float:
        """ for the NPCs to check how much the player has before allowing the conduct of the transaction """
        return self.resources

    def unlock_global_temperature(self) -> None:
        """ triggered when the the player first interacts with Mr Gutters """
        self.flags["globaltemperatureunlocked"] = True
        overlay.gui.show_global_temp = True
        overlay.gui.update_global_temp(0.9)

    def evaluate_game_screen(self, deltatime: float = 1, debugging = False) -> None:
        """ evaluate the game screen by moving the player, processing collisions, etc. Some of the actions need to know the deltatime: how much time has passed since the last frame """
        # evaluate the player animation direction (vertical takes priority, even when moving diagonally)
        if not self.movement_enabled:
            self.walking = False
        if self.move_dir[1] == 1:
            self.anim_dir = "s"
        elif self.move_dir[1] == -1:
            self.anim_dir = "w"
        elif self.move_dir[0] == 1:
            self.anim_dir = "d"
        elif self.move_dir[0] == -1:
            self.anim_dir = "a"

        s = self.speed if not self.collided_last_frame else self.normal_speed # if the player collided last frame, slow down
        self.collided_last_frame = False # reset the previous frame's collision boolean

        if self.walking:
            if self.move_dir[0] != 0 and self.move_dir[1] != 0: # if the player is moving diagonally, the speed on both axis should be divided by root 2 (to maintain a constant linear speed)
                self.player.move(self.move_dir[0]*s*deltatime/(2**0.5), self.move_dir[1]*s*deltatime/(2**0.5), self.anim_dir)
                self.cam.update_movebox(self.move_dir[0]*s*deltatime/(2**0.5), self.move_dir[1]*s*deltatime/(2**0.5))
            else: # else move as normal
                self.player.move(self.move_dir[0]*s*deltatime, self.move_dir[1]*s*deltatime, self.anim_dir)
                self.cam.update_movebox(self.move_dir[0]*s*deltatime, self.move_dir[1]*s*deltatime)

        # evaluate interactions
        interacting: bool = False
        for interactable in self.interactables:
            # check if the interactable is in frame
            if type(interactable) == SustainINC:
                check_lims = (700+interactable.unscaled_size[0], 400+interactable.unscaled_size[1]) # consider the dimensions of the building
            else:
                check_lims = (700, 400)
            if abs(self.cam.unscaled_cam_pos[0]+640-interactable.unscaled_pos[0]) > check_lims[0] or abs(self.cam.unscaled_cam_pos[1]+360-interactable.unscaled_pos[1]) > check_lims[1]:
                interactable.inframe = False
                continue
            else:
                interactable.inframe = True
            # give the player position in a different way to the Building (to consider the centre of the player)
            pos = (self.player.unscaled_pos[0] + 32, self.player.unscaled_pos[1] + 32) if type(interactable) == SustainINC else self.player.unscaled_pos
            if interactable.check_interact(pos): # allow the player to interact with this character/building
                self.player.can_interact = True
                interacting = True
                self.player.interaction_character = interactable
        else: # at the end of the loop, dissallow interaction if no interactable is found within the interaction range
            if not interacting:
                self.player.can_interact = False
                self.player.interaction_character = None

        for b in self.building_list: # check if other buildings are in frame too (deprecated)
            if abs(self.cam.unscaled_cam_pos[0]+640-b.unscaled_pos[0]) > 700+b.unscaled_size[0] or abs(self.cam.unscaled_cam_pos[1]+360-b.unscaled_pos[1]) > 400+b.unscaled_size[1]: b.inframe = False
            else: b.inframe = True

        if self.player_interacting: # process interaction logic if the player is interacting 
            if not self.player.interaction_character == None:
                if self.player.interaction_character.interact():
                        self.player_interacting = False
                        self.movement_enabled = True

        # check for collisions and adjust the player position accordingly
        x, y = self.check_collisions()
        if abs(x) > 1*self.game_scale or abs(y) > 1*self.game_scale:
            self.collided_last_frame = True
        self.player.move(x, y)
        self.cam.update_movebox(x, y)
        
        # update the resources
        if self.debugging: self.resources += 5*self.sustain.cost*deltatime
        else: self.resources += self.sustain.income*deltatime # type: ignore
        overlay.gui.update_resources(self.resources)
        
        # update the global temperature if it has been unlocked
        if self.flags["globaltemperatureunlocked"]:
            self.global_temp += self.get_delta_temp(deltatime) # type: ignore
        if self.global_temp >= 1.5:
            self.end_game(0)
        overlay.gui.update_global_temp(self.global_temp)
        return None
    
    def get_delta_temp(self, deltatime) -> float:
        """ Return how much to change the temperature by for the given time in seconds """
        return max(0, self.flags["carboncontribution"]*deltatime/(600*2/3*500))

    def check_collisions(self) -> tuple[float, float]:
        """ process collisions using the player's 8 collider system """
        if self.collision_cooldown > 0: # if the game was rescaled, don't do anything
            self.collision_cooldown -= 1
            return (0, 0)
        elif self.collision_cooldown == 0: # once the game has reached the end of the cooldown, allow collisions and movement
            self.collision_cooldown = -1
            if not self.player_interacting:
                self.movement_enabled = True
        
        if self.flags["firstmeloninteraction"]: # check the extra colliders if the player hasn't met Melon Usk yet 
            checkrects = [c.collider_rect for c in self.character_list] + [c.col_rect for c in self.colliders] # not checking for building colliders as they interfere with the normal colliders
        else:
            checkrects = [c.collider_rect for c in self.character_list] + [c.col_rect for c in self.colliders+self.extra_colliders]
            
        col_list = self.player.collider_rect.collidelistall(checkrects) # indices of all colliders that are touching the player
        if len(col_list) == 0:
            return (0, 0)
        
        return_vals: list[tuple[float, float]] = []
        for i in col_list: # for each collider touching the player
            col_rect = checkrects[i]
            # check edge collisions and correct them accordingly (hierarchy starting from left)
            if self.player.col['l'].colliderect(col_rect):  # left
                return_vals.append(((col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx)), 0))
            elif self.player.col['r'].colliderect(col_rect):  # right
                return_vals.append((((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2), 0))
            elif self.player.col['t'].colliderect(col_rect):  # top
                return_vals.append((0, (col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))))
            elif self.player.col['b'].colliderect(col_rect):  # bottom
                return_vals.append((0, ((col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)))

            # else check corner collisions and correct them accordingly
            elif self.player.col['tl'].colliderect(col_rect):  # top left
                return_vals.append(((col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx)), (col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))))
            elif self.player.col['bl'].colliderect(col_rect):  # bottom left
                return_vals.append(((col_rect.width/2 - (self.player.col["l"].left - col_rect.centerx)), ((col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)))
            elif self.player.col['br'].colliderect(col_rect):  # bottom right
                return_vals.append((((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2), ((col_rect.centery - self.player.col["b"].bottom) - col_rect.height/2)))
            elif self.player.col['tr'].colliderect(col_rect):  # top right
                return_vals.append((((col_rect.centerx - self.player.col["r"].right) - col_rect.width/2), (col_rect.height/2 - (self.player.col["t"].top - col_rect.centery))))

        return_val = (0, 0)
        for rv in return_vals: # sum all the return values to see what the final correction value should be
            return_val = (return_val[0]+rv[0], return_val[1]+rv[1])
        return return_val
    
    def finish_game(self) -> None:
        """ Win the game with a score based on how close the global temp was to 1.5 degrees """
        self.end_game((1.5-self.global_temp)*20000+1000)
        return None

    def resize(self, game_scale) -> None:
        """ Adjust the everything based on the new scale """
        self.movement_enabled = False # need to disable movement and collisions for the next two frames
        self.collision_cooldown = 2
        self.game_scale = game_scale
        am.load_assets(game_scale)
        
        # assign the relevant anim to each character and update their scale
        self.player.update_scale(game_scale, am.ben_anim)
        self.character_dict["Melon Usk"].update_scale(game_scale, am.melon_anim)
        self.character_dict["Grater Thunderberg"].update_scale(game_scale, am.grater_anim)
        self.character_dict["Mr Gutters"].update_scale(game_scale, am.gutters_anim)
        self.character_dict["Mr Dani"].update_scale(game_scale, am.dani_anim)
        self.character_dict["Sahara Employee #1"].update_scale(game_scale, am.sahara_anim)
        self.character_dict["Sahara Employee #2"].update_scale(game_scale, am.sahara_anim)
        self.character_dict["Buff Jesos"].update_scale(game_scale, am.jesos_anim)
        self.character_dict["Mr Feast"].update_scale(game_scale, am.feast_anim)
        self.character_dict["inV"].update_scale(game_scale, am.inv_anim)
        
        for c in (self.colliders+self.extra_colliders): # update the colliders
            c.update_scale(game_scale)

        for b in self.building_list: # update the buildings
            b.update_scale(game_scale)

        self.cam.rescale(game_scale) # update the camera position

        return None
