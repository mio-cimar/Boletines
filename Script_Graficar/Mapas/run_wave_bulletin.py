# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 08:38:54 2020

@author: GABY
"""

#prueba: run_wave_bulletin
#
#


import netCDF4
#import os
#import conda
#conda_file_dir = conda.__file__
#conda_dir = conda_file_dir.split('lib')[0]
#proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
#os.environ ['PROJ_LIB'] = 'C:/Users/xionf/anaconda3/Lib/site-packages/mpl_toolkits/basemap'
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math as mt

ruta = "/home/miocimar/Desktop/Boletines/Wave/Datos/"


# Extrae los datos del archivo netCDF

file1 = netCDF4.Dataset(ruta + 'hs_oct-dic_2019.nc','r')
file2 = netCDF4.Dataset(ruta + 'dp_oct-dic_2019.nc','r')
file3 = netCDF4.Dataset(ruta + 'tp_oct-dic_2019.nc','r')

HS = file1.variables['Thgt'][:,0,:,:] #altura
DP = file2.variables['Tdir'][:,0,:,:] #dirección de las olas
TP = file3.variables['Tper'][:,0,:,:] #periodo

#utiliza solo una variable porque son las mismas coordenadas y tiempos
LAT  = file1.variables['lat'][:]
LON  = file1.variables['lon'][:]-360
TI= file1.variables['time'][:]

# Cerrar el archivo
for file in range(1,4):
    "file"+ str(file) +".close()"

# Remover los datos incoherentes
HSr=np.ma.concatenate((HS[:1198,:,:], HS[1446:,:,:]), axis=0)
DPr=np.ma.concatenate((DP[:1198,:,:], DP[1446:,:,:]), axis=0)
TPr=np.ma.concatenate((TP[:1198,:,:], TP[1446:,:,:]), axis=0)



#Promedio de los campos 
TPm=np.nanmean(TPr,axis=0) 
HSm=np.nanmean(HSr,axis=0)  

######################################################################################################
#Promedio de dirección de las olas (dp)
#######################################################################################################
#Pasar a radianes y a grados 
FACR= np.pi / 180.
FACG= 180. / np.pi

DPr=np.array(DPr,dtype=np.float64) * FACR

LLAT=41
LLON=61
TT=30
DPm=np.full([LLAT,LLON],np.nan) 


DPc=np.nanmean(np.cos(DPr),axis=0)   #saca el coseno de todas las variables y lo convierte en una matriz
DPs=np.nanmean(np.sin(DPr),axis=0)   #saca el seno de todas las variables y lo convierte en una matriz
TIM= np.array(file2.variables['time'][:]) 
t=len(TIM)  #necesario para la estadistica

#formula 
DPcm=DPc/t
DPsm=DPs/t
   
R=np.sqrt(DPcm**2+DPsm**2)
Rm=R/t

v=np.sqrt(-2*np.log(Rm))

for FF in range(0,LLAT):
          for CC in range(0,LLON):
     
        #    print(FF,CC)
            
            if (DPsm[FF,CC] > 0) & (DPcm[FF,CC] > 0):
              
              DPm[FF,CC] = mt.atan(DPsm[FF,CC]/DPcm[FF,CC]) 
            
            elif (DPsm[FF,CC] < 0) & (DPcm[FF,CC] > 0):
              
              DPm[FF,CC] = mt.atan(DPsm[FF,CC]/DPcm[FF,CC]) + 2*np.pi
            
            else:
              
              DPm[FF,CC] = mt.atan(DPsm[FF,CC]/DPcm[FF,CC]) + np.pi

DPm=DPm*FACG

###################################   Mapas ####################################################
#Quality Figures
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('axes', labelsize=6)

#dimensiones
width = 3.487
height = width / 1.618

#################################################################################################
#                                     Período 
################################################################################################

fig=plt.figure(figsize=(width,height), facecolor='w', edgecolor='k')

m= Basemap(projection='merc',llcrnrlat= LAT.min(),urcrnrlat= LAT.max(),
              resolution='l',  llcrnrlon=LON.min(),urcrnrlon= LON.max())
m.drawparallels(np.arange(0.,21.,2.5),labels=[1,0,0,0],fontsize=6,fontname="Times New Roman",linewidth=0.0)
m.drawmeridians(np.arange(-100.,-69.,5.),labels=[0,0,0,1],fontsize=6,fontname="Times New Roman",linewidth=0.0)
m.drawmapscale(-97, 2., -87., 3, 500, barstyle='fancy',fontsize=6)
m.drawcoastlines(linewidth=0.6)
m.fillcontinents(color='gray',lake_color='blue')
m.drawcountries()
m.drawmapboundary()
m.fillcontinents()

x, y = m(*np.meshgrid(LON,LAT))

CS1=m.pcolormesh(x, y, TPm,vmin=4, vmax=22, shading='flat', cmap=plt.cm.get_cmap('cool', 18))

plt.ylabel("Latitud",size=6,fontname="Times New Roman",labelpad=15)
plt.xlabel("Longitud",size=6,fontname="Times New Roman",labelpad=7)

cb=m.colorbar(CS1,pad="2%")
cb.set_label('[s]', rotation=360,labelpad=7)


fig.savefig('/home/miocimar/Desktop/Boletines/Wave/Mapas/prueba_periodo.png',dpi=300,bbox='tight')
fig.savefig('/home/miocimar/Desktop/Boletines/Wave/Mapas/prueba_periodo.jpg',dpi=300,bbox='tight')
fig.savefig('/home/miocimar/Desktop/Boletines/Wave/Mapas/prueba_periodo.tif',dpi=300,bbox='tight')

plt.show()
plt.close
#################################################################################################
#                                    Mapa de Altura y Direccion de la ola
################################################################################################
fig2=plt.figure(figsize=(width, height), facecolor='w', edgecolor='k')
mapa=Basemap(projection='merc',llcrnrlon=LON.min(), \
		urcrnrlon=LON.max(),llcrnrlat=LAT.min(),urcrnrlat=LAT.max(),resolution='l')

mapa.drawparallels(np.arange(0.,21.,2.5),labels=[1,0,0,0], linewidth=0.0,fontsize=6)
mapa.drawmeridians(np.arange(-100.,-69.,5.),labels=[0,0,0,1], linewidth=0.0,fontsize=6)
mapa.drawmapscale(-97, 2., -87., 3, 500, barstyle='fancy',fontsize=6)
mapa.drawcoastlines(linewidth=0.6)
mapa.drawcountries()
mapa.drawmapboundary()
mapa.fillcontinents()

x, y = mapa(*np.meshgrid(LON,LAT))

 # Convertir de grados norte a coordenadas matematicas
deg=DPm
degN=90 - deg
degN[degN < 0] = degN[degN < 0] + 360
DPmo=degN + 180    
# Añadir vectores
# Normalise the data for uniform arrow size
promu=np.cos(np.deg2rad(DPmo)) 
promv=np.sin(np.deg2rad(DPmo))



CS1=mapa.pcolormesh(x,y,HSm,vmin=0,vmax=4, shading='flat' ,cmap=plt.cm.get_cmap('cool', 40))
holi=mapa.quiver(x[::4,::4],y[::4,::4],promu[::4,::4],promv[::4,::4], edgecolor="k",facecolor="k",scale=None)

cbar = mapa.colorbar(CS1, location='right',pad="2%")
cbar.set_label('[m]',rotation=0,labelpad=7)
plt.xlabel('Longitud', labelpad=10)
plt.ylabel('Latitud', labelpad=20)



fig2.savefig('/home/miocimar/Desktop/Boletines/Wave/Mapas/prueba_dp.png',dpi=300,bbox='tight')
fig2.savefig('/home/miocimar/Desktop/Boletines/Wave/Mapas/prueba_dp.jpg',dpi=300,bbox='tight')
fig2.savefig('/home/miocimar/Desktop/Boletines/Wave/Mapas/prueba_dp.tif',dpi=300,bbox='tight')


plt.show()          
plt.close() 