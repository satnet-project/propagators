

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


class Save_sims:
        
    # Crear una clase aparte

    
    index = 0
    i = 0

    text = []
    text.append("==================================")
    from sys import argv
    text.append(" Family %s" %(argv[1]))
    text.append("==================================")

    for i in range(self.length):

        import get_elements
        object_name = get_elements.Get_name(i)

        text.append(" Satellite: %s" %(object_name.name))

        from sys import argv
        from output_data import Check_data
        actual_available = Check_data(index, object_name.name, argv[2], argv[3])
        available_STK = actual_available.STK 

        if available_STK == 'yes':

            available_predict = actual_available.predict
            available_pyephem = actual_available.pyephem
            available_pyorbital = actual_available.pyorbital
            available_orbitron = actual_available.orbitron

            from output_data import Read_data
            from sys import argv
            data = Read_data(index, index, index, \
            index, self.object_name.name, index, argv[2], argv[3])

            if available_predict == 'yes':

                (std_predict_alt, std_predict_az) = data.STK_vs_predict()

                std_predict_alt = round(float(std_predict_alt), 7)
                std_predict_az = round(float(std_predict_az), 7)

                text.append(" predict data")
                text.append(" Alt: %s Az: %s" %(std_predict_alt, std_predict_az))

            if available_pyephem == 'yes':

                (std_pyephem_alt, std_pyephem_az) = data.STK_vs_PyEphem()

                std_pyephem_alt = round(float(std_pyephem_alt), 7)
                std_pyephem_az = round(float(std_pyephem_az), 7)

                text.append(" PyEphem data")
                text.append(" Alt: %s Az: %s" %(std_pyephem_alt, std_pyephem_az))

            if available_pyorbital == 'yes':

                (std_pyorbital_alt, std_pyorbital_az) = data.STK_vs_PyOrbital()

                std_pyorbital_alt = round(float(std_pyorbital_alt), 7)
                std_pyrobital_az = round(float(std_pyorbital_az), 7)

                text.append(" PyOrbital data")
                text.append(" Alt: %s Az: %s" %(std_pyorbital_alt, std_pyorbital_az))

            if available_orbitron == 'yes':

                (std_orbitron_alt, std_orbitron_az) = data.STK_vs_Orbitron()

                std_orbitron_alt = round(float(std_orbitron_alt), 7)
                std_orbitron_az = round(float(std_orbitron_az), 7)

                text.append(" Orbitron data")
                text.append(" Alt: %s Az: %s" %(std_orbitron_alt, std_orbitron_az))


        elif available_STK == 'no':

            print "Data don't available %s" %(i)

        else:

            pass
            # pass

        i = i + 1
        index = index + 1
        text.append("")

    return text

    # save in pdf file