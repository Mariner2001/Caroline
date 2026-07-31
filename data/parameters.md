# Procedencia de los parámetros

Proyección local métrica centrada en ZH (41,5336445 N; 2,0998452 E).
Constantes: 111 320 m/grado de latitud; 111 320·cos(41,5336°) m/grado de longitud.

## Cinemática peatonal

| Parámetro | Valor | Origen |
|---|---|---|
| Velocidad de marcha | logN(1,35 ; 0,22) m/s | Bohannon (1997) |
| Factor de rodeo κ | U(1,15 ; 1,45) | rango urbano europeo estándar |
| v₀ esprint | 4,5 m/s | estimación; barrido 4,0–5,0 |
| γ fatiga | 1/45 s⁻¹ | estimación |
| v_w asintótica | 1,35 m/s | igual a marcha normal |

## Propagación radioeléctrica

| Parámetro | Valor | Origen |
|---|---|---|
| Pérdidas (simulación) | 128,1 + 37,6·log₁₀(d[km]) dB | 3GPP TR 36.814 |
| Patrón de antena | −mín[12(θ/65°)², 20] dB | 3GPP TR 36.814 |
| Okumura-Hata η | 44,9 − 6,55·log₁₀(h_b) = 35,74 | Hata (1980), h_b = 25 m |
| Sombreado σ | 8 dB (barrido 4–10) | valor típico urbano |
| Decorrelación de sombra | 25 m | valor típico urbano |
| Histéresis de traspaso | 3 dB | valor típico de red |

## Anclajes temporales — **supuesto más frágil del trabajo**

| Parámetro | Valor | Origen |
|---|---|---|
| t₃ (dispersión) | Triangular(04:30; 05:00; 05:15) | **fuente secundaria (T5)** |
| t₄ (llamada) | mezcla 05:45 / 05:55 + jitter 50 s | **fuente secundaria (T5)** |

Deben sustituirse por el dato del expediente. Si los soportes reales difieren,
los resultados de §3 cambian, aunque la estructura cualitativa (holgura amplia,
trayecto holgadamente viable) es estable para cualquier soporte compatible con lo
publicado.

## Búsqueda bayesiana

| Parámetro | Valor | Origen |
|---|---|---|
| λ trama urbana | 2,19 | estimación por tipo de terreno |
| λ corredor Riu Sec | 1,28 | estimación por tipo de terreno |
| λ corredor Ripoll | 1,05 | estimación por tipo de terreno |
| Peso fase A (w_A) | 0,50 (barrido 0,35–0,65) | elección de modelo |
| Paso de retícula | 50 m | — |
| Esfuerzo z por batida | 0,8–1,2 | estimación |

## Test de conmutación Hα/Hβ

| Parámetro | Valor | Origen |
|---|---|---|
| P(avance) bajo Hα | 0,75 | modelo generativo simplificado |
| Nº de celdas bajo Hβ | 3 | modelo generativo simplificado |
| Realizaciones | 2×10⁴ por condición | — |

Requieren recalibración con la topología real de la red. El orden de magnitud de
la discriminación y el sentido del test no dependen de estos valores.

## Escenario vehicular

| Parámetro | Valor | Origen |
|---|---|---|
| Salida | U(05:55 ; 06:25) | derivado de los anclajes |
| Velocidad de circulación | N(112, 14) km/h truncada [70,150] | tráfico nocturno en autopista |
| Sobrecoste incorporación/peajes | Exp(media 4 min) | estimación |
| Distancia a frontera | 152 km | por AP-7 |
