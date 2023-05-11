import pygame
from Scripts.Character import NPC
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt
import Scripts.OverlayGUI as overlay
import Scripts.AssetManager as am

class MelonUsk(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int]) -> None:
        self.flags = flags
        self.player_name = player_name
        super().__init__(anim=am.melon_anim, pos=(690, 1690), name="Melon Usk", prompts=[])
        self.prompts = [
            [ # lvl 0
                InteractionPrompt(f"Hello {player_name}! I am Melon Usk, a fellow concernee for the planet... \n[Press SPACE for the next dialogue]"),
                InteractionPrompt("I'm sure you are as passionate about saving this world as I am!\nUnfortunately, in this world driven by money, there are far too many unsustainable practices that are hurting the planet. Let's together convince them to build a better world!..."),
                OptionsPrompt("For now, you will need money to save this world.\nTry upgrading your business: Sustain, INC to level 5! Come back here once you are done.", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 1
                OptionsPrompt("Let's save this world together!\nTry upgrading your business: Sustain, INC to Level 5. Come back here once you are done!", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 2
                InteractionPrompt("Awesome, it may take a while to completely upgrade your business, but we will get there. For now, let's begin saving the world..."),
                InteractionPrompt("Since you are new here, I must explain the rules to you. In order to make connections, you must get a reference to the person.\n Without one, they will get cranky. Like my friend Buff in Buffville, he will only talk to you if you have been referred to..."),
                OptionsPrompt("For now, go talk to CHARACTER TBD, they have some interesting projects you might be interested in.", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 3
                OptionsPrompt("Go talk to CHARACTER TBD -- I hear thery have some projects you might be interested in.\nI too am preparing something special!", Options([("Let's Go!", self.uninteract)]))
            ]
        ]
        return None
    
    def interact(self) -> bool:
        if self.level == 1 and self.flags["sustainlevel"] >= 5:
            self.level = 2
        return super().interact()

    def uninteract(self) -> None:
        self.flags["firstmeloninteraction"] = True
        if self.level == 0:
            if not overlay.gui.check_objective("upgradesustain"):
                overlay.gui.add_objective("upgradesustain", "Upgrade Sustain, INC")
            self.level = 1
        if self.level == 2:
            if not overlay.gui.check_objective("talkwithTBD"):
                overlay.gui.add_objective("talkwithTBD", "Talk with TBD")
            self.level = 3

        return super().uninteract()
    
    