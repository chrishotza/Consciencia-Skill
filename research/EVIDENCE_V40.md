<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V40 — Evidencia con referencia cross-history

## Estado

**OFICIAL — GitHub Actions run 36793198235.**

V40 conserva el readout reference-based de V34–V36, pero construye las referencias A/B a partir de un history-seed distinto de las trayectorias de prueba.

Seeds de test: 150–159.  
Seeds de referencia: 180–189.  
Los dos conjuntos son disjuntos.

## Resultado primario

| Métrica | Resultado |
|---|---:|
| Contraste 30°−150° | **0.3052216721** |
| Null estratificado, media | -0.0001170007 |
| Null 95% | 0.0881044933 |
| Permutation p | **0.00005** |
| Bootstrap 95% | **[0.2807917046, 0.3292164138]** |
| Bloques history-seed | 40 |
| Estratos históricos | 4 |

Los nueve contextos memory×pressure mantuvieron contraste positivo:

- memoria -0.8: 0.1556 / 0.1276 / 0.1057
- memoria 0.0: 0.5011 / 0.5434 / 0.4338
- memoria +0.8: 0.3035 / 0.2970 / 0.2793

## Qué descarta

V40 muestra que el efecto no requiere que las referencias A/B hayan sido generadas desde la **misma history-seed concreta** que las trayectorias de prueba.

Esto debilita una explicación de “matching exacto de historia” como causa suficiente.

## Qué todavía no descarta

Las referencias y las pruebas siguen compartiendo el mismo **tipo de history-pair**. Por eso V40 todavía no demuestra transferencia entre regímenes históricos diferentes.

El siguiente control es V41: referencia cruzada entre tipos de historia, manteniendo seeds completamente disjuntas.

## Lectura

El resultado refuerza una interpretación de estructura dinámica/geométrica dependiente del readout reference-based, pero no demuestra una propiedad universal del sistema ni consciencia, experiencia subjetiva o sentiencia.

## Reproducibilidad

Run: **36793198235**

Artifact: **11132736775**

Workflow commit: **a2e44f95e8d74a3b6bf4e8da477c0a9931c9a885**

Código: **0e67773d1e816897885dd2a934727e431010c6d4**

</details>

<a id="english"></a>

# V40 — Cross-History Reference Evidence

## Estado

**OFICIAL — GitHub Actions run 36793198235.**

V40 mantuvo el readout reference-based de V34–V36, pero construyó las referencias A/B a partir de una historia-seed distinta de la utilizada por las trayectorias de prueba.

Test history seeds: 150–159.  
Reference history seeds: 180–189.  
Los dos conjuntos son disjuntos.

## Resultado primario

| Métrica | Resultado |
|---|---:|
| Contraste 30°−150° | **0.3052216721** |
| Null estratificado, media | -0.0001170007 |
| Null 95% | 0.0881044933 |
| Permutation p | **0.00005** |
| Bootstrap 95% | **[0.2807917046, 0.3292164138]** |
| Bloques history-seed | 40 |
| Estratos históricos | 4 |

Los nueve contextos memoria×presión mantuvieron contraste positivo:

- memoria −0.8: 0.1556 / 0.1276 / 0.1057
- memoria 0.0: 0.5011 / 0.5434 / 0.4338
- memoria +0.8: 0.3035 / 0.2970 / 0.2793

## Qué descarta

V40 muestra que el efecto no requiere que las referencias A/B hayan sido generadas desde la **misma historia-seed concreta** que las trayectorias de prueba.

Esto debilita una explicación de “matching exacto de historia” como causa suficiente.

## Qué todavía NO descarta

Las referencias y las pruebas siguen compartiendo el mismo **tipo de historia-pair**. Por ello V40 todavía no demuestra transferencia entre regímenes históricos diferentes.

El siguiente control es V41: referencia cruzada entre tipos de historia, manteniendo semillas completamente disjuntas.

## Lectura

El resultado refuerza una interpretación de estructura dinámica/geométrica dependiente del readout reference-based, pero no demuestra una propiedad universal del sistema ni conciencia, experiencia subjetiva o sentiencia.

## Reproducibilidad

Run: **36793198235**

Artifact: **11132736775**

Workflow commit: **a2e44f95e8d74a3b6bf4e8da477c0a9931c9a885**

Código: **0e67773d1e816897885dd2a934727e431010c6d4**
