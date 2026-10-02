<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V59 — Resultado

## Run

- workflow: organism-semantic-self-model-v59
- run: 36804592335
- artifact: organism-semantic-self-model-v59
- replicates: 24
- candidates: {-1.0, +1.0}
- provider: deterministic fake provider

## Resultado primario

La ventaja de selección del self-model fue esencialmente idéntica entre condiciones bridge.

| Métrica | Bridge OFF | Bridge ON |
|---|---:|---:|
| Self-model mean regret | 0.00000 | 0.00000 |
| Random mean regret | 0.23233 | 0.24022 |
| Self-model oracle hit | 100% | 100% |
| Random oracle hit | 50% | 50% |

La ventaja de selección fue 0.23233 OFF y 0.24022 ON. La interacción factorial fue +0.0078888 con sign-flip p = 0.839408.

## Efecto semántico

El semantic bridge todavía produjo un cambio interno grande:

- diferencia absoluta media del estado post-wake, ON vs OFF: 0.94273;
- diferencia absoluta media de señal semántica, ON vs OFF: 0.55376.

La intervención semántica cambió materialmente el estado interno numérico bajo el arnés probado, mientras que la ventaja de selección del self-model medida permaneció estable.

## Interpretación

V59 debe tratarse como un resultado nulo de interacción/composición.

El experimento reproduce la ventaja de selección del self-model en ambos estados del bridge y confirma que el semantic bridge puede desplazar la dinámica interna sin modificar de forma medible esa ventaja bajo este protocolo determinista.

No establece consciencia fenomenológica, experiencia subjetiva ni ninguna afirmación sobre un LLM externo real. El provider utilizado es determinista y sintético.

</details>

<a id="english"></a>

# Evidence V59 — Result

## Run

- workflow: organism-semantic-self-model-v59
- run: 36804592335
- artifact: organism-semantic-self-model-v59
- replicates: 24
- candidates: {-1.0, +1.0}
- provider: deterministic fake provider

## Primary result

The self-model selection advantage was essentially identical across bridge conditions.

| Metric | Bridge OFF | Bridge ON |
|---|---:|---:|
| Self-model mean regret | 0.00000 | 0.00000 |
| Random mean regret | 0.23233 | 0.24022 |
| Self-model oracle hit | 100% | 100% |
| Random oracle hit | 50% | 50% |

Selection advantage was 0.23233 OFF and 0.24022 ON. Their factorial interaction was +0.0078888 with sign-flip p = 0.839408.

## Semantic effect

The semantic bridge still produced a large internal change:

- mean absolute post-wake state difference, ON vs OFF: 0.94273;
- mean absolute semantic signal difference, ON vs OFF: 0.55376.

Thus the semantic intervention materially changed the internal numeric state in the tested harness, while the measured self-model selection advantage remained stable.

## Interpretation

V59 is best treated as a null interaction / compositionality result.

The experiment reproduces the self-model trajectory-selection advantage under both bridge states and confirms that the semantic bridge can shift internal dynamics without measurably changing that selection advantage in this deterministic protocol.

The result does not establish phenomenological consciousness, subjective experience, or any claim about a real external LLM. The provider used here is deterministic and synthetic.
