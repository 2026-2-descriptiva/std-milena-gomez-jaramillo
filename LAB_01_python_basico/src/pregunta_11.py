import gzip

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

    with gzip.open("C:\\Analitica_descriptiva\\std-milena-gomez-jaramillo\\LAB_01_python_basico\\data\\data.csv.gz", "rt", encoding="utf-8") as archivo:
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