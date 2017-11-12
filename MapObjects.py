from Settings import *
from Textures import *

SCORE = 0


# all objects on the map
class Obstacle(pygame.sprite.Sprite):

    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)

    def collisionSide(self,player,axis):
        # if collision occurs after updating xAxis movement, assume the collision occurs on the Xaxis
        if axis == 0:
            # approaching from right
            if player.rect.right - player.xVel > self.rect.right:
                return "right"
            # approaching from left
            elif player.rect.left - player.xVel < self.rect.left:
                return "left"
        # otherwise we assume the collision occurs on the y axis
        elif axis == 1:
            # We subtract the yVelocity to catch instances where the object moves so fast it passes THROUGH the self
            if player.rect.top - player.yVel < self.rect.top:
                return "top"
            if player.rect.bottom - player.yVel > self.rect.bottom:
                return "bottom"

# objects below inherit from Obstacle
# platform object
class Platform(Obstacle):
    texture = pygame.image.load(imgPLATFORM)

    def __init__(self,x,y):
        Obstacle.__init__(self,x,y,self.texture)

    def collisionBehaviour(self,player,axis,fallThrough):
        sideCollided = Obstacle.collisionSide(self, player, axis)

        if sideCollided == "top" and fallThrough == False and player.yVel > 0:
            player.rect.bottom = self.rect.top
            player.yVel = 0
            player.jumpsLeft = MAXJUMPS


# block object
class Block(Obstacle):
    texture = pygame.image.load(imgBLOCK)

    def __init__(self,x,y):
        Obstacle.__init__(self,x,y,self.texture)

    def collisionBehaviour(self,player,axis,fallThrough):
        sideCollided = Obstacle.collisionSide(self,player,axis)
        if sideCollided == "top":
            player.rect.bottom = self.rect.top
            player.yVel = 0
            player.jumpsLeft = MAXJUMPS
        elif sideCollided == "bottom":
            player.rect.top = self.rect.bottom
            player.yVel = 0
        elif sideCollided == "left":
            player.rect.right = self.rect.left

        #player.jumpsLeft = MAXJUMPS
        elif sideCollided == "right":
            player.rect.left = self.rect.right  # stop moving into the block!
            if pygame.Rect.collidepoint(self.rect,self.x+10, self.y-1):
                print("box above it")



class Coin(Obstacle):
    texture = pygame.image.load(imgCOIN)

    def __init__(self,x,y):
        Obstacle.__init__(self,x,y,self.texture)

    def collisionBehaviour(self,player,axis,fallThrough):
        #ignore WHERE it collided, just run collision code
        print("collision with coin")
        pygame.sprite.Sprite.kill(self)
        global SCORE
        SCORE += 1
        print (SCORE)


class Start(Obstacle):
    texture = pygame.image.load(imgSTART)

    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, self.texture)

    def collisionBehaviour(self, player, axis, fallthrough):
        pygame.sprite.Sprite.kill(self)


class Goal(Obstacle):
    texture = pygame.image.load(imgFLAG)

    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, self.texture)

    def collisionBehaviour(self, player, axis, fallThrough):
        pygame.sprite.Sprite.kill(self)
        print("GOAL")

###


obstaclePixels = {
    RED:Platform,
    BLUE:Block,
    MAGENTA:Coin,
    GREEN:Start,
    YELLOW:Goal,
}

# def createObstacle(spriteGroup, obstacleGroup,x,y):
