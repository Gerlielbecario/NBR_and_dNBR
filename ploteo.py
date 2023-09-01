#Este es un codigo que extrae datos de modis

#-----Librerias y funciones--------------------
import os
from modis_tools import lee_archivo,hora_archivo,fecha_archivo
from modis_tools import extrae_datos_hdf,indice_nbr
from interpolacion import interpolar_modis
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.interpolate import griddata


#-------Lectura------------------

print('Iniciando lectura de archivo')


file_data = 'abril.hdf'

folder_data = '/home/user/Escritorio/DATOS_POSTA/6abril/archivo'

file_geo = 'abril_geo.hdf'

folder_geo = '/home/user/Escritorio/DATOS_POSTA/6abril/geolocation'

path_data = os.path.join(folder_data,file_data)

path_geo = os.path.join(folder_geo,file_geo)

print('Archivo leido correctamente')

#-----Apertura de datos----------------


var = lee_archivo(path_data)
geo = lee_archivo(path_geo)

#---Extraigo variables----------

print('Inicializando extraccion de variables')


#Hora y fecha
time = hora_archivo(var)
date = fecha_archivo(var)

#Latitud y longitud
latitude = extrae_datos_hdf(geo,"Latitude")[0]
longitude = extrae_datos_hdf(geo,"Longitude")[0]

#Calculamos Indice normalizado de area quemada
nbr_index = indice_nbr(var,"EV_500_Aggr1km_RefSB","band_names")


print('Extraccion de variables finalizada')
#------Interpolacion

print('Comenzando interpolacion')

xi,yi,matriz= interpolar_modis(longitude,latitude,nbr_index)

print('Interpolacion finalizada')

#---Guardamos el archivo

#print('Inicializando almacenamiento')

#output_path = f'/home/user/Escritorio/DATOS_POSTA/output_matrices/{time}-{date}.npz'
#np.savez(output_path,longitud = lon, latitud = lat , variable = nbr)

#print('Almacenamiento finalizado')

####------
#print('Proceso finalizado')

#print(algo[0])

#-----Ploteo

import cartopy.crs as ccrs
import cartopy.feature as cfeature
fig = plt.figure(figsize=(10, 8))
#ax = plt.axes(projection=ccrs.PlateCarree())



# Definir los límites de visualización para la región del Delta del Paraná
lon_min = -60.5  # Valor mínimo de longitud
lon_max = -58# Valor máximo de longitud
lat_min = -34  # Valor mínimo de latitud
lat_max = -32  # Valor máximo de latitud

ax = plt.axes(projection=ccrs.PlateCarree())

# Limitar la visualización a la región del Delta del Paraná
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# Plotear la matriz interpolada como una imagen en el mapa
cax = ax.pcolormesh(xi, yi, matriz, transform=ccrs.PlateCarree(), shading='auto')




# Agregar características del mapa
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')

# Agregar barra de colores
cbar = plt.colorbar(cax, orientation='vertical', label='NBR')

# Configurar título y etiquetas
plt.title('Matriz de NBR Interpolado')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Mostrar el mapa
plt.show()

