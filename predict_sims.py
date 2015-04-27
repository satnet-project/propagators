
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


class Do_list:

    def __init__(self):

        from sys import argv
        from os import getcwd

        open_tle = open(getcwd() + '/TLEs/' + argv[1], 'r')
        satellite_list = open_tle.readlines()
        satellite_list = [item.rstrip('\n') for item in satellite_list]

        length_list = len(satellite_list)
        y = length_list/3

        list_numbers = map(self.return_list, range(y))
        
        self.show_satellite_list = []
        self.tle_first_line_list = []
        self.tle_second_line_list = []
        
        i = 0
        j = 1
        k = 2

        for i in range(len(list_numbers)):
            self.show_satellite_list.append(satellite_list[list_numbers[i]])
            self.tle_first_line_list.append(satellite_list[j])
            self.tle_second_line_list.append(satellite_list[k])
            
            j = list_numbers[i] + 4
            k = list_numbers[i] + 5                
            
        # Funcion para sacar los valores de la clase
        self.return_values()

    def return_list(self, x):
        return 3*x

    def return_values(self):
        return self.show_satellite_list
        return self.tle_first_line_list
        return self.tle_second_line_list

class Solve_coordinates:

    def __init__(self, lista_elementos, lista_prueba, lista_prueba2):

        self.satellites_number = len(lista_elementos)
        
        # Provide data to pyephem_routine
        for i in range(len(lista_elementos)):
            i = i + 1
            
            # Create new threads
            thread1 = myThread(1, "Thread-1", 1)
            thread1.start()
            thread2 = myThread(2, "Thread-2", 2)
            thread2.start()


class myThread (threading.Thread):
    
    def __init__(self, file, satellite, begin_time, output_file):
        import threading
        import time
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        import subprocess
        args = ("predict", "-t", file, "-f", satellite, begin_time, "-o", output_file)
        compute = subprocess.call(args)
        
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name
        
        if flag_finish == 0:
            thread.exit()
        

if __name__ == '__main__':
    print ""
    print "PyOrbital data"
    do_list = Do_list()

    solve_coordinates = Solve_coordinates(do_list.mostrar_lista_satelites, do_list.mostrar_lista_linea1, do_list.mostrar_lista_linea2)