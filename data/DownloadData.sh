#!/bin/bash

#Run this script as: ./DownloadData.sh

HERE=$(dirname $(realpath -s $0))

PRIMS="Proton Helium Oxygen Iron" #Primary files
DETECTOR="DetectorLocations.obj" #Detector layout file

STORAGEDIR="epscor-summer2021/ml-data" #Name in Alan's dir where the data are stored

cd $HERE

if [[ -n $(hostname | grep "icecube.wisc.edu") ]]; then

  rsync -auP /home/acoleman/public_html/$STORAGEDIR/* ./

elif [[ -n $(whereis wget) ]]; then

  for PRIM in $PRIMS; do
    PRIMFILENAME="MonteCarlo_${PRIM}.obj"

    if [[ -f $HERE/$PRIMFILENAME ]]; then
      echo "$PRIMFILENAME is already here, skipping..."
    else
      wget https://user-web.icecube.wisc.edu/~acoleman/$STORAGEDIR/${PRIMFILENAME}
    fi
  done

  if [[ -f $HERE/$DETECTOR ]]; then
    echo "$DETECTOR is already here, skipping..."
  else
    wget https://user-web.icecube.wisc.edu/~acoleman/$STORAGEDIR/DetectorLocations.obj
  fi

else
  echo "You must either have wget installed or be on the Madison cluster to use this script"
fi


cd $(cd -) #Go back to wherever you were