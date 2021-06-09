from . import particle
from . import recodata

class Event(object):
  """Holds all the information for one triggered airshower"""
  def __init__(self):
    self.primary = particle.Particle()
    self.tankHits = {}
    self.itRecoValues = recodata.RecoData()
    self.customRecoValues = recodata.RecoData()

  def __str__(self):
    string = ""
    string += "=====Event=====\n"
    string += "# Stations: {}\n".format(len(self.tankHits))
    if self.primary.GetType() not in [particle.ParticleType.RECO, particle.ParticleType.NOT_SET]:
      string += "\n----MC Info----\n"
      string += str(self.primary) + '\n'
      string += '\n'

    string += "----Reco Pars----\n"
    string += '--IceTop Reco--\n'
    string += str(self.itRecoValues)

    if self.customRecoValues.status != recodata.RecoStatus.NOT_PERFORMED:
      string += "\n--Cutstom Reco--\n"
      string += str(self.customRecoValues)

    string += "===============\n"

    return string

  def AddHit(self, key, time, amp):
    self.tankHits[key] = (amp, time)

  def GetHit(self, key):
    if not key in self.tankHits:
      print("Key", key, "not found in the list of tank hits")

    return self.tankHits[key]

  def GetSignalAmp(self, key):
    if not key in self.tankHits:
      print("Key", key, "not found in the list of tank hits")

    return self.tankHits[key][0]

  def GetSignalTime(self, key):
    if not key in self.tankHits:
      print("Key", key, "not found in the list of tank hits")
      
    return self.tankHits[key][1]

  def GetPrimary(self):
    return self.primary

  def SetPrimary(self, x):
    assert(isinstance(x, particle.Particle))
    self.primary = x

  def SetITRecoValues(self, x):
    assert(isinstance(x, recodata.RecoData))
    self.itRecoValues = x

  def GetITRecoValues(self):
    return self.itRecoValues

  def SetCustomRecoValues(self, x):
    assert(isinstance(x, recodata.RecoData))
    self.customRecoValues = x

  def GetCustomRecoValues(self):
    return self.customRecoValues