import pygame

#Screen
WIDTH = 800
HEIGHT = 600
FPS = 60
SCALE = 2

#Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED =   (255, 0, 0)
BLUE =  (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW =(255, 255, 0)
CYAN =  (0,255,255)
MAGENTA=(255, 0, 255)
GREY =  (166, 166, 166)

#Controls
CONTROLS = {
    pygame.K_SPACE: "SPACE",
    pygame.K_a: "A",
    pygame.K_d: "D",
    pygame.K_s: "S",
}

#Player Constants
GRAVITY = 1.8
RUNSPEED = 7
JUMPHEIGHT = 20
MAXFALLSPEED = 20
MAXJUMPS = 2
