# Laboratorio 9. Visualización Estática

CC3084 Data Science, Universidad del Valle de Guatemala, Semestre II 2026.

Fernando Rueda - 23748
Fernando Hernández - 23645

Infografía de una página que sintetiza, para un directivo de INGUAT, los
hallazgos del Laboratorio 1 (series de tiempo del flujo migratorio 2009–2026)
y documento que explica las decisiones de diseño detrás de ella.

> Los datos se comparten con fines estrictamente académicos. Este repositorio
> debe mantenerse privado.

## Estructura

```
lab9-ds/
├── data/raw/              # series del Lab 1 (mensuales, train y test), no se modifican
├── src/                   # scripts que calculan las cifras de la infografía
├── outputs/               # tablas y figuras generadas por los scripts
└── docs/explicacion/      # documento de explicación en LaTeX
    ├── main.tex
    └── secciones/
```

| Archivo | Responsable | Contenido |
|---------|-------------|-----------|
| `src/metricas_estacionalidad_pandemia.py` | Hernández | Fuerza estacional, perfil mensual y caída por pandemia de las 7 series |
| `src/metricas_tendencia_volatilidad.py` | Rueda | Crecimiento y volatilidad de las 7 series |
| `docs/explicacion/secciones/01–03` | Hernández | Introducción, recorrido visual, bloques 1–3 |
| `docs/explicacion/secciones/04–05` | Rueda | Paleta y tipografía, bloques 4–5 |
| `docs/explicacion/secciones/06` | Ambos | Cuadrante comparativo |

## Cómo correrlo

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Cada script de `src/` se corre desde la raíz del repo, por ejemplo
`python src/metricas_estacionalidad_pandemia.py`, y escribe en `outputs/`.

El documento se compila desde `docs/explicacion/`:

```bash
cd docs/explicacion && pdflatex main.tex && pdflatex main.tex
```
