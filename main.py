import pygame

import Scripts.AssetManager as am
from Scripts.Character import Character, Player
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

am.load_assets(game_scale)
ben_anim: dict = am.ben_anim
test_character = Character(ben_anim, (5*120, 3*120))
test_character.update_scale(game_scale)

anim_dir = "s"
anim_tick = 1
running_time = 0 # temp

cam = Camera(game_scale)

rate = 4
walking = False
unscaled_pos = (game_scale*1280/2, game_scale*720/2)
pos = (unscaled_pos[0]*game_scale, unscaled_pos[1]*game_scale)
speed = 200
player = Player(pos)
player.update_scale(game_scale)

deltatime = 0

grass_tiles: list[GrassTile] = []
for i in range(-100, 100): # I'm crazy enough to render 4000 blocks for testing
    for j in range(-10, 10):
        g = GrassTile((i*255, j*255))
        grass_tiles.append(g)
        g.update_scale(game_scale)

light_font = pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", 24)

def draw_game_screen() -> None:
    # draw the game screen on the main window
    global anim_tick, ben_idle, running_time, rate, pos, speed
    fps = clock.get_fps()
    fps_text = light_font.render(f"FPS: {int(fps)}", True, 0xFFFFFF)

    running_time += deltatime*1000
    game_screen.fill(BG)
    if walking:
        if anim_dir == "w":
            player.move(0, -speed*deltatime, anim_dir)
            cam.update_movebox(0, -speed*deltatime)
        if anim_dir == "s":
            player.move(0, speed*deltatime, anim_dir)
            cam.update_movebox(0, speed*deltatime)
        if anim_dir == "a":
            player.move(-speed*deltatime, 0, anim_dir)
            cam.update_movebox(-speed*deltatime, 0)
        if anim_dir == "d":
            player.move(speed*deltatime, 0, anim_dir)
            cam.update_movebox(speed*deltatime, 0)
    
    for tile in grass_tiles:
        tile.draw(game_screen, cam.cam_pos, anim_tick)

    player.draw(game_screen, cam.cam_pos, anim_tick, walking)
    test_character.draw(game_screen, cam.cam_pos, anim_tick)
    
    # TODO: also render every character in the order of how they appear on the y axis
    # (first organise them according to their y axis and then render them)
    # OR make collisions work so that problem doesn't even happen
    anim_tick = int(int(running_time/200)%4) # precisely callibrated to work with the animation rate

    """
    if not running_time % (40//rate):
        anim_tick += 1
        if anim_tick == rate:
            anim_tick = 0
    """
    window.blit(game_screen, ((L-game_scale*1280)/2, (H-game_scale*720)/2))
    l, h = fps_text.get_rect().size
    window.blit(fps_text, (L-(l+10), h+10))
    return None


def on_resize() -> None:
    """  Adjust the game size to the new global dimensions """
    global L, H, window, game_scale, game_screen, ben_anim, test_character, grass_tiles

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

    am.load_assets(game_scale)
    ben_anim = am.ben_anim
    
    test_character.update_scale(game_scale, ben_anim)
    player.update_scale(game_scale, ben_anim)
    for tile in grass_tiles:
        tile.update_scale(game_scale)
    cam.rescale(game_scale)

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

    walking = False
    # vertical input
    if not ((keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN])): # check for contradictory key presses
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            anim_dir = "w"
            walking = True
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            anim_dir = "s"
            walking = True
    # horizontal input
    if not ((keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT])): # check for contradictory key presses
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            anim_dir = "a"
            walking = True
        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            anim_dir = "d"
            walking = True
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
