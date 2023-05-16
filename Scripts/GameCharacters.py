import math
import pygame
from Scripts.Character import NPC
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt
import Scripts.OverlayGUI as overlay
import Scripts.AssetManager as am

class MelonUsk(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.flags = flags
        self.player_name = player_name
        self.investment_amount = 3e5

        super().__init__(anim=am.melon_anim, pos=(100, 100), name="Melon Usk", prompts=[])
        self.prompts = [
            [ # lvl 0
                InteractionPrompt(f"MELON USK: Hello {player_name}! I am Melon Usk, a fellow concernee for the planet... \n[Press SPACE for the next dialogue]"),
                InteractionPrompt("I'm sure you are as passionate about saving this world as I am!\nUnfortunately, in this world driven by money, there are far too many unsustainable practices that are hurting the planet. Let's together convince them to build a better world!..."),
                OptionsPrompt("For now, you will need money to save this world.\nTry upgrading your business: Sustain, INC to level 5! Come back here once you are done.", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 1
                OptionsPrompt("MELON USK: Let's save this world together!\nTry upgrading your business: Sustain, INC to Level 5. Come back here once you are done!", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 2
                InteractionPrompt("MELON USK: Awesome, it may take a while to completely upgrade your business, but we will get there. For now, let's begin saving the world..."),
                InteractionPrompt("Since you are new here, I must explain the rules to you. In order to make connections, you must get a reference to the person.\n Without one, they will get cranky. Like my friend Buff in Buffville, he will only talk to you if you have been referred to..."),
                OptionsPrompt("For now, go talk to Grater Thunderberg, they have some interesting projects you might be interested in.", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 3
                OptionsPrompt("MELON USK: Go talk to Grater Thunderberg -- I hear she has some projects you might be interested in.\nI too am preparing something special!", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 4
                InteractionPrompt("MELON USK: I see you are an admirer of Ms Thunderberg. Not many have the patience to deal with her..."),
                InteractionPrompt("But anyways, did you know that transport accounted for 37% (2021 data) of CO2 emissions in end user sectors? It's time we move to cleaner sources..."),
                InteractionPrompt("I am launching ASLET, a company focused on creating electric cars - relying on a significantly cleaner source of energy..."),
                OptionsPrompt("But I'll need your support. Would you be interested in being a 10% ($ 500k) share holder?", Options([("$ 500 K", lambda : self.spend_money(5e5)), ("Not now", self.uninteract)]))
            ],
            [ # lvl 5
                OptionsPrompt("Would you be interested in being a 10% ($ 500k) share holder in ASLET?", Options([("$ 500 K", lambda : self.spend_money(5e5)), ("Not now", self.uninteract)]))
            ],
            [ # lvl 6
                InteractionPrompt("Thank you for investing in ASLET. I'll make sure your investment counts! Until then, I recommend you meet Mr Buff, he has been driving his own sustainibility missions.")
            ]
        ]
        return None


    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        if self.level in [4, 5]:
                self.prompt_index = 0
                self.level = 6
                self.flags["investedinaslet"] = 1
                overlay.gui.push_notification("Income increased by 10%", "info")
                self.flags["buffreference"] = True
        else:
            self.uninteract()
        return None
    

    def interact(self) -> bool:
        if self.level == 0:
            if overlay.gui.check_objective("firstinteract"):
                overlay.gui.remove_objective("firstinteract")
        elif self.level == 1 and self.flags["sustainlevel"] >= 5: # type: ignore
            self.level = 2
        elif self.level in (2, 3) and self.flags["donatetoun"]:
            self.level = 4
            self.investment_amount = max(4*math.exp(2*self.flags['sustainlevel']), self.investment_amount) # type: ignore
            self.prompts[4][3] = OptionsPrompt("But I'll need your support. Would you be interested in being a 10% share holder?", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
            self.prompts[5][0] = OptionsPrompt("I'll need your support. Would you be interested in being a 10% share holder?", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
        elif self.level in (4, 5):
            if self.flags["getresources"]() < self.investment_amount:# type: ignore
                self.prompts[4][3].opts.options[0].inactive = True # type: ignore
                self.prompts[5][0].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[4][3].opts.options[0].inactive = False # type: ignore
                self.prompts[5][0].opts.options[0].inactive = False # type: ignore
        return super().interact()

    def uninteract(self) -> None:
        self.flags["firstmeloninteraction"] = True
        if self.level == 0:
            if not overlay.gui.check_objective("upgradesustain"):
                overlay.gui.add_objective("upgradesustain", "Upgrade Sustain, INC")
            self.level = 1
        elif self.level == 2:
            if not overlay.gui.check_objective("talkwiththunderberg"):
                self.flags["thunderbergreference"] = True
                overlay.gui.push_notification("Reference acquired: Grater THUNDERBERG", "info")
                overlay.gui.add_objective("talkwiththunderberg", "Talk with Grater Thunderberg")
            self.level = 3
        elif self.level == 4:
            self.level = 5

        return super().uninteract()
    
class GraterThunderberg(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.flags = flags
        self.player_name = player_name

        self.donation_amount: float = 8e4
        
        super().__init__(anim=am.grater_anim, pos=(-220, 100), name="Grater Thunderberg", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("GRATER THUNDERBERG: How DARE you talk to me without a reference? Go away!", Options([("Leave", self.uninteract)]))
            ],
            [ # lvl 1
                InteractionPrompt(f"GRATER THUNDERBERG: Oh hello {self.player_name}! Mr Usk referred you to me, it is nice to see you!\nI am a climate change activist out here to make a difference, and I see your goals aligning with mine..."),
                OptionsPrompt(f"For starters, the United Nations needs funding to act against the existential threat posed by climate change.\nWould you be interested in helping them out?", Options([("$ 80 K", lambda : self.spend_money(8e4)), ("Sounds like a scam", self.next_dialogue)])),
                OptionsPrompt(f"HOW DARE YOU.", Options([("Go away", lambda: self.uninteract())]))
            ],
            [ # lvl 2
                InteractionPrompt(f"GRATER THUNDERBERG: Thank you for donating! I'm sure it will help out for a better cause. I'll call you again when I want to pester you. I mean when I need more financing.\nUntil then, I'd like you to meet the UN Secretary-General, Mr. Gutters..."),
                OptionsPrompt("Mr Usk has also been upto some interesting projects lately.", Options([("See you around!", self.uninteract)]))
            ]
        ]
        return None
    
    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        overlay.gui.push_notification(f"Spent dolla {amount}", "info")
        if self.level == 1:
            self.prompt_index = 0
            self.level += 1
            self.flags["donatetoun"] = True
            overlay.gui.add_objective("talkwithgutters", "Meet Mr. Gutters.")
        else:
            self.uninteract()
        return None
    
    def interact(self) -> bool:
        if self.level == 0:
            if overlay.gui.check_objective("talkwiththunderberg"):
                overlay.gui.remove_objective("talkwiththunderberg")

            if self.flags["thunderbergreference"]:
                self.level = 1
                self.donation_amount = max(3*math.exp(2*self.flags['sustainlevel']), self.donation_amount) # type: ignore
                self.prompts[1][1] = OptionsPrompt(f"For starters, the United Nations needs funding to act against the existential threat posed by climate change.\nWould you be interested in helping them out?", Options([(f"$ {overlay.format_value(self.donation_amount)}", lambda : self.spend_money(self.donation_amount)), ("Sounds like a Scam", self.next_dialogue)]))
        elif self.level == 1:
            if self.flags["getresources"]() < self.donation_amount: # type: ignore
                self.prompts[1][1].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[1][1].opts.options[0].inactive = False # type: ignore
        return super().interact()
    

    def uninteract(self) -> None:
        return super().uninteract()

class MrGutters(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.flags = flags
        self.player_name = player_name
        super().__init__(anim=am.ben_anim, pos=(290, 1690), name="Mr Gutters", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("GRATER THUNDERBERG: How DARE you talk to me without a reference? Go away!", Options([("Leave", self.uninteract)]))
            ],
            [ # lvl 1
                InteractionPrompt(f"GRATER THUNDERBERG: Oh hello {self.player_name}! Mr Usk referred you to me, it is nice to see you!\nI am a climate change activist out here to make a difference, and I see your goals aligning with mine..."),
                OptionsPrompt(f"For starters, the United Nations needs funding to act against the existential threat posed by climate change.\nWould you be interested in helping them out?", Options([("$ 80 K", lambda : self.spend_money(8e4)), ("No", self.next_dialogue)])),
                OptionsPrompt(f"HOW DARE YOU.", Options([("Go away", lambda: self.uninteract())]))
            ],
            [ # lvl 2
                InteractionPrompt(f"GRATER THUNDERBERG: Thank you for donating! I'm sure it will help out for a better cause. I'll call you again when I want to pester you. I mean when I need more financing.\nUntil then, I'd like you to meet the UN Secretary-General, Mr. Gutters..."),
                OptionsPrompt("Mr Usk has also been upto some interesting projects lately.", Options([("See you around!", self.uninteract)]))
            ]
        ]
        return None
    
    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        self.uninteract()
        return None
    
    def interact(self) -> bool:
        return super().interact()
    

    def uninteract(self) -> None:
        return super().uninteract()

