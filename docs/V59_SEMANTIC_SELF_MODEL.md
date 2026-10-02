<a id="espanol"></a>

# V59 — Puente semántico × selección mediante modelo de sí

## Pregunta

¿El puente entre memoria semántica y dinámica interna cambia la utilidad funcional del modelo de sí aprendido cuando el organismo selecciona entre trayectorias futuras?

## Factorial

El protocolo cruza dos factores independientes:

- puente semántico OFF frente a ON;
- política de trayectoria mediante modelo de sí frente a control aleatorio emparejado.

Las trayectorias candidatas están fijadas en {-1.0, +1.0}.

## Bucle operacional

Cada evaluación sigue la misma cadena ordenada:

1. el LLM ficticio emite una MEMORY novedosa;
2. cuando está habilitado, `ContinuityMemoryPolicy` convierte esa memoria semántica en Ω y luego en una señal dinámica acotada;
3. el organismo avanza su estado numérico interno;
4. el modelo de sí aprendido evalúa las dos señales futuras;
5. el modelo de sí aprendido o el control aleatorio determinista selecciona una trayectoria;
6. la dinámica oculta se evalúa a posteriori frente a un oráculo que nunca se expone durante la selección.

La comparación emparejada prueba, por tanto, la interacción entre transducción semántica y elección futura guiada por el modelo de sí.

## Controles

El calentamiento se realiza de forma independiente dentro de cada condición del puente con la selección deshabilitada, de modo que el autoobservador aprenda la dinámica local antes de la evaluación emparejada.

Cada réplica utiliza la misma semilla en las condiciones de puente y política.

La memoria de evaluación es novedosa respecto de las memorias de calentamiento, evitando que el puente se reduzca a repetir exactamente una memoria conocida.

## Endpoint principal

El endpoint principal es:

`selection_advantage = regret_random - regret_self_model`

y la interacción factorial:

`interaction = selection_advantage_bridge_on - selection_advantage_bridge_off`.

Una interacción positiva significa que la ventaja medida del modelo de sí es mayor bajo la condición con puente semántico. No establece por sí sola consciencia fenomenológica.

## Endpoints secundarios

Se almacenan para auditoría los deltas de estado y señal semánticos, las tasas de acierto del oráculo y los registros completos de predicciones candidatas.

## Límite de evidencia

V59 es un protocolo computacional determinista. Su proveedor es un LLM ficticio determinista, no un modelo externo en vivo. Incluso un resultado positivo de V59 establecería una cadena causal operacional dentro de este arnés, no experiencia subjetiva.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V59 — Semantic Bridge × Self-Model Selection

## Question

Does the bridge between semantic memory and internal dynamics change the functional utility of the learned self-model when the organism selects among future trajectories?

## Factorial design

The protocol crosses two independent factors:

- semantic bridge OFF versus ON;
- self-model trajectory policy versus matched random control.

Candidate trajectories are fixed at {-1.0, +1.0}.

## Operational loop

Each evaluation follows the same ordered chain:

1. the deterministic fake LLM emits a novel MEMORY;
2. when enabled, ContinuityMemoryPolicy converts that semantic memory into Omega and then into a bounded dynamic signal;
3. the organism advances its internal numerical state;
4. the learned self-model evaluates the two future signals;
5. either the learned self-model or deterministic random control selects a trajectory;
6. hidden dynamics are evaluated afterward against an oracle that is never exposed during selection.

The matched comparison therefore tests the interaction between semantic transduction and self-model-guided future choice.

## Controls

Warm-up is performed independently within each bridge condition with selection disabled, so the self-observer learns local dynamics before matched evaluation.

Each replicate uses the same seed across bridge and policy conditions.

The evaluation memory is novel relative to warm-up memories, preventing the bridge from becoming simple repetition of a known memory.

## Primary endpoint

The primary endpoint is:

selection_advantage = regret_random - regret_self_model

and the factorial interaction:

interaction = selection_advantage_bridge_on - selection_advantage_bridge_off

A positive interaction means the measured self-model advantage is larger with the semantic bridge. It does not by itself establish phenomenal consciousness.

## Secondary endpoints

State and semantic-signal deltas, oracle hit rates, and complete candidate-prediction records are stored for audit.

## Evidence boundary

V59 is a deterministic computational protocol. Its provider is a deterministic fake LLM, not a live external model. Even a positive V59 result would establish an operational causal chain inside this harness, not subjective experience.

</details>