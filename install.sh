#!/bin/bash

DIR=$(pwd)

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential -y
sudo apt-get install python-dev -y
sudo apt-get install wine -y
sudo apt-get install python-pip -y
sudo apt-get install python-matplotlib
sudo pip install pyephem
sudo pip install pyorbital

# Compile Predict
cd predict-mod
ls
cd ..

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
OPT="Yes No"
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
	else
		echo ">>> Invalid Selection";
	fi
done

echo $INSDIR

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
# Propagators 
cp do_list.py ~/$INSDIR					# PyEphem script
cp do_list2.py ~/$INSDIR				# PyOrbital script
cp do_list2.sh ~/$INSDIR				# predict script
# Auxiliary scripts
cp get_elements.py ~/$INSDIR			# Get elements from TLE
cp get_names.py ~/$INSDIR				# Get satellite names from TLE file
cp update_tles.sh ~/$INSDIR				# Update TLE files from Celestrak