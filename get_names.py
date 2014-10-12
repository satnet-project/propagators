
class Get_names:
	
	def __init__(self):

		import os
		import sys

		current_dir = os.getcwd()

		os.chdir(current_dir + '/TLEs')

		open_tle = open(sys.argv[1], 'r')
		names_list = open_tle.readlines()
		names_list = [item.rstrip('\n') for item in names_list] 

		os.chdir(current_dir)

		size_list = len(names_list)
		y = size_list/3

		list_numbers = map(self.return_list, range(y))

		satellites_list = []
		i = 0

		for i in range(len(list_numbers)):
			satellites_list.append(names_list[list_numbers[i]])

		self.save_list(satellites_list)

        def return_list(self, x):
                return 3*x

	def save_list(self, list):

		import os
		current_dir = os.getcwd()

		# PyEphem
		os.chdir(current_dir + '/results/PyEphem')

		create_file_pyephem = open('temp', 'w')
		create_file_pyephem.writelines(["%s\n" % item  for item in list])

		# predict
		os.chdir(current_dir + '/results/predict')

		create_file_predict = open('temp', 'w')
		create_file_predict.writelines(["%s\n" % item  for item in list])

		# pyorbital
		os.chdir(current_dir)
		os.chdir(current_dir + '/results/PyOrbital')

		create_file_pyorbital = open('temp', 'w')
		create_file_pyorbital.writelines(["%s\n" % item for item in list])

		# Orbitron
		os.chdir(current_dir)
		os.chdir(current_dir + '/results/Orbitron')
		
		create_file_orbitron = open('temp', 'w')
		create_file_orbitron.writelines(["%s\n" % item for item in list])

		os.chdir(current_dir)

if __name__ == '__main__':
	get_name = Get_names()
