#!/bin/env python3

#This script includes the creation of a custom module.
#We will read in values from both the Geometry (G) and Physics (P)
#frames and use them to make a plot of the array

#Import matplotlib plotting libraries
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#Import some IceCube libraries
from I3Tray import I3Tray
from icecube import icetray, dataio, dataclasses
from icecube.icetray import I3Units
from icecube.icetray.i3logging import log_info, log_error
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_INFO)

#Numpy to handle calculation of statistics
import numpy as np

#Helps us load many file names at once
import glob

#Argparse helps handle passing in arguments to this script
defaultFiles = glob.glob("/data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/12360/Level3_IC86.2012_12360_Run001*.i3.gz")
defaultGCD = "/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2012.56063_V1_OctSnow.i3.gz"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--gcdfile', type=str, default=defaultGCD, help="The name of the GCD file to use")
parser.add_argument('--input', type=str, nargs='+', default=defaultFiles, help='List of CoREAS simulation files')
args = parser.parse_args()

#####################################################

class PlotOneEvent(icetray.I3Module):
  #This function is run right away when this class is created
  def __init__(self,ctx):
    icetray.I3Module.__init__(self,ctx)

    self.particleName = ""
    self.AddParameter("ParticleName", "Name of the I3Particle in the frame", self.particleName)

    self.pulseSeriesMapName = ""
    self.AddParameter("PulseSeriesMapName", "Name of the I3Particle in the frame", self.pulseSeriesMapName)


  #This function runs before any frames are read in
  def Configure(self):
    log_info("Configuring " + self.name)
    self.particleName = self.GetParameter("ParticleName")
    self.pulseSeriesMapName = self.GetParameter("PulseSeriesMapName")

  #This function runs only on P-Frames
  def Physics(self, frame):
    if not self.particleName in frame:
      log_error("Did not find {} the frame, boss!".format(self.particleName))
      return

    if not self.pulseSeriesMapName in frame:
      log_error("Did not find {} the frame, boss!".format(self.pulseSeriesMapName))
      return

    particle = frame[self.particleName]
    series = frame[self.pulseSeriesMapName]

    if not "I3Geometry" in frame:
      log_error("I do not see any geometry item in the frame, did you load a GCD file as well?")
      return

    geometry = frame["I3Geometry"]
    omgeo = geometry.omgeo #Holds the location of all DOMS in IceCube
    stationgeo = geometry.stationgeo #Holds information about the tanks only


    allHits = []
    allTimes = []
    xPositions = []
    yPositions = []

    #Now we will iterate over all the hit optical-modules (OMs) in the series
    for omkey in series.keys():
      hitSeries = series[omkey]
      pulse = hitSeries[0] #Get the first hit series
      allHits.append(pulse.charge)
      allTimes.append(pulse.time)

      location = omgeo[omkey].position
      xPositions.append(location.x)
      yPositions.append(location.y)




    #Now lets iterate over the ones that were not hit
    notHitXPos = []
    notHitYPos = []
    for stnkey in stationgeo.keys(): #Iterate over all stations
      for tank in stationgeo[stnkey]: #Iterate over the two tanks per station
        omList = tank.omkey_list

        anyFound = False #Keeps track if any of the DOMS in a tank were hit
        for omkey in omList: #Iterate over the OMs in each station
          if omkey in series.keys():
            anyFound = True

        if not anyFound: #If no doms in this tank, mark silent
          location = omgeo[omkey].position
          notHitXPos.append(location.x)
          notHitYPos.append(location.y)




    #Set up the layout of our plots
    NRows = 2
    NCols = 2
    gs = gridspec.GridSpec(NRows, NCols, wspace=0.2, hspace=0.2)
    fig = plt.figure(figsize=(6*NCols, 5*NRows))

    title = "Energy: {0:0.1f} PeV, Zenith: {1:0.1f} deg".format(particle.energy / I3Units.PeV, particle.dir.zenith / I3Units.degree)

    #Make a new axis
    ax = fig.add_subplot(gs[0])
    scat = ax.scatter(xPositions, yPositions, c=np.log10(allHits))
    cbar = fig.colorbar(scat)
    ax.scatter(notHitXPos, notHitYPos, color="gray", marker="x")
    ax.set_xlabel("East / m")
    ax.set_ylabel("North / m")
    ax.set_title(title)
    ax.set_aspect("equal") #Don't let the range of the axis distort the picture

    print("Alan", max(allTimes), min(allTimes))

    #Make a new axis on which to plot the energies
    ax = fig.add_subplot(gs[1])
    scat = ax.scatter(xPositions, yPositions, c=allTimes, cmap='plasma')
    cbar = fig.colorbar(scat)
    ax.scatter(notHitXPos, notHitYPos, color="gray", marker="x")
    ax.set_xlabel("East / m")
    ax.set_ylabel("North / m")
    ax.set_title(title)
    ax.set_aspect("equal") #Don't let the range of the axis distort the picture


    filename = "OneEvent.pdf"
    print("Saving", filename)
    fig.savefig(filename, bbox_inches='tight') #The "tight" argument removes some whitespace
    self.RequestSuspension() #Tells the tray to not process any more files


  #This function runs after all frames are read in
  def Finish(self):
    log_info("Everything is done!")


#####################################################

#This filter will help us keep only the useful events for which the reconstruction worked properly
def PreFilter(frame):
  cut1 = 'IT73AnalysisIceTopQualityCuts' in frame and all(frame["IT73AnalysisIceTopQualityCuts"].values())
  cut2 = "MCPrimary" in frame and frame["MCPrimary"].energy > 10*I3Units.PeV
  return (cut1 and cut2)

#####################################################


# Make the "IceTray"
tray = I3Tray()

#This is a pre-defined module which reads the I3 files that we use to store data
#Note that you have to load the gcd file first before any of the Q/P frames!
tray.AddModule("I3Reader", "reader", FilenameList = [args.gcdfile] + args.input)

#Run our filter here
tray.AddModule(PreFilter, "Filter", streams=[icetray.I3Frame.Physics])

#Add our module to the frame, give it the names of the particle to use and
#the IceTop pulse series to use
tray.AddModule(PlotOneEvent, "MyFunNameHere", 
                ParticleName = "MCPrimary",
                PulseSeriesMapName = "OfflineIceTopHLCTankPulses"
              )

#Ready, set, go
tray.Execute()