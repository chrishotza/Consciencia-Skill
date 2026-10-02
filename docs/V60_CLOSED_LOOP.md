<a id="espanol"></a>

# V60 — Bucle cerrado de feedback semántico

## Pregunta

¿Puede el organismo cerrar un bucle computacional recurrente en el que una trayectoria interna seleccionada modifica la siguiente memoria semántica, esa memoria semántica se vuelve a transducir hacia la dinámica interna y el estado resultante se convierte en la base de la siguiente selección de trayectoria?

## Resultado

El artefacto de CI exitoso contiene 24 réplicas emparejadas con 24 ciclos de evaluación.

- regret medio del modelo de sí: **-0.0842091465**;
- regret medio del control aleatorio: **0.3028308773**;
- ventaja del modelo de sí: **0.3870400237** unidades de regret;
- ventaja acumulada: **9.2889605698**;
- p emparejada por cambio de signo: **0.00005**;
- tasa de aciertos del oráculo del modelo de sí: **96.1806%**;
- tasa de aciertos del control aleatorio: **45.3125%**.

El resultado muestra que el selector basado en el modelo de sí conserva una utilidad funcional fuerte en el protocolo recurrente mientras la siguiente memoria semántica queda condicionada por la acción seleccionada previamente.

## Limitación importante

El brazo con modelo de sí seleccionó `+1` en las 24 réplicas. En consecuencia, el endpoint secundario dentro de cada ejecución que compara señales del puente semántico después de acciones negativas frente a positivas tuvo **cero ejecuciones con ambas ramas de acción**.

El bucle fue ejercitado, pero el experimento no proporcionó cobertura equilibrada y bidireccional de acciones en el brazo con modelo de sí. Por lo tanto, V60 respalda el acoplamiento causal recurrente del sistema y la selección funcional mediante modelo de sí dentro de este arnés, pero no establece un efecto bidireccional de feedback condicionado por la acción.

## Bucle

El protocolo determinista cierra:

```
selección mediante modelo de sí / aleatoria
        │
        ▼
trayectoria seleccionada
        │
        ▼
estado de evento persistente
        │
        ▼
siguiente memoria semántica
        │
        ▼
continuidad / puente semántico
        │
        ▼
estado dinámico interno
        │
        ▼
autoobservador
        │
        └──────────────↺
```

## Límite de evidencia

V60 es un experimento operacional de sistemas. Su proveedor es determinista y sintético. El resultado se refiere a selección computacional y acoplamiento recurrente de estados, no a consciencia fenomenológica ni experiencia subjetiva.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V60 — Closed-Loop Semantic Feedback

## Question

Can the organism close a recurrent computational loop in which a selected internal trajectory changes the next semantic memory, that semantic memory is transduced back into internal dynamics, and the resulting state becomes the basis for the next trajectory selection?

## Result

The successful CI artifact contains 24 paired replicates with 24 evaluation cycles.

- mean self-model regret: **-0.0842091465**;
- mean random-control regret: **0.3028308773**;
- self-model advantage: **0.3870400237** regret units;
- cumulative advantage: **9.2889605698**;
- paired sign-flip p-value: **0.00005**;
- self-model oracle hit rate: **96.1806%**;
- random-control oracle hit rate: **45.3125%**.

The result shows that the self-model selector retained strong functional utility in the recurrent protocol while the next semantic memory was conditioned by the previously selected action.

## Important limitation

The self-model arm selected +1 in all 24 replicates. Consequently, the within-run secondary endpoint comparing semantic-bridge signals after negative versus positive actions had **zero runs containing both action branches**.

The loop was exercised, but the experiment did not provide balanced bidirectional action coverage in the self-model arm. Therefore V60 supports recurrent causal coupling and functional self-model selection within this harness, but does not establish a bidirectional action-conditioned feedback effect.

## Loop

The deterministic protocol closes:

self-model / random selection
        ↓
selected trajectory
        ↓
persistent event state
        ↓
next semantic memory
        ↓
continuity / semantic bridge
        ↓
internal dynamic state
        ↓
self-observer
        ↺

## Evidence boundary

V60 is an operational systems experiment. Its provider is deterministic and synthetic. The result concerns computational selection and recurrent state coupling, not phenomenal consciousness or subjective experience.

</details>