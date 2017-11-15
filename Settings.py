import pygame

VERSION = "A_0.30"

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
#     "JUMP":     pygame.K_SPACE,
#     "LEFT":     pygame.K_a,
#     "RIGHT":    pygame.K_d,
#     "FALL":     pygame.K_s,
# }

CONTROLS = {
    pygame.K_SPACE: "JUMP",
    pygame.K_a: "LEFT",
    pygame.K_d: "RIGHT",
    pygame.K_s: "FALL",

}

#Player Constants
GRAVITY = 1.8
RUNSPEED = 7
JUMPHEIGHT = 20
MAXFALLSPEED = 20
MAXJUMPS = 2
