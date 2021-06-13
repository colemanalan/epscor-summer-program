#!/bin/env python3

#This script includes the creation of a custom module.
#We will use it to read in values from the frame and plot them

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
defaultFiles=glob.glob("/data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/12360/Level3_IC86.2012_12360_Run000*.i3.gz")
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, nargs='+', default=defaultFiles, help='List of CoREAS simulation files')
args = parser.parse_args()

#####################################################

class CalculateDistributions(icetray.I3Module):
  #This function is run right away when this class is created
  def __init__(self,ctx):
    icetray.I3Module.__init__(self,ctx)

    self.particleName = ""
    self.AddParameter("ParticleName", "Name of the I3Particle in the frame", self.particleName)


  #This function runs before any frames are read in
  def Configure(self):
    log_info("Configuring " + self.name)
    self.particleName = self.GetParameter("ParticleName")

    self.particleList = []


  #This function runs only on P-Frames
  def Physics(self, frame):
    if not self.particleName in frame:
      log_error("Did not find {} the frame, boss!".format(self.particleName))
      return

    particle = frame[self.particleName]

    self.particleList.append(particle)


  #This function runs after all frames are read in
  def Finish(self):
    log_info("We are now in the Finish step!")

    #############

    #Make a list of the energies of the particles
    energies = np.array([particle.energy for particle in self.particleList])

    #Make a list of the arrival directions of the particles
    zeniths = np.array([particle.dir.zenith for particle in self.particleList])
    azimuths = np.array([particle.dir.azimuth for particle in self.particleList])

    #Make a list of the impact locations on the ground
    coreX = np.array([particle.pos.x for particle in self.particleList])
    coreY = np.array([particle.pos.y for particle in self.particleList])
    
    #This usually gives the correct number of bins
    nHistBins = int(np.sqrt(len(energies))/2.)

    #############

    #Set up the layout of our plots
    NRows = 2
    NCols = 2
    gs = gridspec.GridSpec(NRows, NCols, wspace=0.2, hspace=0.2)
    fig = plt.figure(figsize=(6*NCols, 5*NRows))

    #Make a new axis on which to plot the cores
    #Color the points by the lg(E) of the event
    ax = fig.add_subplot(gs[0,0])
    scat = ax.scatter(coreX / I3Units.m, coreY / I3Units.m, c=np.log10(energies/I3Units.eV), s=30)
    cbar = fig.colorbar(scat)
    ax.set_xlabel("East / m")
    ax.set_ylabel("North / m")
    ax.set_aspect("equal") #Don't let the range of the axis distort the picture

    #Make a new axis on which to plot the energies
    ax = fig.add_subplot(gs[0,1])
    ax.hist(energies / I3Units.eV, bins=nHistBins)
    ax.set_xlabel("Energy / eV")
    ax.set_ylabel("Counts")

    #Make a new axis on which to plot the zeniths
    ax = fig.add_subplot(gs[1,0])
    ax.hist(zeniths / I3Units.degree, bins=nHistBins)
    ax.set_xlabel("Zenith Angle / deg")
    ax.set_ylabel("Counts")

    #Make a new axis on which to plot the zeniths
    ax = fig.add_subplot(gs[1,1])
    ax.hist(azimuths / I3Units.degree, bins=nHistBins)
    ax.set_xlabel("Azimuth Angle / deg")
    ax.set_ylabel("Counts")


    filename = "ParticleInformation.pdf"
    print("Saving", filename)
    fig.savefig(filename, bbox_inches='tight') #The "tight" argument removes some whitespace


#####################################################

#This filter will help us keep only the useful events for which the reconstruction worked properly
def ITStdFilter(frame):
    return ('IT73AnalysisIceTopQualityCuts' in frame and all(frame["IT73AnalysisIceTopQualityCuts"].values()))

#####################################################


# Make the "IceTray"
tray = I3Tray()

#This is a pre-defined module which reads the I3 files that we use to store data
tray.AddModule("I3Reader", "reader", FilenameList = args.input)

#Run our filter here
tray.AddModule(ITStdFilter, "Filter", streams=[icetray.I3Frame.Physics])

#Add our module to the frame, give it whatever name you want as the second argument
#We have the parameter "ParticleName" defined in the __init__ and Configure functions
#which we can set using the corresponding argument
tray.AddModule(CalculateDistributions, "MyFunNameHere", 
                # ParticleName = "Laputop"
                ParticleName = "MCPrimary"  #You can try this one instead
              )

#Ready, set, go
tray.Execute()