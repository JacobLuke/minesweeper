from Tkinter import *

from Game import Game

class SettingsGUI(object):
    def __init__ (self, settings, root=None, callback=None):
      self.settings = settings
      self.started = root is not None
      if root is None:
        root = Tk()
        root.withdraw()
        callback = root.destroy
      self.window = Toplevel(root)
      
      self.callback = callback
      
      modeFrame = Frame(self.window)
      modeFrame.grid(row=0, column=0, columnspan=4, sticky=N)
      mode = self.settings['MODE']
      self.modeVar = IntVar()
      if isinstance(mode, int):
        self.modeVar.set(mode)
      elif isinstance(mode, tuple):
        self.modeVar.set(Game.Mode.CUSTOM)
      
      for text, val, pos in ( ("Beginner\n9x9\n10 mines", Game.Mode.BEGINNER, 0),
                         ("Intermediate\n16x16\n40 mines", Game.Mode.INTERMEDIATE, 1),
                         ("Advanced\n16x30\n99 mines", Game.Mode.ADVANCED, 2) ):
        Radiobutton ( modeFrame, 
                     text=text, 
                     variable=self.modeVar, 
                     val=val, 
                     justify=LEFT, 
                     command = self.disableCustom
                    ).grid(row=pos, column=0, sticky=W)
      custFrame = Frame(modeFrame)
      custFrame.grid(row=0, column=1, rowspan=3)
      
      Radiobutton ( custFrame,
                    text="Custom", 
                    variable=self.modeVar, 
                    val=Game.Mode.CUSTOM, 
                    justify=LEFT,
                    command=self.enableCustom
                  ).grid(row=0, column=0, sticky=E)
      
      self.customEntries = []
      custFieldFrame = Frame(custFrame)
      custFieldFrame.grid(row=1, column=0, columnspan=3)
      for i,param in enumerate(("Height:", "Width:", "Mines:")):
        lbl = Label(custFieldFrame, text=param)
        lbl.grid(row=i,column=0, sticky=E)
        entry = Entry(custFieldFrame)
        entry.grid(row=i, column=1, sticky=W)
        self.customEntries.append(entry)
      
      if self.modeVar.get() == Game.Mode.CUSTOM:
        for i, param in enumerate(mode):
          self.customEntries[i].insert(0, str(param))
      else:
        self.disableCustom()
      
      self.cancelled = False
      
      self.window.protocol("WM_DELETE_WINDOW", self.cancel)
      
      Button(self.window, text="OK", command=self.accept).grid(row=3, column=1, sticky=SW)
      Button(self.window, text="Cancel", command=self.cancel).grid(row=3, column=2, sticky=SE)
      
      if not self.started:
        root.mainloop()
    
    def enableCustom(self, event=None):
      for widget in self.customEntries:
        widget.config(state=NORMAL)
      
    def disableCustom(self, event=None):
      for widget in self.customEntries:
        widget.config(state=DISABLED)
    
    
    def accept(self):
      if self.modeVar.get() != Game.Mode.CUSTOM:
        self.settings['MODE'] = self.modeVar.get()
      else:
        try:
          height, width, mines = (int(field.get()) for field in self.customEntries)
        except:
          pass
        else:
          clamp = lambda val, lo, hi: lo if val < lo else hi if val > hi else val
          height = clamp(height, 9, 24)
          width = clamp(width, 9, 30)
          mines = clamp(mines, 10, int(round(.875 * width * height)))
          self.settings['MODE'] = height, width, mines
      self.callback()
      
    def cancel(self):
      self.cancelled = True
      self.callback()