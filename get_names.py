
class Get_names:
	
	def __init__(self):

		import os
		import sys

		directorio_actual = os.getcwd()
		print directorio_actual
		from time import sleep
		sleep(5)

		os.chdir(directorio_actual + '/TLEs')

		print os.getcwd()
		
		sleep(5)

		print sys.argv[1]
		
		sleep(5)

		abrir_tle = open(sys.argv[1], 'r')
		lista_nombres_satelites = abrir_tle.readlines()
		lista_nombres_satelites = [item.rstrip('\n') for item in lista_nombres_satelites] 

		os.chdir(directorio_actual)

		tamano_lista = len(lista_nombres_satelites)
		y = tamano_lista/3

		numeros_lista = map(self.devuelve_lista, range(y))

		lista_satelites = []
		i = 0

		for i in range(len(numeros_lista)):
			lista_satelites.append(lista_nombres_satelites[numeros_lista[i]])


		self.save_list(lista_satelites)

        def devuelve_lista(self, x):
                return 3*x

	def save_list(self, lista):

		import os

		directorio_script = os.getcwd()

		# PyEphem
		os.chdir(directorio_script + '/results/PyEphem')

		create_file_pyephem = open('temp', 'w')
		create_file_pyephem.writelines(["%s\n" % item  for item in lista])

		# predict
		os.chdir(directorio_script)
		os.chdir(directorio_script + '/results/predict')

		create_file_predict = open('temp', 'w')
                create_file_predict.writelines(["%s\n" % item  for item in lista])

		# pyorbital
		os.chdir(directorio_script)
		os.chdir(directorio_script + '/results/pyorbital')

		create_file_pyorbital = open('temp', 'w')
		create_file_pyorbital.writelines(["%s\n" % item for item in lista])

		# Orbitron
#		os.chdir(directorio_script)
#		os.chdir(directorio_script + '/Orbitron/Output')
		
#		create_file_orbitron = open('temp', 'w')
#		create_file_orbitron.writelines(["%s\n" % item for item in lista])

		os.chdir(directorio_script)

if __name__ == '__main__':
	get_name = Get_names()
