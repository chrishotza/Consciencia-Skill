# I5.0 — Bounded Global Workspace

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.0 introduce el primer mecanismo explícito de workspace global acotado en Skill-Conscious.

Prueba tres propiedades arquitectónicas que hoy faltan en el programa: capacidad limitada, selección competitiva y broadcast global causal.

## Diseño

Seis módulos producen vectores locales. El workspace selecciona los 2 contenidos más salientes, construye un contenido global ponderado y lo retransmite a todos los módulos.

Hay un control sin broadcast y un control con capacidad ilimitada de 6 módulos.

Cada episodio contiene una señal relevante oculta en un módulo y distractores en los demás. Las mismas entradas se reutilizan en todas las condiciones emparejadas.

## Endpoints

Primario: FULL menos NO_BROADCAST en accuracy emparejada.

Secundarios: BOUNDED(K=2) menos UNBOUNDED(K=6), y lesión de origen seleccionado menos lesión de origen no seleccionado.

La inferencia usa sign-flip emparejado con 20.000 permutaciones.

## Límite

Un resultado positivo demostraría una propiedad computacional del workspace implementado. No demostraría experiencia subjetiva ni que un workspace global sea suficiente para consciencia.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.0 introduces the first explicit bounded global-workspace mechanism in Skill-Conscious.

It tests three architectural properties currently missing from the program: limited capacity, competitive selection, and causal global broadcast.

## Design

Six modules produce local vectors. The workspace selects the 2 most salient contents, builds a weighted global content, and broadcasts it to all modules.

A no-broadcast control and an unlimited-capacity control using all 6 modules are included.

Each episode contains a hidden relevant signal in one module and distractors in the others. Exactly the same paired inputs are reused across conditions.

## Endpoints

Primary: paired FULL minus NO_BROADCAST accuracy.

Secondary: BOUNDED(K=2) minus UNBOUNDED(K=6), and selected-source lesion minus non-selected-source lesion.

Inference uses paired sign-flip with 20,000 permutations.

## Boundary

A positive result would demonstrate a computational property of the implemented workspace. It would not demonstrate subjective experience or sufficiency of a global-workspace architecture for consciousness.

</details>
 
## Verified result

GitHub Actions run **36982788159** completed successfully.

Artifact: **11216003264**  
Artifact SHA-256: **de542f6a858eacfc67f88bf138a8fe9c94dcf34bf89d85446b69015ef51ec799**

Configuration: 6 modules, 2-dimensional vectors, bounded capacity **K=2**, unlimited-capacity control **K=6**, 512 paired episodes.

| Endpoint | Result |
|---|---:|
| Broadcast accuracy advantage (FULL − NO_BROADCAST) | **+0.126953125**, p **4.99975×10⁻⁵** |
| Bounded − unbounded accuracy | **+0.017578125**, p **0.0222489** |
| Selected-source lesion − unselected-source lesion | **−0.490234375**, p **4.99975×10⁻⁵** |

The result verifies the intended computational properties of the prototype under the synthetic task: global broadcast adds measurable information, the bounded K=2 configuration differs from unrestricted access, and lesioning the selected source has a larger directional effect than lesioning an unselected source.

The experiment remains a **synthetic architecture test**. It does not establish consciousness or subjective experience, and it does not yet demonstrate that these mechanisms causally organize the full PersistentOrganism runtime.
