import random

def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

class Game(object):
  Flag = enum('NULL', 'MINE', 'QUESTION')
  
  State = enum('WAITING', 'PLAYING', 'WON', 'LOST')
  
  Mode = enum('BEGINNER', 'INTERMEDIATE', "ADVANCED", CUSTOM=-1)
  
  
  
  
  class Square(object):
    UNCLICKED = "#"
    EMPTY = " "
    FLAG = "!"
    QUESTION = "?"
    MINE = "X"
    
    def __init__(self, i, j):
      self.i = i
      self.j = j
      self.isMine = False
      self.isClicked = False
      self.flag = Game.Flag.NULL
      self.adj = 0
      
    def getChar(self):
      if self.isClicked:
        if self.isMine:
          return Game.Square.MINE
        elif self.adj == 0:
          return Game.Square.EMPTY
        else:
          return str(self.adj)
      elif self.flag is Game.Flag.NULL:
        return Game.Square.UNCLICKED
      elif self.flag is Game.Flag.MINE:
        return Game.Square.FLAG
      else:
        return Game.Square.QUESTION      

  def __init__ (self, settings, m, n, num_mines):
    self.settings = settings
    self.m = m
    self.n = n
    self.time = 0
    self.num_mines = num_mines
    self.num_flagged = 0
    self.remaining = m * n - num_mines
    self.squares = {(i,j):Game.Square(i,j) for i in range(m) for j in range(n)}
    self.state = Game.State.WAITING
    self.listeners = set()
    #self.printGrid()
  
  def addListener(self, obj):
    self.listeners.add(obj)
  
  def printGrid(self):
    print '\n'.join(''.join(line) for line in self.getSquares())
    
  def getSquares(self):
    lines = [[' ' for j in range(self.n)] for i in range(self.m)]
    for i,j in self.squares:  
      lines[i][j] = self.squares[(i,j)].getChar()
    return lines
    
  def getChar(self, i, j):
    return self.squares[(i,j)].getChar()
  
  def click(self, i, j):
    self._click(i, j)
    self.notify()
    
  def _click (self, i, j):
    if i < 0 or j < 0 or i >= self.m or j >= self.n: return
    square = self.squares[(i,j)]
    if square.isClicked or square.flag == Game.Flag.MINE: return
    
    if self.state is Game.State.WAITING:
      self.state = Game.State.PLAYING
      lSquares = list(self.squares.keys())
      for sq in self.getAdj(i, j):
        lSquares.remove((sq.i, sq.j))
      lSquares.remove((i,j))
      
      random.shuffle(lSquares)
      mines = lSquares[:self.num_mines]
      for mine in mines:
        self.squares[mine].isMine = True
        for adj in self.getAdj(*mine):
          adj.adj += 1
    if self.state is Game.State.PLAYING:
      square = self.squares[(i, j)]
      square.isClicked = True
      if square.isMine:
        self.lose()
      else:
        self.remaining -= 1
        if self.remaining == 0:
          self.win()
        elif square.adj == 0:
          for adj in self.getAdj(i, j):
            self._click(adj.i, adj.j)
 
  def win(self):
    self.state = Game.State.WON
    self.settings.winGame()
    self.notify()
    print "GAME WON"
  
  def tick(self):
    if self.isPlaying():
      self.time += 1
      self.notify()
      
  def notify(self):
    for listener in self.listeners:
      listener.update()
  
  def lose(self):
    for square in self.squares.values():
      square.isClicked = True
      square.adj = 0
    self.state = Game.State.LOST
    self.notify()
    self.settings.loseGame()
    
  def isPlaying(self):
    return self.state is Game.State.PLAYING  
  
  def getAdj(self, i, j):
    for x in (i-1, i, i+1):
      for y in (j-1, j, j+1):
        if 0 <= x < self.m and 0 <= y < self.n and (x != i or y != j):
          yield self.squares[(x,y)]
  
  def rightClick(self, i, j):
    
    square = self.squares[(i,j)]
    if square.isClicked:
      #click unflagged adjacent if the right number is flagged
      flagged = set()
      unflagged = set()
      for adj_square in self.getAdj(i,j):    
        if adj_square.flag == Game.Flag.MINE:
          flagged.add(adj_square)
        else:
          unflagged.add(adj_square)
      if len(flagged) == square.adj:
        for adj in unflagged:
          self._click(adj.i, adj.j)            
      else:
        print len(flagged), "are flagged, expected", square.adj
    else:
      if square.flag == Game.Flag.NULL:
        square.flag = Game.Flag.MINE
        self.num_flagged += 1
      elif square.flag == Game.Flag.MINE:
        square.flag = Game.Flag.QUESTION
        self.num_flagged -= 1
      else:
        square.flag = Game.Flag.NULL
    self.notify()
    
class BeginnerGame(Game):
  def __init__(self, settings):
    super(BeginnerGame, self).__init__(settings, 9,9,10)

class IntermediateGame(Game):
  def __init__(self, settings):
    super(IntermediateGame, self).__init__(settings, 16,16,40)

class AdvancedGame(Game):
  def __init__ (self, settings):
    super(AdvancedGame, self).__init__(settings, 16, 30, 99)
    