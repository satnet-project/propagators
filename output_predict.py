

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

class Read_predict_data:

    def __init__(self, index_satellite):

        from os import getcwd, chdir

        index_satellite = index_satellite + 1
        directorio_script = getcwd()

        # predict routine
        self.open_predict(directorio_script)
        self.open_files_predict(index_satellite)

        chdir(directorio_script)

    def open_predict(self, directorio_script):

        from os import chdir, listdir, getcwd

        chdir(directorio_script + '/results/predict')

        self.files_predict = listdir(getcwd())
        self.files_predict.sort()
    
    def open_files_predict(self, index_satellite):

        for i in range(index_satellite):
            self.open_file_predict(self.files_predict[i])

    def open_file_predict(self, name):

        self.predict_simulation_time = []
        self.predict_alt_satellite = []
        self.predict_az_satellite = []

        import csv
        with open(name) as tsv:
            for line in csv.reader(tsv, delimiter = "\t"):
                if float(line[1]) >= 0:
                    linea0 = float(line[0])
                    self.predict_simulation_time.append(linea0)
                    self.predict_alt_satellite.append(float(line[1]))
                    self.predict_az_satellite.append(float(line[2]))