<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V37 — Decoder cross-history sin referencia

## Estado

**OFICIAL — resultado negativo para la hipótesis angular prevista.**

V37 elimina las referencias A/B construidas dentro de cada historia de prueba. Un decoder logístico se entrena con nueve history-seeds y se evalúa sobre la décima, utilizando únicamente 12 estadísticas de la trayectoria futura.

El protocolo usa history-seeds 120–129, seis puntos paramétricos, cuatro pares históricos, nueve contextos memory×pressure, ángulos 0°, 30° y 150°, radio 1.1 e input futuro exactamente cero.

## Resultado

| Ángulo | Accuracy media | SD | Log-loss medio |
|---:|---:|---:|---:|
| 0° | 49.54% | 4.26 pp | 0.7216 |
| 30° | 60.20% | 1.97 pp | 0.6612 |
| 150° | **65.35%** | 4.04 pp | **0.6236** |

La diferencia preespecificada 30°−150° fue **−5.15 puntos porcentuales**, con null 95% de **+3.36 pp** y sign-flip p = **0.9962**.

En los diez history-seeds individuales, la diferencia 30°−150° fue negativa en 9 de 10 casos.

## Lectura

El resultado **no replica** la dirección angular observada en los experimentos basados en referencias de continuación. Bajo este decoder reference-free, 150° presenta mayor discriminabilidad media que 30°.

Es un resultado negativo importante: indica que la propiedad detectada en V33–V36 **no puede describirse todavía como una invariancia general de la trayectoria independiente del esquema de lectura**.

Esto tampoco demuestra que la geometría previa sea un artefacto: se prueba una construcción estadística diferente y cambia simultáneamente la forma de medición y representación. Sí elimina una afirmación más fuerte de robustez universal.

## Reproducibilidad

Run: **36791463538**

Artifact: **11131689476**

Código: **f5401842b89e499759c6e145778367fde976ee8e**

Conclusión metodológica: mantener V37 como **control negativo/limitación explícita**.

</details>

<a id="english"></a>

# V37 — Reference-Free Cross-History Decoder

## Estado

**OFICIAL — resultado negativo para la hipótesis angular prevista.**

V37 elimina las referencias A/B construidas dentro de cada historia de prueba. Un decoder logístico se entrena con nueve history-seeds y se evalúa sobre la décima, utilizando únicamente 12 estadísticas de la trayectoria futura.

El protocolo usa historia-seeds 120–129, seis puntos paramétricos, cuatro pares históricos, nueve contextos memoria×presión, ángulos 0°, 30° y 150°, radio 1.1 y entrada futura exactamente cero.

## Resultado

| Ángulo | Accuracy media | SD | Log-loss medio |
|---:|---:|---:|---:|
| 0° | 49.54% | 4.26 pp | 0.7216 |
| 30° | 60.20% | 1.97 pp | 0.6612 |
| 150° | **65.35%** | 4.04 pp | **0.6236** |

La diferencia preespecificada 30°−150° fue:

- **−5.15 puntos porcentuales**
- null 95%: **+3.36 pp**
- sign-flip p: **0.9962**

Por los diez history-seeds individuales, la diferencia 30°−150° fue negativa en 9 de 10 casos.

## Lectura

El resultado **no replica** la dirección angular observada en los experimentos basados en referencias de continuación. Bajo este decoder reference-free, 150° presenta mayor discriminabilidad media que 30°.

Esto es un resultado negativo importante: indica que la propiedad detectada en V33–V36 **no puede describirse todavía como una invariancia general de la trayectoria independiente del esquema de lectura**.

El resultado tampoco demuestra que la geometría previa sea un artefacto: prueba una construcción estadística diferente y cambia simultáneamente la forma de medición y la representación del resultado. Pero sí elimina una afirmación más fuerte de robustez universal.

## Reproducibilidad

Run: **36791463538**

Artifact: **11131689476**

Código: **f5401842b89e499759c6e145778367fde976ee8e**

Conclusión metodológica: mantener V37 como **control negativo/limitación explícita**.
