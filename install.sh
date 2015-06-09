#!/bin/bash

################################################################################
# Copyright 2014 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
# Author: s.gongoragarcia[at]gmail.com
################################################################################

DIR=$(pwd)

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential -y
sudo apt-get install python-dev -y

# it seems that wine could give problems in 64 bits architectures
# must correct that issue

echo "Orbitron's installation"
sudo apt-get install wine -y
if `wget -qr http://www.stoff.pl/orbitron/files/orbitron.exe -O orbitron.exe`; then
	echo "Install Orbitron at default directory"
else
	if `wget -qr http://orbitron.fox07.de/orbitron.exe -O orbitron.exe`; then
		echo "Install Orbitron at default directory"
	else
		if `wget -qr http://orbitron.dreddi.net/orbitron.exe -O orbitron.exe`; then
			echo "Install Orbitron at default directory"
		else
			echo "Orbitron couldn't be downloaded"
		fi
	fi
fi

wine orbitron.exe

rm orbitron.exe

# Python libraries.
echo "Python libraries"	 
sudo apt-get install python-pip -y
sudo apt-get install python-matplotlib -y
sudo pip install pyephem
sudo pip install pyorbital

# Compile Predict.
sudo apt-get install libncurses5-dev -y
sudo apt-get install libncursesw5-dev -y
	
cd predict-mod
sudo ./configure
cd ..

# Remove trash.
sudo apt-get autoremove

clear
cd ~
echo "========================="
echo "= Please select folder: ="
echo "========================="



select D in */ ; do 
	test -n "$D" && break; 
	echo ">>> Invalid Selection"; 
done

echo " "
OPT="Yes No New_folder"
echo "$D is all right?"

select opt in $OPT;do
	if [ "$opt" = "Yes" ]; then
        	cd "$D"
        	echo -e "Folder $D selected!"
        	INSDIR="$D"
		break

	elif [ "$opt" = "No" ]; then     
        cd "$D"
        clear
        echo "========================="
		echo "= Please select folder: ="
		echo "========================="
		select SD in */ ; do 
			test -n "$SD" && break; 
			echo ">>> Invalid Selection"; 
		done
			
		echo " "
		OPT="Yes No"
		echo "$SD is all right?"

		select opt in $OPT;do
        	if [ "$opt" = "Yes" ]; then
        		cd "$SD"
        		echo -e "Folder $SD selected!"
        		INSDIR="$D$SD"
                	break

        	elif [ "$opt" = "No" ]; then     
        		cd "$D"
        		clear
        		echo "========================="
			echo "= Please select folder: ="
			echo "========================="
			select SSD in */ ; do 
				test -n "$SSD" && break; 
				echo ">>> Invalid Selection"; 
			done
			INSDIR="$D$SD$SSD"
			break
				
		else
			echo ">>> Invalid Selection";
		fi
		done
		break

	elif [ "$opt" = "New_folder" ]; then
		echo "Name..."
		read -e NEW_FOLDER
		mkdir $NEW_FOLDER
        	
		echo "========================="
		echo "= Please select folder: ="
		echo "========================="
		select SD in */ ; do 
			test -n "$SD" && break; 
			echo ">>> Invalid Selection"; 
		done

		echo -e "Folder $SD selected!"
		INSDIR="$D"
		break

	else
		echo ">>> Invalid Selection";
	fi
done

echo "Installation folder ~/$INSDIR"

cd $DIR

echo "Creating directories"
TEMPTLES="TLEs"
mkdir ~/$INSDIR$TEMPTLES				# TLEs folder
TEMPRESULTS="results"
mkdir ~/$INSDIR$TEMPRESULTS
mkdir ~/$INSDIR$TEMPRESULTS/predict		# predict simulations
mkdir ~/$INSDIR$TEMPRESULTS/PyEphem		# PyEphem simulations
mkdir ~/$INSDIR$TEMPRESULTS/PyOrbital	# PyOrbital simulations
mkdir ~/$INSDIR$TEMPRESULTS/Orbitron	# Orbitron simulations
mkdir ~/$INSDIR$TEMPRESULTS/STK			# STK simulations


echo "Copying files"
# Main routine
cp main.sh ~/$INSDIR					# BASH script
# Window routine
cp output_data.py ~/$INSDIR				# Output data to GUI
cp gui.py ~/$INSDIR						# UI
cp configure_simulations.py ~/$INSDIR	# Auxiliary UI
cp scrolledlist.py ~/$INSDIR			# List
# Propagators 
cp pyephem_sims.py ~/$INSDIR			# PyEphem script
cp pyorbital_sims.py ~/$INSDIR			# PyOrbital script
cp predict_sims.sh ~/$INSDIR			# predict script
# Auxiliary scripts
cp get_elements.py ~/$INSDIR			# Get elements from TLE
cp get_names.py ~/$INSDIR				# Get satellite names from TLE file
cp update_tles.sh ~/$INSDIR				# Update TLE files from Celestrak
# Output scripts
cp output_Orbitron.py ~/$INSDIR
cp output_PyOrbital.py ~/$INSDIR
cp output_PyEphem.py ~/$INSDIR
cp output_STK.py ~/$INSDIR
cp output_predict.py ~/$INSDIR
