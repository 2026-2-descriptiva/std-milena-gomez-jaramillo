import pandas as pd

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    ruta = r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_02_pandas\data\tbl1.tsv"

    df = pd.read_csv(ruta, sep="\t")

    valores_unicos = df["c4"].unique()

    valores_mayusculas = [
        valor.upper() for valor in valores_unicos
    ]

    resultado = sorted(valores_mayusculas)

    return resultado


if __name__ == "__main__":
    print(pregunta_06())
