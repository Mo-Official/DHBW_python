import pygame
import random


# window stats
WIDTH = 360
HEIGHT = 480
TITLE = "My Game"
FPS = 30

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)


# init game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()


# game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # process input (event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update logic
    all_sprites.update()

    # render and draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # after drawing everythin
    pygame.display.flip()

pygame.quit()