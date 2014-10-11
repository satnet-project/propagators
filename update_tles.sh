#!/bin/bash

echo "Updating orbital elements!"

cd TLEs/

if [ -f amateur.txt ]
then
	# Clean directory
    rm *
fi

wget -qr www.celestrak.com/NORAD/elements/amateur.txt -O amateur.txt
echo "amateur.txt updated!     [1/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/beidou.txt -O beidou.txt
echo "beidou.txt updated!      [2/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/cubesat.txt -O cubesat.txt
echo "cubesat.txt updated!     [3/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/dmc.txt -O dmc.txt
echo "dmc.txt updated!         [4/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/education.txt -O education.txt
echo "education.txt updated!   [5/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/engineering.txt -O engineering.txt
echo "engineering.txt updated! [6/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/galileo.txt -O galileo.txt
echo "galileo.txt updated!     [7/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/geo.txt -O geo.txt
echo "geo.txt updated!         [8/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/geodetic.txt -O geodetic.txt
echo "geodetic.txt updated!    [9/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/glo-ops.txt -O glo-ops.txt
echo "glo-ops.txt updated!    [10/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/globalstar.txt -O globalstar.txt
echo "globalstar.txt updated! [11/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/gorizont.txt -O gorizont.txt
echo "gorizont.txt updated!   [12/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/gps-ops.txt -O gps-ops.txt
echo "gps-ops.txt updated!    [13/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/intelsat.txt -O intelsat.txt
echo "intelsat.txt updated!   [14/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/iridium.txt -O iridium.txt
echo "iridium.txt updated!    [15/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/military.txt -O military.txt
echo "military.txt updated!   [16/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/molniya.txt -O molniya.txt
echo "molniya.txt updated!    [17/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/musson.txt -O musson.txt
echo "musson.txt updated!     [18/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/nnss.txt -O nnss.txt
echo "nnss.txt updated!       [19/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/noaa.txt -O noaa.txt
echo "noaa.txt updated!       [20/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/orbcomm.txt -O orbcomm.txt
echo "orbcomm.txt updated!    [21/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/other-comm.txt -O other-comm.txt
echo "other-comm.txt updated! [22/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/radar.txt -O radar.txt
echo "radar.txt updated!      [23/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/raduga.txt -O raduga.txt
echo "raduga.txt updated!     [24/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/resource.txt -O resource.txt
echo "resource.txt updated!   [25/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/sarsat.txt -O sarsat.txt
echo "sarsat.txt updated!     [26/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/sbas.txt -O sbas.txt
echo "sbas.txt updated!       [27/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/science.txt -O science.txt
echo "science.txt updated!    [28/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/tdrss.txt -O tdrss.txt
echo "tdrss.txt updated!      [29/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/x-comm.txt -O x-comm.txt
echo -e "x-comm.txt updated!     [30/30]\n"
sleep 0.3

cd ..