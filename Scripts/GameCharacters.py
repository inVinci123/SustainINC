import pygame
import math
from Scripts.Character import NPC
from Scripts.ScreenElements import InteractionPrompt, Options, OptionsPrompt
import Scripts.OverlayGUI as overlay
import Scripts.AssetManager as am

class MelonUsk(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.carbon_contribution = -1
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
            ],
            [ # lvl 7
                InteractionPrompt(f"{player_name}: Hello Mr Usk, I have a favour to ask you. Mr. Dani requests you to join hands with him as he switches to a more sustainable route..."),
                InteractionPrompt("MELON USK: MR DANI? No way, I ain't joining hands with him..."),
                InteractionPrompt("Well if you insist, I'll give him a shot. But only if you are willing to go to Buff Jesos and ask him about the secret of his shampoo- I mean his e-commerce platform, Sahara.")
            ],
            [ # lvl 8
                InteractionPrompt(f"MELON USK: Did he agree to it?"),
                InteractionPrompt(f"{self.player_name}: Well, he asked you to trade your SpaceY rockets..."),
                InteractionPrompt(f"MELON USK: Anything for the Shampoo. I mean, Sahara.")
            ],
            [ # lvl 9
                InteractionPrompt("MELON USK: Thanks, I'm in to partner with Dani now")
            ],
            [ # lvl 10
                InteractionPrompt(f"{self.player_name}: Hey Mr Usk, another favour to ask you. The UN believes that Climate Change can only be solved if all of us come together to tackle it. Would you be interested in joining Greenpeace?"),
                OptionsPrompt("MELON USK: I'll be interested to join if you get Mr Feast in.", Options([("Okay!", self.uninteract)]))
            ],
            [ # lvl 11
                InteractionPrompt(f"{self.player_name}: The UN believes that Climate Change can only be solved if all of us come together to tackle it. Would you be interested in joining Greenpeace?"),
                OptionsPrompt("MELON USK: I heard Mr Feast is in! If you are willing to invest a few more $$ in ASLET, I'll be in!", Options([("$$", lambda: self.spend_money(self.investment_amount))]))
            ],
            [ # lvl 12
                InteractionPrompt("MELON USK: Awesome! Do make sure you get Mr Jesos in too!")
            ]
        ]
        return None


    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        if self.level in [4, 5]:
            self.prompt_index = 0
            self.level = 6
            self.flags["investmentlevel"] = 1
            overlay.gui.push_notification("Income increased by 10%", "info")
        elif self.level == 11:
            self.flags["investmentlevel"] += 1 # type: ignore
            overlay.gui.push_notification("Income increased by 10%", "info")
            self.level = 12
            self.prompt_index = 0
            if overlay.gui.check_objective("convinceusktogogreen"):
                overlay.gui.remove_objective("convinceusktogogreen")
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
            if overlay.gui.check_objective("convinceuskfordani"):
                self.level = 7
            else:
                self.level = 4
                self.investment_amount = max(4*math.exp(2*self.flags['sustainlevel']), self.investment_amount) # type: ignore
                self.prompts[4][3] = OptionsPrompt("But I'll need your support. Would you be interested in being a 10% share holder?", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
                self.prompts[5][0] = OptionsPrompt("I'll need your support. Would you be interested in being a 10% share holder?", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
        elif self.level in (4, 5):
            if overlay.gui.check_objective("convinceuskfordani"):
                self.level = 7
            elif self.flags["getresources"]() < self.investment_amount: # type: ignore
                self.prompts[4][3].opts.options[0].inactive = True # type: ignore
                self.prompts[5][0].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[4][3].opts.options[0].inactive = False # type: ignore
                self.prompts[5][0].opts.options[0].inactive = False # type: ignore
        elif self.level == 6 and overlay.gui.check_objective("convinceuskfordani"):
            self.level = 7
        elif self.level == 7 and overlay.gui.check_objective("getspaceyfromusk"):
            self.level = 8
        elif self.level == 8:
            if not overlay.gui.check_objective("getsaharasecretsfrombuff"):
                self.level = 9
        elif self.level == 9 and overlay.gui.check_objective("convinceusktogogreen"):
            self.level = 10
        elif self.level == 10 and not overlay.gui.check_objective("convincefeasttogogreen"):
            self.level = 11
            self.investment_amount = max(3e9, 4*math.exp(2*self.flags['sustainlevel'])) # type: ignore
            self.prompts[11][1] = OptionsPrompt(f"MELON USK: I heard Mr Feast is in for it. If you are willing to invest $ {overlay.format_value(self.investment_amount)} in ASLET, I'll be in!", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda: self.spend_money(self.investment_amount))]))
        elif self.level == 11:
            if self.flags["getresources"]() < self.investment_amount: # type: ignore
                self.prompts[11][1].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[11][1].opts.options[0].inactive = False # type: ignore
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
        elif self.level == 7:
            overlay.gui.add_objective("getsaharasecretsfrombuff", "Get Sahara secrets from Buff")
            self.flags["buffreference"] = True
        elif self.level == 8:
            if overlay.gui.check_objective("getspaceyfromusk"):
                overlay.gui.remove_objective("getspaceyfromusk")
            self.flags["spaceyacquired"] = True
            overlay.gui.push_notification("SpaceY acquired", "info")
        elif self.level == 9:
            if overlay.gui.check_objective("convinceuskfordani"):
                overlay.gui.remove_objective("convinceuskfordani")
        return super().uninteract()
    
class GraterThunderberg(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.carbon_contribution = -1
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
            ],
            [ # lvl 3
                OptionsPrompt(f"Fridays for Future!", Options([("Leave", self.uninteract)]))
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
        else:
            if self.flags["globaltemperatureunlocked"]:
                self.level = 3
                self.prompt_index = 0
        return super().interact()
    

    def uninteract(self) -> None:
        return super().uninteract()

class MrGutters(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.carbon_contribution = -5
        self.flags = flags
        self.player_name = player_name
        super().__init__(anim=am.ben_anim, pos=(-500, 0), name="Mr Gutters", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("MR GUTTERS: Ei, cara! I busy man, no reference no talk.", Options([("Leave", self.uninteract)]))
            ],
            [ # lvl 1
                InteractionPrompt(f"MR GUTTERS: Ola {self.player_name}! Thank you for your generous donation. To deem whether you are capable for a partnership, I'll quiz you!\n Get ready mate..."),
                OptionsPrompt(f"Q1: What does UN stand for?", Options([("United Nations", self.correct), ("US Navy ", self.incorrect)])),
                OptionsPrompt(f"That was an easy one, let's see how you go now.\nQ2: When were the UN Sustainable Development Goals written?", Options([("1997", self.incorrect), ("2007", self.incorrect), ("2015", self.correct)])),
                OptionsPrompt(f"Inacreditavel! Well, any five year old could answer that. Not this one though.\nQ3: How much of end user sector CO2 emissions did transport account for in 2021?", Options([("37%", self.correct), ("69%", self.incorrect), ("26%", self.incorrect)])),
                OptionsPrompt(f"37% !!! It's time we move to Electric cars already.\nQ4: Approx 100k species face the threat of extinction due to climate change.\nTrue or False?", Options([("True", self.incorrect), ("False", self.correct)])),
                OptionsPrompt(f"It's infact 1 million species. We better hurry up and save the world.\nFinal Q: What temperature threshold was agreed upon in the Paris agreement.", Options([("2.5 degrees", self.incorrect), ("1.5 degrees", lambda: self.correct(True)), ("0.95 degrees", self.incorrect)])),
                # CRITICAL LOGIC ERROR: Space can be pressed to skip through all of the interaction/option prompts
                InteractionPrompt("Resposta Incorreta! Try again...")
            ],
            [ # lvl 2
                InteractionPrompt(f"Parabens! You are officially a partner of the UN, {player_name}.\nYou should now see a global temperature bar under your resources on the top left.\nWe must return it to zero and not let it reach 1.5 degrees, as agreed in the Paris agreement."),
                OptionsPrompt("I shall now assign you to your first mission. Mr Dani, an Asian mining and energy tycoon has had a negative impact on the climate.\nConvince him to transition into sustainable energy.", Options([("Right away!", self.uninteract)]))
            ],
            [ # lvl 3
                InteractionPrompt("MR GUTTERS: Obrigado! We have improved the rate of global warming. But did you know the world meteorological organisation predicted that there is a 66% chance we are gonna break the 1.5C limit.\n We don't have any time to be sitting around, so here's your second mission."),
                InteractionPrompt("Greenpeace is an international organisation focused on ensuring the ability of Earth to nurture life in all it's diversity. We wish to involve prominent public figures. Convince Mr Usk, Mr Jesos, and Mr Feast to join the green side!"),
                InteractionPrompt(f"{self.player_name}: DID YOU SAY MR FEAST! I'M A BIG FAN."),
                OptionsPrompt("MR GUTTERS: Go do it!", Options([("Let's Go!", self.uninteract)]))
            ],
            [ # lvl 4
                InteractionPrompt("Good luck on your mission to convince Mr Usk, Mr Jesos, and Mr Feast!\nCome back for the final mission!")
            ]
        ]
        return None
    
    def correct(self, finished = False) -> None:
        if finished:
            if self.level == 1:
                self.level = 2
                self.prompt_index = 0
                self.flags["unlockglobaltemperature"]() # type: ignore
        else:
            self.prompt_index += 1
        return None
    
    def incorrect(self):
        if self.level == 1:
            self.prompt_index = len(self.prompts[1])-1

    def next_dialogue(self, num=1) -> bool:
        if self.level == 1:
            if self.prompt_index not in (0, len(self.prompts[1])-1): # not the first dialogue or the last dialogue
                self.incorrect()
                return False
        return super().next_dialogue(num)
    
    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        self.uninteract()
        return None
    
    def interact(self) -> bool:
        if self.level == 0 and self.flags["donatetoun"]:
            if overlay.gui.check_objective("talkwithgutters"):
                overlay.gui.remove_objective("talkwithgutters")
            self.level = 1
        if self.level == 2 and self.flags["daniconvinced"]:
            self.level = 3

        return super().interact()
    
    def uninteract(self) -> None:
        if self.level == 2:
            self.flags["danireference"] = True
            overlay.gui.add_objective("convincedani", "Convince Mr. Dani to switch.")
            overlay.gui.push_notification("Reference acquired: Mr Dani")
        if self.level == 3:
            self.level = 4
            overlay.gui.add_objective("convinceusktogogreen", "Convince Mr Usk to join Greenpeace")
            overlay.gui.add_objective("convincejesostogogreen", "Convince Mr Jesos to join Greenpeace")
            overlay.gui.add_objective("convincefeasttogogreen", "Convince Mr Feast to join Greenpeace")
        return super().uninteract()
        

class MrDani(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.carbon_contribution = 40
        self.flags = flags
        self.player_name = player_name
        self.investment_amount = 1e6
        super().__init__(anim=am.ben_anim, pos=(-900, 0), name="Mr Dani", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("MR DANI: Go away, I'm busy making $$.", Options([("Leave", self.uninteract)]))
            ],
            [ # lvl 1
                InteractionPrompt(f"{self.player_name}: Hello Mr. Dani. You have a great mining business out here..."),
                InteractionPrompt(f"MR DANI: Haha indeed, I've built my life on this. What are you here for, {self.player_name}?"),
                InteractionPrompt(f"{self.player_name}: I'm representing the UN. As a concerned individual of the planet, I request you to consider alternative sources of energy..."),
                OptionsPrompt("I see where you are going with this, buddy. I'll consider it if you are willing to invest $ 1M into this", Options([("Dolla Dolla", lambda : self.spend_money(1e6)), ("Not now", self.uninteract)]))
            ],
            [ # lvl 2
                OptionsPrompt("MR DANI: I'll consider switching if you are willing to invest $1M into this", Options([("Dolla Dolla", lambda : self.spend_money(1e6)), ("Not now", self.uninteract)]))
            ],
            [ # lvl 3
                InteractionPrompt("MR DANI: I'll make good use of that money. But I will not start this until you get Melon Usk in with on this business."),
                InteractionPrompt(f"{self.player_name}: Cunning man, you are.")
            ],
            [ # lvl 4
                InteractionPrompt(f"{self.player_name}: I got you the deal."),
                OptionsPrompt("MR DANI: There you are. I'll start to work on the projects now. Head back to Mr Gutters, he was looking for you", Options([("Thank you.", self.uninteract)]))
            ],
            [ # lvl 5
                OptionsPrompt("MR DANI: Yayaya I got the dolla dolla dolla.\nUhm *cough cough* What are you doing here?", Options([("Leave...", self.uninteract)]))
            ]
        ]
        return None

    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        if self.level in (1, 2):
            self.level = 3
            self.prompt_index = 0
            return None
        self.uninteract()
        return None
    
    def interact(self) -> bool:
        if self.level == 0 and self.flags["danireference"]:
            self.level = 1
            self.investment_amount = max(3*math.exp(2*self.flags['sustainlevel']), self.investment_amount) # type: ignore
            self.prompts[1][3] = OptionsPrompt(f"I see where you are going with this, young mate. I'll consider it if you are willing to invest $ {overlay.format_value(self.investment_amount)} into this", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
            self.prompts[2][0] = OptionsPrompt("MR DANI: I'll consider switching if you are willing to invest $1M into this", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
        elif self.level in (1,2):
            if self.flags["getresources"]() < self.investment_amount: # type: ignore
                self.prompts[1][3].opts.options[0].inactive = True # type: ignore
                self.prompts[2][0].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[1][3].opts.options[0].inactive = False # type: ignore
                self.prompts[2][0].opts.options[0].inactive = False # type: ignore
        elif self.level == 3:
            if not overlay.gui.check_objective("convinceuskfordani") and self.flags["spaceyacquired"]: # additional condition to avoid a weird bug
                self.level = 4
                self.flags["daniconvinced"] = True

        return super().interact()
    
    def uninteract(self) -> None:
        if self.level == 3:
            overlay.gui.add_objective("convinceuskfordani", "Convince Melon Usk")
        if self.level == 4:
            self.level = 5
            self.carbon_contribution -= 20 # half the carbon contribution
            overlay.gui.push_notification("Carbon contribution improved!")
            if overlay.gui.check_objective("convincedani"):
                overlay.gui.remove_objective("convincedani")
        return super().uninteract()

# remove this class once you are done, only intended to quicken up the process of making new characters
class TemplateCharacter(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.flags = flags
        self.player_name = player_name
        super().__init__(anim=am.ben_anim, pos=(0, 100), name="PLACEHOLDER FOR THE NAME", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("GO AWAY, ME NO TALK WITHOUT A REFERENCE", Options([("Leave", self.uninteract)]))
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
    
class BuffJesos(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.carbon_contribution = 5
        self.flags = flags
        self.player_name = player_name
        self.investment_amount = 5e8
        super().__init__(anim=am.ben_anim, pos=(0, 500), name="Buff Jesos", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("BUFF JESOS: Go away, I'm busy.", Options([("Leave", self.uninteract)]))
            ],
            [ # lvl 1
                InteractionPrompt(f"BUFF JESOS: Who are you?"),
                InteractionPrompt(f"{self.player_name}: Hello Mr. Jesos! I see your incredible e-commerce platform, Sahara. I am a representative of the UN, {self.player_name}."),
                InteractionPrompt(f"BUFF JESOS: Okay, why are you here, {self.player_name}?"),
                InteractionPrompt(f"{self.player_name}: I was wondering if you are willing to share your secrets of how Sahara works."),
                InteractionPrompt("BUFF JESOS: Are you stupid? No business just gives away their secrets like that..."),
                OptionsPrompt("Well, if you are willing to invest $$", Options([("$ 1b", lambda: self.spend_money(1e9)), ("Not now", self.uninteract)]))
            ],
            [ # lvl 2
                OptionsPrompt("BUFF JESOS: If you are willing to invest $$, I'll consider it.", Options([("$ 1b", lambda: self.spend_money(1e9)), ("Not now", self.uninteract)]))
            ],
            [ # lvl 3
                OptionsPrompt("BUFF JESOS: That money will be put to a good use. I have another favour to ask - Could you convince Mr Usk to trade me his SpaceY rockets?", Options([("Ugh, fine...", self.uninteract)]))
            ],
            [ # lvl 4
                InteractionPrompt(f"{self.player_name}: I got you the SpaceY. Will you honour your end of the deal?"),
                OptionsPrompt("BUFF JESOS: That I shall do.", Options([("Thank you.", self.uninteract)]))
            ],
            [ # lvl 5
                InteractionPrompt(f"{self.player_name}: Hello Mr. Jesos, I have a proposal for you. The UN believes that Climate Change can only be solved if all of us come together to tackle it. Would you be interested in joining Greenpeace?"),
                OptionsPrompt("BUFF JESOS: Interesting Proposal you have. I'll be in if Mr Usk is in.", Options([("Okay", self.uninteract)]))
            ],
            [ # lvl 6
                InteractionPrompt(f"{self.player_name}: The UN believes that Climate Change can only be solved if all of us come together to tackle it. Would you be interested in joining Greenpeace, Mr Jesos?"),
                OptionsPrompt(f"BUFF JESOS: I hear Mr Usk is in too. I'll be in if you are willing to invest $$ into the Jesos Earth Fund", Options([("$$", lambda : self.spend_money(self.investment_amount)), ("Not now...", self.uninteract)]))
            ],
            [ # lvl 7
                InteractionPrompt("BUFF JESOS: I'm in! Mr Gutters was looking for you. Something about a final mission.")
            ]
        ]
        return None

    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        if self.level in (1, 2):
            self.level = 3
            self.prompt_index = 0
            self.flags["investmentlevel"] += 1 # type: ignore
            overlay.gui.push_notification("Income increased by 10%", "info")
            return None
        if self.level == 6:
            self.level = 7
            self.prompt_index = 0
            self.flags["investmentlevel"] += 1 # type: ignore
            overlay.gui.push_notification("Income increased by 10%", "info")
            if overlay.gui.check_objective("convincejesostogogreen"):
                overlay.gui.remove_objective("convincejesostogogreen")
                overlay.gui.add_objective("meetguttersforfinalmission", "Meet Mr Gutters for the final mission.")
        self.uninteract()
        return None
    
    def interact(self) -> bool:
        if self.level == 0:
            if self.flags["buffreference"]:
                self.level = 1
                self.investment_amount = max(3*math.exp(2*self.flags['sustainlevel']), self.investment_amount) # type: ignore
                self.prompts[1][5] = OptionsPrompt(f"Well, if you are willing to invest $ {overlay.format_value(self.investment_amount)}", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda: self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
                self.prompts[2][0] = OptionsPrompt(f"BUFF JESOS: If you are willing to invest $ {overlay.format_value(self.investment_amount)}, I'll consider it.", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda: self.spend_money(self.investment_amount)), ("Not now", self.uninteract)]))
        elif self.level in (1, 2):
            if self.flags["getresources"]() < self.investment_amount: # type: ignore
                self.prompts[1][5].opts.options[0].inactive = True # type: ignore
                self.prompts[2][0].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[1][5].opts.options[0].inactive = False # type: ignore
                self.prompts[2][0].opts.options[0].inactive = False # type: ignore
        elif self.level == 3:
            if self.flags["spaceyacquired"]:
                self.level = 4
        elif self.level == 4 and overlay.gui.check_objective("convincejesostogogreen"):
            if overlay.gui.check_objective("convinceusktogogreen"):
                self.level = 5
            else:
                self.level = 6
                self.investment_amount = max(10e9, 2*math.exp(4*self.flags['sustainlevel'])) # type: ignore
                self.prompts[6][1] = OptionsPrompt(f"BUFF JESOS: I hear Mr Usk is in too. I'll be in if you are willing to invest $ {overlay.format_value(self.investment_amount)} into the Jesos Earth Fund", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now...", self.uninteract)]))
        elif self.level == 5 and not overlay.gui.check_objective("convinceusktogogreen"):
            self.level = 6
            self.investment_amount = max(10e9, 2*math.exp(4*self.flags['sustainlevel'])) # type: ignore
            self.prompts[6][1] = OptionsPrompt(f"BUFF JESOS: I hear Mr Usk is in too. I'll be in if you are willing to invest $ {overlay.format_value(self.investment_amount)} into the Jesos Earth Fund", Options([(f"$ {overlay.format_value(self.investment_amount)}", lambda : self.spend_money(self.investment_amount)), ("Not now...", self.uninteract)]))
        elif self.level == 6:
            if self.flags["getresources"]() < self.investment_amount: # type: ignore
                self.prompts[6][1].opts.options[0].inactive = True # type: ignore
            else:
                self.prompts[6][1].opts.options[0].inactive = False # type: ignore
        return super().interact()
    
    def uninteract(self) -> None:
        if self.level == 1:
            self.level = 2
        elif self.level == 3:
            overlay.gui.add_objective("getspaceyfromusk", "Get SpaceY designs from Mr Usk.")
        elif self.level == 4:
            if overlay.gui.check_objective("getsaharasecretsfrombuff"):
                overlay.gui.remove_objective("getsaharasecretsfrombuff")
                overlay.gui.push_notification("Sahara Secrets obtained!", "info")
            self.flags["saharaacquired"] = True

        return super().uninteract()
    
class AmazonEmployee(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object], pos) -> None:
        self.carbon_contribution = 2
        self.flags = flags
        self.player_name = player_name
        super().__init__(anim=am.ben_anim, pos=pos, name="Amazon Employee", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("Go away, I don't wanna be fired", Options([("Leave", self.uninteract)]))
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

class MrFeast(NPC):
    def __init__(self, player_name: str, flags: dict[str, bool|int|object]) -> None:
        self.carbon_contribution = 1
        self.flags = flags
        self.player_name = player_name
        self.donation_amount = 1e9
        super().__init__(anim=am.ben_anim, pos=(0, -200), name="Mr Feast", prompts=[])
        self.prompts = [
            [ # lvl 0
                OptionsPrompt("Answer this question to get free money!\nHow many trees has Team Trees planted?", Options([("> 20M", lambda : self.spend_money(-5e4)), ("< 20 M", self.next_dialogue)])),
                InteractionPrompt("Incorrect, try again!")
            ],
            [ # lvl 1
                OptionsPrompt("When was Team Seas released?", Options([("October 2021", lambda : self.spend_money(-5e4)), ("July 2020", self.next_dialogue)])),
                InteractionPrompt("Incorrect, try again!")
            ],
            [ # lvl 2
                InteractionPrompt("Come back for more!")
            ],
            [ # lvl 3
                InteractionPrompt(f"{player_name}: Hello Mr Feast! I see you've done some amazing work with your initiatives - Team Trees and Team Seas!"),
                InteractionPrompt("MR FEAST: I'm glad you liked it! Tell me what brings you here."),
                InteractionPrompt(f"{player_name}: Wondering if you are willing to take it further and join GreenPeace?"),
                OptionsPrompt("MR FEAST: I'm up for it if you donate $$ to Team Trees and Team Seas!", Options([("$$", lambda: self.spend_money(self.donation_amount))]))
            ],
            [ # lvl 4
                OptionsPrompt("MR FEAST: I'll join Green Peace if you donate $$ to Team Trees and Team Seas!", Options([("$$", lambda: self.spend_money(self.donation_amount))]))
            ],
            [ # lvl 5
                InteractionPrompt("MR FEAST: I appreciate your generous donation! I shall join Greenpeace right away!")
            ]
        ]
        return None

    def spend_money(self, amount) -> None:
        self.flags["spendresources"](amount) # type: ignore
        if self.level in [0, 1]:
            self.level += 1
            self.prompt_index = 0
            return None
        elif self.level in [3, 4]:
            self.level = 5
            self.prompt_index = 0
            return None
        self.uninteract()
        return None
    
    def interact(self) -> bool:
        if self.level in [0, 1, 2]:
            if overlay.gui.check_objective("convincefeasttogogreen"):
                self.level = 3
                self.donation_amount = max(self.donation_amount, 3*math.exp(2*self.flags['sustainlevel'])) # type: ignore
                self.prompts[3][3] = OptionsPrompt(f"MR FEAST: I'm up for it if you donate $ {overlay.format_value(self.donation_amount)} to Team Trees and Team Seas!", Options([(f"$ {overlay.format_value(self.donation_amount)}", lambda : self.spend_money(self.donation_amount)), ("Not now...", self.uninteract)]))
                self.prompts[4][0] = OptionsPrompt(f"MR FEAST: I'll join Green Peace if you donate $ {overlay.format_value(self.donation_amount)} to Team Trees and Team Seas!", Options([(f"$ {overlay.format_value(self.donation_amount)}", lambda: self.spend_money(self.donation_amount)), ("Not now", self.uninteract)]))
        elif self.level == 3:
            if self.flags["getresources"]() > self.donation_amount: # type: ignore
                self.prompts[3][3].opts.options[0].inactive = False # type: ignore
                self.prompts[4][0].opts.options[0].inactive = False # type: ignore
            else:
                self.prompts[3][3].opts.options[0].inactive = True # type: ignore
                self.prompts[4][0].opts.options[0].inactive = True # type: ignore
        return super().interact()
    
    def uninteract(self) -> None:
        if self.level == 3:
            self.level = 4
        if self.level == 5:
            if overlay.gui.check_objective("convincefeasttogogreen"):
                overlay.gui.remove_objective("convincefeasttogogreen")
        return super().uninteract()