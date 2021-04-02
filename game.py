import pygame
import random
import os

# system stats
game_path = os.path.dirname(__file__)
assets_path = os.path.join(game_path, "assets")

# window stats
WIDTH = 1024
HEIGHT = 640
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
GRAVITY = 5
PLAYER_VR_ACC = -40
PLAYER_VR_SPEED_LIMIT = PLAYER_VR_ACC * 3



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(assets_path, "idle.png")).convert()
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # Span Coordinations
        self.rect.center = (0,0)
        self.speedx = 0
        self.speedy = 0
        self.falling = True
        self.doubleJump = False

    def move(self):
        collisions = pygame.sprite.spritecollide(self, game_map.all_platforms, False)
        keyState = pygame.key.get_pressed()
        if collisions:
            self.speedy = 0
            if not game_map.unwalkable_platforms.has(collisions[0]):
                self.falling = False
                self.rect.bottom = collisions[0].rect.top+1 # +1 is needed otherwise the player keeps bouncing
            if keyState[pygame.K_SPACE]:
                self.speedy += PLAYER_VR_ACC
        else:
            self.falling = True

        if self.falling:
            self.speedy += GRAVITY

        if keyState[pygame.K_a]:
            self.speedx = -PLAYER_HR_ACC

        elif keyState[pygame.K_d]:
            self.speedx = PLAYER_HR_ACC
        else:
            self.speedx = 0

        game_map.scroll["x"]=self.rect.x
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def update(self):
        self.move()
        

# init game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# manage sprites
all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# game map
map_folder = os.path.join(game_path, "maps")

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color, TILE_SIZE):
        super().__init__()
        self.image = pygame.Surface(TILE_SIZE)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #spawn coordinations
        self.rect.left = x
        self.rect.bottom = y

class Map():
    def __init__(self, map_path):
        self.map = self.load_map(map_path)
        self.all_platforms = pygame.sprite.Group()
        self.unwalkable_platforms = pygame.sprite.Group()
        self.TILE_SIZE = (WIDTH//32, HEIGHT//20)
        self.scroll = {"x":0,"y":0}

    def load_map(self, mapName):
        with open(os.path.join(map_folder, mapName), "r") as fh:
            return fh.read().split("\n")
    
    def get_chunk(self, x,y):
        pass

    def clear_map(self):
        for platform in self.all_platforms:
            platform.kill()


    def render_chunk(self):
        self.clear_map()
        for y_pos, _ in enumerate(self.map):
            for x_pos, x in enumerate(self.map[y_pos]):
                if x == "0":
                    pass
                elif x == "1":
                    platform = Platform(
                        x=x_pos*self.TILE_SIZE[0]-self.scroll["x"],
                        y=y_pos*self.TILE_SIZE[1]-self.scroll["y"],
                        color=BROWN,
                        TILE_SIZE=self.TILE_SIZE)
                    self.unwalkable_platforms.add(platform)
                    self.all_platforms.add(platform)
                    all_sprites.add(platform)
                elif x == "2":
                    platform = Platform(
                        x=x_pos*self.TILE_SIZE[0]-self.scroll["x"],
                        y=y_pos*self.TILE_SIZE[1]-self.scroll["y"],
                        color=GREEN,
                        TILE_SIZE=self.TILE_SIZE)
                    self.all_platforms.add(platform)
                    all_sprites.add(platform)

game_map = Map("test.txt")
game_map.render_chunk()


        


# assets




# flow control
running = True
platformerMode = True

def switch_mode():
    global platformerMode
    if platformerMode:
        platformerMode = False
    else:
        platformerMode = True
    
    for x in range(100):
        clock.tick(FPS*100000000)
        pygame.draw.circle(screen, BLACK, (WIDTH//2, HEIGHT//2),x)
        print(x)

while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # process input (event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
            # if event.key == pygame.K_s:
            #   switch_mode()

    
    if platformerMode:
        
        # update logic

        game_map.render_chunk()
        all_sprites.update()

            # render and draw
        screen.fill(TESTCOLOR)
        all_sprites.draw(screen)
        # after drawing everythin
        pygame.display.flip()
    else:
        #screen.fill(BLACK)
        pygame.display.flip()


pygame.quit()
