#!/bin/bash

YOUR_NAME=$(whoami)

echo "Hello ${YOUR_NAME}! Welcome to the bash script"
echo ""

WHERE_AM_I=$(pwd)
echo "You are here: $WHERE_AM_I"
echo ""

echo "I am going to take a nap now"
for i in {1..5}; do
  echo "...zzzzz ($i)"
  sleep 2
done
echo "Ok I am awake now"
echo ""

FILES_IN_HOME_DIR=$(ls ~/)
echo "Your home directory files are:"
echo $FILES_IN_HOME_DIR
echo ""

if [[ -f ~/.bashrc ]]; then
  echo "Oh good, it looks like you have a .bashrc, you will need that"
else
  echo "Oh no! You don't have a .bashrc"
fi
echo ""

if [[ -d ~/work ]]; then
  echo "Oh good, you have a work directory"
else
  echo "You don't have a work directory called ~/work"
  echo "You could make one using: ln -s /data/user/$(whoami) work"
fi
echo ""

echo "Ok, bye!"