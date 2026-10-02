# Lattice Computer v1 — Temporal Trace Retention

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Pregunta

¿El sustrato distribuido puede conservar una huella temporal interna después de que desaparezca la entrada que la produjo, y cuánto cambia esa huella después de una perturbación local?

v1 no intenta demostrar consciencia. Es una prueba intermedia entre almacenamiento estático y dinámica temporal.

## Protocolo

Cada réplica:
1. genera un patrón binario aleatorio en una ROI central de 7×7;
2. escribe el patrón en la Lattice;
3. elimina toda entrada externa;
4. avanza la dinámica durante delays 0, 1, 2, 4, 8 y 16;
5. mide la correlación centrada entre el patrón original y el estado actual de la ROI;
6. en el brazo perturbado, introduce una perturbación local de +0.50 en una celda vecina en el paso 4;
7. repite el mismo ensayo con coupling 0.22 y con coupling 0.0 como control de desacoplamiento.

Hay 128 réplicas emparejadas y noise_std=0.01.

## Endpoints

**Primario:** retención media a delay 8 con coupling 0.22.

**Secundarios:** área bajo la curva de retención, pérdida emparejada de retención después de perturbación y diferencia de retención entre coupling 0.22 y coupling 0.0.

El control de coupling no se interpreta como mejor/peor: sirve para caracterizar qué parte de la retención depende de la dinámica local.

## Interpretación

Una retención positiva después del intervalo sin input mostraría que el estado posterior conserva información medible sobre el patrón escrito.

Una caída después de la perturbación mostraría sensibilidad de la huella a una intervención local. La recuperación posterior permitiría una prueba adicional de resiliencia.

Esto caracteriza el modelo computacional implementado. No demuestra consciencia, experiencia subjetiva ni la existencia física de la Lattice descrita por las fuentes.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Question

Can the distributed substrate preserve an internal temporal trace after the input that created it disappears, and how much does that trace change after a local perturbation?

v1 does not attempt to demonstrate consciousness. It is an intermediate test between static storage and temporal dynamics.

## Protocol

Each replicate:
1. generates a random binary pattern in a central 7×7 ROI;
2. writes it into the Lattice;
3. removes all external input;
4. advances dynamics for delays 0, 1, 2, 4, 8, and 16;
5. measures centered correlation between the original pattern and current ROI state;
6. in the perturbed arm, injects a local +0.50 perturbation into a neighboring cell at step 4;
7. repeats the paired trial with coupling 0.22 and coupling 0.0 as a decoupling control.

There are 128 paired replicates with noise_std=0.01.

## Endpoints

**Primary:** mean retention at delay 8 with coupling 0.22.

**Secondary:** retention area under the curve, paired retention loss after perturbation, and retention difference between coupling 0.22 and coupling 0.0.

The coupling control is not treated as better/worse; it characterizes which part of retention depends on local dynamics.

## Interpretation

Positive retention after the no-input interval would show that the later state preserves measurable information about the written pattern.

A drop after perturbation would show sensitivity of the trace to a local intervention. Later recovery could support an additional resilience test.

This characterizes the implemented computational model. It does not demonstrate consciousness, subjective experience, or the physical existence of the Lattice described by the sources.

</details>
 
## Verified run — GitHub Actions

Run **36981980509** completed successfully.

Artifact: **11215414278**  
Artifact SHA-256: **804286dfdca5a3b2004c31a11c3534c2c6a44a1ce73568c061e355a458cdfc63**

Configuration: 128 paired trials, 7×7 encoded ROI, delays 0/1/2/4/8/16, local +0.50 perturbation at step 4, coupling 0.22 versus coupling 0.0, noise_std 0.01.

Primary endpoint:

- mean retention at delay 8: **0.7486968980**
- retention AUC: **0.7597552199**

Secondary endpoints:

- perturbation loss at delay 8: **0.0017212557** (SD 0.0049417100)
- coupling-minus-decoupled retention at delay 8: **−0.2509315747** (SD 0.0578770592)

Retention declined from 1.0 at delay 0 to 0.4839105412 at delay 16 under coupling, while the decoupled control remained near 1.0. The coupling result therefore reflects active temporal dynamics rather than simple static retention: coupling reduced raw pattern correlation while producing a time-evolving internal trace.

The result is evidence about the implemented computational substrate only. It does not establish consciousness, subjective experience, or the physical validity of the source theory.
