#!/bin/bash

echo "I got some arguments in $0"
echo "The first argument is:  $1"
echo "The second argument is:  $2"


echo ""
echo "I will nap based on your second argument"
for i in $(seq 1 $2); do
  echo "...zzzzz ($i)"
  sleep 2
done
echo "Ok I am awake now"
echo ""

echo "I am going to generate some error output"
ls /this/does/not/exist.txt
echo ""

echo "Ok, bye!"