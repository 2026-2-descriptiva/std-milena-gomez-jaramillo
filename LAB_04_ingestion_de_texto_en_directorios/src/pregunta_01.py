from pathlib import Path
import pandas as pd

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    # Carpeta principal del laboratorio
    laboratorio = Path(__file__).resolve().parents[1]

    # Carpetas de entrada y salida
    carpeta_datos = laboratorio / "data"
    carpeta_salida = laboratorio / "submission"

    carpeta_salida.mkdir(parents=True, exist_ok=True)

    # Procesar entrenamiento y prueba
    for division in ["train", "test"]:

        registros = []

        ruta_division = carpeta_datos / division

        # Recorrer las categorías alfabéticamente
        for carpeta_categoria in sorted(
            ruta_division.iterdir()
        ):

            if not carpeta_categoria.is_dir():
                continue

            categoria = carpeta_categoria.name

            # Recorrer los archivos de texto alfabéticamente
            for archivo in sorted(
                carpeta_categoria.glob("*.txt")
            ):

                frase = archivo.read_text(
                    encoding="utf-8"
                ).strip()

                registros.append({
                    "phrase": frase,
                    "target": categoria,
                })

        # Construir el DataFrame
        df = pd.DataFrame(
            registros,
            columns=["phrase", "target"]
        )

        # Guardar el CSV correspondiente
        ruta_csv = carpeta_salida / f"{division}_dataset.csv"

        df.to_csv(
            ruta_csv,
            index=False,
            encoding="utf-8"
        )



if __name__ == "__main__":
    pregunta_01()
    print("Archivos CSV generados correctamente.")

