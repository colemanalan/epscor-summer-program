import numpy as np

from enum import Enum

class ParticleStatus(Enum):
  """Enum class for the status of an """
  # def __init__(self, arg):
    # self.arg = arg

  NOT_SET = 1
  PRIMARY = 2
  RECO = 3
    

class Particle(object):
  """Class with information about the primary particle""" 

  def __init__(self):
    self.dir = np.array([1.,0.,0.])
    self.energy = 0.
    self.type = "UNKNOWN"
    self.status = ParticleStatus.NOT_SET


  def __str__(self):
    string = ""
    string += "Type: {0}  ({1})\n".format(self.GetType(), self.GetStatus())
    string += "Energy: {0} lg(E/eV)\n".format(np.log10(self.GetEnergy()))
    string += "Zenith: {0:0.2f} deg  Azimuth: {1:0.2f} deg".format(self.GetZenith()*180/np.pi, self.GetAzimuth()*180/np.pi)

    return string


  def SetType(self, x):
    self.type = x

  def GetType(self):
    return self.type


  def SetStatus(self, x):
    assert(x in ParticleStatus)
    self.status = x

  def GetStatus(self):
    return self.status


  def SetDirection(self, zen, azi):
    self.dir = np.array([np.sin(zen)*np.cos(azi), np.sin(zen)*np.sin(azi), np.cos(zen)])

  def GetUnitVector(self):
    return self.dir

  def GetZenith(self):
    return np.arccos(self.dir[2])

  def GetAzimuth(self):
    azi = np.arctan2(self.dir[1], self.dir[0])
    if azi < 0:
      azi += 2 * np.pi
    return azi


  def SetEnergy(self, eng):
    self.energy = eng

  def GetEnergy(self):
    return self.energy


  def GetOpeningAngle(self, other):
    assert(isinstance(other, Particle))
    dotProd = sum(self.dir * other.dir)
    return np.arccos(dotProd)