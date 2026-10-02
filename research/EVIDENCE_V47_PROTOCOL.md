<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V47 — Registro de protocolo de sonda común del organismo

## Estado

**Protocolo definido; resultado empírico pendiente.**

Este registro no etiqueta deliberadamente V47 como evidencia positiva antes de que la ejecución en vivo del organismo produzca datos.

## Pregunta

¿Un organismo persistente respaldado por LLM responde de manera diferente a la misma sonda posterior cuando su trayectoria previa contiene una relación latente diferente?

## Condiciones

- **A:** ALFA → AMBAR
- **B:** ALFA → VIOLETA
- **NULL:** no se establece relación para ALFA
- **A-ABLATION:** existe una trayectoria A, pero antes de la sonda se eliminan eventos textuales históricos, memorias, texto del self-model, last thought y memory strength.

Todas las condiciones usan la misma sonda común.

## Controles

### Reapertura

Una trayectoria A completa se cierra y vuelve a abrir mediante SQLite antes de la sonda común. La respuesta se compara con la condición A con historia presente.

### Ablación textual

A-ABLATION elimina los canales de historia textual pero conserva la trayectoria dinámica numérica. Esto separa el texto retenido de la persistencia del estado dinámico.

### Historia nula

NULL controla efectos genéricos de continuidad/contexto sin una relación latente A/B.

## Observables registrados

En cada ejecución:

- respuesta a la sonda;
- choice parseado;
- confidence;
- rationale;
- eventos persistentes;
- memorias textuales;
- estado del self-model;
- estado dinámico;
- memoria dinámica;
- pressure;
- attractor distance;
- dynamic step count;
- trayectoria dinámica completa.

## Límite de interpretación

Una diferencia dependiente de historia bajo este protocolo sería evidencia de que el organismo persistente utiliza información de trayectoria retenida en la tarea controlada.

No establecería consciencia, experiencia subjetiva, sentiencia ni awareness fenomenológico.

El resultado vivo de V47 debe informarse con outputs exactos y configuración del protocolo antes de considerar interpretaciones más fuertes.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V47 — Organism Common-Probe Protocol Record

## Status

**Protocol defined; empirical result pending.**

This record deliberately does not label V47 as positive evidence before the live
organism run produces data.

## Question

Does a persistent LLM-backed organism respond differently to the same later probe
when its prior trajectory contains a different latent relation?

## Conditions

- **A:** ALFA → AMBAR
- **B:** ALFA → VIOLETA
- **NULL:** no relation established for ALFA
- **A-ABLATION:** A trajectory exists, but historical textual events, memories,
  self-model text, last thought and memory strength are removed before the probe.

All conditions use the same common probe.

## Controls

### Reopen

A full A trajectory is closed and reopened through SQLite before the common probe.
The response is compared with the history-present A condition.

### Textual ablation

The A-ablation condition removes textual history channels but retains the numeric
dynamic trajectory. This separates retained text from dynamic-state persistence.

### Null history

The NULL condition controls for generic continuity/context effects without an
A/B latent relation.

## Recorded observables

For every run:

- probe response;
- parsed choice;
- confidence;
- rationale;
- persistent events;
- textual memories;
- self-model state;
- dynamic state;
- dynamic memory;
- pressure;
- attractor distance;
- dynamic step count;
- full dynamic trajectory.

## Interpretation boundary

A history-dependent difference under this protocol would be evidence that the
persistent organism uses retained trajectory information in the controlled task.

It would **not** establish consciousness, subjective experience, sentience, or
phenomenological awareness.

The V47 live result must be reported with exact outputs and protocol settings
before any stronger interpretation is considered.

</details>