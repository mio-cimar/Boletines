"""
Description: Programa que hace un mapa de corrientes, temperatura y salinidad
Input: datos en formato netCDF
Output: imagenes en png, tif y jpeg
Author M.Sc. Rodney Eduardo Mora Escalante
Creation day Aug 6, 2019
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import netCDF4
import os 

os.environ ['PROJ_LIB'] = '/home/miocimar/anaconda2/share/proj/'

#rutas utilizadas
ruta_img = '/home/miocimar/Desktop/Boletines/Ocean/Mapas/'
ruta = '/home/miocimar/Desktop/Boletines/Ocean/Datos/'

#Opciones para los nombres de los mapas generados
print("Seleccione el trimestre que desea graficar")
print("1. Enero-Febrero-Marzo")
print("2. Abril-Mayo-Junio")
print("3. Julio-Agosto-Setiembre")
print("4. Octubre-Noviembre-Diciembre")

opcion = input("Opcion: ")

if opcion == "1":
    trimestre = "_ene-mar_"
elif opcion == "2":
    trimestre = "_abr-jun_"
elif opcion == "3":
    trimestre = "_jul-set_"
elif opcion == "4":
    trimestre = "_oct-dic_"

print("\nSeleccione el anno de los datos que desea graficar")
print("1. Anno Actual")
print("2. Anno Anterior")
print("3. Otro")

opc = input("Opcion: ")

if opc == "1":
    anno = dt.datetime.now()
    anno = anno.year
elif opc == "2":
    anno = dt.datetime.now()
    anno = anno - dt.timedelta(days=365)
    anno = anno.year
elif opc == "3":
    anno = input("Digite el anno: ")

#Extrae los datos del archivo netCDF
file1 = netCDF4.Dataset(ruta + 'water_temp.nc4','r')
file2 = netCDF4.Dataset(ruta + 'salinity.nc4','r')

file3a = netCDF4.Dataset(ruta + 'water_u.nc4','r')
file3b = netCDF4.Dataset(ruta + 'water_v.nc4','r')

LAT  = file1.variables['lat'][:]
LON  = file1.variables['lon'][:]-360
TI= file1.variables['time'][:]
TEMP = file1.variables['water_temp'][:,0,:,:]
SAL = file2.variables['salinity'][:,0,:,:]

U = file3a.variables['water_u'][:,0,:,:]
V = file3b.variables['water_v'][:,0,:,:]

# Cerrar el archivo
for file in range(1,4):
    "file"+ str(file) +".close()"
    if file == 3:
        "file"+ str(file) +"a.close()"
        "file"+ str(file) +"b.close()"   

# Promedios de los campos
TEMPm=np.nanmean(TEMP,axis=0)        
SALm=np.nanmean(SAL,axis=0)       
Um=np.nanmean(U,axis=0)        
Vm=np.nanmean(V,axis=0)         

#Variables globales para todos los mapas
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('axes', labelsize=6)

#Width as measured in inkscape
width = 3.487
height = width / 1.618
 
#***************************** Mapa de Temperatura *****************************       
print('\nCreando mapas de Temperatura')
plt.figure(figsize=(width, height), facecolor='w', edgecolor='k')

mapa=Basemap(projection='merc',llcrnrlon=LON.min(), \
             urcrnrlon=LON.max(),llcrnrlat=LAT.min(),urcrnrlat=LAT.max(),resolution='h')
x, y = mapa(*np.meshgrid(LON,LAT))

mapa.drawcoastlines(linewidth=0.6)
mapa.drawcountries()
mapa.drawmapboundary()
mapa.fillcontinents()
mapa.drawparallels(np.arange(0.,21.,2.5),labels=[1,0,0,0], linewidth=0.0,fontsize=6)
mapa.drawmeridians(np.arange(-100.,-69.,5.),labels=[0,0,0,1], linewidth=0.0,fontsize=6)

CS1=mapa.pcolormesh(x, y, TEMPm, vmin=20, vmax=32, shading='flat', cmap=plt.cm.get_cmap('jet', 60))
cbar = mapa.colorbar(CS1,location='right',pad="2%")
cbar.set_label('[C]',rotation=0,labelpad=7)

mapa.drawmapscale(-97, 2., -87., 3, 500, barstyle='fancy',fontsize=6)

plt.xlabel('Longitud', labelpad=10)
plt.ylabel('Latitud', labelpad=20)

plt.savefig(ruta_img + 'Temperatura' + trimestre + str(anno) + '.png', dpi=300)
plt.savefig(ruta_img + 'Temperatura' + trimestre + str(anno) + '.tif', dpi=300)
plt.close()

#***************************** Mapa de Salinidad *****************************
print('Creando mapas de Salinidad')
plt.figure(figsize=(width, height), facecolor='w', edgecolor='k')

mapa=Basemap(projection='merc',llcrnrlon=LON.min(), \
		urcrnrlon=LON.max(),llcrnrlat=LAT.min(),urcrnrlat=LAT.max(),resolution='h')
x, y = mapa(*np.meshgrid(LON,LAT))

CS1=mapa.pcolormesh(x,y,SALm,vmin=32, vmax=38, shading='flat', cmap=plt.cm.get_cmap('GnBu_r',60))
cbar = mapa.colorbar(CS1,location='right',pad="2%")
cbar.set_label('[ups]',rotation=0,labelpad=7)

mapa.drawcoastlines(linewidth=0.6)
mapa.drawcountries()
mapa.drawmapboundary()
mapa.fillcontinents()
mapa.drawparallels(np.arange(0.,21.,2.5),labels=[1,0,0,0], linewidth=0.0,fontsize=6)
mapa.drawmeridians(np.arange(-100.,-69.,5.),labels=[0,0,0,1], linewidth=0.0,fontsize=6)
mapa.drawmapscale(-97, 2., -87., 3, 500, barstyle='fancy',fontsize=6)

plt.xlabel('Longitud', labelpad=10)
plt.ylabel('Latitud', labelpad=20)

plt.savefig(ruta_img + 'Salinidad' + trimestre + str(anno) + '.png', dpi=300)
plt.savefig(ruta_img + 'Salinidad' + trimestre + str(anno) + '.tif', dpi=300)
plt.close()

#***************************** Mapa de Corrientes *****************************
print('Creando mapas de Corrientes')
plt.figure(figsize=(width, height), dpi=300, facecolor='w', edgecolor='k')

mapa=Basemap(projection='merc',llcrnrlon=LON.min(), \
		urcrnrlon=LON.max(),llcrnrlat=LAT.min(),urcrnrlat=LAT.max(),resolution='h')
x, y = mapa(*np.meshgrid(LON,LAT))

CS1=mapa.pcolormesh(x,y,np.sqrt((Um**2)+(Vm**2)),vmin=0,vmax=1.2, shading='flat', cmap=plt.cm.get_cmap('viridis',24))
cbar = mapa.colorbar(CS1, location='right',pad="2%")
cbar.set_label('[m/s]',rotation=0,labelpad=7)

mapa.drawcoastlines(linewidth=0.6)
mapa.drawcountries()
mapa.drawmapboundary()
mapa.fillcontinents()
mapa.drawparallels(np.arange(0.,21.,2.5),labels=[1,0,0,0], linewidth=0.0,fontsize=6)
mapa.drawmeridians(np.arange(-100.,-69.,5.),labels=[0,0,0,1], linewidth=0.0,fontsize=6)
mapa.drawmapscale(-97, 2., -87., 3, 500, barstyle='fancy',fontsize=6)

U_norm = Um / np.sqrt(Um ** 2.0 + Vm ** 2.0)
V_norm = Vm / np.sqrt(Um ** 2.0 + Vm ** 2.0)   
Q=mapa.quiver(x[::12, ::12],y[::12, ::12],U_norm[::12, ::12],V_norm[::12, ::12],edgecolor='k', facecolor='k',scale=None)

plt.xlabel('Longitud', labelpad=10)
plt.ylabel('Latitud', labelpad=20)

plt.savefig(ruta_img + 'Corrientes' + trimestre + str(anno) + '.png', dpi=300)
plt.savefig(ruta_img + 'Corrientes' + trimestre + str(anno) + '.tif', dpi=300)
plt.close()