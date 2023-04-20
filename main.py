import pygame

from Scripts.GameManager import GameManager
import Scripts.AssetManager as am
from Scripts.Character import Character, Player, NPC
from Scripts.Camera import Camera
from Scripts.Tiles import GrassTile

pygame.init()

clock: pygame.time.Clock = pygame.time.Clock()
FPS = 60  # frame rate
BLACK = 0x000000  # black bg
BG = 0xD5C6E0  # temporary purple background
L, H = 800, 450

# window dimensions should occupy 75% of the screen
info = pygame.display.Info()
L, H = info.current_w*0.75, info.current_h*0.75

# check the dimensions of the screen and set the game scale
if L/1280 > H/720:
    game_scale = H/720
else:
    game_scale = L/1280

window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
pygame.display.set_caption("Hello, there!")

# create the game screen (keeping it at the aspect ratio 1280x720)
game_screen = pygame.Surface((game_scale*1280, game_scale*720))

debugging: bool = True # set to true to get debug stuff on the screen

anim_tick = 1
running_time = 0
deltatime = 0

gm = GameManager(game_scale, debugging)

def draw_game_screen() -> None:
    # draw the game screen on the main window
    global anim_tick, ben_idle, running_time, rate, pos, speed, game_screen
    fps = clock.get_fps()
    fps_text = am.normal_font[24].render(f"FPS: {int(fps)}", True, 0xFFFFFF)

    running_time += deltatime*1000
    game_screen.fill(BG)

    for tile in gm.grass_tiles:
        tile.draw(game_screen, gm.cam.cam_pos, anim_tick)
    gm.evaluate_game_screen(deltatime)
    gm.player.draw(game_screen, gm.cam.cam_pos, anim_tick, gm.walking)
    if debugging:
        pygame.draw.rect(game_screen, 0xFFFFFF, gm.player.collider_rect, 1)
        pygame.draw.rect(game_screen, 0xFFFFFF, gm.test_character.collider_rect, 1)
    gm.test_character.draw(game_screen, gm.cam.cam_pos, anim_tick, debugging)

    # drawing the move box for debugging
    if debugging: pygame.draw.rect(game_screen, 0xFFFFFF, pygame.Rect((game_scale*1280/2-gm.cam.movebox_lim[0], game_scale*720/2-gm.cam.movebox_lim[1]), (2*gm.cam.movebox_lim[0], 2*gm.cam.movebox_lim[1])), 1)

    anim_tick = int(int(running_time/200)%4) # precisely callibrated to work with the animation rate

    window.blit(game_screen, ((L-game_scale*1280)/2, (H-game_scale*720)/2))
    if debugging:
        l = fps_text.get_rect().width
        window.blit(fps_text, (L-(l+10), 10))
    return None


def on_resize() -> None:
    """  Adjust the game size to the new global dimensions """
    global L, H, window, game_scale, game_screen
    # ensure that the screen dimensions are at least (600, 400)
    if L < 800:
        L = 800
    if H < 450:
        H = 450

    # update the game scale
    if L/1280 > H/720:
        game_scale = H/720
    else:
        game_scale = L/1280
    gm.resize(game_scale)

    # recreate the window and the game_screen with new dimensions
    window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
    game_screen = pygame.Surface((game_scale*1280, game_scale*720))
    print("dimensions changed to ", L, H)
    return None


def process_inputs(events: list[pygame.event.Event]) -> bool:
    """ Process the events/inputs provided by the user, return whether the app should keep running """
    global L, H, walking, anim_dir, rate
    keys_pressed = pygame.key.get_pressed()
    running = True
    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_l:
                # emergency quit (TODO: Remove this)
                running = False
        if e.type == pygame.VIDEORESIZE:
            # if the screen is resized, update everything to the new size
            L, H = window.get_size()
            on_resize()

    if gm.movement_enabled:
        gm.walking = False
        # vertical input
        if not ((keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN])): # check for contradictory key presses
            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                gm.anim_dir = "w"
                gm.walking = True
            elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                gm.anim_dir = "s"
                gm.walking = True
        # horizontal input
        if not ((keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT])): # check for contradictory key presses
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                gm.anim_dir = "a"
                gm.walking = True
            elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                gm.anim_dir = "d"
                gm.walking = True
    return running


def main() -> None:
    """ Main loop where the application runs """
    global L, H, deltatime
    running = True
    while running:
        window.fill(BLACK)
        events: list[pygame.event.Event] = pygame.event.get()
        running = process_inputs(events)
        draw_game_screen()
        deltatime = clock.tick(FPS)/1000
        pygame.display.flip()
    pygame.quit()
    return None


if __name__ == "__main__":
    # execute the program if this is the main file
    main()
