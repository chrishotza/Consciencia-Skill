<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# C0.16 — Organismo persistente integrado con segundo orden condicionado por acción

## Pregunta

C0.13 estableció especificidad de segundo orden condicionada por acción en un experimento controlado.

C0.14 estableció persistencia de los modelos de primer y segundo orden a través de un reinicio.

C0.16 combina esos resultados dentro del ciclo de vida real de PersistentOrganism:

persistent first-order self-model → persistent action-conditioned second-order model → autonomous selection → restart → continued selection

## Diseño

Dos brazos emparejados usan los mismos modelos seedados y el mismo dynamic seed:

- **CONTINUOUS** — 16 ciclos autónomos del organismo sin reinicio.
- **RESTART** — 8 ciclos autónomos, cierre/reapertura de SQLite, carga automática de ambos modelos persistidos y otros 8 ciclos autónomos.

No se suministra entrada semántica durante la sonda. No hay reentrenamiento externo.

## Outputs primarios

1. mismatch de acción posterior al reinicio;
2. mismatch de self-prediction-gain posterior al reinicio.

Outputs secundarios verifican recuperación exacta del digest de los modelos, coincidencia de acciones antes del reinicio y que el organismo reporte el selector action_conditioned_second_order después del reinicio.

## Interpretación

La recuperación exacta de los modelos con operación autónoma continua respalda que el mecanismo de segundo orden ya no es solo un componente de laboratorio aislado: sobrevive dentro del ciclo de vida del organismo persistente.

Sigue siendo evidencia computacional sobre organización y persistencia; no establece consciencia fenomenológica.

## Resultado verificado

GitHub Actions run **36946260825**; artifact **11201973015**; SHA256 **52e60a8bb92b0c4520e1f2cc94cd138daf81bceef9138e009b6dbee635d0833e**.

- post-restart action mismatch: **0.0**, p **1.0**
- post-restart gain mismatch: **0.0**, p **1.0**
- exact persisted model-digest recovery: **100%**
- pre-restart action match: **100%**
- todos los eventos posteriores al reinicio reportaron policy **action_conditioned_second_order**
- maximum action mismatch: **0.0**
- maximum gain mismatch: **0.0**

Interpretación: el selector de segundo orden condicionado por acción funciona ahora dentro del organismo persistente, queda almacenado en SQLite junto con el self-model de primer orden, se restaura automáticamente después del reinicio y continúa seleccionando autónomamente sin input semántico ni reentrenamiento externo.

</details>

<a id="english"></a>

# C0.16 — Integrated Persistent Action-Conditioned Second-Order Organism

## Question

C0.13 established action-conditioned second-order specificity in a controlled experiment.

C0.14 established persistence of the first- and second-order models across a restart boundary.

C0.16 combines those results inside the actual `PersistentOrganism` lifecycle:

`persistent first-order self-model → persistent action-conditioned second-order model → autonomous selection → restart → continued selection`

## Design

Two matched arms use the same seeded models and dynamic seed:

- **CONTINUOUS** — 16 autonomous organism cycles without restart.
- **RESTART** — 8 autonomous cycles, SQLite close/reopen, automatic reload of both persisted models, then 8 more autonomous cycles.

No semantic input is supplied during the probe. No external retraining occurs during the probe.

## Primary outputs

1. post-restart action mismatch;
2. post-restart self-prediction-gain mismatch.

Secondary outputs verify exact model-digest recovery, pre-restart action matching, and that the organism reports the action-conditioned second-order selector after restart.

## Interpretation

Exact model recovery with continued autonomous operation supports that the second-order mechanism is no longer only a standalone laboratory component: it survives inside the persistent organism lifecycle.

This remains computational evidence about organization and persistence; it does not establish phenomenal consciousness.


## Verified result

GitHub Actions run **36946260825**; artifact **11201973015**; SHA256 **52e60a8bb92b0c4520e1f2cc94cd138daf81bceef9138e009b6dbee635d0833e**.

- post-restart action mismatch: **0.0**, p **1.0**
- post-restart gain mismatch: **0.0**, p **1.0**
- exact persisted model-digest recovery: **100%**
- pre-restart action match: **100%**
- all post-restart events reported policy **action_conditioned_second_order**
- maximum action mismatch: **0.0**
- maximum gain mismatch: **0.0**

Interpretation: the action-conditioned second-order selector now runs inside the persistent organism, is stored in SQLite together with the first-order self-model, is automatically restored after restart, and continues autonomous selection without semantic input or external retraining.
