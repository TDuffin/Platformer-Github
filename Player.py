from Settings import *
from Textures import *


# Player Class
class Player(pg.sprite.Sprite):
    jumpsLeft = MAXJUMPS
    yVel = 0
    xVel = 0
    maxYVel = MAXFALLSPEED
    fallThrough = False


    def __init__(self,startPos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(imgPLAYER)
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = startPos
        print("NEW PLAYER")

    def update(self,obstacles):
        if self.yVel < self.maxYVel:
            self.yVel += GRAVITY
        self.rect.x += self.xVel
        self.collisionCheck(obstacles,0,False)
        self.rect.y += self.yVel
        self.collisionCheck(obstacles,1,self.fallThrough)

    def control(self, control, modifier):
        self.fallThrough = False

        if control == "JUMP" and self.jumpsLeft > 0 and modifier == 1:
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
        collisions = pg.sprite.spritecollide(self,group,False)

        for objects in collisions:
            objects.collisionBehaviour(self,axis,fallThrough)



        
        
