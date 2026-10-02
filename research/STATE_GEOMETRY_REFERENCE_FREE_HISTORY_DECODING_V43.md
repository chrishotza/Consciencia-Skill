<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V43 — Decodificación de historia temporal sin referencia

V43 elimina por completo el readout reference-based de V34–V42.

El sistema recibe uno de cuatro templates history-pair y luego el input futuro se fija exactamente en cero durante 60 pasos. Un clasificador debe identificar el template histórico a partir solamente de la continuación interna.

La evaluación primaria es leave-one-parameter-out (LOPO): cada uno de los seis puntos ciegos se reserva por turno. Para cada parámetro reservado, se entrena con los otros cinco puntos, mientras el punto reservado aporta diez history-seeds disjuntas por clase y cinco seeds independientes de ruido de continuación.

Se evalúan por separado estos feature sets:

- solo trayectoria de state;
- trayectoria de state normalizada por L2;
- solo trayectoria de memory;
- solo trayectoria de pressure;
- state + memory + pressure concatenados y normalizados por L2.

Se aplica un null de permutación al readout primario conjunto normalizado LOPO.

Es un test de retención sin referencia. No establece consciencia, experiencia subjetiva, sentiencia ni ninguna afirmación fenomenológica.

</details>

<a id="english"></a>

# V43 — Reference-Free Temporal-History Decoding

V43 removes the V34–V42 reference-based readout entirely.

The system receives one of four paired history templates, then the future input is set exactly to zero for 60 steps. A classifier is asked to identify the historical template from the internal continuation alone.

The primary evaluation is leave-one-parameter-out (LOPO): each of the six blind parameter points is held out in turn. Within each held-out parameter, training uses the other five parameter points, while the held-out parameter contributes ten disjoint history seeds per class and five independent continuation-noise seeds.

Feature sets are evaluated separately:
- state trajectory only;
- L2-normalized state trajectory;
- memory trajectory only;
- pressure trajectory only;
- concatenated state + memory + pressure, L2-normalized.

A permutation null is applied to the primary joint-normalized LOPO readout.

This is a reference-free retention test. It does not establish consciousness, subjective experience, sentience, or any phenomenological claim.
