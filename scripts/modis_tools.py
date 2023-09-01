#Este es un codigo que contiene funciones utiles para trabajar
#con datos satelitales de modis

#Librerias que vamos a utilizar
import numpy as np
import pyhdf.SD
from pyhdf.SD import SD,SDC #Necesitamos la libreria pyhdf para leer archivos y SD una clase
import glob #una libreria que usamos
import pandas as pd
import matplotlib.pyplot as plt
import re #liberia para regex que luego usaremos en texto


#-------------------Funciones------------------------



#-----------------Lee archivos -----------------------
def lee_archivo(File):
    archivo = SD(File,SDC.READ)
    return archivo

#--------------------Lee el contenido de metadata-------------
def busca_meta_data(File):
    meta_data = File.attributes()["CoreMetadata.0"]
    return meta_data

#---------------Devuelve la fecha de archivo------------------------
def fecha_archivo(File):
    meta_data = busca_meta_data(File)
    
    #Generamos una regex con el formato \b(?:word_a\W+(?:\w+\W+){0,20}?word_b)\b
    #Busca en meta_data una seccion del texto donde se halla informacion sobre la fecha
    #en la que se inicio el scaneo
    info_inicio_hora = re.search(r'\b(?:RANGEBEGINNINGDATE\W+(?:\w+\W+){0,20}?RANGEBEGINNINGDATE)\b',meta_data)[0]

    patron_fecha = r'(\d{4})-(\d{2})-(\d{2})'
    
    fecha = re.search(patron_fecha,meta_data)[0]
    
    return fecha



#-------Devuelve la hora del archivo---------------------

def hora_archivo(File):
    
    #Al ingresar el File hdf nos devuelve la hora en la que inicio el scaneo
    #de los datos
    meta_data = busca_meta_data(File)
    
    #Generamos una regex con el formato \b(?:word_a\W+(?:\w+\W+){0,20}?word_b)\b
    #Busca en meta_data una seccion del texto donde se halla informacion sobre el inicio
    #de la hora del scaneo
    info_inicio_hora = re.search(r'\b(?:RANGEBEGINNINGTIME\W+(?:\w+\W+){0,20}?RANGEBEGINNINGTIME)\b',meta_data)[0]

    patron_hora = r'(\d{2}):(\d{2}):(\d{2})'
    
    hora = re.search(patron_hora,info_inicio_hora)[0]
    
    return hora  

#-------Una manera de visualizar tu archivo-----------------

def visualiza_hdf(File):
    
    #El modulo datasets (proviene de la libreria pyhdf) me devuelve informacion sobre que
    #hay dentro del hdf. 
    datasets = {"Datasets": list(File.datasets().keys())}
    
    #Lo transformamos a un dataframe para visualizar
    info_file = pd.DataFrame(datasets)
    
    return info_file


#Funcion que pide como argumento un archivo hdf y el dataset que queramos

def selecciona_sds_hdf(File,sds):
    
    #Seleccionamos el dataset con "select" metodo de la libreria pyhdf
    sds_seleccionado = File.select(sds)
    
    return sds_seleccionado

#Toma como argumento un archivo hdf y el dataset que desee extraer

def extrae_datos_hdf(File,sds):
    
    #Seleccionamos el dataset con la funcion
    dataset = selecciona_sds_hdf(File,sds)
    
    #Extraemos los datos con el metodo get de pyhdf
    sds_datos = dataset.get()
    
    #Devuelve los datos y su dimension
    return sds_datos,sds_datos.shape

def selecciona_atributos_sds(File,sds):
    
    #Seleccionamos el dataset
    dataset = selecciona_sds_hdf(File,sds)
    
    #Utilizamos el metodo attribute, nos devuelve un diccionario con una descripcion
    #global de cada atributo adjunto al archivo hdf
    dic_atributos = dataset.attributes()
    
    return dic_atributos

#Input : File y un dataset
def muestra_atributos_sds(File,sds):
    
    dic_atributos = selecciona_atributos_sds(File,sds)
        
    #Tomamos las llaves y valores del diccionario y los transformamos en listas
    #para luego generar una tabla y visualizarlo
    columna1 = list(dic_atributos.keys())
    columna2 = list(dic_atributos.values())
    
    #Generamos una tabla/dataframe
    df = pd.DataFrame({"":columna1,"Atributos":columna2})
    df = df.set_index("")
    
    #Regresa una tabla donde se muestran los atributos del dataset
    return df


#Se elige un file hdf, sds: el dataset que queramos y el atributo del dataset
def extrae_atributos_sds(File,sds,atributo):
    
    #Utilizamos la funcion para generar un diccionario con los atributos
    dic_atributos = selecciona_atributos_sds(File,sds)
    
    #Del diccionario elegimos el atributo que queremos
    attr = dic_atributos[atributo]
    
    #Devuelve una lista con los valores de mi atributo
    return attr


#Extrae los valores de la banda seleccionada ya convertidos a reflectancia

#File hdf, sds: dataset,canal deseado, nombre de atributo con las bandas
def extrae_banda(File,sds,band,nombre_atributo):
    
    #Extraemos los valores de reflectancia sin conversion
    REF = extrae_datos_hdf(File,sds)[0]
    
    #Extraemos los numeros de bandas que tenemos. Ej:band 1, band2
    #Spliteamos para operar en ellas
    n_bands = extrae_atributos_sds(File,sds,nombre_atributo).split(",")
    
    #Elegimos la banda
    
    posicion_band = n_bands.index(str(band))
    
    
    #Hacemos la conversion
    
    rad_off_ref= extrae_atributos_sds(File,sds,"reflectance_offsets")[posicion_band]
    
    rad_scales_ref = extrae_atributos_sds(File,sds,"reflectance_scales")[posicion_band]
    
    canal = rad_scales_ref * (REF[posicion_band,:,:] - rad_off_ref)
    
    return canal


def indice_nbr(File,sds,nombre_atributo):
    
    #Extraemos las bandas con las cuales vamos a trabajar
    canal_5 = extrae_banda(File,sds,5,nombre_atributo)
    canal_7 = extrae_banda(File,sds,7,nombre_atributo)
    
    #Calculamos el indice NBR
    nbr = (canal_5 - canal_7) / (canal_5 + canal_7)
    
    #array con los valores de nbr
    return nbr  

