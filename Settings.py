import pygame as pg

# Current version of our game
VERSION = "A_0.30"

# Pygame Vectors
vector = pg.math.Vector2()

#Screen
WIDTH = 800
HEIGHT = 600
FPS = 60
#SCALE = 2

#Colours
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

#Controls
# CONTROLS = {
#     "JUMP":     pg.K_SPACE,
#     "LEFT":     pg.K_a,
#     "RIGHT":    pg.K_d,
#     "FALL":     pg.K_s,
# }

CONTROLS = {
    pg.K_SPACE: "JUMP",
    pg.K_a: "LEFT",
    pg.K_d: "RIGHT",
    pg.K_s: "FALL",

}

#Player Constants
GRAVITY = 1.3
RUNSPEED = 7
JUMPHEIGHT = 18
MAXFALLSPEED = 20
MAXJUMPS = 2

# RUNSPEED_V = ()
# JUMPSPEED_V = ()
# GRAVITY_V = ()
# MAXFALLSPEED_V = ()
