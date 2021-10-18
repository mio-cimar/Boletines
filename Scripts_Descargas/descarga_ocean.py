"""
************************************************************
******* Descargar datos de puntos para los boletines *******
************************************************************
input: ---
output: Archivos de datos de Puntos para Boletines
Autor: Tec. Andrey Bonilla
NOTA_1: Se deben cambiar UNICAMENTE los valores de las fechas de inicio y fin segun se necesite
NOTA_2: En las fechas de incio y final se sustitullen los ":" (dos puntos) por "%3A" debido al formato del request

"""
import requests

#url base
url = "http://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_93.0/ts3z?var=salinity&var=water_temp&";

#rango de fechas de los datos 
time_start = "2019-10-01T06%3A00%3A00Z&"; #fecha inicial 
time_end = "2020-01-01T05%3A00%3A00Z&"; #fecha final 

#urls para cada uno de los puntos
urls = [(url + "latitude=10&longitude=277&time_start=" + time_start +"time_end=" + time_end + "vertCoord=0&accept=csv_file"),
(url + "latitude=9&longitude=275.5&time_start=" + time_start +"&time_end=" + time_end + "vertCoord=0&accept=csv_file"),
(url + "latitude=9.5&longitude=274.5&time_start=" + time_start + "&time_end=" + time_end + "vertCoord=0&accept=csv_file"),
(url + "latitude=11&longitude=274&time_start=" + time_start + "&time_end=" + time_end + "vertCoord=0&accept=csv_file"),
(url + "latitude=5.5&longitude=273&time_start=" + time_start + "&time_end=" + time_end + "vertCoord=0&accept=csv_file"),
(url + "latitude=8&longitude=276.5&time_start=" + time_start + "&time_end=" + time_end + "vertCoord=0&accept=csv_file"),
(url + "latitude=10.5&longitude=274&time_start=" + time_start + "&time_end=" + time_end + "vertCoord=0&accept=csv_file")]

#siglas de los puntos a descargar
puntos = [("CA"),("PC"),("PNS"),("PNN"),("IC"),("PS"),("PNC")]

#ruta donde se guardaran los archivos
ruta = "/home/miocimar/Desktop/Boletines/Ocean/"

class Ocean:
        
    def descarga(self):
        
         for pos in range(0, len(urls)):

            r = requests.get(urls[pos], stream = True)
            
            if r.status_code == 200:
                
                print ("Descargando datos de: " + puntos[pos] + "_T-S")
                url_content = r.content
                csv_file = open(ruta + puntos[pos] + "_T-S.csv", "wb")
                csv_file.write(url_content)
                csv_file.close()
    
            else:
                print("No se pudo descargar datos de: " + puntos[pos] + ", Error: " + r.text)

if __name__ == "__main__":
    ocean = Ocean()
    ocean.descarga()