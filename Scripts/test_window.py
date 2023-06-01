import pygame

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Test Window")
r, g, b = 0, 255, 0
red, green, blue = True, True, True

class ToBeImplementedError(Exception):
    def __init__(self, *args: object) -> None:
        msg: str
        super().__init__(*args)

WHITE = 0xFFFFFF
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Bye Bye!")
    screen.fill(0xFFFFFF)
    if red:
        g -= 1
        r += 1
        if r >= 255:
            red = False
            blue, green = True, True
    elif blue:
        r -= 1
        b += 1
        if b >= 255:
            blue = False
    elif green:
        b -= 1
        g += 1
        if g >= 255:
            red = True
    pygame.display.flip()
    clock.tick(60)
raise ToBeImplementedError
pygame.quit()
