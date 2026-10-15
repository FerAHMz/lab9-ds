"""
Metricas de estacionalidad y de golpe de la pandemia para las 7 series del Lab 1.

Alimenta dos piezas de la infografia: el bloque 3 (cuando viene la gente y que
fechas marcan la pauta) y la mitad del cuadrante comparativo que responde
"cual serie es mas estacional" y "cual fue la mas golpeada por la pandemia".

Salidas en outputs/:
    metricas_estacionalidad_pandemia.csv  una fila por serie
    perfil_mensual.csv                    indice estacional por mes y serie
    heatmap_estacionalidad_total.png      borrador del heatmap mes x anio
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "raw" / "series_mensuales.csv"
SALIDAS = RAIZ / "outputs"

# La estacionalidad se mide antes de la pandemia: los ceros de abril a agosto
# de 2020 y la reapertura escalonada distorsionan cualquier descomposicion que
# los incluya, y lo que interesa es el patron "normal" del anio turistico.
INICIO_NORMAL, FIN_NORMAL = "2009-01", "2019-12"
ANIO_BASE, ANIOS_PANDEMIA, ANIO_RECUPERACION = 2019, [2020, 2021], 2025

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def nombre_corto(columna: str) -> str:
    """'region: Europa' -> 'Europa'; 'total' -> 'Total'."""
    return columna.split(": ")[-1] if ": " in columna else columna.capitalize()


def fuerza_estacional(serie: pd.Series) -> float:
    """
    Fuerza estacional de Hyndman y Athanasopoulos, F_s = max(0, 1 - Var(R) / Var(S + R)),
    sobre una STL robusta del logaritmo. Va de 0 (sin patron) a 1 (patron puro).
    Se usa el logaritmo porque la estacionalidad de estas series es multiplicativa:
    el pico de diciembre crece junto con el nivel.
    """
    stl = STL(np.log(serie), period=12, robust=True).fit()
    return max(0.0, 1 - np.var(stl.resid) / np.var(stl.seasonal + stl.resid))


def perfil_mensual(serie: pd.Series) -> pd.Series:
    """
    Indice estacional por mes: cada mes dividido entre el promedio mensual de
    su propio anio, promediado sobre los anios normales. 1.20 significa que ese
    mes recibe 20% mas visitantes que un mes tipico del anio.
    """
    anual = serie.groupby(serie.index.year).transform("mean")
    return (serie / anual).groupby(serie.index.month).mean()


def golpe_pandemia(anual: pd.Series) -> dict:
    base = anual[ANIO_BASE]
    return {
        "caida_2020_pct": 100 * (anual[2020] / base - 1),
        "caida_2020_2021_pct": 100 * (anual[ANIOS_PANDEMIA].sum() / (2 * base) - 1),
        "recuperacion_2025_pct": 100 * anual[ANIO_RECUPERACION] / base,
    }


def heatmap_total(serie: pd.Series, destino: Path) -> None:
    """Borrador del heatmap del bloque 3; la paleta final se define en la seccion 04."""
    tabla = serie.to_frame("v").assign(anio=serie.index.year, mes=serie.index.month)
    tabla = tabla.pivot(index="anio", columns="mes", values="v") / 1000

    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
    im = ax.imshow(tabla, cmap="Blues", aspect="auto")
    ax.set_xticks(range(12), MESES)
    ax.set_yticks(range(len(tabla)), tabla.index)
    ax.set_title("Visitantes por mes (miles), total del pais")
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)
    fig.colorbar(im, ax=ax, shrink=0.8, label="miles de visitantes")
    fig.tight_layout()
    fig.savefig(destino)
    plt.close(fig)


def main() -> None:
    SALIDAS.mkdir(exist_ok=True)
    df = pd.read_csv(ENTRADA, parse_dates=["fecha"]).set_index("fecha")
    normal = df.loc[INICIO_NORMAL:FIN_NORMAL]
    anual = df.groupby(df.index.year).sum()

    filas, perfiles = [], {}
    for col in df.columns:
        perfil = perfil_mensual(normal[col])
        perfiles[nombre_corto(col)] = perfil
        filas.append({
            "serie": nombre_corto(col),
            "fuerza_estacional": fuerza_estacional(normal[col]),
            "mes_pico": MESES[perfil.idxmax() - 1],
            "indice_pico": perfil.max(),
            "mes_valle": MESES[perfil.idxmin() - 1],
            "indice_valle": perfil.min(),
            "amplitud_pico_valle": perfil.max() / perfil.min(),
            **golpe_pandemia(anual[col]),
        })

    metricas = pd.DataFrame(filas).set_index("serie").round(3)
    metricas.to_csv(SALIDAS / "metricas_estacionalidad_pandemia.csv")

    tabla_perfil = pd.DataFrame(perfiles).round(3)
    tabla_perfil.index = MESES
    tabla_perfil.index.name = "mes"
    tabla_perfil.to_csv(SALIDAS / "perfil_mensual.csv")

    heatmap_total(df["total"], SALIDAS / "heatmap_estacionalidad_total.png")

    print(metricas.to_string())
    print()
    print(tabla_perfil.to_string())
    print()
    print("Mas estacional:", metricas["fuerza_estacional"].idxmax())
    print("Mas golpeada (2020-2021):", metricas["caida_2020_2021_pct"].idxmin())


if __name__ == "__main__":
    main()
