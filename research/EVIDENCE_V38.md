<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V38 — Decoder cross-history ciego a amplitud

## Estado

**OFICIAL — señal débil, no concluyente.**

V38 repite el decoder cross-history de V37, pero normaliza cada trayectoria futura por su norma L2 antes de extraer las 12 características. El objetivo es eliminar información de escala global de la trayectoria.

History-seeds 130–139; ángulos 0°, 30° y 150°; nueve contextos memory×pressure; input futuro exactamente cero.

## Resultado

| Ángulo | Accuracy media | SD | Log-loss medio |
|---:|---:|---:|---:|
| 0° | 50.16% | 3.20 pp | 0.7175 |
| 30° | **61.41%** | 4.14 pp | 0.6587 |
| 150° | 58.44% | 1.73 pp | 0.6499 |

Contraste 30°−150°:

- **+2.97 puntos porcentuales**
- null 95%: **+2.69 pp**
- sign-flip p: **0.03135**

## Lectura

Después de eliminar la escala L2 global, la diferencia 30°−150° vuelve a ser positiva. Sin embargo, el tamaño del contraste es pequeño y el resultado es mucho menos fuerte que V34–V36.

Por eso, V38 debe interpretarse como **señal compatible con una componente de forma/orientación que puede sobrevivir a la normalización de amplitud**, no como confirmación independiente fuerte.

La comparación con V37 es importante: ambos pertenecen a la familia reference-free cross-history, pero producen direcciones diferentes bajo dos representaciones. Esto muestra que la sensibilidad del readout sigue siendo una variable crítica.

## Reproducibilidad

Run: **36791533212**

Artifact: **11131543460**

Código: **748d1b9ef4d070f721b0c6252226e97afd0fc89e**

Interpretación restringida al sistema computacional; no demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V38 — Amplitude-Blind Cross-History Decoder

## Estado

**OFICIAL — señal débil, no concluyente.**

V38 repite el decoder cross-history de V37, pero normaliza cada trayectoria futura por su norma L2 antes de extraer las 12 características. La intención es eliminar información de escala global de la trayectoria.

Historia-seeds 130–139; ángulos 0°, 30° y 150°; nueve contextos memoria×presión; entrada futura exactamente cero.

## Resultado

| Ángulo | Accuracy media | SD | Log-loss medio |
|---:|---:|---:|---:|
| 0° | 50.16% | 3.20 pp | 0.7175 |
| 30° | **61.41%** | 4.14 pp | 0.6587 |
| 150° | 58.44% | 1.73 pp | 0.6499 |

Contraste 30°−150°:

- **+2.97 puntos porcentuales**
- null 95%: **+2.69 pp**
- sign-flip p: **0.03135**

## Lectura

Después de eliminar la escala L2 global, la diferencia 30°−150° vuelve a ser positiva. Sin embargo, el tamaño del contraste es pequeño y el resultado es mucho menos fuerte que V34–V36.

Por ello, V38 debe interpretarse como **señal compatible con una componente de forma/orientación que puede sobrevivir a la normalización de amplitud**, no como confirmación independiente fuerte del fenómeno.

La comparación con V37 es especialmente importante: V37 y V38 comparten la familia reference-free cross-history, pero producen direcciones diferentes bajo dos representaciones. Esto indica que la sensibilidad del readout sigue siendo una variable crítica.

## Reproducibilidad

Run: **36791533212**

Artifact: **11131543460**

Código: **748d1b9ef4d070f721b0c6252226e97afd0fc89e**

Interpretación restringida al sistema computacional; no demuestra conciencia ni experiencia subjetiva.
