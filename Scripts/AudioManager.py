import pygame

# init the audio
pygame.mixer.init()

# toggle music/sfx on or off
bgmusic: bool = True
sfx: bool = True

# bg music id
bg_id = 0
bgtracks = [ # music tracks to loop - stardew valley :)
    "./Assets/Audio/stardew7.mp3",
    "./Assets/Audio/stardew5.mp3",
    "./Assets/Audio/stardew6.mp3",
]

soundeffects = { # sound effects dict
    "success": pygame.mixer.Sound("./Assets/Audio/success.mp3"),
    "click": pygame.mixer.Sound("./Assets/Audio/click.mp3"),
    "upgrade": pygame.mixer.Sound("./Assets/Audio/upgrade.wav")
}

def loop() -> None:
    """ check if the bg music needs to change (if allowed) """
    global bg_id, playing
    if bgmusic:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(bgtracks[bg_id])
            pygame.mixer.music.play()
            bg_id += 1 # next song if possible
            if bg_id == len(bgtracks):
                bg_id = 0 # else back to song 0
    return None

def play_sound(sound: str) -> None:
    """ play sfx if allowed """
    global soundeffects
    if not sfx:
        return None
    try:
        pygame.mixer.Sound.play(soundeffects[sound])
    except AttributeError:
        pass
    return None
    