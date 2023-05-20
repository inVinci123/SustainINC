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
    prompt = InteractionPrompt()
    show_prompt: bool = True
    resources_bg = pygame.Surface((280, 30))
    resources_bg.fill(0x121212)
    resources_bg.set_alpha(180)

    temperature_bg = pygame.Surface((280, 30))
    temperature_bg.fill(0x121212)
    temperature_bg.set_alpha(180)
    try:
        resources_text = Text(f"$ {format_value(0)}", (20, 11), (200, 20), am.normal_font[18], 0xFAFAFAFA)
        objectives_text: Text = Text("Objectives", (10, 400), (250, 40), am.normal_font[24], 0xFAFAFAFA)
        global_temp_text = Text("Degrees away from destruction: 0", (20, 40), (200, 20), am.normal_font[18], 0xFAFAFAFA)
    except AttributeError:
        pass

    scale = 1

    notifications: list = []
    max_notifications: int = 5

    objectives: dict[str, str] = {}
    display_objectives: list[Text] = []
    objectives_bg: pygame.Surface = pygame.Surface((100, 100))
    show_global_temp: bool = False

    deleted_notification = None
    refresh = False

    def draw(self, screen: pygame.Surface, deltatime=1) -> None:
        if self.show_prompt:
            self.prompt.draw(screen)
        
        screen.blit(self.resources_bg, (10*self.scale, 10*self.scale)) 
        if self.show_global_temp: screen.blit(self.temperature_bg, (10*self.scale, 50*self.scale)) 
        try:
            self.resources_text.draw(screen)
            self.objectives_text.draw(screen)
            if self.show_global_temp: self.global_temp_text.draw(screen)
        except AttributeError:
            pass
        self.show_prompt = False

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
        self.resources_text = Text("$ " + format_value(val), (20*self.scale, 16*self.scale), (200*self.scale, 20*self.scale), am.normal_font[18], 0xFAFAFAFA)
        return None
    
    def update_global_temp(self, val: float = 0) -> None:
        self.global_temp_text = Text(f"Delta Temp: {val}", (20*self.scale, 56*self.scale), (200*self.scale, 20*self.scale), am.normal_font[18], 0xFAFAFAFA if val < 0.5 else (0xFFFF0000 if val < 1 else 0xFF000000))
        return None
    
    def add_objective(self, id: str, objective: str) -> None:
        self.objectives[id] = objective
        self.refresh_objectives()
        return None
    
    def remove_objective(self, id: str) -> None:
        del self.objectives[id]
        self.refresh_objectives()
        return None
    
    def check_objective(self, id: str) -> bool:
        try:
            self.objectives[id]
            return True
        except KeyError:
            return False
    
    def refresh_objectives(self) -> None:
        self.display_objectives.clear()
        for i, (_, obj) in enumerate(self.objectives.items()):
            self.display_objectives.append(Text(obj, (20*self.scale, (150+37*i)*self.scale), (260*self.scale, 35*self.scale), am.normal_font[18], 0xF9F9F9F9))
        self.objectives_bg = pygame.Surface((280*self.scale, (100+32*len(self.display_objectives))*self.scale))
        self.objectives_bg.fill(0x000000)
        self.objectives_bg.set_alpha(100)
        self.objectives_text = Text("Objectives", (20*self.scale, 120*self.scale), (650*self.scale, 40*self.scale), am.normal_font[24], 0xF9F9F9F9)

        return None
    
    def refresh_notifications(self) -> None:
        new = []
        for i, notif in enumerate(self.notifications):
            new.append(Notification(notif.text.text, (1000*self.scale, (10+55*i)*self.scale), self.scale, notif.type, notif.t))
        self.notifications = new
        return None
    
    def push_notification(self, msg: str, type = "default") -> None:
        self.notifications.append(Notification(msg, (0, 0), self.scale, type))
        self.refresh_notifications()
        return None

    def update_scale(self, scale) -> None:
        self.scale = scale
        self.refresh_notifications()
        self.refresh_objectives()
        self.prompt.update_scale(scale)
        self.resources_bg = pygame.Surface((280*scale, 30*scale))
        self.resources_bg.set_alpha(180)
        self.resources_bg.fill(0x121212)
        self.temperature_bg = pygame.Surface((280*scale, 30*scale))
        self.temperature_bg.set_alpha(180)
        self.temperature_bg.fill(0x121212)
        return None

class Notification:
    def __init__(self, text: str = "Hello World!", pos: tuple[float, float] = (0, 0), scale: float = 1, type: str = "default", remaining_time = 8) -> None:
        self.type = type
        self.scaled_pos = pos
        self.bg = pygame.Surface((270*scale, 50*scale))
        if type == "info":
            self.bg.fill(0x006994)
        elif type == "upgrade":
            self.bg.fill(0x802069)
        else:
            self.bg.fill(0x1A1A1A)
        
        self.bg.set_alpha(180)
        self.text = Text(text, (pos[0]+scale*10, pos[1]+scale*5), (250*scale, 40*scale), am.normal_font[18], 0xFAFAFAFA)
        self.t = remaining_time
        self.deleted = False
        return None

    def draw(self, screen: pygame.Surface, deltatime) -> None:
        screen.blit(self.bg, self.scaled_pos)
        self.t -= deltatime
        if self.t <= 0: self.deleted = True
        self.text.draw(screen)
        return None

gui: OverlayGUI