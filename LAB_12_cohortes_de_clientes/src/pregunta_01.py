from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    # 1. Definir rutas
    laboratorio = Path(__file__).resolve().parents[1]

    ruta_entrada = laboratorio / "data" / "sales.csv.gz"
    carpeta_salida = laboratorio / "submission"

    carpeta_salida.mkdir(parents=True, exist_ok=True)

    # 2. Leer los datos
    df = pd.read_csv(
        ruta_entrada,
        compression="gzip"
    )

    # 3. Convertir las fechas
    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"]
    )

    # 4. Identificar el mes de cada compra
    df["order_month"] = (
        df["OrderDate"].dt.to_period("M")
    )

    # 5. Encontrar el mes de primera compra
    df["cohort"] = (
        df.groupby("CustomerID")["order_month"]
        .transform("min")
    )

    # 6. Calcular meses transcurridos
    df["period_index"] = (
        (df["order_month"].dt.year - df["cohort"].dt.year) * 12
        + (df["order_month"].dt.month - df["cohort"].dt.month)
    )

    # 7. Contar clientes distintos por cohorte y período
    retention = (
        df.groupby(["cohort", "period_index"])
        ["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    # 8. Obtener el tamaño de cada cohorte
    cohort_sizes = (
        retention.loc[
            retention["period_index"] == 0,
            ["cohort", "active_customers"]
        ]
        .rename(columns={
            "active_customers": "cohort_size"
        })
    )

    retention = retention.merge(
        cohort_sizes,
        on="cohort",
        how="left"
    )

    # 9. Calcular la tasa de retención
    retention["retention_rate"] = (
        retention["active_customers"]
        / retention["cohort_size"]
    )

    # 10. Convertir la cohorte a AAAA-MM
    retention["cohort_month"] = (
        retention["cohort"].astype(str)
    )

    # 11. Seleccionar y ordenar columnas
    retention = retention[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate"
        ]
    ].sort_values(
        ["cohort_month", "period_index"]
    ).reset_index(drop=True)

    # 12. Exportar tabla CSV
    retention.to_csv(
        carpeta_salida / "cohort_retention.csv",
        index=False
    )

    # 13. Crear matriz para el mapa de calor
    matriz = retention.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate"
    )

    # 14. Graficar retención
    fig, ax = plt.subplots(figsize=(11, 6))

    valores = np.ma.masked_invalid(
        matriz.to_numpy(dtype=float)
    )

    cmap = plt.get_cmap("YlGnBu").copy()
    cmap.set_bad(color="white")

    imagen = ax.imshow(
        valores,
        cmap=cmap,
        vmin=0,
        vmax=1,
        aspect="auto"
    )

    ax.set_xticks(range(len(matriz.columns)))
    ax.set_xticklabels(matriz.columns)

    ax.set_yticks(range(len(matriz.index)))
    ax.set_yticklabels(matriz.index)

    ax.set_xlabel("Meses desde la primera compra")
    ax.set_ylabel("Cohorte de clientes")
    ax.set_title("Retención mensual de clientes por cohorte")

    # 15. Escribir porcentajes dentro de cada celda
    for fila in range(len(matriz.index)):
        for columna in range(len(matriz.columns)):
            valor = matriz.iloc[fila, columna]

            if pd.notna(valor):
                ax.text(
                    columna,
                    fila,
                    f"{valor:.0%}",
                    ha="center",
                    va="center",
                    color="white" if valor > 0.5 else "black",
                    fontsize=9
                )

    fig.colorbar(
        imagen,
        ax=ax,
        label="Tasa de retención"
    )

    fig.tight_layout()

    # 16. Guardar imagen PNG
    fig.savefig(
        carpeta_salida / "cohort_retention_heatmap.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("\nTABLA DE RETENCIÓN")
    print(retention.to_string(index=False))

    return retention


if __name__ == "__main__":
    build_cohort_analysis()

