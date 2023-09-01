import numpy as np
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#Nombre del archivo .npz
file= '13:40:00-2022-08-22.npz'

folder= '/home/user/Escritorio/DATOS_POSTA'

path = os.path.join(folder,file)

#---Cargo datos

datos = np.load(path)


#Me muestra por pantalla que informacion tengo
print('Dentro del archivo se hallan los siguientes arrays: ')
for arreglo in datos.files:
    dimensiones = datos[arreglo].shape
    peso = datos[arreglo].nbytes
    peso_megas = peso/(1024**2)
    print(arreglo,dimensiones," tamaño en disco:",np.round(peso_megas,2),"MB")

#-----Extraigo datos

nbr = datos['nbr']
lat = datos['lat']
lon = datos['lon']

#---Plotear

# Crear la figura y el mapa
fig = plt.figure(figsize=(10, 8))

ax = plt.axes(projection=ccrs.PlateCarree())

# Plotear la matriz sin interpolación como una imagen en el mapa
cax = ax.pcolormesh(lon, lat, nbr, transform=ccrs.PlateCarree(), shading='auto')

# Agregar características del mapa
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')

# Agregar barra de colores
cbar = plt.colorbar(cax, orientation='vertical', label='NBR')

# Configurar título y etiquetas
plt.title('Matriz de NBR en la Región de Interés')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Mostrar el mapa
plt.show()
