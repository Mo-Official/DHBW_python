import pygame
import random
import os

# system stats
game_path = os.path.dirname(__file__)
assets_path = os.path.join(game_path, "assets")

# window stats
WIDTH = 1080
HEIGHT = 800
TITLE = "My Game"
FPS = 30

# colors
WHITE = (255,255,255)
TESTCOLOR = (205,205,205)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
BROWN = (160,82,45)
CYAN = (224,255,255)


# general stats
PLAYER_HR_ACC = 10
FRIC = 0.5
GRAVITY = 10
PLAYER_VR_ACC = -GRAVITY*5
PLAYER_VR_SPEED_LIMIT = PLAYER_VR_ACC * 3



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(assets_path, "idle.png")).convert()
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 1.7
        # Span Coordinations
        self.rect.center = (WIDTH//3, HEIGHT//3)
        self.speedx = 0
        self.speedy = 0
        self.falling = True
        self.doubleJump = False

    def update(self):
        colliding = pygame.sprite.spritecollide(self, all_platforms, False, )
        keyState = pygame.key.get_pressed()
        if colliding:
            self.speedy = 0
            self.falling = False
            self.rect.bottom = colliding[0].rect.top+1 # +1 is needed otherwise the player keeps bouncing
            if keyState[pygame.K_SPACE]:
                self.speedy += PLAYER_VR_ACC
        else:
            self.falling = True

        if self.falling:
            self.speedy += GRAVITY

        if keyState[pygame.K_a]:
            self.speedx -= PLAYER_HR_ACC

        elif keyState[pygame.K_d]:
            self.speedx += PLAYER_HR_ACC
        else:
            self.speedx = 0
        self.speedx *= FRIC
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #spawn coordinations
        self.rect.left = x
        self.rect.bottom = y


# init game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# manage sprites
all_sprites = pygame.sprite.Group()
all_platforms = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# game map


game_map = [
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","2","2","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","1","1","0","0","0","0","0","0","0","0","2","2","2","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","1","1","1","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","2","2","0"],
    ["2","2","2","2","2","2","0","0","0","0","2","2","2","2","1","1","0"],
    ["1","1","1","1","1","1","0","2","2","0","1","1","1","1","1","1","0"],
    ["1","1","1","1","1","1","0","1","1","0","1","1","1","1","1","1","2"],
    ["1","1","1","1","1","1","0","0","0","0","1","1","1","1","1","1","1"],
    ["1","1","1","1","1","1","0","0","0","0","1","1","1","1","1","1","1"],
    ["1","1","1","1","1","1","0","0","0","0","1","1","1","1","1","1","1"],
    ["1","1","1","1","1","1","0","0","0","0","1","1","1","1","1","1","1"],
]


# assets
TILE_SIZE = 64
for y_pos, y in enumerate(game_map):
    for x_pos, x in enumerate(game_map[y_pos]):
        if x == "0":
            pass
        elif x == "1":
            platform = Platform(x_pos*TILE_SIZE,y_pos*TILE_SIZE,TILE_SIZE, BROWN)
            all_sprites.add(platform)
        elif x == "2":
            platform = Platform(x_pos*TILE_SIZE,y_pos*TILE_SIZE,TILE_SIZE, GREEN)
            all_platforms.add(platform)
            all_sprites.add(platform)



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
    if player.rect.top > HEIGHT:
        running = False


    # render and draw
    screen.fill(TESTCOLOR)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, RED, player.rect)
    # after drawing everythin
    pygame.display.flip()

pygame.quit()
