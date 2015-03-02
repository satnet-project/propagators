

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
		os.chdir(current_dir + '/results')

		create_file_pyephem = open('temp', 'w')
		create_file_pyephem.writelines(["%s\n" % item  for item in list])

		os.chdir(current_dir)

if __name__ == '__main__':
	get_name = Get_names()
