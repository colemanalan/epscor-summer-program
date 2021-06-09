import numpy as np

class Position(object):
  """3D location"""
  def __init__(self, *args):
    self.location = np.array([0.,0.,0.])

    if len(args) == 1:
      pos = args[0]
      if isinstance(pos, Position):
        self.location = other.location
      elif (isinstance(pos, np.ndarray) or isinstance(pos, list)) and len(pos) == 3:
        self.location = np.asarray(pos)
      else:
        self.location[0] = pos[0]
        self.location[1] = pos[1]
        self.location[2] = pos[2]


    elif len(args) == 3:
      self.location[0] = pos[0]
      self.location[1] = pos[1]
      self.location[2] = pos[2]

  def __str__(self):
    return "({0:0.2f}, {1:0.2f}, {2:0.2f})".format(self.location[0],self.location[1],self.location[2])

  def __add__(self,other):
    return Position(self.location + other.location)

  def __iadd__(self,other):
    self.location += other.location
    return self

  def __sub__(self,other):
    return Position(self.location - other.location)

  def __isub__(self,other):
    self.location -= other.location
    return self

  def Magnitude(self):
    return np.sqrt(sum(self.location**2))


class Geometry(object):
  """Class which contains the layout of the detectors"""
  def __init__(self):
    self.positions = {}
    self.snowHeight = {}

  def __len__(self):
    return len(self.positions)

  def __call__(self, key):
    return self.positions[key], self.snowHeight[key]

  def AddPosition(self, key, pos):
    if isinstance(pos, Position):
      self.positions[key] = pos
    else:
      self.positions[key] = Position(pos)

    if not key in self.snowHeight:
      self.snowHeight[key] = 0.


  def AddSnowHeight(self, key, height):
    self.snowHeight[key] = height
    
