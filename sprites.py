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
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        # animation variables
        self.walking = False
        self.jumping = False
        self.falling = False
        self.current_frame = 0
        self.last_update = 0
        # sprite variables
        self.load_images()
        self.image = self.standing_frames_r[0]
        # physics variables
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        

    def load_images(self):
        # Adjustments needed for the xeon spritesheet, beacuse it has too much padding
        X_ADJUSTMENT = 24
        Y_ADJUSTMENT = 20
        WIDTH_ADJUSTMENT = -48
        HEIGHT_ADJUSTMENT = -44
        load = self.game.xeon_spritesheet.get_image

        self.standing_frames_r = [
            load(96+X_ADJUSTMENT, 0+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT)
        ]
        self.walking_frames_r = [
            load(0+X_ADJUSTMENT, 480+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(96+X_ADJUSTMENT, 480+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(192+X_ADJUSTMENT, 480+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(288+X_ADJUSTMENT, 480+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(384+X_ADJUSTMENT, 480+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(0+X_ADJUSTMENT, 576+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(96+X_ADJUSTMENT, 576+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(192+X_ADJUSTMENT, 576+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(288+X_ADJUSTMENT, 576+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
            load(384+X_ADJUSTMENT, 576+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
        ]
        self.jumping_frames_r = [
                load(0+X_ADJUSTMENT, 96+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(96+X_ADJUSTMENT, 96+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(192+X_ADJUSTMENT, 96+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(288+X_ADJUSTMENT, 96+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(384+X_ADJUSTMENT, 96+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(0+X_ADJUSTMENT, 192+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(96+X_ADJUSTMENT, 192+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(192+X_ADJUSTMENT, 192+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(288+X_ADJUSTMENT, 192+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
                load(384+X_ADJUSTMENT, 192+Y_ADJUSTMENT, 96+WIDTH_ADJUSTMENT, 96+HEIGHT_ADJUSTMENT),
        ]

        # flip all frames
        self.standing_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.standing_frames_r))
        self.walking_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.walking_frames_r))
        self.jumping_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.jumping_frames_r))

        # Set key colors
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_frames_r))

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

        # Check if the player is walking
        if int(self.vel.x)==0:
            self.walking = False
        else:
            self.walking = True
        
        # Check if player is jumping of falling
        if int(self.vel.y)<0:
            self.jumping = True
            self.falling = False
        elif int(self.vel.y)>0:
            self.jumping = False
            self.falling = True
        else:
            self.jumping = False
            self.falling = False
        

    def jump(self):
        # jump only if standing on a platform
        # detect two pixels below the player
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2 
        if hits:
            self.vel.y = PLAYER_JUMP
    
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < PLAYER_JUMP//2:
                self.vel.y = PLAYER_JUMP//2

    
    def animate(self):
        now = pg.time.get_ticks()
        def show_continuous_animation(frame_list):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(frame_list)
            self.image = frame_list[self.current_frame]
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        
        def show_linear_animation(frame_list):
            self.last_update = now
            self.current_frame = min(self.current_frame + 1, len(frame_list) -1)
            self.image = frame_list[self.current_frame]
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 100:
                if self.vel.x>0:
                    show_continuous_animation(self.standing_frames_r)
                elif self.vel.x<0:
                    show_continuous_animation(self.standing_frames_l)
        
        # show jump animation
        if self.jumping:
            if now - self.last_update > 50:
                if self.vel.x>0:
                    show_linear_animation(self.jumping_frames_r[:6])
                elif self.vel.x<0:
                    show_linear_animation(self.jumping_frames_l[:6])

        # show falling animation
        elif self.falling:
            if now - self.last_update > 50:
                if self.vel.x>0:
                    show_linear_animation(self.jumping_frames_r[6:8])
                elif self.vel.x<0:
                    show_linear_animation(self.jumping_frames_l[6:8])

        # show walking animation
        elif self.walking:
            if now - self.last_update > 50:
                if self.vel.x>0:
                    show_continuous_animation(self.walking_frames_r)
                elif self.vel.x<0:
                    show_continuous_animation(self.walking_frames_l)


        
            

class Coin(pg.sprite.Sprite):
    def __init__(self, game,x,y, color="green"):
        super().__init__()
        self.game = game
        self.color = color
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.set_value()

    def load_image(self):
        load = self.game.coin_spritesheet.get_image
        if self.color == "green":
            self.image = load(0, 0, 64, 64)
        if self.color == "blue":
            self.image = load(64, 0, 64, 64)
        if self.color == "yellow":
            self.image = load(128, 0, 64, 64)
        if self.color == "red":
            self.image = load(192, 0, 64, 64)
        self.image.set_colorkey(BLACK)

    def set_value(self):
        if self.color == "green":
            self.value = 50
        if self.color == "blue":
            self.value = 100
        if self.color == "yellow":
            self.value = 200
        if self.color == "red":
            self.value = 500

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TiledPlatform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.rect = pg.Rect(x,y,w,h)
        self.rect.x = x
        self.rect.y = y