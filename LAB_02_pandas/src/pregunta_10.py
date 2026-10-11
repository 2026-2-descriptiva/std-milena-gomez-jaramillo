import pandas as pd

def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """
    ruta = r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_02_pandas\data\tbl0.tsv"

    df = pd.read_csv(ruta, sep="\t")

    resultado = df.groupby("c1")["c2"].apply(
        lambda valores: ":".join(
            str(valor) for valor in sorted(valores)
        )
    )

    resultado = resultado.sort_index().to_frame(name="c2")

    return resultado


if __name__ == "__main__":
    print(pregunta_10())
