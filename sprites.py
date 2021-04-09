from settings import *
import pygame as pg
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))

        # some spritesheet need custome scalling
        if self.filename == XEON_SPRITESHEET:
            image = pg.transform.scale2x(image)

        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # animation variables
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        # sprite variables
        self.load_images()
        self.image = self.standing_frames_r[0]
        # physics variables
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        

    def load_images(self):
        load = self.game.spritesheet.get_image
        self.standing_frames_r = [
            load(96, 0, 96, 96)
        ]
        self.walking_frames_r = [
            load(0, 480, 96, 96),
            load(96, 480, 96, 96),
            load(192, 480, 96, 96),
            load(288, 480, 96, 96),
            load(384, 480, 96, 96),
            load(0, 576, 96, 96),
            load(96, 576, 96, 96),
            load(192, 576, 96, 96),
            load(288, 576, 96, 96),
            load(384, 576, 96, 96),
        ]
        self.jumping_frames_r = [
                load(0, 96, 96, 96),
                load(96, 96, 96, 96),
                load(192, 96, 96, 96),
                load(288, 96, 96, 96),
                load(384, 96, 96, 96),
                load(0, 192, 96, 96),
                load(96, 192, 96, 96),
                load(192, 192, 96, 96),
                load(288, 192, 96, 96),
                load(384, 192, 96, 96),
        ]

        # flip all frames
        self.standing_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.standing_frames_r))
        self.walking_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.walking_frames_r))
        self.jumping_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.jumping_frames_r))

        # Set key colors
        map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_frames_l)
        map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_frames_r)
        map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_frames_l)
        map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_frames_r)
        map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_frames_l)
        map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_frames_r)
        


    def update(self):
        self.animate()   
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

        # stats for the player
        if int(self.vel.x)==0:
            self.walking = False
        else:
            self.walking = True
        if int(self.vel.y)<0:
            self.jumping = True
        else:
            self.jumping = False


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

    
    def animate(self):
        now = pg.time.get_ticks()
        def show_animation(frame_list):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(frame_list)
            self.image = frame_list[self.current_frame]
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 50:
                if self.vel.x>0:
                    show_animation(self.standing_frames_r)
                elif self.vel.x<0:
                    show_animation(self.standing_frames_l)
        
        # show walking animation
        if self.walking:
            if now - self.last_update > 50:
                if self.vel.x>0:
                    show_animation(self.walking_frames_r)
                elif self.vel.x<0:
                    show_animation(self.walking_frames_l)

        if self.jumping:
            if now - self.last_update > 50:
                if self.vel.x>0:
                    show_animation(self.jumping_frames_r)
                elif self.vel.x<0:
                    show_animation(self.jumping_frames_l)

        
            

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
    



