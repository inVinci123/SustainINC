import pygame
from decimal import Decimal
import sigfig

from Scripts.ScreenElements import InteractionPrompt, Text
import Scripts.AssetManager as am

def format_value(val: float) -> str:
    a: str = sigfig.round(f"{int(val)}", decimals=3, notation="eng")
    i = a.find('E')
    exp = int(a[i+1:])
    end: str = ''
    if exp >= 36: return "Too much"
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
    
    i = a.find('.')
    return a[:i] + a[i:i+3] +end

class OverlayGUI:
    prompt = InteractionPrompt()
    show_prompt: bool = True
    resources_bg = pygame.Surface((230, 30))
    resources_bg.fill(0x121212)
    resources_bg.set_alpha(180)
    try:
        resources_text = Text(f"{format_value(0)}", (20, 11), (200, 20), am.normal_font[18], 0xFAFAFAFA)
    except AttributeError:
        pass

    scale = 1

    notifications: list = []
    objectives: list = []

    def draw(self, screen: pygame.Surface, deltatime=1) -> None:
        if self.show_prompt:
            self.prompt.draw(screen)
        
        screen.blit(self.resources_bg, (10, 10))
        try:
            self.resources_text.draw(screen)
        except AttributeError:
            pass
        self.show_prompt = False
        first_notif = True
        for n in self.notifications:
            if first_notif:
                n.draw(screen, deltatime+0.04*len(self.notifications))
                first_notif = False
            else:
                n.draw(screen, deltatime)
            if n.deleted:
                self.notifications.remove(n)
                self.refresh_notifications()
                break
        return None

    def update_resources(self, val: float = 0) -> None:
        self.resources_text = Text("$ " + format_value(val), (20, 16), (200, 20), am.normal_font[18], 0xFAFAFAFA)
        return None
    
    def refresh_notifications(self) -> None:
        new = []
        for i, notif in enumerate(self.notifications):
            new.append(Notification(notif.text.text, (1000*self.scale, (400+55*i)*self.scale), self.scale, notif.type, notif.t))
        self.notifications = new
        return None
    
    def push_notification(self, msg: str, type = "default") -> None:
        self.notifications.append(Notification(msg, (0, 0), self.scale, type))
        self.refresh_notifications()
        return None

    def update_scale(self, scale) -> None:
        self.scale = scale
        self.refresh_notifications()
        self.prompt.update_scale(scale)
        self.resources_bg = pygame.Surface((230*scale, 30*scale))
        self.resources_bg.set_alpha(180)
        self.resources_bg.fill(0x121212)
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
        self.text = Text(text, (pos[0]+scale*10, pos[1]+scale*5), (250*scale, 40*scale), am.normal_font[18], 0xFAFAFAFA)# if type == "default" else 0xFAFAFA)
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