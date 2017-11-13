# import dependencies and files
# import pygame
# from PIL import Image
# import math
#from Settings import *
from Player import *
from MapObjects import *
from MenuObjects import *

# game version
VERSION = "A_0.23"

# Init pygame/mixer
pygame.init()
pygame.mixer.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platformer:" + VERSION)
        self.clock = pygame.time.Clock()
        self.spriteGroup = pygame.sprite.Group()
        self.obstacleGroup = pygame.sprite.Group()
        self.sprPlayer = None

        self.mainMenu()


    def loadLevel(self,level):
        self.spriteGroup.empty()
        # buildList = []
        lvlWidth, lvlHeight = level.size
        # load list called pixels with RGB data from image file
        pixels = list(level.getdata())

        i = 0
        #while (i < lvlWidth * lvlHeight - 1):
        for i in range (0, lvlWidth*lvlHeight-1):
            i += 1

            if pixels[i] in obstaclePixels:
                y, x = divmod(i, lvlWidth)
                newObstacle = obstaclePixels[pixels[i]](x*20, y*20)
                self.obstacleGroup.add(newObstacle)
                self.spriteGroup.add(newObstacle)

                if pixels[i] == GREEN:
                    startPos = (x*20, y*20)

        self.sprPlayer = Player(startPos)
        self.spriteGroup.add(self.sprPlayer)

# Game loop
    def gameLoop(self, level):
        self.loadLevel(level)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in CONTROLS:
                        #send player control to player object
                        self.sprPlayer.control(CONTROLS[event.key], 1)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYUP:
                    if event.key in CONTROLS:
                        self.sprPlayer.control(CONTROLS[event.key], -1)


            # side scrolling!
            if (self.sprPlayer.rect.left > WIDTH * 0.7 and self.sprPlayer.xVel > 0) or (self.sprPlayer.rect.right < WIDTH * 0.3 and self.sprPlayer.xVel < 0):
                for obstacle in self.spriteGroup:
                    obstacle.rect.left -= int(self.sprPlayer.xVel)

            # if (self.sprPlayer.rect.top < HEIGHT*0.2 and self.sprPlayer.yVel < 0)or(self.sprPlayer.rect.bottom > HEIGHT*0.6 and se lf.sprPlayer.yVel > 0):
            #     for obstacle in self.spriteGroup:
            #         obstacle.rect.top -= int(self.sprPlayer.yVel)

            self.obstacleGroup.update()
            self.sprPlayer.update(self.obstacleGroup)
    
            self.screen.fill(GREY)
            self.spriteGroup.draw(self.screen)
    
            self.clock.tick(FPS)
            pygame.display.flip()

    def mainMenu(self):

        # self.objectList = []

        btnPlay = Button((WIDTH/2,100),(100,60),"Hello!",GREEN,self.spriteGroup)
        # btnNew  =
        # btnLoad =
        # btnExit =
        startGame = False
        running = True

        while running:

            # loop events
            for event in pygame.event.get():
                # if closed, quid
                if event.type == pygame.QUIT:
                    running = False
                # if clicked, check if button is clicked, then run
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for objects in self.spriteGroup:
                        if objects.ifHovered():
                            #objects.clicked(self)
                            running = False
                            startGame = True
                            # update points txtbox
                            #strPOINTS.changeText("Points Left: " + str(points))
                            break
            # background
            self.screen.fill(WHITE)

            # update all objects on screen
            self.spriteGroup.update()
            self.spriteGroup.draw(self.screen)

            # update screen
            self.clock.tick(FPS)
            pygame.display.flip()

        if startGame == True:
            self.gameLoop(imgMAP)










game = Game()

pygame.quit()
exit()
#game.__init__()