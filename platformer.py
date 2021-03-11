import sys
import random
import pygame
from pygame import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10,420))
        
        self.pos = vec((10,HEIGHT-20))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0,GRAVITY)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms,False)
        if hits:
            self.vel.y = -15
    
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top +1
                self.vel.y = 0
        

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100),12))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))

def plat_gen():
    while len(platforms) < 7 :
        width = random.randrange(50,100)
        p  = Platform()             
        p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH  = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
GRAVITY = 0.5
JUMP = -15

FramePerSec = pygame.time.Clock()

displaySurface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Platformer")

PT1=Platform()
PT1.surf = pygame.Surface((WIDTH,20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH//2, HEIGHT -10))

P1=Player()

platforms = pygame.sprite.Group()
platforms.add(PT1)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

for x in range(random.randint(5,6)):
    pl = Platform()
    platforms.add(pl)
    all_sprites.add(pl)


game_running = True

while game_running:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displaySurface.fill((0,0,0))
    
    
    if P1.rect.top <= HEIGHT // 3:
        P1.pos.y += abs(P1.vel.y)
        plat_gen()
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    P1.move()
    P1.update()

    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
