#!/bin/bash

################################################################################
# Copyright 2015 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
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


FILE=$1
START_TIME=$2
END_TIME=$3

END_TIME=`expr $END_TIME - 1`

SCRIPT_DIR=`pwd`

cd TLEs/

lines=`wc $FILE | awk {'print $1'}`

sats_number=`expr $lines / 3`

declare -i LIMIT=`expr $sats_number + 1`
declare -i n1=1
declare -i j1=1
IDEN=SAT

until [ $n1 -eq $LIMIT ]
do
	export n1
	export j1
	export IDEN

	perl -pi -e 's/.*/$ENV{IDEN}$ENV{n1}/ if $. == $ENV{j1}' $FILE

	j1=$[$n1 * 3]
	j1=$[$j1 + 1]
	n1=$[$n1 + 1]
done	

declare -i k=0
declare -i n=0
declare -i l=-1
declare -i j=0

cd ../

until [ $n -eq $sats_number ]
do

	l=$[$l + 1]
	j=$[$l * 3]
	j=$[$j + 1]

	cd TLEs/

	split -l 72 $FILE

	FILES_SPLITED="`ls x* | wc -l`"

	declare -a LIST_FILES_SPLITED
	LIST_FILES_SPLITED=(`ls x*`)

	export j
	export FAMILY
	export n

	SATELLITE="`awk 'NR==j2' j2="${j}" ${LIST_FILES_SPLITED[k]}`"
	FILESPLITTED="${LIST_FILES_SPLITED[k]}"

	# Llamar a la rutina segundo a segundo

	BEGIN=$START_TIME
	END=$END_TIME

	SATELLITEFILE=SATELLITEFILE
	SATELLITEFINAL=SATELLITEFINAL

	until [ $BEGIN -eq $END ]
	do
		predict -t $FILESPLITTED -f $SATELLITE $BEGIN -o $SATELLITEFILE
		value=`cat $SATELLITEFILE`

		if [ ${value:12:1} != "-" ]; then
			cat $SATELLITEFILE >> $SATELLITE	
		fi
		
		BEGIN=$[$BEGIN + 1]
		
	done
	
	mv $SATELLITE ../results/predict	
	cd ../

	m=$[$n + 1]

	echo -e "Predict - Simulation [$m/$sats_number] done!"

        n=$[$n + 1]

	if [ $l -eq 23 ]; then
		l=-1
		k=$[$k + 1]
	fi

done
