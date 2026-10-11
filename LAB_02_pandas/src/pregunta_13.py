import pandas as pd

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    ruta_tbl0 = r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_02_pandas\data\tbl0.tsv"

    ruta_tbl2 = r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_02_pandas\data\tbl2.tsv"

    df0 = pd.read_csv(ruta_tbl0, sep="\t")
    df2 = pd.read_csv(ruta_tbl2, sep="\t")

    tabla_combinada = pd.merge(df0, df2, on="c0")

    resultado = tabla_combinada.groupby("c1")["c5b"].sum()

    resultado = resultado.sort_index()

    return resultado


if __name__ == "__main__":
    print(pregunta_13())
