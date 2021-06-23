#!/bin/bash

#This program shows how to use arguments
echo "I got some arguments in $0" #  $0 always stores the name of the program
echo "The first argument is:  $1" #  $1 is the first argument passed
echo "The second argument is:  $2" # $2 is the second one, etc.


#This loop will nap for the number of seconds that you passed in argument 2
echo ""
echo "I will nap based on your second argument"
for i in $(seq 1 $2); do
  echo "...zzzzz ($i)"
  sleep 2
done
echo "Ok I am awake now"
echo ""

#Make an error so we can see it later
echo "I am going to generate some error output"
ls /this/does/not/exist.txt
echo ""

echo "Ok, bye!"
