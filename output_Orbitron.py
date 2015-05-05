

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

class Read_orbitron_data:

    def __init__(self, index_satellite, sat_selected, data_dir):
        
        file = data_dir + '/output.txt'

        import os.path
        from os import getcwd
        if os.path.exists(file):
            from os import getcwd, chdir
            index_satellite = index_satellite + 1
            script_dir = getcwd()
        
            # Orbitron routine
            self.open_file_orbitron(index_satellite, file, sat_selected)

            chdir(script_dir)

    def open_file_orbitron(self, index_satellite, file, sat_selected):

        open_file = open(file, 'r')
        file_lines = open_file.readlines()

        file_lines_converted = []

        for i in range(len(file_lines)):
            file_lines_converted.append(file_lines[i].rstrip('\r\n'))

        self.lineas_validas = []
        for i in range(len(file_lines_converted)):
            self.extract_data(file_lines_converted[i])

        self.process_data(sat_selected)

    def extract_data(self, line):

        if line[0:4] == '2014':
            self.lineas_validas.append(line)

    def process_data(self, sat_selected):

        self.orbitron_simulation_time = []
        self.orbitron_az_satellite = []
        self.orbitron_alt_satellite = []

        for i in range(len(self.lineas_validas)):
            sat_name = self.lineas_validas[i][20:36]
            sat_name = sat_name.strip(' ')

            if sat_name == sat_selected:
                year = self.lineas_validas[i][0:4]
                month = self.lineas_validas[i][5:7]
                day = self.lineas_validas[i][8:10]
                hour = self.lineas_validas[i][11:13]
                minute = self.lineas_validas[i][14:16]
                second = self.lineas_validas[i][17:19]

                unix_time = self.local_to_unix(year, month, day, hour, minute, second)

                az = self.lineas_validas[i][41:46]
                alt = self.lineas_validas[i][47:51]
                alt = alt.strip(' ')
                az = az.strip(' ')

                self.orbitron_simulation_time.append(unix_time)
                self.orbitron_az_satellite.append(az)
                self.orbitron_alt_satellite.append(alt)
                
        self.orbitron_simulation_time = [int(item) for item in self.orbitron_simulation_time]
        self.orbitron_alt_satellite = [float(item) for item in self.orbitron_alt_satellite]        
        self.orbitron_az_satellite = [float(item) for item in self.orbitron_az_satellite]

    def local_to_unix(self, year, month, day, hour, minute, second):

        from datetime import datetime
        d = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

        unix_time = d.strftime('%s')

        return unix_time