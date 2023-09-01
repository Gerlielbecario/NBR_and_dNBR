import numpy as np
from scipy.interpolate import griddata


def interpolar_modis(longitude,latitude,datos):
    x_p = np.reshape(longitude, longitude.size)  #vuelvo array de 1D
    y_p = np.reshape(latitude, latitude.size)  #idem


    #busco los maximos y mínimos de este lon-lat para despues armar la nueva grilla
    xmin,xmax,ymin,ymax = min(x_p),max(x_p),min(y_p),max(y_p)
    
    #genero la nueva grilla
    xi = np.arange(xmin, xmax, 0.01)
    yi = np.arange(ymin, ymax, 0.01)
    xi, yi = np.meshgrid(xi, yi)

    # Los valores originales de NBR a interpolar
    values = np.reshape(datos, datos.size)  #aca lo vuelvo un array de 1D para entrarlo en la funcion

    matriz = griddata((x_p, y_p), values, (xi, yi),method='linear')

    return xi,yi,matriz