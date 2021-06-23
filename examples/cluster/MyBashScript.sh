#!/bin/bash

YOUR_NAME=$(whoami)   #Store your username into the var "YOUR_NAME"

echo "Hello ${YOUR_NAME}! Welcome to the bash script"
echo ""

WHERE_AM_I=$(pwd)   #Store your current directory
echo "You are here: $WHERE_AM_I"
echo ""

echo "I am going to take a nap now"
for i in {1..5}; do  #Loop over the numbers 1 - 5 and sleep for 2 sec
  echo "...zzzzz ($i)"
  sleep 2
done
echo "Ok I am awake now"
echo ""

FILES_IN_HOME_DIR=$(ls ~/)  #Store the names of all files in your home dir
echo "Your home directory files are:"
echo $FILES_IN_HOME_DIR
echo ""

if [[ -f ~/.bashrc ]]; then  #Check to see if your bashrc exists
  echo "Oh good, it looks like you have a .bashrc, you will need that"
else
  echo "Oh no! You don't have a .bashrc"
fi
echo ""

if [[ -d ~/work ]]; then  #Check to see if you have a directory called "work"
  echo "Oh good, you have a work directory"
else
  echo "You don't have a work directory called ~/work"
  echo "You could make one using: ln -s /data/user/$(whoami) work"
fi
echo ""

echo "Ok, bye!"
