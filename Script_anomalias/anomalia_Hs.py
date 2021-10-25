"""
Description: Programa que hace un gráfico de anomalia de altura del pico de la ola y periodo
Usage: python anomalia_Hs.py
Input: datos en formato csv
Output: imagenes en png, tif
Author María José Ureña Flores 
Creation day Oct, 22,2021
"""

import os
import csv 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator, FixedFormatter,FormatStrFormatter
from datetime import datetime, timedelta, date
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

hs = list()
tp = list()

for i in range(7):
	hs.append([])
	tp.append([])

n = 0

#ruta = "/Users/maria/Downloads/anomalia/"
ruta = "/home/miocimar/Desktop/WAVES-MIO/Maria/anomalia/Hs_Tp/"

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
            
            print("-------------------------------------") 
            print(file)

                                 
            for i in range(1,LL-1):
                row_TI.append(datetime.strptime(rows_data[i][0],'%Y-%m-%dT%H:%M:%SZ')- timedelta(hours=6)) 
            
            row_tp = []                            
            for i in range(2,LL-1):
                row_tp.append(float(rows_data[i][5]))
                                        
            row_hs = []                    
            for i in range(2,LL-1):
                row_hs.append(float(rows_data[i][4]))

            #promedio
            tp_mean = np.mean(row_tp)
            hs_mean = np.mean(row_hs)

#GRAFICO DE ANOMALIA DE Hs

            for x in row_hs:
                anomalia_hs = row_hs-hs_mean
            
            fig1, ax = plt.subplots(figsize=(width, height), facecolor='w', edgecolor='k')   
            graph1, = plt.plot(row_hs, c = '#0a1d7c', label = 'Altura significativa', linewidth=1)
            plt.ylabel('Altura significativa Hs [m]')  # Ponemos etiqueta al eje y
            ax.tick_params(axis='x', which='major', length =3, width =1, top=False,pad=0.4)
            ax.tick_params(axis='x', which='minor', length =2, width =0.5, top=False)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
            ax.xaxis.set_major_formatter(FixedFormatter(etiquetas))
            plt.xlim(0,cant_dias*horas)  
            fig1 = plt.gcf() # Get reference to current figure
            fig1.savefig(name+"anomalia_Hs.png",dpi=300,bbox='tight')
            fig1.savefig(name+"anomalia_Hs.tif",dpi=300,bbox='tight')
            plt.show()
            
            
#GRAFICO DE ANOMALIA DE Tp
            for x in row_tp:
                anomalia_tp = row_tp-tp_mean
                
            fig2, ax = plt.subplots(figsize=(width, height), facecolor='w', edgecolor='k')   
            graph2, = plt.plot(row_tp, c = '#05aeb2', label = 'Periodo', linewidth=1)
            plt.ylabel('Periodo Tp [s]')  # Ponemos etiqueta al eje y
            ax.tick_params(axis='x', which='major', length =3, width =1, top=False,pad=0.4)
            ax.tick_params(axis='x', which='minor', length =2, width =0.5, top=False)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
            ax.xaxis.set_major_formatter(FixedFormatter(etiquetas))
            plt.xlim(0,cant_dias*horas)  
            fig2 = plt.gcf() # Get reference to current figure
            fig2.savefig(name+"anomalia_Tp.png",dpi=300,bbox='tight')
            fig2.savefig(name+"anomalia_Tp.tif",dpi=300,bbox='tight')
            plt.show()
            
            