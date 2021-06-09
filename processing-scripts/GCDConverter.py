#!/bin/env python3

from utils.geometry import Position, Geometry
from utils import keytools

import pickle

from I3Tray import *
from icecube import icetray, dataio, dataclasses
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

    for key in omgeo.keys():
      if not (61 <= key.om <= 64):
        continue 

      newkey = keytools.GetKeyFromTankKey(key)

      self.geom.AddPosition(newkey, Position(omgeo[key].position))

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