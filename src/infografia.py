"""
Infografia estatica de una pagina con los hallazgos del Lab 1.

Arma el lienzo A3 vertical (11 x 17 pulgadas) con los cinco bloques del boceto
de la seccion 2 del documento, cada uno dibujado por su propia funcion, y lo
exporta en las dos versiones que pide el enunciado.

Salidas en outputs/:
    infografia.png  lienzo digital de 1650 x 2550 px (150 ppp)
    infografia.pdf  version de impresion, exactamente una pagina A3

Antes de correrlo hay que generar las tablas de outputs/ con los scripts de
metricas y de kpis.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data" / "raw"
SALIDAS = RAIZ / "outputs"

# ------------------------------------------------------------------ paleta
# Seccion 4 del documento: dos azules tematicos, dos grises y un acento.
AZUL = "#16365C"         # dato observado, titulos y cifras
AZUL_2 = "#5B8DB8"       # series de apoyo
GRIS_OSCURO = "#5F6A75"  # serie cruda, subtitulos y notas (5.5:1)
GRIS_CLARO = "#C9D1D9"   # referencia que no es foco
ACENTO = "#E07A1F"       # caida, picos, ganador y estimacion (solo graficos y cifras grandes)
ACENTO_TXT = "#B4500E"   # el mismo acento para texto pequeno (5.1:1)
TEXTO = "#1F2933"
PANEL = "#F2F4F7"

# ------------------------------------------------------------------ tipografia
# Tamanos en puntos sobre el lienzo A3, segun la tabla de la seccion 4.
T_TITULAR, T_KPI, T_SUBTITULO = 30, 32, 14
T_BLOQUE, T_TEXTO, T_ETIQUETA, T_FICHA = 13, 10.5, 9, 7.5

_disponibles = {f.name for f in font_manager.fontManager.ttflist}
# Arial y no Helvetica Neue: en macOS esta ultima viene en un .ttc y matplotlib no
# encuentra su negrita, asi que toda la jerarquia por peso se perderia.
FUENTE = next((f for f in ("Arial", "Liberation Sans", "Helvetica") if f in _disponibles),
              "DejaVu Sans")
plt.rcParams.update({
    "font.family": FUENTE, "font.size": T_ETIQUETA, "text.color": TEXTO,
    "axes.edgecolor": GRIS_CLARO, "axes.labelcolor": TEXTO,
    "xtick.color": TEXTO, "ytick.color": TEXTO,
    "axes.spines.top": False, "axes.spines.right": False,
})

# ------------------------------------------------------------------ lienzo
ANCHO, ALTO = 11, 17
MARGEN = 0.045
# Franja vertical de cada bloque (inferior, superior) en fraccion del lienzo,
# con las proporciones de la tabla de la seccion 2: 20, 22, 22, 18 y 18 %.
FRANJAS = {
    1: (0.80, 1.00),
    2: (0.58, 0.80),
    3: (0.36, 0.58),
    4: (0.18, 0.36),
    5: (0.00, 0.18),
}


def panel(fig, x, y, w, h, color=PANEL):
    """Fondo gris muy claro para agrupar tarjetas; es el unico fondo de la pagina."""
    fig.patches.append(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.005",
        transform=fig.transFigure, facecolor=color, edgecolor="none", zorder=0))


def titulo_bloque(fig, numero, texto, y):
    """Numero del bloque en acento y titulo en azul, alineados al margen."""
    fig.text(MARGEN, y, str(numero), fontsize=T_BLOQUE, weight="bold", color=ACENTO)
    fig.text(MARGEN + 0.025, y, texto, fontsize=T_BLOQUE, weight="bold", color=AZUL)


def pendiente(fig, numero, nombre):
    """Reserva la franja de un bloque que todavia no se dibuja."""
    abajo, arriba = FRANJAS[numero]
    fig.patches.append(mpatches.Rectangle(
        (MARGEN, abajo + 0.008), 1 - 2 * MARGEN, arriba - abajo - 0.016,
        transform=fig.transFigure, fill=False, ls="--", lw=0.8, edgecolor=GRIS_CLARO))
    fig.text(0.5, (abajo + arriba) / 2, f"Bloque {numero}: {nombre}", ha="center",
             va="center", fontsize=T_TEXTO, color=GRIS_OSCURO)


# ------------------------------------------------------------------ bloques
def tarjetas_kpi():
    """Cifra, color y contexto de cada tarjeta, leidos de outputs/kpis.csv (seccion 3)."""
    k = pd.read_csv(SALIDAS / "kpis.csv", index_col="kpi")["valor"]
    return [
        (f"{k['record_2019_millones']:.2f} M", AZUL,
         "visitantes en 2019,\nel año más alto de la serie"),
        (f"−{abs(k['caida_2020_pct']):.0f} %", ACENTO,
         "cayó el flujo en 2020 por el\ncierre de fronteras (COVID-19)"),
        (f"+{k['norteamerica_2025_vs_2019_pct']:.0f} %", AZUL,
         f"Norteamérica en 2025 frente a\n2019 (Europa, +{k['europa_2025_vs_2019_pct']:.0f} %)"),
        (f"+{k['diciembre_sobre_mes_tipico_pct']:.0f} %", AZUL,
         "más visitantes en diciembre\nque en un mes típico"),
    ]


def bloque_1_titular_kpis(fig):
    abajo, arriba = FRANJAS[1]
    fig.text(MARGEN, arriba - 0.016,
             "Guatemala recupera a sus viajeros:\nlos mercados lejanos ya superan 2019",
             fontsize=T_TITULAR, weight="bold", color=AZUL, va="top", linespacing=1.1)
    fig.text(MARGEN, arriba - 0.077,
             "Radiografía de 17 años de flujo migratorio (2009–2026) y lo que anticipan los modelos",
             fontsize=T_SUBTITULO, color=GRIS_OSCURO, va="top")

    separacion = 0.014
    ancho = (1 - 2 * MARGEN - 3 * separacion) / 4
    base, alto = abajo + 0.012, 0.085
    for i, (cifra, color, contexto) in enumerate(tarjetas_kpi()):
        x = MARGEN + i * (ancho + separacion)
        panel(fig, x, base, ancho, alto)
        fig.text(x + 0.014, base + alto - 0.012, cifra, fontsize=T_KPI, weight="bold",
                 color=color, va="top")
        fig.text(x + 0.014, base + 0.012, contexto, fontsize=T_TEXTO, color=TEXTO,
                 va="bottom", linespacing=1.3)


def bloque_2_panorama(fig):
    """
    Linea de tiempo del total: el mes crudo en gris y el promedio de 12 meses en azul,
    con solo los eventos que respaldan los datos o el codebook (seccion 3).
    """
    import matplotlib.dates as mdates

    abajo, arriba = FRANJAS[2]
    titulo_bloque(fig, 2, "¿Cómo llegamos aquí? 17 años de visitantes", arriba - 0.018)

    total = (pd.read_csv(DATOS / "series_mensuales.csv", parse_dates=["fecha"])
             .set_index("fecha")["total"] / 1000)
    promedio = total.rolling(12).mean()
    fecha = pd.Timestamp
    techo = 540

    ax = fig.add_axes([MARGEN + 0.04, abajo + 0.022, 1 - 2 * MARGEN - 0.05, arriba - abajo - 0.075])
    ax.axvspan(fecha("2023-01-01"), fecha("2026-12-31"), color=PANEL, lw=0, zorder=0)
    ax.plot(total[:"2025-12"], color=GRIS_OSCURO, lw=0.8)
    ax.plot(total["2025-12":], color=GRIS_OSCURO, lw=0.8, ls=(0, (1, 1.5)))
    ax.plot(promedio, color=AZUL, lw=2.4)
    ax.plot(total["2020-04":"2020-08"], color=ACENTO, lw=3)

    ax.set_ylim(0, techo)
    ax.set_xlim(fecha("2008-10-01"), fecha("2026-12-31"))
    ax.set_yticks([0, 100, 200, 300, 400, 500], ["0", "100 mil", "200 mil", "300 mil", "400 mil", "500 mil"])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(labelsize=T_ETIQUETA)
    ax.grid(axis="y", color=GRIS_CLARO, lw=0.5)
    ax.set_title("Una década de crecimiento, un colapso en 2020 y una recuperación que la base "
                 "subestima desde 2023 (visitantes por mes)",
                 fontsize=T_TEXTO, weight="bold", color=AZUL, loc="left", pad=8)

    # etiquetas directas de las dos lineas
    ax.text(fecha("2009-02-01"), 245, "Cada mes", color=GRIS_OSCURO, fontsize=T_ETIQUETA)
    ax.text(fecha("2012-01-01"), 95, "Promedio de 12 meses", color=AZUL, fontsize=T_ETIQUETA,
            weight="bold")

    # eventos
    anual = total.groupby(total.index.year).sum()
    ax.text(fecha("2011-06-01"), 400,
            f"2009–2019: de {anual[2009] / 1000:.2f} a {anual[2019] / 1000:.2f}\nmillones de visitantes al año",
            color=AZUL, fontsize=T_ETIQUETA, linespacing=1.25)
    pico = total[:"2019-12"].idxmax()
    ax.annotate(f"Récord: {total[pico]:.0f} mil\n(dic-2019)", xy=(pico, total[pico]),
                xytext=(fecha("2016-09-01"), 490), fontsize=T_ETIQUETA, color=TEXTO,
                ha="right", va="center", linespacing=1.2,
                arrowprops=dict(arrowstyle="-", color=GRIS_OSCURO, lw=0.7))
    cierre = 100 * (total["2020-04":"2020-08"].sum() / total["2019-04":"2019-08"].sum() - 1)
    ax.text(fecha("2020-01-01"), 45, f"Abr–ago 2020: fronteras cerradas,\n−{abs(cierre):.0f} % frente a 2019",
            color=ACENTO_TXT, fontsize=T_ETIQUETA, weight="bold", ha="right", linespacing=1.2)
    ax.text(fecha("2021-01-01"), 470, "Reapertura\ngradual", color=TEXTO,
            fontsize=T_ETIQUETA, linespacing=1.2)
    ax.text(fecha("2023-02-15"), 510,
            "Desde 2023 la base no cuenta a\nlos residentes de Guatemala:\nniveles no comparables",
            color=GRIS_OSCURO, fontsize=T_ETIQUETA - 0.5, va="top", linespacing=1.25)
    ax.text(fecha("2026-02-01"), 110, "Ene–jun\n2026,\nparcial", color=GRIS_OSCURO,
            fontsize=T_ETIQUETA - 1, linespacing=1.15)


MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
NOMBRES = {"Total": "Total país", "América Del Centro": "Centroamérica",
           "América Del Norte": "Norteamérica", "Europa": "Europa", "La Aurora": "La Aurora (aéreo)",
           "Valle Nuevo": "Valle Nuevo", "San Cristóbal": "San Cristóbal"}


def heatmap_estacional(fig, rect):
    """Mapa de calor mes x anio del total, escala secuencial blanco -> azul principal."""
    from matplotlib.colors import LinearSegmentedColormap

    total = (pd.read_csv(DATOS / "series_mensuales.csv", parse_dates=["fecha"])
             .set_index("fecha")["total"] / 1000)
    tabla = (total.to_frame("v").assign(anio=total.index.year, mes=total.index.month)
             .pivot(index="anio", columns="mes", values="v"))
    perfil = pd.read_csv(SALIDAS / "perfil_mensual.csv", index_col="mes")["Total"]
    anios = list(tabla.index)

    escala = LinearSegmentedColormap.from_list("azules", ["#FFFFFF", AZUL_2, AZUL])
    escala.set_bad("white")
    ax = fig.add_axes(rect)
    im = ax.imshow(tabla, cmap=escala, vmin=0, vmax=450, aspect="auto")
    ax.set_xticks(range(12), MESES, fontsize=T_ETIQUETA)
    visibles = [2009, 2012, 2015, 2018, 2020, 2023, 2026]
    ax.set_yticks([anios.index(a) for a in visibles], visibles, fontsize=T_ETIQUETA)
    ax.tick_params(length=0)
    ax.spines[["left", "bottom"]].set_visible(False)

    # diciembre, el mes pico, enmarcado en acento
    ax.add_patch(mpatches.Rectangle((10.5, -0.5), 1, len(tabla), fill=False,
                                    edgecolor=ACENTO, lw=2, clip_on=False))
    # fechas que coinciden con los picos, sobre sus columnas, con su indice estacional
    techo = rect[1] + rect[3]
    for x, rotulo, mes in [(2.5, "Semana Santa", "Mar"), (6, "Vacaciones · bono 14", "Jul"),
                           (11, "Fin de año\n· aguinaldo", "Dic")]:
        x_fig = rect[0] + (x + 0.5) / 12 * rect[2]
        fig.text(x_fig, techo + 0.013, rotulo, ha="center", va="bottom",
                 fontsize=T_ETIQUETA - 1, color=TEXTO, linespacing=1.1)
        fig.text(x_fig, techo + 0.003, f"+{100 * (perfil[mes] - 1):.0f} %", ha="center",
                 va="bottom", fontsize=T_ETIQUETA, weight="bold",
                 color=ACENTO_TXT if mes == "Dic" else AZUL)
    # quiebre metodologico entre 2022 y 2023
    fila_2023 = anios.index(2023) - 0.5
    ax.axhline(fila_2023, color=TEXTO, lw=0.9, ls="--", clip_on=False, xmax=1.0)
    ax.text(11.65, fila_2023, " cambio de\n conteo", fontsize=T_ETIQUETA - 1.5, color=GRIS_OSCURO,
            va="center", ha="left", linespacing=1.1)

    barra = fig.add_axes([rect[0], rect[1] - 0.03, rect[2] * 0.45, 0.005])
    cb = fig.colorbar(im, cax=barra, orientation="horizontal", ticks=[0, 150, 300, 450])
    cb.ax.tick_params(length=0, labelsize=T_ETIQUETA - 1)
    cb.outline.set_visible(False)
    fig.text(rect[0] + rect[2] * 0.47, rect[1] - 0.0275, "mil visitantes al mes",
             fontsize=T_ETIQUETA - 1, color=GRIS_OSCURO, va="center")


def cuadrante(fig, x0, abajo, ancho, alto):
    """
    Tabla visual de 7 series x 4 preguntas: una columna de barras por pregunta, cada una
    con su propia escala, y la serie que responde en acento (seccion 6).
    """
    estacional = pd.read_csv(SALIDAS / "metricas_estacionalidad_pandemia.csv", index_col="serie")
    tendencia = pd.read_csv(SALIDAS / "metricas_tendencia_volatilidad.csv", index_col="serie")
    orden = list(NOMBRES)
    columnas = [
        ("¿Más\nestacional?", "índice 0 a 1",
         estacional["fuerza_estacional"], "{:.2f}", ["América Del Norte", "Europa"]),
        ("¿Más\ncrecimiento?", "% anual",
         tendencia["crecimiento_extranjeros_2009_2025_pct"], "{:.1f} %", None),
        ("¿Más\nvolátil?", "% de su nivel",
         100 * tendencia["cv_residuo"], "{:.0f} %", None),
        ("¿Más golpeada\npor la pandemia?", "caída 2020–21",
         -estacional["caida_2020_2021_pct"], "−{:.0f} %", None),
    ]
    etiquetas = 0.1
    ancho_col = (ancho - etiquetas) / 4
    y = list(range(len(orden)))[::-1]
    for i, (pregunta, unidad, valores, formato, ganadoras) in enumerate(columnas):
        valores = valores[orden]
        ganadoras = ganadoras or [valores.idxmax()]
        ax = fig.add_axes([x0 + etiquetas + i * ancho_col, abajo, ancho_col - 0.01, alto])
        colores = [ACENTO if s in ganadoras else GRIS_CLARO for s in orden]
        ax.barh(y, valores, color=colores, height=0.62)
        tope = valores.max()
        for yi, s, v in zip(y, orden, valores):
            gana = s in ganadoras
            ax.text(v + tope * 0.05, yi, formato.format(v), va="center", fontsize=T_ETIQUETA - 0.5,
                    color=ACENTO_TXT if gana else TEXTO, weight="bold" if gana else "normal")
        ax.set_xlim(0, tope * 1.9)
        ax.set_ylim(-0.6, len(orden) - 0.4)
        ax.set_xticks([])
        ax.set_yticks(y, [NOMBRES[s] for s in orden] if i == 0 else [], fontsize=T_ETIQUETA)
        ax.tick_params(left=False)
        ax.spines[["left", "bottom"]].set_visible(False)
        for corte in (5.5, 2.5):
            ax.axhline(corte, color=GRIS_CLARO, lw=0.5)
        izq = x0 + etiquetas + i * ancho_col
        fig.text(izq, abajo + alto + 0.013, pregunta, fontsize=T_ETIQUETA, weight="bold",
                 color=AZUL, va="bottom", linespacing=1.1)
        fig.text(izq, abajo + alto + 0.003, unidad, fontsize=T_ETIQUETA - 1,
                 color=GRIS_OSCURO, va="bottom")


def bloque_3_estacionalidad_cuadrante(fig):
    abajo, arriba = FRANJAS[3]
    titulo_bloque(fig, 3, "¿Qué se repite cada año y quién viene?", arriba - 0.018)
    titulo_y = arriba - 0.042

    fig.text(MARGEN, titulo_y, "Diciembre recibe 35 % más visitantes\nque un mes típico",
             fontsize=T_TEXTO, weight="bold", color=AZUL, va="top", linespacing=1.25)
    heatmap_estacional(fig, [MARGEN + 0.04, abajo + 0.045, 0.33, arriba - abajo - 0.14])

    x0 = 0.5
    fig.text(x0, titulo_y, "San Cristóbal crece más y es la menos predecible;\n"
             "Valle Nuevo fue la más golpeada por la pandemia",
             fontsize=T_TEXTO, weight="bold", color=AZUL, va="top", linespacing=1.25)
    cuadrante(fig, x0, abajo + 0.045, 1 - MARGEN - x0, arriba - abajo - 0.14)
    fig.text(x0, abajo + 0.012,
             "Estacionalidad y volatilidad medidas en 2009–2019. Crecimiento anual de 2009 a 2025\n"
             "contando solo extranjeros, sin el cambio de conteo de 2023.",
             fontsize=T_ETIQUETA - 0.5, color=GRIS_OSCURO, linespacing=1.3)


# Metricas de la serie total en la prueba del Lab 1 (abr-2021 a jun-2026), cuadernos de
# modelado: nombre, MAE, RMSE, si se actualiza cada mes. Seccion 5 del documento.
MODELOS = [
    ("Suavizamiento exp. simple", 158_777, 173_709, False),
    ("Holt-Winters amortiguado", 170_053, 183_865, False),
    ("Holt-Winters", 178_392, 192_825, False),
    ("Seasonal naive", 207_322, 219_664, False),
    ("SARIMA", 226_894, 243_234, False),
    ("Prophet", 232_826, 246_743, False),
    ("Seasonal naive", 65_996, 93_379, True),
    ("SARIMA (ganador)", 50_430, 80_789, True),
]
FIN_ENTRENAMIENTO = "2021-03"


def pronostico_ganador():
    """
    SARIMA(0,1,1)(1,1,0)12 sobre el logaritmo, el modelo elegido para la serie total en
    el Lab 1. Devuelve la estimacion a un mes adelante sobre la prueba con sus bandas de
    80 y 95 %, y la estimacion de los 12 meses siguientes con el modelo ajustado a toda
    la serie.
    """
    import warnings

    import numpy as np
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    warnings.filterwarnings("ignore")
    total = (pd.read_csv(DATOS / "series_mensuales.csv", parse_dates=["fecha"])
             .set_index("fecha")["total"].asfreq("MS"))
    orden = dict(order=(0, 1, 1), seasonal_order=(1, 1, 0, 12))
    ajuste = SARIMAX(np.log(total[:FIN_ENTRENAMIENTO]), **orden).fit(disp=False)
    prueba = total.index[total.index > FIN_ENTRENAMIENTO][0]
    pred = ajuste.apply(np.log(total)).get_prediction(start=prueba)
    futuro = SARIMAX(np.log(total), **orden).fit(disp=False).get_forecast(12)
    return {
        "observado": total,
        "estimacion": np.exp(pred.predicted_mean),
        "ic80": np.exp(pred.conf_int(alpha=0.20)),
        "ic95": np.exp(pred.conf_int(alpha=0.05)),
        "futuro": np.exp(futuro.predicted_mean),
        "futuro80": np.exp(futuro.conf_int(alpha=0.20)),
    }


def bloque_4_modelos_pronostico(fig):
    import matplotlib.dates as mdates
    import numpy as np

    abajo, arriba = FRANJAS[4]
    titulo_bloque(fig, 4, "¿Qué viene? El pronóstico solo sirve si se actualiza", arriba - 0.018)

    # izquierda: duelo de modelos, barras desde cero ordenadas por grupo
    ax = fig.add_axes([0.235, abajo + 0.058, 0.19, arriba - abajo - 0.108])
    y = np.arange(len(MODELOS))[::-1]
    for yi, (nombre, mae, rmse, actualizado) in zip(y, MODELOS):
        ganador = "ganador" in nombre
        color = ACENTO if ganador else (AZUL if actualizado else GRIS_CLARO)
        ax.barh(yi, mae / 1000, color=color, height=0.68)
        ax.text(mae / 1000 + 4, yi, f"{mae / 1000:.0f} mil", va="center", fontsize=T_ETIQUETA,
                color=ACENTO_TXT if ganador else TEXTO, weight="bold" if ganador else "normal")
    ax.set_yticks(y, [m[0] for m in MODELOS], fontsize=T_ETIQUETA)
    ax.set_xlim(0, 290)
    ax.set_xticks([])
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.tick_params(left=False)
    ax.axhline(1.5, color=GRIS_OSCURO, lw=0.6)
    ax.text(290, 7.55, "Pronóstico de 5 años de una vez", ha="right", fontsize=T_ETIQUETA - 0.5,
            color=GRIS_OSCURO, style="italic")
    ax.text(290, 1.35, "Actualizado cada mes", ha="right", va="top", fontsize=T_ETIQUETA - 0.5,
            color=AZUL, style="italic")
    ax.set_title("Actualizado cada mes, el pronóstico erra 3 veces menos",
                 fontsize=T_TEXTO, weight="bold", color=AZUL, loc="right", pad=10)
    fig.text(MARGEN, abajo + 0.012,
             "Error promedio por mes (MAE), total de visitantes, abr-2021 a jun-2026. El ganador erra\n"
             "unos 50 mil por mes (RMSE 81 mil). Sin actualizarse, todos arrastran el colapso de 2020.",
             fontsize=T_ETIQUETA, color=GRIS_OSCURO, linespacing=1.3)

    # derecha: pronostico del ganador con abanico rotulado como estimacion
    p = pronostico_ganador()
    ax = fig.add_axes([0.53, abajo + 0.058, 1 - MARGEN - 0.53, arriba - abajo - 0.108])
    obs = p["observado"]["2021-01":] / 1000
    ax.fill_between(p["ic95"].index, p["ic95"].iloc[:, 0] / 1000, p["ic95"].iloc[:, 1] / 1000,
                    color=ACENTO, alpha=0.14, lw=0)
    ax.fill_between(p["ic80"].index, p["ic80"].iloc[:, 0] / 1000, p["ic80"].iloc[:, 1] / 1000,
                    color=ACENTO, alpha=0.28, lw=0)
    ax.fill_between(p["futuro80"].index, p["futuro80"].iloc[:, 0] / 1000,
                    p["futuro80"].iloc[:, 1] / 1000, color=ACENTO, alpha=0.28, lw=0)
    ax.plot(p["estimacion"].index, p["estimacion"] / 1000, color=ACENTO, lw=1.6)
    ax.plot(p["futuro"].index, p["futuro"] / 1000, color=ACENTO, lw=1.8, ls="--")
    ax.plot(obs.index, obs, color=AZUL, lw=2)
    corte = p["observado"].index[-1] + pd.Timedelta(days=15)
    ax.axvline(corte, color=GRIS_OSCURO, lw=0.7, ls=":")
    techo = 700
    ax.set_ylim(0, techo)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(labelsize=T_ETIQUETA)
    ax.grid(axis="y", color=GRIS_CLARO, lw=0.5)
    ax.text(pd.Timestamp("2021-02-01"), techo * 0.92, "Observado", color=AZUL,
            fontsize=T_ETIQUETA, weight="bold")
    ax.text(pd.Timestamp("2023-04-01"), techo * 0.92, "Estimación a un mes", color=ACENTO_TXT,
            fontsize=T_ETIQUETA, weight="bold")
    ax.text(pd.Timestamp("2023-04-01"), techo * 0.88,
            "rango probable 80 % oscuro, 95 % claro\nen 2022 supera la escala",
            color=ACENTO_TXT, fontsize=T_ETIQUETA - 1, linespacing=1.2, va="top")
    ax.text(corte + pd.Timedelta(days=20), techo * 0.64, "Estimación\njul-26 a jun-27",
            color=ACENTO_TXT, fontsize=T_ETIQUETA - 0.5, weight="bold", linespacing=1.15,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))
    ax.set_title("El modelo ganador sigue la temporada (miles de visitantes)",
                 fontsize=T_TEXTO, weight="bold", color=AZUL, loc="left", pad=10)

    real = p["observado"][p["estimacion"].index]
    dentro = ((real >= p["ic80"].iloc[:, 0]) & (real <= p["ic80"].iloc[:, 1])).mean()
    fig.text(0.53, abajo + 0.012,
             f"El rango del 80 % contuvo {100 * dentro:.0f} de cada 100 meses reales. Para los próximos 12\n"
             f"meses se estiman unos {p['futuro'].sum() / 1e6:.1f} millones de visitantes, con picos en julio y diciembre.",
             fontsize=T_ETIQUETA, color=GRIS_OSCURO, linespacing=1.3)


def recomendaciones():
    """Cada accion con la cifra que la respalda, leida de las tablas de outputs/."""
    tendencia = pd.read_csv(SALIDAS / "metricas_tendencia_volatilidad.csv", index_col="serie")
    pandemia = pd.read_csv(SALIDAS / "metricas_estacionalidad_pandemia.csv", index_col="serie")
    perfil = pd.read_csv(SALIDAS / "perfil_mensual.csv", index_col="mes")
    ganador = next(m for m in MODELOS if "ganador" in m[0])[1]
    mejor_estatico = min(m[1] for m in MODELOS if not m[3])
    extranjeros = tendencia.loc["Total", "extranjeros_2025_vs_2019_pct"]
    crudo = pandemia.loc["Total", "recuperacion_2025_pct"]
    sc = tendencia.loc["San Cristóbal", "crecimiento_extranjeros_2009_2025_pct"]
    vn = pandemia.loc["Valle Nuevo", "caida_2020_2021_pct"]

    def pico(serie, mes):
        return 100 * (perfil.loc[mes, serie] - 1)

    return [
        ("Reportar a los visitantes\nextranjeros por separado", f"{extranjeros:.0f} %",
         f"de 2019 alcanzan en 2025 sin los\nresidentes de Guatemala. El total\n"
         f"crudo, {crudo:.0f} %, oculta la recuperación."),
        ("Lanzar campañas con el\ncalendario de cada mercado", "Dic · Jul · Nov",
         f"Centroamérica +{pico('América Del Centro', 'Dic'):.0f} % en diciembre,\n"
         f"Norteamérica +{pico('América Del Norte', 'Jul'):.0f} % en julio,\n"
         f"Europa +{pico('Europa', 'Nov'):.0f} % en noviembre."),
        ("Reforzar las fronteras\ncon El Salvador", f"+{sc:.1f} % al año",
         f"crecen los extranjeros por San\nCristóbal, la serie más volátil. Valle\n"
         f"Nuevo cayó {abs(vn):.0f} % en 2020 y 2021."),
        ("Actualizar el pronóstico\ncada mes", f"{mejor_estatico / ganador:.0f} veces menos",
         f"error, {ganador / 1000:.0f} mil visitantes al mes frente\na {mejor_estatico / 1000:.0f} mil "
         "del mejor pronóstico\nque no se actualiza."),
    ]


def bloque_5_recomendaciones(fig):
    abajo, arriba = FRANJAS[5]
    titulo_bloque(fig, 5, "¿Qué hacemos? Cuatro acciones para INGUAT", arriba - 0.018)

    separacion = 0.014
    ancho = (1 - 2 * MARGEN - 3 * separacion) / 4
    base, alto = abajo + 0.04, arriba - abajo - 0.075
    for i, (accion, cifra, contexto) in enumerate(recomendaciones()):
        x = MARGEN + i * (ancho + separacion)
        panel(fig, x, base, ancho, alto)
        izq, techo = x + 0.012, base + alto
        fig.text(izq, techo - 0.016, str(i + 1), fontsize=T_BLOQUE, weight="bold", color=ACENTO)
        fig.text(izq + 0.022, techo - 0.012, accion, fontsize=T_TEXTO, weight="bold",
                 color=AZUL, va="top", linespacing=1.2)
        fig.text(izq, techo - 0.046, cifra, fontsize=T_SUBTITULO + 3, weight="bold",
                 color=ACENTO_TXT, va="top")
        fig.text(izq, techo - 0.066, contexto, fontsize=T_ETIQUETA, color=TEXTO,
                 va="top", linespacing=1.3)

    fig.add_artist(plt.Line2D([MARGEN, 1 - MARGEN], [abajo + 0.031, abajo + 0.031],
                              color=GRIS_CLARO, lw=0.8, transform=fig.transFigure))
    fig.text(MARGEN, abajo + 0.027,
             "Fuente: Base de Migración 2009–2026 (enero 2009 a junio 2026), INGUAT / IGM. Visitantes = turistas + "
             "excursionistas. Desde 2023 la base no cuenta a los residentes de Guatemala que regresan al país.\n"
             "Modelos entrenados con enero 2009 a marzo 2021 y evaluados con abril 2021 a junio 2026. Estacionalidad, "
             "tendencia y volatilidad medidas sobre 2009–2019.\n"
             "Autores: Fernando Hernández (23645) y Fernando Rueda (23748). CC3084 Data Science, Universidad del Valle "
             "de Guatemala, 2026. Datos de uso académico, no publicar.",
             fontsize=T_FICHA, color=GRIS_OSCURO, va="top", linespacing=1.4)


def main() -> None:
    SALIDAS.mkdir(exist_ok=True)
    fig = plt.figure(figsize=(ANCHO, ALTO), facecolor="white")
    bloque_1_titular_kpis(fig)
    bloque_2_panorama(fig)
    bloque_3_estacionalidad_cuadrante(fig)
    bloque_4_modelos_pronostico(fig)
    bloque_5_recomendaciones(fig)
    fig.savefig(SALIDAS / "infografia.png", dpi=150, facecolor="white")
    fig.savefig(SALIDAS / "infografia.pdf", facecolor="white")
    plt.close(fig)
    print("infografia guardada en", SALIDAS)


if __name__ == "__main__":
    main()
