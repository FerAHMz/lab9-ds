"""
Metricas de tendencia y volatilidad para las 7 series del Lab 1.

Alimenta la otra mitad del cuadrante comparativo del bloque 3, la que responde
"cual serie presenta mayor tendencia de crecimiento" y "cual exhibe mayor
volatilidad".

Entradas en data/raw/: series_mensuales.csv y visitantes_anual_por_residencia.csv

Salida en outputs/:
    metricas_tendencia_volatilidad.csv  una fila por serie
"""

from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "raw" / "series_mensuales.csv"
RESIDENCIA = RAIZ / "data" / "raw" / "visitantes_anual_por_residencia.csv"
SALIDAS = RAIZ / "outputs"

# Mismo tramo normal que las metricas de estacionalidad: la volatilidad se mide
# antes de la pandemia para que los ceros de 2020 no se cuenten como "ruido".
INICIO_NORMAL, FIN_NORMAL = "2009-01", "2019-12"
ANIO_INICIO, ANIO_PRE, ANIO_FIN = 2009, 2019, 2025

# Desde 2023 la base deja de contar a los residentes de Guatemala, lo que hunde
# el nivel de las series que los incluian sin que haya menos turismo extranjero.
# Por eso el crecimiento tambien se mide solo con extranjeros (extraer_residencia.py).


def nombre_corto(columna: str) -> str:
    """'region: Europa' -> 'Europa'; 'total' -> 'Total'."""
    return columna.split(": ")[-1] if ": " in columna else columna.capitalize()


def crecimiento_compuesto(anual: pd.Series, inicio: int, fin: int) -> float:
    """Tasa de crecimiento anual compuesta (CAGR) entre dos anios completos, en %."""
    return 100 * ((anual[fin] / anual[inicio]) ** (1 / (fin - inicio)) - 1)


def volatilidad(serie: pd.Series) -> dict:
    """
    Coeficiente de variacion de los residuos de una STL robusta: la desviacion
    estandar del componente irregular dividida entre el nivel medio de la serie.
    Al quitar antes la tendencia y la estacionalidad, mide solo lo impredecible;
    el CV de la serie cruda mezclaria las tres cosas.
    """
    stl = STL(serie, period=12, robust=True).fit()
    return {
        "cv_residuo": stl.resid.std() / serie.mean(),
        "cv_serie_cruda": serie.std() / serie.mean(),
        "cambio_mensual_tipico": np.log(serie).diff().std(),
    }


def main() -> None:
    SALIDAS.mkdir(exist_ok=True)
    df = pd.read_csv(ENTRADA, parse_dates=["fecha"]).set_index("fecha")
    normal = df.loc[INICIO_NORMAL:FIN_NORMAL]
    anual = df.groupby(df.index.year).sum()
    residencia = pd.read_csv(RESIDENCIA)

    filas = []
    for col in df.columns:
        serie = nombre_corto(col)
        res = residencia[residencia["serie"] == col].set_index("anio")
        extranjeros = res["extranjeros"]
        filas.append({
            "serie": serie,
            "visitantes_2009": anual.loc[ANIO_INICIO, col],
            "visitantes_2019": anual.loc[ANIO_PRE, col],
            "visitantes_2025": anual.loc[ANIO_FIN, col],
            "crecimiento_2009_2025_pct": crecimiento_compuesto(anual[col], ANIO_INICIO, ANIO_FIN),
            "crecimiento_2009_2019_pct": crecimiento_compuesto(anual[col], ANIO_INICIO, ANIO_PRE),
            "crecimiento_extranjeros_2009_2025_pct": crecimiento_compuesto(extranjeros, ANIO_INICIO, ANIO_FIN),
            "extranjeros_2025_vs_2019_pct": 100 * extranjeros[ANIO_FIN] / extranjeros[ANIO_PRE],
            "residentes_gt_2019_pct": 100 * res.loc[ANIO_PRE, "residentes_gt"] / anual.loc[ANIO_PRE, col],
            **volatilidad(normal[col]),
            "afectada_metodologia_2023": res.loc[ANIO_PRE, "residentes_gt"] > 0,
        })

    metricas = pd.DataFrame(filas).set_index("serie").round(3)
    metricas.to_csv(SALIDAS / "metricas_tendencia_volatilidad.csv")

    print(metricas.to_string())
    print()
    print("Mayor crecimiento 2009-2025:", metricas["crecimiento_2009_2025_pct"].idxmax())
    print("Mayor crecimiento 2009-2019:", metricas["crecimiento_2009_2019_pct"].idxmax())
    print("Mayor crecimiento de extranjeros 2009-2025:",
          metricas["crecimiento_extranjeros_2009_2025_pct"].idxmax())
    print("Mas volatil (CV de residuos):", metricas["cv_residuo"].idxmax())


if __name__ == "__main__":
    main()
