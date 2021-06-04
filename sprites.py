f"""
AUTHOR
------
    Mouaz Tabboush

NAME
----
    sprites

DESCRIPTION
-----------
    sprites - a submodule containing classes for the game's objects
    =====================================================================
    **sprites** is a submodule for the game containing classes for any objects that the player sees and require game logic
    each class has their own **update()** method which is called in the main game loop.
    in most casses object methods are called instead in the update method and not in the main game loop.

CONTENT
-------
    * Player
    * Projectile
    * BaseEnemy
    * HealthDrop
    * TiledPlatform

REQUIREMENTS
------------
    * pygame
    * random
    * settings
    * util

VERSION
-------
    1.0

"""
from os import listdir
from os.path import isfile, join
import random

from pygame.constants import K_d, K_e
from util import debug, print_log
import pygame as pg
from pygame import Surface, key, mask, sprite
from pygame.mixer import fadeout

from settings import *

vec = pg.math.Vector2

class Spritesheet: # to be moved to util
    """
    Spritesheet
    -----------------
        A utility class for loading spritesheets as an entier image.

    Methods
    -----------------
    * get_image(x,y,w,h) -> Surface

    """
    # utility class for loading and parsing spritesheets
    @debug
    def __init__(self, filename) -> None:
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert()
    @debug
    def get_image(self, x, y, w, h) -> Surface:
        # grab an image out of a larger spritesheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0,0), (x,y,w,h))

        # some spritesheet need custome scalling
        if self.filename == XEON_SPRITESHEET:
            image = pg.transform.scale2x(image)
        if self.filename == BULLETS_SPRITESHEET:
            image = pg.transform.scale2x(image)
        return image
    
    

class Image_collection:# to be moved to util
    @debug
    def __init__(self, filename) -> None:
        self.filename = filename
        self.images = self.load_images_from_file(filename)
    @debug
    def get_image(self, name) -> Surface:
        try:
            return self.images[name]
        except Exception:
            print_log(f"ERROR:<Image_collection.get_image>:Image {name} not found!")
            print_log(f"ERROR:<Image_collection.get_image>:Returning a Empty Surface instead!")
            return Surface((50,100))
    @debug
    def load_images_from_file(self, filepath):
        images = {}
        for f in listdir(filepath):
            print_log("INFO:<Image_collection.load_images_from_file>:Loading ..." + join(filepath, f)[-30:])
            try:
                if f == ".DS_Store":
                    continue
                images[f] = pg.transform.scale2x(pg.image.load(join(filepath, f)).convert())
            except Exception as err:
                print_log("ERROR:<Image_collection.load_images_from_file>:can't import ", join(filepath, f))
        return images


class Player(sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        # animation variables
        self.walking: bool = False
        self.facing_right: bool = True
        self.jumping: bool = False
        self.falling: bool = False
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
        self.animation_flags = {"walk": False, "jump": False, "fall": True,"shoot": False, "face_right": True}
        # abilities
        self.health = PLAYER_HEALTH
        self.taking_damage = False
        self.shooting_locked = False
        self.shoot_cooldown = SHOOT_COOLDOWN
        self.last_shot = pg.time.get_ticks()
        self.last_damge = pg.time.get_ticks()
        
    @debug
    def load_images(self):
        load = self.game.xeon_image_collection.get_image

        self.standing_frames_r = [
            load("xeon_idle_1.png")
        ]
        self.walking_frames_r = [
            load("xeon_walking_1.png"),
            load("xeon_walking_2.png"),
            load("xeon_walking_3.png"),
            load("xeon_walking_4.png"),
            load("xeon_walking_5.png"),
            load("xeon_walking_6.png"),
            load("xeon_walking_7.png"),
            load("xeon_walking_8.png"),
            load("xeon_walking_9.png"),
            load("xeon_walking_10.png"),
        ]
        self.jumping_frames_r = [
                load("xeon_jumping_1.png"),
                load("xeon_jumping_2.png"),
                load("xeon_jumping_3.png"),
                load("xeon_jumping_4.png"),
                load("xeon_jumping_5.png"),
                load("xeon_jumping_6.png"),
                load("xeon_jumping_7.png"),
                load("xeon_jumping_8.png"),
                load("xeon_jumping_9.png"),
                load("xeon_jumping_10.png"),
        ]

        # loading the shooting frames
        self.standing_shooting_frames_r = [
                load("xeon_idle_shooting_1.png"),
                load("xeon_idle_shooting_2.png"),
                load("xeon_idle_shooting_3.png"),
        ]

        self.jumping_shooting_frames_r = [
                load("xeon_jumping_shooting_1.png"),
                load("xeon_jumping_shooting_2.png"),
                load("xeon_jumping_shooting_3.png"),
                load("xeon_jumping_shooting_4.png"),
                load("xeon_jumping_shooting_5.png"),
                load("xeon_jumping_shooting_6.png"),
                load("xeon_jumping_shooting_7.png"),
                load("xeon_jumping_shooting_8.png"),
                load("xeon_jumping_shooting_9.png"),
                load("xeon_jumping_shooting_10.png"),
        ]

        self.walking_shooting_frames_r = [
                load("xeon_walking_shooting_1.png"),
                load("xeon_walking_shooting_2.png"),
                load("xeon_walking_shooting_3.png"),
                load("xeon_walking_shooting_4.png"),
                load("xeon_walking_shooting_5.png"),
                load("xeon_walking_shooting_6.png"),
                load("xeon_walking_shooting_7.png"),
                load("xeon_walking_shooting_8.png"),
                load("xeon_walking_shooting_9.png"),
                load("xeon_walking_shooting_10.png")
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

    def update_movement_flags(self):
        if self.vel.x//1 > 0:
            self.movement_flags["right"] = True
        elif self.vel.x//1 < 0:
            self.movement_flags["left"] = True
        else:
            self.movement_flags["right"] = False
            self.movement_flags["left"] = False
        if self.vel.y//1 > 0:
            self.movement_flags["up"] = True
        elif self.vel.y//1 < 0:
            self.movement_flags["down"] = True
        else:
            self.movement_flags["up"] = False
            self.movement_flags["down"] = False

    def update_animation_flags(self):
        if self.movement_flags["right"] or self.movement_flags["left"]:
            self.animation_flags["walk"] = True
        else:
            self.animation_flags["walk"] = False
        
        if self.movement_flags["up"]:
            self.animation_flags["jump"] = True
        else:
            self.animation_flags["jump"] = False

        if self.movement_flags["down"]:
            self.animation_flags["fall"] = True
        else:
            self.animation_flags["fall"] = False

        if self.movement_flags["right"]:
            self.animation_flags["face_right"] = True
        elif self.movement_flags["left"]:
            self.animation_flags["face_right"] = False

        if self.shooting_locked:
            self.animation_flags["shoot"] = False
        

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
        
        
        keyState = key.get_pressed()
                
        self.animate()
        # apply shooting
        if keyState[pg.K_k] and not self.shooting_locked:
            self.animation_flags["shoot"] = True
            self.shooting_locked = True
            self.shot()
        else:
            self.animation_flags["shoot"] = False
            self.animation_flags["shoot"] = self.animation_flags["shoot"]
        
        #h-movement
        self.acc = vec(0,0)
        if keyState[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keyState[pg.K_d]:
            self.acc.x = PLAYER_ACC
        self.move_x()
        # apply collision with platforms on the x
        platforms = self.game.platforms
        platform_hits = sprite.spritecollide(self, platforms, False)
        if platform_hits:
            # handel x collisions             
            for hit in platform_hits:
                if self.movement_flags["left"]:
                    self.collision_flags["left"] = True
                    self.movement_flags["left"] = False
                    self.rect.left = hit.rect.right
                    self.pos.x = self.rect.midbottom[0]
                    self.vel.x = 0
                    self.acc.x = 0
                elif self.movement_flags["right"]:
                    self.collision_flags["right"] = True
                    self.movement_flags["right"] = False
                    self.rect.right = hit.rect.left
                    self.pos.x = self.rect.midbottom[0]
                    self.vel.x = 0
                    self.acc.x = 0
                else:
                    self.collision_flags["left"] = False
                    self.collision_flags["right"] = False

        self.update_movement_flags()
        
        # apply gravity
        self.acc = vec(0,PLAYER_GRAVITY)
        if keyState[pg.K_SPACE] and not self.movement_flags["up"]:
            self.jump()
        self.move_y()

        # apply collision with platforms on the y
        platforms = self.game.platforms
        platform_hits = sprite.spritecollide(self, platforms, False)
        if platform_hits:
            # handel x collisions             
            for hit in platform_hits:
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

        self.update_movement_flags()
        self.update_animation_flags()
  
    def shot(self):
        # create new projectile
        # add it to game.player_projectiles
        # set player.shooting to true
        if not self.facing_right:
            x_offset = self.rect.left
            y_offset = self.rect.y + self.rect.height//3
            x_vel = -10
        else:
            x_offset = self.rect.right
            y_offset = self.rect.y + self.rect.height//3
            x_vel = 10

        projectile = Projectile(x_offset, y_offset, x_vel, self.facing_right, self)
        self.game.player_projectiles.add(projectile)
        self.game.all_sprites.add(projectile)

    def take_damage(self, amount):
        now = pg.time.get_ticks()
        if now - self.last_damge > PLAYER_INVULNERABILITY:
            self.taking_damage = False
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
            pos = self.pos
            self.image = frame_list[self.current_frame]
            #self.rect = self.image.get_rect()
            self.pos = pos
        
        def show_linear_animation(frame_list):
            self.last_update = now
            self.current_frame = min(self.current_frame + 1, len(frame_list) -1)
            pos = self.pos
            self.image = frame_list[self.current_frame]
            #self.rect = self.image.get_rect()
            self.pos = pos

        
        # show jump animation
        if self.animation_flags["jump"]:
            if self.animation_flags["shoot"]:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_continuous_animation(self.jumping_shooting_frames_r[:6])
                    elif not self.animation_flags["face_right"]:
                        show_continuous_animation(self.jumping_shooting_frames_l[:6])
                if self.current_frame == len(self.standing_frames_r[:6]) - 1:
                    self.animation_flags["shoot"] = False
            else:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_linear_animation(self.jumping_frames_r[:6])
                    elif not self.animation_flags["face_right"]:
                        show_linear_animation(self.jumping_frames_l[:6])

        # show falling animation
        elif self.falling:
            if self.animation_flags["shoot"]:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_continuous_animation(self.jumping_shooting_frames_r[6:8])
                    elif not self.animation_flags["face_right"]:
                        show_continuous_animation(self.jumping_shooting_frames_l[6:8])
                if self.current_frame == len(self.jumping_shooting_frames_l[6:8]) - 1:
                    self.animation_flags["shoot"] = False
            else:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_linear_animation(self.jumping_frames_r[6:8])
                    elif not self.animation_flags["face_right"]:
                        show_linear_animation(self.jumping_frames_l[6:8])

        # show walking animation
        elif self.animation_flags["walk"] and not self.taking_damage:
            if self.animation_flags["shoot"]:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_continuous_animation(self.walking_shooting_frames_r)
                    elif not self.animation_flags["face_right"]:
                        show_continuous_animation(self.walking_shooting_frames_l)
                if self.current_frame == len(self.walking_shooting_frames_r) - 1:
                    self.animation_flags["shoot"] = False
            else:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_continuous_animation(self.walking_frames_r)
                    elif not self.animation_flags["face_right"]:
                        show_continuous_animation(self.walking_frames_l)
        else:
            if self.animation_flags["shoot"]:
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_continuous_animation(self.standing_shooting_frames_r)
                    elif not self.animation_flags["face_right"]:
                        show_continuous_animation(self.standing_shooting_frames_l)
                if self.current_frame == len(self.standing_shooting_frames_r) - 1:
                    self.animation_flags["shoot"] = False
            else: 
                if now - self.last_update > 50:
                    if self.animation_flags["face_right"]:
                        show_continuous_animation(self.standing_frames_r)
                    elif not self.animation_flags["face_right"]:
                        show_continuous_animation(self.standing_frames_l)


class Projectile(sprite.Sprite):
    def __init__(self, x, y, x_vel, facing_right, shooter):
        super().__init__()
        self.shooter = shooter
        self.game = shooter.game
        self.load_images()
        self.image =  self.right_frames[0] if facing_right else self.left_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = vec(x_vel, 0)
        self.facing_right = facing_right
        self.init_x_pos = x
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
    @debug
    def load_images(self):
        MARGIN_RIGHT = 1
        HEIGHT = 7
        WIDTH = 16
        load = self.game.bullets_spritesheet.get_image
        self.right_frames = [
            load(0*WIDTH, 0, WIDTH-MARGIN_RIGHT, HEIGHT),
            load(1*WIDTH, 0, WIDTH-MARGIN_RIGHT, HEIGHT),
            load(2*WIDTH, 0, WIDTH-MARGIN_RIGHT, HEIGHT),
            load(3*WIDTH, 0, WIDTH-MARGIN_RIGHT, HEIGHT),
            load(4*WIDTH, 0, WIDTH-MARGIN_RIGHT, HEIGHT),
        ]
        self.left_frames = list(map(lambda x: pg.transform.flip(x,True,False),self.right_frames))

        # Set key color
        # TODO: This can be done a bit more elligantly
        list(map(lambda x: x.set_colorkey(BLACK),self.right_frames))
        list(map(lambda x: x.set_colorkey(BLACK),self.left_frames))
        

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            if self.facing_right:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_frames)
                self.image = self.right_frames[self.current_frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
            else:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_frames)
                self.image = self.left_frames[self.current_frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


    def update(self):
        self.animate()
        # kill after timer is over
        self.x_diff = abs(self.init_x_pos - self.rect.x)
        if self.x_diff > SHOT_KILL_DISTANCE:
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



# debug decorators on this calss aer throwing an error for some reason
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
    @debug
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
