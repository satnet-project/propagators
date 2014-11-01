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

bar=(
'#                (4%)' '#                (7%)'
'##              (10%)' '##              (13%)'
'###             (17%)' '###             (20%)'   
'####            (24%)' '####            (28%)'
'#####           (31%)' '#####           (34%)'
'######          (38%)' '######          (41%)'
'#######         (44%)' '#######         (47%)'
'#######         (50%)' '########        (54%)'
'########        (57%)' '#########       (62%)'	
'#########       (66%)' '##########      (70%)'
'##########      (73%)' '###########     (77%)'
'###########     (80%)' '############    (84%)'
'############    (87%)' '#############   (90%)'
'#############   (94%)' '##############  (97%)' 
'############## (100%)')

cd TLEs/

n=0

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
		printf ' %0.s' {0..70}
		printf "\r"
		echo -ne "Family [$n/29] updated!\t ${bar[$n]}\t ${bold}$i${normal}\r"
		sleep 0.2
	fi;
	
	n=$[$n + 1]
	
done	

cd ..