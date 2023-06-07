import pygame

from Scripts.GameManager import GameManager
import Scripts.AssetManager as am
import Scripts.AudioManager as audio
from Scripts.Character import Character, Player, NPC
from Scripts.Building import SustainINC
from Scripts.Camera import Camera
from Scripts.ScreenElements import Button, Text, InteractionPrompt
import Scripts.OverlayGUI as overlay
from Scripts.Screen import EndScreen, PauseScreen, StartScreen
from Scripts.GalletCity import GalletCity

import sys

# obtain a value for debugging mode (true to get debug stuff on the screen)
if len(sys.argv) > 2:
    print("Too many arguments. Please only provide the file name and/or the debugging boolean (True/False).\nProceeding with no debugging.")
    debugging: bool = False
elif len(sys.argv) == 2 and sys.argv[1].lower() in ["t", "true"]:
    debugging: bool = True
else:
    debugging: bool = False

# initialise pygame
pygame.init()
clock: pygame.time.Clock = pygame.time.Clock()

# set constants
FPS = 60  # frame rate
BLACK = 0x000000  # black bg
BG = 0xD5C6E0  # purple background
L, H = 800, 450 # Length and Height


# window dimensions should occupy 75% of the screen
info = pygame.display.Info()
L, H = info.current_w*0.75, info.current_h*0.75

# check the dimensions of the screen and set the game scale
if L/1280 > H/720:
    game_scale: float = H/720
else:
    game_scale: float = L/1280

# create the game window
window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
pygame.display.set_caption("Sustain, Inc.")

# give the application window an icon
try:
    logo = pygame.image.load("./Assets/sustainlogo.png")
    pygame.display.set_icon(logo)
except FileNotFoundError:
    pass

# create the game screen (keeping it at the aspect ratio 1280x720)
game_screen = pygame.Surface((game_scale*1280, game_scale*720))

# animation & misc stuff
anim_tick: int = 1 # animation index
running_time: float = 0 # how long since the game started
deltatime: float = 0 # how long since last frame call

# pre init the game manager
gm = GameManager(game_scale)
start_menu: bool = True # start with the start menu as true

# set attribute gui of overlay to a new instance (basically using a static instance)
overlay.gui = overlay.OverlayGUI()

paused: bool = False # controls whether the game is in paused state or not

def close_pause_menu() -> None:
    global paused
    paused = False
    return None

def start_game(player_name="Player") -> None:
    """ start the game with player_name """
    global start_menu, running_time, gm

    # Introduce the initial objective and push a start notification
    overlay.gui.push_notification("Game started in debugging mode" if debugging else "Game started.", "info")
    overlay.gui.add_objective("firstinteract", "Interact with Melon Usk")
    overlay.gui.refresh_objectives()

    # initialise the game
    gm.post_init(game_scale, debugging, player_name, end_game)
    overlay.gui.update_scale(game_scale, gm.character_list+[gm.player]) # this develops the map too
    running_time = 0 # restart from 0
    start_menu = False # close the start menu
    on_resize() # update everything to the scale just in case
    return None

running = True # bool to control whether the game is on or not
def quit_game() -> None:
    global running
    running = False
    return None

finished = False # bool to state whether the game has reached the finished state

def end_game(*kwargs) -> None:
    """ Create the endscreen based on the outcome """
    global finished, p, paused
    finished = True
    p = EndScreen(game_scale, quit_game, kwargs[0])
    paused = True
    return None

# game menus/screens
p = PauseScreen(game_scale, close_pause_menu, quit_game)
s = StartScreen(game_scale, start_game, quit_game)

# city bg
bg = GalletCity()
bg.update_scale(game_scale)

def draw_game_screen() -> None:
    """ renders the game_screen and then draws it on the main window """
    global anim_tick, running_time, game_screen
    # fps is displayed in debug mode
    fps = clock.get_fps()
    fps_text = am.normal_font[24].render(f"FPS: {int(fps)}", True, 0xFFFFFF)

    # play the bg music accordingly
    audio.loop()
    # purple bg is layed out first
    game_screen.fill(BG)

    if start_menu:
        # draw the start menu
        s.draw(game_screen, deltatime)
        window.blit(game_screen, ((L-game_scale*1280)/2, (H-game_scale*720)/2))
        if debugging:
            # fps in debugging mode
            l, h = fps_text.get_rect().size
            window.blit(fps_text, (L-(l+10), 10))
        return None
    
    # update the running time with the time since the last frame
    running_time += deltatime*1000

    # draw the city background
    bg.draw(game_screen, gm.cam.cam_pos)
    
    # evaluate the game screen to collect the visual output if not in a paused state
    if not paused: gm.evaluate_game_screen(deltatime, debugging)
    
    # "draw" the colliders (basically updates their relative position)
    for col in (gm.colliders if gm.flags["firstmeloninteraction"] else gm.colliders+gm.extra_colliders):
        col.draw(game_screen, gm.cam.cam_pos, debugging)

    # draw the game characters and elements
    for c in gm.character_list:
        c.draw(game_screen, gm.cam.cam_pos, anim_tick, debugging)
    for b in gm.building_list:
        if type(b) == SustainINC:
            b.draw(game_screen, gm.cam.cam_pos, anim_tick, debugging)
        else:
            b.draw(game_screen, gm.cam.cam_pos)

    # draw the player after everthing else to render it above everything else
    gm.player.draw(game_screen, gm.cam.cam_pos, anim_tick, gm.walking)

    if debugging:
        # player colliders
        pygame.draw.rect(game_screen, 0xFFFFFF, gm.player.collider_rect, 1)
        pygame.draw.rect(game_screen, 0xFFFFFF, gm.player.rect, 1)
        for key in gm.player.col.keys():
            pygame.draw.rect(game_screen, 0xFFFFFF, gm.player.col[key], 1)            

        # other character colliders
        for c in gm.character_list:
            pygame.draw.rect(game_screen, 0xFFFFFF, c.collider_rect, 1)

        # the move box
        pygame.draw.rect(game_screen, 0x000000, pygame.Rect((game_scale*1280/2-gm.cam.movebox_lim[0], game_scale*720/2-gm.cam.movebox_lim[1]), (2*gm.cam.movebox_lim[0], 2*gm.cam.movebox_lim[1])), 1)

    overlay.gui.draw(game_screen, deltatime, paused) # above everything else, render the overlay gui
    if not paused: anim_tick = int(running_time/200)%4 # precisely callibrated to work with the animation rate
    else:
        # update the pause screen if the game is paused
        p.update_data(int(running_time/1000), gm.get_delta_temp(1))
        p.draw(game_screen)
    
    # render the game_screen on the application window
    window.blit(game_screen, ((L-game_scale*1280)/2, (H-game_scale*720)/2))

    # render the player position text if debugging
    pos_text = am.normal_font[18].render(f"Pos: {int(gm.player.unscaled_pos[0]), int(gm.player.unscaled_pos[1])}", True, 0xFFFFFF)
    if debugging:
        l, h = fps_text.get_rect().size
        window.blit(fps_text, (L-(l+10), 10))
        l = pos_text.get_rect().width
        window.blit(pos_text, (L-(l+10), 20+h))
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

    # update the start menu and the assets to the new scale
    if start_menu: am.load_assets(game_scale)
    s.update_scale(game_scale)
    # resize the application window and the game screen
    window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
    game_screen = pygame.Surface((game_scale*1280, game_scale*720))

    if start_menu: return None # no need to update anything else if the game is still in the start menu (will throw errors otherwise)
    # update the game manager elements
    gm.resize(game_scale)
    
    # update the overlay gui
    overlay.gui.update_scale(game_scale, gm.character_list+[gm.player])

    # update the pause screen
    p.update_scale(game_scale)
    p.update_data(int(running_time/1000), gm.get_delta_temp(1))

    # update the bg city
    bg.update_scale(game_scale)
    return None


def process_inputs(events: list[pygame.event.Event]) -> bool:
    """ Process the events/inputs provided by the user, return whether the app should keep running """
    global L, H, walking, anim_dir, paused, finished
    keys_pressed = pygame.key.get_pressed()
    running = True
    if start_menu: # check for different stuff if the game is still in start menu
        for e in events:
            if e.type == pygame.VIDEORESIZE:
                # if the screen is resized, update everything to the new size
                L, H = window.get_size()
                on_resize()
            if e.type == pygame.QUIT:
                running = False
        # process inputs seperately for the start menu
        s.process_inputs(events, keys_pressed)
        return running
    
    # process inputs for the game
    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if not finished:
                    # updating the pause screen data every time it is unpaused
                    paused = not paused
                p.update_ps_audio_values() # update the options of the pause screen if this is triggered
            if e.key == pygame.K_m:
                if not paused:
                    # trigger map
                    overlay.gui.update_scale(game_scale) # update the scale to not bug it out
                    if not gm.player_interacting: gm.movement_enabled = not overlay.gui.trigger_map() # trigger the map and allow/disallow movement based on whether the player is reading the map
            if e.key == pygame.K_SPACE:
                if not paused and not overlay.gui.show_map:
                    if gm.player_interacting: # if the player is already interacting
                        try:
                            if not gm.player.interaction_character.next_dialogue(): # type: ignore
                                gm.player_interacting = False # stop interacting if reached the end of the dialogue
                                gm.movement_enabled = True
                        except AttributeError: # if some weird glitch occurs (rare), cancel the interaction
                            gm.player_interacting = False
                            gm.movement_enabled = True
                            overlay.gui.show_prompt = False
                    elif gm.player.can_interact: # if the player can interact
                        if gm.player.interaction_character != None:
                            gm.player.interaction_character.interact() # interact with the character the player is in range of
                        gm.player_interacting = True
                        gm.movement_enabled = False
            if e.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]: # sprint if shift is down
                gm.speed = gm.fast_speed
        if e.type == pygame.KEYUP:
            if e.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]: # don't sprint if shift isn't pressed
                gm.speed = gm.normal_speed
        if e.type == pygame.VIDEORESIZE:
            # if the screen is resized, update everything to the new size
            L, H = window.get_size()
            on_resize()

    # process the movement inputs
    if gm.movement_enabled and not paused:
        gm.walking = False
        gm.move_dir = (0, 0)
        # vertical input
        if not ((keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN])): # check for contradictory key presses
            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                gm.anim_dir = "w"
                gm.move_dir = (0, -1)
                gm.walking = True
            elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                gm.anim_dir = "s"
                gm.move_dir = (0, 1)
                gm.walking = True
        # horizontal input
        if not ((keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT])): # check for contradictory key presses
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                gm.anim_dir = "a"
                gm.move_dir = (-1, gm.move_dir[1]) # retain the vertical movement direction (for diagonal movement)
                gm.walking = True
            elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                gm.anim_dir = "d"
                gm.move_dir = (1, gm.move_dir[1]) # retain the vertical movement direction (for diagonal movement)
                gm.walking = True
    return running


def main() -> None:
    """ Main loop where the application runs """
    global L, H, deltatime, running
    running = True
    while running:
        # while the game is on, render the game
        window.fill(BLACK)

        events: list[pygame.event.Event] = pygame.event.get()
        running = process_inputs(events) # process the inputs and see if the user wants to quit

        draw_game_screen()
        deltatime = clock.tick(FPS)/1000 # update the deltatime (ms)
        pygame.display.flip() # update the display
    pygame.quit() # when the user quits, quit the game
    return None


if __name__ == "__main__":
    # execute the program when this file is run
    main()
