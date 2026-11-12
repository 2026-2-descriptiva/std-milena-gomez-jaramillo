import gzip
from pathlib import Path

def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    sumas = {}

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            
            columnas = linea.strip().split("\t")

            letra = columnas[0]
            valor = int(columnas[1])

            if letra in sumas:
                sumas[letra] += valor
            else:
                sumas[letra] = valor

    return sorted(sumas.items())


if __name__ == "__main__":
    print(pregunta_03())

