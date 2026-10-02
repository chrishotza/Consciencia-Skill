<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V64 — Persistencia de identidad bajo perturbación del self-model

## Hipótesis

Una firma dinámica interna vinculada a identidad puede persistir después de un overwrite semántico común del self-model y una ablación textual explícita.

## Diseño

24 réplicas emparejadas con dos etiquetas de identidad por réplica.

Encoding:
12 ciclos con self-model semántico específico de identidad y bridge ON.

Perturbación:
4 ciclos con el mismo self-model semántico común para ambas identidades.

Ablación:
se borra el texto SELF_MODEL actual, se deshabilita el semantic self-model bridge y se ejecutan 16 ciclos autónomos sin entrada semántica.

Evaluación:
clasificación logística leave-one-replicate-out entrenada con features numéricas previas a la perturbación y evaluada sobre features numéricas posteriores a la ablación.

## Controles

Bridge OFF repite la misma perturbación común sin permitir que el contenido semántico del self-model altere la dinámica numérica.

## Limitaciones

El provider es determinista y sintético. La clasificación demuestra decodificabilidad de una firma interna operacional, no identidad subjetiva ni consciencia fenomenológica.

</details>

<a id="english"></a>

# Evidence V64 — Identity persistence under self-model perturbation

## Hypothesis

An identity-linked internal dynamic signature can persist after a common semantic
self-model overwrite and explicit textual ablation.

## Design

24 paired replicates with two identity labels per replicate.

Encoding:
12 cycles with identity-specific semantic self-model and bridge ON.

Perturbation:
4 cycles with the same common semantic self-model for both identities.

Ablation:
current SELF_MODEL text cleared, semantic self-model bridge disabled, and 16
autonomous cycles run without semantic input.

Evaluation:
leave-one-replicate-out logistic classification trained on pre-perturbation numeric
features and tested on post-ablation numeric features.

## Controls

Bridge OFF repeats the same common perturbation without allowing semantic
self-model content to alter numerical dynamics.

## Limitations

The provider is deterministic and synthetic. Classification shows decodability of an
operational internal signature, not subjective identity or phenomenological
consciousness.
