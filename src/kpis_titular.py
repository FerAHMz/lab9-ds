"""
Cifras de las tarjetas KPI del bloque 1.

Cada KPI tiene que poder compararse sin trampa. Por eso la recuperacion se mide
en America del Norte y Europa y no en el total: desde 2023 la base deja de
contar a los residentes de Guatemala (1.42 millones en 2022, ver codebook del
Lab 1), y eso hunde el total y a America del Centro sin que haya menos turismo.

Salida: outputs/kpis.csv
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "raw" / "series_mensuales.csv"
PERFIL = RAIZ / "outputs" / "perfil_mensual.csv"
SALIDA = RAIZ / "outputs" / "kpis.csv"


def main() -> None:
    df = pd.read_csv(ENTRADA, parse_dates=["fecha"]).set_index("fecha")
    anual = df.groupby(df.index.year).sum()
    perfil = pd.read_csv(PERFIL, index_col="mes")

    kpis = [
        ("record_2019_millones", anual.loc[2019, "total"] / 1e6,
         "Visitantes en 2019, el anio mas alto de la serie"),
        ("caida_2020_pct", 100 * (anual.loc[2020, "total"] / anual.loc[2019, "total"] - 1),
         "Caida del total en 2020 frente a 2019"),
        ("norteamerica_2025_vs_2019_pct",
         100 * (anual.loc[2025, "region: América Del Norte"] / anual.loc[2019, "region: América Del Norte"] - 1),
         "America del Norte en 2025 frente a 2019"),
        ("europa_2025_vs_2019_pct",
         100 * (anual.loc[2025, "region: Europa"] / anual.loc[2019, "region: Europa"] - 1),
         "Europa en 2025 frente a 2019"),
        ("diciembre_sobre_mes_tipico_pct", 100 * (perfil.loc["Dic", "Total"] - 1),
         "Visitantes de diciembre sobre un mes tipico (2009-2019)"),
    ]
    tabla = pd.DataFrame(kpis, columns=["kpi", "valor", "descripcion"]).set_index("kpi")
    tabla["valor"] = tabla["valor"].round(2)
    tabla.to_csv(SALIDA)
    print(tabla.to_string())


if __name__ == "__main__":
    main()
