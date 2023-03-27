import pygame

pygame.init()

clock: pygame.time.Clock = pygame.time.Clock()
FPS = 60
BG = 0xD5C6E0
L, H = 720, 480

screen = pygame.display.set_mode((L, H))
pygame.display.set_caption("Hello, there!")

running = True
while running:
    screen.fill(BG)
    events: list[pygame.event.Event] = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
