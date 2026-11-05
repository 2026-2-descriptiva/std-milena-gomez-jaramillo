import json
import re
from pathlib import Path

import pandas as pd


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    # 1. Definir las rutas
    laboratorio = Path(__file__).resolve().parents[1]

    ruta_datos = laboratorio / "data" / "ventas.csv.gz"
    ruta_salida = (
        laboratorio / "submission" / "data_quality_report.json"
    )

    # 2. Leer los datos sin modificar sus valores
    df = pd.read_csv(
        ruta_datos,
        compression="gzip",
        dtype=str,
        keep_default_na=False
    )

    # 3. Normalizar únicamente los encabezados
    df.columns = [
        re.sub(r"\s+", "_", columna.strip().replace("\ufeff", "").lower())
        for columna in df.columns
    ]

    # 4. Definir las columnas requeridas
    columnas_requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email"
    ]

    # 5. Verificar la estructura
    faltantes = sorted(
        set(columnas_requeridas) - set(df.columns)
    )

    inesperadas = sorted(
        set(df.columns) - set(columnas_requeridas)
    )

    # 6. Contar filas duplicadas
    duplicados = int(df.duplicated().sum())

    # 7. Contar filas con identificadores repetidos
    duplicados_proveedor = int(
        df["supplier_id"].duplicated(keep=False).sum()
    )

    # 8. Contar valores faltantes
    valores_faltantes = {}

    for columna in df.columns:
        valores_faltantes[columna] = int(
            df[columna].isin(["", "N/A"]).sum()
        )

    # 9. Validar correos electrónicos
    patron_email = r"^[^@\s]+@[^@\s.]+\.[^@\s.]+$"

    correos_validos = df["contact_email"].str.fullmatch(
        patron_email
    )

    correos_invalidos = int((~correos_validos).sum())

    # 10. Validar unidades
    unidades = pd.to_numeric(
        df["units"].replace({"": None, "N/A": None}),
        errors="coerce"
    )

    unidades_invalidas = int(
        (
            unidades.notna()
            & (
                (unidades <= 0)
                | (unidades % 1 != 0)
            )
        ).sum()
    )

    # 11. Obtener países distintos sin modificar sus textos
    paises = sorted(df["country"].unique().tolist())

    # 12. Construir el reporte
    reporte = {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_required_columns": faltantes,
        "unexpected_columns": inesperadas,
        "duplicate_row_count": duplicados,
        "duplicate_supplier_id_row_count": duplicados_proveedor,
        "missing_value_count_by_column": valores_faltantes,
        "invalid_email_count": correos_invalidos,
        "invalid_unit_count": unidades_invalidas,
        "country_values": paises
    }

    # 13. Guardar el reporte JSON
    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(
            reporte,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    return reporte


if __name__ == "__main__":
    resultado = main()
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
