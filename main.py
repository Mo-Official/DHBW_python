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
    * ./assets
    * ./fonts
    * ./maps


    Other Info
    ==========
    * The template of this project and some code snippets are based on this tutorial:
    https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
    * Camera movement is based on this tutorial:
    https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i
    * Regarding Testing
    Most functions inside this File are meant as wrappers,
    therefore testcases are not mentioned here.
    To see planned testcases pleasse refer to `sprites.py` and `tilemap.py`
    * Please refer to `readme.md` for credits of the game assets
"""

import os
import xml.etree.ElementTree as ET

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

class Game:
    """
    Description
    -------------
    A base class to represent a game.
    This class is only meant as a wrapper for the game calls.
    you should not create more that one instance of this class

    Variables
    ----------

        For holding Spritsheets
        -----------------------
        - xeon_image_collection: Image_collection 
        - bullets_spritesheet: Spritesheet
        - healthdrop_spritesheet: Spritesheet
        - healthdrop_xmldata: ET.ElementTree
        - main_menu_background: Surface

        For holding the Map
        -------------------
        - map: TiledMap
        - map_image: Surface
        - map_rect: Rect
    
        For holding Sounds
        ------------------
        - intro_sound:mixer.Sound
        - platformer_bg_sound:mixer.Sound
    
        For controlling the flow
        ------------------------
        - clock: time.Clock
        - playing: bool
        - running: bool

        Game Objects
        ------------
        - screen: pg.Surface
        - all_sprites : sprite.Group
        - platforms : sprite.Group
        - all_physics_objects : sprite.Group
        - coins : sprite.Group
        - player_projectiles : sprite.Group
        - all_enemies : sprite.Group
        - enemy_projectiles : sprite.Group
        - camera : Camera
        - player : Player

        Variables that need to be refactored
        ------------------------------------
        - health_box: pg.Surface

    Methods
    -------
    - load_data()
    - load_map()
    - set_map()
    - new()
    - run()
    - update()
    - events()
    - draw()
    - draw_text()
    - show_start_screen()
    - show_over_screen()
    - scroll_text()
    - wait_for_key()
    - kill_sprite_group()
    - quit()
    """
    # type definitions for asset variables
    xeon_image_collection: Image_collection
    bullets_spritesheet: Spritesheet
    healthdrop_spritesheet: Spritesheet
    healthdrop_xmldata: ET.ElementTree
    main_menu_background: Surface
    map: TiledMap
    map_image: Surface
    map_rect: Rect
    intro_sound:mixer.Sound
    platformer_bg_sound:mixer.Sound

    # type definitions for pygame objects
    screen: pg.Surface
    clock: time.Clock

    # type definitions for logic objects
    all_sprites : sprite.Group
    platforms : sprite.Group
    all_physics_objects : sprite.Group
    coins : sprite.Group
    player_projectiles : sprite.Group
    all_enemies : sprite.Group
    enemy_projectiles : sprite.Group
    camera : Camera
    player : Player

    # type definitions for flow control variabales
    playing: bool
    running: bool

    # variables needed to be refractored
    health_box: pg.Surface

    @debug
    def __init__(self) -> None:
        """__init__ methode of game class that starts pygame"""
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
        """A function that wraps all game assets loading calls.
        Data is stored in game variables."""
        # load Xeon Spritesheet
        print_log("<game.run>:LOADING ASSETS...")
        print_log("<game.run>:LOADING PLAYER SPRITESHEET")
        self.xeon_image_collection = Image_collection(XEON_FRAMES)

        print_log("<game.run>:LOADING BULLETS SPRITESHEET")
        self.bullets_spritesheet = Spritesheet(BULLETS_SPRITESHEET)

        print_log("<game.run>:LOADING HEALTHDROP SPRITESHEET")
        self.healthdrop_spritesheet = Spritesheet(HEALTHDROP_SPRITESHEET)
        self.healthdrop_xmldata = ET.parse(HEALTHDROP_XML_DATA)

        # load menu background
        print_log("<game.run>:LOADING BACKGROUND IMAGE SPRITESHEET")
        self.main_menu_background = pg.image.load(
                                        os.path.join(ASSETS_PATH, "main_menu_background.png") # move to setting
                                        ).convert()

        # load map
        print_log("<game.run>:LOADING MAP")
        self.map, self.map_image, self.map_rect = self.load_map(LEVEL1_PATH)

        # load sounds
        print_log("<game.run>:LOADING SOUNDS")
        self.intro_sound = mixer.Sound(INTRO_SOUND_PATH)
        self.platformer_bg_sound = mixer.Sound(PLATFORMER_BG_SOUND_PATH)

        print_log("<game.run>:ASSETS LOADED SUCCESSFULLY", "SUCCESS")

    @debug
    def load_map(self, mapName) -> Tuple[TiledMap, Surface, Rect]:
        """Loads a map by providing the map's name.

        The map needs to be inside the ./maps folder and has to be a valid tmx file."""
        new_map = TiledMap(mapName)
        map_image = new_map.make_map()
        map_rect = map_image.get_rect()
        return new_map, map_image, map_rect

    @debug
    def set_map(self, mapName):
        """changes the game map.
        The passed mapName need to match directory of a valid map inside `./maps`"""
        print_log("<game.change_map>:loading a new map")
        self.map, self.map_image, self.map_rect = self.load_map(mapName)
        print_log("<game.change_map>:loaded the new map Successfully","SUCCESS")

    @debug
    def new(self) -> None:
        """runs code that starts a new game.

        This method sets up all objects in the current <game.map:TiledMap>
        """

        print_log("<game.new>:STARTING A NEW GAME")

        print_log("<game.new>:SETTING UP GROUPS")
        # start the game
        self.all_sprites = sprite.Group()
        self.platforms = sprite.Group()
        self.all_physics_objects = sprite.Group()
        self.coins = sprite.Group()
        self.player_projectiles = sprite.Group()
        self.all_enemies = sprite.Group()
        self.enemy_projectiles = sprite.Group()

        # new camera
        print_log("<game.new>:SETTING UP CAMERA")
        self.camera = Camera(self.map.width, self.map.height)

        # create tile objects
        print_log("<game.new>:LOADING OBJECTS FROM THE MAP")
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

        print_log("<game.new>:FINNISHED LOADING OBJECTS", "SUCCESS")
        self.run()

    @debug
    def run(self) -> None:
        """A function that controls the main game loop.
        Doesn't return anything.
        """
        self.playing = True
        self.platformer_bg_sound.play()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.platformer_bg_sound.fadeout(1000)


    def update(self) -> None:
        """Calls the update method of all game objects.

        NOTE: Logic being directly updated in this function shall be later moved to each object's class.
        """

        # Update objects logic
        self.all_sprites.update()

        # Make the camera follow the player
        self.camera.update(self.player)

        # Player Coin Collecting
        coin_hits = sprite.spritecollide(self.player,
                                         self.coins,
                                         True,
                                         sprite.collide_circle_ratio(0.5))
        for _ in coin_hits:
            self.player.health += 10
            print_log("<game.update>:Player Collected a coin")

        # Player getting shot
        player_hits = sprite.spritecollide(self.player,
                                           self.enemy_projectiles,
                                           True)
        for hit in player_hits:
            # For each shot, reduce health by 10
            # also push the player
            self.player.health -= 10
            self.player.pos += hit.vel
            print_log("<game.update>:Player got shot")

        # Mobs getting shot
        enemy_hits = sprite.groupcollide(self.player_projectiles, 
                                         self.all_enemies,
                                         True,
                                         False)
        for hit in enemy_hits:
            enemy_sprites = enemy_hits.get(hit)
            for enemy_sprite in enemy_sprites:
                enemy_sprite.die()
                print_log("<game.update>:Enemy Killed")

        # Game Over
        if self.player.rect.bottom > self.camera.height\
                or self.player.health < 10:
            self.playing = False
            print_log("<game.update>:Game Over")


    def events(self):
        """Method for controlling the event loop."""
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

    def draw(self) -> None:
        """ Method for drawing graphics.
        applies the camera's offset and showing the player health bar
        """
        # Game Loop - Draw
        self.screen.fill(BG_COLOR) # might be redundant
        self.screen.blit(self.map_image, self.camera.apply(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.player.image, self.camera.apply(self.player))
        ## after everything ##
        pg.display.flip()



    def draw_text(self, text, size: int, color: Tuple[tuple, tuple], x: int, y: int, surface: pg.surface.Surface = None) -> Tuple[Surface, Rect]:
        """A method that draws a text of a surface or the main screen.
        Fonts have been hardcoded intentionally.

        Parameters
        ----------
        text: string -> text to be drawn
        size: int -> size of the text
        color: tuple -> rgb color of the text
        x: int -> x coordinate of the text
        y: int -> y coordinate of the text
        surface: pg.surface.Surface ->  (optional) draws a text on a surface.

        Tests
        -----
        - passing an invalid surface
        - passing invalid tuple for the color
        - passing negative size
        - passing very large size
        """
        # get the two arcade fonts
        font_in = pg.font.Font(FONT_ARCADE_IN, size)
        font_out = pg.font.Font(FONT_ARCADE_OUT, size)

        # render them to get two surfaces
        text_in_surface: Surface = font_in.render(str(text), True, color[0])
        text_out_surface: Surface = font_out.render(str(text), True, color[1])
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
    def show_start_screen(self) -> None:
        """method that describes how the start screen looks like"""
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
    def show_start_text(self) -> None:
        """method that describes how the intro scene looks like"""
        # TODO: move text to a txt file
        text = """
        Human scientists finally invented the means
        for space exploration.

        Huge amout of people leave earth looking
        for a new life

        Space Trading becomes a very popular
        occupation

        You were once on a space caravan with your
        family

        Space Pirates attacks your caravan

        Pirates killed your parents in the attack
        and you are injured badly

        A scientist fixes you up and gives you
        the name of "XEON"

        Xeon is set out to clean the galaxy
         of space pirates

        """

        # TODO: Move this to a txt file.
        """
        Some story lore

        Xeon wants to clean the galaxy of space pirates.

        Xeon and the scientist create an organisation to fight pirates. (Unimplemented story says hi)

        Xeon's armor allows him to absorb life force from enemies to heal himself. (Unimplemented `Enemies should drop health pickups` says Hi)

        Xeon can fight bosses and absorb their skills. (Megaman says Hi)

        Xeon wants to fight the king of pirates at the end. (Unimplemented Boss fight says Hi)

        After Xeon wins the fight the organization continues on as a private security firm. (Unimplemented Endless mode says Hi)
        """
        print_log("STARTED INTRO")
        self.scroll_text(text)
        print_log("FINNISHED INTRO")

    @debug
    def show_over_screen(self) -> None:
        """ Method for describing how the game over screen look like.
        Also kills all sprites generated from the last round to improve performance."""
        if self.running:
            self.kill_sprite_group(self.all_sprites)
            self.screen.fill(BG_COLOR)
            self.draw_text("Game Over", 64, (WHITE, BLACK), WIDTH/2, HEIGHT/4)
            self.draw_text("Press a key to play again.", 22,
                           (WHITE, BLACK), WIDTH/2, HEIGHT * 3/4)
            pg.display.flip()
            self.wait_for_key()


    def scroll_text(self, text) -> None:
        """Fills the main screen with black and rolls up
        the passed text. font and size are hardcoded
        
        NOTE: for now when passing a long text, lines shouldn't be longer than `43` characters
        or the text will be cut. this is due to the fact that I wanted the textbox to be only 2/3
        of the window's width

        Parameters
        ----------
        text -> text to be scrolled up

        Tests
        -----
        - passing a very long text
        - passing a text with very long lines
        - passing text with escapeable chars
        """
        
        splitted = text.splitlines()
        self.screen.fill(BLACK)
        complete_surface = Surface((WIDTH*2//3, 30*len(splitted)))
        text_lines = []
        for index, line in enumerate(splitted):
            line = line.strip()
            text_surface, text_surface_rect = self.draw_text(
                line, 32, (WHITE, BLACK), x=0, y=32*index, surface=complete_surface)
            text_lines.append((text_surface, text_surface_rect))

        complete_surface_rect = complete_surface.get_rect()
        complete_surface_rect.topleft = (WIDTH//6, HEIGHT)

        waiting = True
        # while the bot of the text surface has not reached the top of screen
        while waiting and complete_surface_rect.bottom > 0:
            # scroll text up
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.playing = False
                if event.type == pg.KEYUP:
                    waiting = False

            self.clock.tick(60)
            complete_surface_rect.y -= 1
            complete_surface.blits(text_lines, False)
            self.screen.blit(complete_surface, complete_surface_rect)
            pg.display.flip()

    @debug
    def wait_for_key(self) -> None:
        """Pauses the game until a key is pressed"""
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
    def kill_sprite_group(self, group: sprite.Group) -> None:
        """Method that kills all sprites in a group.

        Parameters
        ----------
        group: sprite.Group -> group of sprites to be disposed of
        """
        # kill all sprites in a to improve performance
        for sprite in group:
            sprite.kill()

    @debug
    def quit(self) -> None:
        """Quits the game"""
        # Close Game
        pg.quit()

if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_over_screen()
    g.quit()
