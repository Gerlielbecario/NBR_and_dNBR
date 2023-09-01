#Este es un codigo que permite realizar el subset de la region de 
#interes de archivos hdf.
#Requiere de dos archivos. Uno con los datos y otro con la georeferenciacion

#---------Librerias-----------
import os
from modis_tools import lee_archivo, hora_archivo, fecha_archivo
from modis_tools import extrae_datos_hdf, indice_nbr
import numpy as np
import matplotlib.pyplot as plt


#---------Limites del subset--------------

lon_min = -60.5  # Valor mínimo de longitud
lon_max = -58.0  # Valor máximo de longitud
lat_min = -34.0  # Valor mínimo de latitud
lat_max = -32.0  # Valor máximo de latitud

#-----Ruta del archivo-------------------

#Nombre del archivo .hdf con datos  y su ruta
file_data = 'agosto.hdf'

folder_data = '/home/user/Escritorio/DATOS_POSTA/agosto/archivo'

#Nombre del archivo de georeferenciacion y su ruta
file_geo = 'agosto_geo.hdf'
folder_geo = '/home/user/Escritorio/DATOS_POSTA/agosto/geolocation'

#Paths
path_data = os.path.join(folder_data, file_data)
path_geo = os.path.join(folder_geo, file_geo)


#------------Lectura---------------------------------

# Leer los archivos HDF
var = lee_archivo(path_data)
geo = lee_archivo(path_geo)

#-------Extraccion de variables--------------------

#Temporales
time = hora_archivo(var)
date = fecha_archivo(var)

#Espaciales
latitude = extrae_datos_hdf(geo, "Latitude")[0]
longitude = extrae_datos_hdf(geo, "Longitude")[0]

#Datos de nbr
nbr_index = indice_nbr(var, "EV_500_Aggr1km_RefSB", "band_names")

#------Subset-----------------------

# Encontrar índices de latitud y longitud que caen dentro de
# la región de interés
mask_lon = (longitude[0] >= lon_min) & (longitude[0] <= lon_max)
mask_lat = (latitude[:, 0] >= lat_min) & (latitude[:, 0] <= lat_max)

# Aplicar las máscaras a las matrices
lon_sub = longitude[0, mask_lon]
lat_sub = latitude[mask_lat, 0]
matriz = nbr_index[mask_lat][:, mask_lon]

#---------------Guardar archivo-----------------------


#Reemplace aqui la ruta donde desea almacenar el archivo
folder_out = '/home/user/Escritorio/DATOS_POSTA'

##-----------No tocar---------------
name_out = f'{time}-{date}.npz'
outpath = os.path.join(folder_out,name_out)


np.savez(outpath,nbr = matriz,lat = lat_sub,lon = lon_sub)