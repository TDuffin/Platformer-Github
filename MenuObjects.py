from Settings import *


class Button(pg.sprite.Sprite):
    # initialise variables
    def __init__(self, position, size, text, colour, spriteGroup, click_state):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size)
        self.w, self.h = (size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.w, self.h = (size)
        self.text = text
        self.font = pg.font.Font(None, 30)
        self.colour = colour
        self.lightColour = self.colour
        self.darkColour = self.colour // pg.Color(2, 2, 2)
        self.click_state = click_state

        # add self to sprite group!
        spriteGroup.add(self)

    # update button every tick
    def update(self):
        # Change colour if user hovers over button
        self.ifHovered()
        self.image.fill(self.colour)
        # Draw text on top of sprite
        textSurf = self.font.render(self.text, True, BLACK)
        textSize = textSurf.get_rect().size
        self.image.blit(textSurf,(self.w/2 - textSize[0]/2,self.h/2 - textSize[1]/2))


    # if user hovering over the box, make button darker
    def ifHovered(self):
        mouse = pg.mouse.get_pos()
        if self.rect.right > mouse[0] > self.rect.left and self.rect.top < mouse[1] < self.rect.bottom:
            self.colour = self.darkColour
            #print(True)
            return True
        else:
            self.colour = self.lightColour
            return False

    def clicked(self):
        return self.click_state
