import pandas as pd

def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    ruta = r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_02_pandas\data\tbl0.tsv"

    df = pd.read_csv(ruta, sep="\t")

    cantidad = len(df)

    return int(cantidad)


if __name__ == "__main__":
    print(pregunta_01())