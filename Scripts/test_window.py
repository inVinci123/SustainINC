import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Test Window")
WHITE = 0xFFFFFF
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Bye Bye!")
    screen.fill(WHITE)
    pygame.display.flip()
pygame.quit()
