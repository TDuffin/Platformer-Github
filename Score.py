from Settings import *

#Class which tracks the score for every level.
class Score:
    def __init__(self):
        self.score = 5000

    def update_score(self, integer):
        self.score += integer



