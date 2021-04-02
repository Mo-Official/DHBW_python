from settings import *
import pygame as pg
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):
        self.acc = vec(0,0)
        keyState = pg.key.get_pressed()
        if keyState[pg.K_a]:
            self.acc.x = -0.5
        if keyState[pg.K_d]:
            self.acc.x = 0.5

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
