#!/bin/env python3

import pickle
import numpy as np

from utils import event, geometry, particle, recodata

import os
ABS_PATH_HERE=str(os.path.dirname(os.path.realpath(__file__)))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, nargs='+', default=[], help='List of CoREAS simulation directories')
parser.add_argument('--geometry', type=str, default=ABS_PATH_HERE+"/../data/DetectorLocations.obj", help='Detector geometry file name')
args = parser.parse_args()


### Load the pickle file for the geometry
geometryFile = open(args.geometry, "rb")
detectorLocations = pickle.load(geometryFile)
print("Read in", len(detectorLocations), "optical modules")

### Load the pickle file for the geometry
eventList = []
for filename in args.input:
  eventFile = open(filename, "rb")
  eventList += pickle.load(eventFile)
print("Read in", len(eventList), "events")


event = eventList[0] #Just look at the first event for now

#First look at all the hit tanks in the event
print("There are", len(event.keys()), "hit tanks in the event")
for key in event.keys():
  print("    Key:", key)
  print("    Amplitude: {0:0.2f} VEM".format(event.GetSignalAmp(key)))
  print("    Time: {0:0.1f} ns".format(event.GetSignalTime(key)))
  pos, snowHeight = detectorLocations(key)
  print("    Detector location:", pos)
  print("    Snow height above detector: {0:0.2f} m".format(snowHeight))
  print("")


#Get the IceTop reconstruction information
iceTopReco = event.GetITRecoValues()
itParticle = iceTopReco.GetRecoParticle()
print("IceTop Reconstruction Data:")
print("    Energy estimator, lgSref: {0:0.3f}".format(iceTopReco.GetLgSRef()))
print("    Lateral Distribution Slope: {0:0.3f}".format(iceTopReco.GetLDFSlope()))
print("    Shower Curvature:", iceTopReco.GetShowerCurvature())
print("    Reconstruction Status:", iceTopReco.GetReconstructionStatus())
print("    Reconstruction particle below:")
print(itParticle)


#Simulated events will have a primary particle defined
primaryParticle = event.GetPrimary()
print("")
print("Monte Carlo Truth:")
print(primaryParticle)
print("")


#Compare how good the reconstruction of this shower was
coreDistance = (itParticle.GetPosition() - primaryParticle.GetPosition()).Magnitude()
angularSeparation = primaryParticle.GetOpeningAngle(itParticle) #This will be in radians
energyRatio = itParticle.GetEnergy() / primaryParticle.GetEnergy()

print("The reconstructed core was off by {0:0.2f} m".format(coreDistance))
print("The arrival direction was off by {0:0.1f} deg".format(angularSeparation * 180 / np.pi))
print("The energy was off by {0:0.1f}%".format((1 - energyRatio)*100))