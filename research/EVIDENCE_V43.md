<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V43 — Registro de evidencia

Ejecución oficial de GitHub Actions completada correctamente el 1 de octubre de 2026.

Run: 36795357386  
Artifact: 11133184914  
Commit: 78822a6bc45f7af1e154d0c14ca2de251856ec1e

## Resultado

V43 elimina por completo el readout basado en referencias de V34–V42. Después de presentar un template histórico, el input futuro se fija exactamente en cero durante 60 pasos. Un clasificador identifica entonces el template histórico a partir únicamente de la continuación interna.

Accuracy media leave-one-parameter-out, chance = 25%:

| Feature set | LOPO accuracy |
| --- | ---: |
| State trajectory | 79.08% |
| L2-normalized state | 78.25% |
| Memory trajectory | 93.75% |
| Pressure trajectory | 87.50% |
| Joint normalized state+memory+pressure | 89.25% |

Para el readout conjunto normalizado, el null por permutación de etiquetas con 5,000 muestras tuvo media 24.996%, percentil 95 de 26.917% y p = 0.00020.

## Interpretación

Es un resultado genuino de retención de historia **sin referencia**: después de retirar el input externo, la dinámica interna futura conserva suficiente información para recuperar cuál de cuatro historias temporales distintas generó el contexto actual, incluso en puntos paramétricos reservados.

El canal individual más fuerte es memory. State y pressure también contienen información sustancial. Por tanto, V43 respalda codificación interna persistente y distribuida de la historia temporal, en lugar de un efecto geométrico definido únicamente por referencias.

No establece consciencia, experiencia subjetiva, sentiencia ni awareness fenomenológico. En particular, alta decodificabilidad de la historia es evidencia de retención y accesibilidad de información, no de experiencia por sí misma.

</details>

<a id="english"></a>

# V43 — Evidence Record

Official GitHub Actions execution completed successfully on 2026-10-01.

Run: 36795357386  
Artifact: 11133184914  
Commit: 78822a6bc45f7af1e154d0c14ca2de251856ec1e

## Result

V43 removed the V34–V42 reference-based readout entirely. After a history template was presented, future input was set exactly to zero for 60 steps. A classifier then identified the historical template from internal continuation alone.

Leave-one-parameter-out mean accuracy, chance = 25%:

| Feature set | LOPO accuracy |
| --- | ---: |
| State trajectory | 79.08% |
| L2-normalized state | 78.25% |
| Memory trajectory | 93.75% |
| Pressure trajectory | 87.50% |
| Joint normalized state+memory+pressure | 89.25% |

For the joint normalized readout, a 5,000-sample label-permutation null had mean 24.996%, 95th percentile 26.917%, and p = 0.00020.

## Interpretation

This is a genuine reference-free history-retention result: after external input is removed, future internal dynamics retain enough information to recover which of four distinct temporal histories generated the current context, including across held-out parameter points.

The strongest single-channel readout is memory. State and pressure also carry substantial information. Therefore V43 supports persistent, distributed internal encoding of temporal history rather than a purely reference-defined geometric effect.

It does not establish consciousness, subjective experience, sentience, or phenomenological awareness. In particular, high decodability of history is evidence for information retention and accessibility, not evidence by itself for experience.
