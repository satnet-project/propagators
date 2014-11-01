

################################################################################
# Copyright 2014 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
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

	def __init__(self, index_satellite, sat_selected):
		
		file = '/home/case/Orbitron/Output/output.txt'

		import os.path
		if os.path.exists(file):
			from os import getcwd, chdir
			index_satellite = index_satellite + 1
			directorio_script = os.getcwd()
		
			# Orbitron routine
			self.open_file_orbitron(index_satellite, file, sat_selected)

			os.chdir(directorio_script)

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

		# Si la linea empieza por 2014 se agrega, si no, no.
		if line[0:4] == '2014':
			self.lineas_validas.append(line)


	def process_data(self, sat_selected):

		self.orbitron_time = []
		self.orbitron_az_satellite = []
		self.orbitron_alt_satellite = []

		self.year_list = []
		self.month_list = []
		self.day_list = []
		self.hour_list = []
		self.minute_list = []
		self.second_list = []

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

				self.orbitron_time.append(unix_time)
				self.orbitron_az_satellite.append(az)
				self.orbitron_alt_satellite.append(alt)
				
				self.year_list.append(year)
				self.month_list.append(month)
				self.day_list.append(day)
				self.hour_list.append(hour)
				self.minute_list.append(minute)
				self.second_list.append(second)

	def local_to_unix(self, year, month, day, hour, minute, second):

		from datetime import datetime
		d = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

		unix_time = d.strftime('%s')

		return unix_time


class Read_STK_data:

	def __init__(self, index_satellite, directorio_datos):

		import os

		index_satellite = index_satellite
		directorio_script = os.getcwd()
		
		# STK routine
		self.open_STK(directorio_datos)
		self.open_files_STK(index_satellite)

		os.chdir(directorio_script)

	def open_STK(self, directorio_datos):

		import os

		# PyEphem data
		os.chdir(directorio_datos)

		self.files_STK = os.listdir(os.getcwd())
		self.files_STK.sort()

	def open_files_STK(self, index_satellite):
		self.open_file_STK(self.files_STK[index_satellite])

	def open_file_STK(self, name):
	
		self.STK_simulation_time = []
		self.STK_alt_satellite = []
		self.STK_az_satellite = []
		
		import csv
		print "name"
		print name
		with open(name, 'rb') as open_file:
			reader = csv.reader(open_file)
			for row in reader:
				# Tengo que comprobar si la linea esta vacia
				try:
					valor = int((float(row[0]) - 2440587.5)*86400)
					self.STK_simulation_time.append(valor)
					self.STK_az_satellite.append((row[1]))
					self.STK_alt_satellite.append((row[2]))
				except:
					pass

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
		self.files_pyephem.remove('temp')
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


class Read_predict_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()

		# predict routine
		self.open_predict(directorio_script)
		self.open_files_predict(index_satellite)

		os.chdir(directorio_script)

	def open_predict(self, directorio_script):

		import os

		os.chdir(directorio_script + '/results/predict')

		self.files_predict = os.listdir(os.getcwd())
		self.files_predict.remove('temp')
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
				self.predict_simulation_time.append(line[0])
				self.predict_alt_satellite.append(float(line[1]))
				self.predict_az_satellite.append(float(line[2]))


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
		self.files_pyorbital.remove('temp')
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


class Read_data:

	def __init__(self, index_pyephem, index_predict, index_pyorbital):

		import os

		self.index_pyephem = index_pyephem + 1
		self.index_predict = index_predict + 1
		self.index_pyorbital = index_pyorbital + 1

		self.directorio_script = os.getcwd()
	
	def pyephem_minus_predict(self):

		import os

		# Pyephem routine
		self.open_pyephem()
		self.open_files_pyephem()

		# predict routine
		self.open_predict()
		self.open_files_predict()

		difference_alt = []
		difference_az = []

		for i in range(len(self.predict_simulation_time)):
			resta_alt = float(self.predict_alt_satellite[i]) - float(self.pyephem_alt_satellite[i])
			difference_alt.append(resta_alt)

			resta_az = float(self.predict_az_satellite[i]) - float(self.pyephem_az_satellite[i])
			difference_az.append(resta_az)

		os.chdir(self.directorio_script)

		return (difference_alt, difference_az)

	def pyephem_minus_pyorbital(self):

		# pyorbital routine
		self.open_pyorbital()

	def predict_minus_pyorbital(self):

		print "TO-DO"

	def predict_minus_pyephem(self):

		print "TO-DO"

	def pyorbital_minus_pyephem(self):

		print "TO-DO"

	def pyorbital_minus_predict(self):

		print "TO-DO"

	def open_pyephem(self):

		import os

		# PyEphem data
		os.chdir(self.directorio_script + '/results/PyEphem')

		directorio_actual = os.getcwd()

		self.files_pyephem = os.listdir(directorio_actual)
		self.files_pyephem.remove('temp')
		self.files_pyephem.sort()
	
	def open_files_pyephem(self):

		for i in range(self.index_pyephem):
			self.open_file_pyephem(self.files_pyephem[i])
			self.satellite_name = self.files_pyephem[i]

	def open_predict(self):

		from os import chdir, getcwd, listdir

		# predict data
		chdir(self.directorio_script + '/results/predict')

		actual_dir = getcwd()

		self.files_predict = listdir(actual_dir)
		self.files_predict.remove('temp')
		self.files_predict.sort()
	

	def open_files_predict(self):

		for i in range(self.index_predict):
			self.open_file_predict(self.files_predict[i])

	def open_pyorbital(self):

		from os import chdir, getcwd, listdir

		# pyorbital data
		chdir(self.directorio_script + '/results/PyOrbital')

		actual_dir = getcwd()
		
		self.files_pyorbital = listdir(actual_dir)
		self.files_pyorbital.remove('temp')
		self.files_pyorbital.sort()

		if not self.files_pyorbital:
			print "empty list"
		else:
			self.open_files_pyorbital()

	def open_files_pyorbital(self):

		for i in range(self.index_satellite):
			self.open_file_pyorbital(self.files_pyorbital[i])

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


	def open_file_predict(self, name):

		self.predict_simulation_time = []
		self.predict_alt_satellite = []
		self.predict_az_satellite = []

		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
#			import datetime	
#			date = datetime.datetime.fromtimestamp(int(line[0])).strftime('%Y-%m-%d %H:%M:%S')
				self.predict_simulation_time.append(line[0])
				self.predict_alt_satellite.append(float(line[1]))
				self.predict_az_satellite.append(float(line[2]))

	def open_file_pyorbital(self, name):

		self.pyorbital_simulation_time = []
		self.pyorbital_alt_satellite = []
		self.pyorbital_az_satellite = []

		from csv import reader

		with open(name) as tsv:
			for line in reader(tsv, delimiter = "\t"):
				self.pyorbital_simulation_time.append(line[0])
				self.pyorbital_alt_satellite.append(float(line[1]))
				self.pyorbital_az_satellite.append(float(line[2]))

#		minimo = min(enumerate(self.predict_alt_satellite), key=lambda x: abs(x[1]-0))

class Check_data:

	def __init__(self, index_satellite, sat_name):

		index = index_satellite + 1
		satellite_name = "SAT%s" %(index)

		from os import getcwd, chdir
		self.directorio_actual = getcwd()

		self.check_predict(index_satellite, satellite_name)
		self.check_pyephem(index_satellite, satellite_name)
		self.check_pyorbital(index_satellite, satellite_name)
		self.check_orbitron(index_satellite, sat_name)

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

	def check_orbitron(self, index, actual_sat_name):
		file = '/home/case/Orbitron/Output/output.txt'

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