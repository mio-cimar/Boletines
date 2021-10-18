"""
Description: Programa que hace un gráfico 
Usage: python run_points_HsTp_csv_bulletin.py
Input: datos en formato csv
Output: imagenes en png, tif y jpeg
Author Estudiante Alejandro Rodriguez y M.Sc. Rodney Eduardo Mora Escalante
Creation day  Fri Apr 20 16:32:25 2018
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
width = 3.487
height = width / 1.618

fecha = date.today()#fecha actual
año = fecha.year#año actual

#cantidad de días del trimestre
EFM= 62 + c.monthrange(año, 2)[1] #obtiene la cantidad de días de febrero
AMJ=91 #cantidad de días del trimestre
JAS=92 #cantidad de días del trimestre
OND=92 #cantidad de días del trimestre

horas=24

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

hs = list()
tp = list()

for i in range(7):
	hs.append([])
	tp.append([])

n = 0
 
ruta = "/home/miocimar/Desktop/Boletines/Wave/"

for path,dirs,files in os.walk(''+ruta):
    for file in files:        
        filename = os.path.join(path, file)
        name = filename.rstrip(".csv")
        
        if ".csv" in file:
            
            rows_data = []
            with open(filename) as datos:
                data_reader = csv.reader(datos, delimiter = ',')
                for row in data_reader:
                    rows_data.append(row)
                    
            LL=len(rows_data)

            row_TI = []  
            print(file)                     
            for i in range(2,LL-1):
               
                row_TI.append(datetime.strptime(rows_data[i][0],'%Y-%m-%dT%H:%M:%SZ')- timedelta(hours=6))
        
            row_tp = []                            
            for i in range(2,LL-1):
                row_tp.append(float(rows_data[i][5]))
                                        
            row_hs = []                    
            for i in range(2,LL-1):
                row_hs.append(float(rows_data[i][4]))

            hs[n].append(rows_data[2][2])
            hs[n].append(rows_data[2][3])            
            hs[n].append(round(max(row_hs), 2))
            hs[n].append(round(min(row_hs), 2))
            hs[n].append(round(np.nanmean(row_hs), 2))
            tp[n].append(rows_data[2][2])
            tp[n].append(rows_data[2][3])  
            tp[n].append(round(max(row_tp), 2))
            tp[n].append(round(min(row_tp), 2))
            tp[n].append(round(np.nanmean(row_tp), 2))
            n+=1      
#  Grafico temporal
                                                              
            fig, ax = plt.subplots(figsize=(width, height), facecolor='w', edgecolor='k')   
                 
            graph1, = plt.plot(row_hs, c = '#0a1d7c', label = 'Altura significativa', linewidth=1)
            plt.ylim(0,4) 
          
            #plt.xlabel('Tiempo [Horas]',labelpad=0.5)  # Ponemos etiqueta al eje x 
            #plt.yticks(fontsize=16, fontweight='bold', fontname='Arial') 
            plt.ylabel('Altura significativa Hs [m]')  # Ponemos etiqueta al eje y
            #plt.xticks(fontsize=16, fontweight='bold', fontname='Arial') 
           
            ax.tick_params(axis='x', which='major', length =3, width =1, top=False,pad=0.4)
            ax.tick_params(axis='x', which='minor', length =2, width =0.5, top=False)
          
#            ax.tick_params(axis='x', which='major', length =10, width =2, top=False,pad=0.4)
#            ax.tick_params(axis='x', which='minor', length =5, width =1, top=False)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
            ax.xaxis.set_major_formatter(FixedFormatter(etiquetas))
            #plt.xticks(rotation=45, ha='right')
            plt.twinx()  # Creamos un segundo eje y
            graph2, = plt.plot(row_tp, c = '#05aeb2', label = 'Periodo', linewidth=1)
            plt.ylabel('Periodo Tp [s]')  # Ponemos etiqueta al eje y
            #plt.yticks(fontsize=16, fontweight='bold', fontname='Arial')
           
            plt.ylim(0,25)
            plt.xlim(0,cant_dias*horas)   #Para 91 dias 2185 para 92 días modificar a 2209         
            plt.legend([graph1, graph2], ['Hs', 'Tp'], fontsize=6, loc = 1)
            #ax.set_xticks([row_TI[2],row_TI[98],row_TI[210],row_TI[326],row_TI[446],row_TI[574],row_TI[686]])
            #ax.set_xticks([row_TI)
            #ax.set_xticklabels(['','abril','','mayo','','junio',''])
            fig = plt.gcf() # Get reference to current figure
            fig.savefig(name+".png",dpi=300,bbox='tight')
            fig.savefig(name+".tif",dpi=300,bbox='tight')
            plt.show()
            
with open("valores_boletin_HsTp.csv","w") as f:
    wr = csv.writer(f)
    f.write('Altura significativa Hs [m] \n') 
    f.write('Latitud, Longitud, Máximo, Mínimo, Promedio \n') 
    wr.writerows(hs)
    f.write('Período Tp [s] \n') 
    f.write('Latitud, Longitud, Máximo, Mínimo, Promedio \n') 
    wr.writerows(tp)