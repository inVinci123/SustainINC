import pygame
import sigfig

from Scripts.ScreenElements import InteractionPrompt, Text
import Scripts.AssetManager as am

def format_value(val: float) -> str:
    """
    Convert the value into a "money" format
    """
    a: str = sigfig.round(f"{int(val)}", decimals=3, notation="eng") # engineering notation is convenient to use as it only deals with powers of multiple of 3
    i = a.find('E') # index of where th exponent is
    exp = int(a[i+1:])
    end: str = '' # string ending

    # check which suffix should be applied based on the exponent
    if exp >= 36: return "Kedar level money"
    elif exp >= 33: end = " Dc"
    elif exp >= 30: end = " Nn"
    elif exp >= 27: end = " Ot"
    elif exp >= 24: end = " St"
    elif exp >= 21: end = " Sx"
    elif exp >= 18: end = " Qi"
    elif exp >= 15: end = ' Qu'
    elif exp >= 12: end = ' T'
    elif exp >= 9: end = ' B'
    elif exp >= 6: end = ' M'
    elif exp >= 3: end = ' K'
    
    i = a.find('.') # render the relevant digits relative to where the decimal point is
    return a[:i] + a[i:i+3] +end

class OverlayGUI:
    """ Render the overlay GUI - what's being shown over the world """
    # interaction prompt stuff
    prompt = InteractionPrompt()
    show_prompt: bool = False

    # resources stuff
    resources_bg = pygame.Surface((280, 30))
    resources_bg.fill(0x121212)
    resources_bg.set_alpha(180)

    # temperature stuff
    show_global_temp: bool = False
    temperature_bg = pygame.Surface((280, 30))
    temperature_bg.fill(0x121212)
    temperature_bg.set_alpha(180)

    try: # this won't work if assets haven't been loaded, so the exception is ignored and fixed when the scale is updated
        resources_text = Text(f"$ {format_value(0)}", (20, 11), (200, 20), am.normal_font[18], 0xFAFAFAFA)
        objectives_text = Text("Objectives", (10, 400), (250, 40), am.normal_font[24], 0xFAFAFAFA)
        global_temp_text = Text("Degrees away from destruction: 0", (20, 40), (200, 20), am.normal_font[18], 0xFAFAFAFA)
    except AttributeError:
        pass

    scale = 1

    notifications: list = []
    max_notifications: int = 5
    deleted_notification = None

    # objectives
    objectives: dict[str, str] = {}
    display_objectives: list[Text] = []
    objectives_bg: pygame.Surface = pygame.Surface((100, 100))

    # prev frames tuff (to render if the game is paused)
    prev_frame: bool = False
    prev_resources: float = 0
    prev_delta_temp: float = 0

    # map stuff
    show_map: bool = False
    characters: list = []
    name_tags: list = []

    # hint text (at the start telling the player to talk to Melon Usk) & map prompt (M to trigger map)
    show_hint: bool = False
    try:
        hint_text: Text = Text("Go to Melon Usk and press SPACE to talk to him", (0, 0), (200, 100), am.normal_font[24])
        map_prompt: pygame.Surface = am.normal_font[18].render("M to trigger Map", True, 0xFAFAFAFA)
        map_prompt_pos = (1200*scale - map_prompt.get_width(), 700*scale-map_prompt.get_height())
    except AttributeError:
        hint_text: Text
        map_prompt: pygame.Surface
    
    # map stuff
    try:
        map = pygame.transform.scale(am.gallet_city, (768, 768))
    except AttributeError:
        map: pygame.Surface
    map_bg = pygame.Surface((1280, 720))
    map_bg.fill(0x00000000)
    map_bg.set_alpha(200)
    try:
        map_text = am.normal_font[50].render("GAME MAP", True, 0xFFFFFFFF)
        map_text_pos = (640*scale-map_text.get_width()/2 , 60*scale)
    except AttributeError:
        pass

    def draw(self, screen: pygame.Surface, deltatime=1, paused: bool = False) -> None:
        """ draw the overlay GUI elements """
        if self.show_prompt: # prompt
            self.prompt.draw(screen)
            self.prev_frame = True # prompt on previous frame
        elif not paused:
            self.prev_frame = False # no prompt on previous frame
        else:
            if self.prev_frame: # if there was a prompt on previous frame before the game was paused, draw it
                self.prompt.draw(screen, False)

        if self.show_hint: # hint text telling the player to talk to MELON USK
            self.hint_text.draw(screen)

        if not paused:
            # render the in game overlay menu
            self.show_prompt = False
            if self.show_map: # if the map is triggered, overlay the map
                screen.blit(self.map_bg, (0, 0))
                screen.blit(self.map_text, self.map_text_pos)
                for tag in self.name_tags: # blit the name tags of all game characters on the map
                    self.map.blit(tag[0], tag[1])
                screen.blit(self.map, (640*self.scale-384*self.scale, 360*self.scale-490*self.scale)) # draw the map 
            screen.blit(self.map_prompt, self.map_prompt_pos) # map prompt (M to trigger Map)
        
        # draw the resources & temperature
        screen.blit(self.resources_bg, (10*self.scale, 10*self.scale)) 
        if self.show_global_temp: screen.blit(self.temperature_bg, (10*self.scale, 50*self.scale)) 
        try:
            self.resources_text.draw(screen)
            self.objectives_text.draw(screen)
            if self.show_global_temp: self.global_temp_text.draw(screen)
        except AttributeError:
            pass
        
        if self.deleted_notification != None: # check if a notification has been deleted
            self.notifications.pop(self.deleted_notification)
            self.refresh_notifications() # only refresh after everything has been rendered
        self.deleted_notification = None

        # render notifications        
        first_notif = True
        for i, n in enumerate(self.notifications):
            if i < self.max_notifications:
                if first_notif:
                    n.draw(screen, deltatime+0.04*len(self.notifications))
                    first_notif = False
                else:
                    n.draw(screen, deltatime)
            if n.deleted:
                self.deleted_notification = i # delete the notification before the next frame is rendered
        
        # render objectives
        screen.blit(self.objectives_bg, (10*self.scale, 100*self.scale))
        for obj in self.display_objectives:
            obj.draw(screen)
        return None

    def update_resources(self, val: float = 0) -> None:
        """ update resources with the new value """
        self.prev_resources = val
        self.resources_text = Text("$ " + format_value(val), (20*self.scale, 16*self.scale), (200*self.scale, 20*self.scale), am.normal_font[18], 0xFAFAFAFA)
        return None
    
    def update_global_temp(self, val: float = 0) -> None:
        """ update global temperature with the new value """
        self.prev_delta_temp = val
        value = str(val)[:4] if val < 1 else str(val)[:6] # if global temp exceeds 1 give more digits to create a sense of urgency
        self.global_temp_text = Text(f"Delta Temp: {value}", (20*self.scale, 56*self.scale), (300*self.scale, 20*self.scale), am.normal_font[18], 0xFAFAFAFA if val < 0.5 else (0xFFFF0000 if val < 1 else 0xFF000000))
        return None
    
    def add_objective(self, id: str, objective: str) -> None:
        """ add an objective to the dictionary of objectives """
        self.objectives[id] = objective
        self.refresh_objectives()
        return None
    
    def remove_objective(self, id: str) -> None:
        """ remove an objective from the dictionary of objectives """
        del self.objectives[id]
        self.refresh_objectives()
        return None
    
    def check_objective(self, id: str) -> bool:
        """ check if an objective exists in the dictionary of objectives """
        try:
            self.objectives[id]
            return True
        except KeyError:
            return False
    
    def refresh_objectives(self) -> None:
        """ refresh the display objectives with the objectives dictionary """
        self.display_objectives.clear() # clear the old objectives
        for i, (_, obj) in enumerate(self.objectives.items()): # add the new objectives
            self.display_objectives.append(Text(obj, (20*self.scale, (150+37*i)*self.scale), (260*self.scale, 35*self.scale), am.normal_font[18], 0xF9F9F9F9))
        
        # adjust the rest of the stuff based on the number of objectives and the scale
        self.objectives_bg = pygame.Surface((280*self.scale, (100+32*len(self.display_objectives))*self.scale))
        self.objectives_bg.fill(0x000000)
        self.objectives_bg.set_alpha(100)
        self.objectives_text = Text("Objectives", (20*self.scale, 120*self.scale), (650*self.scale, 40*self.scale), am.normal_font[24], 0xF9F9F9F9)
        return None
    
    def refresh_notifications(self) -> None:
        """ refresh the notifications """
        new = [] # new list of notifications
        for i, notif in enumerate(self.notifications): # add all the previous stuff callibrated to the new position & scale
            new.append(Notification(notif.text.text, (1000*self.scale, (10+55*i)*self.scale), self.scale, notif.type, notif.t))
        self.notifications = new
        return None
    
    def push_notification(self, msg: str, type = "default") -> None:
        """ push a notification on the screen (top right) """
        self.notifications.append(Notification(msg, (0, 0), self.scale, type))
        self.refresh_notifications()
        return None

    def update_scale(self, scale, characters=None) -> None:
        """ adjust the overlay gui according to the new scale """
        self.scale = scale

        # refresh notifications and objectives to adjust to the new scale
        self.refresh_notifications()
        self.refresh_objectives()

        # update the resources and global temp to adjust to the new scale
        self.update_global_temp(self.prev_delta_temp)
        self.temperature_bg = pygame.Surface((280*scale, 30*scale))
        self.temperature_bg.set_alpha(180)
        self.temperature_bg.fill(0x121212)
        self.update_resources(self.prev_resources)
        self.resources_bg = pygame.Surface((280*scale, 30*scale))
        self.resources_bg.set_alpha(180)
        self.resources_bg.fill(0x121212)

        self.prompt.update_scale(scale)

        # update the map and it's bg, prompt and text
        self.map_bg = pygame.Surface((1280*scale, 720*scale))
        self.map_bg.fill(0x00000000)
        self.map_bg.set_alpha(200)
        self.map = pygame.transform.scale(am.gallet_city, (768*scale, 768*scale))
        self.map_text = am.normal_font[50].render("GAME MAP", True, 0xFFFFFFFF)
        self.map_text_pos = (640*scale-self.map_text.get_width()/2 , 20*scale)
        self.map_prompt = am.normal_font[18].render("M to trigger Map", True, 0xFAFAFAFA)
        self.map_prompt_pos = (1250*self.scale - self.map_prompt.get_width(), 700*self.scale - self.map_prompt.get_height())

        self.hint_text = Text("Go to Melon Usk and press SPACE to talk to him", (250*scale, 590*scale), (740*scale, 100*scale), am.normal_font[24])

        # if the characters are provided, update the name tags according to the characters too
        if characters != None:
            self.characters = characters
        self.update_map_name_tags(scale)
        return None
    
    def update_map_name_tags(self, scale) -> None:
        """ create name tags for all characters (other than Sahara Employees) at their relative position on the map """
        self.name_tags.clear()
        for c in self.characters:
            if not c.name == "Sahara Employee":
                self.name_tags.append((am.normal_font[12].render(c.name, True, 0xFFFFFFFF, 0x006974FF if c.is_player else 0x00000000), ((c.unscaled_pos[0]+2560)*0.15*scale, (c.unscaled_pos[1]+2560)*0.15*scale)))
        return None
    
    def trigger_map(self) -> bool:
        """ Show or hide map, returning the new state """
        self.show_map = not self.show_map
        return self.show_map


class Notification:
    """ Blueprint for what a notification looks like """
    def __init__(self, text: str = "Hello World!", pos: tuple[float, float] = (0, 0), scale: float = 1, type: str = "default", remaining_time = 8) -> None:
        self.type = type # default, info or upgrade
        self.scaled_pos = pos
        self.bg = pygame.Surface((270*scale, 50*scale))

        # different colours for each notification type
        if type == "info":
            self.bg.fill(0x006994)
        elif type == "upgrade":
            self.bg.fill(0x802069)
        else:
            self.bg.fill(0x1A1A1A)
        self.bg.set_alpha(180)

        # notification text
        self.text = Text(text, (pos[0]+scale*10, pos[1]+scale*5), (250*scale, 40*scale), am.normal_font[18], 0xFAFAFAFA)
        self.t = remaining_time # how long till it's deleted
        self.deleted = False
        return None

    def draw(self, screen: pygame.Surface, deltatime) -> None:
        """ draw the notification """
        screen.blit(self.bg, self.scaled_pos)
        self.t -= deltatime
        if self.t <= 0: self.deleted = True # delete the notification if it's out of time
        self.text.draw(screen)
        return None

gui: OverlayGUI # accessible instance of the overlay class to all importing scripts that is initialised in the main.py