import os

# system stats
GAME_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(GAME_PATH, "assets")
XEON_SPRITESHEET = os.path.join(ASSETS_PATH, "xeon_spritesheet.png") # made with texture Packer
HS_FILE = os.path.join(GAME_PATH, "HighScore.txt")
SOUNDS_PATH = os.path.join(GAME_PATH, "snd")
INTRO_SOUND_PATH = os.path.join(SOUNDS_PATH, "intro.ogg")


# window stats
TITLE = "My Title"
WIDTH = 1024
HEIGHT = 640
TITLE = "My Game"
FPS = 60
FONT_ARIAL = "arial"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -20

# Starting Platforms
PLATFORM_LIST = [
    (0, HEIGHT - 40 , WIDTH, 40),
    (WIDTH/2 - 200, HEIGHT * 3/4 - 50, 100, 20),
    (125, HEIGHT - 350, 100, 20),
    (350, 200, 100, 20),
    (175, 100, 50, 20)]

COIN_LIST = [
    (50, HEIGHT-100, 100),
    (125, HEIGHT - 400, 75),
    (350, 250, 25)
]


# colors
WHITE = (255,255,255)
TESTCOLOR = (205,205,205)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0, 228, 3)
RED = (255,0,0)
BROWN = (160,82,45)
CYAN = (224,255,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0, 155, 155)
BG_COLOR = LIGHTBLUE
XEON_SPRITESHEET_KEYCOLOR = GREEN