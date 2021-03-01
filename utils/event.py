from . import particle
from . import recodata

class Event(object):
  """Holds all the information for one triggered airshower"""
  def __init__(self):
    self.primary = particle.Particle()

    self.tankHits = []

    self.itRecoValues = recodata.RecoData()

  def __str__(self):
    string = ""
    string += "=====Event=====\n"
    string += "# Stations: {}\n".format(len(self.tankHits))
    if self.primary.GetStatus() == particle.ParticleStatus.PRIMARY:
      string += "\n----MC Info----\n"
      string += str(self.primary) + '\n'
      string += '\n'

    string += "----Reco Pars----\n"
    string += str(self.itRecoValues)
    string += '\n'

    string += "===============\n"

    return string

  def GetSignalAmp(self, key):
    return self.tankHits[key][0]

  def GetSignalTime(self, key):
    return self.tankHits[key][1]

  def GetPrimary(self):
    return self.primary

  def SetPrimary(self, x):
    assert(isinstance(x, particle.Particle))
    self.primary = x