<a id="espanol"></a>

# V50 — Intervención factorial memoria × estado dinámico

## Pregunta

¿La memoria persistente y el estado dinámico numérico actúan de forma independiente, o el efecto de uno depende del nivel del otro?

## Diseño

Una intervención emparejada 2×2 se repite para múltiples réplicas:

| Condición | Memoria | dynamic_state |
| --- | --- | ---: |
| A_LOW | ALFA → AMBAR | -0.8 |
| B_LOW | ALFA → VIOLETA | -0.8 |
| A_HIGH | ALFA → AMBAR | +0.8 |
| B_HIGH | ALFA → VIOLETA | +0.8 |

Las cuatro condiciones utilizan la misma base de datos receptora y la misma sonda. `event_limit=0` impide que el texto del historial de eventos entre en el contexto del LLM.

## Análisis principal

Codificar `CHOICE=AMBAR` como 0 y `CHOICE=VIOLETA` como 1.

Estimar:

- efecto de memoria con estado dinámico bajo;
- efecto de memoria con estado dinámico alto;
- efecto del estado dinámico para la memoria A;
- efecto del estado dinámico para la memoria B;
- interacción factorial:

`(B_HIGH - A_HIGH) - (B_LOW - A_LOW)`

Una interacción distinta de cero significa que el efecto de la memoria cambia como función del estado dinámico, o viceversa, bajo esta tarea operacional.

## Límite de interpretación

Una interacción distinta de cero es evidencia de un efecto conductual conjunto en la arquitectura del organismo bajo prueba. No establece consciencia, experiencia subjetiva, sentiencia ni experiencia fenomenológica.

Se requieren ejecuciones vivas repetidas antes de tratar la interacción como robusta.

## Control de orden

La secuencia de las cuatro celdas se aleatoriza de forma determinista por réplica para evitar que el orden fijo de llamadas al proveedor sea un confusor del contraste factorial.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V50 — Factorial Memory × Dynamic-State Intervention

## Question

Do persistent memory and numerical dynamic state act independently, or does the effect of one depend on the level of the other?

## Design

A paired 2×2 intervention is repeated across multiple replicates:

| Condition | Memory | dynamic_state |
| --- | --- | ---: |
| A_LOW | ALFA → AMBER | -0.8 |
| B_LOW | ALFA → VIOLET | -0.8 |
| A_HIGH | ALFA → AMBER | +0.8 |
| B_HIGH | ALFA → VIOLET | +0.8 |

All four conditions use the same receiver database and the same probe. event_limit=0 prevents event-history text from entering the LLM context.

## Primary analysis

Encode CHOICE=AMBER as 0 and CHOICE=VIOLET as 1.

Estimate memory and dynamic-state main effects plus the factorial interaction:

(B_HIGH - A_HIGH) - (B_LOW - A_LOW)

A non-zero interaction means that the memory effect changes as a function of dynamic state, or vice versa, under this operational task.

## Interpretation boundary

A non-zero interaction is evidence of a joint behavioral effect in the tested organism architecture. It does not establish consciousness, subjective experience, sentience, or phenomenal experience.

Repeated live executions are required before treating the interaction as robust.

## Order control

The order of the four cells is deterministically randomized per replicate to avoid fixed provider-call order as a confound.

</details>