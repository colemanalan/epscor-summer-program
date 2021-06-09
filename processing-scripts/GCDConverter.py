#!/bin/env python3

#./GCDConverter.py /cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.icesim3.i3.gz

from utils.geometry import Position, Geometry
from utils import keytools

import pickle

from I3Tray import *
from icecube import icetray, dataio, dataclasses
from icecube.icetray.i3logging import log_fatal, log_info
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_INFO)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, nargs='+', default=[], help='Input data files.')
parser.add_argument('--output', type=str, default="ConvertedGCD.obj", help='Output pickle file')
args = parser.parse_args()

class ConvertGCD(icetray.I3Module):
  def __init__(self,ctx):
    icetray.I3Module.__init__(self,ctx)

  def Configure(self):
    self.geom = Geometry()

  def Geometry(self, frame):
    omgeo = frame["I3Geometry"].omgeo
    stationgeo = frame["I3Geometry"].stationgeo

    for stnkey in stationgeo.keys():

      for tank in stationgeo[stnkey]:
        omList = tank.omkey_list

        for omkey in omList:
          newkey = keytools.GetKeyFromTankKey(omkey)

          self.geom.AddPosition(newkey, Position(omgeo[omkey].position))
          self.geom.AddSnowHeight(newkey, tank.snowheight)


  def Finish(self):
    log_info("Making output file {} with {} OMs".format(str(args.output), len(self.geom)))
    file = open(args.output, "wb")
    pickle.dump(self.geom, file)
    file.close()





tray = I3Tray()

tray.Add('I3Reader', 'TheReader',
          FilenameList = args.input
        )

tray.AddModule(ConvertGCD, "ConvertGCD",)

tray.Execute()