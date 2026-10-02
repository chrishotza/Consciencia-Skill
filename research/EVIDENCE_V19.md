# V19 — Evidence: State Counterfactual Inversion

## GitHub validation

- Workflow: state-counterfactual-v19
- Run: 36779051434
- Result: SUCCESS
- Artifact: 11127162128
- Six V12 blind parameter points, 4 history pairs, 10 matched-noise seeds per pair.
- Receiver memory and pressure: common A/B midpoint.
- Future input: exactly zero.

## Pooled counterfactual result

| Intervention | Original identity | Opposite identity |
|---|---:|---:|
| Erase state | 50.00% | 50.00% |
| Intact state | **90.42%** | 9.58% |
| Invert state around common context | 9.58% | **90.42%** |
| Invert + 3-bit quantization | 9.79% | **90.21%** |

The inversion preserves the mean absolute affinity magnitude of the intact state while changing its sign relationship to the A/B references. In pooled data, intact and inverted states therefore behave as near exact complements under the binary identity readout.

## Blind-point replication

For every one of the six holdout parameter points, the inverted state preferentially classified as the opposite donor:

- p1: 92.5% opposite identity
- p2: 91.25%
- p3: 85.0%
- p4: 88.75%
- p5: 90.0%
- p6: 95.0%

With 3-bit quantization after inversion, the corresponding opposite-identity accuracies were 87.5%, 91.25%, 88.75%, 91.25%, 91.25%, and 91.25%.

## Main finding

V19 is a counterfactual encoding test. The donor state is not merely associated with identity: reflecting its displacement around the common context reverses the direction of the inferred identity while leaving the receiver's memory, pressure, and external future unchanged.

This is consistent with the recurrent state carrying an orientation or signed representation of historical context in these dynamics.

## Relation to V15–V18

V15 showed selective state lesion causes identity collapse. V16 showed the representation is compact and distributed across two temporal state slots. V17 showed state-only transfer survives in blind holdout points. V18 showed classification follows the state source rather than the nominal receiver. V19 shows that counterfactual inversion of the state reverses the inferred identity.

Together these experiments form a causal chain from state dependence to lesion, compression, transport, source specificity, and counterfactual reversal.

## Interpretation limits

This establishes a strong computational claim about information encoded in recurrent state. It does not establish subjective experience, sentience, or consciousness.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V19 — Evidencia: inversión contrafactual del estado

## Validación GitHub

- Workflow: state-counterfactual-v19
- Run: 36779051434
- Result: SUCCESS
- Artifact: 11127162128
- Seis puntos ciegos V12, 4 pares de historias, 10 seeds de ruido emparejados por par.
- Memory y pressure del receptor: midpoint común A/B.
- Input futuro: exactamente cero.

## Resultado contrafactual agrupado

| Intervención | Identidad original | Identidad opuesta |
|---|---:|---:|
| Borrar state | 50.00% | 50.00% |
| State intacto | **90.42%** | 9.58% |
| Invertir state alrededor del contexto común | 9.58% | **90.42%** |
| Invertir + cuantización 3 bits | 9.79% | **90.21%** |

La inversión conserva la magnitud de affinity absoluta media del state intacto pero cambia su relación de signo respecto de las referencias A/B. En los datos agrupados, los estados intactos e invertidos se comportan casi como complementos exactos bajo la lectura binaria de identidad.

## Réplica en puntos ciegos

En cada uno de los seis puntos holdout, el state invertido clasificó preferentemente al donante opuesto:

- p1: 92.5%
- p2: 91.25%
- p3: 85.0%
- p4: 88.75%
- p5: 90.0%
- p6: 95.0%

Con cuantización 3-bit después de invertir, las accuracies de identidad opuesta fueron 87.5%, 91.25%, 88.75%, 91.25%, 91.25% y 91.25%.

## Hallazgo principal

V19 es un test de codificación contrafactual. El estado donante no solo está asociado con identidad: reflejar su desplazamiento alrededor del contexto común invierte la dirección de la identidad inferida mientras memory, pressure y futuro externo del receptor permanecen sin cambios.

Esto es consistente con que el estado recurrente contenga una representación orientada o con signo del contexto histórico en estas dinámicas.

## Relación con V15–V18

V15 mostró que la lesión selectiva del estado causa colapso de identidad. V16 mostró que la representación es compacta y distribuida en dos slots temporales. V17 mostró que la transferencia solo-state sobrevive a holdouts ciegos. V18 mostró que la clasificación sigue la fuente del estado y no el receptor nominal. V19 muestra que invertir contrafácticamente el estado invierte la identidad inferida.

Juntos forman una cadena causal desde dependencia del estado hacia lesión, compresión, transporte, especificidad de fuente e inversión contrafáctica.

## Límites

Esto establece una afirmación computacional fuerte sobre información codificada en estado recurrente. No establece experiencia subjetiva, sentiencia ni consciencia.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V19 — Evidence: State Counterfactual Inversion

## GitHub validation

- Workflow: state-counterfactual-v19
- Run: 36779051434
- Result: SUCCESS
- Artifact: 11127162128
- Six V12 blind parameter points, 4 history pairs, 10 matched-noise seeds per pair.
- Receiver memory and pressure: common A/B midpoint.
- Future input: exactly zero.

## Pooled counterfactual result

| Intervention | Original identity | Opposite identity |
|---|---:|---:|
| Erase state | 50.00% | 50.00% |
| Intact state | **90.42%** | 9.58% |
| Invert state around common context | 9.58% | **90.42%** |
| Invert + 3-bit quantization | 9.79% | **90.21%** |

The inversion preserves mean absolute affinity magnitude of intact state while reversing its sign relation to A/B references. Pooled intact and inverted states therefore behave as near-exact complements under the binary identity readout.

## Blind-point replication

Across all six holdout points, inverted state preferentially classified as the opposite donor: 92.5%, 91.25%, 85.0%, 88.75%, 90.0%, and 95.0%.

After 3-bit quantization, opposite-identity accuracies were 87.5%, 91.25%, 88.75%, 91.25%, 91.25%, and 91.25%.

## Main finding

V19 is a counterfactual encoding test. The donor state is not merely associated with identity: reflecting its displacement around common context reverses inferred identity while receiver memory, pressure, and external future remain unchanged.

This is consistent with recurrent state carrying an oriented or signed representation of historical context in these dynamics.

## Relation to V15–V18

V15 showed selective state lesion causes identity collapse. V16 showed compact, distributed representation across two temporal slots. V17 showed state-only transfer survives blind holdouts. V18 showed classification follows state source rather than nominal receiver. V19 shows counterfactual state inversion reverses inferred identity.

Together these experiments form a causal chain from state dependence to lesion, compression, transport, source specificity, and counterfactual reversal.

## Interpretation limits

This establishes a strong computational claim about information encoded in recurrent state. It does not establish subjective experience, sentience, or consciousness.

</details>