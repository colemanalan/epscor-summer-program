#!/bin/env python3

#This script is an example on how to write a custom module. These are a bit more
#complicated than filters and include various standard functions

from I3Tray import I3Tray
from icecube import icetray, dataio, dataclasses
from icecube.icetray import I3Units
from icecube.icetray.i3logging import log_info, log_error
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_INFO)

import numpy as np

defaultFile="/data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/12360/Level3_IC86.2012_12360_Run000009.i3.gz"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, nargs='+', default=[defaultFile], help='List of CoREAS simulation directories')
args = parser.parse_args()

#####################################################

class CalculateDistributions(icetray.I3Module):
  def __init__(self,ctx):
    icetray.I3Module.__init__(self,ctx)

    self.particleName = ""
    self.AddParameter("ParticleName", "Name of the I3Particle in the frame", self.particleName)


  #This function runs before any frames are read in
  def Configure(self):
    log_info("Configuring " + self.name)
    self.particleName = self.GetParameter("ParticleName")

    self.azimuths = []
    self.zeniths = []


  #This function runs only on Q-Frames
  def DAQ(self, frame):
    log_info("This module does not do anything in the Q frames except say hello!")


  #This function runs only on P-Frames
  def Physics(self, frame):
    log_info("Found a P Frame!")

    if not self.particleName in frame:
      log_error("Did not find {} the frame, boss!".format(self.particleName))
      return

    particle = frame[self.particleName]

    self.azimuths.append(particle.dir.azimuth)
    self.zeniths.append(particle.dir.zenith)


  #This function runs after all frames are read in
  def Finish(self):
    log_info("We are now in the Finish step!")

    avgEnergy = np.average(self.azimuths)
    stdEnergy = np.std(self.azimuths)
    print("The azimuths are {0:0.2f} +/- {1:0.2f} deg".format(avgEnergy/I3Units.degree, stdEnergy/I3Units.degree))

    avgZenith = np.average(self.zeniths)
    stdZenith = np.std(self.zeniths)
    print("The zenith angles are {0:0.2f} +/- {1:0.2f} deg".format(avgZenith/I3Units.degree, stdZenith/I3Units.degree))


#####################################################

# Make the "IceTray"
tray = I3Tray()

#This is a pre-defined module which reads the I3 files that we use to store data
tray.AddModule("I3Reader", "reader", FilenameList = args.input)

#Add our module to the frame, give it whatever name you want as the second argument
#We have the parameter "ParticleName" defined in the __init__ and Configure functions
#which we can set using the corresponding argument
tray.AddModule(CalculateDistributions, "MyFunNameHere", 
                ParticleName = "Laputop"
                # ParticleName = "MCPrimary"  #You can try this one instead
              )

#Ready, set, go
tray.Execute()