import pickle


class Settings(object):
  FILE = ".mswpr"
  
  def __init__ (self):
    self.load()
  
  def load(self):
    try:
      with open(Settings.FILE, 'rb') as inf:
        self.dict = pickle.load(inf)
    except Exception as e:
      self.dict = self.default()
      print e
  
  
  def save(self):
    with open(Settings.FILE, 'wb') as outf:
      pickle.dump(self.dict, outf)
      
  def getState(self):
    return self.dict
  
  def __getitem__ (self, key):
    return self.dict[key]
  
  def __setitem__ (self, key, value):
    self.dict[key] = value
    self.save()
  
  def winGame(self):
    self.dict['WINS'] += 1
    self['GAMES'] += 1
    
  def loseGame(self):
    self['GAMES'] += 1
  
  
  def default(self):
    return {'MODE':None, 'WINS':0, 'GAMES':0}