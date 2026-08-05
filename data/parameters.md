# Inventario de parámetros del modelo

Material complementario del manuscrito *Auditoría cuantitativa de inferencias en un caso
de desaparición no resuelto: Sabadell (Barcelona), 15 de marzo de 2015*.

Este documento cumple el compromiso declarado en §10 del manuscrito: listar **todos** los
parámetros libres del conjunto de análisis, su origen, su valor y si se ha reportado
barrido de sensibilidad.

**Resumen:** 28 parámetros libres · 18 son estimaciones no medidas · 12 carecen de
barrido de sensibilidad · cobertura del 57 %.

---

## Convenciones

**Origen**

| Etiqueta | Significado |
|---|---|
| `literatura` | Valor tomado de fuente publicada y citada en el manuscrito |
| `estimación` | Valor asignado por el autor, sin medición ni fuente |
| `prensa` | Derivado de fuentes secundarias sobre el caso (nivel T₅) |
| `derivado` | Se deduce de otros parámetros, no es libre en sentido estricto |
| `técnico` | Elección de implementación (resolución, extensión de retícula) |

**Barrido**

| Etiqueta | Significado |
|---|---|
| `sí` | Se reporta rango de valores y su efecto sobre el resultado |
| `parcial` | Se exploran algunas alternativas, no un rango sistemático |
| `declarado` | No hay barrido, pero el efecto se discute y se acota en el texto |
| `no` | Valor fijo, sin exploración ni discusión cuantitativa del efecto |

---

## Inventario

### Cinemática peatonal (§3, §6, §7)

| # | Parámetro | Valor | Origen | Barrido | Dónde |
|---|---|---|---|---|---|
| 1 | Velocidad de marcha `V` | logN(1,35 ; 0,22) m/s | literatura (Bohannon 1997) | sí | Tabla §3.4 |
| 2 | Factor de rodeo `κ` | U(1,15 ; 1,45) | estimación | sí | Tabla §3.4 |
| 3 | Instante de dispersión `t₃` | Triangular(04:30; 05:00; 05:15) | prensa | sí | Tabla §3.4 |
| 4 | Instante de llamada `t₄` | mezcla 05:45/05:55 + jitter N(0,50 s) | prensa | parcial | Tabla §3.4 |
| 5 | Velocidad inicial de esprint `v₀` | 4,5 m/s | estimación | **no** | — |
| 6 | Coeficiente de fatiga `γ` | 1/45 s⁻¹ | estimación | **no** | — |
| 7 | Duración de la fase de esprint | 120 s | estimación | **no** | — |

### Propagación y red celular (§4, §5)

| # | Parámetro | Valor | Origen | Barrido | Dónde |
|---|---|---|---|---|---|
| 8 | Pérdidas de propagación | 128,1 + 37,6·log₁₀ d[km] dB | literatura (3GPP TR 36.814) | declarado | §4.2 |
| 9 | Patrón de antena sectorial | −mín[12(θ/65°)², 20] dB | literatura (3GPP TR 36.814) | **no** | — |
| 10 | Altura de estación base `h_b` | 25 m | estimación | declarado | §4.2 |
| 11 | Distancia entre sitios (ISD) | 800 m | estimación | sí | Tabla §5.1 |
| 12 | Desviación de sombreado `σ` | 8 dB | literatura | sí | Tabla §5.1(b) |
| 13 | Decorrelación de sombreado | 25 m | literatura | **no** | — |
| 14 | Histéresis de traspaso | 3 dB | literatura | **no** | — |
| 15 | Intervalo entre registros `E[Δt]` | 180 s | estimación | sí | Tabla §5.1(a) |
| 16 | Desplazamiento residual del terminal | 0–150 m | estimación | sí | Tabla §5.1 |
| 17 | Velocidad del vehículo (cálculo LR) | 100 km/h, rumbo constante | estimación | **no** | declarado como idealización, §5.3 |
| 18 | Probabilidad de rebote `p_reb` | 0,10 | estimación | sí | Tabla §5.4 |
| 19 | Nº de celdas en solapamiento bajo H_β | 3 | estimación | parcial | §5.4 (advertencia) |

### Modelo espacial y búsqueda (§6)

| # | Parámetro | Valor | Origen | Barrido | Dónde |
|---|---|---|---|---|---|
| 20 | Detectabilidad `λ` por terreno | 1,05 / 1,28 / 2,19 | estimación | sí | Tabla §6.6 |
| 21 | Esfuerzo `z` por batida | 1,2 / 1,0 / 0,8 | estimación | **no** | — |
| 22 | Peso de la fase A `w_A` | 0,50 | estimación | sí | §6.6 (0,20–0,80) |
| 23 | Escala de difusión de la fase B | 1,15 m/s × holgura / 3 | estimación | **no** | — |
| 24 | Radio de la retícula | 3 km | técnico | declarado | §6.3 (truncamiento) |

### Escenario vehicular (§8)

| # | Parámetro | Valor | Origen | Barrido | Dónde |
|---|---|---|---|---|---|
| 25 | Ventana de salida | U(05:55 ; 06:25) | derivado | declarado | §8.1 |
| 26 | Velocidad de circulación | N(112, 14) km/h trunc. [70,150] | estimación | **no** | — |
| 27 | Sobrecoste de incorporación y peajes | Exp(media 4 min) | estimación | **no** | — |
| 28 | Distancia por AP-7 | 146 km | estimación | **no** | — |

> **Recuento.** El inventario lista **28 parámetros libres**: 18 estimaciones no
> medidas, 6 valores de literatura, 2 derivados de fuentes secundarias sobre el caso, 1
> elección técnica y 1 derivado de otros. **12 carecen de barrido de sensibilidad**, lo
> que sitúa la cobertura en el 57 %.
>
> Estas cifras son las autoritativas y sustituyen a cualquier recuento anterior: una
> versión previa omitía los tres parámetros de propagación (entradas 8, 9 y 10), que sí
> son libres aunque dos de ellos procedan de literatura.

---

## Qué resultado depende de qué

| Resultado | Parámetros que lo determinan | ¿Todos con barrido? |
|---|---|---|
| 1 — Trayecto viable, holgura de 42,7 min | 1, 2, 3, 4 | sí (4 parcial) |
| 2 — Ambigüedad de razón 5,48 | 8, 10, 12 | parcialmente |
| 3 — TA de GSM aporta 1,0–2,7× | 8, 10, 11, 12 | parcialmente |
| 4 — LR de la cifra de 80 km/h = 2,9 | 11–17 | **no**: 13, 14 y 17 sin barrido |
| 5 — Test de retornos, Λ ≈ 22 | 18, 19 | parcialmente |
| 6 — Las barreras apenas alteran la métrica | 24 | declarado |
| 7 — El corredor relevante es el Riu Sec | 20, 22, 23, 24 | **no**: 23 sin barrido |
| 8 — Margen ferroviario de 8,4 min | 1, 2 | sí |

### Advertencia sobre el alcance de esta cobertura

El manuscrito afirma en §10 que *«los resultados sobre los que se apoya la discusión
corresponden mayoritariamente a los parámetros con barrido reportado»*. La tabla
anterior precisa ese *mayoritariamente*:

- El **Resultado 4** depende de la decorrelación de sombreado (13), la histéresis (14) y
  el modelo de vehículo (17), ninguno con barrido. Los dos primeros son valores
  estándar de literatura; el tercero está declarado explícitamente como idealización en
  §5.3, y su efecto conocido —hacer del 2,9 una cota superior— se reporta.
- El **Resultado 7** depende de la escala de difusión de la fase B (23), sin barrido.
  Su efecto se solapa parcialmente con el de `w_A` (22), que sí lo tiene.

Ninguno de estos parámetros sin barrido invierte el signo de los resultados en las
comprobaciones puntuales realizadas, pero **la cobertura de sensibilidad no es completa**
y esta es la formulación exacta de esa limitación.

---

## Coordenadas de entrada

Proyección local métrica centrada en el punto de dispersión. Constantes empleadas:
111 320 m/grado de latitud y 111 320·cos(41,5336°) m/grado de longitud (aproximación
esférica; véase §2.2 para la discrepancia frente a los valores elipsoidales).

| ID | Descripción | Latitud | Longitud |
|---|---|---|---|
| ZH | Zona de ocio (punto de dispersión) | 41,5336445 | 2,0998452 |
| SUD | Estación Sabadell Sud (última llamada) | 41,5287051 | 2,1054052 |
| FEU | Castell de Can Feu | 41,5393237 | 2,0936818 |
| CEN | Estación Sabadell Centre | 41,5464246 | 2,1156055 |
| NOR | Estación Sabadell Nord | 41,5619458 | 2,0962433 |
| SEC1 | Riu Sec — Sant Quirze del Vallès | 41,5261315 | 2,0894665 |
| SEC2 | Riu Sec — Barberà del Vallès | 41,5167637 | 2,1151786 |
| SEC3 | Riu Sec — Cerdanyola | 41,5010170 | 2,1284971 |
| SEC4 | Riu Sec — Cerdanyola (Acàcies) | 41,4920899 | 2,1441170 |
| RIP1 | Ripoll — parc fluvial (N) | 41,5623380 | 2,1093770 |
| RIP2 | Ripoll — Pont de la Salut | 41,5564364 | 2,1169399 |
| RIP3 | Ripoll — tramo SE | 41,5436708 | 2,1257046 |

El Riu Sec se modela como polilínea de los cuatro puntos confirmados. El Ripoll, como
polilínea de tres puntos confirmados más una prolongación recta de 2 200 m aguas abajo.
La traza ferroviaria R4 se aproxima por el segmento SUD–NOR.

**Sustituir por cartografía hidrográfica y viaria oficial (ICGC) refinaría el modelo
espacial sin alterar el sentido de los resultados** (§10).

---

## Qué cambiaría con datos del expediente

Ordenado por rendimiento esperado, siguiendo §9.1 del manuscrito.

| # | Dato | Sustituiría a | Efecto |
|---|---|---|---|
| 0 | Procedencia de los registros de red | — | **Condiciona 1–3**: sin registros primarios, esas peticiones carecen de objeto |
| 1 | Secuencia ordenada de Cell ID | Parámetros 18, 19 | Ejecuta el test del Resultado 5 sobre dato real |
| 2 | Marcas temporales de registro | Parámetro 15 | Decide el Resultado 4 |
| 3 | Campos del CDR (RTT / potencia / TA) | Supuesto de §4.1 | Valida o invalida toda la §4.2 |
| 4 | Naturaleza de la última llamada | Parámetro 4 | Reordena la estructura temporal |
| 5 | Método y extensión de las batidas | Parámetros 20, 21 | Convierte el Resultado 7 de indicativo en cuantitativo |
| 6 | Hora exacta de la actuación policial | Parámetro 3 | Único supuesto capaz de invalidar el Resultado 1 |
| 7 | Cadena declarada completa + horario R4 | Entradas de §7.3 | Resuelve el Resultado 8 de forma binaria |
| — | Coordenadas y azimuts de las BTS de 2015 | Parámetros 9, 11 | Sustituye la retícula hexagonal por geometría real |
| — | Cartografía ICGC | Polilíneas de cauces | Refina el modelo espacial |

---

## Reproducibilidad

Todos los resultados numéricos y todas las figuras proceden de los scripts de `code/`
con semilla fija `20150315`. Ninguna cifra del manuscrito se ha introducido a mano.

Los valores de este inventario son los efectivamente empleados en el código; cualquier
discrepancia entre esta tabla y los scripts debe resolverse a favor de los scripts, y
comunicarse como incidencia.
