# Untitled Platformer Game
# Year One, Term 1 Project
# Thomas-Luke Duffin, N0727751
import sys
import pygame as pg
from Settings import *
from MenuObjects import *
from Textures import *
from MapObjects import *
from Player import *
from Score import *
    
class Game(object):
    # The game and its states are controlled through this class. Events are also handled here.
    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.
        
        screen: the pg display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state 
        """

        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]()


        
    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            self.state.get_event(event)
            
    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        print("CURRENT:",current_state)
        next_state = self.state.next_state
        print("NEXT:",next_state)
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        #print("PERSISTENT:",persistent)

        self.state = self.states[self.state_name]()
        self.state.startup(persistent)
    
    def update(self, dt):
        """
        Check for state flip and update active state.
        
        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()    
        self.state.update(dt)
        
    def draw(self):
        """Pass display surface to active state for drawing."""
        # for sprite_list in self.persist["sprite_list"]:
        #     sprite_list.update()
        #     sprite_list.draw(self.screen)
        self.state.draw(self.screen)
        
    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """ 
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()
            
            
class GameState(object):
    """
    Parent class for individual game states to inherit from. 
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.screen_surf = pg.display.get_surface()
        self.persist = {}
        self.font = pg.font.Font(None, 24)
        self.sprite_group = pg.sprite.Group()
        self.persist["sprite_group"] = self.sprite_group


    def startup(self, persistent):
        # Called when a state resumes being active.
        # Allows information to be passed between states.
        # persistent: a dict passed from state to state
        self.persist = persistent



    def get_event(self, event):
        # Handle a single event passed by the Game object.
        pass

    def update(self, dt):
        # Update the state. Called by the Game object once per frame.
        # dt: time since last frame
        pass
        
    def draw(self, surface):
        # Draw everything to the screen.
        pass
        
        
class MainMenu(GameState):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.sprite_group.empty()
        self.button_group = pg.sprite.Group()
        #self.title = self.font.render("Splash Screen", True, pg.Color("dodgerblue"))
        #self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        #self, position, size, text, colour, sprite_group

        # Buttons/UI elements
        self.new_button = Button((WIDTH/2, 200), (100, 40), "NEW", pg.Color("dodgerblue"), self.sprite_group, "LEVELLOAD")
        self.load_button = Button((WIDTH/2, 300), (100, 40), "LOAD", pg.Color("dodgerblue"), self.sprite_group, "SAVESELECT")
        self.exit_button = Button((WIDTH/2, 400), (100, 40), "EXIT", pg.Color("dodgerblue"), self.sprite_group, "EXIT")

        for sprite in self.sprite_group:
            self.button_group.add(sprite)

        self.title_label = Text((WIDTH/2,60),"Platformer ver: " + VERSION,50,pg.Color("grey"),self.sprite_group)
        # Setting attribs from global dict.
        self.persist["screen_color"] = "grey"


        # Next state
        self.persist["next_level"] = 1

        # self.next_state = "GAMEPLAY"
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for sprite in self.button_group:
                if sprite.if_hovered():
                    self.next_state = sprite.clicked()
                    self.persist["screen_color"] = "grey"
                    self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("grey"))
        self.sprite_group.update()
        self.sprite_group.draw(surface)

    
class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()

    def startup(self, persistent):
        PERSISTENT["level_complete"] = False
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)
        self.player = self.persist["player"]
        self.obstacle_group = self.persist["obstacle_group"]
        self.sprite_group = self.persist["sprite_group"]
        self.display_group = pg.sprite.Group()
        self.next_state = "LEVELLOAD"

        #SCORE
        self.level_score = Score()

        #HUD/UI Elements
        self.version_label = Text((45,10),"ver: " + VERSION,20,self.screen_color,self.display_group)
        self.score_label = Text((45,30),"scr: " + str(self.level_score.score),20,self.screen_color,self.display_group)
        
    def get_event(self, event):
        #print(event)
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key in CONTROLS:
                # send player control to player object
                self.player.control(CONTROLS[event.key], 1)
            elif event.key == pg.K_ESCAPE:
                self.quit = True
        if event.type == pg.KEYUP:
            if event.key in CONTROLS:
                self.player.control(CONTROLS[event.key], -1)
                
    def update(self, dt):
        if not PERSISTENT["level_complete"] and self.level_score.score > 0:
            if (self.player.rect.left > WIDTH * 0.7 and self.player.xVel > 0) or (
                    self.player.rect.right < WIDTH * 0.3 and self.player.xVel < 0):
                for sprite in self.sprite_group:
                    sprite.rect.left -= int(self.player.xVel)

            #reduce score by dt
            if PERSISTENT["coin_collected"] == True:
                PERSISTENT["coin_collected"] = False
                self.level_score.update_score(500)
            self.level_score.update_score(int(-dt/3))
            # print(self.level_score.score)

            self.score_label.update_text("scr: " + str(self.level_score.score))
            self.display_group.update()
            self.obstacle_group.update()
            self.player.update(self.obstacle_group)

        else:
            PERSISTENT["final_score"] += self.level_score.score
            print(PERSISTENT["final_score"])
            self.player.xVel = 0
            self.player.yVel = 0
            self.done = True
                 
    def draw(self, surface):
        surface.fill(self.screen_color)

        self.sprite_group.draw(surface)
        self.display_group.draw(surface)



class SaveSelect(GameState):
    def __init__(self):
        pass

    def startup(self, persistent):
        pass

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class LevelLoad(GameState):
    def __init__(self):
        super(LevelLoad,self).__init__()

    def startup(self,persistent):
        self.persist = persistent
        level = LEVELS[self.persist["next_level"]]

        self.obstacle_group = pg.sprite.Group()
        self.persist["obstacle_group"] = self.obstacle_group

        self.obstacle_group.empty()
        self.sprite_group.empty()

        lvl_width, lvl_height = level.size
        # load list called pixels with RGB data from image file
        pixels = list(level.getdata())

        i = 0

        for i in range(0, lvl_width * lvl_height - 1):
            i += 1
            if pixels[i] in obstacle_pixels:
                y, x = divmod(i, lvl_width)
                new_obstacle = obstacle_pixels[pixels[i]](x * 20, y * 20)
                self.obstacle_group.add(new_obstacle)
                self.sprite_group.add(new_obstacle)

                if pixels[i] == GREEN:
                    startPos = (x * 20, y * 20)

        player = Player(startPos)
        self.sprite_group.add(player)

        # Load sprite groups to the persist dictionary so that they're overwritten
        self.persist["player"] = player
        self.persist["sprite_group"]=self.sprite_group

        # After loading the level, the next state will always be GAMEPLAY, Then end the instance
        self.persist["current_level"] = self.persist["next_level"]
        self.persist["next_level"] += 1
        self.next_state = "GAMEPLAY"
        self.done = True


class LevelSelect(GameState):
    pass



# TODO Level intro screen
# TODO Level Over Screen
# TODO Pause Screen
# TODO Load/Save system
# TODO Menus and polish
class LevelIntro(GameState):
    def __init__(self):
        super(LevelIntro,self).__init__()

    def startup(self, persistent):
        self.persist = persistent

        #self.level_label

    def get_event(self, event):
        pass

    def update(self, dt):
        pass
    def draw(self, surface):
        pass

class LevelPause(GameState):
    pass


class EndLevel(GameState):
    pass


# Exits the game by immediately setting the "quit" variable to true
class Exit(GameState):
    def __init__(self):
        #kills the game by forcing the game class to break from all of its loops.
        super(Exit, self).__init__()
        self.quit = True




if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Platformer " + VERSION)
    
    # Dictionary stores instance of every game state to be switched to during runtime. 
    states = {
        "MAINMENU": MainMenu,
        "GAMEPLAY": Gameplay,
        "SAVESELECT": SaveSelect,
        "LEVELLOAD": LevelLoad,
        "LEVELSELECT": LevelSelect,
        "LEVELINTRO": LevelIntro,
        "LEVELPAUSE": LevelPause,
        "ENDLEVEL": EndLevel,
        "EXIT": Exit,
        
    }
    
    # Create instance of the Game class, setting its initial state to the Main Menu
    game = Game(screen, states, "MAINMENU")
    game.run()
    pg.quit()
    sys.exit()
