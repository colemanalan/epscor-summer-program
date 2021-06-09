from icecube import dataclasses

#Converts the IceCube class OMKey to a more simple one
#This casts away the offset of the OM at 61
def GetKeyFromTankKey(tankkey):
  om = int(tankkey.om)
  string = int(tankkey.string)

  return (int((string)*2 - 1), int((om-61)/2))