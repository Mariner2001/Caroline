# Reconstrucción cuantitativa de la ventana crítica en una desaparición no resuelta

Análisis espaciotemporal, de posicionamiento celular y de teoría de búsqueda
aplicado a un caso abierto. **Sabadell (Barcelona), 15 de marzo de 2015.**

---

## Qué es esto

Un análisis cuantitativo de tres afirmaciones que circulan públicamente sobre la
ventana crítica del caso, más tres análisis que la discusión pública no ha
abordado. No propone una reconstrucción de los hechos ni atribuye
responsabilidades: calcula qué se sigue, y con qué incertidumbre, de la geometría
del terreno y de la física de la propagación radioeléctrica.

**Todo resultado está diseñado para ser falsable mediante un dato concreto e
identificado.** El apartado *Prioridades de verificación* del paper enumera qué
comprobar y en qué orden.

## Resultados principales

| # | Resultado | Cifra |
|---|---|---|
| 1 | El trayecto crítico exige un cuarto de la marcha normal; viable a pie en el 100 % de 4×10⁵ realizaciones | 719 m, 0,29 m/s |
| 2 | Queda tiempo sin explicar por el desplazamiento | **42,7 min** (IC₉₀ 26–62) |
| 3 | La ambigüedad posicional dominante es ambiental, no instrumental | razón 5,34 vs 1,67 |
| 4 | Un terminal **inmóvil** produce la cifra de velocidad que se cita como prueba de vehículo | mediana **80,0 km/h** con registros a 60 s |
| 5 | Test de retornos en la secuencia de celdas: discrimina desplazamiento de oscilación | Λ ≈ 40 (8 registros) |
| 6 | El corredor fluvial relevante es el **Riu Sec**, no el Ripoll | 839 m vs 2266 m del ancla |
| 7 | Margen ferroviario máximo compatible con una cadena declarada | 8,4 min |

## Estructura

```
.
├── paper/
│   ├── paper.tex           documento principal
│   ├── paper.pdf           compilado (16 pp.)
│   └── figures/            las 6 figuras (generadas por code/)
├── code/
│   ├── 01_temporal_cellular.py    Monte Carlo temporal + simulación celular
│   ├── 02_geospatial.py           geodésica, hidrografía, búsqueda bayesiana
│   ├── 03_handover_test.py        test Hα/Hβ de conmutación
│   └── requirements.txt

└── data/
    ├── coordinates.csv     coordenadas de entrada con fuente
    └── parameters.md       procedencia de cada parámetro
```

## Reproducción

```bash
pip install -r code/requirements.txt

python code/01_temporal_cellular.py    # ~2 min
python code/02_geospatial.py           # ~10 min
python code/03_handover_test.py        # ~1 min

cd paper && for i in 1 2 3; do pdflatex -interaction=nonstopmode paper.tex; done
```

Las tres pasadas de `pdflatex` resuelven referencias cruzadas. Semilla fija
`20150315` en los tres scripts: los números son deterministas.

Los scripts escriben las figuras en el directorio desde el que se ejecutan. Si
los lanzas desde la raíz, muévelas después:

```bash
mv fig*.pdf paper/figures/
```

**Ninguna cifra del `.tex` está escrita a mano.** Todas proceden de la salida de
consola de los scripts.

Requisitos: Python ≥ 3.10 (`numpy`, `scipy`, `matplotlib`) y una distribución
LaTeX con `tikz`, `booktabs`, `tcolorbox`, `amsmath`.

## Qué cambiaría con datos del expediente

Ordenado por rendimiento sobre coste. Los cinco primeros son de coste
esencialmente nulo para quien tenga acceso.

1. **Secuencia ordenada de Cell IDs.** Habilita el test Hα/Hβ sin necesidad de
   coordenadas, azimuts ni potencias. Máximo rendimiento por unidad de
   información requerida.
2. **Marcas temporales exactas de los registros.** Decide por completo el
   Resultado 4: con intervalos de 60 s la inferencia de velocidad carece de
   fundamento; con intervalos de 10 min lo tendría.
3. **Existencia de *timing advance*.** Reduciría la ambigüedad posicional de
   razón 5 a anillos de ≈550 m (GSM) o ≈78 m (LTE).
4. **Naturaleza de la última llamada:** atendida o no. Reordena la estructura
   temporal completa.
5. **Constancia documental de batidas sobre el corredor del Riu Sec.** El modelo
   lo sitúa como objetivo de mayor rendimiento marginal, pero presupone que no
   ha sido inspeccionado.
6. **Horario de la línea R4 del 15/03/2015.** Resuelve el Resultado 7 de forma
   binaria.

## Limitaciones

Trabajo realizado **sin acceso al expediente**. Los anclajes temporales proceden
de fuentes secundarias y son el supuesto más frágil. La configuración real de la
red celular de 2015 es desconocida: la simulación emplea retícula regular y
parámetros estándar, y sus resultados son órdenes de magnitud del sesgo, no
reconstrucción de registros concretos. Los cauces se aproximan por polilíneas de
puntos confirmados; las distancias reportadas son **cotas superiores** del
acercamiento real. Véase §10 del paper para el detalle completo.

El apéndice A documenta seis modelos descartados por refutación interna. Se
incluyen deliberadamente: un resultado negativo que elimina una fuente de error
tiene valor y evita que el mismo error reaparezca.

## Alcance y consideraciones éticas

Este trabajo analiza magnitudes físicas y temporales. **No atribuye
participación, conocimiento ni responsabilidad a persona alguna, ni asigna
probabilidades a hipótesis sobre personas concretas.**

No se nombra a ninguna de las personas presentes aquella noche. Todas eran
menores de edad en 2015, ninguna ha sido acusada formalmente, y les amparan la
presunción de inocencia (art. 24.2 CE) y el derecho al honor (art. 18.1 CE).

La omisión no es solo cautelar sino metodológica: calcular P(implicación |
evidencia) exige la verosimilitud P(evidencia | no implicado) — la frecuencia con
que una persona no implicada produciría la misma evidencia — que en este contexto
es alta y no estimable con los datos disponibles. Omitirla es la falacia del
fiscal. El apéndice A.6 lo desarrolla.

**Si reutilizas este material, mantén esa línea.** Añadir nombres a estos
cálculos no los hace más informativos; los hace jurídicamente peligrosos y
metodológicamente falsos.

## Cómo contribuir

Lo más útil no son más hipótesis, sino cerrar las comprobaciones de la lista de
arriba. Si tienes acceso a alguno de esos datos, o detectas un error en los
cálculos, abre un *issue*.

Los scripts son deterministas: cualquier discrepancia numérica es reproducible y
por tanto discutible.

## Licencia

Se sugiere CC BY 4.0 para el texto y MIT para el código. Añade los ficheros
`LICENSE` correspondientes antes de publicar.
