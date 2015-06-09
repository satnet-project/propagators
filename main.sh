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
# Description: Comparison of the results obtained by using different propagators 
# agains STK simulations.
################################################################################

 #Remove old data
{
	cd TLEs/
	rm COPY*
	rm xa*

	cd ../results/predict
	rm SAT*
	rm temp

	cd ../PyEphem
	rm SAT*
	rm temp

	cd ../PyOrbital
	rm SAT*
	rm temp

	cd ../..
} &> /dev/null

clear

ACTUALDIR=`pwd`
TLESDIR="/TLEs/"



wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then

	if [ ! -d $ACTUALDIR$TLESDIR ]; then
		# If directory doesn't exist,
		# create it.
		mkdir TLEs/
		cd TLEs/
#		chmod +x update_tles.sh
#		./update_tles.sh

	elif [ -d $ACTUALDIR$TLESDIR ]; then
		# If directory exist,
		# check last TLE's update.
		cd TLEs/

		# Check if amateur.txt exist
		if [ ! -f amateur.txt ]; then
			# amateur.txt doesn't exist.
			# Update all data.
			# TO-DO. Update only files needed.
			cd ..

#			chmod +x update_tles.sh
#			./update_tles.sh
		
		elif [ -f amateur.txt ]; then
			# amateur.txt exist		
			# Check file's date
			file_month=`ls -Ald amateur.txt | awk '{print $6}'`
			system_month=`date +"%m"`

			file_day=`ls -Ald amateur.txt | awk '{print $7}'`
			system_day=`date +"%d"`

			cd ..

			if [ "$file_month" = "jan" ]; then
				declare month=1
			elif [ "$file_month" = "ene" ]; then
				declare month=1  
			elif [ "$file_month" = "feb" ]; then
				declare month=2 
			elif [ "$file_month" = "mar" ]; then
				declare month=3
			elif [ "$file_month" = "apr" ]; then
		       		declare month=4
			elif [ "$file_month" = "abr" ]; then
				declare month=4
			elif [ "$file_month" = "may" ]; then
 		       		declare month=5
			elif [ "$file_month" = "jun" ]; then
	        		declare month=6
			elif [ "$file_month" = "jul" ]; then
	        		declare month=7
			elif [ "$file_month" = "aug" ]; then
	        		declare month=8
			elif [ "$file_month" = "ago" ]; then
				declare month=8
			elif [ "$file_month" = "sep" ]; then
	        		declare month=9
			elif [ "$file_month" = "oct" ]; then
	        		declare month=10
			elif [ "$file_month" = "nov" ]; then
	        		declare month=11
			elif [ "$file_month" = "dec" ]; then
	        		declare month=12
			else
				echo "Invalid Month"
			fi

			if [ $month -lt $system_month ]; then
#				chmod +x update_tles.sh
#				./update_tles.sh

				echo "Database updated."
			else
				if [ $file_day -lt $system_day ]; then
#					chmod +x update_tles.sh
#					./update_tles.sh

					echo "Database updated."
				else
					echo "Database updated."
				fi
			fi
	
		fi

	fi

else
	echo "Offline - Update canceled."
fi


# TO-DO Test if predict.qth exists

echo " "

LOCATION=`awk 'NR==1' ~/.predict/predict.qth`
LATITUDE=`awk 'NR==2' ~/.predict/predict.qth`
LONGITUDE=`awk 'NR==3' ~/.predict/predict.qth`
ELEVATION=`awk 'NR==4' ~/.predict/predict.qth`

echo "In first place you must specify your location."
echo "Current location is: $LOCATION"
echo "Latitude: $LATITUDE"
echo "Longitude:  $LONGITUDE"
echo -e "Elevation: $ELEVATION\n" 

echo -e "Want to change it?"
CHANGES="No Yes"
select change in $CHANGES; do
	if [ "$change" = "Yes" ]; then
		# Absolut path because predict need it.
		rm ~/.predict/predict.qth
		echo -e "New location: \c"
		read -e NEW_LOCATION
		echo "New location...: $NEW_LOCATION"
		echo $NEW_LOCATION > ~/.predict/predict.qth
		echo -e "Latitude: \c"
		read -e NEW_LATITUDE
		echo $NEW_LATITUDE >> ~/.predict/predict.qth
		echo -e "Longitude: \c"
		read -e NEW_LONGITUDE
		echo $NEW_LONGITUDE >> ~/.predict/predict.qth
		echo -e "Elevation: \c"
		read -e ELEVATION
		echo $ELEVATION >> ~/.predict/predict.qth
		break

	elif [ "$change" = "No" ]; then
		echo -e "Location $LOCATION approved!"
		break

	else
		echo "Invalid Selection."

	fi
done

echo " "
echo "============================================================="
echo "Specify simulation start time."
echo "============================================================="

OPTIONSTIME="Now Another"
select opt_time in $OPTIONSTIME; do
	if [ "$opt_time" = "Now" ]; then
        echo -e "Simulation will start right now!\n"
		# Unix time
		DATE=`date +%s`
		echo $DATE
		break
	elif [ "$opt_time" = "Another" ]; then                
		echo -e "The starting date and time should be entered now."
		echo ""

		# Date
		echo -e "Day: \c"
		read -e DAY
		echo -e "Month: \c"
		read -e MONTH
		echo -e "Year: \c"
		read -e YEAR

		# Time
		echo -e "Hours (Two digits. 24 hours format.): \c"
		read -e HOURS
		echo -e "Minutes (Two digits): \c"
		read -e MINUTES
		echo -e "Seconds (Two digits): \c"
		read -e SECONDS

		DATE=`date -d "$YEAR-$MONTH-$DAY $HOURS:$MINUTES:$SECONDS" "+%s"`
		# Local time, i need universal time

		echo $DATE

		echo ""
		break
	else
		echo "Wrong chosen"
	fi
done

echo "============================================================="
echo "Set the simulation's interval."
echo "============================================================="


OPTIONSINTERVAL="1hour 1day user_defined"
select opt_interval in $OPTIONSINTERVAL; do
	if [ "$opt_interval" = "1hour" ]; then
		echo -e "1 hour time.\n"
		END_TIME=`expr $DATE + 3600`
		break

	elif [ "$opt_interval" = "1day" ]; then
		echo -e "1 day time.\n"
		END_TIME=`expr $DATE + 86400`
		break

	elif [ "$opt_interval" = "user_defined" ]; then
		echo -e "Set the simulation's range in seconds: \c"
		read -e USER_INTERVAL
		END_TIME=`expr $DATE + $USER_INTERVAL`
		echo " "
		break
	else
		echo ">>> Invalid Selection"
	fi
done

echo "============================================================="
echo "Choose a family!"
echo "============================================================="

cd TLEs/

select d in *; do 
	FAMILY=$d
	break 
done

cp $FAMILY COPY$FAMILY

cd ..

# Extract satellite names
python get_names.py $FAMILY

# Predict data
echo " "
echo "predict data"	
chmod +x predict_sims.sh
bash predict_sims.sh $FAMILY $DATE $END_TIME

# PyEphem data
python pyephem_sims.py $FAMILY $DATE $END_TIME

# pyorbital data
python pyorbital_sims.py $FAMILY $DATE $END_TIME

# Orbitron data
echo -e "\nPerfom Orbitron simulations"
echo -e "Parameters:"
echo -e "Family $FAMILY"
echo "Family $FAMILY"
echo -e "Introduce Orbitron simulations folder: \c"
read -e ORBITRON_FOLDER

# wine "C:\\Program Files\Orbitron\Orbitron.exe"

# Request for STK data
echo "Perfom STK simulations"
echo -e "Introduce STK simulations folder: \c"
read -e STK_FOLDER	
echo " "
echo "$FAMILY family simulations done!"

python gui.py $FAMILY $STK_FOLDER $ORBITRON_FOLDER

# Remove garbage
cd TLEs/

rm $FAMILY
rm xa*

mv COPY$FAMILY $FAMILY

cd ../results/predict
rm *

cd ../PyEphem
rm *

cd ../PyOrbital
rm *

cd ..
