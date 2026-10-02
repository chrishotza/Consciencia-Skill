<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V41 — Transferencia de referencia entre pares históricos

V41 amplía V40 separando no solo el history seed concreto sino también el template history-pair utilizado para construir las continuaciones A/B de referencia.

Mapeo cíclico:

- test pair 0 → reference pair 1
- test pair 1 → reference pair 2
- test pair 2 → reference pair 3
- test pair 3 → reference pair 0

Los seeds de historia de prueba 160–169 y los de referencia 190–199 son disjuntos.

Se mantiene el readout reference-based signed-affinity. Permanecen iguales seis puntos ciegos, nueve contextos memory/pressure, radio 1.1, ángulos 30°/150°, input futuro cero y seeds de continuación disjuntas.

La inferencia se realiza sobre 40 bloques history-seed, con sign-flips estratificados por template test-pair y bootstrap estratificado.

## Interpretación

- persistencia apoyaría transferencia de la geometría de referencia angular entre templates history-pair;
- colapso indicaría que el efecto de referencia depende del matching del template histórico.

Sigue siendo un experimento de dinámica computacional y no establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V41 — Cross-Pair Reference Transfer

V41 extends V40 by separating not only the concrete history seed but also the history-pair template used to construct the A/B reference continuations.

Cyclic mapping:
test pair 0 -> reference pair 1
test pair 1 -> reference pair 2
test pair 2 -> reference pair 3
test pair 3 -> reference pair 0

Test history seeds 160–169 and reference history seeds 190–199 are disjoint.

The reference-based signed-affinity readout is retained. Six blind parameter points, nine memory/pressure contexts, radius 1.1, angles 30°/150°, exactly zero future input, and disjoint continuation seeds are unchanged.

Inference is performed at 40 history-seed blocks, with stratified sign flips by test-pair template and stratified bootstrap.

Interpretation:
- persistence would support transfer of the angular reference geometry across history-pair templates;
- collapse would indicate that the reference effect depends on matching the historical template.

This remains a computational dynamics experiment and does not establish consciousness or subjective experience.
