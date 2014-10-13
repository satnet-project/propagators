#!/bin/bash

bold=`tput bold`
normal=`tput sgr0`

echo "Updating orbital elements!"

files=('amateur' 'beidou' 'cubesat' 'dmc' 'education' \
'engineering' 'galileo' 'geo' 'glo-ops' 'globalstar'  \
'gorizont' 'gps-ops' 'intelsat' 'iridium' 'military'  \
'molniya' 'musson' 'nnss' 'noaa' 'orbcomm' 'other-comm' \
'radar' 'raduga' 'resource' 'sarsat' 'sbas' 'science' \
'tdrss' 'x-comm')

cd TLEs/

n=1

for i in ${files[@]};
do
	if [ -f $i ]
	then
		# Remove file
    	rm $i
	fi

	# Download new file
	wget -qr www.celestrak.com/NORAD/elements/$i.txt -O $i.txt

	# Check if file is empty
	if [[ -s $1 ]] ; then
		echo "Error downloading $i.txt"
	else
		echo -e "Family [$n/29] updated!\t ${bold}$i${normal}"
	fi;
	
	n=$[$n + 1]
	
done	

cd ..