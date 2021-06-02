"""Sprites:

    This script  does thsi and that

    any special cases

    any requirements

    The filed can be imported and contains the following classes:
        * Spritesheet - a utility class for loading sprites
        * Player  
"""
import random
import pygame as pg
from pygame import sprite, mask, key
import xml.etree.ElementTree as ET
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, w, h):
        # grab an image out of a larger spritesheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0,0), (x,y,w,h))

        # some spritesheet need custome scalling
        if self.filename == XEON_SPRITESHEET:
            image = pg.transform.scale2x(image)
        return image


class Player(sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        # animation variables
        self.walking: bool = False
        self.facing_right: bool = True
        self.jumping: bool = False
        self.falling: bool = False
        self.shooting: bool = False
        self.current_frame: int = 0
        self.last_update: int = 0
        # sprite variables
        self.load_images()
        self.image: pg.Surface = self.standing_frames_r[0]
        # physics variables
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.mask = mask.from_surface(self.image)
        self.movement_flags = {"up":False, "down":False, "left":False, "right":False}
        self.collision_flags = {"up":False, "down":False, "left":False, "right":False}
        # abilities
        self.health = PLAYER_HEALTH
        self.taking_damage = False
        

    def load_images(self):
        # Adjustments needed for the xeon spritesheet, beacuse it has too much padding
        X_ADJUSTMENT = 24
        Y_ADJUSTMENT = 20
        WIDTH_ADJUSTMENT = -36
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

        # loading the shooting frames
        self.standing_shooting_frames_r = [
            load(x=192+X_ADJUSTMENT, y=0+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=288+X_ADJUSTMENT, y=0+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=384+X_ADJUSTMENT, y=0+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
        ]

        self.jumping_shooting_frames_r = [
            load(x=0+X_ADJUSTMENT, y=288+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=96+X_ADJUSTMENT, y=288+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=192+X_ADJUSTMENT, y=288+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=288+X_ADJUSTMENT, y=288+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=384+X_ADJUSTMENT, y=288+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=0+X_ADJUSTMENT, y=384+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=96+X_ADJUSTMENT, y=384+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=192+X_ADJUSTMENT, y=384+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=288+X_ADJUSTMENT, y=384+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=384+X_ADJUSTMENT, y=384+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
        ]

        self.walking_shooting_frames_r = [
            load(x=0+X_ADJUSTMENT, y=672+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=96+X_ADJUSTMENT, y=672+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=192+X_ADJUSTMENT, y=672+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=288+X_ADJUSTMENT, y=672+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=384+X_ADJUSTMENT, y=672+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=0+X_ADJUSTMENT, y=768+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=96+X_ADJUSTMENT, y=768+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=192+X_ADJUSTMENT, y=768+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=288+X_ADJUSTMENT, y=768+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
            load(x=384+X_ADJUSTMENT, y=768+Y_ADJUSTMENT, w=96+WIDTH_ADJUSTMENT, h=96+HEIGHT_ADJUSTMENT),
        ]

        # flip all frames
        # TODO: This can be done a bit more elligantly
        self.standing_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.standing_frames_r))
        self.walking_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.walking_frames_r))
        self.jumping_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.jumping_frames_r))
        self.standing_shooting_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.standing_shooting_frames_r))
        self.walking_shooting_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.walking_shooting_frames_r))
        self.jumping_shooting_frames_l = list(map(lambda x: pg.transform.flip(x,True,False),self.jumping_shooting_frames_r))

        # Set key color
        # TODO: This can be done a bit more elligantly
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_shooting_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.standing_shooting_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_shooting_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.walking_shooting_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_frames_r))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_shooting_frames_l))
        list(map(lambda x: x.set_colorkey(XEON_SPRITESHEET_KEYCOLOR),self.jumping_shooting_frames_r))


    def move_x(self):
        # apply equation of motion
        self.movement_flags["left"] = False
        self.movement_flags["right"] = False
        # apply equation of motion
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        movement = self.vel + 0.5 * self.acc
        if self.vel.x//1 > 0:
            self.movement_flags["right"] = True
        elif self.vel.x//1 < 0:
            self.movement_flags["left"] = True
        self.pos.x += movement.x
        self.rect.midbottom = self.pos
    

    def move_y(self):
                # apply equation of motion
        self.movement_flags["up"] = False
        self.movement_flags["down"] = False
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        movement = self.vel + 0.5 * self.acc
        if movement.y//1 > 0:
            self.movement_flags["down"] = True
        elif movement.y//1 < 0:
            self.movement_flags["up"] = True
        self.pos.y += movement.y
        self.rect.midbottom = self.pos
    
        
    def update(self):
        
        self.animate()
        keyState = key.get_pressed()
                
        
        # apply shooting
        if keyState[pg.K_k]:
            self.last_shot = pg.time.get_ticks()
            if pg.time.get_ticks() - self.last_shot > 300:
                    self.shooting = False
            if not self.shooting:
                self.shooting = True
                self.shot()
        else:
            self.shooting = False
       
                
        """
        # control invulnerability
            now = pg.time.get_ticks()
            if self.taking_damage:
                if now - self.last_damge > PLAYER_INVULNERABILITY:
                    self.taking_damage = False
        """

        



        #h-movement
        self.acc = vec(0,0)
        if keyState[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        elif keyState[pg.K_d]:
            self.acc.x = PLAYER_ACC
        self.move_x()    

        # apply collision with platforms on the x
        platforms = self.game.platforms
        platform_hits = sprite.spritecollide(self, platforms, False)
        if platform_hits:
            # get only the mask collisions
            mask_cols = []
            for plt in platform_hits:
                mask_col = sprite.collide_mask(self, plt)
                if mask_col:
                    mask_cols.append(plt)
            # handel x collisions             
            for hit in mask_cols:
                if self.movement_flags["left"]:
                    self.collision_flags["left"] = True
                    self.movement_flags["left"] = False
                    self.rect.left = hit.rect.right
                    self.pos.x = self.rect.bottomleft[0] + (self.rect.width/2) - 20
                    self.vel.x = 0
                    self.acc.x = 0
                elif self.movement_flags["right"]:
                    self.collision_flags["right"] = True
                    self.movement_flags["right"] = False
                    self.rect.right = hit.rect.left
                    self.pos.x = self.rect.bottomright[0] - (self.rect.width/2) + 40
                    self.vel.x = 0
                    self.acc.x = 0
                else:
                    self.collision_flags["left"] = False
                    self.collision_flags["right"] = False
            
        
        # apply gravity
        self.acc = vec(0,PLAYER_GRAVITY)
        if keyState[pg.K_SPACE] and not self.movement_flags["up"]:
            self.jump()
        self.move_y()

        # apply collision with platforms on the y
        platforms = self.game.platforms
        platform_hits = sprite.spritecollide(self, platforms, False)
        if platform_hits:
            # get only the mask collisions
            mask_cols = []
            for plt in platform_hits:
                mask_col = sprite.collide_mask(self, plt)
                if mask_col:
                    mask_cols.append(plt)
            # handel x collisions             
            for hit in mask_cols:
                if self.movement_flags["up"]:
                    self.collision_flags["up"] = True
                    self.movement_flags["up"] = False
                    self.rect.top = hit.rect.bottom + 10
                    self.pos.y =  self.rect.bottom
                    self.vel.y = 0
                elif self.movement_flags["down"]:
                    self.collision_flags["down"] = True
                    self.movement_flags["down"] = False
                    self.rect.bottom = hit.rect.top
                    self.pos.y =  self.rect.bottom
                    self.vel.y = 0
                else:
                    self.collision_flags["up"] = False
                    self.collision_flags["down"] = False

        # Check if the player is walking and which way are they facing
        self.walking = True
        if self.movement_flags["right"]:
            self.facing_right = True
        elif self.movement_flags["left"]:
            self.facing_right = False
        else:
            self.walking = False

        
        # Check if player is jumping of falling
        if self.movement_flags["up"]:
            self.jumping = True
            self.falling = False
            self.walking = False
        elif self.movement_flags["down"]:
            self.jumping = False
            self.falling = True
            self.walking = False
        else:
            self.jumping = False
            self.falling = False
        
    def shot(self):
        # create new projectile
        # add it to game.player_projectiles
        # set player.shooting to true
        
        # BUG: For some reason self.rect.midleft/midright sometimes returns a wrong value
        if not self.facing_right:
            #shot_offset = self.rect.midleft
            shot_offset = (self.rect.x, self.rect.y)
            shot_vel = vec(-10,0)
        else:
            #shot_offset = self.rect.midright
            shot_offset = (self.rect.x, self.rect.y)
            shot_vel = vec(10,0)
        projectile = Projectile(*shot_offset, *shot_vel, self)
        self.game.player_projectiles.add(projectile)
        self.game.all_sprites.add(projectile)

    def take_damage(self, amount):
        if not self.taking_damage:
            self.taking_damage = True
            self.health -= amount
            self.last_damge = pg.time.get_ticks()
        

    def jump(self):
        # jump only if standing on a platform
        # detect two pixels below the player
        self.rect.y += 2
        hits = sprite.spritecollide(self, self.game.platforms, False)
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
            pos = self.pos
            self.rect = self.image.get_rect()
            self.pos = pos
        
        def show_linear_animation(frame_list):
            self.last_update = now
            self.current_frame = min(self.current_frame + 1, len(frame_list) -1)
            self.image = frame_list[self.current_frame]
            pos = self.pos
            self.rect = self.image.get_rect()
            self.pos = pos

        # show idle animation
        if not self.jumping and not self.walking and not self.taking_damage:
            if self.shooting:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_continuous_animation(self.standing_shooting_frames_r)
                    elif not self.facing_right:
                        show_continuous_animation(self.standing_shooting_frames_l)
            else: 
                if now - self.last_update > 100:
                    if self.facing_right:
                        show_continuous_animation(self.standing_frames_r)
                    elif not self.facing_right:
                        show_continuous_animation(self.standing_frames_l)
        
        # show jump animation
        if self.jumping:
            if self.shooting:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_continuous_animation(self.jumping_shooting_frames_r[:6])
                    elif not self.facing_right:
                        show_continuous_animation(self.jumping_shooting_frames_l[:6])
            else:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_linear_animation(self.jumping_frames_r[:6])
                    elif not self.facing_right:
                        show_linear_animation(self.jumping_frames_l[:6])

        # show falling animation
        if self.falling:
            if self.shooting:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_continuous_animation(self.jumping_shooting_frames_r[6:8])
                    elif not self.facing_right:
                        show_continuous_animation(self.jumping_shooting_frames_l[6:8])
            else:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_linear_animation(self.jumping_frames_r[6:8])
                    elif not self.facing_right:
                        show_linear_animation(self.jumping_frames_l[6:8])

        # show walking animation
        if self.walking and not self.taking_damage:
            if self.shooting:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_continuous_animation(self.walking_shooting_frames_r)
                    elif not self.facing_right:
                        show_continuous_animation(self.walking_shooting_frames_l)
            else:
                if now - self.last_update > 50:
                    if self.facing_right:
                        show_continuous_animation(self.walking_frames_r)
                    elif not self.facing_right:
                        show_continuous_animation(self.walking_frames_l)
        


        

class Projectile(sprite.Sprite):
    def __init__(self, x, y, x_vel, y_vel, shooter):
        super().__init__()
        self.shooter = shooter
        self.image = pg.Surface((50,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = vec(x_vel, y_vel)
        self.init_x_pos = x
        self.kill_distance = SHOT_KILL_DISTANCE


    def update(self):
        # kill after timer is over

        self.x_diff = abs(self.init_x_pos - self.rect.x)
        if self.x_diff > self.kill_distance:
            self.kill()
        # move in according to the vel
        self.rect.center += self.vel
        

class BaseEnemy(sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.image = pg.image.load(os.path.join(ASSETS_PATH, "enemy.png")).convert()
        self.image = pg.transform.scale2x(self.image)
        self.image.set_colorkey((77, 75, 118))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.game = game
        self.last_shot = pg.time.get_ticks()

    def move(self):
        """
        Applies the equation of motion to move the sprite on the x-aches
        """
        pass

    def jump(self):
        """
        Applies jumping in neccessary
        """
        pass

    def set_path(self):
        """
        figures out bunch of move instructions needed to get to a certain point
        """
        pass

    def shot(self):
        """
        Shot a projectile in a certain angle
        """
        projectile = Projectile(*self.rect.midleft, *vec(-20, 0), self)
        self.game.enemy_projectiles.add(projectile)
        self.game.all_sprites.add(projectile)
        pass

    def die(self):
        self.kill()

    def update(self):
        """
        Applies gravity, animates and determine behavior towards the player
        """
        # apply equation of motion
        self.acc = vec(0,PLAYER_GRAVITY)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        platform_hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for platform in platform_hits:
            self.pos.y = platform.rect.top + 1
            self.vel.y = 0

        now = pg.time.get_ticks()
        if now - self.last_shot > random.randint(1500,3000):
            self.shot()
            self.last_shot = pg.time.get_ticks()



class Coin(sprite.Sprite):
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
            self.image = load(0, 0, 64, 62)
        if self.color == "blue":
            self.image = load(64, 0, 64, 62)
        if self.color == "yellow":
            self.image = load(128, 0, 64, 62)
        if self.color == "red":
            self.image = load(192, 0, 64, 62)
        
        self.image.set_colorkey(COIN_SPRITESHEET_KEYCOLOR)

    def set_value(self):
        if self.color == "green":
            self.value = 50
        if self.color == "blue":
            self.value = 100
        if self.color == "yellow":
            self.value = 200
        if self.color == "red":
            self.value = 500

class HealthDrop(sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.load_images()
        self.last_update = 0
        self.image = self.frames[0]
        self.current_frame = 0
        # physics variables
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def load_images(self):
        def load_sprite_positions(xmldata):
            sprites = xmldata.findall("sprite")
            sprites_list = []
            for sprite in sprites:
                spriteinfo = (int(sprite.get("x")), int(sprite.get("y")), int(sprite.get("w")), int(sprite.get("h")))
                sprites_list.append(spriteinfo)
            return sprites_list

        load = self.game.healthdrop_spritesheet.get_image
        self.frames = list(map(lambda frame: load(*frame), load_sprite_positions(self.game.healthdrop_xmldata)))
        list(map(lambda frame: frame.set_colorkey(BLACK), self.frames))

    def animate(self):
        now = pg.time.get_ticks()
        def show_continuous_animation(frame_list):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(frame_list)
            self.image = frame_list[self.current_frame]
            midbottom = self.rect.midbottom
            self.rect = self.image.get_rect()
            self.rect.midbottom = midbottom

        # show animation
        if now - self.last_update > 50:
            show_continuous_animation(self.frames)

    def update(self):
        self.animate()


class Platform(sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TiledPlatform(sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.game = game
        self.image = pg.Surface((w,h))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)