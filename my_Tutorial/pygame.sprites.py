import pygame
import random


# window stats
WIDTH = 800
HEIGHT = 600
TITLE = "My Game"
FPS = 30

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

# sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # how the sprite looks like
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        # how the sprite is enclosed
        self.rect = self.image.get_rect()
        # where the is located initiall
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x += 5
        # handle a 
        if self.rect.left > WIDTH:
            self.rect.right = 0

# init game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# managing sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)




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