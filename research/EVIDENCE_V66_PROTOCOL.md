<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V66 — Consolidación DREAM después de ablación de memoria episódica

## Hipótesis

Una lección generada durante DREAM puede permanecer funcionalmente activa después de retirar las memorias episódicas crudas que la produjeron.

## Diseño

24 réplicas emparejadas.

DREAM procesa primero memorias de experiencias repetidas y escribe una lección consolidada. Luego el estado post-DREAM se clona en dos brazos:

- retained_lesson: eliminar solo los registros EXPERIENCE crudos;
- ablated_lesson: eliminar registros EXPERIENCE crudos y la lección CONSOLIDATED.

Ambos brazos ejecutan la misma sonda de recuperación y el semantic dynamic bridge antes de la selección de trayectoria futura.

## Análisis primario

Comparar regret emparejado y oracle-hit rate entre retained_lesson y ablated_lesson.

## Limitación

El provider determinista es sintético. El protocolo demuestra retención y uso causal operacional de una traza computacional consolidada, no memoria subjetiva ni consciencia.

</details>

<a id="english"></a>

# Evidence V66 — Dream consolidation after episodic-memory ablation

## Hypothesis

A DREAM-generated lesson can remain functionally active after the raw episodic
memories that produced it are removed.

## Design

24 matched replicates.

DREAM first processes repeated experience memories and writes a consolidated lesson.
Then the post-dream state is cloned into two arms:

- retained_lesson: delete raw EXPERIENCE records only;
- ablated_lesson: delete raw EXPERIENCE records and the CONSOLIDATED lesson.

Both arms run the same retrieval probe and semantic dynamic bridge before future
trajectory selection.

## Primary analysis

Compare paired regret and oracle-hit rate between retained_lesson and ablated_lesson.

## Limitation

The deterministic provider is synthetic. This protocol demonstrates operational
retention and causal use of a consolidated computational trace, not subjective
memory or consciousness.
