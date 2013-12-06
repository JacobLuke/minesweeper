from Tkinter import *
from Game import Game

class GUI(object):
  def __init__ (self, game):
    self.game = game
    self.root = Tk()
    self.root.withdraw()
    self.window = Toplevel(self.root)
    self.window.title("Minesweeper")
    self.window.protocol("WM_DELETE_WINDOW", self.cleanup)
    
    self.buttons = {}
    for square in game.squares:
      btn = Button(self.window, width=2, height=1, command=self.getClick(*square))
      btn.bind("<ButtonRelease-3>", self.getRightClick(*square))
      btn.grid(row=square[0], column=square[1])
      self.buttons[square] = btn
    
    self.timerId = None
    self.timer = Label(self.window)
    self.timer.grid(row=self.game.m, column=0)
    
    self.minesLeft = Label(self.window, text=str(self.game.num_mines))
    self.minesLeft.grid(row=self.game.m, column=self.game.n-1)
    
    self.update()
  
  def start(self):
    self.root.mainloop()
    
  
  def getClick(self, i, j):
    def f(*args):
      self.game.click(i, j)
      self.update()
      if self.timerId is None:
        self.tick()
    return f
  def getRightClick(self, i, j):
    def f(*args):
      print args
      self.game.rightClick(i,j)
      self.update()
      if self.timerId is None:
        self.tick()
    return f
  
  def tick(self):
    if not self.game.isPlaying(): return
    self.game.time += 1
    self.update()
    if self.game.time < 999:
      self.timerId = self.timer.after(1000, self.tick)
  
  def stopGame(self):
    if self.timerId is not None:
      self.timer.after_cancel(self.timerId)
      self.timerId = None
      
  def update(self):
    for coord in self.buttons:
      char = self.game.getChar(*coord)
      if char == Game.Square.UNCLICKED:
        self.buttons[coord].config(text="")
      elif char == Game.Square.FLAG or char == Game.Square.QUESTION or char == Game.Square.MINE:
        self.buttons[coord].config(text=char)
      elif isinstance(self.buttons[coord], Button):
        self.buttons[coord].destroy()
        lbl = Label(self.window, text=char, width=2, height=1)
        lbl.grid(row=coord[0], column=coord[1])
        lbl.bind("<ButtonRelease-3>", self.getRightClick(*coord))
        self.buttons[coord] = lbl
      else:
        self.buttons[coord].config(text=char)
    self.timer.config(text="%03d" % self.game.time)
    self.minesLeft.config(text="%03d" % (self.game.num_mines - self.game.num_flagged))
    if not self.game.isPlaying():
      self.stopGame()
    
  def cleanup(self):
    self.root.destroy()
    self.stopGame()