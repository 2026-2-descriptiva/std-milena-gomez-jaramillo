from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """


    # --------------------------------------------------
    # 1. DEFINIR RUTAS
    # --------------------------------------------------

    laboratorio = Path(__file__).resolve().parents[1]

    ruta_entrada = (
        laboratorio / "data" / "solicitudes_de_credito.csv.gz"
    )

    ruta_salida = (
        laboratorio / "submission" / "solicitudes_de_credito.csv"
    )

    # --------------------------------------------------
    # 2. LEER LOS DATOS
    # --------------------------------------------------

    df = pd.read_csv(
        ruta_entrada,
        sep=";",
        compression="gzip"
    )

    print("Filas originales:", len(df))

    # --------------------------------------------------
    # 3. SELECCIONAR COLUMNAS
    # --------------------------------------------------

    columnas = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito"
    ]

    df = df[columnas].copy()

    # --------------------------------------------------
    # 4. NORMALIZAR COLUMNAS DE TEXTO
    # --------------------------------------------------

    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito"
    ]

    for columna in columnas_texto:

        df[columna] = (
            df[columna]
            .astype("string")
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        # Convertir textos vacíos en valores faltantes
        df[columna] = df[columna].replace("", pd.NA)

    # --------------------------------------------------
    # 5. NORMALIZAR ESTRATO
    # --------------------------------------------------

    estratos = (
        df["estrato"]
        .astype("string")
        .str.strip()
        .str.replace(r"[^\d-]", "", regex=True)
    )

    df["estrato"] = pd.to_numeric(
        estratos,
        errors="coerce"
    )

    # --------------------------------------------------
    # 6. NORMALIZAR MONTO DEL CRÉDITO
    # --------------------------------------------------

    montos = (
        df["monto_del_credito"]
        .astype("string")
        .str.strip()
    )

    # Eliminar símbolo monetario y espacios
    montos = montos.str.replace(
        r"[$\s]",
        "",
        regex=True
    )

    # Detectar valores como 1,200,000.00
    formato_monetario = montos.str.fullmatch(
        r"-?\d{1,3}(?:,\d{3})+\.\d{2}"
    ).fillna(False)

    # Quitar separadores de miles y decimales .00
    montos.loc[formato_monetario] = (
        montos.loc[formato_monetario]
        .str.replace(",", "", regex=False)
        .str.replace(r"\.00$", "", regex=True)
    )

    df["monto_del_credito"] = pd.to_numeric(
        montos,
        errors="coerce"
    )

    # --------------------------------------------------
    # 7. NORMALIZAR FECHAS
    # --------------------------------------------------

    fechas_originales = (
        df["fecha_de_beneficio"]
        .astype("string")
        .str.strip()
    )

    # Formato día/mes/año
    fechas = pd.to_datetime(
        fechas_originales,
        format="%d/%m/%Y",
        errors="coerce"
    )

    # Formato año/mes/día
    fechas = fechas.fillna(
        pd.to_datetime(
            fechas_originales,
            format="%Y/%m/%d",
            errors="coerce"
        )
    )

    # Formato año-mes-día
    fechas = fechas.fillna(
        pd.to_datetime(
            fechas_originales,
            format="%Y-%m-%d",
            errors="coerce"
        )
    )

    df["fecha_de_beneficio"] = fechas.dt.strftime(
        "%Y-%m-%d"
    )

    # --------------------------------------------------
    # 8. ELIMINAR REGISTROS INCOMPLETOS
    # --------------------------------------------------

    # comuna_ciudadano puede tener valores faltantes
    columnas_obligatorias = [
        columna
        for columna in df.columns
        if columna != "comuna_ciudadano"
    ]

    df = df.dropna(
        subset=columnas_obligatorias
    )

    print(
        "Filas después de eliminar faltantes:",
        len(df)
    )

    # --------------------------------------------------
    # 9. ELIMINAR REGISTROS DUPLICADOS
    # --------------------------------------------------

    df = df.drop_duplicates()

    print(
        "Filas después de eliminar duplicados:",
        len(df)
    )

    # --------------------------------------------------
    # 10. CONVERTIR VALORES NUMÉRICOS A ENTEROS
    # --------------------------------------------------

    df["estrato"] = df["estrato"].astype(int)

    df["monto_del_credito"] = (
        df["monto_del_credito"].astype(int)
    )

    # --------------------------------------------------
    # 11. EXPORTAR ARCHIVO LIMPIO
    # --------------------------------------------------

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        ruta_salida,
        sep=";",
        index=False,
        encoding="utf-8"
    )

    print("\nArchivo generado correctamente:")
    print(ruta_salida)

    # --------------------------------------------------
    # 12. MOSTRAR RESUMEN
    # --------------------------------------------------

    print("\nResumen de limpieza:")
    print("Registros finales:", len(df))
    print("Columnas:", len(df.columns))

    print(
        "Ideas de negocio distintas:",
        df["idea_negocio"].nunique()
    )

    print(
        "Barrios distintos:",
        df["barrio"].nunique()
    )

    print(
        "Montos distintos:",
        df["monto_del_credito"].nunique()
    )

    print(
        "Suma de créditos:",
        df["monto_del_credito"].sum()
    )

    print(
        "Comunas faltantes:",
        df["comuna_ciudadano"].isna().sum()
    )

    return df


if __name__ == "__main__":
    pregunta_01()
