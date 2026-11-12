import gzip
from pathlib import Path

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    conteos = {}

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            metricas = columnas[4].split(",")

            for metrica in metricas:
                clave = metrica.split(":")[0]

                if clave in conteos:
                    conteos[clave] += 1
                else:
                    conteos[clave] = 1
    conteos = dict(sorted(conteos.items()))

    return conteos


if __name__ == "__main__":
    print(pregunta_09())
