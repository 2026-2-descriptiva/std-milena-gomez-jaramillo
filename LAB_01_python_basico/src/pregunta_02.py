import gzip

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    
    conteos = {}  # se resuelve con un diccionario de Python
    
    with gzip.open("C:\\Analitica_descriptiva\\std-milena-gomez-jaramillo\\LAB_01_python_basico\\data\\data.csv.gz", "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")
            letra = columnas[0]
            
            if letra in conteos:
                conteos[letra] += 1
            else:
                conteos[letra] = 1
                
    return sorted(conteos.items())


if __name__ == "__main__":
    print(pregunta_02())
