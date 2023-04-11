import pygame

pygame.init()

clock: pygame.time.Clock = pygame.time.Clock()
FPS = 60  # frame rate
BLACK = 0x000000  # black bg
BG = 0xD5C6E0  # temporary purple background
L, H = 800, 450

# window dimensions should occupy 75% of the screen
info = pygame.display.Info()
L, H = info.current_w*0.75, info.current_h*0.75

# quick check the dimensions of the screen and set the scale of the game
if L/1280 > H/720:
    game_scale = H/720
else:
    game_scale = L/1280

window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
pygame.display.set_caption("Hello, there!")
# create the game screen (keeping it at the aspect ratio 1280x720)
game_screen = pygame.Surface((game_scale*1280, game_scale*720))

# test import images
ben_anim: dict = {
    "w": {
    "idle": [pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale))],
    "walk": [pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale))]
    },
    "s": {
    "idle": [pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale))],
    "walk": [pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale))]
    },
    "d": {
    "idle": [pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale))],
    "walk": [pygame.transform.scale(pygame.image.load("./Assets/right_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale))]
    },
    "a": {
    "idle": [pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale))],
    "walk": [pygame.transform.scale(pygame.image.load("./Assets/left_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale))]
    }
}

anim_dir = "s"
anim_id = 1
x = 0 # temp
rate = 4
walking = False
unscaled_pos = (100, 100)
pos = (unscaled_pos[0]*game_scale, unscaled_pos[1]*game_scale)

def update_pos(x:int=0, y:int=0) -> tuple:
    global unscaled_pos, pos
    unscaled_pos = unscaled_pos[0]+x, unscaled_pos[1]+y
    pos = (unscaled_pos[0]*game_scale, unscaled_pos[1]*game_scale)
    return pos

speed = 3

def draw_game_screen() -> None:
    # draw the game screen on the main window
    global anim_id, ben_idle, x, rate, pos, speed
    x += 1
    game_screen.fill(BG)
    if walking:
        print(pos)
        if anim_dir == "w": update_pos(0, -speed)
        if anim_dir == "s": update_pos(0, speed)
        if anim_dir == "a": update_pos(-speed, 0)
        if anim_dir == "d": update_pos(speed, 0)
    game_screen.blit(ben_anim[anim_dir]["walk" if walking else "idle"][anim_id], pos)

    # IDEA: REMOVE THE RATE CRAP AND MAKE EACH ANIMATION 4 FRAMES LONG
    if not x % (40//rate):
        anim_id += 1
        if anim_id == rate:
            anim_id = 0
    window.blit(game_screen, ((L-game_scale*1280)/2, (H-game_scale*720)/2))
    return None


def on_resize() -> None:
    """  Adjust the game size according to the new global dimensions """
    global L, H, window, game_scale, game_screen, ben_anim

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

    ben_anim = {
        "w": {
        "idle": [pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale))],
        "walk": [pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale))]
        },
        "s": {
        "idle": [pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale))],
        "walk": [pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale))]
        },
        "d": {
        "idle": [pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale))],
        "walk": [pygame.transform.scale(pygame.image.load("./Assets/right_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale))]
        },
        "a": {
        "idle": [pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale))],
        "walk": [pygame.transform.scale(pygame.image.load("./Assets/left_walk_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_walk_2.png"), (80*game_scale, 80*game_scale)), pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale))]
        }
    }

    update_pos()

    # recreate the window and the game_screen with new dimensions
    window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
    game_screen = pygame.Surface((game_scale*1280, game_scale*720))
    print("dimensions changed to ", L, H)
    return None


def process_inputs(events: list[pygame.event.Event]) -> bool:
    """ Process the events/inputs provided by the user, return whether the app should keep running """
    global L, H, walking, anim_dir, rate
    running = True
    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_l:
                running = False
            if e.key == pygame.K_w:
                anim_dir = "w"
                walking = True
            if e.key == pygame.K_a:
                anim_dir = "a"
                walking = True
            if e.key == pygame.K_s:
                anim_dir = "s"
                walking = True
            if e.key == pygame.K_d:
                anim_dir = "d"
                walking = True
        if e.type == pygame.KEYUP:
            if (e.key == pygame.K_w and anim_dir == "w") or (e.key == pygame.K_a and anim_dir == "a") or (e.key == pygame.K_s and anim_dir == "s") or (e.key == pygame.K_d and anim_dir == "d"):
                walking = False
        if e.type == pygame.VIDEORESIZE:
            # if the screen is resized, update everything to the new size
            L, H = window.get_size()
            on_resize()
    return running


def main() -> None:
    """ Main loop where the application runs. """
    global L, H
    running = True
    while running:
        window.fill(BLACK)
        events: list[pygame.event.Event] = pygame.event.get()
        running = process_inputs(events)
        draw_game_screen()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    return None


if __name__ == "__main__":
    # execute the program if this is the main file
    main()
