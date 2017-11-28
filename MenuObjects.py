from Settings import *


class Button(pg.sprite.Sprite):
    # initialise variables
    def __init__(self, position, size, text, colour, sprite_group, click_state):
        pg.sprite.Sprite.__init__(self)
        # Sprite
        self.image = pg.Surface(size)
        self.w, self.h = (size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.w, self.h = (size)
        self.colour = colour
        self.light_colour = self.colour
        self.dark_colour = self.colour // pg.Color(2, 2, 2)
        self.click_state = click_state

        # add self to sprite group!
        sprite_group.add(self)

        # Text
        self.text = text
        self.font = pg.font.Font(None, 30)
        self.text_surf = self.font.render(self.text, True, BLACK)
        self.text_size = self.text_surf.get_rect().size
        self.text_pos = (self.w/2 - self.text_size[0]/2,self.h/2 - self.text_size[1]/2)


    # update button every tick
    def update(self):
        # Change colour if user hovers over button
        self.ifHovered()
        self.image.fill(self.colour)
        # Draw text on top of sprite

        self.image.blit(self.text_surf, self.text_pos)


    # if user hovering over the box, make button darker
    def ifHovered(self):
        mouse = pg.mouse.get_pos()
        if self.rect.right > mouse[0] > self.rect.left and self.rect.top < mouse[1] < self.rect.bottom:
            self.colour = self.dark_colour
            #print(True)
            return True
        else:
            self.colour = self.light_colour
            return False

    def clicked(self):
        return self.click_state

class TextSprite(pg.sprite.Sprite):
    def __init__(self, position, size, text_size, text, sprite_group):
        pg.sprite.Sprite.__init__(self)
        self.image =  pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.text = text
        self.font = pg.font.Font(None, text_size)
        self.text_surf = self.font.render(self.text, True, BLACK)
        self.text_size = self.text_surf.get_rect().size

        sprite_group.add(self)
    def update(self):
        self.image.blit(self.text_surf, (0,0))