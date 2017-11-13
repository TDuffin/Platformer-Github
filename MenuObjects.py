from Settings import *


class Button(pygame.sprite.Sprite):
    # initialise variables
    def __init__(self,position,size,text,colour,spriteGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.w, self.h = (size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.w, self.h = (size)
        self.text = text
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.colour = pygame.Color(colour[0],colour[1],colour[2])
        self.lightColour = self.colour
        self.darkColour = self.colour // pygame.Color(2, 2, 2)

        #add self to sprite group!
        spriteGroup.add(self)

    #update button every tick
    def update(self):
        # change colour if user hovers over button
        self.ifHovered()
        self.image.fill(self.colour)

        # Draw text on top of sprite
        renderedText = self.font.render(self.text, True, BLACK)
        self.image.blit(renderedText, (self.rect.x + 2, self.rect.y + 2))


    # if user hovering over the box, make button darker
    def ifHovered(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.right > mouse[0] > self.rect.left and self.rect.top < mouse[1] < self.rect.bottom:
            self.colour = self.darkColour
            #print(True)
            return True

        else:
            self.colour = self.lightColour
            return False

    # when clicked start the game (unused)
    def clicked(self,game):
        pass
        game.mainMenu.startGame = True
        game.mainMenu.running = False
