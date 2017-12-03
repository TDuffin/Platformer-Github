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
    # The game, states, and events are handled through this class.
    def __init__(self, screen, states, start_state):
        # Initialise game variables.
        # screen is the screen surface, states is a dictionary of all stastes, start_state is the initial state
        # that runs
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]()

        
    def event_loop(self):
        # Events are passed for handling to the current state.
        for event in pg.event.get():
            self.state.get_event(event)
            
    def flip_state(self):
        # Switch to the next game state.
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state

        # persistent dictionary is pulled from previous state to pass to next state
        persistent = self.state.persist

        # Run the startup functions of the next state
        self.state = self.states[self.state_name]()
        self.state.startup(persistent)
    
    def update(self, dt):
        # Check to see if user quits, or that state is done.
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()    
        self.state.update(dt)
        
    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)
        
    def run(self):
        # loops through the game class methods until the player quits
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


class GameState(object):
    # Parent class of all GameStates
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
        # persistent: a dictionary passed from state to state
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

        # Buttons/UI elements
        self.new_button = Button((WIDTH/2, 200), (150, 40), "NEW", pg.Color("dodgerblue"), self.sprite_group, "LEVELLOAD")
        self.load_button = Button((WIDTH/2, 300), (150, 40), "LOAD", pg.Color("dodgerblue"), self.sprite_group, "LOADGAME")
        self.scores_button = Button((WIDTH/2, 400), (150, 40), "HISCORES", pg.Color("dodgerblue"), self.sprite_group, "HISCORES")
        self.exit_button = Button((WIDTH/2, 500), (150, 40), "EXIT", pg.Color("red"), self.sprite_group, "EXIT")

        for sprite in self.sprite_group:
            self.button_group.add(sprite)

        self.title_label = Text((WIDTH/2,60),"Platformer ver: " + VERSION,50,pg.Color("grey"),self.sprite_group)
        # Setting attribs from global dict.
        self.persist["screen_colour"] = "grey"

        # Next state
        self.persist["next_level"] = 1
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for sprite in self.button_group:
                if sprite.if_hovered():
                    self.next_state = sprite.clicked()
                    if self.next_state == "LEVELLOAD":
                        self.persist["next_level"] = 1
                        GLOBALS["final_score"] = 0
                        GLOBALS["level_scores"][:] = []

                    self.persist["screen_colour"] = "grey"
                    self.done = True

    def update(self,dt):
        self.sprite_group.update()

    def draw(self, surface):
        surface.fill(pg.Color("grey"))
        self.sprite_group.draw(surface)

#handles playing of game levels
class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()

    def startup(self, persistent):
        GLOBALS["level_complete"] = False
        self.persist = persistent
        color = self.persist["screen_colour"]
        self.screen_colour = pg.Color(color)
        self.player = self.persist["player"]
        self.obstacle_group = self.persist["obstacle_group"]
        self.sprite_group = self.persist["sprite_group"]
        self.overlay_group = pg.sprite.Group()
        self.next_state = "LEVELLOAD"

        #SCORE
        self.level_score = Score()

        #HUD/UI Elements
        self.score_label = Text((WIDTH/2,35), "SCORE: #####", 30, pg.Color("white"), self.overlay_group)
        
    def get_event(self, event):
        #print(event)
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key in CONTROLS:
                # send player control to player object
                self.player.control(CONTROLS[event.key], 1)
            elif event.key == pg.K_ESCAPE:
                self.next_state = "LEVELPAUSE"
                if self.player.xVel > 0:
                    self.persist["ignore_keyup"].append(pg.K_a)
                elif self.player.xVel < 0:
                    self.persist["ignore_keyup"].append(pg.K_d)
                self.done = True

        # Check if we need to ignore the keyup, otherwise send it to player control
        if event.type == pg.KEYUP:
            if event.key in CONTROLS:
                if event.key in self.persist["ignore_keyup"]:
                    self.persist["ignore_keyup"].remove(event.key)
                else:
                    self.player.control(CONTROLS[event.key], -1)
                
    def update(self, dt):
        #Restart level if the player fails
        if self.level_score.score <= 0 or self.player.rect.top > HEIGHT:
            self.restart_level()

        # Level_complete will equate to False as long as the player has not collected the "goal" object (flag)
        if not GLOBALS["level_complete"]:
            if (self.player.rect.left > WIDTH * 0.6 and self.player.xVel > 0) or (
                    self.player.rect.right < WIDTH * 0.4 and self.player.xVel < 0):
                for sprite in self.sprite_group:
                    sprite.rect.left -= int(self.player.xVel)

            # if a coin is collected, increase score by 500
            if GLOBALS["coin_collected"]:
                GLOBALS["coin_collected"] = False
                self.level_score.update_score(500)
            # reduce score using dt
            self.level_score.update_score(int(-dt/3))

            self.score_label.update_text("SCORE: {}".format(str(self.level_score.score)))
            self.overlay_group.update()
            self.obstacle_group.update()
            self.player.update(self.obstacle_group)

        # Level is complete
        else:
            GLOBALS["final_score"] += self.level_score.score
            GLOBALS["level_scores"].append(self.level_score.score)
            print(GLOBALS["final_score"])
            self.next_state = "ENDLEVEL"
            self.done = True
             
    def draw(self, surface):
        surface.fill(self.screen_colour)
        #draw the game sprites
        self.sprite_group.draw(surface)
        #draw the overlay
        self.overlay_group.draw(surface)

    # Restarts the level
    def restart_level(self):
        self.persist["next_level"] = self.persist["current_level"]
        self.done = True


class SaveGame(GameState):
    def __init__(self):
        super(SaveGame, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.save_game()

        # When saved, load the next level
        self.next_state = "LEVELLOAD"
        self.done = True

    def save_game(self):
        data = []
        data.append(str(self.persist["current_level"])+"\n")
        data.append(str(GLOBALS["final_score"])+"\n")

        for score in GLOBALS["level_scores"]:
            data.append(str(score) + "\n")

        with open(SAVEFILE, 'w') as f:
            f.writelines(data)


class LevelLoad(GameState):
    def __init__(self):
        super(LevelLoad,self).__init__()

    def startup(self,persistent):
        self.persist = persistent

        # If the next_level counter exceeds the number of levels, show hiscores.
        if not LEVELS.get(self.persist["next_level"], False):
            if self.persist.get("load_game", False):
                self.persist["load_game"] = False
                GLOBALS["final_score"] = 0

            self.next_state = "HISCORES"
            self.done = True

        else:
            # Load the level
            self.load_level()

    # Loads the level
    def load_level(self):
        # The level to be loaded is stored under "next level" and fetched from the LEVELS dictionary
        level = LEVELS[self.persist["next_level"]]
        print("Level: ", level)

        # create the obstacle group, add it to the persistent dict.
        self.obstacle_group = pg.sprite.Group()
        self.persist["obstacle_group"] = self.obstacle_group

        # Empty the sprite group to overwrite with new objects
        self.sprite_group.empty()

        # Set the w/h using the .size attribute of the image
        lvl_width, lvl_height = level.size

        # load list called pixels with RGB data from image file
        pixels = list(level.getdata())

        # Check each pixel on the map image
        # If the pixel's colour matches a colour in the dictionary of object/pixel pairs
        for i in range(0, lvl_width * lvl_height - 1):
            i += 1
            if pixels[i] in obstacle_pixels:
                y, x = divmod(i, lvl_width)
                new_obstacle = obstacle_pixels[pixels[i]](x * 20, y * 20)
                self.obstacle_group.add(new_obstacle)
                self.sprite_group.add(new_obstacle)

                if pixels[i] == GREEN:
                    startPos = (x * 20, y * 20)

        # If a player object already exists, set its position to StartPos
        # Otherwise, we create a new player object at StartPos
        if self.persist.get("player", False):
            player = self.persist["player"]
            player.rect.topleft = startPos
            player.xVel = 0
        else:
            player = Player(startPos)

        # Add the player object to the sprite group
        self.sprite_group.add(player)

        # Load sprite groups to the persist dictionary so that they're overwritten
        self.persist["player"] = player
        self.persist["sprite_group"]=self.sprite_group

        # After loading the level, load the level intro screen, increment the next level, and close the state.
        self.persist["current_level"] = self.persist["next_level"]
        self.persist["next_level"] += 1
        self.next_state = "LEVELINTRO"
        self.done = True


class LoadGame(GameState):
    def __init__(self):
        super(LoadGame, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.persist["load_game"] = True

        with open(SAVEFILE, 'r') as f:
            data = f.read().splitlines()

        self.persist["next_level"] = int(data[0]) + 1
        GLOBALS["final_score"] = int(data[1])

        for i in data[2:]:
            GLOBALS["level_scores"].append(int(i))

        self.next_state = "LEVELLOAD"
        self.done = True


class LevelIntro(GameState):
    def __init__(self):
        super(LevelIntro,self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.overlay_group = pg.sprite.Group()
        self.screen_colour = pg.Color("green")
        self.level_label = Text((WIDTH/2, 100), "LEVEL: " + str(self.persist["current_level"]), 60, self.screen_colour, self.overlay_group)
        self.prompt_label = Text((WIDTH/2, 300), "CLICK TO START", 40, self.screen_colour, self.overlay_group)
        self.score_level = Text((WIDTH/2, 400), "CURRENT SCORE: " + str(GLOBALS["final_score"]), 40, self.screen_colour, self.overlay_group)

        self.ignore_keyup = []

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True
                if event.key in CONTROLS:
                    self.ignore_keyup.append(event.key)
            if event.type == pg.KEYUP:
                if event.key in CONTROLS:
                    if event.key in self.persist["ignore_keyup"]:
                        self.ignore_keyup.remove(event.key)
            else:
                self.persist['ignore_keyup'] = self.ignore_keyup
                self.next_state = "GAMEPLAY"
                self.done = True

    def update(self, dt):
        self.overlay_group.update()

    def draw(self, surface):
        surface.fill(self.screen_colour)
        self.overlay_group.draw(surface)


class LevelPause(GameState):
    def __init__(self):
        super(LevelPause, self).__init__()
    def startup(self, persistent):
        self.persist = persistent
        self.button_group = pg.sprite.Group()
        self.label_group = pg.sprite.Group()
        self.sprite_group = self.persist["sprite_group"]
        self.ignore_keyup = self.persist["ignore_keyup"]

        self.paused_label = Text((WIDTH/2, 100),"*PAUSED*",70,pg.Color("grey"),self.label_group)
        self.resume_button = Button((WIDTH/2, 200), (150, 40), "RESUME", pg.Color("dodgerblue"), self.button_group, "GAMEPLAY")
        self.exit_button = Button((WIDTH/2, 300), (150, 40), "EXIT", pg.Color("dodgerblue"), self.button_group, "EXIT")
        self.restart_button = Button((WIDTH/2, 250), (150, 40), "RESTART", pg.Color("dodgerblue"), self.button_group, "RESTART")
        self.menu_button = Button((WIDTH / 2, 350), (150, 40), "MENU", pg.Color("dodgerblue"), self.button_group, "MAINMENU")

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.button_group:
                if button.if_hovered():
                    if button.clicked() in states:
                        self.next_state = button.clicked()
                        self.done = True
                    else:
                        if button.clicked() == "RESTART":
                            self.persist["next_level"] = self.persist["current_level"]
                            self.next_state = "LEVELLOAD"
                            self.done = True

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "GAMEPLAY"
                self.done = True
            if event.key in CONTROLS:
                self.ignore_keyup.append(event.key)
        if event.type == pg.KEYUP:
            if event.key in CONTROLS:
                if event.key in self.persist["ignore_keyup"]:
                    self.ignore_keyup.remove(event.key)
        self.persist["ignore_keyup"] = self.ignore_keyup

    def update(self, dt):
        self.button_group.update()
        self.label_group.update()

    def draw(self, surface):
        # draw the game sprites
        self.sprite_group.draw(surface)
        self.button_group.draw(surface)
        self.label_group.draw(surface)


class EndLevel(GameState):
    def __init__(self):
        super(EndLevel,self).__init__()

    def startup(self, persistent):
        # import persistent dict, initialise sprite groups
        self.persist = persistent
        self.overlay_group = pg.sprite.Group()
        self.button_group = pg.sprite.Group()

        # Screen colour, labels
        self.screen_colour = pg.Color("dodgerblue")
        self.level_label = Text((WIDTH/2, 100), "LEVEL" + str(self.persist["current_level"]), 60, self.screen_colour, self.overlay_group)
        self.score_level = Text((WIDTH/2, 400), "LEVEL SCORE: " + str(GLOBALS["level_scores"][-1]), 40, self.screen_colour, self.overlay_group)
        self.score_total = Text((WIDTH/2, 450), "TOTAL SCORE: " + str(GLOBALS["final_score"]), 40, self.screen_colour, self.overlay_group)

        # Menu buttons
        self.restart_button = Button((WIDTH/2, 170), (200, 40), "RESTART LEVEL", pg.Color("white"), self.button_group, "RESTART")
        self.next_button =    Button((WIDTH/2, 220), (200, 40), "NEXT LEVEL", pg.Color("white"), self.button_group, "SAVEGAME")
        self.exit_button =    Button((WIDTH/2, 270), (200, 40), "EXIT", pg.Color("white"), self.button_group, "EXIT")
        self.menu_button =    Button((WIDTH/2, 320), (200, 40), "MAIN MENU", pg.Color("white"), self.button_group, "MAINMENU")

    def get_event(self, event):
        #Handle mouse events
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.button_group:
                if button.if_hovered():
                    if button.clicked() in states:
                        self.next_state = button.clicked()
                        self.done = True
                    else:
                        # If restart is clicked set next level to start of prev level, restart level
                        if button.clicked() == "RESTART":
                            GLOBALS["final_score"] -= GLOBALS["level_scores"][-1]
                            GLOBALS["level_scores"][-1] = 0
                            self.persist["next_level"] = self.persist["current_level"]
                            self.next_state = "LEVELLOAD"
                            self.done = True

    def update(self, dt):
        # Update the button groups
        self.button_group.update()
        self.overlay_group.update()

    def draw(self, surface):
        surface.fill(self.screen_colour)
        self.button_group.draw(surface)
        self.overlay_group.draw(surface)

# Displays a screen showing hiscores to the player when they finish the game
class HighScores(GameState):
    def __init__(self):
        #Inherit from GameState class
        super(HighScores, self).__init__()

    def startup(self, persistent):
        # Import persistent dict and initialise sprite groups, screen colour
        self.persist = persistent
        self.button_group = pg.sprite.Group()
        self.label_group = pg.sprite.Group()
        self.screen_colour = pg.Color("gold")

        # buttons/labels
        self.exit_button = Button((WIDTH - 100, 500), (100, 40), "EXIT", pg.Color("white"), self.button_group, "EXIT")
        self.menu_button = Button((100, 500), (100, 40), "MAIN", pg.Color("white"), self.button_group, "MAINMENU")
        self.new_button = Button((WIDTH/2, 500), (150, 40), "NEW GAME", pg.Color("green"), self.button_group, "LEVELLOAD")
        self.title_label = Text((WIDTH/2,50), "HIGH SCORES", 80, self.screen_colour, self.label_group)

        # Load scores to the labels
        self.load_scores()

    def get_event(self, event):
        # If the player quits the game, quit
        if event.type == pg.QUIT:
            self.quit = True
            self.done = True

        # Handles button input
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.button_group:
                if button.if_hovered():
                    if button.clicked() in states:
                        self.next_state = button.clicked()

                        # if the new-game button is clicked, start from level 1
                        if self.next_state == "LEVELLOAD":
                            self.persist["next_level"] = 1
                            GLOBALS["final_score"] = 0
                            GLOBALS["level_scores"][:] = []
                        self.done = True

    def update(self, dt):
        # Update the button/labels
        self.button_group.update()
        self.label_group.update()

    def draw(self, surface):
        # Draw the elements to the screen
        screen.fill(self.screen_colour)
        self.button_group.draw(surface)
        self.label_group.draw(surface)

    # Loads the scores for the game
    def load_scores(self):
        final_score = GLOBALS["final_score"]

        with open(HISCOREFILE, 'r') as f:
            hiscores = f.read().splitlines()

        # Copy, by value, the hiscores list to a new list
        score_string = hiscores[:]

        # If the score is on the hiscores list, insert it in the correct place on the list
        for i in range(0, len(score_string)):
            if final_score > int(score_string[i]):
                # Append "new" to the score to indicate that it's a new score
                score_string.insert(i, str(final_score) + " *NEW*")
                hiscores.insert(i, final_score)
                # slice the lists back down to size, then break from the loop
                score_string = score_string[:5]
                hiscores = hiscores[:5]
                break

        # All the boxes will have the same text size, so just define it here to save time
        text_size = 40

        # In Descending order, load the hiscore buttons with their respective score data
        self.first = Text((WIDTH / 2, 200), "1. {:6}".format(score_string[0]), text_size, pg.Color("white"), self.label_group)
        self.second = Text((WIDTH / 2, 240), "2. {:6}".format(score_string[1]), text_size, pg.Color("white"), self.label_group)
        self.third = Text((WIDTH / 2, 280), "3. {:6}".format(score_string[2]), text_size, pg.Color("white"), self.label_group)
        self.fourth = Text((WIDTH / 2, 320), "4. {:6}".format(score_string[3]), text_size, pg.Color("white"), self.label_group)
        self.fifth = Text((WIDTH / 2, 360), "5. {:6}".format(score_string[4]), text_size, pg.Color("white"), self.label_group)

        # Write the new hiscores to the hiscores file, with one score on each line
        data = []
        for i in hiscores:
            data.append(str(i) + "\n")

        with open(HISCOREFILE, 'w') as f:
            f.writelines(data)


# Quits the game
class Exit(GameState):
    def __init__(self):
        super(Exit, self).__init__()
        self.quit = True


if __name__ == "__main__":
    # Initialise pygame modules
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Platformer v:" + VERSION)
    
    # Dictionary stores instance of every game state to be switched to during runtime. 
    states = {
        "MAINMENU": MainMenu,
        "GAMEPLAY": Gameplay,
        "SAVEGAME": SaveGame,
        "LEVELLOAD": LevelLoad,
        "LOADGAME": LoadGame,
        "LEVELINTRO": LevelIntro,
        "LEVELPAUSE": LevelPause,
        "ENDLEVEL": EndLevel,
        "EXIT": Exit,
        "HISCORES": HighScores
    }

    # Create instance of the Game class, setting its initial state to the Main Menu
    game = Game(screen, states, "MAINMENU")
    game.run()

    # When execution is complete, close the game
    pg.quit()
    sys.exit()
