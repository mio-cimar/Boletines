"""
Description: Programa que hace un gráfico temporal
Usage: python run_points_TS_csv_bulletin.py
Input: datos en formato csv
Output: imagenes en png, tif y jpeg
Author M.Sc. Rodney Eduardo Mora Escalante
Creation day Sep 25,2019
Modificado por Maria Jose Urena Nov 11 2019, se le agrego la escritura de las estadisticas a los csv
"""

import os
import csv 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator, FixedFormatter,FormatStrFormatter
from datetime import datetime, timedelta, date
import math
import matplotlib.dates as mdates
import calendar as c

# Quality Figures
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('axes', labelsize=6)
# Width as measured in inkscape
width =3.487
height = width / 1.618  

fecha = date.today()#fecha actual
año = fecha.year#año actual

EFM= 62 + c.monthrange(año, 2)[1] #cantidad de días del trimestre
AMJ=91 #cantidad de días del trimestre
JAS=92 #cantidad de días del trimestre
OND=92 #cantidad de días del trimestre

horas=8

print("Seleccione el trimestre que desea graficar")
print("1. Enero-Febrero-Marzo")
print("2. Abril-Mayo-Junio")
print("3. Julio-Agosto-Setiembre")
print("4. Octubre-Noviembre-Diciembre")

opcion = input("Opción: ")

if (opcion == str(1)):
    cant_dias = EFM
    etiquetas = ['1','5','10','15\nEnero','20','25','1','5','10','15\nFebrero','20','25','1','5','10','15\nMarzo','20','25','1']
#    mt = [0,4,9,14,19,24,31,35,40,45,50,55,59,63,68,73,78,83,cant_dias] # correcto 
    mt = [0,4,9,14,19,24,31,35,40,45,50,55,60,64,69,74,79,84,cant_dias]   #para año bisiesto
    
if (opcion == str(2)):
    cant_dias = AMJ
    etiquetas = ['1','5','10','15\nAbril','20','25','1','5','10','15\nMayo','20','25','1','5','10','15\nJunio','20','25','1']
    mt = [0,4,9,14,19,24,30,34,39,44,49,54,61,65,70,75,80,85,cant_dias] 

if (opcion == str(3)):
    cant_dias = JAS
    etiquetas = ['1','5','10','15\nJulio','20','25','1','5','10','15\nAgosto','20','25','1','5','10','15\nSeptiembre','20','25','1']
    mt = [0,4,9,14,19,24,31,35,40,45,50,55,62,66,71,76,81,86,cant_dias]


if (opcion == str(4)):
    cant_dias = OND
    etiquetas = ['1','5','10','15\nOctubre','20','25','1','5','10','15\nNoviembre','20','25','1','5','10','15\nDiciembre','20','25','1']
    mt = [0,4,9,14,19,24,31,35,40,45,50,55,61,65,70,75,80,85,cant_dias]
    
mt[:] = [x*horas for x in mt] 
majorLocator = FixedLocator(mt)
minorLocator = MultipleLocator(horas)

tso = list()
s = list()
for i in range(7):
    tso.append([])
    s.append([])
n = 0

# Revisar siempre estas dos variables por si en algún momento en la base de datos lo corrigen...
fac=0.001
add=20
ruta = "/home/miocimar/Desktop/Boletines/Ocean/"

for path, dirs, files in os.walk(''+ruta):
    for file in files:        
        filename = os.path.join(path, file)
        name = filename.rstrip(".csv")
        if ".csv" in file:
            
            rows_data = []
            with open(filename, encoding='latin1') as datos: #Nota: se le debe agregar el encoding para que lea correctamente los carateres
                data_reader = csv.reader(datos, delimiter = ',')
                for row in data_reader:
                    rows_data.append(row)
                    
            LL=len(rows_data)


            row_TI = []
            print(file)  
                                 
            for i in range(1,LL-1):
                row_TI.append(datetime.strptime(rows_data[i][0],'%Y-%m-%dT%H:%M:%SZ')- timedelta(hours=6))
    
    
            row_S = []                            
            for i in range(1,LL-1):
                row_S.append((float(rows_data[i][4])*fac)+add)
                                        
            row_T = []                    
            for i in range(1,LL-1):
                row_T.append((float(rows_data[i][5])*fac)+add)
    
            tso[n].append(rows_data[2][1])
            tso[n].append(rows_data[2][2])          
            tso[n].append(round(max(row_T), 2))
            tso[n].append(round(min(row_T), 2))
            tso[n].append(round(np.nanmean(row_T), 2))
            s[n].append(rows_data[2][1])
            s[n].append(rows_data[2][2])
            s[n].append(round(max(row_S), 2))
            s[n].append(round(min(row_S), 2))
            s[n].append(round(np.nanmean(row_S), 2))
            n+=1     

            
#  Grafico temporal
#                           
                                       
            fig, ax = plt.subplots(figsize=(width, height), facecolor='w', edgecolor='k')   
                 
            graph1, = plt.plot(row_T, c = '#FF0000', label = 'Temperatura', linewidth=1)
            plt.ylim(20,32) 
            #plt.xlabel('Tiempo [Horas]',labelpad=0.5)  # Ponemos etiqueta al eje x 
            #plt.yticks(fontsize=16, fontweight='bold', fontname='Arial') 
            plt.ylabel('Temperatura [$^\circ$C]')  # Ponemos etiqueta al eje y
            #plt.xticks(fontsize=16, fontweight='bold', fontname='Arial') 

           
            ax.tick_params(axis='x', which='major', length =3, width =1, top=False,pad=0.4)
            ax.tick_params(axis='x', which='minor', length =2, width =0.5, top=False)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
            ax.xaxis.set_major_formatter(FixedFormatter(etiquetas))
            #plt.xticks(rotation=45, ha='right')
            plt.twinx()  # Creamos un segundo eje y
            graph2, = plt.plot(row_S, c = '#003300', label = 'Salinidad', linewidth=1)
            plt.ylabel('Salinidad [UPS]')  # Ponemos etiqueta al eje y
            #plt.yticks(fontsize=16, fontweight='bold', fontname='Arial')
            plt.ylim(30,38)
            plt.xlim(0,cant_dias*horas)            
            plt.legend([graph1, graph2], ['T', 'S'], fontsize=6, loc = 1)
            #ax.set_xticks([row_TI[2],row_TI[98],row_TI[210],row_TI[326],row_TI[446],row_TI[574],row_TI[686]])
            #ax.set_xticks([row_TI)
            #ax.set_xticklabels(['','abril','','mayo','','junio',''])
            fig = plt.gcf() # Get reference to current figure
            fig.savefig(name+".png",dpi=300,bbox='tight')
            fig.savefig(name+".tif",dpi=300,bbox='tight')
            plt.show()
            
                   
with open("valores_boletin_TS.csv","a") as f:
    wr = csv.writer(f)
    f.write('Temperatura Potencial [\xb0C] \n') 
    f.write('Latitud, Longitud, Máximo, Mínimo, Promedio \n') 
    wr.writerows(tso)
    f.write('Salinidad [UPS] \n') 
    f.write('Latitud, Longitud, Máximo, Mínimo, Promedio \n') 
    wr.writerows(s)         
