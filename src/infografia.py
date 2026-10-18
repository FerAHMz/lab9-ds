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
FUENTE = next((f for f in ("Helvetica Neue", "Helvetica", "Arial") if f in _disponibles),
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
def bloque_1_titular_kpis(fig):
    pendiente(fig, 1, "titular y tarjetas KPI")


def bloque_2_panorama(fig):
    pendiente(fig, 2, "panorama histórico 2009–2026")


def bloque_3_estacionalidad_cuadrante(fig):
    pendiente(fig, 3, "calendario estacional y cuadrante comparativo")


def bloque_4_modelos_pronostico(fig):
    pendiente(fig, 4, "duelo de modelos y pronóstico")


def bloque_5_recomendaciones(fig):
    pendiente(fig, 5, "recomendaciones y ficha técnica")


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
