import gzip
from pathlib import Path

def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    conteos = {}

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            fecha = columnas[2]
            mes = fecha.split("-")[1]

            if mes in conteos:
                conteos[mes] += 1
            else:
                conteos[mes] = 1

    return sorted(conteos.items())


if __name__ == "__main__":
    print(pregunta_04())