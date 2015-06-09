

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


class Read_data:

	def __init__(self, index_pyephem, index_predict, index_pyorbital,\
	index_orbitron, sat_selected, index_STK, STK_dir, orbitron_dir):

		# Orbitron stuff
		self.file = '/home/dayvan/Documentos/propagators/results/Orbitron/dmc.txt'
		self.index_orbitron = index_orbitron + 1
		self.sat_selected = sat_selected
		# PyEphem stuff
		self.index_pyephem = index_pyephem
		# predict stuff		
		self.index_predict = index_predict
		# PyOrbital stuff
		self.index_pyorbital = index_pyorbital
		# STK stuff		
		self.index_STK = index_STK
		self.STK_dir = STK_dir
		self.orbitron_dir = orbitron_dir

		from os import getcwd
		self.directorio_script = getcwd()

	def STK_vs_predict(self):
		
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()				
		
		# predict routine
		from output_predict import Read_predict_data
		predict_data = Read_predict_data(self.index_predict)
		predict_simulation_time = predict_data.predict_simulation_time
		predict_alt_satellite = predict_data.predict_alt_satellite
		predict_az_satellite = predict_data.predict_az_satellite		
		
		# Differences
		list_alt = []
		list_az = []

		time_intersected_predict = []
		time_intersected_predict = list(set(STK_simulation_time).intersection(predict_simulation_time))

		i = 0

		for i in range(len(time_intersected_predict)):

			difference_alt = \
			float(predict_alt_satellite[predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(STK_alt_satellite[STK_simulation_time.index(time_intersected_predict[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(predict_az_satellite[predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(STK_az_satellite[STK_simulation_time.index(time_intersected_predict[i])])

			list_az.append(difference_az)

			i = i + 1

		# Force mean to zero
		m = 0

		from numpy import asarray, sqrt, mean
		alt = asarray(list_alt)
		az = asarray(list_az)
		
		# Standard deviation
		std_alt = sqrt(mean((alt-m)**2))
		std_az = sqrt(mean((az-m)**2))

		chdir(self.directorio_script)

		return std_alt, std_az

	def STK_vs_predict_comp(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite

		# predict routine
		from output_predict import Read_predict_data
		predict_data = Read_predict_data(self.index_predict)
		predict_simulation_time = predict_data.predict_simulation_time
		predict_alt_satellite = predict_data.predict_alt_satellite
		predict_az_satellite = predict_data.predict_az_satellite
		
		# Differences
		list_alt = []
		list_az = []

		time_intersected_predict = []
		time_intersected_predict = list(set(STK_simulation_time).intersection(predict_simulation_time))

		i = 0

		for i in range(len(time_intersected_predict)):

			difference_alt = \
			float(predict_alt_satellite[predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(STK_alt_satellite[STK_simulation_time.index(time_intersected_predict[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(predict_az_satellite[predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(STK_az_satellite[STK_simulation_time.index(time_intersected_predict[i])])

			list_az.append(difference_az)

			i = i + 1


		chdir(self.directorio_script)

		return time_intersected_predict, list_alt, list_az

	def STK_vs_PyEphem(self):

		from os import chdir
		chdir(self.directorio_script)	
		
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite
		
		from output_PyEphem import Read_pyephem_data
		PyEphem_data = Read_pyephem_data(self.index_pyephem)
		pyephem_simulation_time = PyEphem_data.pyephem_simulation_time
		pyephem_az_satellite = PyEphem_data.pyephem_az_satellite
		pyephem_alt_satellite = PyEphem_data.pyephem_alt_satellite	

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(STK_simulation_time).intersection(pyephem_simulation_time))

		i = 0

		for i in range(len(time_intersected)):

			difference_alt = \
			float(pyephem_alt_satellite[pyephem_simulation_time.index(time_intersected[i])]) - \
			float(STK_alt_satellite[STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyephem_az_satellite[pyephem_simulation_time.index(time_intersected[i])]) - \
			float(STK_az_satellite[STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		# Force mean to zero
		m = 0

		from numpy import asarray
		alt = asarray(list_alt)
		az = asarray(list_az)
		
		# Standard deviation
		from numpy import sqrt, mean
		std_alt = sqrt(mean((alt-m)**2))
		std_az = sqrt(mean((az-m)**2))

		chdir(self.directorio_script)

		return std_alt, std_az

	def STK_vs_PyEphem_comp(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite

		from os import chdir
		chdir(self.directorio_script)
		
		from output_PyEphem import Read_pyephem_data
		PyEphem_data = Read_pyephem_data(self.index_pyephem)
		pyephem_simulation_time = PyEphem_data.pyephem_simulation_time
		pyephem_az_satellite = PyEphem_data.pyephem_az_satellite
		pyephem_alt_satellite = PyEphem_data.pyephem_alt_satellite	

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(STK_simulation_time).intersection(pyephem_simulation_time))

		i = 0

		for i in range(len(time_intersected)):

			difference_alt = \
			float(pyephem_alt_satellite[pyephem_simulation_time.index(time_intersected[i])]) - \
			float(STK_alt_satellite[STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyephem_az_satellite[pyephem_simulation_time.index(time_intersected[i])]) - \
			float(STK_az_satellite[STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		chdir(self.directorio_script)

		return time_intersected, list_alt, list_az

	# Standard deviations		
	def STK_vs_PyOrbital(self):

		from os import chdir
		chdir(self.directorio_script)
		
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite
		
		from output_PyOrbital import Read_pyorbital_data
		PyOrbital_data = Read_pyorbital_data(self.index_pyorbital)
		pyorbital_simulation_time = PyOrbital_data.pyorbital_simulation_time
		pyorbital_az_satellite = PyOrbital_data.pyorbital_az_satellite
		pyorbital_alt_satellite = PyOrbital_data.pyorbital_alt_satellite

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(STK_simulation_time).intersection(pyorbital_simulation_time))

		i = 0

		for i in range(len(time_intersected)):
		
			difference_alt = \
			float(pyorbital_alt_satellite[pyorbital_time.index(time_intersected[i])]) -\
			float(STK_alt_satellite[STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyorbital_az_satellite[pyorbital_simulation_time.index(time_intersected[i])]) - \
			float(STK_az_satellite[STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		# Force mean to zero
		m = 0

		from numpy import asarray
		alt = asarray(list_alt)
		az = asarray(list_az)
		
		# Standard deviation
		from numpy import sqrt, mean
		std_alt = sqrt(mean((alt-m)**2))
		std_az = sqrt(mean((az-m)**2))

		chdir(self.directorio_script)

		return std_alt, std_az

	# Altitudes and azimuths
	def STK_vs_PyOrbital_comp(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite
		
		from output_PyOrbital import Read_pyorbital_data
		PyOrbital_data = Read_pyorbital_data(self.index_pyorbital)
		pyorbital_simulation_time = PyOrbital_data.pyorbital_simulation_time
		pyorbital_az_satellite = PyOrbital_data.pyorbital_az_satellite
		pyorbital_alt_satellite = PyOrbital_data.pyorbital_alt_satellite

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(STK_simulation_time).intersection(pyorbital_simulation_time))

		i = 0

		for i in range(len(time_intersected)):
		
			difference_alt = \
			float(pyorbital_alt_satellite[pyorbital_simulation_time.index(time_intersected[i])]) -\
			float(STK_alt_satellite[STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyorbital_az_satellite[pyorbital_simulation_time.index(time_intersected[i])]) - \
			float(STK_az_satellite[STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		chdir(self.directorio_script)

		return time_intersected, list_alt, list_az

	# Standard deviations		
	def STK_vs_Orbitron(self):
		
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite
		
		from output_Orbitron import Read_orbitron_data
		try:
			Orbitron_data = Read_orbitron_data(self.index_orbitron, self.sat_selected, self.orbitron_dir)
			orbitron_simulation_time = Orbitron_data.orbitron_simulation_time
			orbitron_az_satellite = Orbitron_data.orbitron_az_satellite
			orbitron_alt_satellite = Orbitron_data.orbitron_alt_satellite


			list_alt = []
			list_az = []

			time_intersected = []
			time_intersected = list(set(STK_simulation_time).intersection(orbitron_simulation_time))

			for i in range(len(time_intersected)):
		
				difference_alt = \
				float(orbitron_alt_satellite[orbitron_simulation_time.index(time_intersected[i])]) -\
				float(STK_alt_satellite[STK_simulation_time.index(time_intersected[i])])

				list_alt.append(difference_alt)

				difference_az = \
				float(orbitron_az_satellite[orbitron_simulation_time.index(time_intersected[i])]) - \
				float(STK_az_satellite[STK_simulation_time.index(time_intersected[i])])

				list_az.append(difference_az)

			# Force mean to zero
			m = 0

			from numpy import asarray
			alt = asarray(list_alt)
			az = asarray(list_az)
			
			# Standard deviation
			from numpy import sqrt
			std_alt = sqrt(mean((alt-m)**2))
			std_az = sqrt(mean((az-m)**2))

			return std_alt, std_az

		except:
			pass

		# Differences


	# Altitudes and azimuths	
	def STK_vs_Orbitron_comp(self):
		
		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		from output_STK import Read_STK_data
		STK_data = Read_STK_data(self.index_STK, self.STK_dir)
		STK_simulation_time = STK_data.STK_simulation_time
		STK_az_satellite = STK_data.STK_az_satellite
		STK_alt_satellite = STK_data.STK_alt_satellite

		from os import chdir
		chdir(self.directorio_script)
		
		from output_Orbitron import Read_orbitron_data
		try:
			Orbitron_data = Read_orbitron_data(self.index_orbitron, self.sat_selected, self.orbitron_dir)
			orbitron_simulation_time = Orbitron_data.orbitron_simulation_time
			orbitron_az_satellite = Orbitron_data.orbitron_az_satellite
			orbitron_alt_satellite = Orbitron_data.orbitron_alt_satellite

			# Differences
			list_alt = []
			list_az = []

			time_intersected = []
			time_intersected = list(set(STK_simulation_time).intersection(orbitron_simulation_time))

			for i in range(len(time_intersected)):
			
				difference_alt = \
				float(orbitron_alt_satellite[orbitron_simulation_time.index(time_intersected[i])]) -\
				float(STK_alt_satellite[STK_simulation_time.index(time_intersected[i])])

				list_alt.append(difference_alt)

				difference_az = \
				float(orbitron_az_satellite[orbitron_simulation_time.index(time_intersected[i])]) - \
				float(STK_az_satellite[STK_simulation_time.index(time_intersected[i])])

				list_az.append(difference_az)

			return time_intersected, list_alt, list_az
		except:
			pass

class Check_data:

	def __init__(self, index_satellite, sat_name, STK_folder, Orbitron_folder):

		index = index_satellite + 1
		satellite_name = "SAT%s" %(index)

		from os import getcwd, chdir
		self.directorio_actual = getcwd()

		self.check_predict(index_satellite, satellite_name)
		self.check_pyephem(index_satellite, satellite_name)
		self.check_pyorbital(index_satellite, satellite_name)
		self.check_orbitron(index_satellite, sat_name, Orbitron_folder)
		self.check_STK(index_satellite, STK_folder)

		chdir(self.directorio_actual)

	def check_predict(self, index, satellite_name):

		from os import chdir, listdir, getcwd
		chdir(self.directorio_actual + '/results/predict')
		
		files = listdir(getcwd())

		if satellite_name in files:
			self.predict = 'yes'
		else:
			self.predict = 'no'

	def check_pyephem(self, index, satellite_name):

		from os import chdir, listdir, getcwd
		chdir(self.directorio_actual + '/results/PyEphem')

		files = listdir(getcwd())

		if satellite_name in files:
			self.pyephem = 'yes'
		else:
			self.pyephem = 'no'

	def check_pyorbital(self, index, satellite_name):

		from os import chdir, listdir, getcwd
		chdir(self.directorio_actual + '/results/PyOrbital')

		files = listdir(getcwd())

		if satellite_name in files:
			self.pyorbital = 'yes'
		else:
			self.pyorbital = 'no'

	def check_orbitron(self, index, actual_sat_name, Orbitron_folder):

		file = Orbitron_folder + '/output.txt'

#		file = '/home/case/Orbitron/Output/output.txt'

		try:
			open_file = open(file, 'r')
			file_lines = open_file.readlines()

			file_lines_converted = []

			for i in range(len(file_lines)):
				file_lines_converted.append(file_lines[i].rstrip('\r\n'))

			lineas_validas = []
			for j in range(len(file_lines_converted)):
				if file_lines_converted[j][0:4] == '2014':
					lineas_validas.append(file_lines_converted[j])

			sats_name = []
			for k in range(len(lineas_validas)):
				sat_name = lineas_validas[k][20:36]
				sat_name = sat_name.strip(' ')

				sats_name.append(sat_name)
		
			if actual_sat_name in sats_name:
				self.orbitron = 'yes'
			else:
				self.orbitron = 'no'
					
		# File not available
		except IOError:
			self.orbitron = 'no'

	def check_STK(self, index, STK_folder):
		from os import listdir
		
		if index < len(listdir(STK_folder)):
			self.STK = 'yes'
		else:
			self.STK = 'no'
