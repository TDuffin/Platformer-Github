import pygame as pg

# Current version of the game
VERSION = "A_0.60"

# Screen
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colours
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)
GREEN   = (0, 255, 0)
YELLOW  = (255, 255, 0)
CYAN    = (0,255,255)
MAGENTA = (255, 0, 255)
GREY    = (166, 166, 166)
DARKRED = (180, 0, 0)

# Controls, player can use any combination of keys during gameplay
CONTROLS = {
    # WASD settings
    pg.K_SPACE: "JUMP",
    pg.K_a: "LEFT",
    pg.K_d: "RIGHT",
    pg.K_s: "FALL",
    # Arrow key settings
    pg.K_LEFT: "LEFT",
    pg.K_RIGHT : "RIGHT",
    pg.K_DOWN : "FALL",
    pg.K_UP : "JUMP",
}

#Player Constants
GRAVITY = 1.3 # Downward acceleration of the player
RUNSPEED = 7 # Runspeed of player, in px/frame
JUMPHEIGHT = 18 # Jump velocity of the player
MAXFALLSPEED = 20 # Max fall speed of the player, stopping them from falling through the ground when making high jumps
MAXJUMPS = 2 # Number of jumps a player can make before falling to the ground

# Persistent dictionary to track certain game variables across files/classes
GLOBALS = {
    "level_complete": False,
    "coin_collected": False,
    "final_score": 0,
    "level_scores": [],
}

# Save File
SAVEFILE = "save_file.txt"
HISCOREFILE = "high_scores.txt"