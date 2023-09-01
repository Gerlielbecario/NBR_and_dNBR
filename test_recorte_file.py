import os
from modis_tools import lee_archivo, hora_archivo, fecha_archivo
from modis_tools import extrae_datos_hdf, indice_nbr
from interpolacion import interpolar_modis
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata
import geopandas

# Definir las coordenadas de la región de interés
lon_min = -60.5  # Valor mínimo de longitud
lon_max = -58.0  # Valor máximo de longitud
lat_min = -34.0  # Valor mínimo de latitud
lat_max = -32.0  # Valor máximo de latitud

# Definir las rutas de los archivos
file_data = 'abril.hdf'
folder_data = '/home/user/Escritorio/DATOS_POSTA/6abril/archivo'
file_geo = 'abril_geo.hdf'
folder_geo = '/home/user/Escritorio/DATOS_POSTA/6abril/geolocation'
path_data = os.path.join(folder_data, file_data)
path_geo = os.path.join(folder_geo, file_geo)

# Leer los archivos HDF
var = lee_archivo(path_data)
geo = lee_archivo(path_geo)

# Extraer variables
time = hora_archivo(var)
date = fecha_archivo(var)
latitude = extrae_datos_hdf(geo, "Latitude")[0]
longitude = extrae_datos_hdf(geo, "Longitude")[0]
nbr_index = indice_nbr(var, "EV_500_Aggr1km_RefSB", "band_names")

# Encontrar índices de latitud y longitud que caen dentro de la región de interés
mask_lon = (longitude[0] >= lon_min) & (longitude[0] <= lon_max)
mask_lat = (latitude[:, 0] >= lat_min) & (latitude[:, 0] <= lat_max)

# Aplicar las máscaras a las matrices
lon_roi = longitude[0, mask_lon]
lat_roi = latitude[mask_lat, 0]
nbr_roi = nbr_index[mask_lat][:, mask_lon]


# Realizar interpolación
#xi, yi, matriz = interpolar_modis(lon_roi, lat_roi, nbr_roi)

# Crear la figura y el mapa
#fig = plt.figure(figsize=(10, 8))

#from matplotlib.ticker import FixedLocator
#import cartopy.feature as cfeature
#import cartopy.crs as ccrs
#from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

#ax = plt.axes(projection=ccrs.PlateCarree())

# Plotear la matriz sin interpolación como una imagen en el mapa
#cax = ax.pcolormesh(lon_roi, lat_roi, nbr_roi, transform=ccrs.PlateCarree(), shading='auto')

# Agregar características del mapa
#ax.add_feature(cfeature.COASTLINE)
#ax.add_feature(cfeature.BORDERS, linestyle=':')
#ax.add_feature(cfeature.LAND, edgecolor='black')

# Agregar barra de colores
#cbar = plt.colorbar(cax, orientation='vertical', label='NBR')

# Configurar título y etiquetas
#plt.title('Matriz de NBR en la Región de Interés')
#ax.set_xlabel('Longitud')
#ax.set_ylabel('Latitud')

# Mostrar el mapa
#plt.show()

print(lat_roi.shape)