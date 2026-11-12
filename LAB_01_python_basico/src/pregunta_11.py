import gzip
from pathlib import Path

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    sumas = {}

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            valor = int(columnas[1])
            codigos = columnas[3].split(",")

            for codigo in codigos:
                if codigo in sumas:
                    sumas[codigo] += valor
                else:
                    sumas[codigo] = valor
                    
    sumas = dict(sorted(sumas.items()))

    return sumas


if __name__ == "__main__":
    print(pregunta_11())