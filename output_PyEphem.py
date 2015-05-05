

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

class Read_pyephem_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()
		
		# Pyephem routine
		self.open_pyephem(directorio_script)
		self.open_files_pyephem(index_satellite)

		os.chdir(directorio_script)

	def open_pyephem(self, directorio_script):

		import os

		# PyEphem data
		os.chdir(directorio_script + '/results/PyEphem')

		self.files_pyephem = os.listdir(os.getcwd())
		self.files_pyephem.sort()

	def open_files_pyephem(self, index_satellite):

		for i in range(index_satellite):
			self.open_file_pyephem(self.files_pyephem[i])
			self.satellite_name = self.files_pyephem[i]

	def open_file_pyephem(self, name):
	
		self.pyephem_simulation_time = []
		self.pyephem_alt_satellite = []
		self.pyephem_az_satellite = []
		
		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
				self.pyephem_simulation_time.append(int(line[0]))
				self.pyephem_alt_satellite.append(float(line[1]))
				self.pyephem_az_satellite.append(float(line[2]))
				

		self.pyephem_simulation_time = [int(item) for item in self.pyephem_simulation_time]
		self.pyephem_alt_satellite = [float(item) for item in self.pyephem_alt_satellite]		
		self.pyephem_az_satellite = [float(item) for item in self.pyephem_az_satellite]

