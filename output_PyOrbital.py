

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

class Read_pyorbital_data:

    def __init__(self, index_satellite):

        from os import chdir, getcwd, listdir

        index_satellite = index_satellite + 1
        directorio_script = getcwd()

        # pyorbital routine
        self.open_pyorbital(directorio_script, index_satellite)

        chdir(directorio_script)

    def open_pyorbital(self, directorio_script, index_satellite):

        from os import chdir, listdir, getcwd

        # pyorbital data
        chdir(directorio_script + '/results/PyOrbital')
        
        self.files_pyorbital = listdir(getcwd())
        self.files_pyorbital.sort()

        if not self.files_pyorbital:
            print "PyOrbital hasn't data available!"
        else:
            self.open_files_pyorbital(index_satellite)

    def open_files_pyorbital(self, index_satellite):

        for i in range(index_satellite):
            self.open_file_pyorbital(self.files_pyorbital[i])

    def open_file_pyorbital(self, name):

        self.pyorbital_simulation_time = []
        self.pyorbital_alt_satellite = []
        self.pyorbital_az_satellite = []

        import csv

        with open(name) as tsv:
            for line in csv.reader(tsv, delimiter = "\t"):
                self.pyorbital_simulation_time.append(line[0])
                self.pyorbital_alt_satellite.append(float(line[1]))
                self.pyorbital_az_satellite.append(float(line[2]))