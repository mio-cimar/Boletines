"""
Description: Programa que hace un mapa del Campo de Oleaje
Input: datos en formato netCDF
Output: imagenes en png, tif y jpeg
Author M.Sc. Rodney Eduardo Mora Escalante
Creation day Aug 6,2019
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import netCDF4
import glob

# Extrae los datos del archivo netCDF
count=0
TU=[]
TV=[]

path = "/home/miocimar/Desktop/Boletines/Wind/Datos/*.nc"
ruta = "/home/miocimar/Desktop/Boletines/Wind/Mapas/"

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
for filename in glob.glob(path):
    file = netCDF4.Dataset(filename,'r')

    count+=1
    LAT  = file.variables['lat_0'][:]
    LON  = file.variables['lon_0'][:]-360

    U = file.variables['UGRD_P0_L103_GLL0'][0,:,:]
    V = file.variables['VGRD_P0_L103_GLL0'][0,:,:]
    
    file.close()
    
    TU.append(U)
    TV.append(V)
    
# Promedios de los campos
Um=np.nanmean(TU,axis=0)        
Vm=np.nanmean(TV,axis=0)   
  
#Variables globales para todos los mapas
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('axes', labelsize=6)

# Width as measured in inkscape
width = 3.487
height = width / 1
#1.618  
   
#***************************** Mapa de Viento ***************************** 
print("\nCreando mapas de Viento")
plt.figure(figsize=(width, height), facecolor='w', edgecolor='k')
mapa=Basemap(projection='merc',llcrnrlon=LON.min(), \
		urcrnrlon=LON.max(),llcrnrlat=LAT.min(),urcrnrlat=LAT.max(),resolution='h')

x, y = mapa(*np.meshgrid(LON,LAT))
clevs = np.arange(0, 21, 1)

CS1=mapa.pcolormesh(x,y,np.sqrt((Um**2)+(Vm**2)),vmin=0,vmax=20, shading='flat',cmap=plt.cm.get_cmap('terrain',40))
cbar = mapa.colorbar(CS1, location='right',pad="2%")
cbar.set_label('[m/s]',rotation=0,labelpad=7)

mapa.drawcoastlines(linewidth=0.6)
mapa.drawcountries()
mapa.drawmapboundary()
mapa.drawparallels(np.arange(0.,21.,2.5),labels=[1,0,0,0], linewidth=0.0,fontsize=6)
mapa.drawmeridians(np.arange(-100.,-69.,5.),labels=[0,0,0,1], linewidth=0.0,fontsize=6)
mapa.drawmapscale(-97, 2., -87., 3, 500, barstyle='fancy',fontsize=6)

# Anadir vectores
U_norm = Um / np.sqrt(Um ** 2.0 + Vm ** 2.0)
V_norm = Vm / np.sqrt(Um ** 2.0 + Vm ** 2.0)   
Q=mapa.quiver(x[::6, ::6],y[::6, ::6],U_norm[::6, ::6],V_norm[::6, ::6],edgecolor='k', facecolor='k',scale=None)

plt.xlabel('Longitud', labelpad=10)
plt.ylabel('Latitud', labelpad=20)

plt.savefig(ruta + 'Viento' + trimestre + str(anno) + '.png', dpi=300, bbox='tight')
plt.savefig(ruta + 'Viento' + trimestre + str(anno) + '.png', dpi=300, bbox='tight')
plt.close()
