
from pathlib import Path
import pandas as pd

laboratorio = Path(
    r"C:\Analitica_descriptiva\std-milena-gomez-jaramillo\LAB_06_limpieza_de_solicitudes_de_credito"
)

df = pd.read_csv(
    laboratorio / "data" / "solicitudes_de_credito.csv.gz",
    sep=";",
    compression="gzip",
    dtype=str
)

for columna in [
    "monto_del_credito",
    "idea_negocio",
    "barrio",
    "línea_credito"
]:
    print(f"\n--- {columna} ---")

    print("Valores distintos:", df[columna].nunique())

    print(
        df[columna]
        .value_counts(dropna=False)
        .tail(30)
        .to_string()
    )

print("\nMontos con caracteres especiales:")
montos = df["monto_del_credito"].dropna()

print(
    montos[
        montos.str.contains(
            r"[^\d]",
            regex=True
        )
    ].drop_duplicates().head(40).to_list()
)
