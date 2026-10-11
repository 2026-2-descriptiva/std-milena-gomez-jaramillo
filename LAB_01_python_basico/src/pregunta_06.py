import gzip

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    extremos = {}

    with gzip.open("C:\\Analitica_descriptiva\\std-milena-gomez-jaramillo\\LAB_01_python_basico\\data\\data.csv.gz", "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            metricas = columnas[4].split(",")

            for metrica in metricas:
                clave, valor = metrica.split(":")
                valor = int(valor)

                if clave in extremos:
                    extremos[clave][0] = min(extremos[clave][0], valor)
                    extremos[clave][1] = max(extremos[clave][1], valor)
                else:
                    extremos[clave] = [valor, valor]

    return [
        (clave, valores[0], valores[1])
        for clave, valores in sorted(extremos.items())
    ]


if __name__ == "__main__":
    print(pregunta_06())