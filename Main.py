from Game import Game, BeginnerGame, IntermediateGame, AdvancedGame
from GUI import GUI
from Settings import Settings
from SettingsGUI import SettingsGUI
import sys

import Tkinter




game_by_mode = {Game.Mode.ADVANCED: AdvancedGame, Game.Mode.BEGINNER: BeginnerGame, Game.Mode.INTERMEDIATE: IntermediateGame}

class Minesweeper(object):
  def __init__ (self, *args):
    self.settings = Settings()
    self.game = self.getGame()
    
    self.gui = GUI(self.settings, self.game)
  
  def getGame(self):
    mode = self.settings['MODE']
    if mode in game_by_mode:
      return game_by_mode[mode](self.settings)
    elif mode is None:
      gui = SettingsGUI(self.settings)
      if gui.cancelled:
        sys.exit(0)
      return self.getGame()
    elif not isinstance(mode, tuple) or len(mode) != 3:
      raise ValueError("expected 3-tuple for Custom Game, got {0}".format(mode))
    return Game(self.settings,*mode)
  
  def run(self):
    return self.gui.start()
  
  def restart (self):
    self.game = self.getGame()
    self.gui = GUI(self.settings, self.game)


def main():
  m = Minesweeper()
  while True:
    result = m.run()
    if result is None: break
    m.restart()
  
if __name__ == '__main__':
  main()