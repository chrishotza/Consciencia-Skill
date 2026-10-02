# Lattice Computer v0 — Distributed Computational Substrate

<details>
<summary>🇪🇸 Español — abrir</summary>

## Base de la hipótesis

En *La Teoría Sintérgica*, Jacobo Grinberg-Zylberbaum describe la Lattice como una estructura del espacio capaz de contener información y cuya organización/coherencia se relaciona con la experiencia. En la página impresa 86, dentro de "Repercusiones prácticas", propone utilizar esa estructura como base de sistemas de computación capaces de almacenar información y realizar operaciones de análisis y cómputo.

En *Las Manifestaciones del Ser*, vuelve a describir el continuo espacio-materia en términos de organización de información y relaciona la interacción entre campos neuronales y la estructura sintérgica con la experiencia.

Estos pasajes se usan aquí como **fuente de hipótesis de ingeniería**, no como validación experimental de una física de la Lattice.

## Traducción computacional v0

Lattice Computer v0 representa la Lattice como un campo 2D localmente acoplado.

Cada célula contiene un estado continuo x[i,j].

La dinámica usa:

- estado local;
- vecinos inmediatos;
- entrada externa local;
- no linealidad;
- fuga;
- ruido opcional.

No existe conectividad global directa. La propagación se produce mediante interacciones locales.

## Qué implementa

1. Almacenamiento distribuido.
2. Computación de operaciones booleanas dentro de la estructura.
3. Dinámica local recurrente.
4. Medición operacional de coherencia.
5. Medición operacional de redundancia espacial.
6. Lesión causal de regiones.
7. Serialización y restauración exacta.

## Primer protocolo

experiments/lattice_v0.py no intenta demostrar consciencia.

Mide:

- fidelidad de almacenamiento/computación;
- propagación causal de una perturbación;
- diferencia entre Lattice acoplada y desacoplada;
- efecto de una lesión regional;
- retención dinámica;
- coherencia y redundancia.

La primera pregunta es deliberadamente básica:

> ¿Puede una estructura distribuida almacenar y transformar información localmente, y cambia su organización medible cuando se elimina su acoplamiento?

## Próximas extensiones

### Lattice-1
Memoria temporal y retención bajo perturbación.

### Lattice-2
Mapa de influencia causal entre regiones.

### Lattice-3
Observador de la propia Lattice y modelo de segundo orden.

### Lattice-4
Factor de direccionalidad operacionalizado como atención/asignación de recursos.

### Lattice-5
Integración con PersistentOrganism, reinicio y ablación.

### Lattice-6
Cruce con I4/I5: metacognición de la fiabilidad de regiones internas.

</details>

<details>
<summary>🇺🇸 English — open</summary>

## Hypothesis basis

In *La Teoría Sintérgica*, Jacobo Grinberg-Zylberbaum describes the Lattice as a structure of space capable of containing information whose organization/coherence is related to experience. On printed page 86, in "Repercusiones prácticas," he proposes using that structure as a basis for computing systems able to store information and perform analysis and computation.

In *Las Manifestaciones del Ser*, he again describes the space-matter continuum in terms of information organization and relates the interaction between neural fields and the syntergic structure to experience.

These passages are used here as **engineering-hypothesis sources**, not as experimental validation of a physical Lattice.

## v0 computational translation

Lattice Computer v0 represents the Lattice as a locally coupled 2D field.

Each cell contains a continuous state x[i,j].

The dynamics use:

- local state;
- immediate neighbors;
- local external input;
- nonlinearity;
- leak;
- optional noise.

There is no direct global connectivity. Propagation occurs through local interactions.

## What it implements

1. Distributed storage.
2. Boolean computation inside the structure.
3. Local recurrent dynamics.
4. An operational coherence measure.
5. A spatial redundancy measure.
6. Causal regional lesions.
7. Exact serialization and restoration.

## First protocol

experiments/lattice_v0.py does not attempt to demonstrate consciousness.

It measures:

- storage/computation fidelity;
- causal perturbation spread;
- coupled versus decoupled Lattice behavior;
- regional lesion effects;
- dynamic retention;
- coherence and redundancy.

The deliberately basic first question is:

> Can a distributed structure store and transform information locally, and does its measurable organization change when its coupling is removed?

## Next extensions

### Lattice-1
Temporal memory and retention under perturbation.

### Lattice-2
Causal influence mapping between regions.

### Lattice-3
An observer of the Lattice itself and a second-order model.

### Lattice-4
Directionality operationalized as attention/resource allocation.

### Lattice-5
Integration with PersistentOrganism, restart, and ablation.

### Lattice-6
Crossing with I4/I5: metacognitive modeling of the reliability of internal regions.

</details>

## Source boundary

The source text is treated as historical/theoretical input. Experimental results from this branch describe only the implemented computational model and its controls.


## Verified run — GitHub Actions

Run **36977088882** completed successfully from commit **15af73518f2a0761c8f37e137772778a0a5b3a26**.

Artifact: **lattice-computer-v0-5ed28ec2622764bb183501726b5e7ebd89078d8d**  
Artifact ID: **11213079445**  
SHA-256: **1a7b9560aa4bf166d39a715c9e1807bbbd94b8b435bc394a83d60929b38dc658**

Parameters: size 16; bit width 12; 64 trials; 12 dynamic steps.

Measured results:

| Observable | Result |
|---|---:|
| XOR accuracy | **1.0** |
| Coupled − decoupled perturbation-spread delta | **0.0481567383** |
| Lesion mean absolute effect | **0.0238895653** |
| Coupled mean retention | **0.5475138436** |
| Decoupled mean retention | **1.0000000000** |
| Coupled mean coherence | **0.9730625127** |
| Decoupled mean coherence | **0.6094002602** |
| Coupled mean redundancy | **0.9562321010** |
| Decoupled mean redundancy | **−0.0128536083** |

The retention result is intentionally not interpreted as a simple coupling-improves-memory effect: the matched control shows higher raw retention under decoupling, while coupling produces substantially higher coherence/redundancy and measurable perturbation spread. The protocol therefore establishes that coupling changes the computational organization; it does not establish that coupling is globally beneficial.

The artifact contains manifest.json and summary.json.

The scientific boundary remains unchanged: this is evidence about the implemented computational substrate, not validation of the physical claims of Syntergic Theory and not evidence of subjective consciousness.
