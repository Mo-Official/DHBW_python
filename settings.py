import os

__doc__ = """
    Author: Mouaz Tabboush 
    Settings - This Script is where all the constants for the game are stored.
    ==========================================================================
    The this script is meant to be imported by other game scripts to access constants

    Requirements
    ============
    * os

    Other
    =====
    * Change LOGGING to True to log processes on the terminal.
    * Change CALLS_DEBUG to True to log function calls on the terminal.
"""


# Shows game Logs in the console if set to true
LOGGING_TO_CONSOLE = False
LOGGING_TO_FILE = True

# Customize Logs
LOG_INFO = True # set to true to see additional info when loading stuff

# Shows function calls if set to true
# NOTE: Functions need to have the @debug decorator in order to be debugged
CALLS_DEBUG = False


# System stats
# Using os.path to make sure the game runs on all OS
GAME_PATH = os.path.dirname(__file__)
HS_FILE = os.path.join(GAME_PATH, "HighScore.txt")
ASSETS_PATH = os.path.join(GAME_PATH, "assets")
SOUNDS_PATH = os.path.join(GAME_PATH, "snd")
FONT_PATH = os.path.join(GAME_PATH, "fonts")
MAP_PATH = os.path.join(GAME_PATH, "maps")

# Paths to assets
XEON_FRAMES = os.path.join(ASSETS_PATH, "xeon_frames") # made with Gimp
COIN_SPRITESHEET = os.path.join(ASSETS_PATH, "coins_spritesheet.png") # made with Texture Packer
HEALTHDROP_SPRITESHEET = os.path.join(ASSETS_PATH, "healthdrop_spritesheet.png") # made with Texture Packer
BULLETS_SPRITESHEET = os.path.join(ASSETS_PATH, "bullets_normal.png") # made with Texture Packer
HEALTHDROP_XML_DATA = os.path.join(ASSETS_PATH, "healthdrop_spritesheet.xml") # made with Texture Packer
MAIN_MENU_BG = os.path.join(ASSETS_PATH, "main_menu_background.png")

# Paths to maps
LEVEL1_PATH = os.path.join(MAP_PATH, "level1.tmx") # made with Tiled
LEVEL2_PATH = os.path.join(MAP_PATH, "level2.tmx") # made with Tiled

# Paths to Sounds
INTRO_SOUND_PATH = os.path.join(SOUNDS_PATH, "intro.ogg")
PLATFORMER_BG_SOUND_PATH = os.path.join(SOUNDS_PATH, "platformer-bg.mp3")

# Paths to Fonts
FONT_ARCADE_IN = os.path.join(FONT_PATH, "8-bit Arcade In.ttf")
FONT_ARCADE_OUT = os.path.join(FONT_PATH, "8-bit Arcade Out.ttf")

# Path to texts
INTRO_TEXT = os.path.join(GAME_PATH, "intro.txt")



# Window stats
WIDTH = 1024
HEIGHT = 800
TITLE = "Xeon - The Unfinished game"
FPS = 60
MUSIC_ON = True # turn of for a quiter experince :)
MASTER_SOUND = 0.2 # can be between 0.0 and 1.0


# NOTE: Not being used anymore. using Font_Arcade instead.
FONT_ARIAL = "arial"

# Player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -20
PLAYER_HEALTH = 100
PLAYER_INVULNERABILITY = 1000
SHOT_KILL_DISTANCE = 600
SHOOT_COOLDOWN = 400

# Position of the camera's target on the window
CAM_POINT = (int(WIDTH/2),(HEIGHT/2))

# Color definitions
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
PINK = (236,57,190)

BG_COLOR = LIGHTBLUE
XEON_SPRITESHEET_KEYCOLOR = GREEN
COIN_SPRITESHEET_KEYCOLOR = PINK
BASE_ENEMY_KEYCOLOR = (77, 75, 118)
