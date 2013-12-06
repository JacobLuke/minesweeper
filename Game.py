import random

class Game(object):
  class FlagType(object):pass
  
  NULL_FLAG = FlagType()
  MINE_FLAG = FlagType()
  Q_FLAG = FlagType()
  
  class State(object):pass
  
  WAITING = State()
  PLAYING = State()
  WON = State()
  LOST = State()
  
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
      self.flag = Game.NULL_FLAG
      self.adj = 0
      
    def getChar(self):
      if self.isClicked:
        if self.isMine:
          return Game.Square.MINE
        elif self.adj == 0:
          return Game.Square.EMPTY
        else:
          return str(self.adj)
      elif self.flag is Game.NULL_FLAG:
        return Game.Square.UNCLICKED
      elif self.flag is Game.MINE_FLAG:
        return Game.Square.FLAG
      else:
        return Game.Square.QUESTION      

  def __init__ (self, m, n, num_mines):
    self.m = m
    self.n = n
    self.time = 0
    self.num_mines = num_mines
    self.num_flagged = 0
    self.remaining = m * n - num_mines
    self.squares = {(i,j):Game.Square(i,j) for i in range(m) for j in range(n)}
    self.state = Game.WAITING
    
    self.printGrid()
    
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
    self.printGrid()
    
  def _click (self, i, j):
    if i < 0 or j < 0 or i >= self.m or j >= self.n: return
    square = self.squares[(i,j)]
    if square.isClicked or square.flag == Game.MINE_FLAG: return
    
    if self.state is Game.WAITING:
      self.state = Game.PLAYING
      lSquares = list(self.squares.keys())
      for sq in self.getAdj(i, j):
        lSquares.remove((sq.i, sq.j))
      random.shuffle(lSquares)
      mines = lSquares[:self.num_mines]
      for mine in mines:
        self.squares[mine].isMine = True
        for adj in self.getAdj(*mine):
          adj.adj += 1
    if self.state is Game.PLAYING:
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
    self.state = Game.WON
    print "GAME WON"
    
  def lose(self):
    for square in self.squares.values():
      square.isClicked = True
      square.adj = 0
    self.state = Game.LOST
    
  def isPlaying(self):
    return self.state is Game.PLAYING  
  
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
        if adj_square.flag == Game.MINE_FLAG:
          flagged.add(adj_square)
        else:
          unflagged.add(adj_square)
      if len(flagged) == square.adj:
        for adj in unflagged:
          self._click(adj.i, adj.j)            
      else:
        print len(flagged), "are flagged, expected", square.adj
    else:
      if square.flag == Game.NULL_FLAG:
        square.flag = Game.MINE_FLAG
        self.num_flagged += 1
      elif square.flag == Game.MINE_FLAG:
        square.flag = Game.Q_FLAG
        self.num_flagged -= 1
      else:
        square.flag = Game.NULL_FLAG
    self.printGrid()
class BeginnerGame(Game):
  def __init__(self):
    super(BeginnerGame, self).__init__(9,9,10)

class IntermediateGame(Game):
  def __init__(self):
    super(IntermediateGame, self).__init__(16,16,40)

class HardGame(Game):
  def __init__ (self):
    super(HardGame, self).__init__(16, 30, 99)
    