# I5.3 — Causal Attention Allocation

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.3 separa la **asignación causal de atención** de la consulta discreta de I5.2.

La hipótesis es:

`estado global → modelo de atención → distribución de recursos → acceso selectivo`

El mecanismo produce una distribución continua de atención sobre cuatro módulos y usa esa distribución como intervención sobre el acceso computacional.

## Diseño

- cuatro módulos candidatos;
- un estado global bidimensional codifica el contexto relevante;
- `AttentionSchema` predice una distribución de atención;
- `AttentionSchema.allocate` convierte esa predicción en pesos de atención;
- el endpoint primario mide cuánta masa de atención cae sobre el módulo objetivo.

## Controles

- **FULL** — asignación guiada por el modelo de atención;
- **SHUFFLED** — distribución de atención reordenada;
- **UNIFORM** — recurso uniforme;
- **RANDOM** — distribución aleatoria;
- **LESION** — lesión del controlador, aproximada por pérdida de concentración.

## Endpoint primario

FULL menos SHUFFLED en **target attention mass**.

Endpoints secundarios:

- FULL menos UNIFORM;
- FULL menos RANDOM;
- FULL menos LESION;
- tasa de cambio de selección cuando cambia el estado global.

Se usan 512 episodios y 20.000 permutaciones sign-flip.

## Límite científico

Es un test de mecanismo de asignación causal de atención. No demuestra consciencia, experiencia subjetiva ni una arquitectura completa de atención.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.3 separates **causal attention allocation** from the discrete query mechanism in I5.2.

The hypothesis is:

`global state → attention model → resource distribution → selective access`

The mechanism produces a continuous attention distribution over four modules and uses that distribution as an intervention on computational access.

## Design

- four candidate modules;
- a two-dimensional global state encodes the relevant context;
- `AttentionSchema` predicts an attention distribution;
- `AttentionSchema.allocate` turns that prediction into attention weights;
- the primary endpoint measures how much attention mass falls on the target module.

## Controls

- **FULL** — allocation guided by the attention model;
- **SHUFFLED** — attention distribution reordered;
- **UNIFORM** — uniform resource allocation;
- **RANDOM** — random distribution;
- **LESION** — controller lesion, approximated by loss of concentration.

## Primary endpoint

FULL minus SHUFFLED **target attention mass**.

Secondary endpoints:

- FULL minus UNIFORM;
- FULL minus RANDOM;
- FULL minus LESION;
- selection-change rate when global state changes.

512 episodes and 20,000 sign-flip permutations are used.

## Scientific boundary

This is a causal attention-allocation mechanism test. It does not demonstrate consciousness, subjective experience, or a complete attention architecture.

</details>
