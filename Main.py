import Game
import GUI

BEGINNER = "BEGINNER"
INTERMEDIATE = "INTERMEDIATE"
HARD = "HARD"


class Minesweeper(object):
  def __init__ (self, mode):
    if mode == BEGINNER:
      self.game = Game.BeginnerGame()
    elif mode == INTERMEDIATE:
      self.game = Game.IntermediateGame()
    elif mode == HARD:
      self.game = Game.HardGame()
    else:
      self.game = Game.Game(*mode)
    self.gui = GUI.GUI(self.game)
  def run(self):
    self.gui.start()
  
  def restart (self, mode):
    if mode == BEGINNER:
      self.game = Game.BeginnerGame()
    elif mode == INTERMEDIATE:
      self.game = Game.IntermediateGame()
    elif mode == HARD:
      self.game = Game.HardGame()
    else:
      self.game = Game.Game(*mode)
    self.gui = GUI.GUI(self.game)
  def run(self):
    self.gui.start()

if __name__ == "__main__":
  m = Minesweeper(HARD)
  m.run()