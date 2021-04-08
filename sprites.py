from settings import *
import pygame as pg
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):        
        self.acc = vec(0,PLAYER_GRAVITY)
        keyState = pg.key.get_pressed()
        if keyState[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keyState[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # euqations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # TEMP: Player stays inside the screen instead of scrolling
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1 
        if hits:
            self.vel.y = PLAYER_JUMP

class Coin(pg.sprite.Sprite):
    def __init__(self,x,y, value=50):
        super().__init__()
        self.value = value
        self.image = pg.Surface((self.value//2,self.value//2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center= (x,y)
        

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    



