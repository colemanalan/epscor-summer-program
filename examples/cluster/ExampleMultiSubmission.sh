#!/bin/bash

#This program shows how to use arguments
echo "I got some arguments in $0" #  $0 always stores the name of the program
echo "The first argument is:  $1" #  $1 is the first argument passed
echo "The second argument is:  $2" # $2 is the second one, etc.
echo ""

SIM_DIR=/data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/$1/
echo "Will use simulations from this dir: $SIM_DIR"
echo ""

#We will use the argument to read in a specific files
FILES_TO_USE=$(ls $SIM_DIR/Level3_IC86.2012_12360_Run0120${2}?.i3.gz)

echo "This script would use these files:"
echo $FILES_TO_USE
echo ""

#Make an error so we can see it later
echo "I am going to generate some error output"
ls /this/does/not/exist.txt
echo ""

echo "Ok, bye!"
