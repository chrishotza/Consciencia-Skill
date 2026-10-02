<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V46 — Generalización de historia entre sondas

V46 prueba si la información de historia temporal retenida por el sistema sigue siendo accesible cuando cambia el estímulo externo posterior.

Hay tres sondas deterministas (A, B, C). Para cada punto paramétrico reservado y sonda reservada, el clasificador se entrena con los otros cinco puntos y las otras dos sondas, y luego predice la clase histórica a partir de la **trayectoria futura del state solamente** bajo la sonda no vista.

No se proporciona al clasificador trayectoria de referencia, transformación angular ni feature actual de memory/pressure.

La accuracy de azar es 25%. El resultado se evalúa en los 18 folds parámetro×sonda.

Esto es un test de generalización de tarea/contexto para acceso a historia interna. No establece consciencia, experiencia subjetiva, sentiencia ni awareness fenomenológico.

</details>

<a id="english"></a>

# V46 — Cross-Probe History Generalization

V46 tests whether temporal-history information retained by the system remains accessible when the subsequent external stimulus changes.

There are three deterministic probes (A, B, C). For each held-out parameter point and held-out probe, the classifier trains on the other five parameter points and the other two probes, then predicts the history class from the future **state trajectory only** under the unseen probe.

No reference trajectory, angular transform, or current memory/pressure feature is provided to the classifier.

Chance accuracy is 25%. The result is evaluated across all 18 parameter×probe folds.

This is a task/context generalization test for internal history access. It does not establish consciousness, subjective experience, sentience, or phenomenological awareness.
