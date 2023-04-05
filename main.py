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


def draw_game_screen() -> None:
    # draw the game screen on the main window
    game_screen.fill(BG)
    window.blit(game_screen, ((L-game_scale*1280)/2, (H-game_scale*720)/2))
    return None


def on_resize() -> None:
    """  Adjust the game size according to the new global dimensions """
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

    # recreate the window and the game_screen with new dimensions
    window = pygame.display.set_mode((L, H), pygame.RESIZABLE)
    game_screen = pygame.Surface((game_scale*1280, game_scale*720))
    print("dimensions changed to ", L, H)
    return None


def process_inputs(events: list[pygame.event.Event]) -> bool:
    """ Process the events/inputs provided by the user, return whether the app should keep running """
    global L, H
    running = True
    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_l:
                running = False
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
