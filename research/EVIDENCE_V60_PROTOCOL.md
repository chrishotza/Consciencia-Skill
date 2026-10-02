<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V60 — Feedback semántico en bucle cerrado

## Hipótesis

El organismo debería poder mantener un loop recurrente en el que su trayectoria seleccionada se persiste como estado, influye en la siguiente memory semántica y esa memory semántica se convierte nuevamente en dinámica interna antes de la siguiente selección de trayectoria.

## Diseño

Cada réplica:

1. construye una historia warmup emparejada con semantic bridge habilitado y self-selection deshabilitada;
2. clona el mismo estado persistente en un brazo self-model y uno random;
3. ejecuta ciclos repetidos wake → semantic bridge → selección autónoma;
4. utiliza el mismo seed y conjunto candidato {-1, +1} en ambos brazos;
5. evalúa cada trayectoria seleccionada contra un oracle post hoc que nunca participa de la selección.

El provider sintético lee la última acción autónoma persistida y emite una memory semántica determinista asociada a esa acción. La memory entra luego en ContinuityMemoryPolicy y en el semantic dynamic bridge.

## Medida primaria

Regret inmediato medio:

actual_distance - oracle_distance

y ventaja emparejada del self-model:

regret_random - regret_self_model.

## Medida secundaria

Diferencia del feedback signal dentro de la ejecución entre ciclos posteriores a acciones negativas y positivas.

No es un efecto causal aislado formal porque historia de acciones y estado interno coevolucionan dentro del loop cerrado.

## Limitaciones

El provider es determinista y sintético. El protocolo no prueba fenomenología, autoinformes subjetivos ni comportamiento de un LLM externo real.

</details>

<a id="english"></a>

# Evidence V60 — Closed-loop semantic feedback

## Hypothesis

The organism should be able to maintain a recurrent loop in which its selected trajectory is persisted as state, influences the next semantic memory, and that semantic memory is converted back into the organism's internal dynamics before the next trajectory selection.

## Design

Each replicate:

1. constructs a matched warmup history with semantic bridge enabled and self-selection disabled;
2. clones the same persistent state into a self-model arm and a random-control arm;
3. runs repeated wake → semantic bridge → autonomous selection cycles;
4. uses the same seed and candidate set {-1, +1} in both arms;
5. evaluates each selected trajectory against a post-hoc oracle that never participates in selection.

The synthetic provider reads the latest persisted autonomous action and emits a deterministic semantic memory associated with that action. The memory then enters the ContinuityMemoryPolicy and semantic dynamic bridge.

## Primary measure

Mean immediate regret:

`actual_distance - oracle_distance`

and paired self-model advantage:

`regret_random - regret_self_model`.

## Secondary measure

Within-run feedback signal difference between cycles following negative and positive actions.

This is not a formal isolated causal effect because action history and internal state co-evolve over the closed loop.

## Limitations

The provider is deterministic and synthetic. The protocol does not test phenomenology, subjective reports, or real external LLM behavior.