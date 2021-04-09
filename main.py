import pygame as pg
import random
from settings import *
from sprites import *
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
        self.spritesheet = Spritesheet(XEON_SPRITESHEET)

    def new(self):
        # reset the game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.scorllable_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        # experimental platform
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.scorllable_sprites.add(p)

        # experimental coins
        for coin in COIN_LIST:
            c = Coin(*coin)
            self.coins.add(c)
            self.all_sprites.add(c)
            self.scorllable_sprites.add(c)

        # create player 
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.run()
        
        pass

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pass

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # Stop Player from falling when colliding with platform
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if self.player.vel.y > 0: # if player is falling, set him above the platform
                self.player.pos.y = hits[0].rect.top + 1
            if self.player.vel.y < 0: # if the player is jumping (hit from below) the player should fall back
                self.player.vel.y = 0
                self.player.pos.y += 10
            self.player.vel.y = 0
        
        # Camera Scrolling:
        # if player reaches top 1/3 of screen scroll up
        if self.player.rect.top <= HEIGHT * 1/3:
            self.player.pos.y += abs(self.player.vel.y)
            for sprite in self.scorllable_sprites:
                sprite.rect.y += abs(self.player.vel.y)
        # if player reaches bottom 1/6 of screen scroll down
        if self.player.pos.y >= HEIGHT * 5/6:
            self.player.pos.y -= abs(self.player.vel.y)
            for sprite in self.scorllable_sprites:
                sprite.rect.y -= abs(self.player.vel.y)
        # if player reaches right 1/3 of screen scroll right
        if self.player.pos.x >= WIDTH * 1/2:
            self.player.pos.x -= abs(self.player.vel.x // 1)
            for sprite in self.scorllable_sprites:
                sprite.rect.x -= abs(self.player.vel.x // 1)
        # if player reaches left 1/3 of screen scroll left
        if self.player.pos.x <= WIDTH * 1/2:
            self.player.pos.x += abs(self.player.vel.x // 1)
            for sprite in self.scorllable_sprites:
                sprite.rect.x += abs(self.player.vel.x // 1)
        
        # Player Coin Collecting
        coins = pg.sprite.spritecollide(self.player, self.coins, True)
        if coins:
            self.score += coins[0].value

        # Game Over:
        if self.player.rect.bottom > HEIGHT:
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
                    
    
    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
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
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 64, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("A and D to move and Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH/2, HEIGHT * 3/4 + 100)
        pg.display.flip()
        self.wait_for_key()        

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
    