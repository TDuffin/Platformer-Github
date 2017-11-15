from Settings import *
from Textures import *


# Player Class
class Player(pygame.sprite.Sprite):
    jumpsLeft = MAXJUMPS
    yVel = 0
    xVel = 0
    maxYVel = MAXFALLSPEED
    prevCollisions = []
    fallThrough = False

    def __init__(self,startPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgPLAYER)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = startPos

    def update(self,obstacles):
        if self.yVel < self.maxYVel:
            self.yVel += GRAVITY
        self.rect.x += self.xVel
        self.collisionCheck(obstacles,0,False)
        self.rect.y += self.yVel
        self.collisionCheck(obstacles,1,self.fallThrough)

    def control(self,control,modifier):
        #keys = pygame.mouse.get_pressed()
        self.fallThrough = False
        if control == "JUMP" and modifier == 1 and self.jumpsLeft > 0:
            self.yVel = -JUMPHEIGHT
            self.jumpsLeft -= 1
        elif control == "RIGHT":
            self.xVel += RUNSPEED * modifier
        elif control == "LEFT":
            self.xVel -= RUNSPEED * modifier
        elif control == "FALL" and modifier == 1:
            self.fallThrough = True

    # 0 for x axis col.check, 1 for y axis col.check
    def collisionCheck(self,group,axis,fallThrough):
        collisions = pygame.sprite.spritecollide(self,group,False)

        for objects in collisions:
            objects.collisionBehaviour(self,axis,fallThrough)



        
        
