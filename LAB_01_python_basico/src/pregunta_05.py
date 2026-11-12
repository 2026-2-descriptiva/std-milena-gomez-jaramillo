import gzip
from pathlib import Path

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    
    extremos = {}

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            letra = columnas[0]
            valor = int(columnas[1])

            if letra in extremos:
                extremos[letra][0] = max(extremos[letra][0], valor)
                extremos[letra][1] = min(extremos[letra][1], valor)
            else:
                extremos[letra] = [valor, valor]

    return [
        (letra, valores[0], valores[1])
        for letra, valores in sorted(extremos.items())
    ]


if __name__ == "__main__":
    print(pregunta_05())