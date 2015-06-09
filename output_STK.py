

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
        try:
            family.remove('temp.txt')
        except:
            pass
        
        open_names_TLE = open(script_dir + '/results/temp')
        names_TLE = open_names_TLE.readlines()
        names_TLE = [item.rstrip('\n\r') for item in names_TLE]
        names_TLE = [item.strip() for item in names_TLE]

        satellite = names_TLE[index_satellite]        

        try:
            satellite = satellite.replace(satellite[satellite.index('('):(1 + satellite.index(')'))], '')

        except:
            pass
        
        # Rutina para obtener el numero del catalogo del NORAD correspondiente al satelite
        open_NORAD_database = open(script_dir + '/NORAD_Catalog.csv')
        from csv import reader
        NORAD_database = reader(open_NORAD_database)
        
        for row in NORAD_database:
                
            if satellite in row[2]:
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
                names_STK_final.append(int(name_STK_final))

        if number in names_STK_final:
            self.open_file_STK(family[0], names_STK_final.index(number), len(names_STK_final), script_dir)
        
    # Extraer los datos del fichero.
    def open_file_STK(self, family, index, list_length, script_dir):
            
        self.STK_simulation_time = []
        self.STK_alt_satellite = []
        self.STK_az_satellite = []

        # Creo que el indice esta mal, por eso me daba fallos antes.

        i = 0
        gaps = 1

        index_list = []
        index_list.append(1)

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
                if j >= index_list[index]:
                    valor = int((float(row[0]) - 2440587.5)*86400)
                    self.STK_simulation_time.append(valor)
                    self.STK_az_satellite.append((row[1]))
                    self.STK_alt_satellite.append((row[2]))
            except IndexError:
                pass