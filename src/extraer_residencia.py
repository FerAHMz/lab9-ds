"""
Visitantes anuales de las 7 series separados en residentes de Guatemala y
extranjeros, a partir de la base limpia del Lab 1.

Desde 2023 la base de migracion deja de contar a los residentes de Guatemala
que regresan al pais. Esta tabla permite medir el crecimiento sin ese quiebre.
Solo hace falta correrlo una vez; la salida se versiona en data/raw/.

Entrada: ../Laboratorio-1-Series-de-Tiempo/data/processed/base_limpia.csv
Salida:  data/raw/visitantes_anual_por_residencia.csv
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BASE_LAB1 = RAIZ.parent / "Laboratorio-1-Series-de-Tiempo" / "data" / "processed" / "base_limpia.csv"
SALIDA = RAIZ / "data" / "raw" / "visitantes_anual_por_residencia.csv"

# mismas 7 series que construye la etapa 05 del Lab 1
SERIES = {
    "total": None,
    "region: América Del Centro": ("region_dos", "América Del Centro"),
    "region: América Del Norte": ("region_dos", "América Del Norte"),
    "region: Europa": ("region_dos", "Europa"),
    "frontera: La Aurora": ("frontera", "La Aurora"),
    "frontera: Valle Nuevo": ("frontera", "Valle Nuevo"),
    "frontera: San Cristóbal": ("frontera", "San Cristóbal"),
}


def main() -> None:
    base = pd.read_csv(BASE_LAB1, usecols=["anio", "region_dos", "frontera", "pais",
                                           "viajeros", "es_visitante"])
    visitantes = base[base["es_visitante"]]
    filas = []
    for serie, filtro in SERIES.items():
        sub = visitantes if filtro is None else visitantes[visitantes[filtro[0]] == filtro[1]]
        es_gt = sub["pais"] == "Guatemala"
        tabla = pd.DataFrame({
            "residentes_gt": sub[es_gt].groupby("anio")["viajeros"].sum(),
            "extranjeros": sub[~es_gt].groupby("anio")["viajeros"].sum(),
        }).fillna(0)
        filas.append(tabla.assign(serie=serie).reset_index())
    salida = pd.concat(filas)[["serie", "anio", "residentes_gt", "extranjeros"]].round(0)
    salida.to_csv(SALIDA, index=False)
    print(salida[salida["anio"].isin([2019, 2025])].to_string(index=False))


if __name__ == "__main__":
    main()
