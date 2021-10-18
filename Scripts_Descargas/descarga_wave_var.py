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
url_base = "https://pae-paha.pacioos.hawaii.edu/thredds/ncss/ww3_global/WaveWatch_III_Global_Wave_Model_best.ncd?";

#rango de fechas de los datos 
time_start = "2019-10-01T06%3A00%3A00Z&"; #fecha inicial 
time_end = "2020-01-01T05%3A00%3A00Z&"; #fecha final 

#parametros fijos del url
url_params = "north=20&west=-100&east=-70&south=0&disableProjSubset=on&horizStride=1&time_start=" + time_start + "time_end=" + time_end + "timeStride=1&vertCoord=0"

#variables a descargar(formato necesario para el request)
variables = [("Tdir&"),("Tper&"),("Thgt&")]

#nombre abreviado de las variables para guardar los archivos descargados
var = [("dp"),("tp"),("hs")]

#ruta donde se guardaran los archivos
ruta = "/home/miocimar/Desktop/Boletines/Wave/Datos/"

#diccionario para automatizar la generacion de los nombres de los archivos
meses = {"01":"ene", "02":"feb", "03":"mar", "04":"abr", "05":"may", "06":"jun",
         "07":"jul", "08":"ago", "09":"set", "10":"oct", "11":"nov", "12":"dic",}

class Wave_Var:
    
    def generar_nombre(self, var):
        
        parts_start = time_start.split('-')
        parts_end = time_end.split('-')
        
        if parts_end[1] == "01":
            mes_end = "12"
        else:
            mes_end = "0" + str(int(parts_end[1])-1)             
                
        if parts_start[1] in meses and mes_end in meses:
            return var + "_" + meses[parts_start[1]] + "-" + meses[mes_end] + "_" + parts_start[0] + ".nc"
                
    
    def descargar(self):
        
        for pos in range(0, len(variables)):
            url = url_base + "var=" + variables[pos] + url_params 
            
            r = requests.get(url, stream = True)
            
            if r.status_code == 200:
                nom_file = self.generar_nombre(var[pos])
                
                print ("Descargando datos de: " + nom_file)
                
                url_content = r.content
                nc_file = open(ruta + nom_file, "wb")
                nc_file.write(url_content)
                nc_file.close()
                
            else:
                print("No se pudo descargar datos de: " + variables[pos] + ", Error: " + r.text) 
    
if __name__ == "__main__":
    wave_var = Wave_Var()
    wave_var.descargar()