import pygame as pg
from pygame import Surface, time, mixer, sprite

from settings import *
from sprites import *
from tilemap import *
from util import *

__doc__ = """
    Author: Mouaz Tabboush

    main - the main module for the game
    ===================================

    **main** is the main module for running the game containing a the Game class which saves all game attributes inside one object.
    the Game class has a **run** methods which calls runs the main game loop.

    main only contains one class as a wrapper for the game loop.



    Requirements
    ============

    * pygame
    * os
    * xml.etree.ElementTree
    * settings
    * sprites
    * tilemap
    * util


    Other Info
    ===================================

    * The template of this project and some code snippets are based on this tutorial:
    https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq

    * Camera movement is based on this tutorial:
    https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i

    * Please refer to readme.md for credits of the game assets
"""

import os
import xml.etree.ElementTree as ET

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


class Game:
    """
    Description
    -----------
    A base class to represent a game.
    This class is **only** meant as a wrapper for the game.
    you should **not** create more that one instance of this class

    Attributes
    ----------

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
    @debug
    def __init__(self):
        """__init__ methode of game class that starts pygame and loads data"""
        print_log("STARTED A GAME")

        print_log("DEFINING VARIABLE TYPES")
        # type definitions for asset variables
        self.xeon_image_collection: Image_collection
        self.bullets_spritesheet: Spritesheet
        self.healthdrop_spritesheet: Spritesheet
        self.healthdrop_xmldata: ET.ElementTree
        self.main_menu_background: Surface
        self.map: TiledMap
        self.map_image: Surface
        self.map_rect: Rect
        self.intro_sound:mixer.Sound
        self.platformer_bg_sound:mixer.Sound

        # type definitions for game varaibles
        self.screen: pg.Surface
        self.clock: time.Clock
        self.running: bool

        # type definitions for game logic variables
        self.all_sprites : sprite.Group
        self.platforms : sprite.Group
        self.all_physics_objects : sprite.Group
        self.coins : sprite.Group
        self.player_projectiles : sprite.Group
        self.all_enemies : sprite.Group
        self.enemy_projectiles : sprite.Group
        self.camera : Camera

        print_log("STARTING PYGAME")
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = time.Clock()
        self.running = True
        self.load_data()

    @debug
    def load_data(self) -> None:
        """
        A function that wraps all game assets loading calls.
        Data is stored in game variables.
        """
        # load Xeon Spritesheet
        print_log("LOADING ASSETS...")
        print_log("LOADING PLAYER SPRITESHEET")
        self.xeon_image_collection = Image_collection(XEON_SPRITESHEET)

        print_log("LOADING BULLETS SPRITESHEET")
        self.bullets_spritesheet = Spritesheet(BULLETS_SPRITESHEET)

        print_log("LOADING HEALTHDROP SPRITESHEET")
        self.healthdrop_spritesheet = Spritesheet(HEALTHDROP_SPRITESHEET)
        self.healthdrop_xmldata = ET.parse(HEALTHDROP_XML_DATA)

        # load menu background
        print_log("LOADING BACKGROUND IMAGE SPRITESHEET")
        self.main_menu_background = pg.image.load(os.path.join(
            ASSETS_PATH, "main_menu_background.png")).convert()

        # load map
        print_log("LOADING MAP")
        # TODO: PASS THE LEVEL LOADED IS A PARAM
        self.map = TiledMap(LEVEL1_PATH)
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

        # load sounds
        print_log("LOADING SOUNDS")
        self.intro_sound = mixer.Sound(INTRO_SOUND_PATH)
        self.platformer_bg_sound = mixer.Sound(PLATFORMER_BG_SOUND_PATH)

        print_log("ASSETS LOADED SUCCESSFULLY", "SUCCESS")

    @debug
    def new(self):
        """
        runs code that starts a new game.
        this method sets up the enemies, player and coins before running the **run()** method.
        """

        print_log("<game.new>:STARTING A NEW GAME")

        print_log("<game.new>:SETTING UP GROUPS")
        # start the game
        self.all_sprites = sprite.Group()
        self.platforms = pg.sprite.Group()
        self.all_physics_objects = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player_projectiles = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.enemy_projectiles = pg.sprite.Group()

        # new camera
        print_log("<game.new>:SETTING UP CAMERA")
        self.camera = Camera(self.map.width, self.map.height)

        # create tile objects
        print_log("<game.new>:ADDED OBJECTS TO THE MAP")
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
                self.all_sprites.add(self.player)
            if tile_object.name == "platform":
                p = TiledPlatform(self, tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height)
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

    @debug
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
        # self.platformer_bg_sound.play()
        while self.playing:
            self.clock.tick(FPS)
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
        coin_hits = pg.sprite.spritecollide(
            self.player, self.coins, True, pg.sprite.collide_circle_ratio(0.5))
        for coin in coin_hits:
            self.player.health += 10

        # Mobs getting shot
        enemy_hits = pg.sprite.groupcollide(
            self.player_projectiles, self.all_enemies, True, False)
        for hit in enemy_hits:
            enemy_sprites = enemy_hits.get(hit)
            for enemy_sprite in enemy_sprites:
                enemy_sprite.kill()

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
        self.health_box = pg.Surface((300, 50))
        self.health_box.fill(BLACK)
        self.screen.blit(self.health_box, (0, 0))

        # Draw fbs
        self.fbs_box = pg.Surface((300, 50))
        self.fbs_box.fill(BLACK)
        self.screen.blit(self.fbs_box, (0, 0))
        self.draw_text("FPS: "+str(FPS), 32, (WHITE, BLACK), 150, 30)

        ## after everything ##
        pg.display.flip()


    def draw_text(self, text: str, size: int, color: Tuple[tuple, tuple], x: int, y: int, surface: pg.surface.Surface = None):
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
        # get the two arcade fonts
        font_in = pg.font.Font(FONT_ARCADE_IN, size)
        font_out = pg.font.Font(FONT_ARCADE_OUT, size)

        # render them to get two surfaces
        text_in_surface: Surface = font_in.render(text, True, color[0])
        text_out_surface: Surface = font_out.render(text, True, color[1])
        text_in_rect: Rect = text_in_surface.get_rect()
        text_out_rect: Rect = text_out_surface.get_rect()
        text_in_rect.topleft = (0, 0)
        text_out_rect.topleft = (0, 0)

        # create a final surface and blit the two surfaces on it
        text_surface = Surface(text_in_surface.get_size())
        text_surface.blit(text_in_surface, text_in_rect)
        text_surface.blit(text_out_surface, text_out_rect)

        # change position to match given x and y
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.x = x
        text_surface_rect.y = y

        # blit on the given surface if any are provided
        if surface is None:
            self.screen.blit(text_surface, text_surface_rect)
        else:
            surface.blit(text_surface, text_surface_rect)

        # return the text_surface so you dont have to draw it again.
        return text_surface, text_surface_rect

    @debug
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
        # self.intro_sound.play()
        self.screen.blit(self.main_menu_background,
                         self.main_menu_background.get_rect())

        self.draw_text("Press a key to play", 64,
                       (RED, BLACK), WIDTH/2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()
        self.intro_sound.fadeout(1000)
        self.show_start_text()

    @debug
    def show_start_text(self):
        # move text to a txt file
        text = """
        Year 2023. Sep. 21
        Human scientists finally invented
        the means for space exploration.
        One Scientist known as Alfred Baker

        Year 2034. Oct. 31

        Year 2171. Oct. 31

        Year 2171. Oct. 31

        Year 2171. Oct. 31

        Year 2171. Oct. 31

        Year 2171. Oct. 31
        """
        self.screen.fill(BLACK)
        complete_surface = Surface((WIDTH*2//3, HEIGHT*3))
        text_lines = []
        for index, line in enumerate(text.splitlines()):
            line = line.strip()
            text_surface, text_surface_rect = self.draw_text(
                line, 32, (WHITE, BLACK), x=0, y=32*index, surface=complete_surface)
            text_lines.append((text_surface, text_surface_rect))

        complete_surface_rect = complete_surface.get_rect()
        complete_surface_rect.topleft = (WIDTH//6, HEIGHT)

        print_log("STARTED INTRO")
        waiting = True
        # while the bot of the text surface has not reached the top of screen
        while waiting and complete_surface_rect.bottom > 0:
            # scroll text up
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

            self.clock.tick(60)
            complete_surface_rect.y -= 1
            complete_surface.blits(text_lines, False)
            self.screen.blit(complete_surface, complete_surface_rect)
            pg.display.flip()
        print_log("FINNISHED INTRO")

    @debug
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
            self.draw_text("Game Over", 64, (WHITE, BLACK), WIDTH/2, HEIGHT/4)
            self.draw_text(
                f"Your Score is {self.score}", 22, (WHITE, BLACK), WIDTH/2, HEIGHT/2)
            self.draw_text("Press a key to play again.", 22,
                           (WHITE, BLACK), WIDTH/2, HEIGHT * 3/4)
            pg.display.flip()
            self.wait_for_key()

    @debug
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

    @debug
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

    @debug
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
    @debug
    def get_outline(self, image, color=RED):
        """Returns an outlined image of the same size.  the image argument must
        either be a convert surface with a set colorkey, or a convert_alpha
        surface. color is the color which the outline will be drawn."""
        rect = image.get_rect()
        mask = pg.mask.from_surface(image)
        outline = mask.outline()
        outline_image = pg.Surface(rect.size).convert_alpha()
        outline_image.fill((0, 0, 0, 0))
        for point in outline:
            outline_image.set_at(point, color)
        return outline_image


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_over_screen()
    g.quit()
