"""
****************************************************************
******* Descargar variables de oleaje para los boletines *******
****************************************************************
input: ---
output: Archivos de datos de VaraibelesOleaje para Boletines
Autor: Tec. Andrey Bonilla
NOTA_1: Se deben cambiar UNICAMENTE los valores de las fechas de inicio y fin segun se necesite
NOTA_2: En las fechas de incio y final se sustitullen los ":" (dos puntos) por "%3A" debido al formato del request

"""
import requests

#url base
url_base = "http://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_93.0/";

#rango de fechas de los datos 
time_start = "2019-10-01T06%3A00%3A00Z&"; #fecha inicial 
time_end = "2020-01-01T03%3A00%3A00Z&"; #fecha final 

#parametros fijos del url
url_params = "north=20&west=-100&east=-70&south=0&disableProjSubset=on&horizStride=1&time_start=" + time_start + "time_end=" + time_end + "timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf4"

#cambio en el url base para descargar las variables necesarias
opc = [("ts3z?"), ("uv3z?")]

#variables a descargar(formato necesario para el request)
variables = [("salinity&"),("water_temp&"),("water_u&"),("water_v&")]

#ruta donde se guardaran los archivos
ruta = "/home/miocimar/Desktop/Boletines/Ocean/Datos/"

class Ocean_Var:
    
    def descargar(self, var, url):
        r = requests.get(url, stream = True)
        
        if r.status_code == 200:
            
            print("Descargando datos de: " + var) 
            
            url_content = r.content
            nc_file = open(ruta + var + ".nc4", "wb")
            nc_file.write(url_content)
            nc_file.close()
            
        else:
            print("No se pudo descargar datos de: " + var + ", Error: " + r.text) 

    #genera el URL necesario para descargar los datos de cada variable uniendo las diferentes partes
    def crear_url(self):
        
        for x in opc:
            
            if x == "ts3z?":
                
                for pos in range(0, 2):#primeras 2 variables
                    url = url_base + x + "var=" + variables[pos] + url_params 

                    var = variables[pos].replace("&", "")                  
                    self.descargar(var, url)
                    
            else:
                
                for pos in range(2, 4):#variables restantes
                    url = url_base + x + "var=" + variables[pos] + url_params 
            
                    var = variables[pos].replace("&", "")              
                    self.descargar(var, url)
    
if __name__ == "__main__":
    ocean_var = Ocean_Var()
    ocean_var.crear_url()