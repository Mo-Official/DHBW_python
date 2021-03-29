import pygame
import random
import os

# window stats
WIDTH = 600
HEIGHT = 800
TITLE = "Shmup!"
FPS = 60

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)



# level stats
ACC = 5



# sprites classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # how the sprite looks like
        self.image = pygame.image.load(os.path.join(img_folder, "playerShip1_blue.png")).convert()
        self.image = pygame.transform.scale(self.image, (30,40))
        self.image.set_colorkey(BLACK)
        
        # how the sprite is enclosed
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)         
        # where the is located initiall
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 0



    def update(self):
        # handle friction
        self.speedx = 0
        # handel controls
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -ACC
        if keystate[pygame.K_d]:
            self.speedx = ACC
        
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > WIDTH - 10:
            self.rect.right = WIDTH - 10

        self.rect.x += self.speedx

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
     def __init__(self, imgIndex=1):
        super().__init__()
        # how the sprite looks like
        self.image = pygame.image.load(os.path.join(img_folder, f"enemyBlack{imgIndex}.png"))
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (30,40))
        # how the sprite is enclosed
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)        
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        # mob stats
        self.health = 2

     def update(self):
         self.rect.y += self.speedy
         if self.rect.top > HEIGHT:
             self.rect.x = random.randrange(WIDTH-self.rect.width)
             self.rect.y = random.randrange(-100, -40)
             self.speedy = random.randrange(1, 5)

     def reduce_health(self):
        self.health -=1
        if self.health == 0:
            self.kill()



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # how the sprite looks like
        self.image = pygame.image.load(os.path.join(img_folder, "laserBlue01.png")).convert()
        self.image.set_colorkey(BLACK)
        # how the sprite is enclosed
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
             self.kill()


# init game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# manage assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

background = pygame.image.load(os.path.join(img_folder, "black.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()



# managing sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8):
    m = Mob(random.randint(2,5))
    all_sprites.add(m)
    mobs.add(m)



# game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # process input (event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update logic
    all_sprites.update()


    # check if mob hits the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    if hits:
        running = False
    
    # kill mobs and bullets on collide
    hit_list = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hit_list:
        hit.reduce_health()

    for i in range(len(hit_list)):
        m = Mob(random.randint(2,5))
        all_sprites.add(m)
        mobs.add(m)



    # render and draw
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
        
    # after drawing everythin
    pygame.display.flip()

pygame.quit()