import pygame

pygame.mixer.init()

bgmusic: bool = True
sfx: bool = True

bg_id = 0
bgtracks = [
    # "./Assets/Audio/stardew1.mp3",
    # "./Assets/Audio/stardew2.mp3",
    # "./Assets/Audio/stardew3.mp3",
    # "./Assets/Audio/stardew4.mp3",
    "./Assets/Audio/stardew6.mp3",
    "./Assets/Audio/stardew7.mp3"
    "./Assets/Audio/stardew5.mp3",
]

soundeffects = {
    "success": pygame.mixer.Sound("./Assets/Audio/success.mp3"),
    "click": pygame.mixer.Sound("./Assets/Audio/click.mp3"),
    "upgrade": pygame.mixer.Sound("./Assets/Audio/upgrade.wav")
}

def loop() -> None:
    global bg_id, playing
    if bgmusic:
        if not pygame.mixer.music.get_busy():
            print("playing")
            pygame.mixer.music.load(bgtracks[bg_id])
            pygame.mixer.music.play()
            bg_id += 1
            if bg_id == len(bgtracks):
                bg_id = 0
    return None

def play_sound(sound: str) -> None:
    global soundeffects
    if not sfx:
        return None
    try:
        pygame.mixer.Sound.play(soundeffects[sound])
    except AttributeError:
        pass
    return None
    