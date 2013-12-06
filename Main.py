import Game
import GUI

import Tkinter

BEGINNER = "BEGINNER"
INTERMEDIATE = "INTERMEDIATE"
HARD = "HARD"

game_by_mode = {HARD: Game.HardGame, BEGINNER: Game.BeginnerGame, INTERMEDIATE: Game.IntermediateGame}

class Minesweeper(object):
  def __init__ (self, *args):
    self.game = Minesweeper.getGame(*args)
    self.gui = GUI.GUI(self.game)
  
  @staticmethod
  def getGame(*args):
    if len(args) < 1:
      raise ValueError("need at least one argument for Minesweeper")
    if args[0] in game_by_mode:
      if len(args) != 1:
        raise ValueError("expected 1 argument, got {0}".format(len(args)))
      return game_by_mode[args[0]]()
    if len(args) != 3:
      raise ValueError("expected 3 arguments for Custom Game, got {0}".format(len(args)))
    return Game.Game(*args)
  
  def run(self):
    self.gui.start()
  
  def restart (self, *args):
    self.game = Minesweeper.getGame(*args)
    self.gui = GUI.GUI(self.game)

 
 
if __name__ == "__main__":
  m = Minesweeper(HARD)
  m.run()