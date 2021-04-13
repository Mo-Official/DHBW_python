import pygame as pg
import random
from settings import *
from sprites import *
from tilemap import *
import os




class Game:
    def __init__(self):
        # initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_arial = pg.font.match_font(FONT_ARIAL)
        self.score = 0
        self.load_data()

    def load_data(self):
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

        # load map
        self.map = TiledMap(LEVEL1_PATH)
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

        # load sounds
        self.intro_sound = pg.mixer.Sound(INTRO_SOUND_PATH)
        self.platformer_bg_sound = pg.mixer.Sound(PLATFORMER_BG_SOUND_PATH)


    def new(self):
        # reset the game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.scorllable_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        # experimental platform
        """for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.scorllable_sprites.add(p)"""

        # experimental coins
        """for coin in COIN_LIST:
            c = Coin(*coin)
            self.coins.add(c)
            self.all_sprites.add(c)
            self.scorllable_sprites.add(c)"""

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
                c = Coin(self, tile_object.x, tile_object.y, tile_object.color)
                self.all_sprites.add(c)
                self.coins.add(c)



        # create player 
        self.run()
        
        pass

    def run(self):
        # Game Loop
        self.playing = True
        self.platformer_bg_sound.play()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.platformer_bg_sound.fadeout(1000)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # Stop Player from falling when colliding with platform 
        hits = pg.sprite.spritecollide(self.player, self.platforms, False, )
        if hits:
            # check for the lowest platform
            lowest = hits[0]
            for hit in hits:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = hit

            # if player is falling, and his feet is about the platform set him above the platform
            if self.player.vel.y > 0: 
                if self.player.rect.bottom < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0

            # if the player is jumping (hit from below) the player should fall back  
            if self.player.vel.y < 0:      
                self.player.pos.y += 10
                self.player.vel.y = 0
        
        # New Camera Scrolling
        self.camera.update(self.player)
        
        # Player Coin Collecting
        coins = pg.sprite.spritecollide(self.player, self.coins, True)
        for coin in coins:
            self.score += coin.value

        # Game Over:
        if self.player.rect.bottom > self.camera.height:
            self.playing = False

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                    
    
    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.map_image, self.camera.apply(self.map_rect))

        #self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        
        # Draw Player Score
        self.draw_text(str(self.score), 32, WHITE, WIDTH/2, 15)
        ## after everything ##
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_arial, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
        
        

    
    def show_start_screen(self):
        self.intro_sound.play()
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 64, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("A and D to move and Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH/2, HEIGHT * 3/4 + 100)
        pg.display.flip()
        self.wait_for_key()
        self.intro_sound.fadeout(1000)

    def show_over_screen(self):
        if self.running:
            self.kill_sprite_group(self.all_sprites)
            self.screen.fill(BG_COLOR)
            self.draw_text("Game Over", 64, WHITE, WIDTH/2, HEIGHT/4)
            self.draw_text(f"Your Score is {self.score}", 22, WHITE, WIDTH/2, HEIGHT/2)
            self.draw_text("Press a key to play again.", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
            pg.display.flip()
            self.wait_for_key()   

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYUP:
                    waiting = False

    def kill_sprite_group(self, group):
        # kill all sprites in a to improve performance 
        for sprite in group:
            sprite.kill()

    def quit(self):
        # Close Game
        pg.quit()



if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_over_screen()
    g.quit()
    