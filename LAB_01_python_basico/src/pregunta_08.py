import gzip

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """
    grupos = {}

    with gzip.open("C:\\Analitica_descriptiva\\std-milena-gomez-jaramillo\\LAB_01_python_basico\\data\\data.csv.gz", "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            letra = columnas[0]
            valor = int(columnas[1])

            if valor in grupos:
                grupos[valor].add(letra)
            else:
                grupos[valor] = {letra}

    return [
        (valor, sorted(letras))
        for valor, letras in sorted(grupos.items())
    ]


if __name__ == "__main__":
    print(pregunta_08())