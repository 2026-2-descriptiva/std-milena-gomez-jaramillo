# def pregunta_01():
#     """
#     Calcule la suma de los valores de la segunda columna (`value`) del
#     archivo `data/data.csv.gz` y retorne el resultado como un número entero.

#     Ejemplo del formato de la respuesta:

#         214
#     """
    

#     raise NotImplementedError


import pandas as pd

import gzip

with gzip.open(
    "LAB_01_python_basico/data/data.csv.gz",
    "rt",
    encoding="utf-8",
) as archivo:
    for _ in range(5):
        print(archivo.readline())



# data = pd.read_csv("LAB_01_python_basico\data\data.csv.gz", compression="gzip")

# print(data)