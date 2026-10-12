import re
from pathlib import Path
import pandas as pd

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    # 1. Localizar el archivo de datos
    ruta = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "clusters_report.txt"
    )

    # 2. Leer el reporte como texto
    texto = ruta.read_text(encoding="utf-8")

    # 3. Identificar el comienzo de cada clúster
    patron = re.compile(
        r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s*(.*)$"
    )

    registros = []
    registro_actual = None

    # 4. Recorrer el reporte línea por línea
    for linea in texto.splitlines():

        coincidencia = patron.match(linea)

        if coincidencia:

            # Guardar el clúster anterior
            if registro_actual is not None:
                registros.append(registro_actual)

            # Extraer los campos del nuevo clúster
            cluster, cantidad, porcentaje, palabras = (
                coincidencia.groups()
            )

            registro_actual = {
                "cluster": int(cluster),
                "cantidad_de_palabras_clave": int(cantidad),
                "porcentaje_de_palabras_clave": float(
                    porcentaje.replace(",", ".")
                ),
                "fragmentos": [palabras],
            }

        elif registro_actual is not None:

            # Ignorar líneas vacías
            if linea.strip():
                registro_actual["fragmentos"].append(
                    linea.strip()
                )

    # 5. Guardar el último clúster
    if registro_actual is not None:
        registros.append(registro_actual)

    # 6. Limpiar y consolidar las palabras clave
    for registro in registros:

        texto_palabras = " ".join(
            registro["fragmentos"]
        )

        texto_palabras = " ".join(
            texto_palabras.split()
        )
        
        palabras = [
            palabra.strip()
            for palabra in texto_palabras.split(",")
        ]

        registro["principales_palabras_clave"] = (
            ", ".join(palabras).rstrip(".")
        )


        del registro["fragmentos"]

    # 7. Construir el DataFrame
    resultado = pd.DataFrame(
        registros,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return resultado


if __name__ == "__main__":
    print(pregunta_01())
