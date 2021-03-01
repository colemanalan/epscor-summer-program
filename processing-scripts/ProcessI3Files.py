#!/bin/env python3

from utils import event, particle

import pickle

from I3Tray import *
from icecube import icetray, dataio, phys_services
from icecube.icetray import I3Units
from icecube.icetray.i3logging import log_fatal, log_info

import os
ABS_PATH_HERE=str(os.path.dirname(os.path.realpath(__file__)))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, nargs='+', default=[], help='Input data files.')
parser.add_argument('--gcd', type=str, default="/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_IC86_Merged.i3.gz", help='GCD file for the event')
parser.add_argument('--output', type=str, required=True, default="", help='GCD file for the event')
args = parser.parse_args()



class CrunchFiles(icetray.I3Module):
  def __init__(self,ctx):
    icetray.I3Module.__init__(self,ctx)
    self.eventList = [] 

    self.pulseNames = []
    self.AddParameter("PulseNames", "Frame name of the pulses to store", self.pulseNames)

  def Configure(self):
    self.pulseNames = self.GetParameter("PulseNames")

  def Physics(self,frame):

    if "MCPrimary" in frame:
      primary = frame["MCPrimary"]
    elif "PolyplopiaPrimary" in frame:
      primary = frame["PolyplopiaPrimary"]    
    elif "I3MCTree_preMuonProp" in frame:
      primary = frame["I3MCTree_preMuonProp"][0]
    else:
      log_fatal("I could not find a valid primary")

    mcParticle = particle.Particle()
    mcParticle.SetStatus(particle.ParticleStatus.PRIMARY)
    mcParticle.SetDirection(primary.dir.zenith, primary.dir.azimuth)
    mcParticle.SetEnergy(primary.energy / I3Units.eV)
    mcParticle.SetType(primary.type_string)


    evt = event.Event()
    evt.SetPrimary(mcParticle)

    print(evt)

    for name in self.pulseNames:
      if not name in frame:
        print(frame)
        log_fatal("The object '{}' does not exist in the frame".format(name))

      pulses = frame[name]

      for key in pulses.keys():
        print(key)
        pulse = pulses[key]
        amp = pulse.charge
        time = pulse.time

        #TODO

    assert(False)

  def Finish(self):
    log_info("Making output file " + str(args.output))
    # plt.savefig(args.output, bbox_inches='tight')
    # plt.close()


tray = I3Tray()
tray.Add('I3Reader', 'TheReader',
          FilenameList = [args.gcd] + args.input
        )

tray.AddModule("I3NullSplitter","splitter",
               SubEventStreamName="DumpEvent"
               )

tray.AddModule(CrunchFiles, "Processor",
               PulseNames=["Test", "Test2"])

tray.Execute()