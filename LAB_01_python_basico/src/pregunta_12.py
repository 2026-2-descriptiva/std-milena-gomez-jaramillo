import gzip

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    sumas = {}

    with gzip.open("C:\\Analitica_descriptiva\\std-milena-gomez-jaramillo\\LAB_01_python_basico\\data\\data.csv.gz", "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            letra = columnas[0]
            metricas = columnas[4].split(",")

            for metrica in metricas:
                clave, valor = metrica.split(":")
                valor = int(valor)

                if letra in sumas:
                    sumas[letra] += valor
                else:
                    sumas[letra] = valor

    sumas = dict(sorted(sumas.items()))

    return sumas


if __name__ == "__main__":
    print(pregunta_12())
