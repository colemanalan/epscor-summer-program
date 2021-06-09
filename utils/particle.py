import numpy as np

from enum import Enum
from .geometry import Position

class ParticleType(Enum):
  """Enum class for the status/mass of the particle """
  NOT_SET = 1
  RECO = 2
  PROTON = 3
  HELIUM = 4
  OXYGEN = 5
  SILICON = 6
  IRON = 7
    

class Particle(object):
  """Class with information about the primary particle""" 

  def __init__(self):
    self.dir = np.array([1.,0.,0.]) #x,y,z unit vector
    self.pos = Position() #x,y,z of location
    self.energy = 0. #Particle energy in eV
    self.type = ParticleType.NOT_SET #See ParticleType enum


  def __str__(self):
    string = ""
    string += "Type: {0}\n".format(self.GetType())
    if self.GetEnergy() > 0:
      string += "Energy: {0:0.2f} lg(E/eV)\n".format(np.log10(self.GetEnergy()))
    else:
      string += "Energy: NOT ASSIGNED\n"
    string += "Zenith: {0:0.2f} deg  Azimuth: {1:0.2f} deg\n".format(self.GetZenith()*180/np.pi, self.GetAzimuth()*180/np.pi)
    string += "Position: " + str(self.pos)

    return string


  def SetType(self, x):
    assert(x in ParticleType)
    self.type = x

  def GetType(self):
    return self.type

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

  def SetPosition(self, pos):
    if isinstance(pos, Position):
      self.pos = pos
    else:
      self.pos = Position(pos)

  def GetPosition(self):
    return pos


  def SetEnergy(self, eng):
    self.energy = eng

  def GetEnergy(self):
    return self.energy


  #Calculates the angle between this particle's trajectory and another particle's
  #other: another instance of the Particle class
  def GetOpeningAngle(self, other):
    assert(isinstance(other, Particle)) #You must give this function a particle
    dotProd = sum(self.dir * other.dir)
    return np.arccos(dotProd)