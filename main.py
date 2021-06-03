import os
import xml.etree.ElementTree as ET

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg
from pygame import Surface

from settings import *
from sprites import *
from tilemap import *
from util import *

"""Main Game Script

Author:
    Name : MOUAZ TABBOUSH
    Date : 19.04.2020

File Description:
    This is the main file for the game.
    The Game class represents the whole loop for a pygame project.
    Each element in a pygame project e.g main-loop, update section, render section, event loop
    are neatly devided into methods that are run in the run method.

File Content:
    Classes:
        * Game

Dependancies:
    * pygame
    * random
    * os
    * xml.etree.ElementTree
    * settings.py
    * sprites.py
    * tilemap.py

Other:
    * The template of this project and some code snippets are based on this tutorial:
    https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
    * Camera movement is based on this tutorial:
    https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i
"""



class Game:
    """
    A base class to represent a game.


    Attributes
    ----------
    screen : object -> the main pygame display
    clock : object -> controls fps
    font_arial : object -> holds the arial font
    score : int -> holds player score (may be removed later)
    highscore : int -> holds highscore
    xeon_spritesheet : object -> holds images for xeon (Player Sprite)
    coin_spritesheet : object -> holds images for collectable (depricated)
    healthdrop_spritesheet : object -> holds images for collectables
    map : object -> renders tile images on each 64x64 surface from the tmx map
    map_image : object -> surface to hold the map image after calling map.render()
    map_rect : object -> the rect of the map_image
    intro_sound : object -> plays and stops the intro music
    platformer_bg_sound : object -> plays and stops the level bg music
    all_sprites : list -> list for the sprites. needed when applying an effect on all sprites
    platforms : list -> list for platforms. needed when checking for collisions with player and mobs
    all_physics_objects : list -> list for all objects that have gravity effect, excluds player
    coins : list -> list for all collectable coins/healthdrops
    player_projectiles : list -> list for all player projectiles.
    all_enemies : list -> list of all enemies
    enemy_projectiles : list -> list for all enemies projectiles.
    camera : object -> a camera object that applies a setoff for all objects
    player : object -> the player sprite.
    playing : boolean -> checks whether the user is playing a level or is on the menu
    running : boolean -> exits game if set to false 
    waiting : boolean -> flow control variable. pauses the game when set to true

    Methods
    -------
    load_data()
        Loads all game data like highscore, spritesheets and music
    new()
        runs the needed code when a game starts. runs code that only need to run once per round
    run()
        controls game loop and calls update(), events(), draw()
    update()
        updates game logic
    events()
        listens to player inputs and other events
    draw()
        draws on screen
    draw_text()
        utility method for drawing text on screen
    show_start_screen()
        shows start screen
    show_over_screen()
        shows over screen
    wait_for_key()
        pauses the game until a key is pressed
    kill_sprite_group()
        utility method for killing all sprites inside a group
    quit()
        quits game
    
    """
    def __init__(self):
        """__init__ methode of game class that starts pygame and loads data"""
        pg.init()
        pg.mixer.init()
        self.screen: pg.Surface = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_arial = pg.font.match_font(FONT_ARIAL)
        self.font_arcade_in = FONT_ARCADE_IN
        self.score = 0
        self.load_data()
        self.fps = FPS

    def load_data(self):
        """Loads all game data and assets.

        Constants are loaded from settings.py

        Parameters
        ----------
        none.

        Returns
        -------
        none.
        
        Rasises
        -------
        Exception
            can't load highscore
        """
        # load Highscore
        with open(HS_FILE, "r") as fh:
            try:
                self.highscore = int(fh.read())
            except Exception as e:
                self.highscore = 0
                print("Can't load Highscore")
                print(e)
        # load Xeon Spritesheet
        self.xeon_spritesheet = Spritesheet(XEON_SPRITESHEET)

        # load coin Spritesheet
        self.coin_spritesheet = Spritesheet(COIN_SPRITESHEET)
        self.bullets_spritesheet = Spritesheet(BULLETS_SPRITESHEET)
        self.healthdrop_spritesheet = Spritesheet(HEALTHDROP_SPRITESHEET)
        self.healthdrop_xmldata = ET.parse(HEALTHDROP_XML_DATA)

        # load menu background
        self.main_menu_background = pg.image.load(os.path.join(ASSETS_PATH, "main_menu_background.png")).convert()

        # load map
        self.map = TiledMap(LEVEL1_PATH) #TODO: PASS THE LEVEL LOADED IS A PARAM
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

        # load sounds
        self.intro_sound = pg.mixer.Sound(INTRO_SOUND_PATH)
        self.platformer_bg_sound = pg.mixer.Sound(PLATFORMER_BG_SOUND_PATH)


    def new(self):
        """runs code that starts a new gameplayer.
        this method sets up the assets, enemies, player and coins before running the run() method

        Constants needed are loaded from settings.py

        Parameters
        ----------
        none.

        Returns
        -------
        none.

        Rasises
        -------
        none.
        """
        # start the game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.all_physics_objects = pg.sprite.Group()
        #self.scorllable_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player_projectiles = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.enemy_projectiles = pg.sprite.Group()

        # new camera
        self.camera = Camera(self.map.width, self.map.height)

        # create tile objects
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
                self.all_sprites.add(self.player)
            if tile_object.name == "platform":
                p = TiledPlatform(self, tile_object.x,tile_object.y, tile_object.width, tile_object.height)
                self.platforms.add(p)
            if tile_object.name == "coin":
                c = HealthDrop(self, tile_object.x, tile_object.y)
                self.all_sprites.add(c)
                self.coins.add(c)
            if tile_object.name == "base_enemy":
                e = BaseEnemy(self, tile_object.x, tile_object.y)
                self.all_sprites.add(e)
                self.all_enemies.add(e)
                self.all_physics_objects.add(e)

        # create player 
        self.run()
        
        pass

    def run(self):
        """A simple function to control game loop

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        # Game Loop
        self.playing = True
        #self.platformer_bg_sound.play()
        while self.playing:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()
        self.platformer_bg_sound.fadeout(1000)

    def update(self):
        """Game.update

            This method updates logic between game objects.
            These are the mechanisms supported in this method:
                * platform collisions with the player.
                * platform collisions for the mobs
                * camera scrolling
                * player collision with enemy bullets
                * enemies collision with player bullets
                * player collecting coins
                * player death by getting health below zero
                * player fall off screen death

            Parameters
            ----------
            none.
            Returns 
            -------
            none.
            Rasises
            -------
            none.
        """
        # Game Loop - Update
        self.all_sprites.update()



        # New Camera Scrolling
        self.camera.update(self.player)
        # Player Coin Collecting
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, True, pg.sprite.collide_circle_ratio(0.5))
        for coin in coin_hits:
            self.player.health += 10

        # Player getting shot
        # with directional push effect.
        # fixme: add screenshake
        player_hits = pg.sprite.spritecollide(self.player, self.enemy_projectiles, True)
        if player_hits:
            self.player.vel += player_hits[0].vel // 5
            self.player.take_damage(10)

        # Mobs getting shot
        enemy_hits = pg.sprite.groupcollide(self.player_projectiles, self.all_enemies, True, False)
        for hit in enemy_hits:
            sprites = enemy_hits.get(hit)
            for sprite in sprites:
                sprite.kill()

        # Game Over:
        if self.player.rect.bottom > self.camera.height:
            self.playing = False
        if self.player.health < 10:
            self.playing = False

    def events(self):
        """ Method for controlling the event loop.
        the event that are handeled in this method are:
        * clicking on the exit button to exit the game
        * pressing the spacebar to jump
        * releasing the spacebar to cut the jump

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        # Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                if event.key == pg.K_k:
                    self.player.shooting_locked = False

    
    def draw(self):
        """ Method for drawing graphics, 
        applying the camera offset and showing the player health bar

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        # Game Loop - Draw
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.map_image, self.camera.apply(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            # draw sptite outline
            #self.screen.blit(self.get_outline(sprite.image), self.camera.apply(sprite))
            
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        # draw player outline
        #self.screen.blit(self.get_outline(self.player.image), self.camera.apply(self.player))
        
        # Draw Player Score
        self.health_box = pg.Surface((300,50))
        self.health_box.fill(BLACK)
        self.screen.blit(self.health_box, (0, 0))

        # Draw fbs
        self.fbs_box = pg.Surface((300,50))
        self.fbs_box.fill(BLACK)
        self.screen.blit(self.fbs_box, (0, 0))
        self.draw_text("FPS: "+str(self.fps), 32, (WHITE,BLACK), 150, 30)

        ## after everything ##
        pg.display.flip()

    def draw_text(self, text: str, size: int, color: Tuple[tuple,tuple], x: int, y: int, surface:pg.surface.Surface=None):
        """A method that draws a text of a surface or the main screen

        Parameters
        ----------
        text: string -> text to be drawn
        size: int -> size of the text
        color: tuple -> rgb color of the text
        x: int -> x coordinate of the text
        y: int -> y coordinate of the text
        surface: pg.surface.Surface ->  (optional) draws a text on a surface.

        Returns
        -------
        none.

        Rasises
        -------
        none.

        """
        font_in = pg.font.Font(FONT_ARCADE_IN, size)
        font_out = pg.font.Font(FONT_ARCADE_OUT, size)
        text_in_surface = font_in.render(text, True, color[0])
        text_out_surface = font_out.render(text, True, color[1])
        text_in_rect = text_in_surface.get_rect()
        text_in_rect.midtop = (x,y)
        text_out_rect = text_out_surface.get_rect()
        text_out_rect.midtop = (x,y)
        if surface is None:
            self.screen.blit(text_in_surface, text_in_rect)
            self.screen.blit(text_out_surface, text_out_rect)
        else:
            surface.blit(text_in_surface, text_in_rect)
            surface.blit(text_out_surface, text_out_rect)

    def show_start_screen(self):
        """ method that describes how the start screen look like

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        #self.intro_sound.play()
        screen_surface = Surface((WIDTH, HEIGHT))
        screen_surface.blit(self.main_menu_background, self.main_menu_background.get_rect())
        self.screen.blit(screen_surface, screen_surface.get_rect())

        self.draw_text("Press a key to play", 64, (RED,BLACK), WIDTH/2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()
        self.intro_sound.fadeout(1000)

    def show_over_screen(self):
        """ Method for describing how the game over screen look like

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        if self.running:
            self.kill_sprite_group(self.all_sprites)
            self.screen.fill(BG_COLOR)
            self.draw_text("Game Over", 64, (WHITE,BLACK), WIDTH/2, HEIGHT/4)
            self.draw_text(f"Your Score is {self.score}", 22, (WHITE,BLACK), WIDTH/2, HEIGHT/2)
            self.draw_text("Press a key to play again.", 22, (WHITE,BLACK), WIDTH/2, HEIGHT * 3/4)
            pg.display.flip()
            self.wait_for_key()   


    def wait_for_key(self):
        """ method that pauses the game until a key is pressed

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYUP:
                    waiting = False

    def kill_sprite_group(self, group: pg.sprite.Group):
        """ Method that kills all sprites in a group.

        Parameters
        ----------
        group: pg.sprite.Group -> group of sprites to be disposed of
        
        Returns
        -------
        none.
        
        Rasises
        -------
        none.
        """
        # kill all sprites in a to improve performance 
        for sprite in group:
            sprite.kill()

    def quit(self):
        """ Quits the game

        Parameters
        ----------
        none.
        Returns
        -------
        none.
        Rasises
        -------
        none.
        """
        # Close Game
        pg.quit()

    # SOURCE: https://pastebin.com/XXRngMZh
    def get_outline(self, image, color=RED):
        """Returns an outlined image of the same size.  the image argument must
        either be a convert surface with a set colorkey, or a convert_alpha
        surface. color is the color which the outline will be drawn."""
        rect = image.get_rect()
        mask = pg.mask.from_surface(image)
        outline = mask.outline()
        outline_image = pg.Surface(rect.size).convert_alpha()
        outline_image.fill((0,0,0,0))
        for point in outline:
            outline_image.set_at(point,color)
        return outline_image



if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_over_screen()
    g.quit()
    