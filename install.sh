#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install wine
sudo apt-get install python-pip

echo "Creating directories"
mkdir ~/propagators
mkdir ~/propagators/TLEs
mkdir ~/propagators/results/predict
mkdir ~/propagators/results/PyEphem
mkdir ~/propagators/results/PyOrbital
mkdir ~/propagators/results/Orbitron
mkdir ~/propagators/results/STK
cp main.sh ~/propagators
cp gui.py ~/propagators