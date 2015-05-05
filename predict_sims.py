
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


# argv[1] = family

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
        
        begin_time1 = 5
        begin_time2 = 10
        output_file1 = "ficherosalida1"
        output_file2 = "ficherodesalida2"
        
        # Provide data to pyephem_routine
        for i in range(len(lista_elementos)):
            i = i + 2
            
            # Create new threads
            import threading
            from sys import argv
            myThread = threading.Thread()
            thread1 = myThread(argv[1], lista_elementos[i], begin_time1, output_file1)
            thread2 = myThread(argv[1], lista_elementos[i + 1], begin_time2, output_file2)
            
            thread1.start()
            thread2.start()


class myThread:
    
    def __init__(self, file, satellite, begin_time, output_file):
 
        import threading
        import time
        threading.Thread.__init__(self)
 
        
        self.run(file, satellite, begin_time, output_file)
        
        
    def run(self, file, satellite, begin_time, output_file):

        print "file name is: %s" %(file)
        print "satellite name is: %s" %(satellite)
        print "begin time is: %d" %(begin_time)
        print "output file is: %s" %(output_file)



#        import subprocess
#        args = ("predict", "-t", file, "-f", satellite, begin_time, "-o", output_file)
#        compute = subprocess.call(args)
#        
#        print "Starting " + self.name
#        print_time(self.name, self.counter, 5)
#        print "Exiting " + self.name
#        
#        if flag_finish == 0:
#            thread.exit()
        

if __name__ == '__main__':

    print ""
    print "Predict data -test-"
    do_list = Do_list()

    solve_coordinates = Solve_coordinates(do_list.show_satellite_list, do_list.tle_first_line_list, do_list.tle_second_line_list)