from matplotlib.fontconfig_pattern import family_escape
from posix import getcwd
from lib2to3.fixer_util import Number
from docutils.nodes import row


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

		self.orbitron_time = []
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

				self.orbitron_time.append(unix_time)
				self.orbitron_az_satellite.append(az)
				self.orbitron_alt_satellite.append(alt)

	def local_to_unix(self, year, month, day, hour, minute, second):

		from datetime import datetime
		d = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

		unix_time = d.strftime('%s')

		return unix_time

class Read_STK_data:

	def __init__(self, index_satellite, directorio_datos):

		from os import getcwd, chdir

		script_dir = getcwd()
		
		# STK routine
		files = self.open_STK(directorio_datos)
		self.open_files_STK(index_satellite, script_dir, files)

		chdir(script_dir)

	def open_STK(self, directorio_datos):

		from os import listdir
		files = listdir(directorio_datos)

		return files

	def open_files_STK(self, index_satellite, script_dir, files):

		from os import listdir
		family = listdir(script_dir + '/results/STK')
		family.remove('temp.txt')
		
		open_names_TLE = open(script_dir + '/results/temp')
		names_TLE = open_names_TLE.readlines()
		names_TLE = [item.rstrip('\n\r') for item in names_TLE]
		names_TLE = [item.strip() for item in names_TLE]


		
		satellite = names_TLE[index_satellite]		

		print "satellite: %s" %(satellite)

		try:
			satellite = satellite.replace(satellite[satellite.index('('):(1 + satellite.index(')'))], '')

		except:
			pass
		
#		try:
#			satellite = satellite.replace(' ', '_')
#			print "satellite3: %s" %(satellite)
#		
#		except:
#			pass
#				
#		try:
#			satellite = satellite.strip()
#			print "satellite4: %s" %(satellite)
#			
#		except:
#			pass
		
		
		# Rutina para obtener el numero del catalogo del NORAD correspondiente al satelite
		open_NORAD_database = open(script_dir + '/NORAD_Catalog.csv')
		from csv import reader
		NORAD_database = reader(open_NORAD_database)
		
		for row in NORAD_database:
				
			if satellite.lower() in row[2].strip().lower():
				number = row[0]
				# Rutina para autocompletar los numberos.
				if len(number) == 4:
					number = '0' + number
				elif len(number) == 3:
					number = '00' + number
				elif len(number) == 2:
					number = '000' + number
				elif len(number) == 1:
					number = '0000' + number
				else:
					pass
				number = int(number)
				print "number %s" %(number)
			else:
				error = 1
				print "error"

		# Fichero con las simulaciones disponibles		
		open_names_STK = open(script_dir + '/results/STK/temp.txt')
		names_STK = str(open_names_STK.readlines())
		names_STK = names_STK.split()
		
		names_STK_final = []

		for i in range(len(names_STK)):		
			if 'Satellite' in names_STK[i]:
				import string
				name_STK_final = string.replace(names_STK[i], 'Satellite-', '')
				name_STK_final = string.replace(name_STK_final, ',', '')
				name_STK_final = string.replace(name_STK_final, ':', '')
				name_STK_final = string.replace(name_STK_final, "['Place-CUVI-To-", '')
				name_STK_final = name_STK_final[-5:]
				names_STK_final.append(int(name_STK_final))

		if number in names_STK_final:
			self.open_file_STK(family[0], names_STK_final.index(number), len(names_STK_final), script_dir)
		
	# Extraer los datos del fichero.
	def open_file_STK(self, family, index, list_length, script_dir):
			
		self.STK_simulation_time = []
		self.STK_alt_satellite = []
		self.STK_az_satellite = []

		i = 0
		gaps = 1

		index_list = []
		from csv import reader
		open_index = open(script_dir + '/results/STK/' + family)
		read_index = reader(open_index)
		for row in read_index:
			i = i + 1
			try:
				valor = row[0][0]
			except IndexError:
				gaps = gaps + 1
				index_list.append(i + 2)
				pass
		
		j = 0

		open_sims = open(script_dir + '/results/STK/' + family)	
		read_sims = reader(open_sims)
		for row in read_sims:
			j = j + 1
			try:
				if j >= index_list[index] and j < (index_list[index + 1] - 2):
					valor = int((float(row[0]) - 2440587.5)*86400+3600)
					self.STK_simulation_time.append(valor)
					self.STK_az_satellite.append((row[1]))
					self.STK_alt_satellite.append((row[2]))
			except IndexError:
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
		self.files_predict.sort()
	
	def open_files_predict(self, index_satellite):

		for i in range(index_satellite):
			self.open_file_predict(self.files_predict[i])

	def open_file_predict(self, name):

		self.predict_simulation_time = []
		self.predict_alt_satellite = []
		self.predict_az_satellite = []

		import csv
		
		# offset
		# localtime = utc_time + offset
		# offset = local_time - utc_time
		
		import datetime
		
		offset = int(datetime.datetime.now().strftime("%s"))\
		 - int(datetime.datetime.utcnow().strftime("%s"))	

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
				if float(line[1]) >= 0:
					linea0 = float(line[0]) - offset
					self.predict_simulation_time.append(linea0)
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

	def __init__(self, index_pyephem, index_predict, index_pyorbital,\
	index_orbitron, sat_selected, index_STK, STK_dir, orbitron_dir):

		# Orbitron stuff
		self.file = '/home/case/Orbitron/Output/output.txt'
		self.index_orbitron = index_orbitron + 1
		self.sat_selected = sat_selected
		# PyEphem stuff
		self.index_pyephem = index_pyephem
		# predict stuff		
		self.index_predict = index_predict + 1
		# PyOrbital stuff
		self.index_pyorbital = index_pyorbital
		# STK stuff		
		self.index_STK = index_STK
		self.STK_dir = STK_dir
		self.orbitron_dir = orbitron_dir

		from os import getcwd
		self.directorio_script = getcwd()

	def STK_vs_predict(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		files = self.open_STK(self.STK_dir)
		self.open_files_STK(self.index_STK, directorio_script, files)
		chdir(directorio_script)		
		
		# predict routine
		self.open_predict(directorio_script)
		self.open_files_predict()
		
		# Differences
		list_alt = []
		list_az = []

		time_intersected_predict = []
		time_intersected_predict = list(set(self.STK_simulation_time).intersection(self.predict_simulation_time))

		i = 0

		for i in range(len(time_intersected_predict)):

			difference_alt = \
			float(self.predict_alt_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected_predict[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(self.predict_az_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected_predict[i])])

			list_az.append(difference_az)

			i = i + 1

		# Force mean to zero
		m = 0

		import numpy
		alt = numpy.asarray(list_alt)
		az = numpy.asarray(list_az)
		
		# Standard deviation
		std_alt = numpy.sqrt(numpy.mean((alt-m)**2))
		std_az = numpy.sqrt(numpy.mean((az-m)**2))

		chdir(self.directorio_script)

		return std_alt, std_az

	def STK_vs_predict_comp(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		files = self.open_STK(self.STK_dir)
		self.open_files_STK(self.index_STK, directorio_script, files)
		chdir(directorio_script)

		# predict routine
		self.open_predict(directorio_script)
		self.open_files_predict()
		
		# Differences
		list_alt = []
		list_az = []

		time_intersected_predict = []
		time_intersected_predict = list(set(self.STK_simulation_time).intersection(self.predict_simulation_time))

		i = 0

		for i in range(len(time_intersected_predict)):

			difference_alt = \
			float(self.predict_alt_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected_predict[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(self.predict_az_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected_predict[i])])

			list_az.append(difference_az)

			i = i + 1


		chdir(self.directorio_script)

		return time_intersected_predict, list_alt, list_az

	def STK_vs_PyEphem(self):

		from os import chdir
		chdir(self.directorio_script)

		object_pyephem = Read_pyephem_data(self.index_pyephem)

		pyephem_time = object_pyephem.pyephem_simulation_time
		pyephem_time = [int(item) for item in pyephem_time]

		pyephem_alt = object_pyephem.pyephem_alt_satellite
		pyephem_alt = [float(item) for item in pyephem_alt]
		
		pyephem_az = object_pyephem.pyephem_az_satellite
		pyephem_az = [float(item) for item in pyephem_az]

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(self.STK_simulation_time).intersection(pyephem_time))

		i = 0

		for i in range(len(time_intersected)):

			difference_alt = \
			float(pyephem_alt[pyephem_time.index(time_intersected[i])]) - \
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyephem_az[pyephem_time.index(time_intersected[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		# Force mean to zero
		m = 0

		import numpy
		alt = numpy.asarray(list_alt)
		az = numpy.asarray(list_az)
		
		# Standard deviation
		std_alt = numpy.sqrt(numpy.mean((alt-m)**2))
		std_az = numpy.sqrt(numpy.mean((az-m)**2))

		chdir(self.directorio_script)

		return std_alt, std_az

	def STK_vs_PyEphem_comp(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		files = self.open_STK(self.STK_dir)
		self.open_files_STK(self.index_STK, directorio_script, files)
		chdir(directorio_script)

		from os import chdir
		chdir(self.directorio_script)

		object_pyephem = Read_pyephem_data(self.index_pyephem)

		pyephem_time = object_pyephem.pyephem_simulation_time
		pyephem_time = [int(item) for item in pyephem_time]

		pyephem_alt = object_pyephem.pyephem_alt_satellite
		pyephem_alt = [float(item) for item in pyephem_alt]
		
		pyephem_az = object_pyephem.pyephem_az_satellite
		pyephem_az = [float(item) for item in pyephem_az]

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(self.STK_simulation_time).intersection(pyephem_time))

		i = 0

		for i in range(len(time_intersected)):

			difference_alt = \
			float(pyephem_alt[pyephem_time.index(time_intersected[i])]) - \
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyephem_az[pyephem_time.index(time_intersected[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		chdir(self.directorio_script)

		return time_intersected, list_alt, list_az

	# Standard deviations		
	def STK_vs_PyOrbital(self):

		from os import chdir
		chdir(self.directorio_script)

		object_pyorbital = Read_pyorbital_data(self.index_pyorbital)

		pyorbital_time = object_pyorbital.pyorbital_simulation_time
		pyorbital_time = [int(item) for item in pyorbital_time]

		pyorbital_alt = object_pyorbital.pyorbital_alt_satellite
		pyorbital_alt = [float(item) for item in pyorbital_alt]

		
		pyorbital_az = object_pyorbital.pyorbital_az_satellite
		pyorbital_az = [float(item) for item in pyorbital_az]

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(self.STK_simulation_time).intersection(pyorbital_time))

		i = 0

		for i in range(len(time_intersected)):
		
			difference_alt = \
			float(pyorbital_alt[pyorbital_time.index(time_intersected[i])]) -\
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyorbital_az[pyorbital_time.index(time_intersected[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		# Force mean to zero
		m = 0

		import numpy
		alt = numpy.asarray(list_alt)
		az = numpy.asarray(list_az)
		
		# Standard deviation
		std_alt = numpy.sqrt(numpy.mean((alt-m)**2))
		std_az = numpy.sqrt(numpy.mean((az-m)**2))

		chdir(self.directorio_script)

		return std_alt, std_az

	# Altitudes and azimuths
	def STK_vs_PyOrbital_comp(self):

		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		files = self.open_STK(self.STK_dir)
		self.open_files_STK(self.index_STK, directorio_script, files)
		chdir(directorio_script)
		from os import chdir
		chdir(self.directorio_script)

		object_pyorbital = Read_pyorbital_data(self.index_pyorbital)

		pyorbital_time = object_pyorbital.pyorbital_simulation_time
		pyorbital_time = [int(item) for item in pyorbital_time]

		pyorbital_alt = object_pyorbital.pyorbital_alt_satellite
		pyorbital_alt = [float(item) for item in pyorbital_alt]

		
		pyorbital_az = object_pyorbital.pyorbital_az_satellite
		pyorbital_az = [float(item) for item in pyorbital_az]

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(self.STK_simulation_time).intersection(pyorbital_time))

		i = 0

		for i in range(len(time_intersected)):
		
			difference_alt = \
			float(pyorbital_alt[pyorbital_time.index(time_intersected[i])]) -\
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(pyorbital_az[pyorbital_time.index(time_intersected[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

			i = i + 1

		chdir(self.directorio_script)

		return time_intersected, list_alt, list_az

	# Standard deviations		
	def STK_vs_Orbitron(self):

		object_orbitron = Read_orbitron_data(self.index_orbitron, self.sat_selected, self.orbitron_dir)
		orbitron_time = object_orbitron.orbitron_time
		orbitron_time = [int(item) for item in orbitron_time]

		orbitron_alt = object_orbitron.orbitron_alt_satellite
		orbitron_alt = [float(item) for item in orbitron_alt]
		
		orbitron_az = object_orbitron.orbitron_az_satellite
		orbitron_az = [float(item) for item in orbitron_az]

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(self.STK_simulation_time).intersection(orbitron_time))

		for i in range(len(time_intersected)):
		
			difference_alt = \
			float(orbitron_alt[orbitron_time.index(time_intersected[i])]) -\
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(orbitron_az[orbitron_time.index(time_intersected[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

		# Force mean to zero
		m = 0

		import numpy
		alt = numpy.asarray(list_alt)
		az = numpy.asarray(list_az)
		
		# Standard deviation
		std_alt = numpy.sqrt(numpy.mean((alt-m)**2))
		std_az = numpy.sqrt(numpy.mean((az-m)**2))

		return std_alt, std_az

	# Altitudes and azimuths	
	def STK_vs_Orbitron_comp(self):
		
		# STK routine
		from os import getcwd, chdir
		directorio_script = getcwd()		
		# STK routine
		files = self.open_STK(self.STK_dir)
		self.open_files_STK(self.index_STK, directorio_script, files)
		chdir(directorio_script)

		from os import chdir
		chdir(self.directorio_script)

		object_orbitron = Read_orbitron_data(self.index_orbitron, self.sat_selected, self.orbitron_dir)
		orbitron_time = object_orbitron.orbitron_time
		orbitron_time = [int(item) for item in orbitron_time]

		orbitron_alt = object_orbitron.orbitron_alt_satellite
		orbitron_alt = [float(item) for item in orbitron_alt]
		
		orbitron_az = object_orbitron.orbitron_az_satellite
		orbitron_az = [float(item) for item in orbitron_az]

		# Differences
		list_alt = []
		list_az = []

		time_intersected = []
		time_intersected = list(set(self.STK_simulation_time).intersection(orbitron_time))

		for i in range(len(time_intersected)):
		
			difference_alt = \
			float(orbitron_alt[orbitron_time.index(time_intersected[i])]) -\
			float(self.STK_alt_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_alt.append(difference_alt)

			difference_az = \
			float(orbitron_az[orbitron_time.index(time_intersected[i])]) - \
			float(self.STK_az_satellite[self.STK_simulation_time.index(time_intersected[i])])

			list_az.append(difference_az)

		return time_intersected, list_alt, list_az


	# predict data
	def open_predict(self, script_dir):

		from os import chdir, getcwd, listdir
		chdir(script_dir + '/results/predict')

		self.files_predict = listdir(getcwd())
		self.files_predict.sort()
	

	def open_files_predict(self):

		for i in range(self.index_predict):
			self.open_file_predict(self.files_predict[i])

	def open_file_predict(self, name):

		self.predict_simulation_time = []
		self.predict_alt_satellite = []
		self.predict_az_satellite = []

		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
				self.predict_simulation_time.append(int(line[0]))
				self.predict_alt_satellite.append(float(line[1]))
				self.predict_az_satellite.append(float(line[2]))

	def open_STK(self, directorio_datos):

		from os import listdir
		files = listdir(directorio_datos)

		return files

	def open_files_STK(self, index_satellite, script_dir, files):

		from os import listdir
		family = listdir(script_dir + '/results/STK')
		family.remove('temp.txt')
		
		open_names_TLE = open(script_dir + '/results/temp')
		names_TLE = open_names_TLE.readlines()
		names_TLE = [item.rstrip('\n\r') for item in names_TLE]
		names_TLE = [item.strip() for item in names_TLE]

		satellite = names_TLE[index_satellite]		
#		satellite = satellite.replace(satellite[satellite.index('('):(1 + satellite.index(')'))], '')
		satellite = satellite.strip()
			
		# Rutina para obtener el numero del catalogo del NORAD correspondiente al satelite
		open_NORAD_database = open(script_dir + '/NORAD_Catalog.csv')
		from csv import reader
		NORAD_database = reader(open_NORAD_database)
		
		for row in NORAD_database:
			
			if satellite.lower() in row[2].strip().lower():
				number = row[0]
				# Rutina para autocompletar los numberos.
				if len(number) == 4:
					number = '0' + number
				elif len(number) == 3:
					number = '00' + number
				elif len(number) == 2:
					number = '000' + number
				elif len(number) == 1:
					number = '0000' + number
				else:
					pass
			else:
				error = 1

		# Fichero con las simulaciones disponibles		
		open_names_STK = open(script_dir + '/results/STK/temp.txt')
		names_STK = str(open_names_STK.readlines())
		names_STK = names_STK.split()

		names_STK_final = []

		for i in range(len(names_STK)):		
			if 'Satellite' in names_STK[i]:
				import string
				name_STK_final = string.replace(names_STK[i], 'Satellite-', '')
				name_STK_final = string.replace(name_STK_final, ',', '')
				name_STK_final = string.replace(name_STK_final, ':', '')
				name_STK_final = string.replace(name_STK_final, "['Place-CUVI-To-", '')
				name_STK_final = name_STK_final[-5:]
				names_STK_final.append(name_STK_final)


		if number in names_STK_final:
			self.open_file_STK(family[0], names_STK_final.index(number), len(names_STK_final), script_dir)

#		if names_STK_final.index(number):
#			self.open_file_STK(family[0], names_STK_final.index(number), len(names_STK_final), script_dir)
		
	# Extraer los datos del fichero.
	def open_file_STK(self, family, index, list_length, script_dir):
			
		self.STK_simulation_time = []
		self.STK_alt_satellite = []
		self.STK_az_satellite = []

		i = 0
		gaps = 1

		index_list = []
		from csv import reader
		open_index = open(script_dir + '/results/STK/' + family)
		read_index = reader(open_index)
		for row in read_index:
			i = i + 1
			try:
				valor = row[0][0]
			except IndexError:
				gaps = gaps + 1
				index_list.append(i + 2)
				pass
		
		j = 0

		open_sims = open(script_dir + '/results/STK/' + family)	
		read_sims = reader(open_sims)
		for row in read_sims:
			j = j + 1
			try:
				if j >= index_list[index] and j < (index_list[index + 1] - 2):
					valor = int((float(row[0]) - 2440587.5)*86400)
					self.STK_simulation_time.append(valor)
					self.STK_az_satellite.append((row[1]))
					self.STK_alt_satellite.append((row[2]))
			except IndexError:
				pass
			print STK_simulation_time[0]
			


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
