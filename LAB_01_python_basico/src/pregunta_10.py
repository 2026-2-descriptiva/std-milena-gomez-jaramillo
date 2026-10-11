import gzip

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    resultado = []

    with gzip.open("C:\\Analitica_descriptiva\\std-milena-gomez-jaramillo\\LAB_01_python_basico\\data\\data.csv.gz", "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            letra = columnas[0]

            codigos = columnas[3].split(",")
            metricas = columnas[4].split(",")

            cantidad_codigos = len(codigos)
            cantidad_metricas = len(metricas)

            resultado.append(
                (letra, cantidad_codigos, cantidad_metricas)
            )

    return resultado


if __name__ == "__main__":
    print(pregunta_10())

