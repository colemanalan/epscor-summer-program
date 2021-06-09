#!/bin/env python3

#Simulation data: /data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/
# UnThinned
# proton 12360
# iron 12362
# helium 12630
# oxygen 12631
# Thinned
# proton 20143
# iron 20144
# helium 20145
# oxygen 20146

from utils import event, particle, recodata
from utils import keytools

import pickle

from I3Tray import *
from icecube import icetray, dataio, phys_services, dataclasses
from icecube.icetop_Level3_scripts import icetop_globals
from icecube.icetray import I3Units
from icecube.icetray.i3logging import log_fatal, log_info
from icecube.recclasses import I3LaputopParams, LaputopParameter as Par
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_INFO)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, nargs='+', default=[], help='Input data files.')
parser.add_argument('--gcd', type=str, default="/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_IC86_Merged.i3.gz", help='GCD file for the event')
parser.add_argument('--output', type=str, required=True, default="", help='Output pickle file')
args = parser.parse_args()


#IceTray module to read in the I3File data and convert it to the custom classes
#of this project. Produces a pickle file with all of the required data.
class CrunchFiles(icetray.I3Module):
  def __init__(self,ctx):
    icetray.I3Module.__init__(self,ctx)
    self.eventList = [] 

    self.pulseNames = []
    self.AddParameter("PulseNames", "Frame name of the pulses to store", self.pulseNames)

  def Configure(self):
    self.pulseNames = self.GetParameter("PulseNames")

  def ConvertParticle(self, inParticle):
    outParticle = particle.Particle()
    outParticle.SetDirection(inParticle.dir.zenith, inParticle.dir.azimuth)
    outParticle.SetEnergy(inParticle.energy / I3Units.eV)
    outParticle.SetPosition(inParticle.pos)

    typeString = inParticle.type_string
    if typeString == "PPlus":
      outParticle.SetType(particle.ParticleType.PROTON)
    elif typeString == "unknown":
      outParticle.SetType(particle.ParticleType.RECO)


    return outParticle


  def Physics(self,frame):
    if frame["I3EventHeader"].sub_event_stream != "ice_top":
      return

    if "MCPrimary" in frame:
      primary = frame["MCPrimary"]
    elif "PolyplopiaPrimary" in frame:
      primary = frame["PolyplopiaPrimary"]    
    elif "I3MCTree_preMuonProp" in frame:
      primary = frame["I3MCTree_preMuonProp"][0]
    else:
      log_fatal("I could not find a valid primary")

    mcParticle = self.ConvertParticle(primary)


    evt = event.Event()
    evt.SetPrimary(mcParticle)


    for name in self.pulseNames:
      if not name in frame:
        print(frame)
        log_fatal("The object '{}' does not exist in the frame".format(name))

      recoPulses = frame[name]
      if isinstance(recoPulses, (dataclasses.I3RecoPulseSeriesMapMask, dataclasses.I3RecoPulseSeriesMap)):
        recoPulses = dataclasses.I3RecoPulseSeriesMap.from_frame(frame, name)

      for key, pulses in recoPulses:
        pulse = pulses[0]
        amp = pulse.charge
        time = pulse.time

        newkey = keytools.GetKeyFromTankKey(key)
        evt.AddHit(newkey, time, amp)


    if "LaputopParams" in frame and "Laputop" in frame:
      recoParticle = self.ConvertParticle(frame["Laputop"])
      params = I3LaputopParams.from_frame(frame, "LaputopParams")

      # if params.value(Par.Log10_S125) < 0.5:
      #   return

      data = recodata.RecoData()
      data.SetValues(recoParticle, params.value(Par.Log10_S125), params.value(Par.Beta), params.value(Par.CurvParabA))
      data.GetRecoParticle().SetEnergy(params.energy()/I3Units.eV)

      evt.SetITRecoValues(data)

      if frame["Laputop"].fit_status == dataclasses.I3Particle.FitStatus.OK:
        evt.itRecoValues.status = recodata.RecoStatus.SUCEEDED
      elif frame["Laputop"].fit_status == dataclasses.I3Particle.FitStatus.InsufficientHits:
        return #Don't even include it here
      else:
        evt.itRecoValues.status = recodata.RecoStatus.FAILED

    else:
      log_fatal("Did not find any Laputop information in the frame")


    self.eventList.append(evt)

    if len(self.eventList) == 10000:
      self.RequestSuspension()

    # print(evt)
    # exit()


  def Finish(self):
    log_info("Making output file {} with {} events".format(str(args.output), len(self.eventList)))
    file = open(args.output, "wb")
    pickle.dump(self.eventList, file)
    file.close()


tray = I3Tray()
tray.Add('I3Reader', 'TheReader',
          FilenameList = [args.gcd] + args.input
        )

# tray.AddModule("I3NullSplitter","splitter",
#                SubEventStreamName="DumpEvent"
#                )

tray.AddModule(CrunchFiles, "Processor",
               # PulseNames=["OfflineIceTopSLCTankPulses", icetop_globals.icetop_HLCseed_clean_hlc_pulses])
               PulseNames=[icetop_globals.icetop_HLCseed_clean_hlc_pulses])

tray.Execute()