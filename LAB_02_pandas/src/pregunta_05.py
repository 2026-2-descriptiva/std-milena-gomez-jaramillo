import pandas as pd

def pregunta_05():
    """
    Usando `data/tbl0.tsv`, encuentre el valor máximo de la columna `c2` para
    cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice
    son las categorías, en orden alfabético, y cuyos valores son los máximos.

    Ejemplo del formato de la respuesta:

        c1
        A    9
        B    9
        C    9
        ...
    """
    ruta = r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_02_pandas\data\tbl0.tsv"

    df = pd.read_csv(ruta, sep="\t")

    maximos = df.groupby("c1")["c2"].max()

    maximos = maximos.sort_index()

    return maximos


if __name__ == "__main__":
    print(pregunta_05())
