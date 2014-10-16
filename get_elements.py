class Get_elements:

	def __init__(self, file, index):
	
		self.index = index + 1
		
		file = str(file)

		import os

		directorio_actual = os.getcwd()
		os.chdir(directorio_actual + '/TLEs')

                abrir_tle = open(file, 'r')
                lista_nombres_satelites = abrir_tle.readlines()
                lista_nombres_satelites = [item.rstrip('\n') for item in lista_nombres_satelites]


		os.chdir(directorio_actual)

                tamano_lista = len(lista_nombres_satelites)
                y = tamano_lista/3

                numeros_lista = map(self.devuelve_lista, range(y))

                lista_satelites = []
		lista_linea1 = []
		lista_linea2 = []
                i = 0
                j = 1
                k = 2

                for i in range(len(numeros_lista)):
                        lista_satelites.append(lista_nombres_satelites[numeros_lista[i]])
                        lista_linea1.append(lista_nombres_satelites[j])
                        lista_linea2.append(lista_nombres_satelites[k])
                        j = numeros_lista[i] + 4
                        k = numeros_lista[i] + 5


		self.solve_coordinates(lista_satelites, lista_linea1, lista_linea2)

        def devuelve_lista(self, x):
                return 3*x

	def solve_coordinates(self, satellites, lines1, lines2):

		import ephem

                self.observer = ephem.Observer()
                self.get_location()

                self.observer.lon = ephem.degrees(self.lon)
                self.observer.lat = ephem.degrees(self.lat)
                self.observer.elevation = self.ele

                self.observer.date = ephem.now()
                self.observer.epoch = ephem.now()
		
                for i in range(self.index):
                        self.pyephem_routine(satellites[i], lines1[i], lines2[i])


	def pyephem_routine(self, name, line1, line2):
		import ephem
		satellite = ephem.readtle(name, line1, line2)
		satellite.compute(self.observer)

		# Inclinacion en grados.
		self.inclination = satellite._inc
		import math 
		self.inclination = math.degrees(self.inclination)
		self.mean_motion = satellite._n
		self.epoch = satellite._epoch

	# No es relevante. Comprobar.
        def get_location(self):
                self.lon = '-2.314722'
                self.lat = '36.832778'
                self.ele = 20


class Get_name:

	def __init__(self, index):

		from os import getcwd, chdir
		actual_dir = getcwd()

		chdir(actual_dir + '/results/predict')

		open_temp = open('temp', 'r')
		names_list = open_temp.readlines()
		names_list = [item.rstrip('\n') for item in names_list]
		names_list = [item.rstrip('\r') for item in names_list]
		names_list = [item.strip() for item in names_list]

		self.name = names_list[index]

		chdir(actual_dir)


class Get_names:

	def __init__(self):

		from os import getcwd, chdir
		actual_dir = getcwd()

		chdir(actual_dir + '/results/predict')

		open_temp = open('temp', 'r')
		names_list = open_temp.readlines()
		names_list = [item.rstrip('\n') for item in names_list]
		names_list = [item.rstrip('\r') for item in names_list]
		names_list = [item.strip() for item in names_list]

		self.names_list = names_list

		chdir(actual_dir)

class Get_list_length:

	def __init__(self):
		
		from os import getcwd, chdir
		
		actual_dir = getcwd()
		chdir(actual_dir + '/results/predict')

		open_temp = open('temp', 'r')
		names_list = open_temp.readlines()

		chdir(actual_dir)

		self.length = len(names_list)

