#!/bin/env python3

#This example shows the way to add a filter to reject events based on the contents
#of the frames. 
#There is a P-Frame filter which rejects based on the reconstructed zenith angle
#You will need to be in an icecube environment to run this script!

from I3Tray import I3Tray
from icecube import icetray, dataio, dataclasses
from icecube.icetray import I3Units
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_INFO)

defaultFile="/data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/12360/Level3_IC86.2012_12360_Run000009.i3.gz"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, nargs='+', default=[defaultFile], help='List of CoREAS simulation directories')
args = parser.parse_args()

#######################################

#We define a very similar filter "module" that will run on P-Frames
#This will only allow reconstructions with a zenith angle less than
#13 deg to pass the filter and be processed by further frames.
def MyPFrameFilter(frame):
  print("MyPFrameFilter is running on a P frame")

  #If there is no reconstruction in the frame, skip it
  if not "Laputop" in frame:
    print("  the event is rejected because there is no reconstruction")
    return False

  recoParticle = frame["Laputop"]

  cut = recoParticle.dir.zenith < 13*I3Units.degree

  if not cut:
    print("  the event is rejected because the reconstructed"+
          "zenith angle is {0:0.1f} deg".format(recoParticle.dir.zenith/I3Units.degree))
    return False

  return True


#This isn't really a filter, it just lets us know when the filters were passed
def ZenithAlertScript(frame):
  print("This event passed the zenith filter!")
  print(frame["Laputop"])
  

#######################################

# Make the "IceTray"
tray = I3Tray()

#This is a pre-defined module which reads the I3 files that we use to store data
tray.AddModule("I3Reader", "reader", FilenameList = args.input)

#Add the P filter as a module to the tray
#Tell it to run only on the "Physics" frames
tray.Add(MyPFrameFilter, streams=[icetray.I3Frame.Physics])

#Add our alert script which will let us know when the filter passes
tray.Add(ZenithAlertScript, streams=[icetray.I3Frame.Physics])


#Ready, set, go
tray.Execute()