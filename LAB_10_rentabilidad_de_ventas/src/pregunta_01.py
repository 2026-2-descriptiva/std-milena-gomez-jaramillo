from pathlib import Path
import pandas as pd

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """


    # 1. Definir rutas
    laboratorio = Path(__file__).resolve().parents[1]

    ruta_entrada = (
        laboratorio / "data" / "superstore_orders.csv.gz"
    )

    carpeta_salida = laboratorio / "submission"
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    # 2. Leer el archivo comprimido
    df = pd.read_csv(
        ruta_entrada,
        sep=";",
        decimal=",",
        compression="gzip"
    )

    # 3. Crear variables auxiliares
    df["is_loss"] = df["Profit"] < 0

    df["loss_amount"] = (
        df["Profit"].where(df["Profit"] < 0, 0) * -1
    )

    # 4. Resumen global de rentabilidad
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    profitability_summary = pd.DataFrame([
        {
            "lines": len(df),
            "orders": df["Order ID"].nunique(),
            "sales": total_sales,
            "profit": total_profit,
            "profit_margin": round(
                total_profit / total_sales, 4
            ),
            "loss_lines": int(df["is_loss"].sum()),
            "loss_line_rate": round(
                df["is_loss"].mean(), 4
            ),
            "lost_profit": df["loss_amount"].sum()
        }
    ])

    # 5. Clasificar los descuentos
    def clasificar_descuento(valor):
        if valor == 0:
            return "0%"
        elif 0 < valor <= 0.05:
            return "1%-5%"
        elif 0.05 < valor <= 0.10:
            return "6%-10%"
        else:
            return "más de 10%"

    df["discount_band"] = (
        df["Discount"].apply(clasificar_descuento)
    )

    orden_descuentos = [
        "0%",
        "1%-5%",
        "6%-10%",
        "más de 10%"
    ]

    # 6. Resumen por rango de descuento
    discount_summary = (
        df.groupby("discount_band")
        .agg(
            lines=("Profit", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_line_rate=("is_loss", "mean"),
            lost_profit=("loss_amount", "sum")
        )
        .reindex(orden_descuentos)
        .reset_index()
    )

    discount_summary["profit_margin"] = (
        discount_summary["profit"]
        / discount_summary["sales"]
    )

    discount_summary["profit_margin"] = (
        discount_summary["profit_margin"].round(4)
    )

    discount_summary["loss_line_rate"] = (
        discount_summary["loss_line_rate"].round(4)
    )

    discount_summary = discount_summary[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit"
        ]
    ]

    # 7. Analizar segmentos y categorías
    priority_segments = (
        df.groupby(
            ["Customer Segment", "Product Category"]
        )
        .agg(
            lines=("Profit", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            lost_profit=("loss_amount", "sum")
        )
        .reset_index()
    )

    # Considerar solamente grupos con 100 o más líneas
    priority_segments = priority_segments[
        priority_segments["lines"] >= 100
    ].copy()

    # 8. Calcular margen por segmento
    priority_segments["profit_margin"] = (
        priority_segments["profit"]
        / priority_segments["sales"]
    ).round(4)

    # 9. Ordenar por pérdidas y seleccionar los primeros 5
    priority_segments = (
        priority_segments
        .sort_values(
            "lost_profit",
            ascending=False
        )
        .head(5)
        .reset_index(drop=True)
    )

    priority_segments = priority_segments[
        [
            "Customer Segment",
            "Product Category",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "lost_profit"
        ]
    ]

    # 10. Exportar los tres archivos
    profitability_summary.to_csv(
        carpeta_salida / "profitability_summary.csv",
        index=False
    )

    discount_summary.to_csv(
        carpeta_salida / "discount_summary.csv",
        index=False
    )

    priority_segments.to_csv(
        carpeta_salida / "priority_segments.csv",
        index=False
    )

    # 11. Mostrar resultados
    print("\nRESUMEN GLOBAL")
    print(profitability_summary.to_string(index=False))

    print("\nDESCUENTOS")
    print(discount_summary.to_string(index=False))

    print("\nSEGMENTOS PRIORITARIOS")
    print(priority_segments.to_string(index=False))

    return (
        profitability_summary,
        discount_summary,
        priority_segments
    )


if __name__ == "__main__":
    pregunta_01()

