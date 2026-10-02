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

## Resultado verificado

Workflow de GitHub Actions: **36985957522**; artifact **11218020500**; commit experimental **60263ada3a28af29c3f1fa29246355bb434242fc**; seed **20261003**; **512** episodios.

Endpoints:

- target attention mass FULL: **0.9845638420**;
- FULL − SHUFFLED target mass: **+0.9768188958**, p **4.99975×10⁻⁵**;
- FULL − UNIFORM target mass: **+0.7345638420**, p **4.99975×10⁻⁵**;
- FULL − RANDOM target mass: **+0.7429394202**, p **4.99975×10⁻⁵**;
- FULL − LESION target mass: **+0.7345638420**, p **4.99975×10⁻⁵**;
- attention selection-change rate: **1.0**.

Interpretación: bajo este arnés sintético, el modelo de atención concentró de forma reproducible recursos sobre el módulo objetivo y esa concentración desapareció bajo los controles SHUFFLED, UNIFORM, RANDOM y la pérdida de concentración del controlador. El efecto verifica el mecanismo de asignación causal probado, no una atención autónoma del organismo completo.

## Límite científico

Es un test de mecanismo de asignación causal de atención. No demuestra consciencia, experiencia subjetiva ni una arquitectura completa de atención, y la condición LESION es una pérdida operacional de concentración del controlador, no una lesión anatómica o neuronal.

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

## Verified result

GitHub Actions workflow: **36985957522**; artifact **11218020500**; experimental commit **60263ada3a28af29c3f1fa29246355bb434242fc**; seed **20261003**; **512** episodes.

Endpoints:

- FULL target attention mass: **0.9845638420**;
- FULL − SHUFFLED target mass: **+0.9768188958**, p **4.99975×10⁻⁵**;
- FULL − UNIFORM target mass: **+0.7345638420**, p **4.99975×10⁻⁵**;
- FULL − RANDOM target mass: **+0.7429394202**, p **4.99975×10⁻⁵**;
- FULL − LESION target mass: **+0.7345638420**, p **4.99975×10⁻⁵**;
- attention selection-change rate: **1.0**.

Interpretation: under this synthetic harness, the attention model reproducibly concentrated resources on the target module, and that concentration disappeared under SHUFFLED, UNIFORM, RANDOM, and controller-concentration-loss controls. The effect verifies the tested allocation mechanism, not autonomous attention in the full organism.

## Scientific boundary

This is a causal attention-allocation mechanism test. It does not demonstrate consciousness, subjective experience, or a complete attention architecture; the LESION condition is an operational loss-of-concentration control rather than an anatomical or neuronal lesion.

</details>
