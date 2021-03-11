# Simple pygame program


# Import and initialize the pygame library

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEMOTION,
    QUIT,

)

pygame.init()


# Set up the drawing window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

ship_surf = pygame.Surface((50,50))

# Run until the user asks to quit

running = True

while running:

    screen.fill((255, 255, 255))
    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            pass

        if event.type == MOUSEMOTION:
            mouse_X = pygame.mouse.get_pos()[0]
            pygame.draw.circle(ship_surf, (0,0,100), pygame.mouse.get_pos(), 10)

        elif event.type == QUIT:
            running = False
        


    # Fill the background with white

    # Flip the display
    pygame.display.flip()
    screen.blit(ship_surf)
    pygame.time.wait(60)

# Done! Time to quit.

pygame.quit()