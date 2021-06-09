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
    self.recoParticle.SetType(particle.ParticleType.RECO)
    self.status = RecoStatus.NOT_PERFORMED
    self.showerCurvature = 0.
    self.lgSRef = 0.
    self.ldfSlope = 1.

  def __str__(self):
    string = ""
    string += str(self.recoParticle) + '\n'
    string += "lgSref: {0:0.2f} lg(S/VEM)\n".format(self.lgSRef)
    string += "LDF Slope: {0:0.2f}\n".format(self.ldfSlope)
    string += "Curvature: {0:0.2f} m\n".format(self.showerCurvature)
    string += "Status: {}\n".format(self.status)

    return string

  def SetValues(self, particle, lgSRef, ldfSlope, curve):
    self.SetRecoParicle(particle)
    self.SetLgSRef(lgSRef)
    self.SetLDFSlope(ldfSlope)
    self.SetShowerCurvature(curve)


  def SetLgSRef(self, x):
    self.lgSRef = x
    
  def GetLgSRef(self):
    return self.lgSRef


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