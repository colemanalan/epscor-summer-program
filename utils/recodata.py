from . import particle

from enum import Enum

class RecoStatus(Enum):
  NOT_PERFORMED = 1
  FAILED = 2
  SUCEEDED = 3


class RecoData(object):
  """Holds the information for the reconstructed quantities of an airshower"""
  def __init__(self):
    self.recoParticle = particle.Particle()
    self.recoParticle.SetStatus(particle.ParticleStatus.RECO)
    self.status = RecoStatus.NOT_PERFORMED
    self.showerCurvature = 0.
    self.sRef = 0.
    self.ldfSlope = 1.

  def __str__(self):
    string = ""
    string += str(self.recoParticle) + '\n'
    string += "Sref: {0:0.2f} VEM\n".format(self.sRef)
    string += "LDF Slope: {0:0.2f}\n".format(self.ldfSlope)
    string += "Curvature: {0:0.2f} m\n".format(self.showerCurvature)
    string += "Status: {}\n".format(self.status)

    return string

  def SetRecoData(self, particle, sref, ldfSlope, curve):
    self.SetRecoParicle(particle)
    self.SetSRef(sref)
    self.SetLDFSlope(ldfSlope)
    self.SetShowerCurvature(curve)


  def SetSRef(self, x):
    self.sRef = x
    
  def GetSRef(self):
    return self.sRef


  def SetRecoParicle(self, x):
    assert(isinstance(x, particle.Particle))
    self.recoParticle = x

  def GetRecoParticle(self):
    return self.recoParticle


  def SetShowerCurvature(self, x):
    self.showerCurvature = x

  def GetShowerCurvature(self):
    return self.showerCurvature


  def SetLDFSlope(self, x):
    self.ldfSlope = x

  def GetLDFSlope(self):
    return ldfSlope