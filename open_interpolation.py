import numpy as np
import os

#---Lectura

folder = '/home/user/Escritorio/DATOS_POSTA/output_matrices'

file = '13:50:00-2022-04-06.npz'

path = os.path.join(folder,file)

#----Apertura

var = np.load(path)

print(type(var))