<a id="espanol"></a>

# V56 — Admisión de memoria compatible con el futuro

## Motivación

AEVUM define persistencia condicionada y memoria sin acumulación. V56 convierte ese principio en una política opcional de memoria del organismo.

## Política

Para cada memoria candidata:

- `coupling` es la superposición léxica con la memoria reciente más similar;
- `novelty = 1 - coupling`;
- `persistence` es la importancia declarada en [0,1];
- el operador AEVUM congelado decide si la candidata sigue siendo admisible.

El operador es:

`Omega = 1.2 * novelty - 1.0 * coupling - 0.8 * persistence`

`Omega > 0` significa admisible.

## Alcance

V56 deliberadamente no modifica el comportamiento predeterminado de memoria del organismo. Primero valida la política como adaptador determinista aislado.

## Por qué importa

El programa de consciencia no debería equiparar identidad con acumulación ilimitada. Un organismo persistente necesita una razón explícita para conservar una relación y un mecanismo igualmente explícito para permitir que material obsoleto o redundante se disuelva.

## Límite de evidencia

Este es un experimento de política de memoria. No establece consciencia.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V56 — Future-Compatible Memory Admission

## Motivation

AEVUM defines conditional persistence and non-accumulative memory. V56 turns that principle into an optional organism memory policy.

## Policy

For each candidate memory:

- coupling is lexical overlap with the most similar recent memory;
- novelty = 1 - coupling;
- persistence is declared importance in [0,1];
- the frozen AEVUM operator decides whether the candidate remains admissible.

The operator is:

Omega = 1.2 * novelty - 1.0 * coupling - 0.8 * persistence

Omega > 0 means admissible.

## Scope

V56 deliberately does not change the organism's default memory behavior. It first validates the policy as an isolated deterministic adapter.

## Why it matters

The consciousness program should not equate identity with unlimited accumulation. A persistent organism needs an explicit reason to retain a relation and an equally explicit mechanism for obsolete or redundant material to dissolve.

## Evidence boundary

This is a memory-policy experiment. It does not establish consciousness.

</details>